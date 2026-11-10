"""Storage layer of the salon appointment app: one sqlite3 file.

The Store saves bookings and writes one history row for every create or move
attempt, accepted or rejected. All decisions come from rules.py.
"""
import sqlite3
from datetime import datetime

import rules

SCHEMA = """
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT UNIQUE,
    client TEXT,
    service_id TEXT,
    stylist TEXT,
    start TEXT,
    end TEXT,
    minutes INTEGER,
    state TEXT
);
CREATE TABLE IF NOT EXISTS seen_requests (
    request_id TEXT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    at TEXT,
    booking_id INTEGER NULL,
    request_id TEXT,
    actor TEXT,
    action TEXT,
    old_state TEXT NULL,
    new_state TEXT NULL,
    outcome TEXT
);
"""


def _clean(value):
    """A form field as a string without outer spaces; a missing one becomes ''."""
    if value is None:
        return ""
    return str(value).strip()


class Store:
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row  # rows can be turned into dicts
        # IF NOT EXISTS: opening the same file again keeps the saved data.
        self.db.executescript(SCHEMA)
        self.db.commit()
        self.services = rules.load_services()

    def close(self):
        self.db.close()

    # ---- history -------------------------------------------------------

    def _log(self, booking_id, request_id, actor, action, old_state, new_state, outcome):
        """Write one history row and save it to disk straight away."""
        self.db.execute(
            "INSERT INTO history (at, booking_id, request_id, actor, action,"
            " old_state, new_state, outcome) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now().isoformat(timespec="seconds"), booking_id, request_id,
             actor, action, old_state, new_state, outcome),
        )
        self.db.commit()

    def _reject_create(self, request_id, role, outcome):
        """A rejected create: no booking is stored, only the history row."""
        self._log(None, request_id, role, "create", None, None, outcome)
        return {"outcome": outcome}

    # ---- create --------------------------------------------------------

    def create_booking(self, role, data):
        request_id = _clean(data.get("request_id"))
        client = _clean(data.get("client"))
        service_id = _clean(data.get("service_id"))
        stylist = _clean(data.get("stylist"))
        start = _clean(data.get("start"))

        # Only a client may ask for a booking.
        if role != "client":
            return self._reject_create(request_id, role, "not_permitted")

        # Without a request_id we cannot tell a repeat from a new request.
        if not request_id:
            return self._reject_create(request_id, role, "missing_field")

        # Have we seen this request_id before (accepted OR rejected)?
        seen = self.db.execute(
            "SELECT 1 FROM seen_requests WHERE request_id = ?", (request_id,)
        ).fetchone()
        if seen:
            return self._reject_create(request_id, role, "duplicate_request")

        # From here on the id counts as seen, whatever the result is.
        self.db.execute("INSERT INTO seen_requests (request_id) VALUES (?)", (request_id,))
        self.db.commit()

        # A blank start is not listed here: the rules call it bad_date_format.
        if not client or not service_id or not stylist:
            return self._reject_create(request_id, role, "missing_field")

        if service_id not in self.services:
            return self._reject_create(request_id, role, "unknown_service")
        minutes = self.services[service_id]["minutes"]

        # This stylist's bookings that still hold their slot (not cancelled).
        rows = self.db.execute(
            "SELECT start, end FROM bookings WHERE stylist = ? AND state != ?",
            (stylist, "cancelled"),
        ).fetchall()
        existing = [(rules.parse_start(r["start"]), rules.parse_start(r["end"])) for r in rows]

        outcome, start_dt, end_dt = rules.check_request(start, minutes, existing)
        if outcome != "accepted":
            return self._reject_create(request_id, role, outcome)

        # Accepted: store the booking in its first state.
        cur = self.db.execute(
            "INSERT INTO bookings (request_id, client, service_id, stylist,"
            " start, end, minutes, state) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (request_id, client, service_id, stylist,
             start_dt.strftime(rules.START_FORMAT), end_dt.strftime(rules.START_FORMAT),
             minutes, "booked"),
        )
        self.db.commit()
        booking_id = cur.lastrowid
        self._log(booking_id, request_id, role, "create", None, "booked", "accepted")
        return {"outcome": "accepted", "id": booking_id, "state": "booked"}

    # ---- move ----------------------------------------------------------

    def move_booking(self, role, booking_id, to_state):
        row = self.db.execute(
            "SELECT request_id, state FROM bookings WHERE id = ?", (booking_id,)
        ).fetchone()
        if row is None:
            self._log(None, None, role, "move", None, None, "not_found")
            return {"outcome": "not_found"}

        old_state = row["state"]
        outcome = rules.check_move(old_state, to_state, role)
        if outcome != "accepted":
            # Rejected: the state stays as it was, and we still report it.
            self._log(booking_id, row["request_id"], role, "move", old_state, old_state, outcome)
            return {"outcome": outcome, "state": old_state}

        self.db.execute("UPDATE bookings SET state = ? WHERE id = ?", (to_state, booking_id))
        self.db.commit()
        self._log(booking_id, row["request_id"], role, "move", old_state, to_state, "accepted")
        return {"outcome": "accepted", "state": to_state}

    # ---- read ----------------------------------------------------------

    def list_bookings(self):
        rows = self.db.execute("SELECT * FROM bookings ORDER BY start, id").fetchall()
        return [dict(r) for r in rows]

    def summary(self):
        """Count and minutes per stylist over every stored booking, any state."""
        count = self.db.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
        rows = self.db.execute(
            "SELECT stylist, SUM(minutes) AS total FROM bookings GROUP BY stylist"
        ).fetchall()
        return {
            "count": count,
            "minutes_by_stylist": {r["stylist"]: r["total"] for r in rows},
        }

    def history(self):
        rows = self.db.execute("SELECT * FROM history ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
