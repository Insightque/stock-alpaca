# 2026-06-10-0351-hourly-autopilot

## 요약

`0351` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/same-day orders/positions/asset 상태를 다시 확인했다. stale cleanup이 `hourly-20260610-0311-buy-nvda`를 정상 취소해 open-order lifecycle은 clean해졌고, `review_backlog_pending_1d_count=0`이라 buy throttle도 열려 있었다.

sell-first 재평가에서는 `AVGO`와 `RGTI`가 same-day sell duplicate로, `SO`가 live spread `2.3170%`와 decision-grade metric gap으로 막혀 executable risk-reducing sell이 남지 않았다. buy fallback에서는 `COP/SLB/WMT/PFE/BAC/AMZN` same-day buy duplicate, `SPY/QQQ` validation floor per-order cap, `NVDA` same-cluster warning-band add block, `AAPL/NKE/NEE` 최근 review 약세, `HOOD` speculative 신규 노출이 남아 `JNJ` 1주 healthcare diversifier validation buy가 가장 보수적이면서 hard gate를 모두 통과하는 후보가 됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | live Alpaca clock `2026-06-09T14:54:53.337787802-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup이 stale NVDA buy를 취소했고 live open orders 0건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live account/orders/positions/asset 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha one-call-per-hour throttle `provider_error`는 nonblocking |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Review backlog throttle | PASS | `pending_1d_count=0`, `pending_5d_count=13`, `pending_20d_count=1`; 신규 buy slot 차단 없음 |
| Quote/spread | PASS for JNJ | JNJ live/preflight quote `237.49/237.55`, spread `0.0253%`, quote age 약 `3.8`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_duplicate_sell | 0.3202% | trim rationale는 유지되지만 same-day sell fill 2주가 남아 duplicate gate 차단 |
| RGTI | blocked_duplicate_sell | 0.0513% | speculative loss-control trigger는 유지되지만 same-day sell fill 22주가 남아 duplicate gate 차단 |
| SO | blocked_spread_and_metric_gap | 2.3170% | live spread가 policy cap 초과, trim decision-grade metric gap도 지속 |
| JNJ | selected_validation_buy | 0.0253% | healthcare diversifier, research preflight coverage 확보, duplicate/open-order conflict 없음 |
| XOM | watch_existing_energy | 0.0269% | spread와 tradability는 양호하지만 기존 energy exposure가 있어 new diversification benefit이 JNJ보다 낮음 |
| NVDA | blocked_same_cluster_add | 0.0339% | quote는 양호하지만 ai_semiconductor warning-band 아래 same-cluster add block |
| SPY | blocked_floor_cap | 0.0122% | 1주 ask `735.48 USD`가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0085% | 1주 ask `704.48 USD`가 validation floor per-order cap 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | same-day regular-session trim fill 2주가 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | same-day regular-session trim fill 22주가 남아 추가 trim 불가 |
| SO | watch | spread_within_policy | live spread `2.3170%`와 decision-grade metric gap이 동시에 남음 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-09T14:54:53.337787802-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-10-0351-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; JNJ quote freshness 약 `3.8`분; spread `0.0253%`; order shape `buy 1 share / limit 237.55 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0351` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/ticker artifacts다.

- Planned orders: 1
- Submitted orders: `JNJ` buy 1주 @ `237.55 USD` day limit
- Alpaca order id: `6f39a832-aec9-4c63-96bb-491a32b8864b`
- same client id reconciliation: `filled_avg_price=237.54 USD`, `filled_at=2026-06-09T18:59:06.623080055Z`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle `provider_error` only |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0351-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0351-hourly-autopilot-post-trade.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0351-hourly-autopilot-runtime-gate-evaluation.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-10-0351-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `0`이라 신규 buy throttle이 열려 있다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 fallback 매수는 막는다.
- `same_day_duplicate_symbol_side`: 같은 미국 장 세션에서 이미 같은 symbol/side 주문 또는 fill이 있으면 중복 관측을 줄이기 위해 추가 주문을 차단하는 gate다.

## 제출 후 정산

- `get_order_by_client_id` 기준 `JNJ` 주문은 `filled`다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개로 증가했고 `JNJ` 1주가 새로 추가됐다.
- `get_account_info` snapshot은 portfolio value `98,919.80 USD`, cash `32,163.64 USD`, buying power `300,049.79 USD`다.
