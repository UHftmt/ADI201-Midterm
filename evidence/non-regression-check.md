# Non-Regression Check (Phase 2, team)

Write your prediction **before** running. A case that fails only because a component is not merged yet is expected. Any other failure is a regression in the base.

| Member | Case | On own build | Merged, before porting (prediction) | Merged, before porting (result) | Merged, after porting | Port commit |
|---|---|---|---|---|---|---|
| *e.g., A* | *e.g., totals* | *e.g., PASS* | *e.g., PASS* | *e.g., PASS* | *e.g., PASS* | *e.g., (none)* |
| *e.g., B* | *e.g., low_stock_alerts* | *e.g., PASS* | *e.g., FAIL (component not merged)* | *e.g., FAIL* | *e.g., PASS* | *e.g., cb85728* |

**Transfer trial** (a teammate who did not do the merge): time taken *e.g., 14 minutes*; commands run *e.g., 5*; what they had to ask *e.g., which Python version*; README fixed *e.g., added the version line*.
