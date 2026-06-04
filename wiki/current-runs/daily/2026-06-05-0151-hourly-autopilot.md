# 2026-06-05-0151-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0151` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup 기준 미체결 autopilot order는 없었고, scheduler Alpaca core preflight는 market/account/positions/open-orders/quotes hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider pass, `alpha-vantage`는 `empty_response` gap이었다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `QQQ`, `SPY`, `SLB`, `AAPL`, `XOM`, `WMT`, `FCX`는 같은 정규장 same-day filled buy라 duplicate discipline 때문에 제외했고, `BAC`는 같은 세션 earlier canceled buy 이력이 있어 duplicate risk를 피했다. `V`는 runtime IEX quote spread가 1%를 넘어 hard spread gate에서 탈락했다. `GOOGL`과 `NEE`는 quote/spread는 통과했지만 2026-06-04 5D review 약세가 이어져 COP보다 replacement rank가 낮았다. `COP`는 research preflight shortlist 포함, 기존 energy/commodity diversifier holding, runtime quote `119.14/119.17`에서 spread `0.0252%`, same-day duplicate/open-order 충돌이 없어 1주 validation buy를 제출했다. Alpaca MCP `order_id=640b1123-bbf3-46f4-ada0-361ca2516672`는 reconciliation 시점 기준 `status=new` open order이고 COP 보유수량은 아직 1주다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T12:54:21.237362554-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup 기준 stale candidate/open order 없음, runtime `get_orders(status=open)`도 제출 전 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_orders/get_account_info/get_asset/get_stock_latest_quote` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha Vantage는 `empty_response` gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | COP runtime quote `2026-06-04T16:54:38.259198073Z`, spread `0.0252%` |
| Risk plan | PASS | `COP` 1주 buy_notional `119.17`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `COP` 1주 regular day limit buy를 생성했고 reconciliation 기준 `status=new` open order로 확인됐다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| COP | submitted_open | 0.0252% | energy/commodity diversifier 기존 보유로 same-day duplicate/open-order 충돌이 없고 runtime quote/asset check를 통과했다. 현재 status `new` open order다. |
| GOOGL | watch | 0.0135% | quote/spread는 양호하지만 2026-06-04 5D review가 약해 COP보다 replacement rank가 낮다. |
| NEE | watch | 0.0350% | defensive utility 후보지만 recent weak review와 macro/rate-sensitive 부담 때문에 COP보다 우선순위가 낮다. |
| V | watch | 1.2288% | runtime IEX spread가 policy 0.50% hard cap을 초과한다. |
| INTC | watch | - | AI semiconductor_complex 집중도와 prior weak review 때문에 COP보다 우선순위가 낮다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 20D expected-excess/relative metric을 결정급으로 채우지 못했다. |
| SO | watch | decision_grade_metric_gap | 5D review는 중립 약함이지만 per-symbol decision-grade expected-excess 공백이 남아 trim justification이 부족했다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `COP` buy 1 @ `119.17` day limit
- Alpaca order id: `640b1123-bbf3-46f4-ada0-361ca2516672`
- Client order id: `hourly-20260605-0151-buy-cop`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, COP quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`, reconciliation 기준 `status=new`, `filled_qty=0`
- Reconciliation: `get_order_by_client_id`와 same-window `get_orders(symbol=COP)`가 모두 동일 COP order 1건을 `status=new`로 반환했다. `get_orders(status=open)` 전체 조회도 COP 1건 open을 확인했다. `get_all_positions` 기준 COP 보유수량은 아직 1주 그대로이며, runtime `get_account_info` 기준 cash `32141.17`, portfolio value `103239.37`, buying power `257409.48`, long market value `71098.20`으로 관측됐다. `get_account_activities_by_type(FILL)` 1회는 tool-layer `cancelled`라 fill cross-check는 gap으로 남겼다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | COP 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0151-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0151-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0151-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0151-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `empty_response`: 이번 cycle의 Alpha Vantage는 shortlisted symbols 기준 candidate news가 비어 있어 `empty_response` gap으로 남았다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 제출되었거나 체결된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 weak-review mega-cap/defensive 후보보다 COP가 더 높은 learning-order 우선순위를 가졌다.
