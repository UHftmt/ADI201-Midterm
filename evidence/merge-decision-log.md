# Merge Decision Log (Phase 2, team)

**Base chosen:** Yuhe's build (`44cb016`, `domain.py` / `database.py` / `app.py`). **Why:** It passes 10 of 10 contract-compliant known-answer cases, cleanly separates persistence (`database.py`), domain/state-machine rules (`domain.py`), and Flask web views (`app.py`), uses SQLite with a `services` catalog and `audit_log`, enforces role-based state transitions (`client` vs `staff`), and writes sandboxed reminders to `reminders.log`.

| Component | From whom | Commit hash | Kept or dropped | Reason (about the system) |
|---|---|---|---|---|
| Base SQLite store, RBAC state machine & Flask app | Yuhe | `44cb016` | kept (base) | Passes 10/10 Phase 1 contract cases, persists across restarts, separates rules from routes, and records full audit history. |
| Duplicate Phase 1 booking/storage core (`store.py`, `rules.py`, `app.py` core) | Vinh | `a2f78d6` (from `7d5cb6a`) | pending / drop duplicate core | Base already provides SQLite storage, RBAC, and validation; evaluate `ben_minutes` summary and `/staff/history` UI for porting in Step 4. |
| Duplicate Phase 1 booking/storage core (`app.py` core, `customer.html`, `frontdesk.html`) | Shiming | `ff5d783` (from `2b3c342`) | pending / drop duplicate core | Base already provides `/book`, `/staff`, and SQLite service-duration lookups (`S1`–`S4` vs fixed 30-min slots); evaluate `/provider` schedule view, front-desk reschedule (`/move`), and `booked -> no_show` transition for porting in Step 4. |
