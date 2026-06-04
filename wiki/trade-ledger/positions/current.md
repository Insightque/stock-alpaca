# portfolio-current

_Last updated: 2026-06-05 01:41 KST_

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: $103,185.52
- Cash: $32,141.17
- Buying power: $257,576.32
- Long market value: $71,044.35

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-05-0131-hourly-autopilot]]
- Open/new: 없음. reconciliation 기준 `FCX` same-cycle order는 즉시 `filled`로 전환됐고 open order는 0건이다.
- Filled: `FCX` buy 1 @ `69.58` limit, `status=filled`, `filled_avg_price=69.51`, `client_order_id=hourly-20260605-0131-buy-fcx`. same-day earlier fills `WMT`, `XOM`, `AAPL`, `SLB`, `SPY`, `QQQ`도 order history에 남아 있다.
- Position count observed by Alpaca MCP: 32
- Recent FILL scope: 이번 reconciliation 시점 기준 `FCX` 보유수량은 1주에서 2주로 늘었고 open order는 0건이다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-0131-hourly-autopilot-post-trade.json`

## 계좌 요약 주석

- 위 계좌 요약 수치는 submit 이후 runtime `get_account_info` MCP call 기준이다.
- runtime `get_order_by_client_id`, symbol-specific `get_orders`, `get_account_activities(FILL)`, `get_all_positions`가 모두 FCX fill과 수량 증가를 확인했다.
- `get_orders(status=open)` 전체 조회 1회는 tool-layer `cancelled`였지만, `get_orders(status=open, symbols=FCX)` 재조회는 0건이었고 same-cycle order는 `filled`로 종결됐다.
