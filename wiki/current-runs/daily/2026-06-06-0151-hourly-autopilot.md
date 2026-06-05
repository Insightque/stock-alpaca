# 2026-06-06-0151-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0151` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 remaining open order 0건으로 `pass`, scheduler Alpaca core preflight는 `clock/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였고 `alpha-vantage`는 one-call-per-hour throttle에 따른 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. same-day duplicate 규칙 때문에 `BAC`, `WMT`, `FCX`, `PLTR`, `AAPL`, `V`, `NVDA`, `SLB`, `COP`는 추가 buy 대상에서 제외했고, `QQQ`, `SPY`, `SMH`는 1주 ask `715.51 USD` / `743.57 USD` / `583.21 USD`가 validation per-order cap 약 `496.29 USD`를 초과했다. `TSLA`는 speculative low-confidence bucket이라 승격하지 않았고 `NKE`는 hold-heavy turnaround review 약세로 `AMZN`보다 ranking이 낮았다. 반면 `AMZN`은 research preflight shortlist 포함 기존 mega-cap AI/cloud holding으로서 four-provider positive research confirmation, Yahoo recommendation breadth, fresh preflight quote `253.12/253.17`, spread `0.0197%`, active/tradable, duplicate/open-order conflict 없음, review backlog throttle 통과 조건을 충족했다. 최근 5D review 약세는 ranking note로만 반영하고, hard gates가 모두 통과한 상태에서 learning_trade_directive가 요구하는 floor-size observation을 확보하기 위해 `AMZN` 1주 validation add를 제출했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | scheduler core preflight `get_clock` timestamp `2026-06-05T12:51:11.868313181-04:00`, hard gate `pass` |
| Stale order lifecycle | PASS | scheduler cleanup pass, stale autopilot order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_account_info/get_orders(status=open)/get_account_activities(FILL)` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | preflight `AMZN` quote `2026-06-05T16:51:31.704340805Z`, spread `0.0197%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `place_stock_order` accepted, `get_order_by_client_id` 기준 `2026-06-05T17:01:54.545263432Z` `253.17 USD` filled |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AMZN | submitted_filled | 0.0197% | research preflight shortlist, same-day duplicate 없음, Yahoo recommendation breadth 강함, floor-size learning trade 조건 충족 |
| NKE | watch_review_weak | 0.0233% | spread는 통과했지만 hold-heavy turnaround thesis와 최근 review 약세로 `AMZN`보다 ranking이 낮았다. |
| TSLA | watch_low_confidence | 0.0227% | speculative growth/event-driven 성격이 강하고 current thesis confidence가 낮다. |
| QQQ | watch_notional_cap | 0.0056% | benchmark fallback은 유효했지만 1주 ask `715.51 USD`가 validation per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0067% | benchmark fallback은 유효했지만 1주 ask `743.57 USD`가 validation per-order cap을 초과했다. |
| SMH | watch_notional_cap | 0.0206% | semiconductor ETF fallback은 유효했지만 1주 ask `583.21 USD`가 validation per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 남아 있지만 per-symbol decision-grade expected-excess 공백이 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `AMZN` buy 1 @ `253.17` day limit
- Alpaca order id: `ccfc1bb3-2f8a-4752-8185-a6b230ef6bad`
- Client order id: `hourly-20260606-0151-buy-amzn`
- Pre-submit gate summary: paper mode `true`, market clock source `0151` scheduler core preflight hard-gate `pass`, order plan path `wiki/trade-ledger/orders/2026-06-06-0151-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, AMZN quote freshness 약 `5.9`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0151` stale cleanup/core/research preflight와 policy/review/AMZN artifacts
- `place_stock_order`: first submit accepted, retry 불필요
- Reconciliation: `get_order_by_client_id`와 `get_orders(status=all, symbols=AMZN, after=2026-06-05T04:00:00Z)`가 동일 filled order를 확인했고 `get_account_activities(FILL)`도 같은 체결 1건을 반환했다. post-submit `get_all_positions` 기준 `AMZN`은 `3주 @ 271.12`에서 `4주 @ 266.6325`로 갱신됐다. post-submit `get_account_info`는 tool safety monitor가 취소되어 cash는 pre-submit 현금 `28,975.27 USD`에서 confirmed fill `253.17 USD`를 차감한 `28,722.10 USD` 추정치로 기록한다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | AMZN 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0151-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0151-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0151-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0151-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 `provider_error`로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled 또는 submit된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `validation per-order cap`: `paper_validation_execution.validation_order_sizing.max_validation_notional_pct_per_order`에 따라 계좌 가치의 0.5%를 넘는 1주 fallback ETF/benchmark 매수는 막는다.
