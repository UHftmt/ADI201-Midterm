# Architecture (one page)

> Draft written by Claude Code from the finished code on Nov 10 (see `ai-use-log.md`). Vinh: check each line against the code and reword it in your own words before the submit.

**Entities** *(the things stored, with their fields)*:

- **Booking**: `id` (1, 2, 3 in the order they were accepted), `request_id`, `client`, `service_id`, `stylist`, `start`, `end`, `minutes`, `state`.
- **Seen request**: every `request_id` that reached the rules, accepted or refused. This is how a repeated id is caught.
- **History row** (the audit log): `at` (time), `booking_id`, `request_id`, `actor` (the role), `action` (`create`, `move` or `remind`), `old_state`, `new_state`, `outcome`. Refused attempts get a row too.
- **Service** is read from `fixtures/idea2-appointments/services.csv` (id, name, minutes). It is not stored in the database.

**States and who may move each** *(from, to, role)*:

| From | To | Who |
|---|---|---|
| (new request) | `booked` | client |
| `booked` | `confirmed` | staff |
| `booked` | `cancelled` | client or staff |
| `confirmed` | `arrived` | staff |
| `confirmed` | `no_show` | staff |
| `confirmed` | `cancelled` | client or staff |
| `arrived` | `completed` | staff |

The table lives in one place, `ALLOWED_MOVES` in `rules.py`. The check runs in this order: a move that is not in the table is `illegal_move`; a move that is in the table but tried by the wrong role is `not_permitted`. A refused move leaves the booking in the state it had. `completed`, `no_show` and `cancelled` are end states: nothing moves out of them.

A new request is checked in this order: repeated `request_id` (`duplicate_request`), start not written as `YYYY-MM-DD HH:MM` (`bad_date_format`), ends after 17:00 or starts before 09:00 (`after_close`), overlaps another booking of the same stylist that is not cancelled (`conflict`). Two bookings that touch end to start do not overlap.

**Roles and what each can see:**

- **Client** (`/book`): the booking form, the result of the last request in plain words, the list of bookings, and a Cancel button where the table allows a client to cancel.
- **Staff** (`/staff`): the queue of every booking with only the buttons staff may press from that state, a "Send reminder" button, and the count and total minutes per stylist. `/staff/history` shows the audit log.
- There are no accounts. The role comes from the page the request is sent from. The server checks every move against the table, so a hand-made request that claims to be a client still cannot confirm.

**Data store**: one SQLite file, `salon.db` (or the path in the `SALON_DB` setting), with tables `bookings`, `seen_requests` and `history`. `store.py` is the only file that talks to the database. The tables are created only if missing, so stopping and starting the app keeps the data.

**The external step I sandboxed**: a real salon would send a reminder text or email. Here "Send reminder" adds one line ending in `REMINDER (not sent)` to `outbox/reminders.log`, next to the database file. Nothing leaves the computer.

**Where each Difficulty Bar feature lives** *(file names)*:

| # | Requirement | Where |
|---|---|---|
| 1 | Two roles, different views | `app.py`, `templates/book.html`, `templates/staff.html` |
| 2 | Tracked state with rules | `rules.py` (`ALLOWED_MOVES`, `check_move`, `check_request`) |
| 3 | Persistence | `store.py`, `salon.db` |
| 4 | Staff queue | `/staff` in `app.py`, `templates/staff.html` |
| 5 | Fake external step | the reminder route in `app.py`, `outbox/reminders.log` |
| 6 | Human checkpoint | a booking stays `booked` until staff press Confirm on `/staff` |
| 7 | Known-answer tests and one engineered failure | `tests/known-answer/cases.json`, `tests/known-answer/run.py`, `evidence/engineered-failure.md` |
