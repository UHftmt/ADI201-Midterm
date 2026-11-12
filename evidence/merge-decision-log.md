# Merge Decision Log (Phase 2, team)

**Base chosen:** Yuhe's build (`44cb016`, `domain.py` / `database.py` / `app.py`). **Why:** It passes 10 of 10 contract-compliant known-answer cases, cleanly separates persistence (`database.py`), domain/state-machine rules (`domain.py`), and Flask web views (`app.py`), uses SQLite with a `services` catalog and `audit_log`, enforces role-based state transitions (`client` vs `staff`), and writes sandboxed reminders to `reminders.log`.

| Component | From whom | Commit hash | Kept or dropped | Reason (about the system) |
|---|---|---|---|---|
| Base SQLite store, RBAC state machine & Flask app | Yuhe | `44cb016` | kept (base) | Passes 10/10 Phase 1 contract cases, persists across restarts, separates rules from routes, and records full audit history. |
| Per-stylist `ben_minutes` summary metric (`domain.py`) | Vinh | `68899a7` (from `store.py`) | kept | Base only computed Ana's minutes; porting Ben's minutes provides full staff summary metrics and matches Vinh's `whole_fixture_count_and_minutes`. |
| Audit history UI (`/staff/history`, `templates/history.html`) | Vinh | `6c885d7` (from `app.py`, `history.html`) | kept | Base recorded actions to SQLite `audit_log` but lacked a browser view; porting Vinh's history template provides a full human-auditable view of events and rejections. |
| Per-provider daily schedule view (`/provider`, `templates/provider.html`) | Shiming | `709baf9` (from `app.py`, `provider.html`) | kept | Base provided client and staff queues but no per-stylist filter view; porting Shiming's provider schedule provides dedicated provider visibility. |
| Front-desk reschedule feature & `booked -> no_show` move (`domain.py`, `app.py`) | Shiming | `cd854ef` (from `app.py`) | kept | Ported front-desk move/reschedule capability (originally on Yuhe's Phase 1 "Drop first" list) with operating hours, duration lookup, and conflict checks, plus staff `booked -> no_show` transition. |
| Duplicate Phase 1 booking/storage core (`store.py`, `rules.py`, `app.py` core) | Vinh | `a2f78d6` (from `7d5cb6a`) | dropped | Base already provides SQLite storage, RBAC, and validation; dropped duplicate store/rules logic in favor of base. |
| Duplicate Phase 1 booking/storage core (`app.py` core, `customer.html`, `frontdesk.html`) | Shiming | `f72fec1` (from `2b3c342`) | dropped | Base already provides `/book`, `/staff`, and variable duration support from `services.csv` (Shiming's core hardcodes 30-min slots). |
