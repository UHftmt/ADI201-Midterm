"""Web layer of the salon appointment app (Flask).

The pages (/book, /staff) and the JSON API (/api/...) call the SAME Store
methods, so the known-answer tests exercise the code the browser uses.
All decisions are made by rules.py through store.py, never by the page.

Run:  python3 app.py   then open http://127.0.0.1:5000
"""
import os
from datetime import datetime

from flask import Flask, g, jsonify, redirect, render_template, request, url_for

import rules
from store import Store

HERE = os.path.dirname(os.path.abspath(__file__))

# The salon's stylists, shown in the dropdown on the client page.
STYLISTS = ["Ana", "Ben"]

# A reminder only makes sense while the visit is still ahead.
REMIND_STATES = ["booked", "confirmed"]

# Plain-language labels. The contract word is always shown next to its label.
STATE_TEXT = {
    "booked": "asked for, waiting for the front desk",
    "confirmed": "approved by the front desk",
    "arrived": "client is in the salon",
    "completed": "visit finished",
    "no_show": "client did not come",
    "cancelled": "called off",
}
OUTCOME_TEXT = {
    "accepted": "Done. The request was accepted.",
    "bad_date_format": "The start must be written exactly like 2026-11-02 09:00 and be a real date and time.",
    "after_close": "The visit would not fit inside opening hours (09:00 to 17:00).",
    "conflict": "That stylist already has a booking that overlaps this time.",
    "duplicate_request": "This request id was already used, so the request was not processed again.",
    "missing_field": "A required field was left empty.",
    "unknown_service": "That service is not on the salon's list.",
    "not_permitted": "This role is not allowed to make that change.",
    "illegal_move": "A booking cannot go from its current state to that state.",
    "not_found": "There is no booking with that number.",
    "reminder_written": "The reminder was written to the local outbox file. Nothing was sent.",
    "reminder_not_allowed": "Reminders are only for bookings that are booked or confirmed.",
}
# The text on the button that moves a booking TO each state.
BUTTON_TEXT = {
    "confirmed": "Confirm",
    "arrived": "Mark arrived",
    "completed": "Mark completed",
    "no_show": "Mark no-show",
    "cancelled": "Cancel",
}


def moves_for(state, role):
    """The states this role may move a booking to from `state`.

    Read from rules.ALLOWED_MOVES, so the buttons always match the rules.
    """
    return [to for (frm, to), roles in rules.ALLOWED_MOVES.items()
            if frm == state and role in roles]


def create_app(db_path=None):
    """Build the Flask app. Tests pass a temporary db_path."""
    if db_path is None:
        db_path = os.environ.get("SALON_DB") or os.path.join(HERE, "salon.db")
    db_path = os.path.abspath(db_path)
    # The fake outbox lives in the same folder as the database file.
    reminders_log = os.path.join(os.path.dirname(db_path), "outbox", "reminders.log")

    app = Flask(__name__)

    def get_store():
        """One Store (one sqlite connection) per request, opened on first use."""
        if "store" not in g:
            g.store = Store(db_path)
        return g.store

    @app.teardown_appcontext
    def close_store(error):
        """Flask calls this when the request is over: close the connection."""
        store = g.pop("store", None)
        if store is not None:
            store.close()

    @app.context_processor
    def template_helpers():
        """Names every template can use."""
        return {
            "state_text": STATE_TEXT,
            "button_text": BUTTON_TEXT,
            "moves_for": moves_for,
            "remind_states": REMIND_STATES,
            # The result of the last action comes back in the address: ?outcome=word
            "outcome": request.args.get("outcome"),
            "outcome_text": OUTCOME_TEXT,
        }

    # ---- pages ---------------------------------------------------------

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/book")
    def book_page():
        store = get_store()
        return render_template("book.html", bookings=store.list_bookings(),
                               services=store.services, stylists=STYLISTS)

    @app.get("/staff")
    def staff_page():
        store = get_store()
        return render_template("staff.html", bookings=store.list_bookings(),
                               services=store.services, summary=store.summary())

    @app.get("/staff/history")
    def history_page():
        return render_template("history.html", rows=get_store().history())

    # ---- form actions: do the action, then go back to the page ----------

    @app.post("/book")
    def book_form():
        # This form is the client page, so the role is "client".
        result = get_store().create_booking("client", request.form)
        return redirect(url_for("book_page", outcome=result["outcome"]))

    @app.post("/bookings/<int:booking_id>/move")
    def move_form(booking_id):
        # The role is a hidden field of the page. A forged value gets no
        # extra power: rules.check_move decides, and answers not_permitted.
        role = request.form.get("role", "")
        result = get_store().move_booking(role, booking_id, request.form.get("to", ""))
        page = "staff_page" if role == "staff" else "book_page"
        return redirect(url_for(page, outcome=result["outcome"]))

    @app.post("/staff/bookings/<int:booking_id>/remind")
    def remind(booking_id):
        # Find the booking in the stored list.
        booking = None
        for b in get_store().list_bookings():
            if b["id"] == booking_id:
                booking = b
        if booking is None:
            outcome = "not_found"
        elif booking["state"] not in REMIND_STATES:
            outcome = "reminder_not_allowed"
        else:
            # The fake external step: one line in a local file, nothing is sent.
            os.makedirs(os.path.dirname(reminders_log), exist_ok=True)
            client = " ".join(booking["client"].split())  # keep it on one line
            line = "\t".join([
                datetime.now().isoformat(timespec="seconds"),
                "booking " + str(booking["id"]),
                client,
                booking["start"],
                "REMINDER (not sent)",
            ])
            with open(reminders_log, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            outcome = "reminder_written"
        return redirect(url_for("staff_page", outcome=outcome))

    # ---- JSON API (used by tests/known-answer/run.py) -------------------
    # A rule rejection is still HTTP 200: the outcome word is in the body.
    # Only a body that is not a JSON object gets HTTP 400.

    def json_body():
        body = request.get_json(silent=True)  # None when it is not valid JSON
        return body if isinstance(body, dict) else None

    @app.post("/api/bookings")
    def api_create():
        body = json_body()
        if body is None or not isinstance(body.get("data"), dict):
            return jsonify({"error": "send a JSON object with role and data"}), 400
        return jsonify(get_store().create_booking(body.get("role"), body["data"]))

    @app.post("/api/bookings/<int:booking_id>/move")
    def api_move(booking_id):
        body = json_body()
        if body is None:
            return jsonify({"error": "send a JSON object with role and to"}), 400
        return jsonify(get_store().move_booking(body.get("role"), booking_id, body.get("to")))

    @app.get("/api/bookings")
    def api_list():
        store = get_store()
        result = {"outcome": "accepted"}
        result.update(store.summary())  # count and minutes_by_stylist
        result["bookings"] = store.list_bookings()
        return jsonify(result)

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
