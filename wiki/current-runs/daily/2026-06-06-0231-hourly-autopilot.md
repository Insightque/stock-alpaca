# 2026-06-06-0231-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0231` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 remaining open order 0건으로 `pass`, scheduler Alpaca core preflight는 `clock/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였고 `alpha-vantage`는 one-call throttle에 따른 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. 0231 recent fills 기준 `PFE`, `AMZN`, `COP`, `SLB`, `NVDA`, `V`, `AAPL`, `PLTR`, `FCX`, `WMT`, `BAC`는 same-day duplicate 규칙 때문에 추가 buy 대상에서 제외했다. `QQQ`와 `SPY`는 1주 ask가 validation per-order cap을 초과했고, `TSM`은 이미 큰 `ai_semiconductor_complex` 노출 때문에 selective allocation 구간에서 same-cluster add 우선순위가 낮았다. `NKE`는 consumer turnaround 5D 약세가 더 컸고 `SO`는 반복된 utilities validation 약세가 누적됐다. `NEE`는 existing utilities diversifier로서 four-provider positive research confirmation, FRED macro row, fresh preflight quote `85.45/85.47`, spread `0.0234%`, active/tradable, duplicate/open-order conflict 없음, review backlog throttle 통과 조건을 충족했다. hard gates가 모두 통과한 상태에서 learning_trade_directive가 요구하는 floor-size observation을 확보하기 위해 `NEE` 1주 validation add를 제출 대상으로 계획했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | scheduler core preflight clock `2026-06-05T13:31:11.663765087-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, stale autopilot order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, quote age 약 `3.8`분 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | preflight `NEE` quote `2026-06-05T17:31:28.011510693Z`, spread `0.0234%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | 첫 submit cancellation 후 동일 `client_order_id` 재시도에서 order 생성 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| NEE | submit_candidate | 0.0234% | same-day duplicate 없음, utilities diversifier, FRED macro confirmation 유지, floor-size learning trade 조건 충족 |
| SO | watch_review_weaker | 0.0215% | quote/spread는 좋지만 repeated weak utilities validation이 더 누적돼 NEE보다 ranking이 낮다. |
| NKE | watch_review_weak | 0.0233% | catalyst headline은 있지만 5D review 약세가 더 크고 hold-heavy recommendation profile이다. |
| TSM | watch_cluster_concentration | 0.0357% | quote/spread는 통과하지만 ai_semiconductor_complex 기존 노출이 높아 selective allocation 구간에서 add 우선순위가 낮다. |
| QQQ | watch_notional_cap | 0.0056% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0040% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | target-band deterioration와 earnings-event drawdown은 보이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | utilities/rate-sensitive validation review 약세는 남아 있지만 trim을 정당화할 per-symbol metric이 없다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Planned order: `NEE` buy 1 @ `85.47` day limit
- Planned client order id: `hourly-20260606-0231-buy-nee`
- Pre-submit gate summary: paper mode `true`, market clock `2026-06-05T13:31:11.663765087-04:00`, order plan path `wiki/trade-ledger/orders/2026-06-06-0231-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, NEE quote freshness 약 `3.8`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0231` stale cleanup/core/research preflight와 policy/review/NEE artifacts
- Submit result: 첫 `place_stock_order`는 safety cancellation으로 반환됐다. 즉시 `get_order_by_client_id(hourly-20260606-0231-buy-nee)` 404와 `get_orders(status=all, symbols=NEE, after=2026-06-05T04:00:00Z)` 0건을 확인한 뒤 동일 `client_order_id`로 1회만 재시도했고, `hourly-20260606-0231-buy-nee` 1주 regular-session day limit buy가 Alpaca order id `202d7a0d-c061-4385-a693-b91f403a2b4f`로 생성됐다.
- Reconciliation: `get_order_by_client_id`, `get_order_by_id`, `get_orders(status=all, symbols=NEE, after=2026-06-05T17:40:00Z)`가 동일 order를 `status=new`, `filled_qty=0`으로 확인했다. `get_orders(status=open, symbols=NEE)`와 추가 market-data refresh는 tool layer에서 cancelled 되었고, post-submit `get_all_positions/get_account_info` refresh는 이번 cycle에서 확보하지 못했다. 따라서 post-trade snapshot은 0231 scheduler preflight의 마지막 확정 계좌/포지션과 confirmed open-order state를 결합해 기록했다. `NEE` 보유수량은 확인 가능한 최신 snapshot 기준 아직 `4주 @ 86.745`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | NEE 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0231-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0231-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 one-call-per-hour throttle 때문에 nonblocking gap으로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled 또는 submit된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `validation per-order cap`: `paper_validation_execution.validation_order_sizing.max_validation_notional_pct_per_order`에 따라 계좌 가치 대비 과도한 1주 fallback ETF/benchmark 매수는 막는다.
