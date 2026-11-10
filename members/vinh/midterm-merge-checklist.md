# Phase 2 Merge Checklist (team)

Use one shared repository. The merge is finished only when every member's known-answer tests pass on the merged system. "It runs" does not count.

## Step 0: Before you touch code (15 minutes)
- [ ] Every member's `phase1-submit` tag exists, even if the build is partial. (Phase 1 was a ZIP, so the tag is in your own repository.)
- [ ] **Shared repository recipe.** One member (any member; the base is chosen in Step 1 and may be someone else) creates a **private** GitHub repository (the whole team needs a free GitHub account) and adds the teammates and the instructor (ask in class for the username). Everyone adds it as a remote: `git remote add team <repo-url>`. Every member's Phase 1 tag has the same name, so push yours under your own name: `git push team phase1-submit:refs/tags/phase1-submit-<yourname>`. The member who created the repository also runs `git push team HEAD:main`.
- [ ] **Bring the other members' builds in with their history** (the grade for individual work reads each member's commits, so never delete their `.git`). From the base repository, for each other member: `git remote add <name> <path-or-url-of-their-repo>`, `git fetch <name>`, `git merge -s ours --no-commit --allow-unrelated-histories <name>/main`, `git read-tree --prefix=members/<name>/ -u <name>/main`, `git commit -m "bring in <name>'s Phase 1 build"`. Their cases go to `tests/known-answer/<name>/cases.json`, and the merged `run.py` runs every `tests/known-answer/*/cases.json` (the starter `run.py` already does this).
- [ ] Each member runs their own `tests/known-answer/run.py` on their own build and records the result in the "own build" column of `evidence/non-regression-check.md`.

## Step 1: Pick one architecture (the base)
- [ ] The team picks one member's build as the **base**. Do not concatenate files from several builds.
- [ ] Record the reason in `evidence/merge-decision-log.md`. Prefer the base that already passes the most tests and has persistence, roles, and an audit trail.

## Step 2: Map names
- [ ] For every other member's build, fill in `evidence/mapping-table.md`, one table each (its job is to guide **porting code** and to translate the member's `run.py` hooks; the cases already use the common words): entity, field, state, and outcome names (theirs, then the base's). Example: `order_ref` is `request_id`; `cooking` is `in_progress`; `NO_STOCK` is `out_of_stock`.
- [ ] Write one `tests/known-answer/run.py` for the merged system that translates to the common vocabulary (see the project contract).

## Step 3: Predict, then check (the failure drill)
- [ ] Before porting anything, run **every member's** `cases.json` on the base alone. Write down which cases you expect to fail, and why.
- [ ] Run them. Put the real results beside your prediction in `evidence/non-regression-check.md` (the "merged, before porting" column). A case that fails because a component is missing is expected; a case that fails for any other reason is a regression in the base.

## Step 4: Port components, one at a time
For each component you keep from a non-base member:
- [ ] Port it into the base using the mapping table. One commit per component, message names the source member and file.
- [ ] Rerun every member's cases after **each** port. Stop and fix if a case that passed now fails.
- [ ] Add a row to the merge decision log: component, from whom, commit hash, kept or dropped, reason.

## Step 5: What you drop
- [ ] Every dropped component has a reason that is about the system, not about the person. Example: "in-memory store loses orders on restart, so we kept the SQLite version."

## Step 6: Final checks
- [ ] All cases from all members pass on the merged system ("merged, after porting" column has no `FAIL`).
- [ ] **Transfer trial:** a teammate who did not do the merge clones the repo into a clean folder and follows only `README.md`. Record the time, the commands, and anything they had to ask. Fix the README for what they hit.
- [ ] Every member can explain every component, including ones they did not write. Phase 3 asks.
- [ ] Support-burden and continue / revise / stop thresholds are done (ADI501 only). Each ADI501 student commits their own two files in `adi501/<name>/` in the shared repository; the team's Drive link is to the ZIP of the merged repository, which therefore contains them.

## What a good non-regression table looks like

| Member | Case | On own build | Merged, before porting | Merged, after porting |
|---|---|---|---|---|
| A | totals | PASS | PASS | PASS |
| B | low_stock_alerts | PASS | FAIL (component not merged) *(expected)* | PASS |

*e.g., the two columns for B's `low_stock_alerts` show the merge doing its job: the case fails before the port because the base has no such component, and passes after it.*
