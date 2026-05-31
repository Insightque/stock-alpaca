# 2026-05-31-1431-after-hours-autopilot

## 요약

- 워크플로우: `harness/workflows/after-hours-autopilot.md`
- 세션: `after_hours`; policy profile: `after_hours_policy`; artifact tag: `after-hours`; review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인.
- 정규장 상태: Alpaca MCP scheduler preflight 기준 closed (`2026-05-31T01:31:05.351691263-04:00`), after-hours 실행 조건 충족.
- 주문 결과: 제출 없음. `place_stock_order` 호출 없음, `client_order_id` 없음, reconcile 해당 없음.

## 게이트 결과

| Gate | Result |
| --- | --- |
| Alpaca core preflight | pass rows retained; `first_blocking_gate=market_closed`는 장외 workflow에서 expected/nonblocking |
| Universe strict | PASS |
| MCP strict | PASS |
| Risk policy | PASS, empty order plan warning only |
| Fresh quote | FAIL |
| Spread | PASS |
| Separate after-hours budget | PASS, `risk_inputs.after_hours_new_orders_submitted_today=0` |

## 제출 차단 사유

QQQ 기준 quote가 장외 제출 freshness cap을 초과했다. Scheduler quote `2026-05-29T20:58:00.000802558Z`는 artifact 생성 시각 대비 약 1953.38분 old이다. `after_hours_policy.max_quote_age_minutes_submit=5.0`이므로 신규 장외 주문은 비실행 처리했다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-31-1431-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-31-1431-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-05-31-1431-after-hours-autopilot-after-hours-gate-evaluation.json`
- Scheduler Alpaca preflight: `wiki/evidence-store/sources/2026-05-31-1431-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research preflight: `wiki/evidence-store/sources/2026-05-31-1431-after-hours-autopilot-research-mcp-preflight.json`

## 주문/회고 버킷

주문 계획은 `market.session=after_hours`이고 주문 배열은 비어 있다. 장외 주문 예산은 regular validation count와 분리해 `after_hours_new_orders_submitted_today=0`으로 기록했다. 실제 주문이 없어 after-hours validation review bucket에 신규 fill/reconcile 항목은 없다.
