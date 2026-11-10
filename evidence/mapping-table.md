# Mapping table (Phase 2)

One table per non-base member. It says what that member's names mean in the base build, so that their `cases.json` still means the same thing. The common words (states, outcomes, roles, step names) are fixed by the project contract and do not need mapping; map **your internal names** to them.

## Member: *(name)*  ->  base: *(name)*

| Kind | Their name | Base name | Note |
|---|---|---|---|
| entity | *e.g., Order* | *e.g., Ticket* | |
| field | *e.g., `order_ref`* | *e.g., `request_id`* | |
| state | *e.g., `cooking`* | *e.g., `in_progress`* | |
| outcome | *e.g., `NO_STOCK`* | *e.g., `out_of_stock`* | |
| route / page | *e.g., `/kitchen`* | *e.g., `/staff/queue`* | |
| method / function | *e.g., `Counter.low_stock()`* | *e.g., `Shop.low_stock()`* | *if a name has no equivalent in the base, say so and how you port it* |

*The example rows show the style. Replace them with your own.*
