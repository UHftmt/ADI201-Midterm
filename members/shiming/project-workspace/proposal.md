# Project proposal — Juniper Studio

> **Team working draft, not submission-ready prose.** The assignment says not to paste AI output as answers. Rewrite these notes together in your own words, confirm the baseline and risk, and freeze the test cases before your next build.

## 1. Idea, team, and you

- Idea number: 2
- Team number: 3
- Team members: Shiming, Vinh, Yuhe
- Course: ADI201

## 2. User and job

**Team notes:** Customers request a salon appointment; front-desk staff review the queue, confirm or move bookings, and record arrival outcomes. Providers check their own schedules.

## 3. Workflow

1. Customer chooses a fictional service, provider, date, and time, then submits a request.
2. The system checks opening hours and provider conflicts, saves the request, and adds a reminder entry to a local log.
3. Front desk reviews the queue and confirms the request or moves it to an available slot.
4. Front desk records arrival, completion, or no-show; provider checks their schedule.

## 4. Success measure and baseline

- Measure: percentage of accepted bookings with no overlapping appointment for the same provider.
- Method: run a fixed set of 10 booking cases, including conflicting and adjacent time slots; count accepted bookings that have no overlap. The automated test set currently checks the conflict and adjacent-slot cases.
- Baseline: **estimate: 90%** conflict-free bookings in a small manual-workflow sample. This is a planning estimate, not observed data; the team must measure and replace it before reporting results.
- Target: 100% of accepted test bookings have no provider/time conflict.

## 5. Smallest meaningful version (cut line)

- Must finish: customer booking form; conflict and business-hour checks; SQLite persistence; front-desk queue with confirmation, status updates, and rescheduling; provider schedule view; reminder log with no messages sent; automated tests.
- Cut first: login/permissions, live email or SMS, payments, external calendar/API integrations, multiple locations, and recurring appointments.

## 6. Difficulty-bar self-score

| Requirement | Met? | Exact feature |
|---|---|---|
| Two or more roles with different views | Yes | Customer `/customer`, staff `/frontdesk`, and provider `/provider` views. These are demo views, not authenticated accounts. |
| Tracked state with named steps and rules | Yes | `booked → confirmed → arrived → completed`; `booked`/`confirmed` can also become `no-show`; invalid transitions are rejected. |
| Persistence after restart | Yes | SQLite stores appointments, reminder entries, and audit events in `instance/appointments.sqlite3`. |
| Staff queue updated by user side | Yes | Customer submissions appear in the front-desk queue. |
| Fake external step | Yes | A scheduled reminder message is written to SQLite; no email or SMS is sent. |
| Human checkpoint | Yes | Front desk must explicitly confirm or move the request; it is not automatically confirmed. |
| Known-answer test set plus engineered failure | **Partial — timing requirement not met retroactively** | `tests/test_app.py` checks expected booking, status, persistence, and move outcomes; it deliberately tries an overlapping booking and expects rejection. These tests were added during the prototype build, not before it. Freeze and timestamp a known-answer set before the next implementation iteration; do not claim it was written before this prototype. |

Complexity-menu items: persistent SQLite store (`appointments`); human approval (`/frontdesk`); automated test suite (`tests/test_app.py`); audit log (`audit_log` table); role-based views (demo routes).

## 7. Data and safety statement

**Team notes:** Use fictional names and appointments only; collect no real health or contact information. The reminder step only writes a local log entry. There is no real messaging, payment, calendar integration, or authentication; the demo role pages are not access controls and must stay local/classroom-only.

## 8. Top risk and fallback

- Top risk: the team may not have time to test scheduling edge cases, especially overlaps when the front desk moves a booking.
- Fallback: keep the fixed 30-minute slots and two fictional providers; if rescheduling bugs remain, retain booking and conflict checks but drop provider changes and clearly document that cut.
