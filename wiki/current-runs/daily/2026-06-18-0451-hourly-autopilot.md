# 2026-06-18-0451-hourly-autopilot scheduled paper autopilot

## 요약

`0451` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, pre-submit 단계에서는 `SBUX`가 current-cycle research-preflight-covered 신규 consumer discretionary diversifier fallback으로 승격됐다. stale cleanup은 remaining open orders `0`, Alpaca core preflight hard gate는 `pass`, research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` positive `3` confirmations로 strict submit threshold를 충족했다. live continuity 기준 `SBUX`는 active tradable NASDAQ stock, same-day duplicate `0`, IEX quote `99.56/99.59`, spread `0.0301%`, validation floor per-order cap `약 500.64 USD` 이하 1주 notional을 모두 만족했다.

다만 actual Alpaca submit timestamp가 `2026-06-17T20:01:40.378968465Z`, 즉 `16:01:40 ET`로 regular-session close 이후였다. live clock 재확인 결과 `2026-06-17T16:02:00.785015971-04:00`, `is_open=false`가 확인돼 market-open hard gate가 최종 submit boundary에서 실패했다. 따라서 same `order_id=bf29b7a9-3ddb-4fbc-8aca-6efc70d2cff6`, `client_order_id=hourly-20260618-0451-buy-sbux`를 Alpaca MCP `cancel_order_by_id`로 즉시 취소했고, reconciliation 기준 `filled_qty=0`, `filled_avg_price=null`, `open orders=0`, `SBUX position 없음`으로 정리됐다. 이번 cycle의 최종 결과는 `candidate selected -> accepted after close -> immediate cancel -> no standing order/no fill`이다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Pre-submit market clock | PASS | live Alpaca `get_clock` `2026-06-17T15:54:24.777131681-04:00`, regular market open |
| Stale order lifecycle | PASS | `0451` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 account `ACTIVE`, open orders `0` |
| Research MCP | PASS tiered | `SEC EDGAR/FRED/Yahoo` positive `3`; `Alpha` empty_response, `Firecrawl` credits gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy count | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for SBUX | live IEX quote `99.56/99.59`, spread `0.0301%`, quote age 약 `0.04`분 |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 planned SBUX 1주 validation buy PASS |
| Final submit boundary clock | FAIL | actual submit time `16:01:40 ET`, live recheck `16:02:00 ET`, `is_open=false` |
| Final standing order state | PASS after correction | same order id 즉시 취소, `filled_qty=0`, `open orders=0` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_same_day_buy_for_trim | 0.0431% | `0211` same-day buy fill과 trim metric gap이 겹쳐 trim 승격 불가 |
| RGTI | blocked_same_day_duplicate_sell | 0.0494% | speculative trim trigger는 있으나 same US-date after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | blocked_same_day_duplicate_sell | 0.0385% | repeated weak-review trim rationale와 quote/spread는 pass하지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
| WMT | blocked_same_day_duplicate_buy | 0.0169% | `2026-06-17T14:07:50Z` fill 이후 same US-date duplicate buy 규율 유지 |
| BAC | blocked_same_day_duplicate_buy | 0.0177% | `2026-06-17T13:39:20Z` fill 이후 same US-date duplicate buy 규율 유지 |
| NEE | blocked_same_day_duplicate_buy | 0.0233% | `2026-06-17T14:59:48Z` fill 이후 same US-date duplicate buy 규율 유지 |
| XOM | blocked_same_day_duplicate_buy | 0.0285% | `2026-06-17T16:17:56Z` fill 이후 same US-date duplicate buy 규율 유지 |
| GOOGL | blocked_same_day_duplicate_buy | 0.0385% | `2026-06-17T16:40:11Z` fill 이후 same US-date duplicate buy 규율 유지 |
| SLB | blocked_same_day_duplicate_buy | 0.0397% | `2026-06-17T17:39:03Z` fill 이후 same US-date duplicate buy 규율 유지 |
| SPY | blocked_validation_floor_cap | 0.0054% | 1주 ask가 validation floor per-order cap `약 500.64 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0305% | 1주 ask가 validation floor per-order cap `약 500.64 USD`를 초과 |
| SMH | blocked_validation_floor_cap | 0.0449% | 1주 ask가 validation floor per-order cap `약 500.64 USD`를 초과 |
| SBUX | selected_then_canceled_at_close | 0.0301% | pre-submit hard gates 통과 후 submit 시각이 regular close 이후로 밀려 즉시 취소 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `same_day_buy_for_trim` | 0211 same-day buy fill이 있어 이번 cycle trim을 열지 않는다. trim metric gap도 남아 있다. |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-17T15:54:24.777131681-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-18-0451-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; `SBUX` quote `99.56/99.59` at `2026-06-17T19:54:26.242930941Z`; quote age 약 `0.04`분; spread `0.0301%`; order shape `buy 1 share / limit 99.59 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0451` stale/core/research preflight, runtime gate note, policy/review/ticker artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| SBUX | buy | 1 | 99.59 | `bf29b7a9-3ddb-4fbc-8aca-6efc70d2cff6` | `accepted` at `16:01:40 ET`, then immediate `canceled`, `filled_qty=0` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | shortlist shape 수정 후 재검증 PASS |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | planned SBUX 1주 validation buy PASS, staged deployment warning only |

## 제출 후 정산

- live `get_clock` 기준 `2026-06-17T16:02:00.785015971-04:00`, `is_open=false`였다.
- `get_order_by_id` 기준 `SBUX` 주문은 `canceled_at=2026-06-17T20:02:04.050879938Z`, `filled_qty=0`, `filled_avg_price=null`이다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_orders(status=all, symbols=SBUX, after=2026-06-17T00:00:00-04:00)` 기준 same-day `SBUX` order history는 canceled 1건뿐이다.
- `get_all_positions` 기준 positions는 `34`개이며 `SBUX` position은 생성되지 않았다.
- `get_account_info` snapshot은 cash `28,003.45 USD`, portfolio value `100,278.09 USD`, buying power `298,725.70 USD`다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0451-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0451-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0451-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0451-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0451-hourly-autopilot-post-trade.json`

## 지표 설명

- `selected_then_canceled_at_close`: pre-submit gate는 통과했지만 actual Alpaca submit timestamp가 regular close를 넘겨 workflow hard gate를 만족하지 못해 즉시 취소한 상태다.
- `same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy는 regular-session에서 다시 만들지 않는다.
- `same_day_buy_for_trim`: 같은 미국 거래일에 같은 symbol buy가 체결되면 trim/exit 재평가는 다음 cycle로 넘긴다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `500.64 USD`다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 analyst review와 policy learning에 사용한다.
