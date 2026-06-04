# 2026-06-04-2331-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler stale cleanup은 남은 stale/open autopilot order 없이 `pass`였다. Alpaca core preflight의 clock/account/positions/open orders/recent activities/quotes는 모두 통과했고, market clock은 `2026-06-04T10:31:14.382322504-04:00` 기준 regular market open이었다.

이번 run은 `submit` mode였고, workflow 요구대로 sell/trim을 먼저 평가한 뒤 floor-size learning order를 만들었다. `QQQ`는 직전 23:11 cycle buy가 `2026-06-04T14:20:05.463508Z`에 이미 filled되어 same-day duplicate buy discipline에 걸렸기 때문에 broad-index fallback benchmark인 `SPY` 1주 regular-session day limit buy로 내렸다. Alpaca MCP `place_stock_order`는 `client_order_id=hourly-20260604-2331-buy-spy` / `order_id=a15802cd-81bf-4450-bfa5-52f8782fe8c9`를 생성했고, 같은 client order id reconciliation 결과 `filled_avg_price=753.75`, `status=filled`를 즉시 확인했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T10:34:47.63990962-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-04-2331-hourly-autopilot-stale-order-cleanup.json`에서 stale/open autopilot order 없음 |
| Alpaca core MCP | PASS | account ACTIVE, positions 32건, open orders 0건, preflight quote hard gate pass |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha는 hourly throttle로 `provider_error` gap 기록 |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | SPY spread `0.0040%`, quote timestamp `2026-06-04T14:34:41.220956164Z` |
| Risk plan | PASS | `SPY` 1주 buy_notional `753.98`, cash/exposure/ticker caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `SPY` 1주 regular day limit buy를 생성했고 즉시 filled로 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SPY | submitted | 0.0040% | QQQ same-day duplicate가 이미 filled였기 때문에 broad-index fallback benchmark로 승격했고, hard gate와 risk caps를 모두 통과한 뒤 즉시 filled됐다. |
| QQQ | watch | 0.0068% | benchmark quality는 유지됐지만 23:11 cycle buy가 이미 filled여서 same-day duplicate symbol/side discipline 때문에 재매수하지 않았다. |
| BAC | watch | 0.0375% | macro confirmation과 spread는 양호하지만 이번 cycle에서는 duplicate-free benchmark fallback이 우선이었다. |
| AMZN | watch | 0.1615% | mega-cap quality add blocker는 없지만 benchmark learning order가 먼저 workflow floor를 충족했다. |
| PLTR | watch | 0.0000% | validation winner이지만 이번 cycle은 same-day duplicate 회피와 benchmark observation 보강이 더 우선이었다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | cluster 경고구간과 급락으로 trim 재점검 대상이지만 decision-grade 20D metric 공백이 남아 즉시 trim order로 올리지 않았다. |
| SO | watch | decision_grade_metric_gap | FRED macro confirmation은 pass지만 per-symbol expected-excess 공백 때문에 trim justification이 부족했다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 trim fraction을 whole-share로 맞추기 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `SPY` buy 1 @ `753.98` day limit
- Alpaca order id: `a15802cd-81bf-4450-bfa5-52f8782fe8c9`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, SPY quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, reconciliation 기준 `status=filled`, `filled_qty=1`, `filled_avg_price=753.75`
- Reconciliation: `get_order_by_client_id`에서 동일 order 1건과 fill을 확인했고 `get_orders status=open`은 0건이었다. `get_all_positions` 기준 SPY는 2주로 증가했고 `get_account_info` 기준 cash `32850.02`, buying power `257857.68`, portfolio value `102506.84`로 갱신됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개 |
| `check-risk-policy.py --json` | PASS | SPY 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-04-2331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-04-2331-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-04-2331-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-04-2331-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-04-2331-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-04-2331-hourly-autopilot-research-mcp-preflight.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: 이번 run에서는 `0`이라 buy slot throttle을 유발하지 않았고, pending `20D=2`는 lifecycle 추적 용도로만 기록했다.
- `provider_error`: 이번 run의 Alpha Vantage는 장애가 아니라 hourly throttle 때문에 scheduler preflight가 provider call을 건너뛴 상태다. core와 나머지 research confirmations는 유지되어 strict MCP gate는 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled된 동일 symbol/side buy는 open order가 없더라도 새 validation buy로 재사용하지 않는 규칙이다.
