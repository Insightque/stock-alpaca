# 2026-06-03-2251-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler stale cleanup은 남은 stale/open autopilot order 없이 `pass`였다. Alpaca core preflight의 clock/account/positions/open orders/recent activities/quotes는 모두 통과했고, market clock은 `2026-06-03T09:51:08.474978097-04:00` 기준 regular market open이었다.

이번 run은 `submit` mode였지만 주문은 제출하지 않았다. Universe strict, MCP tiered strict, risk validator 대상 order plan은 통과 가능하도록 작성했으며, 실제 주문 후보는 sell/trim 진단, critical-source, validation lifecycle, portfolio construction 필터를 통과하지 못했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler Alpaca preflight clock `2026-06-03T09:51:08.474978097-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-03-2251-hourly-autopilot-stale-order-cleanup.json`에서 blocking autopilot open order 없음 |
| Alpaca core MCP | PASS | account ACTIVE, positions 32건, open orders 0건, quote hard gate pass |
| Research MCP | PASS tiered | SEC EDGAR/Firecrawl/Yahoo 3개 positive; Alpha provider_error(throttle), FRED provider_error 429 기록 |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | MIXED | SPY/QQQ/BAC/WMT/NKE/NOK/TSLA/NEE는 pass, SO/AVGO는 spread fail |
| Risk plan | PASS expected empty-order warning | 주문 0건, 현재 포지션 포함 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SPY | watch | 0.0040% | broad-index validation exposure가 이미 있고 replacement-rank 개선이 충분하지 않다. |
| QQQ | watch | 0.0094% | 기존 benchmark hold가 있어 추가 add가 포트폴리오 기여를 의미 있게 높이지 못했다. |
| BAC | watch | 0.0385% | 금융 분산 후보지만 rate-sensitive positive thesis는 FRED macro row 실패 때문에 watch로 강등했다. |
| WMT | watch | 0.0173% | defensive quality hold지만 최근 weak validation-add 맥락과 기존 보유 대비 replacement-rank 우위가 부족했다. |
| NKE | watch | 0.0457% | 최근 weak validation review와 기존 held exposure 대비 replacement-rank 개선이 부족했다. |
| NOK | blocked add | 0.0603% | 기존 큰 보유와 due 5D validation review 때문에 explicit add discipline을 유지했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| TSLA | watch | held_quantity_and_metric_gap | spread는 0.0426%로 정상화됐지만 1주 보유라 25% trim 규칙을 만족하는 부분 축소가 어렵고 decision-grade expected-excess가 비어 있다. |
| SO | watch | spread_within_policy fail | weak defensive review 이후 재점검 대상이지만 spread 8.8639%와 FRED macro gap 때문에 trim 주문으로 올리지 않았다. |
| NEE | hold_watch | decision_grade_metric_and_macro_gap | spread 0.0464%는 통과권이지만 FRED 429와 decision-grade expected-excess 공백으로 trim justification이 부족했다. |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 주문 후보가 비어 있어 작성/호출 대상이 없었다.
- Post-trade reconciliation: submit attempt는 없었지만 preflight open orders 0건, positions 32건, recent fills snapshot을 post-trade artifact에 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | 주문 0건 경고만 발생 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-03-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-03-2251-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-03-2251-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-03-2251-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-03-2251-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-03-2251-hourly-autopilot-research-mcp-preflight.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy review backlog count다. 이번 run에서는 2로 임계치 8 미만이라 buy slot 축소를 유발하지 않았고, sell/trim 진단과 독립적으로 유지했다.
- `gap_category`: 이번 run의 research 공백은 Alpha `provider_error`(one-call-per-hour throttle), FRED `provider_error`(429)로 분류했다.
- `portfolio_construction_policy`: 새 매수가 기존 보유 대비 분산, replacement-rank, portfolio contribution을 실제로 개선하는지 보는 계층이다.
