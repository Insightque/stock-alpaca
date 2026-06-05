# 2026-06-05-2251-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `2251` stale cleanup/core/research preflight를 우선 사용했다. scheduler clock `2026-06-05T09:51:09.685015001-04:00` 기준 미국 정규장은 열려 있었고, research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였으며 `alpha-vantage`는 one-call-per-hour throttle에 따른 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. 직전 `2231` cycle의 `BAC`는 same-day filled 상태라 duplicate buy 재진입이 막혔고, 그 다음 actionable 후보인 `SLB`는 runtime asset check `active/tradable`, live quote `56.62/56.66`, quote age `4.4`분, spread `0.0706%`, review backlog throttle 통과, 2026-06-05 portfolio review의 5D follow-through 양호 조건을 동시에 만족해 floor-size learning buy 1주 후보로 승격했다. strict universe/MCP/risk validator는 모두 통과했지만, `place_stock_order`는 runtime safety cancellation으로 두 차례 모두 제출되지 않았고 reconciliation 결과 실제 Alpaca 주문은 생성되지 않았다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | scheduler-owned core preflight clock `2026-06-05T09:51:09.685015001-04:00`와 22:51 cycle 조립 시각 `2026-06-05T14:00:33Z` 기준 regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, remaining stale autopilot orders 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(SLB)/get_stock_latest_quote(SLB)/get_all_positions/get_account_info` 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage는 one-call-per-hour throttle `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | SLB runtime quote `2026-06-05T13:56:09.34016401Z`, quote age `4.4`분, spread `0.0706%` |
| Risk plan | PASS | SLB 1주 buy notional `56.66`, cash/ticker/theme/factor/cluster caps 통과 |
| Execution | CANCELLED | `place_stock_order`가 runtime safety cancellation으로 두 차례 모두 제출되지 않았고 `client_order_id=hourly-20260605-2251-buy-slb`로 생성된 Alpaca 주문이 없었다. |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| BAC | recheck_only | preflight usable | 2231 cycle same-day filled buy가 있어 duplicate symbol/side gate가 이번 cycle 재진입을 막았다. |
| SLB | submit_cancelled | 0.0706% | 2026-06-05 portfolio review에서 5D 성과가 +4.58%, SPY 대비 +4.77%p로 양호했고 live quote/open-order/review backlog 하드 게이트를 모두 통과했지만, 실제 submit은 runtime safety monitor가 취소했다. |
| AAPL | watch | preflight usable | mega-cap quality add는 가능하지만 현재 포트폴리오의 mega-cap 노출 대비 SLB의 cluster diversification 기여가 더 컸다. |
| SPY | watch | preflight usable | benchmark floor buy는 fallback으로 유효하지만 SLB가 더 직접적인 policy-learning 표본이었다. |
| WMT | watch | preflight usable | defensive-diversification 5D review가 반복적으로 중립 약해 SLB보다 우선순위가 낮았다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Planned order: `SLB` buy 1 @ `56.66` day limit
- Client order id: `hourly-20260605-2251-buy-slb`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, SLB quote freshness `4.4`분 및 spread `PASS`, BAC same-day duplicate 차단 확인, SLB duplicate/open-order conflict 없음
- `place_stock_order`: runtime safety cancellation으로 두 차례 모두 submit되지 않았다.
- Reconciliation: `get_order_by_client_id(hourly-20260605-2251-buy-slb)`는 404를 반환했고 `get_orders(status=all, symbols=SLB, after=2026-06-05T04:00:00Z)`는 0건이었다. `get_all_positions` 기준 `SLB` 보유수량은 여전히 3주이며 open orders도 없다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | SLB 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-2251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-2251-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-2251-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 one-call-per-hour throttle 때문에 추가 provider call을 건너뛰었고, 이는 tiered research gate 하에서 nonblocking gap으로 남겼다.
- `review_backlog_throttle`: pending review 개수에 따라 신규 validation buy 슬롯을 줄이거나 막는 정책인데, 이번 run은 `pending_1d_count=0`이라 buy stop 조건에 닿지 않았다.
- `portfolio_construction_policy`: 신규 buy를 기존 보유와 비교해 분산 기여와 replacement rank를 함께 평가하는 규칙이다.
