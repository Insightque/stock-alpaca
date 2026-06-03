# 2026-06-04-0311-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler stale cleanup은 남은 stale/open autopilot order 없이 `pass`였다. Alpaca core preflight의 clock/account/positions/open orders/recent activities/quotes는 모두 통과했고, market clock은 `2026-06-03T14:11:09.223009494-04:00` 기준 regular market open이었다.

이번 run은 `submit` mode였지만 주문은 제출하지 않았다. Universe strict, MCP tiered strict, risk validator 대상 order plan은 통과 가능하도록 작성했으며, 22:31-23:31 KST regular validation buy entry window가 이미 닫혀 신규 buy는 만들지 않았다. Sell/trim 진단은 buy gate와 독립적으로 먼저 평가했지만 TSLA/SO/NEE 모두 정상 sell gate를 끝까지 통과하지 못했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler Alpaca preflight clock `2026-06-03T14:11:09.223009494-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-04-0311-hourly-autopilot-stale-order-cleanup.json`에서 blocking autopilot open order 없음 |
| Alpaca core MCP | PASS | account ACTIVE, positions 32건, open orders 0건, quote hard gate pass |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha provider_error(rate limit) 기록 |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Validation buy entry window | BLOCK new buys | 22:31-23:31 KST regular validation buy window outside current run |
| Quote/spread | MIXED | SPY/QQQ/BAC/WMT/AMZN/NOK/SO/NEE는 0.50% 이내, TSLA는 spread gate 실패 |
| Risk plan | PASS expected empty-order warning | 주문 0건, 현재 포지션 포함 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SPY | watch | 0.0026% | broad-index validation exposure가 이미 있고, entry window 밖에서 추가 add가 포트폴리오 기여를 높이지 못한다. |
| QQQ | watch | 0.0040% | 기존 benchmark hold가 있어 추가 add가 의미 있는 diversification이나 replacement-rank 개선으로 이어지지 않았다. |
| BAC | watch | 0.0191% | 이번 cycle에서는 FRED macro row가 복구됐지만 regular validation buy entry window가 닫혀 있어 신규 add를 만들지 않았다. |
| WMT | watch | 0.0172% | defensive-retail validation hold이지만 최근 약한 review 이후 replacement-rank edge가 부족했고 entry window도 닫혀 있다. |
| AMZN | watch | 0.0121% | 기존 mega-cap tech 노출이 이미 커서 fresh add가 portfolio contribution을 개선하지 못했고 entry window도 닫혀 있다. |
| NOK | blocked add | 0.0590% | 기존 큰 보유와 due 5D validation review 때문에 explicit add discipline을 유지했고 entry window도 닫혀 있다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| TSLA | watch | spread_and_held_quantity_and_metric_gap | spread 1.0979%가 정책 한도를 넘고 1주 보유라 25% trim을 whole-share로 만들기 어렵고 decision-grade expected-excess도 비어 있다. |
| SO | watch | decision_grade_metric_gap | spread 0.0327%와 FRED macro row는 통과했지만 decision-grade expected-excess 공백 때문에 trim justification이 부족했다. |
| NEE | watch | decision_grade_metric_gap | spread 0.0235%와 FRED macro row는 통과했지만 decision-grade expected-excess 공백 때문에 trim justification이 부족했다. |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 주문 후보가 비어 있어 작성/호출 대상이 없었다.
- Post-trade reconciliation: submit attempt는 없었지만 preflight open orders 0건, positions 32건, recent activities snapshot을 post-trade artifact에 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개 |
| `check-risk-policy.py --json` | PASS | 주문 0건 경고만 발생 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-04-0311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-04-0311-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-04-0311-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-04-0311-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-04-0311-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-04-0311-hourly-autopilot-research-mcp-preflight.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy review backlog count다. 이번 run에서는 2로 임계치 8 미만이라 buy slot 축소를 유발하지 않았고, sell/trim 진단과 독립적으로 유지했다.
- `gap_category`: 이번 run의 research 공백은 Alpha `provider_error`(daily rate limit)로 분류했고, FRED는 `pass`로 회복됐다.
- `portfolio_construction_policy`: 새 매수가 기존 보유 대비 분산, replacement-rank, portfolio contribution을 실제로 개선하는지 보는 계층이다.
