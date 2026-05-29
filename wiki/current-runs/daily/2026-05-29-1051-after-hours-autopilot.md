# 2026-05-29-1051-after-hours-autopilot

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
| Regular market not open | PASS | Alpaca MCP clock `2026-05-28T21:52:58.896313726-04:00`, `is_open=false` |
| Alpaca core | PASS | Scheduler preflight의 account/positions/open orders/asset/quote rows와 fresh Alpaca MCP clock/account/position/order/quote 확인 사용 |
| Universe strict | PASS | 62개 broad metadata universe, `SPY`, `QQQ` 포함 |
| MCP strict | PASS | SEC EDGAR/FRED/Firecrawl/Yahoo Finance pass. Alpha Vantage는 daily rate limit `provider_error`이나 최소 research confirmation 3개 충족 |
| Separate after-hours budget | PASS | 같은 after-hours session의 fill activity에서 ADBE 1건 확인. `risk_inputs.after_hours_new_orders_submitted_today=1`, cap 2 |
| Quote/spread | MIXED | NOK/NVDA는 fresh quote와 spread 통과. ADBE/XOM/LIN은 spread 또는 freshness 실패, QQQ/SPY/SMH는 notional cap 초과 |
| Ticker thesis | BLOCK | NOK는 신규 추격 금지 thesis, NVDA는 AI semiconductor 집중도 회피 |
| Risk policy | PASS | `scripts/check-risk-policy.py --json` PASS, empty-order warning only |

## 주문 후보 판단

- `NOK`: fresh overnight quote, spread 약 0.1301%로 통과했지만, [[NOK]] thesis에 신규 추격 금지가 있어 보유 유지 후보로만 기록.
- `NVDA`: fresh overnight quote, spread 약 0.1963%로 통과했지만 기존 AI semiconductor 노출이 커서 장외 validation에서 추가하지 않음.
- `XOM`: fresh overnight quote지만 spread 약 0.3064%로 after-hours cap 0.25%를 초과.
- `ADBE`: 09:11 after-hours run에서 이미 1주 체결됐고 현재 quote spread가 after-hours cap을 초과해 제외.
- `QQQ`, `SPY`, `SMH`: 1주 notional이 after-hours per-order cap보다 커서 제외.
- `LIN`: quote stale 및 after-hours spread cap 초과로 제외.

## 실행 결과

- 주문 계획: `wiki/trade-ledger/orders/2026-05-29-1051-after-hours-autopilot.json`, `market.session=after_hours`, `orders=[]`, `risk_inputs.after_hours_new_orders_submitted_today=1`.
- Submit: `place_stock_order` 호출 없음.
- Reconcile: 제출 시도가 없었으므로 신규 `client_order_id` reconciliation 대상 없음. 같은 after-hours session의 기존 ADBE fill은 Alpaca MCP order/activity에서 확인.
- Review bucket: 신규 체결 없음. 기존 ADBE 체결의 `after_hours_validation` 회고 일정은 유지.

## 원천

- `wiki/evidence-store/sources/2026-05-29-1051-after-hours-autopilot-alpaca-core-preflight.json`
- `wiki/evidence-store/sources/2026-05-29-1051-after-hours-autopilot-research-mcp-preflight.json`
- `wiki/evidence-store/run-manifests/2026-05-29-1051-after-hours-autopilot.json`
- `wiki/trade-ledger/orders/2026-05-29-1051-after-hours-autopilot.json`

## 검증

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-1051-after-hours-autopilot.json` PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-1051-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-29-1051-after-hours-autopilot.json` PASS with `orders is empty` warning
