# Salon & Clinic Appointment Scheduler (Idea 2)

A lightweight appointment booking and intake web application for a fictional salon or clinic, featuring conflict detection, role-based workflow queues, and a sandboxed notification log.

## Run it
```bash
python3 app.py
```
Open your browser to:
- Client booking form: `http://localhost:5000/book` (or `http://localhost:5000/`)
- Staff dashboard queue: `http://localhost:5000/staff`
- Audit history viewer: `http://localhost:5000/staff/history` (ported from Vinh)
- Provider daily schedule: `http://localhost:5000/provider` (ported from Shiming)

## Python and version
- Python 3.11+ (Tested on Python 3.13)
- Dependencies installed via `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

## Test it
```bash
python3 tests/known-answer/run.py
```
Runs the known-answer test suite and prints one `PASS` or `FAIL` line per case.

## My cut line
**Will certainly finish:**
- Client booking form (`/book`) with service and stylist selection.
- Operating hours (09:00–17:00), formatting (`YYYY-MM-DD HH:MM`), duplicate check, and stylist conflict validation.
- Staff dashboard queue (`/staff`) displaying pending, confirmed, and completed appointments.
- State transitions (`booked` → `confirmed` → `arrived` → `completed`, plus `cancelled` and `no_show`).
- SQLite persistence (`appointments.db`) surviving application restarts.
- Sandboxed reminder notification logging (`reminders.log`).

**Drop first:**
- Client self-rescheduling screen.
- Custom stylist break management.
- Automated reminder countdown ticker.

## Difficulty Bar: the feature that meets each row

| # | Requirement | My feature (name the file or page) |
|---|---|---|
| 1 | Two or more roles with different views | `/book` page for clients; `/staff` dashboard for front-desk staff and stylists (`app.py`) |
| 2 | A tracked state with rules | `booked` → `confirmed` → `arrived` → `completed` (plus `cancelled`, `no_show`); only staff can confirm or complete (`app.py`) |
| 3 | Persistence | SQLite database `appointments.db` saving appointments and service catalog across restarts (`database.py` / `app.py`) |
| 4 | Staff dashboard or queue | Front-desk queue (`/staff`) updating dynamically with new bookings and conflict warnings (`app.py`, `templates/staff.html`) |
| 5 | A fake external step | Appointment reminders appended to local `reminders.log` instead of sending real SMS or email |
| 6 | A human checkpoint | Front desk manually inspects pending bookings on `/staff` and clicks Confirm/Reject before moving to `confirmed` |
| 7 | Known-answer tests plus one engineered failure | `tests/known-answer/run.py` running `cases.json`, plus engineered failure test on overlapping stylist bookings (`evidence/engineered-failure.md`) |

**Three complexity-menu items and where they appear:**
1. **Persistent store:** SQLite database `appointments.db` holding appointments, services, and state history.
2. **Human-approval step:** Front-desk staff checkpoint on `/staff` to review and confirm or reject bookings.
3. **Role-based access control:** Client role restricted to booking/cancelling; staff role controls confirmation, arrival, and completion.
4. **Monitoring / audit log:** Append-only log recording actor, previous state, new state, and rejected requests (`reminders.log` / audit events in DB).

## How `run` talks to my app
`tests/known-answer/run.py` talks directly to the application via the Flask test client (`app.test_client()`) or programmatic application hooks in `app.py`. The hooks translate internal responses and database records to the common contract vocabulary (`accepted`, `conflict`, `bad_date_format`, `after_close`, `duplicate_request`, `not_permitted`, `illegal_move`).

## Data-safety boundary
All client names, stylists, and booking requests are fictional (e.g., `client-a`, stylists Ana and Ben). The reminder notification step writes to a local text file `reminders.log` instead of invoking any external SMS or email API. No real phone numbers, emails, payment cards, or external credentials are used or stored.

