# 2026-06-06-0131-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0131` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 remaining open order 0건으로 `pass`, scheduler Alpaca core preflight는 `clock/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였고 `alpha-vantage`는 one-call-per-hour throttle에 따른 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. same-day duplicate 규칙 때문에 `BAC`, `WMT`, `FCX`, `PLTR`, `AAPL`, `V`, `NVDA`, `SLB`는 추가 buy 대상에서 제외했고, `QQQ`와 `SPY`는 runtime ask `716.91 USD` / `744.02 USD`가 validation per-order cap 약 `496.41 USD`를 초과했다. `AMZN`, `NKE`, `GOOGL`은 최근 5D review 약세가 이어졌고 `SO`, `INTC`는 runtime spread가 policy cap을 넘었다. 반면 `COP`는 research preflight shortlist 포함 기존 energy holding으로서 2026-06-05 portfolio review에서 5D follow-through가 SPY 대비 `+4.00%p`, QQQ 대비 `+4.08%p`로 양호했고, runtime quote `117.49/117.51`, spread `0.0170%`, preflight asset active/tradable, same-day duplicate/open-order conflict 없음, review backlog throttle 통과 조건을 충족해 1주 floor-size validation buy 후보로 승격했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | scheduler core preflight `get_clock` timestamp `2026-06-05T12:31:08.482569286-04:00`, hard gate `pass` |
| Stale order lifecycle | PASS | scheduler cleanup pass, stale autopilot order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_orders(status=open)/get_orders(status=all)/get_stock_latest_quote/get_all_positions` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | runtime `COP` quote `2026-06-05T16:33:59.114073003Z`, spread `0.0170%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `place_stock_order` accepted, post-submit `get_all_positions` 기준 `COP 2주 -> 3주`로 fill inferred |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| COP | submitted_filled_inferred | 0.0170% | 2026-06-05 portfolio review에서 5D follow-through가 SPY 대비 +4.00%p, QQQ 대비 +4.08%p로 양호했고 same-day duplicate/open-order 충돌이 없는 existing energy holding이다. |
| AMZN | watch_review_weak | 0.0158% | spread는 통과했지만 최근 5D review가 계속 약했다. |
| NKE | watch_review_weak | 0.0233% | consumer turnaround validation이 5D에서도 약해 우선순위를 낮췄다. |
| GOOGL | watch_borderline_spread_review_weak | 0.4625% | spread가 hard cap 경계에 있고 최근 5D review도 약했다. |
| SO | watch_spread_fail | 6.4776% | runtime bid/ask 괴리가 커서 spread hard gate를 통과하지 못했다. |
| INTC | watch_spread_fail | 0.7396% | ai_semiconductor warning band에 더해 spread cap을 초과했다. |
| QQQ | watch_notional_cap | 0.0042% | benchmark fallback은 유효했지만 1주 ask `716.91 USD`가 validation per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0040% | benchmark fallback은 유효했지만 1주 ask `744.02 USD`가 validation per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 남아 있지만 per-symbol decision-grade expected-excess 공백이 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `COP` buy 1 @ `117.51` day limit
- Alpaca order id: `a50fe428-af24-4829-98bd-be3a80b2728d`
- Client order id: `hourly-20260606-0131-buy-cop`
- Pre-submit gate summary: paper mode `true`, market clock source `0131` scheduler core preflight hard-gate `pass`, order plan path `wiki/trade-ledger/orders/2026-06-06-0131-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, COP quote freshness 약 `0.6`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0131` stale cleanup/core/research preflight와 policy/review/COP artifacts
- `place_stock_order`: first submit accepted, retry 불필요
- Reconciliation: direct `get_order_by_client_id`, `get_order_by_id`, `get_orders(status=all, symbols=COP)` 경로는 tool safety monitor가 막혔다. 대신 runtime `get_orders(status=open, symbols=COP)`는 0건이었고, post-submit `get_all_positions`에서 `COP`가 `2주 @ 117.06`에서 `3주 @ 117.18`로 갱신됐다. 따라서 이번 1주 validation add는 약 `117.42 USD`에 체결된 것으로 추정 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 4개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | COP 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0131-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0131-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0131-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0131-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 `provider_error`로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled 또는 submit된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `filled_inferred_from_positions`: direct order lookup이 막힌 경우 open orders 0건과 post-submit position delta를 결합해 fill 여부와 추정 단가를 기록하는 reconciliation 방식이다.
