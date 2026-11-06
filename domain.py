"""Domain logic, validation engine, state machine, and notification logger for Idea 2."""
import re
from datetime import datetime, timedelta
from pathlib import Path
from database import get_db_connection, log_audit

ROOT_DIR = Path(__file__).resolve().parent
REMINDERS_LOG = ROOT_DIR / "reminders.log"

DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")

VALID_ROLES = {"client", "staff"}
VALID_STATES = {"booked", "confirmed", "arrived", "completed", "no_show", "cancelled"}

ALLOWED_TRANSITIONS = {
    # (current_state, target_state): set of allowed roles
    (None, "booked"): {"client", "staff"},
    ("booked", "confirmed"): {"staff"},
    ("confirmed", "arrived"): {"staff"},
    ("arrived", "completed"): {"staff"},
    ("confirmed", "no_show"): {"staff"},
    ("booked", "cancelled"): {"client", "staff"},
    ("confirmed", "cancelled"): {"client", "staff"},
}


def log_reminder(client, request_id, stylist, start_time, service_name):
    """Sandboxed external step: append appointment reminder to local log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = (
        f"[{timestamp}] [REMINDER] Appointment {request_id} for {client} "
        f"({service_name}) with {stylist} at {start_time}\n"
    )
    with open(REMINDERS_LOG, "a", encoding="utf-8") as f:
        f.write(log_line)


def create_appointment(db_path, actor, data):
    """Validate and insert a new appointment booking.
    
    Returns dict:
      {"outcome": "accepted", "state": "booked", "item_id": id} on success,
      or {"outcome": <rejection_reason>} on validation failure.
    """
    request_id = data.get("request_id")
    client = data.get("client")
    service_id = data.get("service_id")
    stylist = data.get("stylist")
    start_str = data.get("start")

    # 1. Check duplicate request_id
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM appointments WHERE request_id = ?", (request_id,))
    if cur.fetchone():
        conn.close()
        log_audit(db_path, actor, request_id, None, None, "duplicate_request")
        return {"outcome": "duplicate_request"}

    # 2. Check date format: strict YYYY-MM-DD HH:MM
    if not start_str or not DATE_REGEX.match(start_str):
        conn.close()
        log_audit(db_path, actor, request_id, None, None, "bad_date_format")
        return {"outcome": "bad_date_format"}

    try:
        start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
    except ValueError:
        conn.close()
        log_audit(db_path, actor, request_id, None, None, "bad_date_format")
        return {"outcome": "bad_date_format"}

    # 3. Lookup service and calculate end time
    cur.execute("SELECT name, minutes FROM services WHERE service_id = ?", (service_id,))
    svc = cur.fetchone()
    if not svc:
        conn.close()
        log_audit(db_path, actor, request_id, None, None, "invalid_request")
        return {"outcome": "invalid_request"}

    service_name = svc["name"]
    duration_min = svc["minutes"]
    end_dt = start_dt + timedelta(minutes=duration_min)

    # 4. Check operating hours: 09:00 to 17:00
    opening_time = start_dt.replace(hour=9, minute=0, second=0, microsecond=0)
    closing_time = start_dt.replace(hour=17, minute=0, second=0, microsecond=0)

    if start_dt < opening_time or end_dt > closing_time:
        conn.close()
        log_audit(db_path, actor, request_id, None, None, "after_close")
        return {"outcome": "after_close"}

    # 5. Check stylist conflict with active bookings (booked, confirmed, arrived, completed)
    # Bookings that are cancelled do not block.
    cur.execute(
        """
        SELECT request_id, start_time, end_time FROM appointments
        WHERE stylist = ? AND state NOT IN ('cancelled')
        """,
        (stylist,)
    )
    existing_slots = cur.fetchall()
    for slot in existing_slots:
        ex_start = datetime.strptime(slot["start_time"], "%Y-%m-%d %H:%M")
        ex_end = datetime.strptime(slot["end_time"], "%Y-%m-%d %H:%M")

        # Two intervals [S1, E1) and [S2, E2) overlap iff max(S1, S2) < min(E1, E2)
        if max(start_dt, ex_start) < min(end_dt, ex_end):
            conn.close()
            log_audit(db_path, actor, request_id, None, None, "conflict")
            return {"outcome": "conflict"}

    # All checks passed: insert appointment in 'booked' state
    end_str = end_dt.strftime("%Y-%m-%d %H:%M")
    cur.execute(
        """
        INSERT INTO appointments (request_id, client, service_id, stylist, start_time, end_time, state)
        VALUES (?, ?, ?, ?, ?, ?, 'booked')
        """,
        (request_id, client, service_id, stylist, start_str, end_str)
    )
    item_id = cur.lastrowid
    conn.commit()
    conn.close()

    log_audit(db_path, actor, request_id, None, "booked", "accepted")
    log_reminder(client, request_id, stylist, start_str, service_name)

    return {"outcome": "accepted", "state": "booked", "item_id": item_id}


def move_appointment(db_path, actor, appt_id, to_state):
    """Attempt a state transition on an appointment.
    
    Returns dict:
      {"outcome": "accepted", "state": to_state} on success,
      {"outcome": "not_permitted", "state": current_state} if role unauthorized,
      {"outcome": "illegal_move", "state": current_state} if transition invalid.
    """
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, request_id, client, stylist, start_time, service_id, state FROM appointments WHERE id = ?", (appt_id,))
    appt = cur.fetchone()
    if not appt:
        conn.close()
        return {"outcome": "invalid_request"}

    current_state = appt["state"]
    request_id = appt["request_id"]

    # 1. Check if the transition itself is valid in the state table
    transition_key = (current_state, to_state)
    if transition_key not in ALLOWED_TRANSITIONS:
        conn.close()
        log_audit(db_path, actor, request_id, current_state, current_state, "illegal_move")
        return {"outcome": "illegal_move", "state": current_state}

    # 2. Check if the actor role is allowed to make this transition
    allowed_roles = ALLOWED_TRANSITIONS[transition_key]
    if actor not in allowed_roles:
        conn.close()
        log_audit(db_path, actor, request_id, current_state, current_state, "not_permitted")
        return {"outcome": "not_permitted", "state": current_state}

    # Execute transition
    cur.execute("UPDATE appointments SET state = ? WHERE id = ?", (to_state, appt_id))
    conn.commit()
    conn.close()

    log_audit(db_path, actor, request_id, current_state, to_state, "accepted")
    return {"outcome": "accepted", "state": to_state}


def list_appointments_summary(db_path):
    """Retrieve summary metrics and appointment count."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM appointments WHERE state NOT IN ('cancelled')")
    count = cur.fetchone()[0]

    # Calculate total minutes for Ana from accepted bookings
    cur.execute(
        """
        SELECT COALESCE(SUM(s.minutes), 0)
        FROM appointments a
        JOIN services s ON a.service_id = s.service_id
        WHERE a.stylist = 'Ana' AND a.state NOT IN ('cancelled')
        """
    )
    ana_minutes = int(cur.fetchone()[0])
    conn.close()

    return {
        "outcome": "accepted",
        "count": count,
        "ana_minutes": ana_minutes
    }

