# 2026-05-31-0811-after-hours-autopilot

## 요약

- 워크플로우: `harness/workflows/after-hours-autopilot.md`
- 세션: `after_hours`
- 정책 프로필: `after_hours_policy`
- artifact tag: `after-hours`
- review bucket: `after_hours_validation`
- 결과: 주문 없음. `fresh_quote` gate 실패로 `place_stock_order`를 호출하지 않았다.

## 사용한 원천

- Scheduler Alpaca core preflight: `wiki/evidence-store/sources/2026-05-31-0811-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research MCP preflight: `wiki/evidence-store/sources/2026-05-31-0811-after-hours-autopilot-research-mcp-preflight.json`
- Runtime Alpaca MCP spot-check: `wiki/evidence-store/sources/2026-05-31-0811-after-hours-autopilot-runtime-alpaca-spot-check.json`

Scheduler Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours workflow에서 예상되는 상태라 단독 차단 사유로 보지 않았다. 같은 preflight와 runtime Alpaca MCP read-only spot-check로 정규장 닫힘, 계좌/포지션 preflight PASS, open US-equity orders `[]`, QQQ active/tradable/overnight_tradable, QQQ overnight quote/snapshot evidence를 확인했다. Runtime account/positions standalone call은 tool layer에서 cancelled 되었으므로 scheduler-owned account/positions PASS row를 유지했다.

## Gate 결과

- `ALPACA_PAPER_TRADE=true`: PASS
- 정규장 열림 여부: 정규장 닫힘 PASS (`2026-05-30T19:13:03.12927549-04:00`)
- after-hours profile/session/artifact/review bucket 분리: PASS
- 별도 after-hours 주문 예산: PASS. `risk_inputs.after_hours_new_orders_submitted_today=0`; regular validation order count를 재사용하지 않았다.
- universe strict: PASS
- MCP strict: PASS. sec-edgar, firecrawl, yahoo-finance 3개 research confirmation 확보; alpha-vantage empty response와 FRED 429 provider error는 provider gap으로 기록했다.
- risk policy: PASS. 주문 후보가 없어 `orders is empty` warning만 존재한다.
- quote freshness: FAIL. QQQ runtime overnight quote `2026-05-29T08:00:00.386377592Z`는 의사결정 시점 기준 약 2353.05분 경과해 `after_hours_policy.max_quote_age_minutes_submit=5.0`을 초과했다.
- spread gate: QQQ spread는 약 0.2025%로 after-hours cap 0.25% 이내였지만 stale quote 때문에 주문 제출 근거로 사용하지 않았다.

## 주문 및 reconcile

- 주문 계획: `wiki/trade-ledger/orders/2026-05-31-0811-after-hours-autopilot.json`
- `market.session=after_hours`: 설정됨
- `risk_inputs.after_hours_new_orders_submitted_today=0`: 설정됨
- 주문 수: 0
- `client_order_id`: 없음
- `place_stock_order`: 호출하지 않음
- reconciliation: submit attempt가 없어서 해당 없음

## 검증

- `check-universe-coverage.py --strict --json`: PASS
- `check-mcp-coverage.py --strict --json`: PASS
- `check-risk-policy.py --json`: PASS (`orders is empty` warning)
