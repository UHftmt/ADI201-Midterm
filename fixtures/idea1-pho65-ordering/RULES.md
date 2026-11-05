# Idea 1 rules (read before writing `cases.json`)

**Files:** `menu-stock.csv` (item_id, name, price_usd, stock_on_hand) and `order-requests.csv` (request_id, customer, item_id, qty, payment_choice). Process requests **in file order**. Money is US dollars with two decimals.

**Rules**
1. `sandbox_card` orders are `paid` when accepted. `pay_in_store` orders are `placed` when accepted.
2. A request is `out_of_stock` if `qty` is more than the item's current stock. Rejected requests change nothing.
3. An accepted request reduces stock by `qty`. Later requests see the reduced stock.
4. A second request with a `request_id` you have already seen is `duplicate_request`. The first one stays as it was. An id counts as seen as soon as it has been processed, even if that request was rejected (for example `out_of_stock`).
5. An order total is the sum of price x qty. Sandbox means no real money moves.
6. A `qty` of 0 or less, or an `item_id` that is not in `menu-stock.csv`, is rejected with outcome `invalid_request`. Rejected requests change nothing.

**What the files contain on purpose:** at least one repeated request id, at least one request for an item with too little stock, and a mix of both payment choices. Work out which rows by reading the files yourself, then compute stock and totals by hand.

**Not in the files:** the other states (`in_progress`, `ready`, `picked_up`, `abandoned`) and role limits. Write your own extra inputs in `cases.json` for those.
