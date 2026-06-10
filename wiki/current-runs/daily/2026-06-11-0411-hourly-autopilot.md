# 2026-06-11-0411-hourly-autopilot

## 요약

`0411` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건으로 종료됐고, Alpaca core preflight hard gate도 `pass`였다. 이번 cycle도 required core row가 모두 fresh/pass라 추가 Alpaca read-only MCP 호출 없이 scheduler evidence로 clock/account/positions/open-orders/recent-fills/quotes 상태를 확정했다.

sell-first 재평가에서는 `AVGO`와 `RGTI` 모두 live spread는 policy cap 이내로 정상화됐지만 `2026-06-10 ET` same-day sell fill이 남아 duplicate sell discipline에 막혔고, `SO`는 trim decision-grade metric gap이 이어졌다. buy fallback에서는 `FCX/WMT/SLB/NKE/NEE/COP/AMZN/XOM`이 same-day buy duplicate, `MCD`가 live spread `1.2599%`로 policy cap `0.50%`를 크게 넘는 동시에 유지 중인 ticker thesis evidence도 없어 hard gate를 통과하지 못했고, `GOOGL`이 recent weak review에 따른 `candidate_floor.require_no_thesis_break`, `NVDA`가 ai_semiconductor_complex warning-band add block, `SPY/QQQ`가 validation floor per-order cap에 걸렸다. 따라서 이번 cycle은 exact blocker를 남긴 채 `orders: []` no-submit 예외 run으로 종료한다.

연구 MCP는 tiered pass를 유지했다. `SEC EDGAR/FRED/Firecrawl/Yahoo Finance`는 pass였고, `Alpha Vantage`는 one-call-per-hour throttle 때문에 `provider_error`로 기록됐지만 최소 confirmation 수는 충족했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler artifact와 workflow policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler Alpaca clock `2026-06-10T15:11:11.51334323-04:00`, regular market open |
| Stale order lifecycle | PASS | `0411` stale cleanup artifact와 core preflight open-orders row 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass, account/positions/open-orders/recent-activities/quotes 모두 usable |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `provider_error` throttle gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`라 신규 buy 슬롯은 `1`개로 축소되지만 stop threshold `12` 미만 |
| Quote/spread | MIXED PASS | `AVGO/RGTI/SO/FCX/WMT/SLB/NKE/NEE/COP/AMZN/XOM/GOOGL/NVDA/SPY/QQQ`는 cap 이내, `MCD`는 spread hard gate fail |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 현재 포지션 포함, orders `0` 허용 |
| Final submit path | BLOCK | sell path는 duplicate/metric gap, buy path는 same-day duplicate/spread fail/thesis evidence 부족/weak review/same-cluster add-block/per-order cap |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_duplicate_same_day | 0.1206% | ai_semiconductor warning-band trim rationale는 유지되지만 same-day sell duplicate가 남는다 |
| RGTI | blocked_duplicate_same_day | 0.0508% | speculative loss-control trim trigger는 active지만 same-day sell fill이 이미 있다 |
| SO | blocked_metric_gap | 0.0212% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| FCX | blocked_duplicate_same_day | 0.0320% | same-day regular-session buy fill이 남아 재매수 duplicate gate 차단 |
| WMT | blocked_duplicate_same_day | 0.0083% | same-day buy duplicate |
| SLB | blocked_duplicate_same_day | 0.0179% | same-day buy duplicate |
| XOM | blocked_duplicate_same_day | 0.0727% | live spread는 정상 범위지만 same-day buy duplicate가 남는다 |
| NKE | blocked_duplicate_same_day | 0.0227% | `0231` buy fill이 same-day duplicate gate를 유지한다 |
| NEE | blocked_duplicate_same_day | 0.0117% | same-day buy duplicate |
| COP | blocked_duplicate_same_day | 0.0249% | same-day buy duplicate |
| AMZN | blocked_duplicate_same_day | 0.0210% | same-day buy duplicate |
| MCD | blocked_spread_fail_and_thesis_evidence_missing | 1.2599% | live spread가 hard cap을 크게 넘고 유지 중인 ticker thesis page도 없다 |
| GOOGL | blocked_weak_review | 0.1713% | quote/spread는 양호하지만 recent weak review와 replacement rank 약화로 floor-size fallback에서 탈락 |
| NVDA | blocked_same_cluster_add_block | 0.2142% | quote/spread는 양호하지만 ai_semiconductor_complex warning-band add block 유지 |
| SPY | blocked_floor_cap | 0.0041% | 1주 ask `727.49 USD`가 validation floor per-order cap 약 `486.31 USD` 초과 |
| QQQ | blocked_floor_cap | 0.0201% | 1주 ask `695.95 USD`가 validation floor per-order cap 약 `486.31 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | spread는 정상화됐지만 `2026-06-10 ET` same-day trim fill이 남는다 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 주문 후보가 최종 hard gate를 통과하지 못해 작성/호출 대상이 없었다. sell path는 `duplicate_symbol_side_same_day`, `sell_metric_gap`에 막혔고 buy path는 `duplicate_symbol_side_same_day`, `spread_within_policy`, `thesis_evidence_missing`, `candidate_floor.require_no_thesis_break`, `same_cluster_warning_add_block`, `validation_floor_per_order_cap`에 막혔다.
- Post-trade reconciliation: submit attempt는 없었고 scheduler-owned `0411` Alpaca core preflight 기준 account `ACTIVE`, positions `33`, open orders `0`, cash `31,263.75 USD`, portfolio value `97,261.58 USD`, long market value `65,997.83 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 6개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle `provider_error` only |
| `check-risk-policy.py --json` | PASS | 주문 0건, 현재 포지션 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0411-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0411-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0411-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0411-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0411-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소되지만 stop threshold에는 도달하지 않았다.
- `thesis_evidence_missing`: quote/spread와 research preflight가 양호해도 유지 중인 ticker thesis page가 없으면 신규 buy를 submit-mode 후보로 승격하지 않는다는 뜻이다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 benchmark fallback 매수는 막는다.
