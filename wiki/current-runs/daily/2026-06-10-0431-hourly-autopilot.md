# 2026-06-10-0431-hourly-autopilot

## 요약

`0431` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/same-day fills/positions/asset/quotes를 다시 확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었고, `review_backlog_pending_1d_count=0`이라 buy throttle도 열려 있었다.

sell-first 재평가에서는 `AVGO`와 `RGTI`가 same-day sell duplicate로, `SO`가 live spread cap 초과와 trim decision-grade metric gap으로 막혀 executable risk-reducing sell이 남지 않았다. buy fallback에서는 `FCX/COP/SLB/WMT/PFE/BAC/AMZN/JNJ` same-day buy duplicate, `QQQ/SPY` validation floor per-order cap, `NVDA` same-cluster warning-band add block, `UNH` spread cap 초과, `AAPL` 최근 review 약세, `NEE` 직전 skipped-review low-priority가 남아 `XOM` 1주 energy diversifier validation buy가 가장 보수적이면서 hard gate를 모두 통과하는 후보가 됐다. direct Alpaca MCP submit 결과 `XOM` 1주는 `148.35 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | live Alpaca clock `2026-06-09T15:33:48.037828129-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders 0건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha one-call-per-hour throttle `provider_error`는 nonblocking |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Review backlog throttle | PASS | `pending_1d_count=0`, `pending_5d_count=13`, `pending_20d_count=1`; 신규 buy slot 차단 없음 |
| Quote/spread | PASS for XOM | XOM live quote `148.36/148.40`, spread `0.0270%`, quote age 약 `0.02`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_duplicate_sell | 2.7339% | trim rationale는 유지되지만 same-day sell fill 2주가 남아 duplicate gate 차단 |
| RGTI | blocked_duplicate_sell | 0.0512% | speculative loss-control trigger는 유지되지만 same-day sell fill 22주가 남아 duplicate gate 차단 |
| SO | blocked_metric_gap | 1.0298% | live spread가 policy cap 초과이고 trim decision-grade metric gap도 남음 |
| XOM | selected_validation_buy | 0.0270% | existing energy diversifier holding, research preflight coverage 확보, same-day duplicate/open-order conflict 없음 |
| QQQ | blocked_floor_cap | 0.0327% | 1주 ask `704.15 USD`가 validation floor per-order cap 초과 |
| SPY | blocked_floor_cap | 0.0204% | 1주 ask `734.27 USD`가 validation floor per-order cap 초과 |
| NVDA | blocked_same_cluster_add | 0.0146% | ai_semiconductor_complex warning-band/add block 유지 |
| UNH | blocked_spread | 0.9948% | live two-sided spread가 policy cap 초과 |
| AAPL | blocked_weak_review | 0.2961% | latest 1D/5D review 약세로 floor-size fallback 우선순위에서 밀림 |
| NEE | watch_lower_rank | 0.0118% | quote는 pass지만 직전 skipped-review가 missed-opportunity가 아니라고 확인돼 XOM 대비 우선순위가 낮음 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | same-day regular-session trim fill 2주가 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | same-day regular-session trim fill 22주가 남아 추가 trim 불가 |
| SO | watch | sell_metric_gap | spread cap 초과와 trim decision-grade metric gap이 동시에 남음 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-09T15:33:48.037828129-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-10-0431-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; XOM quote freshness 약 `0.02`분; spread `0.0270%`; order shape `buy 1 share / limit 148.40 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0431` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/ticker artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| XOM | buy | 1 | 148.40 | `5a36c3ae-d9e0-4af8-a378-b82ced709bb6` | `filled_avg_price=148.35 USD` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle `provider_error` only |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 제출 후 정산

- `get_order_by_id`와 `get_orders(status=all, symbols=XOM)` 기준 `XOM` 주문은 `filled`다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `XOM`은 `3주 -> 4주`, `avg_entry_price=149.2625`, `qty_available=4`로 증가했다.
- `get_account_info` snapshot은 portfolio value `98,676.74 USD`, cash `31,951.54 USD`, buying power `299,131.58 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-09T19:38:00Z)`는 `XOM` buy 1 fill만 반환했다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0431-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0431-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0431-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0431-hourly-autopilot-post-trade.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0431-hourly-autopilot-runtime-gate-evaluation.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-10-0431-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `0`이라 신규 buy throttle이 열려 있다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 fallback 매수는 막는다.
- `same_day_duplicate_symbol_side`: 같은 미국 장 세션에서 이미 같은 symbol/side fill이 있으면 중복 관측을 줄이기 위해 추가 주문을 차단하는 gate다.
