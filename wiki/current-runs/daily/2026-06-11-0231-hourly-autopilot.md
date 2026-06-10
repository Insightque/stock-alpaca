# 2026-06-11-0231-hourly-autopilot

## 요약

`0231` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, Alpaca core preflight에 세부 tool row가 비어 있던 부분은 workflow 계약에 따라 live Alpaca MCP `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_account_activities(activity_types=FILL, after=2026-06-10)/get_watchlists/get_stock_latest_quote(feed=iex)/get_asset(NKE)`로 개별 재확인했다. stale cleanup과 live open-order check 모두 submit 전 `0`건이었고, sell-first 재평가에서는 `AVGO`가 spread fail과 same-day sell duplicate, `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였다.

buy fallback에서는 `NEE/FCX/AMZN/SLB/COP/JNJ/XOM/PFE/BAC/WMT/AAPL`이 same-day buy duplicate, `SPY/QQQ`가 validation floor per-order cap, `CVX`가 spread fail로 남았고, `NKE`가 research-preflight-covered consumer diversifier floor-size buy로 승격됐다. direct Alpaca MCP submit 결과 `client_order_id=hourly-20260611-0231-buy-nke`, `order_id=9b08f07e-f93e-47d6-b1d1-5d707abec8eb`가 생성됐고 immediate reconciliation 기준 상태는 `new`, `filled_qty=0` open order다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler artifact와 runtime policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-10T13:38:03.967009093-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` submit 전 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha throttle provider_error only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`라 신규 buy 슬롯은 `1`개, sell/trim은 비차단 |
| Quote/spread | PASS for NKE | NKE quote `43.98/43.99`, spread `0.0227%`, quote age `3.6`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_spread_and_duplicate | 1.4569% | trim rationale는 유지되지만 spread hard gate fail과 same-day sell duplicate가 겹친다 |
| RGTI | blocked_duplicate_same_day | 0.1005% | speculative loss-control trigger는 유지되지만 same-day sell duplicate가 남는다 |
| SO | blocked_metric_gap | 0.3175% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| NKE | selected_buy | 0.0227% | preflight-covered consumer diversifier, same-day duplicate/open-order conflict 없음 |
| AMZN | blocked_duplicate_same_day | 0.0503% | 0131 cycle buy fill이 same-day duplicate로 남는다 |
| CVX | blocked_spread | 4.9474% | live quote wide spread로 hard gate fail |
| SPY | blocked_floor_cap | 0.0055% | 1주 ask가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0230% | 1주 ask가 validation floor per-order cap 초과 |
| AAPL | blocked_duplicate_same_day | 0.0205% | same-day after-hours filled buy 2건이 남는다 |
| BAC | blocked_duplicate_same_day | 0.0182% | same-day regular-session filled buy가 남는다 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_within_policy | spread fail과 same-day sell duplicate가 함께 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T13:38:03.967009093-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-11-0231-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; NKE quote freshness `3.6`분; spread `0.0227%`; order shape `buy 1 share / limit 43.99 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0231` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/NKE artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| NKE | buy | 1 | 43.99 | `9b08f07e-f93e-47d6-b1d1-5d707abec8eb` | `status=new`, `filled_qty=0` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle gap only |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 제출 후 정산

- `place_stock_order`는 정상 반환됐고 `client_order_id=hourly-20260611-0231-buy-nke`, `order_id=9b08f07e-f93e-47d6-b1d1-5d707abec8eb`로 기록됐다.
- `get_order_by_id`와 `get_orders(status=all, symbols=NKE, after=2026-06-10T17:30:00Z)` 기준 주문은 `status=new`, `filled_qty=0`, `filled_avg_price=null` open order다.
- `get_orders(status=open)` 기준 open orders는 `NKE` 1건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `NKE`는 아직 `4주`, `avg_entry_price=45.5075`, `qty_available=4`로 unchanged다.
- `get_account_info` snapshot은 portfolio value `97,407.42 USD`, cash `31,307.73 USD`, buying power `295,239.29 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-10T17:30:00Z)`는 새 fill activity를 반환하지 않았다. 이 주문은 다음 cycle stale cleanup/lifecycle check 대상으로 남긴다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0231-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0231-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0231-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-11-0231-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소된다.
- `spread_pct`: `(ask-bid)/ask*100` 기준 호가 스프레드다. regular-session hard gate는 `0.50%` 이하다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 fallback 매수는 막는다.
