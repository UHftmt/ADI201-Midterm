# Architecture

This project is a small Flask + SQLite appointment demo for a fictional salon called Juniper Studio.

## Entities

- Customer request: the person booking a service, captured in `customer_name`, `service`, `provider`, and appointment date/time.
- Appointment: stored in the `appointments` table with `id`, `customer_name`, `service`, `provider`, `start_at`, `end_at`, `status`, and `created_at`.
- Reminder: stored in `reminder_log`, with the scheduled time and message for a local reminder record.
- Audit trail: stored in `audit_log`, with action and details for each status or move event.

## Roles and states

Customer role:
- submits a new booking through `/customer`
- cannot change appointment state after submission

Front desk role:
- reviews `/frontdesk`
- confirms or moves `booked` or `confirmed` appointments
- moves status in the allowed chain: `booked -> confirmed -> arrived -> completed`
- may also close a booking as `no-show` from `booked` or `confirmed`
- cannot skip allowed transitions; invalid transitions return a 400 error

Provider role:
- views `/provider?provider=<name>`
- sees only the schedule for the selected provider

## Data store

The app uses SQLite and initializes `appointments`, `reminder_log`, and `audit_log` in `instance/appointments.sqlite3` when the app starts. The database is the persistence layer and survives app restarts when the same database path is reused.

## External step that is sandboxed

The reminder step is intentionally fake. When a customer books, the app creates a `reminder_log` row with the scheduled time and a reminder message. Nothing is emailed or texted. That keeps the workflow realistic without sending real communications or exposing credentials.

## Where the features live

- booking request and validation: `customer()` in `app.py`
- provider conflict checks: `has_conflict()` and `create_appointment()`
- status transitions: `update_status()`
- front desk move workflow: `move_appointment()`
- provider schedule view: `provider_schedule()`
- reminder and audit writing: `log_audit()` and the appointment insert logic
