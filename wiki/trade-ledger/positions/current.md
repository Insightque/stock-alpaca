# portfolio-current

- 갱신: 2026-05-29 01:18 KST (`2026-05-29-0111-hourly-autopilot` post-trade reconciliation)
- Paper account only. 최신 account refresh는 runtime `cancelled` gap이므로 scheduler account preflight와 이번 positions/open-order/fill reconciliation을 함께 사용한다.
- Open US equity orders: 없음.
- 이번 실행 결과: XOM 1주 buy limit 148.37 체결.
- Positions refresh: registered Alpaca MCP `get_all_positions` PASS, XOM qty=2 avg_entry_price=147.72, 총 position symbols 31개.
- Source refs: [[2026-05-29-0111-hourly-autopilot]], `wiki/trade-ledger/positions/2026-05-29-0111-hourly-autopilot-post-trade.json`.
