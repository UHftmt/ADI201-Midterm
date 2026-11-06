# Automation Lead-In (lab output)

This is the output of the Week 7 lead-in lab. It is part of your Phase 1 evidence folder, and it helps with your state table and checkpoint (Steps 1.2 and 1.7).

## Part 1: State machine (illegal moves count too)

| From | To | Who may do it | Outcome / Rule |
|---|---|---|---|
| `(none)` | `booked` | `client`, `staff` | Initial intake passes formatting, operating hours, and conflict checks |
| `booked` | `confirmed` | `staff` | Front desk approves booking |
| `confirmed` | `arrived` | `staff` | Client checks in at salon |
| `arrived` | `completed` | `staff` | Service completed |
| `booked` | `cancelled` | `client`, `staff` | Booking cancelled before confirmation |
| `confirmed` | `cancelled` | `client`, `staff` | Booking cancelled after confirmation |
| `confirmed` | `no_show` | `staff` | Client failed to appear for appointment |
| `booked` | `confirmed` | `client` | Rejected: `not_permitted` (only staff can confirm) |
| `booked` | `completed` | `staff` | Rejected: `illegal_move` (cannot skip confirmed and arrived) |
| `completed` | `booked` | `nobody` | Rejected: `illegal_move` |

## Part 2: Human checkpoint

| Field | Your answer | Example |
|---|---|---|
| Who approves | Front-desk receptionist / coordinator | *Front desk* |
| What they see | Client name, requested service, stylist, time window, and stylist conflict status | *Client, time, provider, conflict warning* |
| On reject | Booking moves to `cancelled` with reason logged in `audit_log` | *Booking returns to `booked` with a reason in the log* |
| On no answer | Booking remains in pending review queue; never auto-confirmed | *After 24 hours the booking is flagged, never auto-confirmed* |

## Part 3: Audit log (three example rows)

| item | actor | old | new | rejected attempts logged? |
|---|---|---|---|---|
| `B-001` | `client` | `(none)` | `booked` | no (successful intake creation) |
| `B-001` | `client` | `booked` | `booked` | yes: rejected attempt (`not_permitted` to confirm) |
| `B-001` | `staff` | `booked` | `confirmed` | no (successful human approval) |

## Part 4: Scheduled job (before / after)

| Item | Before | After | Side effect |
|---|---|---|---|
| `B-001` (unconfirmed > 24h) | `booked` | `flagged` | Local alert appended to `reminders.log`, no real SMS sent |

Safe to run twice? Yes: The query is idempotent; it selects only unconfirmed `booked` appointments older than 24 hours that are not already flagged.

## Part 5: Prediction and peer check

| Question | My prediction | Partner's check |
|---|---|---|
| Can a client move an appointment from `booked` to `confirmed`? | Rejected with `not_permitted`; state stays `booked` | PASS (`client_cannot_confirm_booking`) |
| Can an appointment jump directly from `booked` to `completed`? | Rejected with `illegal_move`; state stays `booked` | PASS (`cannot_skip_states_to_completed`) |
