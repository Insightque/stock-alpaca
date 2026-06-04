# portfolio-current

_Last updated: 2026-06-05 01:03 KST_

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: $102,771.44
- Cash: $32,482.30
- Buying power: $257,589.13
- Long market value: $70,289.14

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-05-0051-hourly-autopilot]]
- Open/new: 없음. reconciliation 기준 XOM same-cycle order는 즉시 `filled`로 전환됐고 open order는 0건이다.
- Filled: `XOM` buy 1 @ 153.41 limit, `status=filled`, `filled_avg_price=153.26`, `client_order_id=hourly-20260605-0051-buy-xom`. same-day earlier fills `AAPL`, `QQQ`, `SPY`, `SLB`도 order history에 남아 있다.
- Position count observed by Alpaca MCP: 32
- Recent FILL scope: 이번 reconciliation 시점 기준 XOM 보유수량은 2주에서 3주로 늘었고 open order는 0건이다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-0051-hourly-autopilot-post-trade.json`

## 계좌 요약 주석

- 위 계좌 요약 수치는 scheduler core preflight의 마지막 confirmed snapshot이다.
- post-trade runtime `get_account_info` MCP call은 `cancelled`로 돌아와, 체결 자체는 `get_order_by_client_id`, `get_orders`, `get_account_activities(FILL)`, `get_all_positions`로 대조했다.
