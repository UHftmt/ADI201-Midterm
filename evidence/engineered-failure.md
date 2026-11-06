# Engineered Failure Record

Break one thing on purpose, predict what happens first, then prove it. Write the prediction **before** you break anything.

| Field | Your entry | Example (Idea 2) |
|---|---|---|
| Date and time of prediction | Nov 06, 15:43 | *Oct 29, 14:05* |
| What I will break | Bypass stylist interval overlap check in `domain.py:create_appointment` | *Submit two bookings for the same provider and the same time* |
| Prediction: what the tool will do | When submitting overlapping requests for Ana (`B-001` at 09:00 for 45m and `B-002` at 09:30 for 90m), the second booking will be incorrectly accepted. `run.py` will report: `FAIL seeded_conflict_same_stylist_overlap: expected {'outcome': 'conflict'}, got {'outcome': 'accepted', 'state': 'booked'}`. | *The second booking is rejected with `conflict`; the first is unchanged* |
| Evidence (paste output or log lines) | `FAIL seeded_conflict_same_stylist_overlap: expected {'outcome': 'conflict'}, got {'outcome': 'accepted', 'state': 'booked'}` | *Second booking was accepted; the schedule shows two bookings at 10:00* |
| What was wrong (cause) | The simulated bug bypassed the timestamp comparison `max(start_dt, ex_start) < min(end_dt, ex_end)`, allowing two overlapping bookings for stylist Ana to occupy the same time slot. | *The conflict check compared dates only, not times* |
| Fix (commit hash and one sentence) | 4d584e2: restored interval overlap comparison `max(start_dt, ex_start) < min(end_dt, ex_end)` in `domain.py`. | *a1b2c3d: compare date and start time* |
| Repeat test (case name in `cases.json`) | `engineered_failure_stylist_conflict_repeat` (PASS) | *`double_booking_conflict`, now PASS* |

The prediction was completely accurate on the first try. This demonstrates that our known-answer suite and conflict engine correctly isolate double-booking regressions and verify that overlapping appointments are never silently scheduled.
