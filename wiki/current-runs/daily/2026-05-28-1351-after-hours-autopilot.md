# 2026-05-28-1351-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`; artifact tag: `after-hours`; review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- Alpaca regular market: closed (`is_open=false`), after-hours workflow에서는 `market_closed`를 예상 비차단 상태로 처리
- 초기 후보: `QQQ`, `NOK`, `XOM`, `ORCL`, `AMD`, `ADBE`, `INTC`, `LLY`

## 게이트 상태

- Alpaca core: PASS. Scheduler preflight의 account/positions/open orders/asset/quote rows와 fresh Alpaca MCP clock/account/position/order/quote 재확인을 사용.
- Universe strict: PASS. 62개 broad metadata universe, `SPY`, `QQQ` 포함.
- MCP strict: PASS. SEC EDGAR/FRED/Firecrawl/Yahoo Finance pass, Alpha Vantage는 `empty_response` gap이나 최소 research confirmation 3개 이상 충족.
- Quote/spread: NOK fresh overnight quote PASS. QQQ는 spread는 통과하지만 whole-share notional cap 초과로 제외.
- Separate after-hours budget: PASS. `risk_inputs.after_hours_new_orders_submitted_today=1`, session cap 2, planned order 1.
- Risk policy: PASS (`scripts/check-risk-policy.py --json`).

## 주문 후보

- Planned: NOK 1주 buy limit 15.40, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, client_order_id `ah-20260528-1351-nok-buy-01`.
- 제외: QQQ는 1주 notional이 after-hours per-order cap을 초과. INTC는 이전 after-hours validation bucket에서 이미 체결되어 즉시 중복 add를 피함.

## 원천

- `wiki/evidence-store/sources/2026-05-28-1351-after-hours-autopilot-alpaca-core-preflight.json`
- `wiki/evidence-store/sources/2026-05-28-1351-after-hours-autopilot-research-mcp-preflight.json`
- `wiki/trade-ledger/orders/2026-05-28-1351-after-hours-autopilot.json`
- `wiki/evidence-store/run-manifests/2026-05-28-1351-after-hours-autopilot.json`

## 실행 결과

- Submit: Alpaca MCP `place_stock_order` 1회 호출.
- Reconcile: `client_order_id=ah-20260528-1351-nok-buy-01`로 즉시 조회.
- Status: filled, NOK 1주, fill price 15.40.
- Post-trade: open US equity orders 없음, NOK position 402주 확인.
- Review bucket: `after_hours_validation`; horizons `next_regular_open`, `1D`, `5D`, `20D`.
