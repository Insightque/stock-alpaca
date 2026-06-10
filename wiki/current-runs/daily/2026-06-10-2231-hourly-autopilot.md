# 2026-06-10-2231-hourly-autopilot

## 요약

`2231` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/positions/same-day fills/quotes를 짧게 재확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었고, review backlog는 `pending_1d_count=9`라 신규 buy 슬롯만 `1`개로 축소됐지만 sell/trim 진단은 독립적으로 유지됐다.

sell-first 재평가에서는 `RGTI`가 speculative loss-control trim trigger를 유지했지만 live quote `19.70/19.80`의 spread `0.5063%`가 policy cap `0.50%`를 소폭 넘었고, `AVGO`와 `SO`도 각각 `3.9322%`, `5.8278%` spread로 risk-reducing sell hard gate를 통과하지 못했다. buy fallback에서는 `SPY/QQQ`가 validation floor per-order cap 초과, `NOK`가 validation_lifecycle add-block, `BAC/PFE/PLTR/NKE`가 lower-rank fallback으로 남아 `WMT` 1주 floor-size defensive add가 가장 보수적인 learning order가 됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` paper mode와 scheduler artifact 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-10T09:35:58.973712921-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `empty_response`는 nonblocking |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`로 buy 슬롯 `1`개로 축소, sell/trim은 비차단 |
| Quote/spread | PASS for WMT | WMT live quote `118.75/118.79`, spread `0.0337%`, quote age 약 `0.01`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | blocked_spread | 0.5063% | speculative loss-control trim trigger는 active지만 spread가 cap을 소폭 초과 |
| AVGO | blocked_spread | 3.9322% | post-earnings de-risk trim rationale는 유지되지만 spread hard gate fail |
| SO | blocked_metric_gap | 5.8278% | spread cap 초과와 trim decision-grade metric gap이 동시 잔존 |
| WMT | selected_validation_buy | 0.0337% | existing consumer defensive holding, no same-day duplicate, one-slot throttle 아래 최우선 floor-size buy |
| BAC | watch_lower_rank | 0.0551% | eligible지만 현재 cycle의 defensive learning order로는 WMT보다 우선순위가 낮음 |
| PFE | watch_lower_rank | 0.0388% | eligible지만 recent review 품질이 WMT보다 약함 |
| PLTR | watch_lower_rank | 0.0849% | eligible지만 one-slot throttle 환경에서 defensive 분산 기여가 낮음 |
| NOK | blocked_add | 0.0731% | `review-due-index` validation_lifecycle add-block 유지 |
| SPY | blocked_floor_cap | 0.1214% | 1주 ask `733.32 USD`가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0541% | 1주 ask `702.38 USD`가 validation floor per-order cap 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | spread_within_policy | spread `0.5063%`가 cap `0.50%`를 소폭 초과 |
| AVGO | watch | spread_within_policy | live spread `3.9322%`로 trim hard gate fail |
| SO | watch | sell_metric_gap | spread cap 초과와 decision-grade replacement metric gap 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T09:35:58.973712921-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-10-2231-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; WMT quote freshness 약 `0.01`분; spread `0.0337%`; order shape `buy 1 share / limit 118.79 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `2231` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/ticker artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| WMT | buy | 1 | 118.79 | `8b189213-3d70-40a4-8957-2fcdd8b454fd` | `filled_avg_price=118.49 USD` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` only |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |


## 제출 후 정산

- `get_order_by_id`와 `get_orders(status=all, symbols=WMT)` 기준 `WMT` 주문은 `filled`다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `WMT`는 `7주 -> 8주`, `avg_entry_price=118.20625`, `qty_available=8`로 증가했다.
- `get_account_info` snapshot은 portfolio value `98,755.50 USD`, cash `31,250.14 USD`, buying power `298,482.29 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-10)`는 `WMT` buy 1 fill과 earlier same-day `AAPL` buy 2 fills를 반환했다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-2231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-2231-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-2231-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-2231-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-10-2231-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소되지만 sell/trim 진단은 독립적으로 유지된다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 fallback 매수는 막는다.
- `validation_lifecycle add-block`: due review 또는 장기 add-block이 남은 종목의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에 적용됐다.
