# Non-Regression Check (Phase 2, team)

Write your prediction **before** running. A case that fails only because a component is not merged yet is expected. Any other failure is a regression in the base.

| Member | Case | On own build | Merged, before porting (prediction) | Merged, before porting (result) | Merged, after porting | Port commit |
|---|---|---|---|---|---|---|
| Yuhe | `happy_path_booking_and_lifecycle` | PASS | PASS | PASS | *(pending)* | |
| Yuhe | `client_cannot_confirm_booking` | PASS | PASS | PASS | *(pending)* | |
| Yuhe | `cannot_skip_states_to_completed` | PASS | PASS | PASS | *(pending)* | |
| Yuhe | `seeded_conflict_same_stylist_overlap` | PASS | PASS | PASS | *(pending)* | |
| Yuhe | `seeded_bad_date_format` | PASS | PASS | PASS | *(pending)* | |
| Yuhe | `seeded_after_close` | PASS | PASS | PASS | *(pending)* | |
| Yuhe | `duplicate_request_id` | PASS | PASS | PASS | *(pending)* | |
| Yuhe | `hand_computed_ana_booked_minutes` | PASS | PASS | PASS | *(pending)* | |
| Yuhe | `restart_persists_appointments` | PASS | PASS | PASS | *(pending)* | |
| Yuhe | `engineered_failure_stylist_conflict_repeat` | PASS | PASS | PASS | *(pending)* | |
| Vinh | `happy_path_full_visit` | FAIL *(Vinh expected `illegal_move`/`confirmed`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `accepted`, `completed`)* | *(pending)* | |
| Vinh | `client_cannot_confirm` | FAIL *(Vinh expected `duplicate_request`/`confirmed`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `not_permitted`, `booked`)* | *(pending)* | |
| Vinh | `client_cannot_mark_arrived` | FAIL *(Vinh expected `state: arrived`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `not_permitted`, `confirmed`)* | *(pending)* | |
| Vinh | `client_cannot_mark_no_show` | FAIL *(Vinh expected `state: no_show`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `not_permitted`, `confirmed`)* | *(pending)* | |
| Vinh | `client_cannot_mark_completed` | FAIL *(Vinh expected `state: completed`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `not_permitted`, `arrived`)* | *(pending)* | |
| Vinh | `client_can_cancel_own_booking` | PASS | PASS | PASS | *(pending)* | |
| Vinh | `staff_marks_no_show` | PASS | PASS | PASS | *(pending)* | |
| Vinh | `staff_cannot_skip_to_completed` | FAIL *(Vinh expected `not_permitted` instead of `illegal_move`)* | FAIL *(same Phase 1 answer-key error in `cases.json`)* | FAIL *(got `illegal_move`, `booked`)* | *(pending)* | |
| Vinh | `completed_cannot_be_cancelled` | PASS | PASS | PASS | *(pending)* | |
| Vinh | `duplicate_request_id` | PASS | PASS | PASS | *(pending)* | |
| Vinh | `back_to_back_is_not_a_conflict` | PASS | PASS | PASS | *(pending)* | |
| Vinh | `ends_exactly_at_close` | PASS | PASS | PASS | *(pending)* | |
| Vinh | `seeded_bad_date_format` | PASS | PASS | PASS | *(pending)* | |
| Vinh | `seeded_after_close` | PASS | PASS | PASS | *(pending)* | |
| Vinh | `seeded_conflict_ana` | PASS | PASS | PASS | *(pending)* | |
| Vinh | `seeded_conflict_ben` | FAIL *(missing `B-004` setup step in `cases.json`)* | FAIL *(same Phase 1 test-setup omission in `cases.json`)* | FAIL *(got `accepted`, `booked`)* | *(pending)* | |
| Vinh | `whole_fixture_count_and_minutes` | FAIL *(Vinh expected `""`, `7`, `2`, `2`)* | FAIL *(base missing `ben_minutes` component + Phase 1 answer-key error)* | FAIL *(got `accepted`, `3`, `65`; no `ben_minutes`)* | *(pending)* | |
| Vinh | `restart_keeps_bookings_and_state` | PASS | PASS | PASS | *(pending)* | |
| Shiming | `happy_path_complete_booking` | PASS | PASS *(via `run.py` Step 2 translator)* | PASS | *(pending)* | |
| Shiming | `illegal_status_jump_from_booked` | PASS | PASS *(via `run.py` Step 2 translator)* | PASS | *(pending)* | |
| Shiming | `same_provider_same_slot_is_rejected` | PASS | PASS *(via `run.py` Step 2 translator)* | PASS | *(pending)* | |
| Shiming | `adjacent_slots_are_allowed` | PASS | PASS *(via `run.py` Step 2 translator)* | PASS | *(pending)* | |
| Shiming | `no_show_keeps_slot_blocked` | PASS | PASS *(note: intermediate `booked -> no_show` not in base yet, `booked` still blocks slot)* | PASS | *(pending)* | |
| Shiming | `appointment_persists_after_restart` | PASS | PASS *(via `run.py` Step 2 translator)* | PASS | *(pending)* | |

**Transfer trial** *(pending — to be completed by a teammate who did not do the merge after Step 6)*
