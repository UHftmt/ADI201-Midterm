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

## Command decision table (use from Phase 1 onward)

Before you let an agent run a command, fill in a row. If the "Risk" cell says anything you cannot explain, the decision is **do not run**.

| Command | Target (files or system) | Purpose | Risk | Recovery | Decision |
|---|---|---|---|---|---|
| *e.g., `pip install flask`* | *e.g., this project's virtual environment* | *e.g., install the web library* | *e.g., installs a package from the internet* | *e.g., delete the virtual environment folder* | *e.g., run* |

## Stop signs (do not run the command; ask first)

- It deletes files outside your project folder.
- It needs an API key, password, or login that you would have to paste.
- It sends a real message, email, or payment.
- You cannot say in one sentence what it does.
