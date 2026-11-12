# AI-Use Log

**How to use this file**

- Add one row **at the time** you use AI, not afterward. A row takes about one minute.
- Copy the example rows' style. Each row must say what AI proposed, what you decided, and how you checked it.
- Pass condition: every AI use in this project has a row; every row names a verification method and a decision you made yourself; at least one row (from Phase 1 onward) records something you **rejected**.

## Log

| # | Date | Phase | Tool / agent | Task or prompt (short) | What it proposed | I accepted / revised / rejected | How I verified | My decision and any open problem |
|---|---|---|---|---|---|---|---|---|
| 1 | Nov 9 | 1 Setup | Claude Code | "Set up my repository from the starter as Step 1.1 says" | Copied the contract files, templates and Idea 2 fixtures into `midterm-vinh/` and made the setup commit | Accepted | `git log --oneline` shows one commit; compared the file list with Step 1.1 | Kept. It also copied the merge and presentation checklists, which Step 1.1 does not list; harmless |
| 2 | Nov 9 | 1 Cut line | Claude Code | "Draft my README cut line, Difficulty Bar table and state rules" | A cut line, seven feature rows, three menu items, a who-may-move-what table | TO DECIDE (Vinh) | TO DO: read each row against the contract and RULES.md | TO DO |
| 3 | Nov 9 | 1 Tests first | Claude Code | "Write my cases.json" | It declined to write expected values, because Step 1.3 says an agent may not produce them; it gave me a worksheet with the steps filled in and the answers blank | Accepted | Read Step 1.3 in START-HERE.html | I fill in every `expected` and `how_computed` myself |
| 4 | Nov 10 | 1 Tests first | Claude Code | "Take the answers I chose on the answer sheet and put them into cases.json" | It copied my 18 answers into the file unchanged, turned the fixture rows I ticked into steps, and listed the cases where my answer disagreed with a written rule or with another answer of mine. It did not give me the values | Accepted the copy; the listed cases are still open | Read the printed summary of the file against the list I sent; `grep -c "FILL IN"` gives 0 | Committed as `tests: known-answer cases written before build`. Open: case 17 has no outcome, most `how_computed` lines are empty, and I have not yet re-checked the flagged cases |
| 5 | Nov 10 | 1 Build, slice 1 | Claude Code sub-agent | "Build `rules.py` (move table, request checks) and `store.py` (SQLite) from RULES.md and my README state table; do not read cases.json" | Two files, plus 12 choices the brief had not fixed (for example: a refused request still uses up its `request_id`; a start before 09:00 is answered `after_close`) | Accepted | The agent's 67-line check script, re-run by the main session: 0 failures | Kept. Open: a start before 09:00 has no contract word of its own |
| 6 | Nov 10 | 1 Build, slice 2 | Claude Code sub-agent | "Build the Flask pages for client and staff, a JSON API, and the reminder outbox on top of slice 1" | `app.py`, five templates, `requirements.txt`. It left reminders out of the history table because `store.py` had no method for it | Revised: the reminder gap was not accepted and was sent back in slice 3 | Its check script (49 checks, all pass) re-run by the main session; four pages answered 200 on a live server | Kept the pages. Stylists `Ana` and `Ben` are a fixed list in `app.py` |
| 7 | Nov 10 | 1 Build, slice 3 | Claude Code sub-agent | "Write the three hooks in `run.py`; add reminders to the history; never edit cases.json or bend the app to pass a case" | The hooks, a `log_event` method, and a report of 10 PASS and 8 FAIL. It also listed what the app answers for each failing case | Accepted the code. **Rejected** using its list to overwrite my expected values: Step 1.3 says the answers are mine | `python3 tests/known-answer/run.py` run by the main session: 10 PASS, 8 FAIL, exit code 1 | The 8 failing cases stay as I wrote them until I re-work each one by hand from RULES.md and the README table |
| 8 | Nov 10 | 1 Docs | Claude Code | "Fill in ARCHITECTURE.md and correct the README from the finished code" | A one-page architecture draft and six README corrections (page order, reminder path, test note) | TO DECIDE (Vinh) | TO DO: read both against the code and reword the architecture page | TO DO |
| 9 | Nov 12 | 1 Tests, re-work | Claude Code | "Make a page where I fix the failing cases, then put my answers into the real test" | A local answer page with the state table, request checks and fixture rows beside each case, and hints that explain a rule without giving the value; it then copied my answers into cases.json unchanged. When case 17 still failed it pointed me back at a rule, and asked me once for the outcome word | Accepted the page and the copy. Kept my own outcome word `conflict` for case 17 | `git diff` shows only my answers changed; `python3 tests/known-answer/run.py`: 17 PASS, 1 FAIL | Committed as `c43a12c` and `f009a0f`. Later the same day I changed case 17's outcome to `accepted` myself: 18 PASS. Open: case 13 still uses the same row as case 14 |

## Command decision table (use from Phase 1 onward)

Before you let an agent run a command, fill in a row. If the "Risk" cell says anything you cannot explain, the decision is **do not run**.

| Command | Target (files or system) | Purpose | Risk | Recovery | Decision |
|---|---|---|---|---|---|
| `python3 tests/known-answer/run.py` | temporary folders only | run the known-answer cases | none: each case uses its own temporary database | nothing to undo | run |
| `python3 app.py` with `SALON_DB` set to a temporary file | port 5000 on this computer, one temporary file | check that the four pages load | port 5000 could already be in use | stop the process by its id | run |
| `pip install flask` | the shared Python on this Mac | install the web library | changes a Python used by other courses | none easy | **do not run**: Flask 2.1.3 was already installed |

## Stop signs (do not run the command; ask first)

- It deletes files outside your project folder.
- It needs an API key, password, or login that you would have to paste.
- It sends a real message, email, or payment.
- You cannot say in one sentence what it does.
