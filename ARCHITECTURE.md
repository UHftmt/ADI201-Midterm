# Architecture (one page)

**Entities**:
- `Service`: `service_id` (e.g. S1, S2), `name` (e.g. Haircut, Color), `minutes` (e.g. 45, 90).
- `Appointment`: `request_id` (e.g. B-001), `client` (e.g. client-a), `service_id`, `stylist` (e.g. Ana, Ben), `start` (timestamp `YYYY-MM-DD HH:MM`), `end` (computed timestamp `start + minutes`), `state` (`booked`, `confirmed`, `arrived`, `completed`, `no_show`, `cancelled`).
- `AuditLog`: `id`, `timestamp`, `actor` (`client`, `staff`), `request_id`, `old_state`, `new_state`, `outcome` (`accepted` or failure reason).

**States and who may move each**:

| From | To | Who may do it | Notes |
|---|---|---|---|
| (none) | `booked` | `client`, `staff` | Initial placement upon successful creation & validation |
| `booked` | `confirmed` | `staff` | Front-desk staff reviews & confirms schedule |
| `confirmed` | `arrived` | `staff` | Client checks in at salon |
| `arrived` | `completed` | `staff` | Service finished |
| `booked`, `confirmed` | `cancelled` | `client`, `staff` | Cancel appointment |
| `confirmed` | `no_show` | `staff` | Client failed to appear |

*Any move by an unauthorized role yields `not_permitted`. Any transition not in this table yields `illegal_move`.*

**Roles and what each can see:**
- `client`: Accesses `/book` intake form; submits requests, selects stylist, service, time slot; can view/cancel their booking.
- `staff`: Accesses `/staff` dashboard queue; views conflict alerts, confirms pending requests, marks arrivals, completions, cancellations, and no-shows.

**Data store**:
- SQLite database (`appointments.db`) with tables:
  - `services`
  - `appointments`
  - `audit_log`

**The external step I sandboxed**:
- Real action: Outgoing SMS/email notification to clients confirming appointment details or appointment reminders.
- Sandboxed implementation: Appends JSON/text log lines to local file `reminders.log` (e.g., `[REMINDER] Sent to client-a for Haircut with Ana at 2026-11-02 09:00`) with zero external API calls, credentials, or network transmission.

**Where each Difficulty Bar feature lives**:
- Roles & Views: `app.py` (`/book`, `/staff`) and HTML templates in `templates/`
- State Machine & Rules: `domain.py` / `app.py`
- Persistence: `database.py` (`appointments.db`)
- Staff Queue: `app.py` route `/staff` rendering `templates/staff.html`
- Fake External Step: `domain.py` (`log_reminder`) / `reminders.log`
- Human Checkpoint: `/staff` action button requiring staff confirmation
- Known-Answer Tests: `tests/known-answer/cases.json` & `run.py`

