# 2026-06-05-0031-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0031` stale cleanup/core/research preflight를 우선 사용했다. 다만 prior-cycle `BAC` buy 1건은 cleanup 시점에는 fresh였지만 이번 decision 시점에는 stale unfilled autopilot order가 되었기 때문에, workflow 계약에 따라 Alpaca MCP `cancel_order_by_id`로 먼저 취소하고 open-order lifecycle gate를 복구했다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `SLB`, `SPY`, `QQQ`는 같은 정규장 same-day filled buy라 duplicate discipline 때문에 제외했고, `AMZN`은 2026-06-04 5D review가 약했다. `AAPL`은 runtime IEX quote `310.06/310.10`에서 spread `0.0129%`로 policy 한도 이내였고 mega-cap quality 기존 보유로 floor-size learning buy 조건을 충족해 1주 buy를 제출했다. Alpaca MCP `order_id=b0b8c633-96d5-4aa1-bdb2-c0d455110a66`는 `2026-06-04T15:41:26.912888446Z`에 즉시 `filled`로 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T11:34:25.101791594-04:00`, regular market open |
| Stale order lifecycle | PASS after runtime cancel | scheduler cleanup는 `BAC`를 fresh open order로 남겼지만, decision 시점 stale 전환 후 Alpaca MCP로 `2026-06-04T15:38:31Z` 취소 완료 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_account_info/get_orders/get_all_positions/get_order_by_client_id/get_stock_latest_quote` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha Vantage는 `provider_error` gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | AAPL quote `2026-06-04T15:36:04.107218872Z`, spread `0.0129%` |
| Risk plan | PASS | `AAPL` 1주 buy_notional `310.10`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP `place_stock_order`가 `AAPL` 1주 regular day limit buy를 생성했고 same client id reconciliation 기준 `filled` 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AAPL | submitted_filled | 0.0129% | stale BAC open-order 정리 후 duplicate/open-order 충돌이 없고, mega-cap quality 기존 보유로 floor-size learning buy 조건을 충족했다. |
| AMZN | watch | 0.0235% | quote/spread는 양호하지만 2026-06-04 5D review가 `약함`이라 AAPL보다 replacement rank가 낮았다. |
| PLTR | watch | 0.0351% | research coverage는 pass지만 speculative_growth 노출과 stale thesis note 때문에 우선순위가 낮았다. |
| SPY | watch | 0.0040% | `2026-06-04T14:40:11.754058Z` same-day filled buy가 있어 duplicate discipline 때문에 제외했다. |
| SLB | watch | 0.0173% | `2026-06-04T15:20:39.771624551Z` same-day filled buy가 있어 duplicate discipline 때문에 제외했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings 이후 급락 반전으로 trim 재점검 대상이지만 20D expected-excess/relative metric을 결정급으로 채우지 못했다. |
| SO | watch | decision_grade_metric_gap | 5D review는 중립 약함이지만 per-symbol decision-grade expected-excess 공백이 남아 trim justification이 부족했다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 whole-share trim이 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Canceled stale order: `BAC` buy 1 @ `53.60`, `client_order_id=hourly-20260604-2351-buy-bac`, `status=canceled`, `canceled_at=2026-06-04T15:38:31.780201499Z`
- Submitted order: `AAPL` buy 1 @ `310.10` day limit
- Alpaca order id: `b0b8c633-96d5-4aa1-bdb2-c0d455110a66`
- Filled at: `2026-06-04T15:41:26.912888446Z` / average fill `310.07`
- Reconciliation: `get_order_by_client_id`와 same-window `get_orders` 모두 `AAPL`을 `filled`로 반환했고, `get_all_positions` 기준 AAPL 보유수량은 1주에서 2주로 늘었다. runtime `get_account_info` 기준 portfolio value `103,075.23 USD`, cash `32,482.30 USD`, buying power `258,122.41 USD`로 갱신됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개 |
| `check-risk-policy.py --json` | PASS | AAPL 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0031-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0031-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0031-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0031-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 `provider_error`로 남았고, 나머지 4개 research confirmation으로 tiered strict gate를 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled된 동일 symbol/side buy는 추가 validation buy로 재사용하지 않는 규칙이다.
- `risk_open_order_lifecycle`: fresh였던 prior-cycle autopilot open order가 decision 시점에 stale로 넘어가면, 새 주문 전에 cancel/reconcile을 먼저 완료해야 하는 gate다.
