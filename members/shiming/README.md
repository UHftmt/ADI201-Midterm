# Juniper Studio appointment demo

This repository contains a local, fake-data booking app for a fictional salon. It keeps all customer and staff data on the machine only, and it does not send real emails or SMS messages.

## Run locally

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in a browser. The app uses a Flask test client in the test harness (`tests/test_app.py`) and the SQLite database is stored in `instance/appointments.sqlite3`.

## Cut line and difficulty bar

Cut line (must finish):
- customer booking request form
- provider conflict checks and business-hours validation
- front-desk queue with confirm/move workflow
- status transitions: booked → confirmed → arrived → completed, with no-show allowed from booked/confirmed
- SQLite persistence and restart-safe data
- provider schedule view
- reminder log that records a fake reminder without sending it
- automated known-answer tests and one engineered-failure regression

Dropped first if time runs short:
- real authentication or role login
- real email/SMS delivery
- payments or booking charges
- recurring appointments or multi-location support
- external calendar/API integrations

| Feature | Complexity menu item | Notes |
|---|---|---|
| Customer booking flow | SQLite persistent store | Save the request, validate provider/date/time, and create a reminder log entry |
| Front desk approval checkpoint | Human approval | Staff must explicitly confirm or move before the appointment is treated as active |
| Provider conflict rules | State machine rules | Booked and confirmed appointments block overlapping times for the same provider |
| Staff queue updates | Role-based views | Customer submissions appear immediately in the front-desk queue |
| Provider schedule view | Role-based views | Providers see only their own schedule |
| Reminder logging | Fake external step | Reminder is written to SQLite, never sent to a real channel |
| Restart persistence | SQLite persistent store | App state remains available after app recreation |

## Data safety boundary

Everything in this demo is fictional. The app has no credentials, no authentication system, no real external API keys, and no real message sends. Customer names and appointment details are placeholder values only. The reminder step records a scheduled log entry instead of sending an external message.

## Known-answer test command

```sh
python -m unittest discover -s tests -v
```

This command runs the known-answer checks and the engineered-failure regression. The app is tested through a Flask `test_client()` and a temporary SQLite database. No real email, SMS, payment, or external calendar calls are involved.
