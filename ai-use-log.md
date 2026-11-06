# AI-Use Log

**How to use this file**

- Add one row **at the time** you use AI, not afterward. A row takes about one minute.
- Copy the example rows' style. Each row must say what AI proposed, what you decided, and how you checked it.
- Pass condition: every AI use in this project has a row; every row names a verification method and a decision you made yourself; at least one row (from Phase 1 onward) records something you **rejected**.

## Log

| # | Date | Phase | Tool / agent | Task or prompt (short) | What it proposed | I accepted / revised / rejected | How I verified | My decision and any open problem |
|---|---|---|---|---|---|---|---|---|
| 1 | Nov 03 | 1 Setup | Antigravity | Idea 2 cut line and difficulty bar planning | Proposed core workflow, cut line with drop-first list (rescheduling screen, custom breaks), and 7 difficulty features | Accepted core; rejected complex client self-rescheduling | Checked against midterm-project-contract.md difficulty bar requirements | Kept scope tight to finish on time; no open problems |
| 2 | Nov 06 | Phase 1 Setup | Antigravity | Review instructions, create README.md and Phase 1 roadmap | Proposed 7-step guide and draft README.md with Flask stack | Accepted Flask stack and README cut line | Verified against proposal.md and contract section 1 | Proceed to Step 2 (tests first); no open problems |
| 3 | Nov 06 | Phase 1 Tests | Antigravity | Draft cases.json covering the 5 contract types | Proposed 9 test cases in common vocabulary | Accepted 9 cases; confirmed hand arithmetic (Ana 65m) | Checked against RULES.md, booking-requests.csv, and contract section 3 | Committed tests before build; no open problems |
| 4 | Nov 06 | Phase 1 Plan | Antigravity | Slice planning and command authorization | Proposed 4 slices and external messaging package | Accepted 4 slices; rejected external messaging package (Twilio/SendGrid) | Verified against contract rules on sandboxing & data safety | Kept sandboxed reminders log; logged rejected command |
| 5 | Nov 06 | Phase 1 Failure Drill | Antigravity | Engineered failure experiment on stylist conflict check | Proposed bypassing interval check in domain.py | Accepted approach; confirmed exact failure output matches prediction | Ran python3 tests/known-answer/run.py, verified failure, restored fix, added repeat test | Repeat test PASS; no open problems |
| 6 | Nov 06 | Phase 1 Docs | Antigravity | Complete ARCHITECTURE.md, automation-leadin.md, and workbook reflection | Proposed component mapping and job link answer | Reviewed and accepted mapping | Verified file paths and state tables match app code exactly | Ready for final verification and tagging |

## Command decision table (use from Phase 1 onward)

Before you let an agent run a command, fill in a row. If the "Risk" cell says anything you cannot explain, the decision is **do not run**.

| Command | Target (files or system) | Purpose | Risk | Recovery | Decision |
|---|---|---|---|---|---|
| `pip install twilio sendgrid schedule` | Python environment / internet | Proposed external packages for customer notifications | Risk of live sends violating contract data-safety boundary | `pip uninstall` packages | **Do not run (Rejected)** |
| `python3 tests/known-answer/run.py` | Local repository test runner | Execute known-answer test cases against application hooks | Low risk: test execution on local SQLite db | Fix failing test or code | **Run (Approved)** |
| `git commit -m "..."` | Git repository index/history | Record verified milestones and slice commits | Low risk: standard version control | `git reset HEAD~1` if needed | **Run (Approved)** |

## Stop signs (do not run the command; ask first)

- It deletes files outside your project folder.
- It needs an API key, password, or login that you would have to paste.
- It sends a real message, email, or payment.
- You cannot say in one sentence what it does.
