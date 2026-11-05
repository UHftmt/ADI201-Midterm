# Engineered Failure Record

Break one thing on purpose, predict what happens first, then prove it. Write the prediction **before** you break anything.

| Field | Your entry | Example (Idea 2) |
|---|---|---|
| Date and time of prediction | | *Oct 29, 14:05* |
| What I will break | | *Submit two bookings for the same provider and the same time* |
| Prediction: what the tool will do | | *The second booking is rejected with `conflict`; the first is unchanged* |
| Evidence (paste output or log lines) | | *Second booking was accepted; the schedule shows two bookings at 10:00* |
| What was wrong (cause) | | *The conflict check compared dates only, not times* |
| Fix (commit hash and one sentence) | | *a1b2c3d: compare date and start time* |
| Repeat test (case name in `cases.json`) | | *`double_booking_conflict`, now PASS* |

If the prediction was right the first time, say so and explain what that tells you. If it was wrong, say what you learned.
