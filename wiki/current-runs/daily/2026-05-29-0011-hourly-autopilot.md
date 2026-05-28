# 2026-05-29-0011-hourly-autopilot scheduled paper autopilot

## 요약

- Paper mode: `ALPACA_PAPER_TRADE=true`. 정규장 clock은 `2026-05-28T11:11:17.646180689-04:00` 기준 open=true이고, 계획 생성 시각은 `2026-05-28T15:13:38Z`이다.
- Scheduler stale cleanup: `wiki/evidence-store/sources/2026-05-29-0011-hourly-autopilot-stale-order-cleanup.json` status=`pass`. Fresh AAPL open buy가 남아 있지만 stale 후보가 아니며 age가 13.21분으로 lifecycle 한도 30분 안이다. 새 주문은 AAPL 및 같은 mega-cap tech cluster를 피했다.
- Alpaca core gate: PASS. scheduler core preflight의 clock/account/positions/orders/activities/assets/quotes/snapshots/trades가 모두 pass이고 quote row는 20분 freshness 한도 안이다.
- Research MCP gate: SEC EDGAR, FRED, Firecrawl, Yahoo Finance PASS; Alpha Vantage는 `empty_response` gap. 4개 usable/pass로 submit 기준 3개를 충족했다.
- 계획 결과: SPY, BAC, NEE 각 1주 regular-session day limit paper validation buy 후보.

## 후보 및 주문 계획

| Symbol | Action | Qty | Limit | Spread % | 근거 |
| --- | --- | ---: | ---: | ---: | --- |
| SPY | buy | 1 | 753.38 | 0.0040 | S&P 500 broad-index ETF 1주 검증. AAPL fresh open order와 다른 broad_index cluster이고, 특정 단일 테마 집중을 키우지 않으면서 정규장 베타를 관찰한다. |
| BAC | buy | 1 | 51.17 | 0.0195 | 대형 은행/financials 1주 검증. 금리 민감 금융 노출은 현재 포트폴리오에서 작고, AAPL open mega-cap cluster와 겹치지 않아 분산 관찰 가치가 있다. |
| NEE | buy | 1 | 87.83 | 0.0228 | Utilities/renewable power 1주 검증. AAPL open mega-cap tech cluster와 겹치지 않고, AI semiconductor 및 고베타 성장주 집중을 늘리지 않는 방어적 전력 노출이다. |

## 게이트

- Universe strict: PASS. 62개 metadata universe, SPY/QQQ 포함, pre-MCP shortlist 10개, final candidates 3개.
- MCP strict: PASS. Alpaca core PASS + research usable/pass 4개. Alpha Vantage gap은 `empty_response`로 기록하고 점수에는 미사용.
- Quote freshness/spread: PASS. SPY 1.97분/0.004%, BAC 2.01분/0.0195%, NEE 1.98분/0.0228%.
- Open-order lifecycle: PASS. 남은 open order는 AAPL hourly-20260528-2351-aapl-buy-01 age 13.21m; stale cleanup이 취소 실패를 남기지 않았고 계획은 동일 symbol/side 및 같은 correlated-cluster 추가 매수를 피했다.
- Risk validator: PASS. Buy notional 892.38달러, post-cash 38,375.40달러, post-invested 63,731.11달러로 medium-risk-v1.1 한도 안이다. Daily submitted-before-run은 12건이고 계획 3건 포함 15건은 daily cap 20건 안이다.

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | source_refs |
| --- | --- | --- | --- | --- | --- |
| alpaca | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-29-0011-hourly-autopilot-alpaca-core-preflight.json |
| sec-edgar | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-29-0011-hourly-autopilot-research-mcp-preflight.json |
| alpha-vantage | true | false | gap | empty_response | wiki/evidence-store/sources/2026-05-29-0011-hourly-autopilot-research-mcp-preflight.json |
| fred | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-29-0011-hourly-autopilot-research-mcp-preflight.json |
| firecrawl | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-29-0011-hourly-autopilot-research-mcp-preflight.json |
| yahoo-finance | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-29-0011-hourly-autopilot-research-mcp-preflight.json |

## 제출 및 사후 점검

| Symbol | Client order id | Status | Filled qty | Fill price | 비고 |
| --- | --- | --- | ---: | ---: | --- |
| SPY | `hourly-20260529-0011-spy-buy-01` | filled | 1 | 753.38 | Alpaca MCP accepted; reconciliation fill 확인 |
| BAC | `hourly-20260529-0011-bac-buy-01` | filled | 1 | 51.14 | Alpaca MCP accepted; reconciliation fill 확인 |
| NEE | `hourly-20260529-0011-nee-buy-01` | new/open | 0 |  | Alpaca MCP accepted; open-order lifecycle follow-up 필요 |

- Post-trade reconciliation: client-order-id checks completed for SPY/BAC/NEE, open orders PASS with NEE and prior AAPL open, FILL activities show SPY/BAC fills, positions refresh PASS, account refresh PASS.
- Review due: SPY/BAC `회고 대기`; NEE/AAPL open-order lifecycle follow-up 필요.

## 지표 설명

- `spread_pct`: Alpaca latest quote의 bid/ask 중간값 대비 스프레드. 0.50% 이하여야 제출 가능하다.
- `quote_age_minutes`: 주문 계획 생성 시점 기준 quote 경과 시간. 정책상 20분 이하여야 한다.
- `research confirmations`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass로 확인된 provider 수. Buy 제출은 3개 이상이 필요하다.
- `risk_open_order_lifecycle`: stale unfilled autopilot order가 취소 또는 조정되지 않아 새 주문을 막는 상태. 이번 run에서는 fresh AAPL open order만 있어 AAPL과 같은 cluster 추가를 피했다.
