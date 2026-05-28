# portfolio-current

- 갱신: 2026-05-29 00:59 KST (`2026-05-29-0051-hourly-autopilot` post-trade reconciliation)
- Paper account only. 최신 account refresh는 runtime `cancelled` gap이므로 직전 성공 account snapshot과 이번 positions/open-order reconciliation을 함께 사용한다.
- Open US equity orders: 없음.
- 이번 실행 결과: AMZN 1주 buy limit 270.55 체결. INTC 1주 계획은 submit cancelled 및 same-client-id reconciliation 404 후 retry cancelled로 실제 주문 없음.
- Positions refresh: registered Alpaca MCP `get_all_positions` PASS, AMZN qty=2 avg_entry_price=270.30, INTC qty=1 유지, 총 position symbols 30개.
- Source refs: [[2026-05-29-0051-hourly-autopilot]], `wiki/trade-ledger/positions/2026-05-29-0051-hourly-autopilot-post-trade.json`.
