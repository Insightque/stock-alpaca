# 2026-06-06-0251-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0251` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 fresh open autopilot order 1건(`NEE`)을 남긴 채 `pass`였고, scheduler Alpaca core preflight는 `clock/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였고 `alpha-vantage`는 one-call throttle에 따른 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. 0251 stale cleanup 기준 `NEE` fresh open buy 1건이 남아 있어 same symbol/cluster 신규 buy는 차단했다. same-day duplicate discipline으로 `AAPL`, `NVDA`, `WMT`, `SLB`, `BAC`, `COP`, `PFE`, `AMZN`, `V`, `PLTR`, `FCX`는 추가 buy 대상에서 제외했다. `SPY`는 1주 ask가 validation per-order cap을 초과했고, `HOOD`는 research coverage는 pass지만 speculative broker candidate이며 ticker thesis evidence가 얕다. `GOOGL`과 `NKE`는 quote/spread는 통과하지만 최근 5D review 약세가 이어져 replacement rank가 낮다. `CVX`는 existing energy diversifier로서 four-provider positive research confirmation, fresh preflight quote `187.62/187.68`, spread `0.0320%`, active/tradable, duplicate/open-order conflict 없음, review backlog throttle 통과 조건을 충족했다. hard gates가 모두 통과한 상태에서 learning_trade_directive가 요구하는 floor-size observation을 확보하기 위해 `CVX` 1주 validation add를 제출 대상으로 계획했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | scheduler core preflight clock `2026-06-05T13:51:09.616704425-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, stale autopilot order 0건, fresh `NEE` open buy 1건은 same symbol/cluster 차단만 적용 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, quote age 약 `4.1`분 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | preflight `CVX` quote `2026-06-05T17:51:30.236568449Z`, spread `0.0320%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | Alpaca MCP가 `CVX` 1주 regular-session day limit buy를 생성했고 reconciliation 기준 `status=new` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| CVX | submit_candidate | 0.0320% | energy diversifier, four-provider confirmation, fresh open `NEE`와 다른 cluster, floor-size learning trade 조건 충족 |
| GOOGL | watch_review_weak | 0.0163% | quote/spread는 양호하지만 5D review 약세와 mega-cap replacement rank 부족 |
| NKE | watch_review_weak | 0.0233% | consumer turnaround 5D 약세와 hold-heavy recommendation profile |
| HOOD | watch_thesis_shallow | 0.0373% | speculative broker candidate, source confidence medium, reusable thesis evidence 얕음 |
| NEE | skip_open_order | 0.0350% | fresh open buy `hourly-20260606-0231-buy-nee`가 남아 same symbol/cluster 신규 buy 차단 |
| SPY | watch_notional_cap | 0.0148% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | target-band deterioration와 earnings-event drawdown은 보이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | utilities/rate-sensitive validation review 약세는 남아 있지만 trim을 정당화할 per-symbol metric이 없다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Planned order: `CVX` buy 1 @ `187.68` day limit
- Planned client order id: `hourly-20260606-0251-buy-cvx`
- Pre-submit gate summary: paper mode `true`, market clock `2026-06-05T13:51:09.616704425-04:00`, order plan path `wiki/trade-ledger/orders/2026-06-06-0251-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, CVX quote freshness 약 `4.1`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0251` stale cleanup/core/research preflight와 policy/review/CVX artifacts
- Submit result: `place_stock_order`가 `hourly-20260606-0251-buy-cvx` 1주 regular-session day limit buy를 Alpaca order id `5fbf3e4a-cd4d-4551-88ef-d14fb2dd78fe`로 생성했고 direct lookup 기준 `status=new`, `filled_qty=0`이다.
- Reconciliation: `get_order_by_client_id`와 `get_order_by_id`가 동일 CVX 주문을 `status=new`, `filled_qty=0`으로 확인했다. post-submit `get_all_positions/get_open_position/get_stock_latest_trade`는 tool layer에서 cancelled 되어 latest confirmed positions snapshot은 0251 scheduler core preflight 기준 `CVX 1주 @ 184.03`, position count `33`을 유지 기록한다. 계좌 수치는 last confirmed pre-submit snapshot인 portfolio value `99,069.12 USD`, cash `28,696.01 USD`, buying power `243,685.21 USD`, long market value `70,373.11 USD`를 유지한다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 4개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | CVX 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0251-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0251-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 one-call-per-hour throttle 때문에 nonblocking gap으로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled 또는 submit된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `validation per-order cap`: `paper_validation_execution.validation_order_sizing.max_validation_notional_pct_per_order`에 따라 계좌 가치 대비 과도한 1주 fallback ETF/benchmark 매수는 막는다.
