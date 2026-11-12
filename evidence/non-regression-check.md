# Non-Regression Check (Phase 2, team)

Write your prediction **before** running. A case that fails only because a component is not merged yet is expected. Any other failure is a regression in the base.

| Member | Case | On own build | Merged, before porting (prediction) | Merged, before porting (result) | Merged, after porting | Port commit |
|---|---|---|---|---|---|---|
| Yuhe | `happy_path_booking_and_lifecycle` | PASS | PASS | PASS | PASS | *(none)* |
| Yuhe | `client_cannot_confirm_booking` | PASS | PASS | PASS | PASS | *(none)* |
| Yuhe | `cannot_skip_states_to_completed` | PASS | PASS | PASS | PASS | *(none)* |
| Yuhe | `seeded_conflict_same_stylist_overlap` | PASS | PASS | PASS | PASS | *(none)* |
| Yuhe | `seeded_bad_date_format` | PASS | PASS | PASS | PASS | *(none)* |
| Yuhe | `seeded_after_close` | PASS | PASS | PASS | PASS | *(none)* |
| Yuhe | `duplicate_request_id` | PASS | PASS | PASS | PASS | *(none)* |
| Yuhe | `hand_computed_ana_booked_minutes` | PASS | PASS | PASS | PASS | *(none)* |
| Yuhe | `restart_persists_appointments` | PASS | PASS | PASS | PASS | *(none)* |
| Yuhe | `engineered_failure_stylist_conflict_repeat` | PASS | PASS | PASS | PASS | *(none)* |
| Vinh | `happy_path_full_visit` | FAIL *(Vinh expected `illegal_move`/`confirmed`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `accepted`, `completed`)* | PASS | `6057acb` (Vinh re-worked his own answers by hand; replaces `39dde4c`) |
| Vinh | `client_cannot_confirm` | FAIL *(Vinh expected `duplicate_request`/`confirmed`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `not_permitted`, `booked`)* | PASS | `6057acb` (Vinh re-worked his own answers by hand; replaces `39dde4c`) |
| Vinh | `client_cannot_mark_arrived` | FAIL *(Vinh expected `state: arrived`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `not_permitted`, `confirmed`)* | PASS | `6057acb` (Vinh re-worked his own answers by hand; replaces `39dde4c`) |
| Vinh | `client_cannot_mark_no_show` | FAIL *(Vinh expected `state: no_show`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `not_permitted`, `confirmed`)* | PASS | `6057acb` (Vinh re-worked his own answers by hand; replaces `39dde4c`) |
| Vinh | `client_cannot_mark_completed` | FAIL *(Vinh expected `state: completed`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `not_permitted`, `arrived`)* | PASS | `6057acb` (Vinh re-worked his own answers by hand; replaces `39dde4c`) |
| Vinh | `client_can_cancel_own_booking` | PASS | PASS | PASS | PASS | *(none)* |
| Vinh | `staff_marks_no_show` | PASS | PASS | PASS | PASS | *(none)* |
| Vinh | `staff_cannot_skip_to_completed` | FAIL *(Vinh expected `not_permitted` instead of `illegal_move`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `illegal_move`, `booked`)* | PASS | `6057acb` (Vinh re-worked his own answers by hand; replaces `39dde4c`) |
| Vinh | `completed_cannot_be_cancelled` | PASS | PASS | PASS | PASS | *(none)* |
| Vinh | `duplicate_request_id` | PASS | PASS | PASS | PASS | *(none)* |
| Vinh | `back_to_back_is_not_a_conflict` | PASS | PASS | PASS | PASS | *(none)* |
| Vinh | `ends_exactly_at_close` | PASS | PASS | PASS | PASS | *(none)* |
| Vinh | `seeded_bad_date_format` | PASS | PASS | PASS | PASS | *(none)* |
| Vinh | `seeded_after_close` | PASS | PASS | PASS | PASS | *(none)* |
| Vinh | `seeded_conflict_ana` | PASS | PASS | PASS | PASS | *(none)* |
| Vinh | `seeded_conflict_ben` | FAIL *(missing `B-004` setup step in `cases.json`)* | FAIL *(same Phase 1 test-setup omission in `cases.json`)* | FAIL *(got `accepted`, `booked`)* | PASS | `6057acb` (Vinh re-worked his own answers by hand; replaces `39dde4c`) |
| Vinh | `whole_fixture_count_and_minutes` | FAIL *(Vinh expected `""`, `7`, `2`, `2`)* | FAIL *(base missing `ben_minutes` component + Phase 1 answer-key error)* | FAIL *(got `accepted`, `3`, `65`; no `ben_minutes`)* | FAIL *(outcome only: Vinh's answer `conflict`, the app says `accepted`; count `3`, Ana `65`, Ben `45` match)* | `68899a7` (ben_minutes port) + `6057acb` (Vinh's own answers) |
| Vinh | `restart_keeps_bookings_and_state` | PASS | PASS | PASS | PASS | *(none)* |
| Shiming | `happy_path_complete_booking` | PASS | PASS *(via `run.py` Step 2 translator)* | PASS | PASS | `8099227` (step translator) |
| Shiming | `illegal_status_jump_from_booked` | PASS | PASS *(via `run.py` Step 2 translator)* | PASS | PASS | `8099227` (step translator) |
| Shiming | `same_provider_same_slot_is_rejected` | PASS | PASS *(via `run.py` Step 2 translator)* | PASS | PASS | `8099227` (step translator) |
| Shiming | `adjacent_slots_are_allowed` | PASS | PASS *(via `run.py` Step 2 translator)* | PASS | PASS | `8099227` (step translator) |
| Shiming | `no_show_keeps_slot_blocked` | PASS | PASS *(note: intermediate `booked -> no_show` not in base yet, `booked` still blocks slot)* | PASS | PASS | `cd854ef` (booked->no_show port) |
| Shiming | `appointment_persists_after_restart` | PASS | PASS *(via `run.py` Step 2 translator)* | PASS | PASS | `8099227` (step translator) |

**Transfer trial** *(pending — to be completed by a teammate who did not do the merge after Step 6)*
