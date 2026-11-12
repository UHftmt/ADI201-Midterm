# Mapping table (Phase 2)

One table per non-base member. It says what that member's names mean in the base build, so that their `cases.json` still means the same thing. The common words (states, outcomes, roles, step names) are fixed by the project contract and do not need mapping; map **your internal names** to them.

> Draft written by Claude Code on Nov 11 by reading the three builds' code (no cases were run to make it). The base is taken to be Yuhe's build because the merge sits on Yuhe's branch; the team still has to confirm the base and its reason in `merge-decision-log.md`. Each member: check your own table.

## Member: Vinh  ->  base: Yuhe

Vinh's build is in `members/vinh/`.

| Kind | Their name | Base name | Note |
|---|---|---|---|
| entity | booking (table `bookings`) | appointment (table `appointments`) | same thing: one accepted request |
| entity | table `history` | table `audit_log` | Vinh's has two extra columns, `booking_id` and `action` (`create`, `move`, `remind`) |
| entity | table `seen_requests` | none | the base finds a repeated id by looking in `appointments`. Vinh's also remembers the ids of refused requests, so the two builds can answer differently when a refused id is sent again |
| entity | services read from `services.csv` each start | table `services`, filled from the same file | same data |
| field | `start`, `end` | `start_time`, `end_time` | same text format, `YYYY-MM-DD HH:MM` |
| field | `minutes` (stored on the booking) | not stored; looked up in `services` | |
| field | `at` (history) | `timestamp` (audit_log) | |
| field | `request_id`, `client`, `service_id`, `stylist`, `state` | same names | |
| state | `booked`, `confirmed`, `arrived`, `completed`, `no_show`, `cancelled` | same words | both use the contract words |
| outcome | `accepted`, `duplicate_request`, `bad_date_format`, `after_close`, `conflict`, `not_permitted`, `illegal_move` | same words | |
| outcome | `missing_field`, `unknown_service`, `not_found` | `invalid_request` | not contract words in either build |
| route / page | `/book`, `/staff` | `/book`, `/staff` | |
| route / page | `/staff/history` | none | the base has no page that shows the audit log |
| route / page | `POST /bookings/<id>/move` | `POST /staff/action` | |
| route / page | `POST /staff/bookings/<id>/remind` | none as a button | the base writes the reminder line itself, inside `log_reminder` |
| route / page | `/api/bookings`, `/api/bookings/<id>/move` | `/api/appointments` | |
| method / function | `Store.create_booking(role, data)` | `create_appointment(db_path, actor, data)` | |
| method / function | `Store.move_booking(role, id, to)` | `move_appointment(db_path, actor, appt_id, to_state)` | |
| method / function | `Store.summary()` | `list_appointments_summary(db_path)` | |
| method / function | `rules.ALLOWED_MOVES`, `rules.check_move` | `ALLOWED_TRANSITIONS` in `domain.py` | the same seven moves. The base also lets `staff` create a booking; Vinh's allows only `client` |
| method / function | `rules.check_request` | the checks inside `create_appointment` | |
| file | reminders in `outbox/reminders.log` next to the database | `reminders.log` in the repository root | the base's file is tracked by git and changes on every test run |

## Member: Shiming  ->  base: Yuhe

Shiming's build is in `members/shiming/`.

| Kind | Their name | Base name | Note |
|---|---|---|---|
| entity | appointment (table `appointments`) | appointment (table `appointments`) | |
| entity | table `reminder_log` | file `reminders.log` | Shiming keeps reminders in the database |
| entity | table `audit_log` (`appointment_id`, `action`, `details`, `created_at`) | table `audit_log` (`actor`, `request_id`, `old_state`, `new_state`, `outcome`) | different columns; Shiming's has no actor or outcome column |
| field | `customer_name` | `client` | |
| field | `provider` | `stylist` | Shiming's are `Avery`, `Jordan`; the fixture uses `Ana`, `Ben` |
| field | `service` (a name: `Consultation`, `Cut and style`, `Color consultation`) | `service_id` (`S1` to `S4`) | Shiming's services are not the fixture's services |
| field | `start_at`, `end_at` | `start_time`, `end_time` | |
| field | `status` | `state` | |
| field | none | `request_id` | Shiming's build has no request id, so it has no duplicate check |
| field | every appointment is 30 minutes (`APPOINTMENT_MINUTES`) | minutes come from `services.csv` | |
| state | `no-show` | `no_show` | hyphen in Shiming's, underscore in the contract |
| state | none | `cancelled` | Shiming's build has no cancelled state |
| state | `booked`, `confirmed`, `arrived`, `completed` | same words | Shiming's also allows `booked` -> `no-show`; the base does not |
| outcome | error messages shown on the page, and HTTP 400 for a refused status change | `bad_date_format`, `after_close`, `conflict`, `illegal_move`, `not_permitted` | Shiming's app does not return the contract's outcome words; their runner (`members/shiming/tests/known-answer/run.py`) reads the page result instead. Shiming to confirm the translation |
| route / page | `/customer` | `/book` | |
| route / page | `/frontdesk` | `/staff` | |
| route / page | `/provider` | none | a per-provider schedule page; the base has no equivalent |
| route / page | `POST /frontdesk/<id>/status` | `POST /staff/action` | |
| route / page | `POST /frontdesk/<id>/move` | none | moves an appointment to a new time (rescheduling); the base has no equivalent |
| method / function | `create_appointment(...)`, `validate_slot`, `has_conflict` | `create_appointment(db_path, actor, data)` | |
| method / function | `STATUS_TRANSITIONS` | `ALLOWED_TRANSITIONS` | Shiming's table has no roles in it |
