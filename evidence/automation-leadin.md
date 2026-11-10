# Automation Lead-In (lab output)

This is the output of the Week 7 lead-in lab. It is part of your Phase 1 evidence folder, and it helps with your state table and checkpoint (Steps 1.2 and 1.7).

Copy the tables from `midterm-lab-automation-leadin.html` (in your repository root, or in `project-workspace/`) and fill them in for **your** idea. The example column shows the style; replace it.

## Part 1: State machine (illegal moves count too)

| From | To | Who may do it | Example (Idea 2) |
|---|---|---|---|
| | | | *booked -> confirmed, front desk* |
| | | | *completed -> booked, nobody: rejected as `illegal_move`* |

## Part 2: Human checkpoint

| Field | Your answer | Example |
|---|---|---|
| Who approves | | *Front desk* |
| What they see | | *Client, time, provider, conflict warning* |
| On reject | | *Booking returns to `booked` with a reason in the log* |
| On no answer | | *After 24 hours the booking is flagged, never auto-confirmed* |

## Part 3: Audit log (three example rows)

| item | actor | old | new | rejected attempts logged? |
|---|---|---|---|---|
| | | | | |
| *e.g., B-104* | *e.g., front_desk* | *e.g., booked* | *e.g., confirmed* | *e.g., yes: a row with new = `rejected:illegal_move`* |

## Part 4: Scheduled job (before / after)

| Item | Before | After | Side effect |
|---|---|---|---|
| | | | |
| *e.g., B-105 (not confirmed in 24 h)* | *e.g., booked* | *e.g., flagged* | *e.g., one log line, no message sent* |

Safe to run twice? *e.g., Yes: the second run finds nothing in `booked` older than 24 h that is not already flagged.*

## Part 5: Prediction and peer check

| Question | My prediction | Partner's check |
|---|---|---|
| | | |
