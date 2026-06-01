# 2026-06-01-1231-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인

이번 실행은 Alpaca 정규장이 닫힌 상태에서 장외 workflow로 진행했다. Scheduler-owned Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 실행에서 예상된 상태라 단독 차단 사유로 보지 않았다. 같은 preflight와 런타임 Alpaca MCP spot-check로 account, open orders, prior after-hours order history, QQQ overnight quote/spread를 확인했다. Positions와 asset live spot-check는 MCP runtime에서 cancelled 되었지만 scheduler-owned pass row가 있어 after-hours-required evidence로 사용했다.

## Gate 결과

| Gate | 결과 | 메모 |
| --- | --- | --- |
| paper mode | PASS | `.env`에서 true 확인, 값 외 정보는 기록하지 않음 |
| regular market open | PASS | Alpaca MCP clock 기준 정규장 닫힘 |
| after-hours policy profile | PASS | `after_hours_policy` 사용 |
| Alpaca core MCP | PASS | `market_closed`는 장외에서 expected/nonblocking, 계좌/포지션/주문/asset/quote row 사용 가능 |
| universe strict | PASS | strict validator 통과 |
| MCP strict | PASS | research confirmations 3개 충족, FRED 429은 provider gap으로 기록 |
| quote/spread | PASS BUT NOT ACTIONABLE | QQQ overnight quote fresh, spread 약 0.0108%; 예산 소진으로 신규 후보 없음 |
| risk policy | PASS | empty order plan, `orders is empty` warning만 있음 |
| separate after-hours order budget | BLOCK | `risk_inputs.after_hours_new_orders_submitted_today=2`, session limit 2 도달 |

## 주문 결정

신규 주문 없음. `after_hours_new_orders_submitted_today=2`가 이미 `after_hours_policy.max_new_orders_per_session=2`에 도달했기 때문에 submit path 진입 전에 차단했다. 따라서 `place_stock_order` 호출, 신규 `client_order_id` 생성, retry, alternate client id 사용은 모두 없었다.

관측된 장외 session 주문:

- `ah-20260601-0911-nvda-buy-01`: canceled, filled_qty 0, `extended_hours=true`
- `ah-20260601-0931-avgo-buy-01`: filled, filled_qty 1, `extended_hours=true`

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-01-1231-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-01-1231-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-01-1231-after-hours-autopilot-after-hours-gate-evaluation.json`
- Scheduler Alpaca preflight: `wiki/evidence-store/sources/2026-06-01-1231-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research preflight: `wiki/evidence-store/sources/2026-06-01-1231-after-hours-autopilot-research-mcp-preflight.json`

## 검증

- `check-universe-coverage.py --strict --json`: PASS
- `check-mcp-coverage.py --strict --json`: PASS
- `check-risk-policy.py --json`: PASS (`orders is empty` warning)
