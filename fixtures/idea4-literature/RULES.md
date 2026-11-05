# Idea 4 rules (read before writing `cases.json`)

**Files:** `draft-citations.csv` (cite_id, claim, source_id, quoted_text, url) and the frozen set in `sources/` (`papers.json`, `arxiv-metadata.atom`). No live web.

**Rules**
1. **Link check (offline):** a URL is live if and only if it is exactly equal to the `url` field of a source in `papers.json`. Otherwise `dead_link`.
2. **Quote check:** the quoted text must be an exact substring of that source's frozen abstract. Otherwise `quote_not_found`.
3. **Source check:** a `source_id` that is not in the frozen set is `invented_reference`.
4. A reviewer (a person) must open every source before a citation can be `accepted`. A citation that fails any check is `rejected`.

**What the files contain on purpose:** citations that pass all checks, and at least one for each failure word above. Work out which by reading the files, using only the three rules.
