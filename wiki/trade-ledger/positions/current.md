# portfolio-current

- 갱신: 2026-05-29 06:25 KST (`2026-05-29-0625-analyst-review-cycle` read-only reconciliation)
- Paper account only. `ALPACA_PAPER_TRADE=true` 확인. 이 workflow는 주문 제출/교체/취소/청산을 하지 않았다.
- Account: `ACTIVE`, portfolio_value 102374.13, cash 37187.61, buying_power 133318.68, long_market_value 65186.52.
- Market clock: 2026-05-28 17:21:29 ET 기준 closed, next open 2026-05-29 09:30 ET.
- Open US equity orders: 없음.
- Positions refresh: registered Alpaca MCP `get_all_positions` PASS, 총 position symbols 31개.
- Recent fills/orders: registered Alpaca MCP `get_orders`와 `get_account_activities`로 2026-05-22 이후 fills/canceled/expired orders를 reconciliation했다.
- Portfolio history: `get_portfolio_history` 3회 cancelled, `gap_category=cancelled`, `retry_count=2`.
- Source refs: [[2026-05-29-portfolio-review]], [[2026-05-29-0625-analyst-review-cycle-sources]].
