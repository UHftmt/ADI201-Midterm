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

**2.2** One total or count I computed by hand, with the arithmetic: *(e.g., "Ana: 45 + 20 = 65 minutes booked")*

**2.3** Did my `tests:` commit come before my first build commit? Paste the two `git log --oneline` lines.

## Section 3: Plan review

**3.1** The first three slices the agent proposed, in one sentence each:

**3.2** One thing in the plan I rejected or changed, and why:

**3.3** One command I did not approve, and the row of the command decision table that explains it:

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
