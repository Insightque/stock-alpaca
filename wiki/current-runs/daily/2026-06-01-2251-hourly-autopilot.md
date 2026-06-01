# 2026-06-01-2251-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler stale cleanup은 남은 stale/open autopilot order 없이 `pass`였다. Alpaca core preflight는 clock/account/positions/open orders/recent activities/quotes를 모두 통과했고, quote row는 `2026-06-01T13:51:32Z` 기준으로 decision 시점 20분 이내였다.

이번 run은 `submit` mode였지만 주문은 제출하지 않았다. Universe strict, MCP tiered strict, risk validator 대상 order plan은 통과했고, 실제 주문 후보는 sell/trim 진단, validation lifecycle, critical source, portfolio construction 필터를 통과하지 못했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | Alpaca preflight clock `2026-06-01T09:51:12.061717275-04:00`, regular market open |
| Stale order cleanup | PASS | stale/open autopilot order 없음: `wiki/evidence-store/sources/2026-06-01-2251-hourly-autopilot-stale-order-cleanup.json` |
| Alpaca core MCP | PASS | account ACTIVE, positions 32건, open orders 0건, quote batch 62건 |
| Research MCP | PASS tiered | SEC EDGAR/Firecrawl/Yahoo 3개 positive; Alpha/FRED provider_error 기록 |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | MIXED | SPY/BAC/SMH/AAPL/HOOD 등 pass, AMD/AVGO/TSLA는 spread cap 초과 |
| Risk plan | PASS expected empty-order warning | 주문 0건, 현재 포지션 포함 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SPY | watch | 0.004% | broad-index validation exposure가 이미 있고 replacement-rank 개선이 충분하지 않다. |
| BAC | watch | 0.0195% | 금융 분산 후보지만 rate-sensitive positive thesis는 FRED macro row 실패 때문에 watch로 강등했다. |
| SMH | watch | 0.0451% | 반도체 ETF지만 AI semiconductor cluster/target-band 경고와 기존 노출 때문에 신규 add를 보류했다. |
| AAPL | blocked add | 0.0194% | validation lifecycle 1D review pending으로 추가매수 차단. |
| HOOD | watch | 0.0569% | speculative/high-beta 성격과 portfolio-construction 필터 때문에 validation buy로 승격하지 않았다. |
| AMD/AVGO/TSLA | blocked sell/trim | 6.4516% / 2.8666% / 1.0719% | sell/trim 후보로 점검했지만 spread cap 0.50% 초과 또는 active trigger 부족. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AMD | watch | spread_within_policy fail | target-band 경고권이나 thesis break/hard cap breach 없음. quote spread 6.4516%로 trim 불가. |
| TSLA | watch | spread_within_policy fail | 약세지만 thesis-break 확인 전이고 quote spread 1.0719%로 trim 불가. |
| RGTI | hold_watch | sell_trigger_none | speculative loss-control -8%에 미달해 close/trim trigger 없음. |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Post-trade reconciliation: submit attempt는 없었지만 preflight open orders 0건, positions 32건, recent activities 20건을 snapshot에 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | 주문 0건 경고만 발생 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-01-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-01-2251-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-01-2251-hourly-autopilot-post-trade.json`

## 지표 설명

- `spread_pct`: bid/ask 중간값 대비 스프레드다. 정규장 제출 상한은 `harness/risk-policy.yaml`의 0.50%다.
- `mcp_coverage`: Alpaca core와 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 확인 상태다. submit mode에서는 core pass와 research positive 3개 이상이 필요하다.
- `sell_candidate_diagnostics`: 보유 종목을 새 매수보다 먼저 점검한 결과다. trigger가 없거나 sell gate가 막으면 주문하지 않고 재점검 후보로만 남긴다.
- `validation_lifecycle`: validation buy 이후 1D/5D/20D 회고가 필요한지와 추가매수 차단 여부를 기록한다.
- `portfolio_construction_policy`: 새 매수가 기존 보유와 비교해 분산, 대체 순위, 포트폴리오 기여를 개선하는지 보는 계층이다.
