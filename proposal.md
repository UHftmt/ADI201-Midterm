# Midterm Proposal

**How to use this file**

- Replace each *e.g.* example with your own text. Delete the example when you are done.
- Keep the whole file to about one page (not counting the table in section 6).
- Write in your own words. Do not paste AI output as your answers. Log any AI help in `ai-use-log.md`.
- Pass condition: every section filled; section 6 has seven rows that each name a feature; you can explain every line out loud.

## 1. Idea, team, and you

| Field | Your answer |
|---|---|
| Idea number (1–5) | 2 (Appointment and intake for a fictional salon or clinic) |
| Team number | Team 3 |
| Your name | Yuhe Luo |
| Course | ADI201 |

## 2. User and job

Clients who want to book salon/service appointments online without phone tag, and front-desk staff who need a conflict-free schedule with clear appointment statuses.

## 3. Workflow

Five or fewer steps, from the user's point of view.

1) Client selects a service, stylist, date, and start time on the booking page.
2) System checks operating hours (09:00–17:00), formatting, and stylist conflicts; if valid, saves booking in `booked` state.
3) Front-desk staff reviews the queue on their dashboard and marks the appointment `confirmed`.
4) At appointment time, staff marks the client `arrived`, then `completed` (or records `no_show` / `cancelled`).

## 4. Success measure and baseline

| Field | Your answer |
|---|---|
| The one number I will measure | Number of double-booking conflicts prevented out of 10 sample requests |
| How I will measure it | Automated test script (`run.py`) evaluating conflict detection against fixture requests |
| Baseline today (label it *measured* or *estimate*) | 0 conflicts caught automatically using paper appointment book (estimate) |

## 5. Smallest meaningful version (cut line)

| I will certainly finish | I will drop first if I run out of time |
|---|---|
| Client booking form, operating hours and conflict validation, staff dashboard queue, state transitions (`booked` → `confirmed` → `arrived` → `completed`), SQLite persistence, and sandboxed reminder logging | Client self-rescheduling screen, custom stylist break management, automated reminder countdown ticker |

## 6. Difficulty-bar self-score

Each row must name an exact feature in **your** design. If you cannot name one, the row is **not met**: add a feature.

| # | Requirement | Met? (yes / no) | The exact feature that meets it |
|---|---|---|---|
| 1 | Two or more user roles with different views | yes | `/book` page for clients to submit bookings; `/staff` dashboard for front desk and stylists to view queues |
| 2 | A tracked state with rules | yes | `booked` → `confirmed` → `arrived` → `completed` (or `no_show` / `cancelled`); only staff can confirm or complete |
| 3 | Persistence | yes | SQLite database `appointments.db` saving appointments and service catalog across restarts |
| 4 | A staff-facing dashboard or queue updated from the user side | yes | Front-desk queue (`/staff/queue`) that updates when clients submit new bookings and flags stylist conflicts |
| 5 | A fake external step | yes | Appointment reminders appended to local `reminders.log` instead of sending real SMS or email |
| 6 | A human checkpoint | yes | Front desk manually inspects pending bookings and resolves conflicts before moving to `confirmed` |
| 7 | Known-answer tests plus one engineered failure | yes | `tests/known-answer/run.py` running `cases.json`, plus engineered failure test on overlapping stylist bookings |

**Complexity menu (name at least three and say where each appears):**

1. **Persistent store**: SQLite database `appointments.db` holding appointments, services, and state history.
2. **Human-approval step**: Front-desk staff checkpoint on `/staff` to review and confirm or reject bookings.
3. **Role-based access**: Client role restricted to booking/cancelling; staff role controls confirmation, arrival, and completion.
4. **Monitoring or audit log**: Append-only log recording actor, previous state, new state, and rejected requests.

## 7. Data and safety statement

All client names, stylists, and bookings are fictional (names like "client-a", stylists "Ana" and "Ben"). The reminder notification step writes to a local text file `reminders.log` instead of sending real SMS or email. No real phone numbers, emails, payment cards, or external credentials are used or stored.

## 8. Top risk and fallback

Risk: Complex datetime parsing or timezone edge cases causing false conflicts or allowing bookings after closing. Fallback: Enforce strict `YYYY-MM-DD HH:MM` parsing and compare fixed minute offsets without external calendar API dependencies.

## 9. Pilot question (ADI501 only)

N/A (Enrolled in ADI201)
