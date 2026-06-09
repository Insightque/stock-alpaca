# 2026-06-10-0451-hourly-autopilot

## 요약

`0451` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/open orders/same-day fills/positions/asset/quotes를 다시 확인해 `V` 1주 payments diversifier validation buy를 draft order로 준비했다. 다만 validator 수정 후 최종 submit 경계에서 Alpaca live clock을 다시 조회했을 때 `2026-06-09T16:04:43.735524355-04:00`로 미국 정규장이 이미 종료돼 `first_blocking_gate=market_closed`가 발생했다.

sell-first 재평가에서는 `AVGO`와 `RGTI`가 same-day sell duplicate로, `SO`는 live spread는 정상화됐지만 trim decision-grade metric gap으로 막혀 executable risk-reducing sell이 남지 않았다. buy fallback에서는 `XOM/FCX/COP/SLB/WMT/PFE/BAC/AMZN/JNJ` same-day buy duplicate, `QQQ/SPY` validation floor per-order cap, `NVDA` same-cluster warning-band add block, `UNH` spread cap 초과, `AAPL` 최근 review 약세가 남았고, closed-market hard gate 때문에 최종 submit은 수행하지 않았다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler-owned preflight와 repo policy 기준 paper mode 유지 |
| Market clock | FAIL at submit boundary | live Alpaca clock `2026-06-09T16:04:43.735524355-04:00`, regular market closed |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders 0건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `empty_response`는 nonblocking |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Review backlog throttle | PASS | `pending_1d_count=0`, `pending_5d_count=13`, `pending_20d_count=1`; 신규 buy slot 차단 없음 |
| Quote/spread | PASS for V | V live quote `325.08/325.11`, spread `0.0092%`, quote age 약 `0.01`분 |
| Risk plan | PASS | no-order blocked plan으로 validator 통과 |
| Final submit path | FAIL | market_closed hard gate로 submit 중단 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_duplicate_sell | 2.6286% | trim rationale는 유지되지만 same-day sell fill 2주가 남아 duplicate gate 차단 |
| RGTI | blocked_duplicate_sell | 0.0510% | speculative loss-control trigger는 유지되지만 same-day sell fill 22주가 남아 duplicate gate 차단 |
| SO | blocked_metric_gap | 0.0215% | spread는 정상화됐지만 trim decision-grade replacement margin 공백이 남음 |
| V | blocked_market_closed | 0.0092% | research preflight shortlist 포함, same-day duplicate 없음, but final live clock closed |
| XOM | blocked_same_day_duplicate | 0.0403% | 직전 `0431` cycle same-day buy fill이 있어 duplicate gate 차단 |
| QQQ | blocked_floor_cap | 0.0141% | 1주 ask `706.97 USD`가 validation floor per-order cap 초과 |
| SPY | blocked_floor_cap | 0.0041% | 1주 ask `736.73 USD`가 validation floor per-order cap 초과 |
| NVDA | blocked_same_cluster_add | 0.0193% | ai_semiconductor_complex warning-band/add block 유지 |
| UNH | blocked_spread | 1.7776% | live two-sided spread가 policy cap 초과 |
| AAPL | blocked_weak_review | 0.0103% | latest 1D/5D review 약세로 floor-size fallback 우선순위에서 밀림 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | same-day regular-session trim fill 2주가 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | same-day regular-session trim fill 22주가 남아 추가 trim 불가 |
| SO | watch | sell_metric_gap | spread는 정상화됐지만 trim decision-grade metric gap이 남음 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-09T16:04:43.735524355-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-10-0451-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; V quote freshness 약 `0.01`분; spread `0.0092%`; order shape `buy 1 share / limit 325.11 / day / stock / regular session`; duplicate/open-order check `PASS`; final blocker `market_closed`; source refs는 `0451` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/ticker artifacts다.

- `place_stock_order`는 호출하지 않았다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | pre_mcp_shortlist 10개로 조정 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` only |
| `check-risk-policy.py --json` | PASS | no-order blocked plan, staged deployment warning only |

## 제출 후 정산

- no-submit run이라 신규 주문/체결은 없다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- latest reconciled account/positions state는 scheduler-owned `0451` core preflight snapshot을 유지했다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0451-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0451-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0451-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0451-hourly-autopilot-post-trade.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0451-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `0`이라 신규 buy throttle은 열려 있었지만 market_closed가 더 먼저 막았다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 fallback 매수는 막는다.
- `same_day_duplicate_symbol_side`: 같은 미국 장 세션에서 이미 같은 symbol/side fill이 있으면 중복 관측을 줄이기 위해 추가 주문을 차단하는 gate다.
