# 2026-06-05-0011-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0011` stale cleanup/core/research preflight를 우선 사용했다. `2026-06-04T11:15:39.322531376-04:00` runtime Alpaca clock 기준 미국 정규장은 열려 있었고, stale cleanup 이후 남은 open order는 `BAC` buy 1건뿐이었다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. buy fallback 후보 중 `AAPL`은 runtime quote `2026-06-04T15:16:15.62335292Z`에서 spread 약 `0.5089%`로 policy 상한 `0.50%`를 초과해 hard gate 탈락했고, `AMZN`은 2026-06-04 portfolio review의 5D 약세 때문에 우선순위가 낮았다. `SLB`는 2026-06-04 5D review에서 energy diversifier 중 follow-through가 가장 양호했고 runtime quote `57.65/57.66`로 spread `0.0173%`를 유지해 1주 validation buy를 제출했다. Alpaca MCP `order_id=5fb634fc-6fed-47b9-9ced-86ebdf06f652`는 `2026-06-04T15:20:39.771624551Z`에 즉시 `filled`로 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T11:15:39.322531376-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-05-0011-hourly-autopilot-stale-order-cleanup.json`, stale cancellation 실패 없음 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_account_info/get_orders/get_all_positions/get_stock_latest_quote/get_asset` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive, Alpha Vantage는 `provider_error` gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | SLB quote `2026-06-04T15:16:39.502804575Z`, spread `0.0173%` |
| Risk plan | PASS | `SLB` 1주 buy_notional `57.66`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP `place_stock_order`가 `SLB` 1주 regular day limit buy를 생성했고 same client id reconciliation 기준 `filled` 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SLB | submitted_filled | 0.0173% | 2026-06-04 portfolio review에서 5D follow-through가 SPY 대비 +4.06%p, QQQ 대비 +2.97%p로 양호했고 same-day duplicate/open-order 충돌이 없어 floor-size learning buy로 승격했다. |
| AAPL | watch | 0.5089% | runtime quote `2026-06-04T15:16:15.62335292Z`에서 spread가 policy 상한 `0.50%`를 소폭 초과해 hard gate에서 제외했다. |
| AMZN | watch | 0.0196% | runtime spread는 양호했지만 2026-06-04 portfolio review의 5D 판단이 `약함`이라 SLB보다 우선순위가 낮았다. |
| SPY | watch | 0.0198% | `2026-06-04T14:40:11.754058Z` same-day filled buy가 있어 duplicate discipline 때문에 제외했다. |
| QQQ | watch | 0.0041% | `2026-06-04T14:20:05.463508Z` same-day filled buy가 있어 duplicate discipline 때문에 제외했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings 이후 급락으로 trim 재점검 대상이지만 20D expected-excess/relative metric을 결정급으로 채우지 못했다. |
| SO | watch | decision_grade_metric_gap | 5D review는 중립 약함이지만 per-symbol decision-grade expected-excess 공백이 남아 trim justification이 부족했다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `SLB` buy 1 @ `57.66` day limit
- Alpaca order id: `5fb634fc-6fed-47b9-9ced-86ebdf06f652`
- Filled at: `2026-06-04T15:20:39.771624551Z` / average fill `57.65`
- Remaining open order: `BAC` buy 1 @ `53.60`, `status=new`, `client_order_id=hourly-20260604-2351-buy-bac`
- Reconciliation: `get_order_by_client_id`는 `SLB`를 `filled`로 반환했고, `get_all_positions` 기준 SLB 보유수량은 2주에서 3주로 늘었다. runtime `get_account_info` 기준 portfolio value `103,222.48 USD`, cash `32,792.37 USD`, buying power `258,869.54 USD`로 갱신됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개 |
| `check-risk-policy.py --json` | PASS | SLB 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0011-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0011-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0011-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0011-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: 이번 run에서는 `0`이라 validation buy throttle을 유발하지 않았다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 `provider_error`로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled된 동일 symbol/side buy는 추가 validation buy로 재사용하지 않는 규칙이다.
