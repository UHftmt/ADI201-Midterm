# AI-Use Log

**How to use this file**

- Add one row **at the time** you use AI, not afterward. A row takes about one minute.
- Copy the example rows' style. Each row must say what AI proposed, what you decided, and how you checked it.
- Pass condition: every AI use in this project has a row; every row names a verification method and a decision you made yourself; at least one row (from Phase 1 onward) records something you **rejected**.

## Log

| # | Date | Phase | Tool / agent | Task or prompt (short) | What it proposed | I accepted / revised / rejected | How I verified | My decision and any open problem |
|---|---|---|---|---|---|---|---|---|
| 1 | Nov 03 | 1 Setup | Antigravity | Idea 2 cut line and difficulty bar planning | Proposed core workflow, cut line with drop-first list (rescheduling screen, custom breaks), and 7 difficulty features | Accepted core; rejected complex client self-rescheduling | Checked against midterm-project-contract.md difficulty bar requirements | Kept scope tight to finish on time; no open problems |

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
