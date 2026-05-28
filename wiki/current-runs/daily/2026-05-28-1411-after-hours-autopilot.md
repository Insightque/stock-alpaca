# 2026-05-28-1411-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`; artifact tag: `after-hours`; review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- Alpaca regular market: closed (`is_open=false`, `2026-05-28T01:13:25.825028326-04:00`), after-hours workflow에서는 `market_closed`를 예상 비차단 상태로 처리
- Scheduler preflight: `2026-05-28-1411-after-hours-autopilot-alpaca-core-preflight.json`, `2026-05-28-1411-after-hours-autopilot-research-mcp-preflight.json` 사용

## 게이트 상태

- Alpaca core: PASS. Scheduler preflight의 account/positions/open orders/asset/quote/spread rows와 fresh Alpaca MCP clock/account/positions/orders 조회를 사용.
- Universe strict: PASS. 62개 broad metadata universe, `SPY`, `QQQ` 포함.
- MCP strict: PASS. SEC EDGAR/FRED/Firecrawl/Yahoo Finance pass, Alpha Vantage는 `empty_response` gap이나 최소 research confirmation 3개 이상 충족.
- Separate after-hours budget: FAIL. Alpaca MCP `get_orders`와 기존 after-hours order plan 기준 `after_hours_new_orders_submitted_today=2`, `after_hours_policy.max_new_orders_per_session=2`.
- Risk policy: FAIL. `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1411-after-hours-autopilot.json`를 실행했으나 현재 system Python에 PyYAML이 없어 validator load 단계에서 실패.

## 주문 계획

- 제출 주문 없음.
- Order plan은 `market.session=after_hours`, `risk_inputs.after_hours_new_orders_submitted_today=2`, `orders=[]`로 기록.
- 예산 gate가 이미 실패했고 risk validator도 PASS하지 않았으므로 `place_stock_order` 호출 전 pre-submit gate summary 단계로 진행하지 않았다.

## 검증

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-28-1411-after-hours-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-28-1411-after-hours-autopilot.json`: PASS
- `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1411-after-hours-autopilot.json`: FAIL, `PyYAML is required to load harness/risk-policy.yaml`

## 원천

- `wiki/evidence-store/sources/2026-05-28-1411-after-hours-autopilot-alpaca-core-preflight.json`
- `wiki/evidence-store/sources/2026-05-28-1411-after-hours-autopilot-research-mcp-preflight.json`
- `wiki/trade-ledger/orders/2026-05-28-1411-after-hours-autopilot.json`
- `wiki/evidence-store/run-manifests/2026-05-28-1411-after-hours-autopilot.json`

## 실행 결과

- Submit: 없음.
- Reconcile: submit attempt가 없어서 불필요.
- Review bucket: 신규 체결이 없어 추가 review marker 없음. 기존 `INTC`, `NOK` after-hours fills는 `after_hours_validation` bucket에 유지.
