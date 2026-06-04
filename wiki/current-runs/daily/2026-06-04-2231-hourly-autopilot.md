# 2026-06-04-2231-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler stale cleanup은 남은 stale/open autopilot order 없이 `pass`였다. Alpaca core preflight의 clock/account/positions/open orders/recent activities/quotes는 모두 통과했고, market clock은 `2026-06-04T09:31:11.536439016-04:00` 기준 regular market open이었다.

이번 run은 `submit` mode였지만 주문은 제출하지 않았다. Universe strict, MCP tiered strict, risk validator 대상 order plan은 모두 통과 가능하도록 작성했으며, 실제 주문 후보는 sell/trim 진단, portfolio construction, validation lifecycle discipline을 통과하지 못했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler stale cleanup 및 Alpaca preflight clock `2026-06-04T09:31:11.536439016-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-04-2231-hourly-autopilot-stale-order-cleanup.json`에서 stale/open autopilot order 없음 |
| Alpaca core MCP | PASS | account ACTIVE, positions 32건, open orders 0건, quote hard gate pass |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha `empty_response` gap 기록 |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | MIXED | QQQ/BAC/NVDA/SMH/AMZN/GOOGL/NOK는 pass, SPY/AVGO/WMT/XOM은 spread gate fail |
| Risk plan | PASS expected empty-order warning | 주문 0건, 현재 포지션 포함 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SPY | blocked | 0.6290% | broad-index benchmark hold 자체는 유지되지만 현재 live spread가 policy 상한 0.50%를 넘었다. |
| QQQ | watch | 0.1700% | benchmark ETF hold가 이미 있어 추가 1주가 replacement-rank나 portfolio contribution을 의미 있게 개선하지 못했다. |
| BAC | watch | 0.0945% | FRED macro confirmation은 복구됐지만 existing holdings 대비 fresh add 우위가 충분하지 않았다. |
| NVDA | watch | 0.0610% | 5D review는 양호하지만 ai_semiconductor theme 27.66%와 factor/cluster 34.10%/34.10% 집중이 same-cluster add를 막았다. |
| SMH | watch | 0.0880% | ETF spread는 깨끗하지만 반도체 theme/cluster 비중이 이미 높고 SEC ETF lookup은 `empty_response` gap이다. |
| AMZN | watch | 0.0593% | 5D review가 약했고 mega-cap quality add가 AI core holdings보다 우선순위가 낮다. |
| GOOGL | watch | 0.0388% | Yahoo/Firecrawl support는 남아 있지만 5D review가 약해 신규 validation add 근거가 부족하다. |
| NOK | blocked add | 0.0636% | existing large position과 validation lifecycle blocked_add 상태 때문에 20D review 전 추가매수를 열지 않았다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_within_policy fail | AI semiconductor_complex 비중 34.10%와 당일 -14.37% reversal로 trim 재점검 대상이지만 live spread 4.8896%가 상한을 크게 넘었다. |
| SO | watch | decision_grade_metric_gap | FRED macro confirmation은 pass지만 5D review 약세를 실제 trim order로 올릴 decision-grade expected-excess가 없다. |
| TSLA | watch | held_quantity_and_metric_gap | spread 0.4945%는 간신히 통과했지만 1주 보유라 trim fraction을 whole-share로 맞추기 어렵고 decision-grade metric도 비어 있다. |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 주문 후보가 비어 있어 작성/호출 대상이 없었다.
- Post-trade reconciliation: submit attempt는 없었지만 scheduler preflight account/positions/open orders/recent fills snapshot을 `wiki/trade-ledger/positions/2026-06-04-2231-hourly-autopilot-post-trade.json`에 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개 |
| `check-risk-policy.py --json` | PASS | 주문 0건 경고만 발생 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-04-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-04-2231-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-04-2231-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-04-2231-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-04-2231-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-04-2231-hourly-autopilot-research-mcp-preflight.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: 이번 run에서는 0이라 buy slot throttle을 유발하지 않았고, pending 20D 2건은 lifecycle 추적 용도로만 기록했다.
- `gap_category`: 이번 run의 research 공백은 Alpha `empty_response` 하나뿐이며 core/research minimum confirmations는 유지됐다.
- `portfolio_construction_policy`: 새 매수가 existing holdings 대비 분산, replacement-rank, portfolio contribution을 실제로 개선하는지 보는 계층이다.
