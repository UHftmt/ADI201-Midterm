# Midterm Project Contract

Every personal build and the merged team build must follow this contract. It exists so that a teammate, and the instructor, can check your work with one command instead of reading all your code.

## 1. Files your repository must contain

| File or folder | What it holds | Written when |
|---|---|---|
| `README.md` | One command to run, one command to test, and the data-safety boundary | Phase 1 |
| `ARCHITECTURE.md` | Entities, states, roles, data store, and the external step you sandboxed (one page) | Phase 1 |
| `tests/known-answer/cases.json` | Expected values for your idea, **written before the agent builds the feature** | Phase 1, before building |
| `tests/known-answer/run.py` (from the starter skeleton) | One command that runs `cases.json` against your build and prints one `PASS` or `FAIL` line per case. Your README gives the exact command. | Phase 1 |
| `midterm-workbook.md` | Short answers as you go, including item 7.3, the job link (copy it from the starter in Step 1.1) | Phase 1 and 3 |
| `evidence/` | The templates from the starter, filled in | Phase 1 and 2 |
| tag `phase1-submit` | The commit you submit on Sun Nov 8 | Phase 1 deadline |

Rules: commit your `cases.json` before the first build commit, so the history shows the answers came first. A build that hard-codes a known-answer value, fakes a result, contains a live credential, or sends a real message is capped at 70/100.

## 2. Common vocabulary (so builds can be compared)

Teammates build the same idea, so they must use the same words in `cases.json`, even if each build uses different names inside. The words are fixed per idea:

| Idea | States (common names) | Outcome words for a rejected input | Roles |
|---|---|---|---|
| 1 Pho65 ordering | `placed`, `paid`, `in_progress`, `ready`, `picked_up`, `abandoned` (card orders are `paid` on placement; pay-in-store orders start `placed`) | `duplicate_request`, `out_of_stock`, `invalid_request` | customer, staff, kitchen, system |
| 2 Appointments (client = the person booking; staff = front desk and stylist) | `booked`, `confirmed`, `arrived`, `completed`, `no_show`, `cancelled` | `duplicate_request`, `bad_date_format`, `conflict`, `after_close` | client, staff |
| 3 Claim check | `submitted`, `sourced`, `verified`, `refuted`, `unverifiable` | `citation_not_found` | submitter, verifier, system (does the lookup) |
| 4 Literature assistant | `drafted`, `link_checked`, `quote_checked`, `human_opened`, `accepted`, `rejected` | `dead_link`, `quote_not_found`, `invented_reference` | researcher, reviewer, system (runs the link and quote checks) |
| 5 Your own idea | Taken from your team's approved Idea 5 proposal (the team baseline) | same | same |

**Words for every idea:** a role tries a move it may not make: outcome `not_permitted`. A state change that is not in your state table: outcome `illegal_move`. An accepted action: outcome `accepted`.

Your build may call a state `cooking` internally. Your `tests/known-answer/run.py` translates it to `in_progress`. That translation table is the **mapping table** you will need again in Phase 2.

## 3. What `cases.json` looks like and must cover

The file is `{"cases": [ ... ]}`. Each case has `name`, `type` (a short label of your choice, for example `happy_path`, `role_not_allowed`, `seeded_failure`, `restart`), `input`, `expected`, `how_computed`. Every case starts with a **fresh, empty app** (no items). `input` is always a **list of steps**, and the same step vocabulary is used for every idea, so a teammate's `cases.json` can run against your build in Phase 2.

**Steps.** Each step is an object with `"do"` and, for all but `list` and `restart`, `"as"` (the role acting):

| Step | Meaning | Other keys |
|---|---|---|
| `{"do": "create", "as": ROLE, "data": {...}}` | A role submits a new item (an order, booking, claim, or citation). Items are numbered 1, 2, 3 in the order the case creates them. | `data`: the fields in the table below |
| `{"do": "move", "as": ROLE, "item": N, "to": STATE}` | A role tries to move item number N to a state | `item` (1-based), `to` (a common state word) |
| `{"do": "list"}` | List all items | none |
| `{"do": "restart"}` | Stop and start your app; the saved data must still be there | none |

`data` fields per idea (the column names of the fixture CSV): Idea 1 `request_id, customer, item_id, qty, payment_choice`; Idea 2 `request_id, client, service_id, stylist, start`; Idea 3 `claim_id, claim_text, draft_cited_sources`; Idea 4 `cite_id, claim, source_id, quoted_text, url`. Idea 5: the fields your approved proposal names.

**`expected`.** List only the keys you care about; `run.py` checks only those. The result is taken from the **last step**:

- `outcome`: `accepted` or a rejection word from section 2 (always present).
- `proposed` (Idea 3 only): the verdict the system proposed, returned by the lookup step (see below).
- `state`: the state of the item that step created or touched, afterward. A rejected `move` still reports the item's unchanged state. If the step touched no item (a rejected `create`, a `list`, or a `restart`), `state` is absent, so do not list it.
- `count`: the number of items, after a `list` step. A `list` step may also carry extra keys of its own (for example `"reorder_at"`) and may return extra aggregates (for example `accepted_total_usd`, `final_stock`, `low_stock`); these are part of your idea's cases, so agree their names with your teammates.
- Any hand-computed number (for example `total`, or `minutes`) as a plain key of the same name, written as a JSON number such as `98.5` (not a string); say which in `how_computed`.

**Idea 3 steps (claim check).** The same four steps, used like this:

- `create` as `submitter`, with `data` `{claim_id, claim_text, draft_cited_sources}`. Write `draft_cited_sources` as the string from the CSV, for example `"S1;S2"`. It gives outcome `accepted` and state `submitted`. It does not look anything up.
- **The lookup** is a `move` to `sourced` as `system`. It applies the four rules in `RULES.md` and stores a **proposed** verdict. The step reports state `sourced` and the extra key `proposed` (`verified`, `refuted`, or `unverifiable`). If the claim cites a source that is not in the frozen set, the step reports outcome `citation_not_found` (instead of `accepted`), `proposed` is `refuted`, and the state is still `sourced`.
- **The verdict** is a `move` to `verified`, `refuted`, or `unverifiable` as `verifier`, from `sourced` only. If the verifier picks a different verdict than `proposed`, that is an **override**: add a `"reason"` key to the step (for example `"reason": "second source found offline"`) and record the override in your audit log. A verdict is final: nothing moves out of it.
- Allowed moves: `submitted` to `sourced` (system only), and `sourced` to a verdict (verifier only). A move that is not on this list is `illegal_move`, and that is checked first. A move that is on the list but tried by the wrong role is `not_permitted`.

A build must be a **web app** (a browser page for each role that acts, plus the saved data store). `run.py` talks to the same code that the pages use (for example with the Flask test client, or HTTP calls to the running server), so one set of cases tests the real app. The Python standard library is enough (for example `wsgiref` and `sqlite3`). Flask is also fine: install it with `pip install flask` inside a virtual environment, and say so in your README.

At least one case for each of: the happy path, every state change a role is **not** allowed to make, each seeded failure from your idea's fixtures, a total or count that you computed by hand, and one restart check (stop, start, state is still there). Each case lists its steps, the expected result, and **how you computed the expected result** (for example "7.00 + 12.50 = 19.50, by hand"). You may add a case after the tests-first commit (for example the repeat test of your engineered failure).

## 4. Scoring against the contract

Phase 1 is scored against your cut line. Ideas 1–4 have no proposal: you state your cut line (what you will certainly finish and what you drop first) in `README.md`. Idea 5 uses the cut line in your own approved proposal. A smaller scope can earn full marks if the cut line says so up front. Missing contract files cost points; a missing cut-line feature costs nothing if the cut line excluded it.
