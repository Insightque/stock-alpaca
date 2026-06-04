# portfolio-current

_Last updated: 2026-06-05 02:22 KST_

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: $103,311.34
- Cash: $31,649.57
- Buying power: $256,800.45
- Long market value: $71,661.77

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-05-0211-hourly-autopilot]]
- Open/new: 없음. same-day earlier fills `GOOGL`, `COP`, `FCX`, `WMT`, `XOM`, `AAPL`, `SLB`, `SPY`, `QQQ`는 order history에 남아 있다.
- Filled: `GOOGL` buy 1 @ `372.48` limit, `filled_avg_price=372.43`, `client_order_id=hourly-20260605-0211-buy-googl`.
- Position count observed by Alpaca MCP: 32
- Recent reconciliation scope: `get_order_by_client_id`, `get_orders(symbol=GOOGL)`, `get_all_positions`, `get_account_info` 기준 GOOGL fill과 updated position/account state를 확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-0211-hourly-autopilot-post-trade.json`

## 계좌 요약 주석

- 위 계좌 요약 수치는 submit 이후 runtime `get_account_info` MCP call 기준이다.
- GOOGL는 2주에서 3주로 증가했고 평균단가는 `381.52 USD`로 갱신됐다.
- `get_orders(status=open)`와 `get_account_activities_by_type(FILL)`는 tool-layer `cancelled`였지만, order/position/account state 대조는 모두 완료했다.
