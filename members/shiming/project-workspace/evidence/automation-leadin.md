# Automation lead-in evidence

This file records the local-only automated workflow that mirrors the architecture above.

| State | Allowed mover | Action | Result |
|---|---|---|---|
| booked | customer, front desk | booking request created | appointment saved |
| confirmed | front desk | approval step | staff checkpoint reached |
| arrived | front desk | customer checked in | visit started |
| completed | front desk | close the visit | final state reached |
| no-show | front desk | mark missed appointment | blocked from rebooking in same slot |

## Checkpoint

The human checkpoint is the front desk queue. A customer request is not marked active until staff either confirms or moves it.

## Audit log excerpt

- `appointment_booked`: customer request submitted
- `status_changed`: status moved from booked to confirmed
- `status_changed`: status moved from confirmed to arrived
- `status_changed`: status moved from arrived to completed
- `appointment_moved`: front desk rescheduled the appointment
