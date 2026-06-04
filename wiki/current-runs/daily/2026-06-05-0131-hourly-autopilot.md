# 2026-06-05-0131-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0131` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup 기준 미체결 autopilot order는 없었고, scheduler Alpaca core preflight는 market/account/positions/open-orders/quotes hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider pass, `alpha-vantage`는 one-call-per-hour throttle에 따른 `provider_error` gap이었다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `QQQ`, `SPY`, `SLB`, `AAPL`, `XOM`, `WMT`는 같은 정규장 same-day filled buy라 duplicate discipline 때문에 제외했고, `BAC`는 같은 세션 earlier canceled buy 이력이 있어 duplicate risk를 피했다. `NVDA`는 AI semiconductor_complex 집중이 높고, `AMZN`, `NKE`, `NEE`, `TSLA`는 최근 review 약세나 rate-sensitive 부담으로 우선순위가 낮았다. `FCX`는 research preflight shortlist 포함, 기존 materials/mining holding, runtime quote `69.56/69.58`에서 spread `0.0288%`, same-day duplicate/open-order 충돌이 없어 1주 validation buy를 제출했다. Alpaca MCP `order_id=1e90f417-7b16-4201-a6b5-f94710b16b3a`는 `2026-06-04T16:41:07.019702918Z`에 `69.51 USD`로 즉시 `filled`로 전환됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T12:34:31.694331764-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup 기준 stale candidate/open order 없음, runtime `get_orders(status=open, symbols=FCX)`도 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_asset/get_orders/get_stock_latest_quote/get_account_info/get_all_positions` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha Vantage는 `provider_error` gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | FCX runtime quote `2026-06-04T16:34:43.302721119Z`, spread `0.0288%` |
| Risk plan | PASS | `FCX` 1주 buy_notional `69.58`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP `place_stock_order`가 `FCX` 1주 regular day limit buy를 생성했고 same client id reconciliation 기준 `filled` 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| FCX | submitted_filled | 0.0288% | materials/mining diversification holding으로 same-day duplicate/open-order 충돌이 없었고 runtime quote/asset check를 통과해 floor-size learning order로 승격됐다. |
| HOOD | watch | 0.0351% | research coverage는 pass지만 speculative_growth 노출과 portfolio construction discipline 때문에 FCX보다 우선순위가 낮다. |
| AMZN | watch | 0.0197% | quote/spread는 양호하지만 최근 5D review가 약해 FCX보다 replacement rank가 낮다. |
| NVDA | watch | 0.0230% | research coverage와 liquidity는 양호하지만 AI semiconductor_complex 집중이 높아 add 우선순위를 낮췄다. |
| NEE | watch | 0.0233% | defensive utility 후보지만 recent weak review와 rate-sensitive context 때문에 FCX보다 우선순위가 낮다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 20D expected-excess/relative metric을 결정급으로 채우지 못했다. |
| SO | watch | decision_grade_metric_gap | 5D review는 중립 약함이지만 per-symbol decision-grade expected-excess 공백이 남아 trim justification이 부족했다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `FCX` buy 1 @ `69.58` day limit
- Alpaca order id: `1e90f417-7b16-4201-a6b5-f94710b16b3a`
- Filled at: `2026-06-04T16:41:07.019702918Z` / average fill `69.51`
- Client order id: `hourly-20260605-0131-buy-fcx`
- Same-session prior orders before this run: `QQQ`, `SPY`, `BAC(canceled)`, `SLB`, `AAPL`, `XOM`, `WMT`
- Reconciliation: `get_order_by_client_id`, symbol-specific `get_orders`, `get_account_activities(FILL)`가 모두 동일 `FCX` fill을 반환했고, `get_all_positions` 기준 FCX 보유수량은 1주에서 2주로 증가했다. runtime `get_account_info` 기준 cash `32141.17`, portfolio value `103185.52`, buying power `257576.32`, long market value `71044.35`로 갱신됐다. `get_orders(status=open)` 전체 조회 1회는 tool-layer `cancelled`였지만 `get_orders(status=open, symbols=FCX)` 재조회는 0건이었고 same-cycle order는 `filled`로 종결됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | FCX 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0131-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0131-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0131-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0131-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 `provider_error`로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 제출되었거나 취소 이력이 있는 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 speculative_growth 후보와 weak-review mega-cap 후보보다 FCX가 더 높은 learning-order 우선순위를 가졌다.
