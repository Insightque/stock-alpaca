# 2026-06-11-0251-hourly-autopilot

## 요약

`0251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건으로 종료됐고, Alpaca core preflight hard gate도 `pass`였다. 이번 cycle은 `0231`에서 열려 있던 `NKE` buy가 `2026-06-10T17:44:44.080648Z`에 `43.98 USD`로 체결됐음을 post-trade reconciliation으로 먼저 반영한 뒤, sell-first와 buy fallback을 다시 평가했다.

sell-first에서는 `AVGO`가 live spread `2.1053%`로 trim hard gate를 통과하지 못했고 same-day sell duplicate도 남았으며, `RGTI`는 same-day filled trim duplicate, `SO`는 trim decision-grade metric gap으로 막혔다. buy fallback에서는 `NKE/NEE/FCX/AMZN/SLB/COP/JNJ/XOM/PFE/BAC/WMT/AAPL`이 same-day buy duplicate, `SPY/QQQ`가 validation floor per-order cap, `NOK`가 validation_lifecycle add-block, `INTC`가 recent weak exit review 때문에 `candidate_floor.require_no_thesis_break`를 통과하지 못했다. 따라서 이번 cycle은 exact blocker를 남긴 채 `orders: []` no-submit 예외 run으로 종료한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler artifact와 workflow policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler Alpaca clock `2026-06-10T13:51:10.075000493-04:00`, regular market open |
| Stale order lifecycle | PASS | `0251` stale cleanup artifact와 core preflight open-orders row 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass, account/positions/open-orders/recent-activities/quotes 모두 usable |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha one-call throttle `provider_error` only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`라 신규 buy 슬롯은 `1`개로 축소되지만 stop threshold `12` 미만 |
| Quote/spread | MIXED | `RGTI/SO/NKE/SPY/QQQ/NOK/INTC`는 spread cap 이내, `AVGO`는 `2.1053%`로 fail |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 현재 포지션 포함, orders `0` 허용 |
| Final submit path | BLOCK | sell 3종은 spread/duplicate/metric gate 미통과, buy fallback은 duplicate/cap/add-block/no-thesis-break blocker |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_spread_and_duplicate | 2.1053% | ai_semiconductor warning-band trim rationale는 유지되지만 spread hard gate fail과 same-day sell duplicate가 겹친다 |
| RGTI | blocked_duplicate_same_day | 0.0995% | speculative loss-control trim trigger는 active지만 `2311` cycle same-day filled trim이 남는다 |
| SO | blocked_metric_gap | 0.2969% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| NKE | blocked_duplicate_same_day | 0.0227% | `17:44:44Z` fill로 same-day duplicate buy gate가 재매수를 막는다 |
| SPY | blocked_floor_cap | 0.0055% | 1주 ask `729.99 USD`가 validation floor per-order cap 약 `488.39 USD`를 초과 |
| QQQ | blocked_floor_cap | 0.0143% | 1주 ask `699.01 USD`가 validation floor per-order cap 약 `488.39 USD`를 초과 |
| NOK | blocked_add_block | 0.0744% | `review-due-index`의 validation_lifecycle add-block 유지 |
| INTC | blocked_no_thesis_break | 0.0469% | 최근 1D/5D review `약함`과 full-exit 회고가 남아 no-thesis-break floor를 통과하지 못함 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_within_policy | spread fail이 첫 blocker이고 same-day sell duplicate도 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 주문 후보가 최종 hard gate를 통과하지 못해 작성/호출 대상이 없었다. sell path는 `spread_within_policy`, `duplicate_symbol_side_same_day`, `sell_metric_gap`에 막혔고 buy path는 `duplicate_symbol_side_same_day`, `validation_floor_per_order_cap`, `validation_lifecycle_blocked_add`, `candidate_floor.require_no_thesis_break`에 막혔다.
- Post-trade reconciliation: submit attempt는 없었지만 `hourly-20260611-0231-buy-nke`가 `43.98 USD`로 체결된 것을 확인했고, open orders는 `0`, positions는 `33`, account snapshot은 portfolio value `97,677.60 USD`, cash `31,263.75 USD`, buying power `295,902.61 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha one-call throttle `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | 주문 0건, 현재 포지션 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0251-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0251-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0251-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소되지만 stop threshold에는 도달하지 않았다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 benchmark fallback 매수는 막는다.
- `candidate_floor.require_no_thesis_break`: floor-size learning buy라도 최근 review와 exit evidence가 thesis break에 가깝다면 재진입을 허용하지 않는 최소 조건이다.
