# 2026-06-06-0211-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0211` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 remaining open order 0건으로 `pass`, scheduler Alpaca core preflight는 `clock/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였고 `alpha-vantage`는 `NEWS_SENTIMENT` 0건에 따른 `empty_response` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. same-day duplicate 규칙 때문에 `BAC`, `WMT`, `FCX`, `PLTR`, `AAPL`, `V`, `NVDA`, `SLB`, `COP`, `AMZN`은 추가 buy 대상에서 제외했고, `QQQ`와 `SPY`는 1주 ask가 validation per-order cap을 초과했다. `WMT`는 5D가 `중립 양호`지만 같은 세션 체결이 있어 duplicate gate에 막혔고, `INTC`는 5D review 약세와 ai_semiconductor_complex 간접 노출 때문에 `PFE`보다 ranking이 낮았다. `PFE`는 existing healthcare diversifier로서 four-provider positive research confirmation, Yahoo의 AI drug discovery headline, fresh preflight quote `26.08/26.09`, spread `0.0383%`, active/tradable, duplicate/open-order conflict 없음, review backlog throttle 통과 조건을 충족했다. hard gates가 모두 통과한 상태에서 learning_trade_directive가 요구하는 floor-size observation을 확보하기 위해 `PFE` 1주 validation add를 제출했고, 즉시 reconciliation 기준 주문은 `status=new`, `filled_qty=0` open order다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` timestamp `2026-06-05T13:14:31.433003301-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, stale autopilot order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, quote age 약 `2.2`분 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `empty_response` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | preflight `PFE` quote `2026-06-05T17:11:28.278680781Z`, spread `0.0383%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `place_stock_order` accepted, immediate reconciliation 기준 `status=new` open order |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| PFE | submitted_open | 0.0383% | same-day duplicate 없음, healthcare diversifier, AI drug discovery Yahoo headline, floor-size learning trade 조건 충족 |
| WMT | watch_duplicate | 0.0416% | 5D는 `중립 양호`지만 `2026-06-05` ET same-day fill이 있어 duplicate symbol/side gate에 걸렸다. |
| INTC | watch_review_weak | 0.0196% | quote/spread는 통과하지만 5D review 약세와 ai_semiconductor_complex 간접 노출로 ranking이 낮다. |
| QQQ | watch_notional_cap | 0.0056% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0027% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | target-band deterioration와 earnings-event drawdown은 보이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | utilities/rate-sensitive validation review 약세는 남아 있지만 trim을 정당화할 per-symbol metric이 없다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `PFE` buy 1 @ `26.09` day limit
- Alpaca order id: `c646425a-7a9d-42c2-b611-7776cce9446d`
- Client order id: `hourly-20260606-0211-buy-pfe`
- Pre-submit gate summary: paper mode `true`, market clock `2026-06-05T13:14:31.433003301-04:00`, order plan path `wiki/trade-ledger/orders/2026-06-06-0211-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, PFE quote freshness 약 `2.2`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0211` stale cleanup/core/research preflight와 policy/review/PFE artifacts
- `place_stock_order`: first submit accepted, retry 불필요
- Reconciliation: `get_order_by_client_id`와 `get_orders(status=all, symbols=PFE, after=2026-06-05T04:00:00Z)`가 동일 order를 `status=new`, `filled_qty=0`으로 확인했다. `get_orders(status=open, symbols=PFE)`는 tool layer에서 1회 cancelled 되었지만 direct order lookup과 all-orders reconciliation이 open order 상태를 재확인했다. `get_all_positions` 기준 `PFE` 보유수량은 아직 `3주 @ 26.196667`이고, post-submit `get_account_info`는 성공해 cash `28,722.10 USD`, buying power `243,636.32 USD`, portfolio value `98,973.27 USD`를 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | PFE 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0211-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0211-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0211-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0211-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `empty_response`: 이번 cycle의 Alpha Vantage는 `NEWS_SENTIMENT` 0건으로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled 또는 submit된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `validation per-order cap`: `paper_validation_execution.validation_order_sizing.max_validation_notional_pct_per_order`에 따라 계좌 가치 대비 과도한 1주 fallback ETF/benchmark 매수는 막는다.
