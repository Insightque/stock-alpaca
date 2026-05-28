# portfolio-current

2026-05-28 23:42 KST hourly autopilot post-trade reconciliation 후 갱신.

- Paper account: Alpaca MCP post-submit account refresh는 runtime에서 `cancelled`되어 23:31 scheduler preflight account snapshot을 기준으로 유지한다. Preflight 기준 cash 39,805.64, portfolio value 101,433.68.
- New submitted orders: SO 1주 buy limit 93.55 filled at 93.38; GOOGL 1주 buy limit 389.00 open/new.
- Not submitted: HOOD 1주 buy는 first submit cancelled, same-client-id reconciliation 404, same-id retry도 runtime safety monitor cancelled로 실제 주문 없음.
- Open orders: `hourly-20260528-2331-googl-buy-01` GOOGL 1주 buy limit 389.00 status new.
- Position check: Alpaca MCP `get_all_positions` PASS. SO position is 2 shares, avg_entry_price 93.83; WMT and PFE previous regular-session fills are reflected at 2 shares each.

Source refs: `wiki/evidence-store/run-manifests/2026-05-28-2331-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2331-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-28-2331-hourly-autopilot-post-trade.json`.
