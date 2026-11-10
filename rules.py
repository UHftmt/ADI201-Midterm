"""Rules of the salon appointment app. Pure functions: no database, no Flask.

Everything here answers a question with a contract word such as "accepted",
"conflict" or "illegal_move". store.py asks these questions and saves the result.
"""
import csv
import os
import re
from datetime import datetime, time, timedelta

STATES = ["booked", "confirmed", "arrived", "completed", "no_show", "cancelled"]
ROLES = ["client", "staff"]

# The state table from the README: (from_state, to_state) -> roles that may do it.
# A pair that is not a key of this dict is not a legal move for anyone.
ALLOWED_MOVES = {
    ("booked", "confirmed"): {"staff"},
    ("booked", "cancelled"): {"client", "staff"},
    ("confirmed", "arrived"): {"staff"},
    ("confirmed", "no_show"): {"staff"},
    ("confirmed", "cancelled"): {"client", "staff"},
    ("arrived", "completed"): {"staff"},
}

# Opening hours, the same every day.
OPEN = time(9, 0)
CLOSE = time(17, 0)

# A start must look exactly like 2026-11-02 09:00.
START_PATTERN = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"
START_FORMAT = "%Y-%m-%d %H:%M"

# services.csv sits next to this file, so the path works from any folder.
SERVICES_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "fixtures", "idea2-appointments", "services.csv",
)


def check_move(current_state, to_state, role):
    """May this role move a booking from current_state to to_state?"""
    # Checked first: is the move in the table at all? Unknown state words and
    # same-state moves are not keys, so they land here too.
    if (current_state, to_state) not in ALLOWED_MOVES:
        return "illegal_move"
    # The move exists, but is this role one of the roles allowed to make it?
    if role not in ALLOWED_MOVES[(current_state, to_state)]:
        return "not_permitted"
    return "accepted"


def parse_start(text):
    """Turn 'YYYY-MM-DD HH:MM' into a datetime. Return None if it is not valid."""
    if not isinstance(text, str):
        return None
    # The shape must match completely (re.ASCII: only the digits 0-9 count).
    if not re.fullmatch(START_PATTERN, text, re.ASCII):
        return None
    # The shape is right, but it must also be a real date and time
    # (2026-02-30 or 25:00 have the right shape and are still wrong).
    try:
        return datetime.strptime(text, START_FORMAT)
    except ValueError:
        return None


def check_request(start_text, minutes, existing):
    """Check one booking request. Returns (outcome, start_dt, end_dt).

    existing: list of (start_dt, end_dt) for the same stylist's bookings that
    were accepted and are not cancelled.
    """
    # 1. Is the start written correctly?
    start_dt = parse_start(start_text)
    if start_dt is None:
        return ("bad_date_format", None, None)

    # The booking occupies start up to start + minutes.
    end_dt = start_dt + timedelta(minutes=minutes)

    # 2. Does it fit inside opening hours of that day?
    #    Ending exactly at closing time is fine.
    open_dt = datetime.combine(start_dt.date(), OPEN)
    close_dt = datetime.combine(start_dt.date(), CLOSE)
    if start_dt < open_dt or end_dt > close_dt:
        return ("after_close", start_dt, end_dt)

    # 3. Does it overlap another booking of this stylist?
    #    Two time ranges overlap when each one starts before the other ends.
    #    Starting exactly when another ends is NOT an overlap.
    for other_start, other_end in existing:
        if start_dt < other_end and other_start < end_dt:
            return ("conflict", start_dt, end_dt)

    return ("accepted", start_dt, end_dt)


def load_services(path=SERVICES_CSV):
    """Read services.csv into {service_id: {"name": ..., "minutes": int}}."""
    services = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            services[row["service_id"]] = {
                "name": row["name"],
                "minutes": int(row["minutes"]),
            }
    return services
