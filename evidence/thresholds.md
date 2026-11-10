# Continue / Revise / Stop Thresholds (ADI501 only, Phase 2, 3 points)

Use the measure from your `baseline-vs-pilot.md`. Give numbers, not words. The three rules must cover every possible result, with no gaps and no overlap. Your tool does not run a real pilot, so these thresholds are your rules for a pilot you would run next; say what you would measure and for how long.

| Decision | Rule (numbers) | Example (booking tool, minutes for 20 bookings) |
|---|---|---|
| Continue | | *Pilot 10 minutes or less AND zero double-bookings in the 20-request test* |
| Revise | | *Pilot more than 10 up to 25 minutes, OR one to two double-bookings* |
| Stop | | *Pilot more than 25 minutes, OR three or more double-bookings, OR any real client data exposed* |

**Why these numbers (2 sentences):** *e.g., The baseline is 34 minutes, so a 70% cut is a clear win. Any exposure of client data stops the pilot because trust is hard to rebuild.*
