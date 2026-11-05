# Midterm Concepts

Read this when a term in Start Here is new. Each entry says what the term is, why it matters, where it appears in your build, and gives you a prompt to ask your agent. The prompts are for understanding. They are not for producing your answers.

## Known-answer test

**What it is:** A test whose expected result you decided, by hand, before the code existed.

**Why it matters:** If the agent writes both the code and the expected values, a wrong rule passes its own test. Your hand-computed answers are the only independent check.

**In your build:** `tests/known-answer/cases.json`, with a `how_computed` line per case. The git history must show it came first.

**Ask your agent:** "Explain why a test written after the code can hide a bug that a test written before it would catch. Use a 10-line example."

## Cut line

**What it is:** The line between the features you will certainly finish and the ones you drop first.

**Why it matters:** You are graded against your own cut line. A smaller, finished tool earns more than a larger, broken one.

**In your build:** The top of your `README.md` (Idea 5: your approved proposal).

**Ask your agent:** "How do I decide which of this list of features to cut first if I run out of time? Ask me questions instead of deciding for me."

## State machine

**What it is:** A list of states and the only moves allowed between them, with who may make each move.

**Why it matters:** Bugs in tracked items are almost always an illegal move that nothing stopped, such as a customer marking their own order ready.

**In your build:** The states in the contract vocabulary and the `role_not_allowed` cases in `cases.json`.

**Ask your agent:** "Draw a state machine for a library book (available, borrowed, overdue, lost) and list three moves that must be illegal."

## Human checkpoint

**What it is:** A point where automation stops and a named person approves, corrects, or overrides before anything final happens.

**Why it matters:** A button that does nothing, or a requester who can approve their own request, is not a checkpoint.

**In your build:** Difficulty Bar row 6.

**Ask your agent:** "Give two examples of a real approval step and two that only look like one."

## Audit log

**What it is:** An append-only record of who changed what, from which state to which, and when.

**Why it matters:** It is how you explain, in Phase 3, why the system is in the state it is in.

**In your build:** The monitoring or audit-log item on the complexity menu, and Part 3 of the lead-in lab.

**Ask your agent:** "Why should an audit log be written in the same step as the change it records?"

## Persistence

**What it is:** Data that survives stopping and restarting the program, for example in a SQLite file.

**Why it matters:** Memory-only data vanishes on restart, and a tool that forgets its orders is not a tool.

**In your build:** The restart check case in `cases.json`.

**Ask your agent:** "What is the smallest SQLite example that saves a row and reads it back after the program restarts?"

## Sandboxing the external step

**What it is:** Replacing a real action (payment, email, text) with a safe stand-in such as a log file or a frozen fixture.

**Why it matters:** One real send or live key ends the project at a 70/100 cap, and can cause real harm.

**In your build:** Difficulty Bar row 5 and your data-safety boundary.

**Ask your agent:** "Show how to write an 'email' to a log file instead of sending it, so the rest of the code does not know the difference."

## Engineered failure

**What it is:** A failure you cause on purpose, after predicting what will happen.

**Why it matters:** Predicting first shows whether you understand the system. A surprise is what you learn from.

**In your build:** `evidence/engineered-failure.md`.

**Ask your agent:** "Why is writing a prediction before running an experiment better than just running it?"

## Mapping table

**What it is:** A table that translates one member's names (states, fields, outcomes) into the base build's names.

**Why it matters:** Two builds can mean the same thing with different words. Without a map, every merged test fails for the wrong reason.

**In your build:** Phase 2, Step 2 of the merge checklist, and your `tests/known-answer/run.py` translation.

**Ask your agent:** "Give an example of two programs that name the same state differently, and show a translation table."

## Non-regression check

**What it is:** Re-running everyone's old tests after each change to prove nothing that worked has broken.

**Why it matters:** A merge can fix one thing and silently break another.

**In your build:** `evidence/non-regression-check.md`: prediction beside result.

**Ask your agent:** "What does 'regression' mean in software, and how does a non-regression test help during a merge?"

## Baseline versus pilot (ADI501)

**What it is:** The same measure taken on the old way of working and on your tool, with the same inputs.

**Why it matters:** "It feels faster" is not evidence. A fair comparison needs the same inputs and an honest label: measured or estimate.

**In your build:** `evidence/baseline-vs-pilot.md`.

**Ask your agent:** "Give an example of a comparison that looks fair but is not, because the inputs differ."

## Continue / revise / stop thresholds (ADI501)

**What it is:** Numbers, decided in advance, that say whether a pilot should keep going, change, or end.

**Why it matters:** Deciding after you see the result lets hope choose for you.

**In your build:** `evidence/thresholds.md`, defended in Phase 3.

**Ask your agent:** "Why do pilots set stop criteria before they start? Give one example from a project you know."
