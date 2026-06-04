# 2026-06-05-0111-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0111` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup 기준 미체결 autopilot order는 없었고, scheduler Alpaca core preflight는 market/account/positions/open-orders/quotes hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider pass, `alpha-vantage`는 one-call-per-hour throttle에 따른 `provider_error` gap이었다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `SPY`, `QQQ`, `SLB`, `AAPL`, `XOM`은 같은 정규장 same-day filled buy라 duplicate discipline 때문에 제외했고, `BAC`는 같은 세션 earlier canceled buy 이력이 있어 duplicate risk를 피했다. `PLTR`은 speculative_growth와 stale thesis note 때문에 우선순위가 낮았고, `GOOGL`, `V`, `AMZN`은 최근 5D review가 약하거나 초과수익 폭이 제한적이었다. `WMT`는 2026-06-04 analyst review에서 5D `중립 양호`로 회복됐고, 기존 consumer defensive holding으로 same-day duplicate가 없으며 runtime quote `118.37/118.40`에서 spread `0.0253%`로 policy 한도 이내여서 1주 validation buy를 제출했다. Alpaca MCP `order_id=c4705629-49b0-4080-851a-e889edb7c843`는 `2026-06-04T16:20:17.746749451Z`에 `118.36 USD`로 즉시 `filled`로 전환됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T12:14:34.731518354-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup 기준 stale candidate/open order 없음, runtime `get_orders status=open`도 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_asset/get_orders/get_stock_latest_quote/get_account_info` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha Vantage는 `provider_error` gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | WMT runtime quote `2026-06-04T16:15:34.402915497Z`, spread `0.0253%` |
| Risk plan | PASS | `WMT` 1주 buy_notional `118.40`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP `place_stock_order`가 `WMT` 1주 regular day limit buy를 생성했고 same client id reconciliation 기준 `filled` 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| WMT | submitted_filled | 0.0253% | 2026-06-04 5D review가 `중립 양호`로 회복됐고, same-day duplicate/open-order 충돌이 없는 기존 defensive holding으로 floor-size learning buy 조건을 충족했다. |
| PLTR | watch | 0.0351% | research coverage는 pass지만 speculative_growth 노출과 stale thesis note 때문에 우선순위가 낮다. |
| GOOGL | watch | 0.0190% | quote/spread는 양호하지만 최근 1D/5D review가 약해 replacement rank가 낮다. |
| NVDA | watch | 0.0138% | research coverage와 liquidity는 양호하지만 AI semiconductor_complex 집중이 높아 add 우선순위를 낮췄다. |
| V | watch | 0.0200% | quality diversification 후보지만 5D review가 약해 WMT보다 learning-order 우선순위가 낮다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 20D expected-excess/relative metric을 결정급으로 채우지 못했다. |
| SO | watch | decision_grade_metric_gap | 5D review는 중립 약함이지만 per-symbol decision-grade expected-excess 공백이 남아 trim justification이 부족했다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `WMT` buy 1 @ `118.40` day limit
- Alpaca order id: `c4705629-49b0-4080-851a-e889edb7c843`
- Filled at: `2026-06-04T16:20:17.746749451Z` / average fill `118.36`
- Client order id: `hourly-20260605-0111-buy-wmt`
- Same-session prior orders before this run: `QQQ`, `SPY`, `BAC(canceled)`, `SLB`, `AAPL`, `XOM`
- Reconciliation: `get_order_by_client_id`, same-window `get_orders`, `get_account_activities(FILL)`가 모두 동일 `WMT` fill을 반환했고, runtime `get_account_info` 기준 cash `32210.68`, portfolio value `103075.90`, buying power `257459.91`, long market value `70865.22`로 갱신됐다. direct position refresh는 `cancelled`였으므로 마지막 confirmed preflight의 `WMT 3주`에 filled qty `1주`를 더해 reconciliation상 `WMT 4주`로 기록했다. open orders는 0건이다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | WMT 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0111-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0111-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0111-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0111-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 `provider_error`로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 제출되었거나 취소 이력이 있는 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 weak-review mega-cap 후보와 speculative_growth 후보보다 WMT가 더 높은 learning-order 우선순위를 가졌다.
