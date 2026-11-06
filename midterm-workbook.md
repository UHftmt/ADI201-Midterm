# Midterm Workbook

Type your answers here, in your own words. Short is fine. Where a section says "evidence", put the detail in the named file and summarize here. Do not paste AI output as answers.

| Section | Summarize here | Full detail |
|---|---|---|
| 1 Setup and cut line | Cut line, seven rows | `README.md` |
| 2 Tests first | What your cases cover | `tests/known-answer/cases.json` |
| 3 Plan review | Plan summary, what you rejected | `ai-use-log.md` |
| 4 Engineered failure | Prediction, result | `evidence/engineered-failure.md` |
| 5 Merge (Phase 2) | Base, what you dropped | `evidence/merge-decision-log.md` |
| 6 Presentation prep | Your contribution, your challenge answers | (this file) |
| 7 Reflection | Answers | (this file) |
| ADI501 | Summary | `evidence/governance-table.md`, `baseline-vs-pilot.md`, `support-burden.md`, `thresholds.md` |

## Section 1: Setup and cut line

**1.1** My idea, team, and one-sentence user and job: Idea 2, Team 3; clients booking salon appointments online and front-desk staff needing a conflict-free, tracked schedule.

**1.2** Features I will certainly finish: Client booking form (`/book`), operating hours (09:00–17:00) and conflict validation, staff queue/dashboard (`/staff`), state transitions (`booked` → `confirmed` → `arrived` → `completed`), SQLite persistence, and sandboxed reminder logger.

**1.3** Features I will drop first: Client self-rescheduling screen, custom stylist break management, and automated reminder countdown ticker.

**1.4** For each Difficulty Bar row, the exact feature that meets it (one line per row, 1 to 7):
1. Roles: `/book` page for clients; `/staff` dashboard for front-desk staff and stylists.
2. State machine: `booked` → `confirmed` → `arrived` → `completed` (plus `cancelled`, `no_show`); only staff may confirm/complete.
3. Persistence: SQLite database `appointments.db` saving bookings and service catalog.
4. Staff dashboard/queue: `/staff` queue updating dynamically with new bookings and conflict warnings.
5. Sandboxed external step: Local text file `reminders.log` recording outgoing reminder messages with no real SMS/email API.
6. Human checkpoint: Front-desk manager manually reviews pending `booked` items and clicks Confirm/Reject.
7. Known-answer tests + engineered failure: `cases.json` suite plus engineered stylist conflict test in `evidence/engineered-failure.md`.

## Section 2: Tests first

**2.1** Which fixture rows are seeded failures, and how did I find them without asking an agent to list them?
- `B-002`: Overlaps with `B-001` (Ana, 09:00–09:45) starting at 09:30 (`conflict`).
- `B-005`: Starts at `11/02/2026 10:30`, violating the required `YYYY-MM-DD HH:MM` format (`bad_date_format`).
- `B-006`: Overlaps with `B-004` (Ben, 09:30–10:15) starting at 10:00 (`conflict`).
- `B-007`: Service S4 (30 min) starts at 16:45 and ends at 17:15, which is after 17:00 closing (`after_close`).
I found them by manually reading `RULES.md` and `services.csv`, calculating start/end times in my head for each row of `booking-requests.csv` in file order, and checking format and closing constraints.

**2.2** One total or count I computed by hand, with the arithmetic: *(e.g., "Ana: 45 + 20 = 65 minutes booked")*
Ana booked minutes: B-001 (S1 = 45 min) + B-003 (S3 = 20 min) = 45 + 20 = 65 minutes. (B-002 was rejected for conflict so it occupies 0 minutes, and B-007 was rejected for after_close).

**2.3** Did my `tests:` commit come before my first build commit? Paste the two `git log --oneline` lines.
Yes, the tests commit came directly before the first build commit:
```text
0c9a02c build(slice1-3): storage, validation engine, and state machine hooks
783a58b tests: known-answer cases written before build
```

## Section 3: Plan review

**3.1** The first three slices the agent proposed, in one sentence each:
- Slice 1: Implement SQLite schema (`services`, `appointments`, `audit_log`), load `services.csv`, and connect the runner hooks (`new_app`, `restart_app`, `do_step`) in `tests/known-answer/run.py`.
- Slice 2: Implement validation rules to enforce opening hours (09:00–17:00), `YYYY-MM-DD HH:MM` date formatting, duplicate `request_id` detection, and stylist overlap conflict checks.
- Slice 3: Enforce role-based access control (`client` vs `staff`) and valid state transitions (`booked` → `confirmed` → `arrived` → `completed`, plus `cancelled` and `no_show`) with audit logging.

**3.2** One thing in the plan I rejected or changed, and why:
I rejected integrating live external email/SMS APIs (such as Twilio or SendGrid) and background scheduler daemons proposed for notifications. Real sends violate the data-safety boundary in the project contract and cap the grade at 70/100, so I insisted on a sandboxed local file logger (`reminders.log`).

**3.3** One command I did not approve, and the row of the command decision table that explains it:
I did not approve `pip install twilio sendgrid schedule` (row 1 of the Command Decision Table in `ai-use-log.md`), because installing external notification SDKs introduces unnecessary internet dependencies and the risk of accidental live transmissions.

## Section 4: Engineered failure

**4.1** What I broke and what I predicted:

**4.2** What happened, and was my prediction right? What did I learn?

## Section 5: Merge (Phase 2)

**5.1** Which build was the base and why (about the system, not the person):

**5.2** One case that failed after porting a component, and what I did:

**5.3** One thing the transfer trial teammate got stuck on:

## Section 6: Presentation prep

**6.1** The commit that shows my own contribution (hash and one sentence):

**6.2** Pick a component I did not write. Explain in three sentences what it does and one thing that would break if it were removed:

**6.3** If the instructor asks me to add a new state live, which three files change?

## Section 7: Reflection

**7.1** One thing the agent got wrong that my known-answer tests caught:

**7.2** One thing I would do differently if I started again:

**7.3 (required) Job link.** Name one real job task this tool maps to (for example, "a front-desk manager checks a booking for conflicts") and one thing it would still need before anyone could use it for real work (for example, real data, accounts, or a human review step):

## ADI501 additions (summaries)

**A.1** The biggest governance risk in my tool and what I did about it:

**A.2** My baseline and pilot numbers (label measured or estimate), and what they do not prove:

**A.3** The thing most likely to break in six months, and who would fix it:

**A.4** My thresholds, and why those numbers:
