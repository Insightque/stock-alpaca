# 2026-06-05-0051-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0051` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup 기준 미체결 autopilot order는 없었고, scheduler Alpaca core preflight는 market/account/positions/open-orders/quotes hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider pass, `alpha-vantage`는 `empty_response` gap이었다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `AAPL`, `SLB`, `SPY`, `QQQ`는 같은 정규장 same-day filled buy라 duplicate discipline 때문에 제외했고, `BAC`는 같은 세션 earlier canceled buy 이력이 있어 duplicate risk를 피했다. `GOOGL`은 1D/5D review가 계속 약했고, `NVDA`는 AI semiconductor cluster 집중이 이미 높아 floor-size add 우선순위를 낮췄다. `XOM`은 research preflight shortlist 안에 있으면서 same-day duplicate가 없고, 기존 energy hedge/diversifier holding으로 runtime open-order/asset check를 통과했으며 scheduler quote `153.37/153.41`에서 spread `0.0261%`로 policy 한도 이내여서 1주 validation buy를 제출했다. Alpaca MCP `order_id=46a4b55c-3721-4b27-ab8a-8d04b6806aca`는 `2026-06-04T16:02:05.40965797Z`에 `153.26 USD`로 즉시 `filled`로 전환됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T11:55:48.708076806-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup 기준 stale candidate/open order 없음, runtime `get_orders status=open`도 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_orders/get_all_positions/get_asset` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha Vantage는 `empty_response` gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | XOM preflight quote `2026-06-04T15:51:32.64134203Z`, spread `0.0261%` |
| Risk plan | PASS | `XOM` 1주 buy_notional `153.41`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP `place_stock_order`가 `XOM` 1주 regular day limit buy를 생성했고 same client id reconciliation 기준 `filled` 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| XOM | submitted_filled | 0.0261% | same-day duplicate/open-order 충돌이 없고, energy hedge/diversifier 기존 보유로 floor-size learning buy 조건을 충족했다. |
| GOOGL | watch | 0.0190% | quote/spread는 양호하지만 최근 1D/5D review가 약해 replacement rank가 낮았다. |
| NVDA | watch | 0.0138% | quote/spread는 양호하지만 AI semiconductor_complex 집중이 높아 이번 cycle add 우선순위를 낮췄다. |
| BAC | watch | 0.0185% | financials 분산 후보지만 같은 정규장 earlier canceled buy 이력이 있어 duplicate conflict 가능성을 피했다. |
| SO | watch | 0.0220% | 방어주 성격은 유효하지만 최근 review와 trim diagnostics가 모두 약해 신규 floor-size buy 우선순위가 낮았다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 20D expected-excess/relative metric을 결정급으로 채우지 못했다. |
| SO | watch | decision_grade_metric_gap | 5D review는 중립 약함이지만 per-symbol decision-grade expected-excess 공백이 남아 trim justification이 부족했다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `XOM` buy 1 @ `153.41` day limit
- Alpaca order id: `46a4b55c-3721-4b27-ab8a-8d04b6806aca`
- Filled at: `2026-06-04T16:02:05.40965797Z` / average fill `153.26`
- Client order id: `hourly-20260605-0051-buy-xom`
- Same-session prior orders before this run: `QQQ`, `SPY`, `BAC(canceled)`, `SLB`, `AAPL`
- Reconciliation: `get_order_by_client_id`와 same-window `get_orders` 모두 `XOM`을 `filled`로 반환했고, `get_all_positions` 기준 XOM 보유수량은 2주에서 3주로 늘었다. runtime `get_account_info`는 두 차례 모두 `cancelled`였으므로 계좌 현금/포트폴리오 합계는 scheduler core preflight의 마지막 confirmed snapshot을 유지하고, fill price는 `get_account_activities(FILL)` `2026-06-04T16:02:05.409658Z`로 대조했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | XOM 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0051-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0051-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0051-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0051-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `empty_response`: 이번 cycle의 Alpha Vantage는 shortlist symbols 기준 반환된 candidate news item이 없어 `empty_response` gap으로 기록했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 제출되었거나 취소 이력이 있는 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 same-day duplicate와 cluster discipline을 통과한 XOM이 더 높은 learning-order 우선순위를 가졌다.
