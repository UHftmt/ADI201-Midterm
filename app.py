from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from flask import (
    Flask,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

PROVIDERS = ("Avery", "Jordan")
SERVICES = ("Consultation", "Cut and style", "Color consultation")
APPOINTMENT_MINUTES = 30
OPENING_HOUR = 9
CLOSING_HOUR = 17

STATUS_TRANSITIONS = {
    "booked": {"confirmed", "no-show"},
    "confirmed": {"arrived", "no-show"},
    "arrived": {"completed"},
    "completed": set(),
    "no-show": set(),
}

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    service TEXT NOT NULL,
    provider TEXT NOT NULL,
    start_at TEXT NOT NULL,
    end_at TEXT NOT NULL,
    status TEXT NOT NULL CHECK (
        status IN ('booked', 'confirmed', 'arrived', 'completed', 'no-show')
    ),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reminder_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id),
    scheduled_at TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id),
    action TEXT NOT NULL,
    details TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="local-demo-key-change-before-deployment",
        DATABASE=str(Path(app.instance_path) / "appointments.sqlite3"),
    )
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    initialize_database(app)
    app.teardown_appcontext(close_db)

    @app.get("/")
    def index():
        return redirect(url_for("customer"))

    @app.route("/customer", methods=["GET", "POST"])
    def customer():
        if request.method == "POST":
            customer_name = request.form.get("customer_name", "").strip()
            service = request.form.get("service", "")
            provider = request.form.get("provider", "")
            start_at = parse_appointment_time(
                request.form.get("appointment_date", ""),
                request.form.get("appointment_time", ""),
            )
            if not customer_name or len(customer_name) > 80:
                flash("Enter a name between 1 and 80 characters.", "error")
            elif service not in SERVICES:
                flash("Choose one of the listed services.", "error")
            elif provider not in PROVIDERS:
                flash("Choose one of the listed providers.", "error")
            elif start_at is None:
                flash("Choose a valid date and appointment time.", "error")
            else:
                try:
                    validate_slot(start_at)
                except ValueError as error:
                    flash(str(error), "error")
                else:
                    try:
                        appointment_id = create_appointment(
                            customer_name, service, provider, start_at
                        )
                    except ValueError as error:
                        flash(str(error), "error")
                        return redirect(url_for("customer"))
                    flash(
                        f"Request #{appointment_id} submitted. The front desk must confirm it.",
                        "success",
                    )
                    return redirect(url_for("customer"))

        return render_template(
            "customer.html",
            providers=PROVIDERS,
            services=SERVICES,
            today=datetime.now().date().isoformat(),
        )

    @app.get("/frontdesk")
    def frontdesk():
        appointments = get_db().execute(
            """
            SELECT * FROM appointments
            ORDER BY
                CASE status
                    WHEN 'booked' THEN 0
                    WHEN 'confirmed' THEN 1
                    WHEN 'arrived' THEN 2
                    ELSE 3
                END,
                start_at
            """
        ).fetchall()
        reminders = get_db().execute(
            """
            SELECT reminder_log.*, appointments.customer_name
            FROM reminder_log
            JOIN appointments ON appointments.id = reminder_log.appointment_id
            ORDER BY reminder_log.scheduled_at, reminder_log.id
            """
        ).fetchall()
        return render_template(
            "frontdesk.html",
            appointments=appointments,
            reminders=reminders,
            transitions=STATUS_TRANSITIONS,
            providers=PROVIDERS,
        )

    @app.post("/frontdesk/<int:appointment_id>/status")
    def update_status(appointment_id: int):
        target = request.form.get("status", "")
        db = get_db()
        db.execute("BEGIN IMMEDIATE")
        appointment = get_appointment(appointment_id)
        if target not in STATUS_TRANSITIONS[appointment["status"]]:
            db.rollback()
            abort(400, description="That appointment status transition is not allowed.")

        now = timestamp_now()
        db.execute(
            "UPDATE appointments SET status = ? WHERE id = ?",
            (target, appointment_id),
        )
        log_audit(
            appointment_id,
            "status_changed",
            f"{appointment['status']} -> {target}",
            now,
        )
        db.commit()
        flash(f"Appointment #{appointment_id} moved to {target}.", "success")
        return redirect(url_for("frontdesk"))

    @app.post("/frontdesk/<int:appointment_id>/move")
    def move_appointment(appointment_id: int):
        new_start = parse_appointment_time(
            request.form.get("appointment_date", ""),
            request.form.get("appointment_time", ""),
        )
        new_provider = request.form.get("provider", "")
        if new_start is None or new_provider not in PROVIDERS:
            flash("Choose a valid date, time, and provider.", "error")
            return redirect(url_for("frontdesk"))

        try:
            validate_slot(new_start)
        except ValueError as error:
            flash(str(error), "error")
            return redirect(url_for("frontdesk"))

        db = get_db()
        db.execute("BEGIN IMMEDIATE")
        appointment = get_appointment(appointment_id)
        if appointment["status"] not in {"booked", "confirmed"}:
            db.rollback()
            abort(400, description="Only booked or confirmed appointments can be moved.")
        if has_conflict(
            new_provider,
            new_start,
            new_start + timedelta(minutes=APPOINTMENT_MINUTES),
            exclude_id=appointment_id,
        ):
            db.rollback()
            flash("That provider already has an appointment at that time.", "error")
            return redirect(url_for("frontdesk"))

        new_end = new_start + timedelta(minutes=APPOINTMENT_MINUTES)
        old_slot = f"{appointment['provider']} at {appointment['start_at']}"
        db.execute(
            """
            UPDATE appointments
            SET provider = ?, start_at = ?, end_at = ?
            WHERE id = ?
            """,
            (new_provider, new_start.isoformat(timespec="minutes"),
             new_end.isoformat(timespec="minutes"), appointment_id),
        )
        log_audit(
            appointment_id,
            "appointment_moved",
            f"{old_slot} -> {new_provider} at {new_start.isoformat(timespec='minutes')}",
            timestamp_now(),
        )
        db.commit()
        flash(f"Appointment #{appointment_id} moved.", "success")
        return redirect(url_for("frontdesk"))

    @app.get("/provider")
    def provider_schedule():
        provider = request.args.get("provider", PROVIDERS[0])
        if provider not in PROVIDERS:
            abort(400, description="Unknown provider.")
        appointments = get_db().execute(
            """
            SELECT * FROM appointments
            WHERE provider = ?
            ORDER BY start_at
            """,
            (provider,),
        ).fetchall()
        return render_template(
            "provider.html", provider=provider, providers=PROVIDERS,
            appointments=appointments,
        )

    return app


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        connection = sqlite3.connect(
            current_app.config["DATABASE"], isolation_level=None
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection
    return g.db


def close_db(_error: BaseException | None = None) -> None:
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def initialize_database(app: Flask) -> None:
    connection = sqlite3.connect(app.config["DATABASE"])
    try:
        connection.executescript(SCHEMA)
    finally:
        connection.close()


def timestamp_now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def parse_appointment_time(date_value: str, time_value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(f"{date_value}T{time_value}")
    except ValueError:
        return None


def validate_slot(start_at: datetime) -> None:
    end_at = start_at + timedelta(minutes=APPOINTMENT_MINUTES)
    if start_at <= datetime.now():
        raise ValueError("Appointments must be scheduled in the future.")
    if start_at.minute not in (0, 30) or start_at.second or start_at.microsecond:
        raise ValueError("Choose a start time on the hour or half-hour.")
    closing_time = start_at.replace(
        hour=CLOSING_HOUR, minute=0, second=0, microsecond=0
    )
    if start_at.hour < OPENING_HOUR or end_at > closing_time:
        raise ValueError("Appointments are available between 9:00 AM and 5:00 PM.")


def has_conflict(
    provider: str,
    start_at: datetime,
    end_at: datetime,
    exclude_id: int | None = None,
) -> bool:
    query = """
        SELECT 1 FROM appointments
        WHERE provider = ?
          AND start_at < ?
          AND end_at > ?
    """
    params: list[Any] = [
        provider,
        end_at.isoformat(timespec="minutes"),
        start_at.isoformat(timespec="minutes"),
    ]
    if exclude_id is not None:
        query += " AND id != ?"
        params.append(exclude_id)
    return get_db().execute(query, params).fetchone() is not None


def create_appointment(
    customer_name: str, service: str, provider: str, start_at: datetime
) -> int:
    db = get_db()
    db.execute("BEGIN IMMEDIATE")
    end_at = start_at + timedelta(minutes=APPOINTMENT_MINUTES)
    if has_conflict(provider, start_at, end_at):
        db.rollback()
        raise ValueError("That provider already has an appointment at that time.")

    now = timestamp_now()
    cursor = db.execute(
        """
        INSERT INTO appointments
            (customer_name, service, provider, start_at, end_at, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'booked', ?)
        """,
        (
            customer_name,
            service,
            provider,
            start_at.isoformat(timespec="minutes"),
            end_at.isoformat(timespec="minutes"),
            now,
        ),
    )
    appointment_id = cursor.lastrowid
    scheduled_at = start_at - timedelta(days=1)
    db.execute(
        """
        INSERT INTO reminder_log (appointment_id, scheduled_at, message, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            appointment_id,
            scheduled_at.isoformat(timespec="minutes"),
            f"Reminder for {customer_name}: {service} with {provider}.",
            now,
        ),
    )
    log_audit(appointment_id, "appointment_booked", "Customer request submitted", now)
    db.commit()
    return appointment_id


def get_appointment(appointment_id: int) -> sqlite3.Row:
    appointment = get_db().execute(
        "SELECT * FROM appointments WHERE id = ?", (appointment_id,)
    ).fetchone()
    if appointment is None:
        abort(404)
    return appointment


def log_audit(
    appointment_id: int, action: str, details: str, created_at: str
) -> None:
    get_db().execute(
        """
        INSERT INTO audit_log (appointment_id, action, details, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (appointment_id, action, details, created_at),
    )


if __name__ == "__main__":
    create_app().run(debug=True)
