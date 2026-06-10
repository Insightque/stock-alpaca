# 2026-06-10-2251-hourly-autopilot

## 요약

`2251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/positions/same-day fills/quotes를 짧게 재확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었고, review backlog는 `pending_1d_count=9`라 신규 buy 슬롯만 `1`개로 축소됐지만 risk-reducing sell/trim은 독립적으로 유지됐다.

sell-first 재평가에서는 `AVGO`와 `RGTI`가 모두 spread hard gate를 통과했지만, `AVGO`가 ai_semiconductor warning band, post-earnings de-risking rationale, 더 큰 negative expected-excess, 더 높은 replacement margin을 동시에 보여 우선 trim 후보로 승격됐다. 따라서 buy fallback으로 가지 않고 `AVGO` 2주 trim @ `373.21 USD`를 direct Alpaca MCP로 제출했고, immediate reconciliation 기준 `filled_avg_price=373.25 USD`로 즉시 전량 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` paper mode와 scheduler artifact 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-10T09:53:20.05800006-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `provider_error` throttle gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`로 buy 슬롯 `1`개로 축소, sell/trim은 비차단 |
| Quote/spread | PASS for AVGO | AVGO live quote `373.21/374.78`, spread `0.4191%`, quote age 약 `0.3`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | selected_trim | 0.4191% | ai_semiconductor warning-band / post-earnings de-risking rationale active, 25% trim executable |
| RGTI | watch_lower_rank | 0.0971% | speculative loss-control trim gate는 열렸지만 AVGO보다 target-band deterioration과 replacement margin이 약함 |
| SO | blocked_metric_gap | 0.0751% | spread 정상화 후에도 trim decision-grade metric gap 지속 |
| BAC | watch_fallback | 0.0182% | eligible buy fallback이지만 eligible AVGO trim이 우선 |
| PFE | watch_fallback | 0.0389% | eligible buy fallback이지만 eligible AVGO trim이 우선 |
| PLTR | blocked_spread | 1.6283% | spread cap 초과 |
| NOK | blocked_add | 0.0723% | `review-due-index` validation_lifecycle add-block 유지 |
| SPY | blocked_floor_cap | 0.0122% | 1주 ask `735.35 USD`가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0156% | 1주 ask `705.77 USD`가 validation floor per-order cap 초과 |
| WMT | blocked_duplicate_same_day | 0.0594% | same-day buy fill `hourly-20260610-2231-buy-wmt` 이미 존재 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | trim | executable | target-band de-risking과 post-earnings weakness가 유지되고 spread가 정상화돼 2주 trim 실행 |
| RGTI | watch | lower_ranked_than_selected_trim | sell gate는 통과했지만 이번 cycle의 우선 trim은 AVGO |
| SO | watch | sell_metric_gap | spread 정상화 후에도 decision-grade replacement metric gap 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T09:53:20.05800006-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-10-2251-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; AVGO quote freshness 약 `0.3`분; spread `0.4191%`; order shape `sell 2 shares / limit 373.21 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `2251` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/ticker artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| AVGO | sell | 2 | 373.21 | `155edaa1-e527-4c67-b43a-07e2cea9ad40` | `filled_avg_price=373.25 USD` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle gap only |
| `check-risk-policy.py --json` | PASS | AVGO trim order-plan risk gate 통과 |

## 제출 후 정산

- `get_order_by_id`와 `get_orders(status=all, symbols=AVGO)` 기준 `AVGO` 주문은 `filled`다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `AVGO`는 `8주 -> 6주`, `avg_entry_price=417.04625`, `qty_available=6`으로 감소했다.
- `get_account_info` snapshot은 portfolio value `98,683.18 USD`, cash `31,996.64 USD`, buying power `299,310.65 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-10)`는 `AVGO` partial fill 1건 + final fill 1건, `WMT` buy 1 fill, earlier same-day `AAPL` buy 2 fills를 반환했다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-2251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-2251-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-2251-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-2251-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-10-2251-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소되지만 sell/trim 진단은 독립적으로 유지된다.
- `target_band_de_risking`: target/warning band를 넘긴 동일 theme/cluster 노출이 약화 신호와 함께 나타날 때 staged trim을 허용하는 규칙이다.
- `validation_lifecycle add-block`: due review 또는 장기 add-block이 남은 종목의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에 적용됐다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 provider call을 건너뛰었고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
