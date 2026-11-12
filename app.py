"""Flask Web Application for Salon & Clinic Appointment Scheduler (Idea 2)."""
import os
import random
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import init_db, get_db_connection
from domain import create_appointment, move_appointment

ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = ROOT_DIR / "appointments.db"

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "salon-in-memory-dev-key")

# Ensure database and services are initialized
init_db(DB_PATH)


@app.route("/")
def index():
    return redirect(url_for("book"))


@app.route("/book", methods=["GET", "POST"])
def book():
    conn = get_db_connection(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT service_id, name, minutes FROM services ORDER BY service_id")
    services = cur.fetchall()
    conn.close()

    if request.method == "POST":
        data = {
            "request_id": request.form.get("request_id", "").strip(),
            "client": request.form.get("client", "").strip(),
            "service_id": request.form.get("service_id", "").strip(),
            "stylist": request.form.get("stylist", "").strip(),
            "start": request.form.get("start", "").strip(),
        }

        result = create_appointment(DB_PATH, actor="client", data=data)
        if result["outcome"] == "accepted":
            flash(f"Booking {data['request_id']} successfully placed! Current state: booked.", "success")
            return redirect(url_for("book"))
        else:
            flash(f"Booking rejected: {result['outcome']}", "error")

    default_req_id = f"B-{random.randint(100, 999)}"
    return render_template("book.html", services=services, default_request_id=default_req_id)


@app.route("/staff")
def staff():
    conn = get_db_connection(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, a.request_id, a.client, a.stylist, a.start_time, a.end_time, a.state, s.name as service_name, s.minutes
        FROM appointments a
        JOIN services s ON a.service_id = s.service_id
        ORDER BY a.start_time ASC
    """)
    rows = cur.fetchall()
    conn.close()

    pending = [r for r in rows if r["state"] == "booked"]
    active = [r for r in rows if r["state"] in ("confirmed", "arrived")]
    history = [r for r in rows if r["state"] in ("completed", "cancelled", "no_show")]

    return render_template("staff.html", pending=pending, active=active, history=history)


@app.route("/staff/history")
def staff_history():
    conn = get_db_connection(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, timestamp, actor, request_id, old_state, new_state, outcome
        FROM audit_log
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return render_template("history.html", rows=rows)


@app.route("/staff/action", methods=["POST"])
def staff_action():
    appt_id = int(request.form.get("appt_id"))
    to_state = request.form.get("to_state")

    result = move_appointment(DB_PATH, actor="staff", appt_id=appt_id, to_state=to_state)
    if result["outcome"] == "accepted":
        flash(f"Appointment updated to '{to_state}'.", "success")
    else:
        flash(f"Action rejected: {result['outcome']}", "error")

    return redirect(url_for("staff"))


@app.route("/api/appointments", methods=["GET", "POST"])
def api_appointments():
    if request.method == "POST":
        data = request.json or {}
        actor = data.get("as", "client")
        step_data = data.get("data", {})
        res = create_appointment(DB_PATH, actor, step_data)
        return jsonify(res)
    else:
        conn = get_db_connection(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM appointments")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return jsonify(rows)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

