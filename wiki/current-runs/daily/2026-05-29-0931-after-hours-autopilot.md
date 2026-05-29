# 2026-05-29-0931-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`; artifact tag: `after-hours`; review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- Alpaca regular market: closed (`is_open=false`), after-hours workflow에서는 `market_closed`를 예상 비차단 상태로 처리
- 초기 후보: `QQQ`, `NOK`, `SMH`, `SPY`, `NVDA`, `ADBE`, `LIN`, `XOM`

## 게이트 상태

| Gate | Status | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `ALPACA_PAPER_TRADE=true` |
| Regular market not open | PASS | Alpaca MCP clock `2026-05-28T20:33:24.772390256-04:00`, `is_open=false` |
| Alpaca core | PASS | Scheduler preflight의 account/positions/open orders/asset/quote rows와 fresh Alpaca MCP clock/position/order/quote 확인 사용 |
| Universe strict | PASS | 62개 broad metadata universe, `SPY`, `QQQ` 포함 |
| MCP strict | PASS | SEC EDGAR/Firecrawl/Yahoo Finance pass. Alpha Vantage는 `empty_response`, FRED는 timeout이나 최소 research confirmation 3개 충족 |
| Separate after-hours budget | PASS | 같은 after-hours session의 Alpaca order query에서 ADBE 1건 확인. `risk_inputs.after_hours_new_orders_submitted_today=1`, cap 2 |
| Quote/spread | MIXED | NOK/NVDA는 fresh quote와 spread 통과. ADBE/XOM/LIN은 spread 또는 중복-session 제약으로 제외 |
| Risk policy | PASS | `scripts/check-risk-policy.py --json` PASS, empty-order warning only |

## 주문 후보 판단

- `NOK`: fresh overnight quote, spread 약 0.0647%로 통과했지만, [[NOK]] thesis에 20D 과열 구간으로 신규 추격 금지가 있어 보유 유지 후보로만 기록.
- `NVDA`: fresh overnight quote, spread 약 0.028%로 통과했지만 기존 AI semiconductor 노출이 커서 장외 validation에서 추가하지 않음.
- `ADBE`: 09:11 after-hours run에서 이미 1주 체결됐고 현재 quote spread가 after-hours cap을 초과해 제외.
- `QQQ`, `SPY`, `SMH`: 1주 notional이 after-hours per-order cap보다 커서 제외.
- `XOM`, `LIN`: after-hours spread cap 초과로 제외.

## 실행 결과

- 주문 계획: `wiki/trade-ledger/orders/2026-05-29-0931-after-hours-autopilot.json`, `market.session=after_hours`, `orders=[]`, `risk_inputs.after_hours_new_orders_submitted_today=1`.
- Submit: `place_stock_order` 호출 없음.
- Reconcile: 제출 시도가 없었으므로 신규 `client_order_id` reconciliation 대상 없음. 직전 after-hours 주문은 Alpaca MCP `get_orders`에서 `ah-20260529-0911-adbe-buy-01` filled로 확인.
- Review bucket: 신규 체결 없음. 기존 ADBE 체결의 `after_hours_validation` 회고 일정은 유지.

## 원천

- `wiki/evidence-store/sources/2026-05-29-0931-after-hours-autopilot-alpaca-core-preflight.json`
- `wiki/evidence-store/sources/2026-05-29-0931-after-hours-autopilot-research-mcp-preflight.json`
- `wiki/evidence-store/run-manifests/2026-05-29-0931-after-hours-autopilot.json`
- `wiki/trade-ledger/orders/2026-05-29-0931-after-hours-autopilot.json`

## 검증

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-0931-after-hours-autopilot.json` PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-0931-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-29-0931-after-hours-autopilot.json` PASS with `orders is empty` warning
