# Idea 3 rules (read before writing `cases.json`)

**Files:** `submitted-claims.csv` (claim_id, claim_text, draft_cited_sources) and the frozen documents in `sources/` (see `sources/SOURCES.md` for what S1, S2 and the others are). Your tool may only use these frozen sources. No live web.

**Rules for the verdict.** Judge each claim against **all** frozen sources, not only the ones in `draft_cited_sources`. Apply these in order and stop at the first that fits:
1. **Missing citation:** the claim cites a source that is not in the frozen set. Verdict `refuted`, outcome `citation_not_found`.
2. **Contradiction:** at least **one** frozen source contradicts the claim. Verdict `refuted`.
3. **Verified:** no source contradicts it, and at least **two** frozen sources support it. Verdict `verified`.
4. **Unverifiable:** anything else (one source supports it and none contradict, or no source says anything). Verdict `unverifiable`.

"Support" means the source states the same fact at the precision the claim uses. `20:17` is supported by a source that says `20:17:40`, and "about 21.5 kg" is supported by "21.55 kg". A source contradicts a claim if it states a fact that cannot be true together with the claim: a different number, date, or name, or an incompatible event (for example, landed softly versus crashed). You may add an offset that a source states (for example, "approximately six hours after landing"). Your tool may hold a table of facts that you extracted from the frozen sources (the landing time, a weight); that is not hard-coding. Hard-coding is writing the expected verdict for a claim id. You may compute from times or figures a source states (for example, adding hours to a stated time), but not from your own outside knowledge.

**Roles and the checkpoint:** the **system** moves a claim from `submitted` to `sourced`: it looks up the sources and stores a **proposed** verdict by the four rules above (a claim that cites a missing source is proposed `refuted` with outcome `citation_not_found`). The **verifier** (a person) then confirms or overrides it, and is the only role that may set `verified`, `refuted`, or `unverifiable`. The submitter trying to set a verdict is rejected with outcome `not_permitted`. A verifier override is a verdict change made by the verifier and recorded in your audit log.

**What the files contain on purpose:** claims that agree with the sources, one that only one source covers, claims that a source contradicts, a number or a date that is a little off, and one claim that cites a source that does not exist. Decide each verdict yourself by reading the sources.

**Careful with dates and times:** a UTC date and a US date can differ for the same event. If a claim's truth depends on the time zone, state in your `README.md` which zone rule you use and apply it the same way everywhere. Your cases are checked against the rule you wrote.
