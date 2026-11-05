# Idea 2 rules (read before writing `cases.json`)

**Files:** `services.csv` (service_id, name, minutes) and `booking-requests.csv` (request_id, client, service_id, stylist, start). Process requests **in file order**. Roles: a `client` asks, `staff` (front desk, and the stylist/provider) confirm. The contract word for the person is `client`.

**Rules**
1. **Opening hours:** 09:00 to 17:00, every day in the file. A booking occupies `start` up to `start + minutes` from `services.csv`.
2. **after_close:** the booking would end after 17:00 (ending exactly at 17:00 is fine).
3. **bad_date_format:** `start` must look like `YYYY-MM-DD HH:MM` (for example `2026-11-02 09:00`). Anything else is rejected.
4. **conflict:** two bookings for the **same stylist** overlap in time. The earlier request in the file keeps the slot. A booking that starts exactly when another ends does **not** overlap. A rejected request never blocks anyone.
5. **duplicate_request:** a `request_id` you have already seen.
6. Accepted bookings start in state `booked`. Later states: `confirmed`, `arrived`, `completed`, `no_show`, `cancelled`.

**What the files contain on purpose:** a bad date format, a booking that runs past closing, and overlapping bookings for two stylists. This file has **no** repeated id and nothing cancelled or no-show: write your own extra inputs in `cases.json` for `duplicate_request`, `cancelled`, `no_show`, and the role limits.

**By hand:** for each stylist, add up the minutes of their accepted bookings. That is a good total case.
