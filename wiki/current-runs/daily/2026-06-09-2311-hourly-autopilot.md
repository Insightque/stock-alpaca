# 2026-06-09-2311-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `2311` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 stale candidate 0건으로 종료됐지만, core preflight와 open-order cleanup 결과에는 직전 `2251` cycle에서 제출한 `AVGO` trim sell 2주가 여전히 `status=new` open order로 남아 있었다. 이번 cycle은 sell/trim을 먼저 다시 평가했지만 `AVGO`는 unresolved open-order lifecycle, `RGTI`는 same-day duplicate symbol/side, `SO`는 decision-grade metric gap으로 모두 live submit까지 승격되지 못했다.

buy fallback도 검토했다. `BAC`는 다른 cluster의 floor-size diversifier 후보로는 남아 있었지만 `paper_validation_execution.validation_order_sizing.open_order_policy.require_lifecycle_gate_pass=true`와 기존 scheduler-owned learning order 미해결 상태 때문에 이번 cycle에서 두 번째 validation order를 겹쳐 쌓지 않았다. benchmark fallback `SPY`와 `QQQ`는 1주 ask가 validation floor per-order cap을 초과했다. 따라서 이번 cycle의 최종 blocker는 `risk_open_order_lifecycle`이며, 새 주문은 제출하지 않고 report/manifest/order-plan/post-trade reconciliation만 갱신한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler Alpaca clock `2026-06-09T10:11:10.039371794-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-09-2311-hourly-autopilot-stale-order-cleanup.json`에서 stale candidate 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, open orders/positions/account/quotes 모두 존재 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `provider_error` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for diagnostics | `AVGO/RGTI/SO/BAC/SPY/QQQ` 모두 20분 이내 fresh quote 확보 |
| Risk validator | PASS | `orders: []` + current positions/open order 포함 상태로 통과 |
| Open-order lifecycle | BLOCK | `hourly-20260609-2251-sell-avgo` unresolved open order 1건이 남아 있어 이번 cycle 추가 validation submit 차단 |
| Final submit path | BLOCK | `AVGO` lifecycle, `RGTI` same-day duplicate, `SO` metric gap, `SPY/QQQ` floor-cap |

## 후보와 판단

| Symbol | 판단 | Gate | 이유 |
| --- | --- | --- | --- |
| AVGO | watch_open_order | `risk_open_order_lifecycle` | 2251 cycle trim sell 2주가 `status=new`로 남아 있어 같은 symbol/side add-on submit 금지 |
| RGTI | watch_duplicate | `duplicate_symbol_side_same_day` | 2026-06-09 ET same-day sell fill 22주가 이미 있음 |
| SO | watch_metric_gap | `decision_grade_metric_gap` | spread는 정상이나 trim justification용 replacement margin 공백 지속 |
| BAC | watch_buy_deferred | `risk_open_order_lifecycle` | 다른 cluster fallback buy 후보지만 unresolved hourly open order 위에 새 learning order를 추가로 쌓지 않음 |
| SPY | watch_notional_cap | `validation_floor_per_order_cap` | 1주 ask `743.10 USD`가 floor cap 약 `501.47 USD` 초과 |
| QQQ | watch_notional_cap | `validation_floor_per_order_cap` | 1주 ask `718.74 USD`가 floor cap 약 `501.47 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | risk_open_order_lifecycle | 기존 trim order fill/cancel 결과가 먼저 필요 |
| RGTI | watch | duplicate_symbol_side_same_day | earlier same-day sell fill 때문에 추가 trim 불가 |
| SO | watch | decision_grade_metric_gap | decision-grade metric 공백 지속 |

## 주문/체결 및 reconciliation

- Planned orders: 0
- Submitted orders: 0
- Existing open order carried into this cycle: `AVGO` sell 2 @ `403.00 USD`, `client_order_id=hourly-20260609-2251-sell-avgo`, `status=new`
- Post-trade reconciliation: 이번 cycle은 submit attempt는 없었지만 open order가 존재해 reconciliation을 수행했다. scheduler-owned core preflight 기준 open orders `1`, positions `32`, same-day fill activity는 `RGTI` sell partial/fill 2건이며 신규 `AVGO` fill은 없다. `AVGO` 보유수량은 `10주`, `qty_available=8주`로 기존 open sell 2주가 계속 예약돼 있다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha gap only |
| `check-risk-policy.py --json` | PASS | 주문 0건, current positions/open order 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-09-2311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-09-2311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-09-2311-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-09-2311-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-09-2311-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-09-2311-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-09-2311-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-09-2311-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `risk_open_order_lifecycle`: stale order failure가 아니어도, scheduler-owned validation order가 unresolved open 상태로 남아 있으면 이번 cycle의 추가 validation submit을 막는 lifecycle gate로 사용했다.
- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 benchmark fallback 매수는 허용되지 않는다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler-owned one-call throttle 때문에 `provider_error` gap으로만 기록됐고, 나머지 4개 research confirmation이 유지돼 strict MCP gate는 통과했다.
