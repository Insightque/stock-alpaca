# 2026-06-04-2251-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler stale cleanup은 남은 stale/open autopilot order 없이 `pass`였다. Alpaca core preflight의 clock/account/positions/open orders/recent activities/quotes는 모두 통과했고, market clock은 `2026-06-04T09:51:11.073962224-04:00` 기준 regular market open이었다.

이번 run은 `submit` mode였고, workflow 요구대로 sell/trim을 먼저 평가한 뒤 floor-size learning order를 만들었다. 최종 계획은 `QQQ` 1주 regular-session day limit buy였지만, Alpaca MCP `place_stock_order`가 같은 `client_order_id`로 두 번 모두 tool safety layer에서 `cancelled` 처리되어 실제 주문 객체는 생성되지 않았다. 이후 `get_order_by_client_id`, `get_orders`, `get_all_positions`, `get_account_info`로 reconciliation을 수행했고 계좌/주문 상태 변화가 없음을 확인했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | stale cleanup 및 Alpaca preflight clock `2026-06-04T09:51:11.073962224-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-04-2251-hourly-autopilot-stale-order-cleanup.json`에서 stale/open autopilot order 없음 |
| Alpaca core MCP | PASS | account ACTIVE, positions 32건, open orders 0건, quote hard gate pass |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha는 hourly throttle로 `provider_error` gap 기록 |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | QQQ spread `0.0530%`, quote timestamp `2026-06-04T13:51:28.778732416Z` |
| Risk plan | PASS | `QQQ` 1주 buy_notional `735.58`, cash/exposure/ticker caps 통과 |
| Final submit path | FAIL at tool layer | Alpaca MCP `place_stock_order`가 두 번 모두 tool safety layer에서 `cancelled`; Alpaca order object 미생성 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| QQQ | selected | 0.0530% | 기존 benchmark holding이며 add blocker가 없고, AI semiconductor cluster를 더 키우지 않는 broad-index cluster라 floor-size learning order로 선택했다. |
| SPY | watch | 0.0478% | spread gate는 통과했지만 이번 cycle에서는 기존 보유 benchmark 중 QQQ가 우선순위가 더 높았다. |
| BAC | watch | 0.0374% | macro confirmation과 spread는 양호하지만 floor-size learning directive에서는 benchmark add가 우선이었다. |
| AMZN | watch | 0.0356% | mega-cap quality add blocker는 없지만 최근 5D review 약세가 남아 first validation order로는 후순위였다. |
| PLTR | watch | 0.0552% | validation winner지만 이번 run의 목적은 broad-index benchmark observation 보강이라 recheck candidate로만 남겼다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | cluster 경고와 급락으로 trim 재점검 대상이지만 decision-grade 20D metric 공백이 남아 즉시 trim order로 올리지 않았다. |
| SO | watch | decision_grade_metric_gap | FRED macro confirmation은 pass지만 per-symbol expected-excess 공백 때문에 trim justification이 부족했다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 trim fraction을 whole-share로 맞추기 어렵고 decision-grade metric도 비어 있다. |

## 주문 시도와 reconciliation

- Planned orders: `QQQ` buy 1 @ `735.58` day limit
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, QQQ quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order` attempt 1: `client_order_id=hourly-20260604-2251-buy-qqq` -> tool safety layer `cancelled`
- Reconciliation after attempt 1: `get_order_by_client_id` 404, `get_orders` same-day QQQ 0건, QQQ position 여전히 2주, account unchanged
- `place_stock_order` attempt 2: same `client_order_id` retry -> tool safety layer `cancelled`
- Final reconciliation: order object 없음, open orders 0건, fills 추가 없음, portfolio/account state change 없음

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개 |
| `check-risk-policy.py --json` | PASS | `QQQ` 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-04-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-04-2251-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-04-2251-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-04-2251-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-04-2251-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-04-2251-hourly-autopilot-research-mcp-preflight.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: 이번 run에서는 `0`이라 buy slot throttle을 유발하지 않았고, pending `20D=2`는 lifecycle 추적 용도로만 기록했다.
- `provider_error`: 이번 run의 Alpha Vantage는 장애가 아니라 hourly throttle 때문에 scheduler preflight가 provider call을 건너뛴 상태다. core와 나머지 research confirmations는 유지되어 strict MCP gate는 통과했다.
- `submit_tool_safety_cancelled`: 시장/리스크/coverage gate가 아니라 external tool safety layer가 `place_stock_order` 호출 자체를 중단시킨 경우를 뜻한다. 이번 run의 reconciliation 결과 Alpaca 계좌 state change는 없었다.
