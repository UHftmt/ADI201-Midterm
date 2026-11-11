# Mapping table (Phase 2)

One table per non-base member. It says what that member's names mean in the base build, so that their `cases.json` still means the same thing. The common words (states, outcomes, roles, step names) are fixed by the project contract and do not need mapping; map **your internal names** to them.

> The base is confirmed as Yuhe's build (`44cb016`, `domain.py` / `database.py` / `app.py`) in `evidence/merge-decision-log.md`. Each table guides porting code and translates member runner hooks.

## Member: Vinh  ->  base: Yuhe

Vinh's build is in `members/vinh/`.

| Kind | Their name | Base name | Note |
|---|---|---|---|
| entity | booking (table `bookings`) | appointment (table `appointments`) | Same entity: one accepted booking request |
| entity | table `history` | table `audit_log` | Vinh's has extra columns (`booking_id`, `action`); base records `actor`, `request_id`, `old_state`, `new_state`, `outcome` |
| entity | table `seen_requests` | none | Base checks `appointments` for `request_id` duplicates; Vinh's also remembers refused IDs |
| entity | services read from `services.csv` each start | table `services`, filled from `services.csv` | Same underlying fixture data |
| field | `start`, `end` | `start_time`, `end_time` | Same text format: `YYYY-MM-DD HH:MM` |
| field | `minutes` (stored on the booking) | looked up in `services` table | Same duration math |
| field | `at` (history) | `timestamp` (audit_log) | Both record ISO/timestamp strings |
| field | `request_id`, `client`, `service_id`, `stylist`, `state` | same names | 1:1 match |
| state | `booked`, `confirmed`, `arrived`, `completed`, `no_show`, `cancelled` | same words | Exact 1:1 match with contract vocabulary |
| outcome | `accepted`, `duplicate_request`, `bad_date_format`, `after_close`, `conflict`, `not_permitted`, `illegal_move` | same words | Exact 1:1 match with contract vocabulary |
| outcome | `missing_field`, `unknown_service`, `not_found` | `invalid_request` | Internal non-contract words |
| route / page | `/book`, `/staff` | `/book`, `/staff` | Matching client and staff web views |
| route / page | `/staff/history` | none | Audit log viewer page; candidate to port in Step 4 |
| route / page | `POST /bookings/<id>/move` | `POST /staff/action` | State transition form endpoint |
| route / page | `POST /staff/bookings/<id>/remind` | logged via `log_reminder()` | Base automatically appends to `reminders.log` upon booking creation |
| route / page | `/api/bookings`, `/api/bookings/<id>/move` | `/api/appointments` | REST endpoints |
| method / function | `Store.create_booking(role, data)` | `create_appointment(db_path, actor, data)` | Booking creation logic |
| method / function | `Store.move_booking(role, id, to)` | `move_appointment(db_path, actor, appt_id, to_state)` | State machine transition engine |
| method / function | `Store.summary()` | `list_appointments_summary(db_path)` | Vinh returns `minutes_by_stylist` (`ana_minutes` + `ben_minutes`); base only returns `ana_minutes`. Port `ben_minutes` in Step 4. |
| method / function | `rules.ALLOWED_MOVES`, `rules.check_move` | `ALLOWED_TRANSITIONS` in `domain.py` | Same moves; base also allows `staff` to book |
| method / function | `rules.check_request` | checks inside `create_appointment` | Opening hours, format, and overlap intervals |
| file | `outbox/reminders.log` next to DB | `reminders.log` in repository root | Fake external step logging |

## Member: Shiming  ->  base: Yuhe

Shiming's build is in `members/shiming/`.

| Kind | Their name | Base name | Note |
|---|---|---|---|
| entity | appointment (table `appointments`) | appointment (table `appointments`) | Same entity |
| entity | table `reminder_log` | file `reminders.log` | Shiming stores reminders in SQLite table; base appends to local log file |
| entity | table `audit_log` (`appointment_id`, `action`, `details`, `created_at`) | table `audit_log` (`actor`, `request_id`, `old_state`, `new_state`, `outcome`) | Base tracks actor and outcome words |
| field | `customer_name` | `client` | Client name |
| field | `provider` | `stylist` | Shiming fixtures use `Avery`, `Jordan`; base/contract uses `Ana`, `Ben` |
| field | `service` (`Consultation`, `Cut and style`, `Color consultation`) | `service_id` (`S1`–`S4`) | Shiming's `Consultation` is 30 min, mapped in `run.py` to `S4` (30 min) so duration math aligns |
| field | `start_at`, `end_at` | `start_time`, `end_time` | ISO time strings |
| field | `status` | `state` | Status field |
| field | none (no request_id in Shiming's schema) | `request_id` | Synthetic `request_id` generated during `run.py` translation |
| field | fixed 30 minutes (`APPOINTMENT_MINUTES`) | variable minutes from `services.csv` | Variable duration supported via `services` catalog |
| state | `no-show` | `no_show` | Hyphen in Shiming's, underscore in contract. Normalized in `run.py`. |
| state | none | `cancelled` | Base supports cancellation |
| state | `booked`, `confirmed`, `arrived`, `completed` | same words | Exact contract matches |
| state rule difference | `("booked", "no-show")` allowed for frontdesk | Only `("confirmed", "no_show")` in base | Candidate to evaluate/port in Step 4 |
| outcome | error messages / HTTP 400 | contract outcome words (`bad_date_format`, `after_close`, `conflict`, `not_permitted`, `illegal_move`) | Shiming's strings (`accepted`, `not_permitted`, `state_persists`) mapped in `run.py` |
| step format | `{"as": ..., "action": "..."}` | `{"do": "create"|"move"|"list"|"restart", ...}` | English action sentences translated to contract steps in `tests/known-answer/run.py` |
| route / page | `/customer` | `/book` | Client booking page |
| route / page | `/frontdesk` | `/staff` | Front-desk management view |
| route / page | `/provider` | none | Per-stylist schedule page; candidate to port in Step 4 |
| route / page | `POST /frontdesk/<id>/status` | `POST /staff/action` | State transition endpoint |
| route / page | `POST /frontdesk/<id>/move` | none | Front-desk rescheduling; candidate to port in Step 4 |
| method / function | `create_appointment(...)`, `validate_slot`, `has_conflict` | `create_appointment(db_path, actor, data)` | Booking creation & conflict detection |
| method / function | `STATUS_TRANSITIONS` | `ALLOWED_TRANSITIONS` | Base enforces role-based move permissions |
