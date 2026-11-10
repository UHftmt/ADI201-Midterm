# Salon Appointment Desk (Idea 2, Team 3, Vinh Hoang)

A small web app for a made-up salon. A client asks for an appointment; the front desk sees it in a queue and confirms it; the app refuses requests that break the salon's rules.

> Draft written on Nov 9 before the build (Step 1.2). Feature and file names are a best guess and get corrected after the build.

## Run it
```
python3 app.py
```
Then open `http://localhost:5000/book` (client page) and `http://localhost:5000/staff` (front-desk page).

## Python and version
Python 3.11 or newer (built on 3.12). One package, Flask: `pip install -r requirements.txt`.

## Test it
```
python3 tests/known-answer/run.py
```
It prints one `PASS` or `FAIL` line per case.

## My cut line
**Will certainly finish:** client booking page; the four rejection rules from `fixtures/idea2-appointments/RULES.md` (`bad_date_format`, `after_close`, `conflict`, `duplicate_request`); front-desk queue; the six states with role limits; SQLite storage that survives a restart; a history of every action; reminders written to a local file.

**Drop first:** rescheduling an existing booking; a per-stylist calendar view; login accounts (the role is picked on the page instead).

## Difficulty Bar: the feature that meets each row
| # | Requirement | My feature (name the file or page) |
|---|---|---|
| 1 | Two or more roles with different views | `/book` for the client, `/staff` for the front desk (`app.py`, `templates/`) |
| 2 | A tracked state with rules | `booked`, `confirmed`, `arrived`, `completed`, `no_show`, `cancelled`; the table of allowed moves per role is in `rules.py` |
| 3 | Persistence | SQLite file `salon.db`, tables `bookings`, `seen_requests`, `history` (`store.py`) |
| 4 | Staff dashboard or queue | `/staff` lists every booking the clients made, newest state first, with the buttons staff may press |
| 5 | A fake external step | "Send reminder" appends one line to `outbox/reminders.log`; nothing leaves the computer |
| 6 | A human checkpoint | a booking stays `booked` until a staff member presses Confirm on `/staff` |
| 7 | Known-answer tests plus one engineered failure | `tests/known-answer/cases.json`, `tests/known-answer/run.py`, `evidence/engineered-failure.md` |

**Three complexity-menu items and where they appear:** persistent store (`store.py`, `salon.db`); human-approval step (Confirm on `/staff`); audit log (`history` table, shown at `/staff/history`).

## State rules (who may move what)
| From | To | Who |
|---|---|---|
| (new request) | `booked` | client |
| `booked` | `confirmed` | staff |
| `booked` | `cancelled` | client or staff |
| `confirmed` | `arrived` | staff |
| `confirmed` | `no_show` | staff |
| `confirmed` | `cancelled` | client or staff |
| `arrived` | `completed` | staff |

A move in this table tried by the wrong role gives `not_permitted`. A move that is not in this table gives `illegal_move`.

## How `run` talks to my app
`run.py` uses the Flask test client, so it calls the same routes the pages use. My internal words are the contract's common words, so the mapping table is one-to-one; it is at the top of `run.py`.

## Data-safety boundary
Every client, stylist and booking is made up (`client-a`, `Ana`, `Ben`). No accounts, no passwords, no keys. No message is ever sent: reminders only go to a local text file.
