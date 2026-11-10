# Merge Decision Log (Phase 2, team)

**Base chosen:** *e.g., Dana's build.* **Why:** *e.g., it passes 11 of 14 cases, uses SQLite, and has an audit log. The others keep orders in memory.*

| Component | From whom | Commit hash | Kept or dropped | Reason (about the system) |
|---|---|---|---|---|
| *e.g., low-stock alert* | *e.g., Lee* | *e.g., 9f3c2ab* | *e.g., kept* | *e.g., the base had no alert, and Lee's passes its two cases after the port* |
| *e.g., in-memory order store* | *e.g., Lee* | *e.g., n/a* | *e.g., dropped* | *e.g., loses orders on restart; the base's SQLite store does not* |
