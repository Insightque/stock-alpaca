# 2026-06-06-0311-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0311` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 stale autopilot order 0건으로 `pass`였고, scheduler Alpaca core preflight는 `clock/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였고 `alpha-vantage`는 one-call throttle에 따른 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. runtime Alpaca read-only 재확인 기준 fresh open order는 `CVX`, `NEE` 2건이라 same symbol/cluster 신규 buy만 차단했고, same-day duplicate discipline으로 `BAC`, `WMT`, `FCX`, `PLTR`, `AAPL`, `V`, `NVDA`, `SLB`, `COP`, `AMZN`, `PFE`는 추가 buy 대상에서 제외했다. `SPY`와 `QQQ`는 1주 ask가 validation per-order cap을 초과했고 `NKE`는 consumer turnaround 5D 약세가 이어졌다. `SO`는 repeated weak-to-neutral review라는 약점이 있지만, four-provider positive research confirmation과 FRED macro row, fresh runtime quote `93.30/93.32`, spread `0.0214%`, active/tradable, duplicate/open-order conflict 없음, invested ratio 약 `70.9%`의 acceleration 구간이라는 조건에서 가장 낮은 리스크의 diversifier floor-size learning trade 후보였다. hard gates가 모두 통과한 상태에서 learning_trade_directive가 요구하는 최소 1건의 policy-learning observation을 확보하기 위해 `SO` 1주 validation add를 제출 대상으로 계획했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` `2026-06-05T14:15:29.093440825-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, stale autopilot order 0건, fresh open buy `CVX`/`NEE` 2건은 same symbol/cluster 차단만 적용 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime account/open-orders/quote 교차 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | runtime `SO` quote `2026-06-05T18:15:52.534535839Z`, spread `0.0214%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | 첫 submit cancellation 후 same `client_order_id` reconciliation/retry까지 완료, Alpaca order 생성 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | submit_candidate | 0.0214% | utilities diversifier, four-provider confirmation + FRED macro row, fresh open-order conflict 없음, floor-size learning trade 조건 충족 |
| NKE | watch_review_weak | 0.0233% | quote/spread는 양호하지만 consumer turnaround 5D 약세와 replacement rank 부족 |
| NEE | skip_open_order | 0.0233% | fresh open buy `hourly-20260606-0231-buy-nee`가 남아 same symbol/cluster 신규 buy 차단 |
| SPY | watch_notional_cap | 0.0121% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과 |
| QQQ | watch_notional_cap | 0.0154% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과 |
| PLTR | skip_same_day_duplicate | n/a | same-day filled buy가 already recorded |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | target-band deterioration와 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 없다. |
| SO | watch | decision_grade_metric_gap | utilities/rate-sensitive review 약세는 누적됐지만 trim order로 승격할 per-symbol decision-grade metric이 비어 있다. |
| TSLA | watch | held_quantity_and_metric_gap | speculative loss control 신호는 보이지만 1주 보유라 trim minimum-remaining gate를 충족하기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Planned order: `SO` buy 1 @ `93.32` day limit
- Planned client order id: `hourly-20260606-0311-buy-so`
- Pre-submit gate summary: paper mode `true`, market clock `2026-06-05T14:15:29.093440825-04:00`, order plan path `wiki/trade-ledger/orders/2026-06-06-0311-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, SO quote freshness 약 `1.2`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0311` stale cleanup/core/research preflight와 policy/review/SO artifacts
- Submit result: 첫 `place_stock_order`는 tool safety cancellation으로 반환됐다. 즉시 `get_order_by_client_id` 404, `get_orders(status=all, symbols=SO, after=2026-06-05T04:00:00Z)` 0건, `get_orders(status=open, symbols=SO)` 0건, latest positions/account reconciliation을 확인한 뒤 동일 `client_order_id`로 1회만 재시도했고 `hourly-20260606-0311-buy-so` 1주 regular-session day limit buy가 Alpaca order id `dcf8d47c-979f-469c-a22c-06d04c5a25f1`로 생성됐다. direct lookup 기준 현재 `status=new`, `filled_qty=0`이다.
- Reconciliation: `get_order_by_client_id`와 `get_order_by_id`가 동일 주문을 `status=new`, `filled_qty=0`으로 확인했고 `get_orders(status=open, symbols=SO)`도 같은 open order를 반환했다. post-submit `get_all_positions`는 tool layer에서 cancelled 되어 latest confirmed pre-submit positions snapshot 기준 `SO 4주 @ 92.54`, position count `33`을 유지 기록한다. post-submit `get_account_info`는 성공해 portfolio value `98,610.82 USD`, cash `28,696.01 USD`, buying power `242,395.53 USD`, long market value `69,914.81 USD`를 기록한다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | SO 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0311-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0311-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 one-call-per-hour throttle 때문에 nonblocking gap으로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled 또는 submit된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `validation per-order cap`: `paper_validation_execution.validation_order_sizing.max_validation_notional_pct_per_order`에 따라 계좌 가치 대비 과도한 1주 benchmark fallback 매수는 막는다.
