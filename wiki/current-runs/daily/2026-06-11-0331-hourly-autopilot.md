# 2026-06-11-0331-hourly-autopilot

## 요약

`0331` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건으로 종료됐고, Alpaca core preflight hard gate도 `pass`였다. 이번 cycle은 required core/research row가 모두 fresh/pass라 추가 Alpaca read-only MCP 호출 없이 scheduler evidence로 clock/account/positions/open-orders/recent-fills/quotes 상태를 확정했다.

sell-first 재평가에서는 `AVGO`가 ai_semiconductor warning-band trim rationale를 유지했지만 live spread `1.9201%`로 policy cap `0.50%`를 초과해 hard gate에서 탈락했고, `RGTI`는 `2026-06-10 ET` same-day sell duplicate, `SO`는 trim decision-grade metric gap이 이어졌다. buy fallback에서는 `FCX/WMT/SLB/NKE/NEE/COP/AMZN`이 same-day buy duplicate, `XOM`이 same-day duplicate에 더해 live spread `0.5784%`로 cap 초과, `GOOGL`이 recent weak review에 따른 `candidate_floor.require_no_thesis_break`, `NVDA`가 ai_semiconductor_complex warning-band add block, `SPY/QQQ`가 validation floor per-order cap에 걸렸다. 따라서 이번 cycle은 exact blocker를 남긴 채 `orders: []` no-submit 예외 run으로 종료한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler artifact와 workflow policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler Alpaca clock `2026-06-10T14:31:09.959288663-04:00`, regular market open |
| Stale order lifecycle | PASS | `0331` stale cleanup artifact와 core preflight open-orders row 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass, account/positions/open-orders/recent-activities/quotes 모두 usable |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `empty_response` gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`라 신규 buy 슬롯은 `1`개로 축소되지만 stop threshold `12` 미만 |
| Quote/spread | MIXED PASS | `RGTI/SO/FCX/WMT/SLB/NKE/NEE/COP/AMZN/GOOGL/NVDA/SPY/QQQ`는 cap 이내, `AVGO/XOM`은 spread hard gate fail |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 현재 포지션 포함, orders `0` 허용 |
| Final submit path | BLOCK | sell path는 spread/duplicate/metric gap, buy path는 same-day duplicate/spread fail/weak review/same-cluster add-block/per-order cap |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_spread_fail | 1.9201% | ai_semiconductor warning-band trim rationale는 유지되지만 live spread가 policy cap을 넘었다 |
| RGTI | blocked_duplicate_same_day | 0.0502% | speculative loss-control trim trigger는 active지만 same-day sell fill이 남는다 |
| SO | blocked_metric_gap | 0.0212% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| FCX | blocked_duplicate_same_day | 0.0318% | same-day regular-session buy fill이 남아 재매수 duplicate gate 차단 |
| WMT | blocked_duplicate_same_day | 0.0083% | same-day buy duplicate |
| SLB | blocked_duplicate_same_day | 0.0179% | same-day buy duplicate |
| XOM | blocked_duplicate_same_day_and_spread_fail | 0.5784% | same-day buy duplicate에 더해 live spread가 cap을 초과한다 |
| NKE | blocked_duplicate_same_day | 0.0227% | `0231` buy fill이 same-day duplicate gate를 유지한다 |
| NEE | blocked_duplicate_same_day | 0.0118% | same-day buy duplicate |
| COP | blocked_duplicate_same_day | 0.0250% | same-day buy duplicate |
| AMZN | blocked_duplicate_same_day | 0.0209% | same-day buy duplicate |
| GOOGL | blocked_weak_review | 0.0112% | quote/spread는 양호하지만 recent review 약세와 replacement rank 약화로 floor-size fallback에서 탈락 |
| NVDA | blocked_same_cluster_add_block | 0.0544% | quote/spread는 양호하지만 ai_semiconductor_complex warning-band add block 유지 |
| SPY | blocked_floor_cap | 0.0069% | 1주 ask `729.24 USD`가 validation floor per-order cap 약 `487.89 USD` 초과 |
| QQQ | blocked_floor_cap | 0.0272% | 1주 ask `697.84 USD`가 validation floor per-order cap 약 `487.89 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_within_policy | warning-band trim rationale는 유지되지만 spread `1.9201%`가 hard cap 초과 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 주문 후보가 최종 hard gate를 통과하지 못해 작성/호출 대상이 없었다. sell path는 `spread_within_policy`, `duplicate_symbol_side_same_day`, `sell_metric_gap`에 막혔고 buy path는 `duplicate_symbol_side_same_day`, `spread_within_policy`, `candidate_floor.require_no_thesis_break`, `same_cluster_warning_add_block`, `validation_floor_per_order_cap`에 막혔다.
- Post-trade reconciliation: submit attempt는 없었고 scheduler-owned `0331` Alpaca core preflight 기준 account `ACTIVE`, positions `33`, open orders `0`, cash `31,263.75 USD`, portfolio value `97,578.98 USD`, long market value `66,315.23 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | 주문 0건, 현재 포지션 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0331-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0331-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0331-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소되지만 stop threshold에는 도달하지 않았다.
- `same_cluster_warning_add_block`: `ai_semiconductor_complex`가 warning band 위에 있어 추가 buy는 distinct-cluster 또는 더 강한 replacement margin이 필요하다는 뜻이다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 benchmark fallback 매수는 막는다.
