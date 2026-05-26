# 2026-05-27 02:11 KST hourly autopilot

## 요약

- 실행 모드: scheduled Alpaca paper autopilot, submit gate 검증.
- Paper mode: `.env`의 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: 2026-05-26 13:12:13 ET 기준 open, next close 16:00 ET.
- Alpaca core: pass. clock/account/open orders/positions/fills/watchlist/quote/news/asset check가 usable했다.
- First blocking gate: 없음.
- Research MCP: SEC EDGAR pass, Alpha Vantage pass, FRED preflight pass, Firecrawl wrapper_error, Yahoo Finance cancelled. Research usable count는 3개다.
- Universe gate: 62개 metadata universe와 `SPY`, `QQQ` 포함.
- 주문 계획/실행: `NOK` 1주 paper validation buy 제출, filled.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 근거 | 차단/주의 |
| ---: | --- | --- | --- | --- |
| 1 | NOK | submit candidate | Alpaca 52-week high/AI networking lab news, SEC recent 6-K, Alpha Vantage news/sentiment, FRED preflight, quote spread 0.060% | 이미 400주 보유, medium source confidence, ADR/high-volatility, Yahoo/Firecrawl gap |
| 2 | SMH | recheck | 반도체 ETF 모멘텀, fresh quote, AI semiconductor basket proxy | 기존 AMD/AVGO/LRCX/NVDA/TSM로 cluster 집중 |
| 3 | NVDA | recheck | fresh tight quote, AI semiconductor quality 후보 | 기존 보유와 반도체 cluster 집중, 신규 validation slot은 cluster 분산 우선 |
| 4 | FCX | skip | materials/mining 분산 후보 | 2026-05-26 같은 거래일에 이미 1주 buy fill |
| 5 | LLY | skip | healthcare growth 후보 | 2026-05-26 같은 거래일에 이미 1주 buy fill |

## 주문 계획

| 티커 | Side | Qty | Type | Limit | Reference | Spread | Rationale |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| NOK | buy | 1 | limit/day | 16.51 | 16.505 | 0.061% | 이미 보유 중인 NOK에 1주만 추가해 paper validation evidence를 늘린다. AI networking catalyst와 SEC/Alpha/FRED 확인은 통과했지만 breakout 직후, ADR, medium source confidence라 size는 validation floor로 제한한다. |

## 제출/스킵

- Validator: universe strict PASS, MCP strict PASS, risk policy PASS.
- Same-day fills: `LLY` 1주 buy, `FCX` 1주 buy. `NOK` same-day duplicate buy는 없다.
- `FCX`, `LLY` 추가 buy는 same-day duplicate/conflict 회피로 skip했다.
- `SMH`, `NVDA`, `AMD`, `MU`, `INTC`는 반도체 cluster 집중 때문에 이번 validation order에서 후순위로 뒀다.
- Active trim triggers: 개별 ticker 15% cap, speculative 12% cap, cash 20% floor, invested 80% cap은 현재 위반하지 않는다. thesis-break나 stale-thesis underperformance만으로 즉시 trim할 보유 종목은 없다.
- 제출: NOK 1주 day limit buy, limit 16.51, client_order_id `hourly-20260527-0211-nok-buy-1`.
- Post-trade: Alpaca order id `63e51a21-cbff-429c-82dc-9651d9756426`, status filled, filled_qty 1, filled_avg_price 16.50, filled_at `2026-05-26T17:21:49.961677153Z`.
- Reconciliation: `get_orders(status=all, symbols=NOK)`, `get_account_activities(FILL)`, and `get_all_positions`로 fill과 NOK 401주 position을 확인했다. `get_order_by_client_id`와 post-fill `get_account_info`는 wrapper cancelled였다.

## MCP Coverage

| MCP | Outcome | Used | Gap category | Note |
| --- | --- | --- | --- | --- |
| alpaca | pass | yes | not_applicable | clock/account/orders/positions/fills/quote/news/asset pass |
| sec-edgar | pass | yes | not_applicable | local CIK cache로 `NOK -> 0000924613`, company info/recent filings pass |
| alpha-vantage | pass | yes | not_applicable | TOOL_LIST/TOOL_GET(PING)/TOOL_CALL(PING)/TOOL_GET(NEWS_SENTIMENT)/TOOL_CALL(NEWS_SENTIMENT) pass |
| fred | pass | yes | not_applicable | scheduler preflight `get_macro_snapshot` pass |
| firecrawl | failed | no | wrapper_error | Codex tool catalog에 registered Firecrawl MCP tool 미노출 |
| yahoo-finance | failed | no | cancelled | registered Yahoo Finance MCP call cancelled |

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`. Risk policy의 submit 상한은 0.50%다.
- `quote_age_minutes`: 주문 제출 후보는 quote/snapshot 기준 20분 이내여야 한다.
- `first_blocking_gate`: 주문 제출을 중단시킨 첫 hard gate다. 이번 run은 없음이다.
- `research MCP confirmation`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass인 provider 수다. 이번 run은 SEC/Alpha/FRED 3개가 pass다.
- `validation floor`: paper 검증 목적의 1주 소액 주문이다. 수익 극대화가 아니라 후속 1D/5D/20D 회고용 evidence 수집이 목적이다.

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-0211-hourly-autopilot-sources.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0211-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0211-hourly-autopilot.json`
