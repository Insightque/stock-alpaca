# 2026-06-05-0211-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0211` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup 기준 미체결 autopilot order는 없었고, scheduler Alpaca core preflight는 market/account/positions/open-orders/quotes hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider pass, `alpha-vantage`는 one-call-per-hour throttle에 따른 `provider_error` gap이었다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `QQQ`, `SPY`, `SLB`, `AAPL`, `XOM`, `WMT`, `FCX`, `COP`는 같은 정규장 same-day filled buy라 duplicate discipline 때문에 제외했고, `BAC`는 같은 세션 earlier canceled buy 이력이 있어 duplicate risk를 피했다. `NVDA`와 `SMH`는 AI semiconductor cluster warning 구간 때문에 이번 cycle add 우선순위에서 밀렸다. `NKE`와 `INTC`는 quote/spread는 통과했지만 최근 review 약세와 포트폴리오 기여도가 낮아 `GOOGL`보다 replacement rank가 낮았다. `GOOGL`은 research preflight shortlist 포함, 기존 mega-cap quality holding, runtime quote `372.43/372.48`에서 spread `0.0134%`, same-day duplicate/open-order 충돌이 없어 1주 validation buy를 제출했고 Alpaca MCP `order_id=7e8243e9-1a7a-4644-b242-a039774b2711`는 `filled_avg_price=372.43`으로 즉시 체결됐다. post-trade reconciliation 기준 GOOGL 보유수량은 3주가 됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T12:54:21.237362554-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup 기준 stale candidate/open order 없음, runtime `get_orders(status=open)`도 제출 전 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_orders/get_account_info/get_asset/get_stock_latest_quote` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha Vantage는 `empty_response` gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | GOOGL runtime quote `2026-06-04T17:16:34.091424512Z`, spread `0.0134%` |
| Risk plan | PASS | `GOOGL` 1주 buy_notional `372.48`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `GOOGL` 1주 regular day limit buy를 생성했고 즉시 `filled`로 확인됐다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| GOOGL | submitted_filled | 0.0134% | mega-cap quality 기존 보유 2주에 대한 floor-size validation add로 제출했고 즉시 체결됐다. |
| NKE | watch | 0.0231% | consumer diversifier지만 최근 1D review 약세와 lower replacement rank 때문에 GOOGL보다 우선순위가 낮다. |
| INTC | watch | 0.0270% | quote/spread는 통과했지만 AI semiconductor_complex 집중도와 prior weak review 때문에 floor-size buy 우선순위에서 밀렸다. |
| NVDA | watch | 0.0091% | 핵심 AI thesis는 유지되지만 cluster warning 구간과 기존 큰 보유 비중 때문에 추가 신규 buy를 보수적으로 유지했다. |
| BAC | watch | 0.0185% | runtime quote는 양호하지만 same-session earlier canceled buy 이력이 있어 duplicate-risk discipline 때문에 제외했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 20D expected-excess/relative metric을 결정급으로 채우지 못했다. |
| SO | watch | decision_grade_metric_gap | 5D review는 중립 약함이지만 per-symbol decision-grade expected-excess 공백이 남아 trim justification이 부족했다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `GOOGL` buy 1 @ `372.48` day limit
- Alpaca order id: `7e8243e9-1a7a-4644-b242-a039774b2711`
- Client order id: `hourly-20260605-0211-buy-googl`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, GOOGL quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`, reconciliation 기준 `status=filled`, `filled_qty=1`, `filled_avg_price=372.43`
- Reconciliation: `get_order_by_client_id`와 same-window `get_orders(symbol=GOOGL)`가 모두 동일 GOOGL order 1건을 `status=filled`로 반환했다. `get_all_positions` 기준 GOOGL 보유수량은 2주에서 3주로 증가했고 평균단가는 `381.52`로 갱신됐다. runtime `get_account_info` 기준 cash `31649.57`, portfolio value `103311.34`, buying power `256800.45`, long market value `71661.77`으로 관측됐다. `get_orders(status=open)`와 `get_account_activities_by_type(FILL)`는 tool-layer `cancelled`였지만 order/position/account cross-check로 체결을 확정했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | GOOGL 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0211-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0211-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0211-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0211-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 추가 provider call을 생략했고 `provider_error` gap으로 남았다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 제출되었거나 체결된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 weak-review consumer/legacy-semi 후보보다 GOOGL이 더 높은 learning-order 우선순위를 가졌다.
