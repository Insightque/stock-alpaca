# 2026-06-11-0311-hourly-autopilot

## 요약

`0311` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건으로 종료됐고, Alpaca core preflight hard gate도 `pass`였다. 이번 cycle은 required core/research row가 모두 fresh/pass라 추가 Alpaca read-only MCP 호출 없이 scheduler evidence로 clock/account/positions/open-orders/recent-fills/quotes 상태를 확정했다.

sell-first 재평가에서는 `AVGO`와 `RGTI`가 모두 spread는 policy cap 이내로 정상화됐지만 `2026-06-10 ET` same-day sell fill이 남아 duplicate sell discipline에 막혔고, `SO`는 quote/spread는 통과했지만 trim decision-grade metric gap이 이어졌다. buy fallback에서는 `FCX/WMT/SLB/XOM/NKE/NEE/COP/AMZN`이 same-day buy duplicate, `GOOGL`이 recent weak review에 따른 `candidate_floor.require_no_thesis_break`, `NVDA`가 ai_semiconductor_complex warning-band add block, `SPY/QQQ`가 validation floor per-order cap에 걸렸다. 따라서 이번 cycle은 exact blocker를 남긴 채 `orders: []` no-submit 예외 run으로 종료한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler artifact와 workflow policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler Alpaca clock `2026-06-10T14:11:10.333073013-04:00`, regular market open |
| Stale order lifecycle | PASS | `0311` stale cleanup artifact와 core preflight open-orders row 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass, account/positions/open-orders/recent-activities/quotes 모두 usable |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha one-call throttle `provider_error` only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`라 신규 buy 슬롯은 `1`개로 축소되지만 stop threshold `12` 미만 |
| Quote/spread | PASS on candidate stack | `AVGO/RGTI/SO/GOOGL/NVDA`와 same-day duplicate buy stack 모두 spread cap 이내 |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 현재 포지션 포함, orders `0` 허용 |
| Final submit path | BLOCK | sell path는 duplicate/metric gap, buy path는 same-day duplicate/weak review/same-cluster add-block/per-order cap |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_duplicate_same_day | 0.3991% | ai_semiconductor warning-band trim rationale는 유지되지만 same-day sell fill이 남아 duplicate sell gate가 추가 trim을 막는다 |
| RGTI | blocked_duplicate_same_day | 0.0500% | speculative loss-control trim trigger는 active지만 same-day sell fill이 남는다 |
| SO | blocked_metric_gap | 0.0212% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| FCX | blocked_duplicate_same_day | 0.0159% | same-day regular-session buy fill이 남아 재매수 duplicate gate 차단 |
| WMT | blocked_duplicate_same_day | 0.0167% | same-day buy duplicate |
| SLB | blocked_duplicate_same_day | 0.0178% | same-day buy duplicate |
| XOM | blocked_duplicate_same_day | 0.0198% | same-day buy duplicate |
| NKE | blocked_duplicate_same_day | 0.0227% | `0231` buy가 `17:44:44Z` fill로 반영돼 same-day duplicate gate 유지 |
| NEE | blocked_duplicate_same_day | 0.0235% | same-day buy duplicate |
| COP | blocked_duplicate_same_day | 0.0249% | same-day buy duplicate |
| AMZN | blocked_duplicate_same_day | 0.0293% | same-day buy duplicate |
| GOOGL | blocked_weak_review | 0.0168% | quote/spread는 양호하지만 recent review 약세와 replacement rank 약화로 floor-size fallback에서 탈락 |
| NVDA | blocked_same_cluster_add_block | 0.0197% | quote/spread는 양호하지만 ai_semiconductor_complex warning-band add block 유지 |
| SPY | blocked_floor_cap | 0.0055% | 1주 ask `730.75 USD`가 validation floor per-order cap 약 `488.64 USD` 초과 |
| QQQ | blocked_floor_cap | 0.0372% | 1주 ask `699.77 USD`가 validation floor per-order cap 약 `488.64 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | spread는 정상 범위지만 same-day trim fill이 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 주문 후보가 최종 hard gate를 통과하지 못해 작성/호출 대상이 없었다. sell path는 `duplicate_symbol_side_same_day`, `sell_metric_gap`에 막혔고 buy path는 `duplicate_symbol_side_same_day`, `candidate_floor.require_no_thesis_break`, `same_cluster_warning_add_block`, `validation_floor_per_order_cap`에 막혔다.
- Post-trade reconciliation: submit attempt는 없었고 scheduler-owned `0311` Alpaca core preflight 기준 account `ACTIVE`, positions `33`, open orders `0`, cash `31,263.75 USD`, portfolio value `97,727.43 USD`, long market value `66,463.68 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha one-call throttle `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | 주문 0건, 현재 포지션 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0311-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0311-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0311-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소되지만 stop threshold에는 도달하지 않았다.
- `same_cluster_warning_add_block`: `ai_semiconductor_complex`가 warning band 위에 있어 추가 buy는 distinct-cluster 또는 더 강한 replacement margin이 필요하다는 뜻이다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 benchmark fallback 매수는 막는다.
