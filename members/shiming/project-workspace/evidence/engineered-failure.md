# Engineered failure record

## Prediction

Date: 2026-11-08

If two bookings are submitted for the same provider at the same time, the app should reject the second one. This is the key conflict rule in the salon workflow. The expected result is `not_permitted`, and the appointment count should remain at one.

## Evidence

I ran the regression on the app and verified the behavior with the unit tests:

```sh
cd /home/ming99/shiming/201/midterm-shiming
. .venv/bin/activate
python -m unittest discover -s tests -v
```

The relevant test passed:

- `test_engineered_failure_rejects_overlapping_booking` passed
- duplicate booking was rejected with the message `already has an appointment`
- `COUNT(*) FROM appointments` remained `1`

## Repeat test

This case is now covered in `tests/test_app.py` as a regression and is also represented in the known-answer set in `tests/known-answer/cases.json` as `same_provider_same_slot_is_rejected`.
