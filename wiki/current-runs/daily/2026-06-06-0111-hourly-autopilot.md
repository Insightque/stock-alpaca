# 2026-06-06-0111-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0111` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 remaining open order 0건으로 `pass`, scheduler Alpaca core preflight는 `clock/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였고 `alpha-vantage`는 one-call-per-hour throttle에 따른 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. 직전 `NVDA` validation buy는 scheduler core preflight의 recent fills row에서 `2026-06-05T16:02:01.455431Z` / `208.73 USD` filled로 확인되어 open-order lifecycle blocker가 해소됐다. same-day duplicate 규칙 때문에 `BAC`, `WMT`, `FCX`, `PLTR`, `AAPL`, `V`, `NVDA`는 추가 buy 대상에서 제외했고, `QQQ`와 `SPY`는 runtime ask `719.56 USD` / `745.65 USD`가 validation per-order cap 약 `498.41 USD`를 초과했다. `GOOGL`, `AMZN`, `INTC`, `NKE`, `SO`는 최근 5D review가 약해 replacement rank가 `SLB`보다 낮았다. 반면 `SLB`는 research preflight shortlist 포함 기존 energy-services holding으로서 2026-06-05 portfolio review에서 5D follow-through가 SPY 대비 `+4.77%p`, QQQ 대비 `+4.86%p`로 양호했고, runtime quote `55.68/55.70`, spread `0.0359%`, asset active/tradable, same-day duplicate/open-order conflict 없음, review backlog throttle 통과 조건을 충족해 1주 floor-size validation buy 후보로 승격했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | scheduler core preflight `get_clock` timestamp `2026-06-05T12:11:11.300575883-04:00`, hard gate `pass` |
| Stale order lifecycle | PASS | scheduler cleanup pass, stale autopilot order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_account_info/get_all_positions/get_orders(status=open)/get_stock_latest_quote` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | runtime `SLB` quote `2026-06-05T16:14:26.272514414Z`, spread `0.0359%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `place_stock_order` accepted, `get_order_by_client_id` 기준 즉시 `filled` 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SLB | submitted_filled | 0.0359% | 2026-06-05 portfolio review에서 5D follow-through가 SPY 대비 +4.77%p, QQQ 대비 +4.86%p로 양호했고 same-day duplicate/open-order 충돌이 없는 existing energy-services holding이다. |
| COP | watch | 0.0340% | 5D review는 양호하지만 energy cluster에서 직전 보유/표본이 이미 있어 `SLB`보다 replacement rank가 낮았다. |
| GOOGL | watch_review_weak | 0.2083% | mega-cap quality label 대비 최근 5D review가 계속 약했다. |
| AMZN | watch_review_weak | 0.0198% | 5D review 약세가 이어져 floor-size learning buy 우선순위가 낮았다. |
| SO | watch_review_weak | 0.0323% | macro row는 있지만 utilities validation cohort가 반복적으로 약해 add 우선순위를 낮췄다. |
| QQQ | watch_notional_cap | 0.0056% | benchmark fallback은 유효했지만 1주 ask `719.56 USD`가 validation per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0040% | benchmark fallback은 유효했지만 1주 ask `745.65 USD`가 validation per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 남아 있지만 per-symbol decision-grade expected-excess 공백이 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `SLB` buy 1 @ `55.70` day limit
- Alpaca order id: `168aa67e-ad79-4dad-8e9c-4962fca93ef2`
- Filled at: `2026-06-05T16:15:33.962605999Z` / average fill `55.67`
- Client order id: `hourly-20260606-0111-buy-slb`
- Pre-submit gate summary: paper mode `true`, market clock source `0111` scheduler core preflight hard-gate `pass`, order plan path `wiki/trade-ledger/orders/2026-06-06-0111-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, SLB quote freshness 약 `1.1`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0111` stale cleanup/core/research preflight와 policy/review/SLB artifacts
- `place_stock_order`: accepted on first submit, retry 불필요
- Reconciliation: `get_order_by_client_id(hourly-20260606-0111-buy-slb)` 기준 `status=filled`, `filled_qty=1`, `filled_avg_price=55.67` 확인. post-submit `get_orders`, `get_all_positions`, `get_account_info` refresh는 tool layer에서 cancelled 되어 last confirmed pre-submit account snapshot `portfolio_value 99,681.62 USD`, `cash 29,148.36 USD`, `buying_power 245,718.16 USD`, `long_market_value 70,533.26 USD`를 유지 기록했고, runtime pre-submit positions의 `SLB 3주`에 confirmed fill 1주를 더해 reconciliation상 `SLB 4주`로 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | SLB 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0111-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0111-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0111-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0111-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 `provider_error`로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled 또는 submit된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `validation per-order cap`: floor-size learning buy라도 `paper_validation_execution.validation_order_sizing`의 per-order notional cap은 유지되므로 `QQQ/SPY` 1주 fallback은 이번 cycle에서 예산 초과로 남겼다.
