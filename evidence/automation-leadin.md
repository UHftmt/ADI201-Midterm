# Automation Lead-In (lab output)

This is the output of the Week 7 lead-in lab. It is part of your Phase 1 evidence folder, and it helps with your state table and checkpoint (Steps 1.2 and 1.7).

Copy the tables from `midterm-lab-automation-leadin.html` (in your repository root, or in `project-workspace/`) and fill them in for **your** idea. The example column shows the style; replace it.

> Parts 1 and 3 were filled in by Claude Code on Nov 10 from the finished app (see `ai-use-log.md`). Parts 2, 4 and 5 are design choices and predictions, so they are left for Vinh.

## Part 1: State machine (illegal moves count too)

| From | To | Who may do it | Example (Idea 2) |
|---|---|---|---|
| (new request) | `booked` | client | |
| `booked` | `confirmed` | staff | *booked -> confirmed, front desk* |
| `booked` | `cancelled` | client or staff | |
| `confirmed` | `arrived` | staff | |
| `confirmed` | `no_show` | staff | |
| `confirmed` | `cancelled` | client or staff | |
| `arrived` | `completed` | staff | |
| `confirmed` | `booked` | nobody: this pair is not in the table, so it is refused as `illegal_move` | *completed -> booked, nobody: rejected as `illegal_move`* |
| `confirmed` | `arrived` | a client who tries it is refused as `not_permitted`; the booking stays `confirmed` | |

## Part 2: Human checkpoint

| Field | Your answer | Example |
|---|---|---|
| Who approves | | *Front desk* |
| What they see | | *Client, time, provider, conflict warning* |
| On reject | | *Booking returns to `booked` with a reason in the log* |
| On no answer | | *After 24 hours the booking is flagged, never auto-confirmed* |

## Part 3: Audit log (three example rows)

| item | actor | old | new | rejected attempts logged? (yes: the last two rows are refused moves, with old = new) |
|---|---|---|---|---|
| D-1 | client | (none) | booked | action `create`, outcome `accepted` |
| D-1 | staff | booked | confirmed | action `move`, outcome `accepted` |
| D-1 | client | confirmed | confirmed | action `move`, outcome `not_permitted` |
| D-1 | staff | confirmed | confirmed | action `move`, outcome `illegal_move` |
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
