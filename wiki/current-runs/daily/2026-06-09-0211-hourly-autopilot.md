# 2026-06-09-0211-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0211` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 open order 0건으로 종료됐고 core preflight hard gate도 `pass`였다. 이번 cycle은 scheduler evidence만으로 Alpaca core coverage를 확정할 수 있어 추가 Alpaca read-only MCP 호출은 생략했다. same-day fills와 포지션/계좌 상태도 scheduler-owned core preflight row로 그대로 재확인했다.

이번 run은 sell/trim을 먼저 평가했다. `RGTI`는 speculative sleeve trim trigger가 계속 active지만 2251 cycle same-day filled trim 때문에 duplicate sell gate에 막혔다. `AVGO`는 scheduler preflight quote가 `394.89/398.50`로 벌어져 spread `0.9100%` hard gate도 넘었고, same-day after-hours sell 2건이 남아 duplicate discipline이 먼저 추가 trim을 막았다. `SO`는 quote/spread는 정상이지만 decision-grade metric gap이 남았다. buy fallback에서는 `review_backlog_pending_1d_count=13`이 YAML stop threshold `12`를 초과해 신규 buy slot이 먼저 차단됐고, 보조 후보 `SPY/QQQ`는 1주 ask가 validation floor per-order cap 약 `500.49 USD`를 넘었으며 `NOK`는 validation_lifecycle add-block이 유지됐다. 따라서 이번 cycle도 exact blocker를 남긴 채 `orders: []`로 종료한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler Alpaca clock `2026-06-08T13:11:12.170962402-04:00`, regular market open |
| Stale order lifecycle | PASS | `0211` stale cleanup artifact 기준 open order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, quotes/account/positions/open-orders/recent-activities 모두 충족 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha one-call throttle `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK | `pending_1d_count=13`으로 YAML `stop_new_buys_at_pending_1d=12` 초과. sell/trim에는 비적용 |
| Quote/spread | MIXED | `RGTI/SO/SPY/QQQ/NOK`는 preflight fresh quote 확보와 spread cap 통과, `AVGO`는 spread `0.9100%`로 hard gate 실패 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | BLOCK | sell 3종은 duplicate/spread/metric gate 미통과, buy fallback은 backlog/notional cap/lifecycle blocker |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | watch_same_day_sell | 0.0449% | speculative loss trigger는 유지되지만 `hourly-20260608-2251-sell-rgti` filled가 same-day all-orders에 남아 추가 trim 불가 |
| AVGO | blocked_duplicate_and_spread | 0.9100% | warning-band trim rationale는 유지되지만 same-day after-hours sell 2건 때문에 duplicate discipline이 먼저 작동했고 현재 spread도 cap 초과 |
| SO | watch_metric_gap | 0.0219% | weak-to-neutral review 누적은 있으나 trim replacement margin이 비어 있음 |
| SPY | blocked_review_backlog_and_floor_cap | 0.0041% | 신규 buy slot은 backlog throttle로 차단됐고 1주 ask `740.46 USD`도 validation floor per-order cap을 초과 |
| QQQ | blocked_review_backlog_and_floor_cap | 0.0042% | 신규 buy slot은 backlog throttle로 차단됐고 1주 ask `717.27 USD`도 validation floor per-order cap을 초과 |
| NOK | blocked_review_backlog_and_lifecycle | 0.0681% | backlog throttle가 먼저 걸리고 `review-due-index`의 add-block도 유지됨 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | same_day_duplicate_symbol_side | 2251 cycle trim 30주 filled가 same-day all-orders에 남아 0211 cycle 추가 trim 불가 |
| AVGO | watch | same_day_duplicate_symbol_side | scheduler preflight spread는 `0.9100%`로 cap을 넘겼고 same-day after-hours sell 2건이 duplicate discipline을 유지 |
| SO | watch | decision_grade_metric_gap | quote/spread는 정상이나 trim justification용 expected-excess/replacement margin 공백 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 주문 후보가 최종 hard gate를 통과하지 못해 작성/호출 대상이 없었다. buy path는 `review_backlog_throttle`, `validation_floor_per_order_cap`, `validation_lifecycle_blocked_add`에 막혔고 sell path는 `same_day_duplicate_symbol_side`, `spread_within_policy`, `decision_grade_metric_gap`에 막혔다.
- Post-trade reconciliation: submit attempt는 없었지만 scheduler preflight recent-activities 기준 same-day filled orders 4건(`AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건)을 재확인했다. positions는 `32`, account snapshot은 portfolio value `100098.61 USD`, cash `31774.85 USD`, buying power `301899.01 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha one-call throttle `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | 주문 0건, 현재 포지션 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-09-0211-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-09-0211-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-09-0211-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-09-0211-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-09-0211-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-09-0211-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-09-0211-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-09-0211-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy review backlog count다. 이번 run에서는 `13`으로 YAML stop threshold `12`를 넘어 신규 buy를 막았지만, risk-reducing sell에는 적용하지 않았다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 benchmark fallback 매수는 막는다.
- `alpha-vantage` one-call throttle: scheduler research preflight가 이번 시간대 추가 Alpha call을 의도적으로 생략한 `provider_error` row를 남겼고, 나머지 4개 research provider pass로 strict MCP gate는 유지됐다.
