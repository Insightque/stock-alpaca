# 2026-05-29-0911-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`; artifact tag: `after-hours`; review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- Alpaca regular market: closed (`is_open=false`), after-hours workflow에서는 `market_closed`를 예상 비차단 상태로 처리
- 초기 후보: `QQQ`, `NOK`, `SMH`, `SPY`, `NVDA`, `ADBE`, `LIN`, `XOM`

## 게이트 상태

- Alpaca core: PASS. Scheduler preflight의 account/positions/open orders/asset/quote rows와 fresh Alpaca MCP clock/account/position/order/asset/quote 재확인을 사용.
- Universe strict: PASS. 62개 broad metadata universe, `SPY`, `QQQ` 포함.
- MCP strict: PASS. SEC EDGAR/Firecrawl/Yahoo Finance pass, Alpha Vantage는 `empty_response`, FRED는 504 `provider_error`이나 최소 research confirmation 3개 이상 충족.
- Quote/spread: ADBE fresh overnight quote PASS, spread 0.0866%로 `after_hours_policy.max_spread_pct=0.25` 이내. XOM은 fresh였지만 0.4509% spread로 제외.
- Separate after-hours budget: PASS. `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap 2, planned order 1.
- Risk policy: PASS (`scripts/check-risk-policy.py --json`).

## 주문 후보

- Planned: ADBE 1주 buy limit 242.58, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, client_order_id `ah-20260529-0911-adbe-buy-01`.
- 제외: QQQ/SPY는 1주 notional이 after-hours per-order cap을 초과. NVDA는 quote/spread는 통과하지만 기존 AI semiconductor exposure가 커서 추가하지 않음. XOM은 spread gate 실패.

## 원천

- `wiki/evidence-store/sources/2026-05-29-0911-after-hours-autopilot-alpaca-core-preflight.json`
- `wiki/evidence-store/sources/2026-05-29-0911-after-hours-autopilot-research-mcp-preflight.json`
- `wiki/trade-ledger/orders/2026-05-29-0911-after-hours-autopilot.json`
- `wiki/evidence-store/run-manifests/2026-05-29-0911-after-hours-autopilot.json`

## 실행 결과

- Submit: Alpaca MCP `place_stock_order` 1회 호출.
- Reconcile: `client_order_id=ah-20260529-0911-adbe-buy-01`로 즉시 조회.
- Status: filled, ADBE 1주, fill price 242.36.
- Post-trade: open US equity orders 없음, ADBE position 1주 확인.
- Post-trade artifact: `wiki/trade-ledger/positions/2026-05-29-0911-after-hours-autopilot-post-trade.json`
- Review bucket: `after_hours_validation`; horizons `next_regular_open`, `1D`, `5D`, `20D`.
