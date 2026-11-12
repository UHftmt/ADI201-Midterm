# AI-Use Log

> The entries below reconstruct AI use from this Copilot session on Oct 27, 2026; they were not recorded at the moment of each use. Keep adding a row immediately for future use and have the team verify the decisions.

## Log

| # | Date | Phase | Tool / agent | Task or prompt (short) | What it proposed / produced | Team decision | How verified | Open problem / next action |
|---|---|---|---|---|---|---|---|---|
| 1 | Oct 27, 2026 | 0 Proposal | Copilot SDK in VS Code | Create the proposal workspace | Created an empty proposal worksheet with the eight required sections | Used as a worksheet; team details were supplied by Shiming | Read the worksheet and compared it with the requested section list | |
| 2 | Oct 27, 2026 | 1 Prototype | Copilot SDK in VS Code | Build a salon appointment app using Flask and SQLite | Created customer, front-desk, and provider views; conflict checks; status transitions; SQLite persistence; reminder/audit logs; tests | Flask + SQLite was selected by the user. The project brief requires reminders to be logged, never sent, so live email/SMS was left out | Inspected implementation and ran the unit tests; all 8 tests passed | Demo routes have no authentication; keep fake data/local use only |
| 3 | Oct 27, 2026 | 1 Prototype | Copilot SDK in VS Code | Fix observed test and runtime issues | Fixed database access, booking conflict reporting, schedule test expectation, and transaction ordering | Changes were applied to the prototype | Re-ran `python -m unittest discover -s tests -v` with the configured Python 3.12 interpreter; 8 tests passed | The known-answer tests were added during the prototype build, not before it; freeze a test set before the next build iteration |
| 4 | Oct 27, 2026 | 0 Proposal / tooling | Copilot helped draft the proposal and record tool/test results. The team will review and revise the proposal, confirm the estimate, and complete its own credential-rule acknowledgement. | | | | |
| 5 | Nov 8, 2026 | 1 Phase 1 setup and build | Copilot SDK in VS Code | Set up the midterm repository, freeze known-answer cases, bring in the salon appointment app, and validate the suite | Created the repo scaffold, test-first case file, and app implementation with SQLite persistence and the conflict rules | Kept the project local-only and fake-data, with the appointment tests run after the case freeze | `. .venv/bin/activate && python -m unittest discover -s tests -v` returned `OK` for 9 tests | None; the app remains a local demo and does not include real sends |

## Command decision table

| Command / action | Target | Purpose | Risk | Recovery | Decision / result |
|---|---|---|---|---|---|
| `pip install Flask` (workspace Python package tool) | Configured Python environment | Make the Flask test import available | Installs a package; the first configured interpreter did not match the environment used by the terminal test | Re-run in the selected environment or use a project virtual environment; no project data was changed | Used; subsequently configured the Python 3.12 interpreter and verified tests there |
| `/home/ming99/miniforge3/bin/python -m unittest discover -s tests -v` | Project test suite | Validate the appointment flows and conflict case | Executes local tests and writes temporary test databases | Tests use temporary directories and clean them up | Run; all 8 tests passed |
| `/home/ming99/miniforge3/bin/python --version` | Selected Python interpreter | Check Python availability/version | Read-only | None needed | Run; printed `Python 3.12.12` |
| `git --version` | Git executable | Check Git availability/version | Read-only | None needed | Run; printed `git version 2.53.0` |

No live message, email, payment, API key, password, or login was used.
