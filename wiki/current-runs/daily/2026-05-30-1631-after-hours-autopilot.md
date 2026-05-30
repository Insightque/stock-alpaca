# 2026-05-30-1631-after-hours-autopilot

## 요약

- 워크플로우: `harness/workflows/after-hours-autopilot.md`
- 세션: `after_hours`
- 정책 프로필: `after_hours_policy`
- artifact tag: `after-hours`
- review bucket: `after_hours_validation`
- 결과: 주문 없음. `fresh_quote` gate 실패로 `place_stock_order`를 호출하지 않았다.

## 사용한 원천

- Scheduler Alpaca core preflight: `wiki/evidence-store/sources/2026-05-30-1631-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research MCP preflight: `wiki/evidence-store/sources/2026-05-30-1631-after-hours-autopilot-research-mcp-preflight.json`
- Runtime Alpaca MCP spot-check: `wiki/evidence-store/sources/2026-05-30-1631-after-hours-autopilot-runtime-alpaca-spot-check.json`

Scheduler Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours workflow에서 예상되는 상태라 단독 차단 사유로 보지 않았다. 같은 preflight의 account, positions, open orders, asset, quote/spread 행을 사용했고, runtime Alpaca MCP로 정규장 폐장, 계좌/포지션 조회 가능, 미체결 US equity 주문 없음, QQQ active/tradable/overnight_tradable, QQQ overnight quote를 재확인했다.

## Gate 결과

- `ALPACA_PAPER_TRADE=true`: PASS
- 정규장 열림 여부: 정규장 닫힘 PASS
- after-hours profile/session/artifact/review bucket 분리: PASS
- universe strict: PASS
- MCP strict: PASS
- risk policy: PASS, empty order plan warning만 존재
- quote freshness: FAIL. QQQ overnight quote timestamp `2026-05-29T08:00:00.386377592Z`는 의사결정 시점 기준 약 1412.8분 경과해 `after_hours_policy.max_quote_age_minutes_submit=5.0`을 초과했다.
- spread gate: stale quote 때문에 주문 제출 gate로 평가하지 않음

## 주문 및 reconcile

- 주문 계획: `wiki/trade-ledger/orders/2026-05-30-1631-after-hours-autopilot.json`
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
