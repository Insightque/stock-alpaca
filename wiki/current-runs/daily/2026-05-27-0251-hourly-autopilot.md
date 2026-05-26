# 2026-05-27 02:51 KST hourly autopilot

## 요약

- 실행 모드: scheduled Alpaca paper autopilot, submit gate 검증.
- Paper mode: `.env`의 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: 2026-05-26 13:58:37 ET refresh 기준 open, next close 16:00 ET.
- Alpaca core: pass. Scheduler-owned preflight의 clock/account/open orders/positions/fills/watchlist/asset/quote/snapshot/latest trade가 usable했고, AAPL quote는 Alpaca MCP로 17:56:03Z에 재조회했으며 clock도 17:58:37Z에 재조회했다.
- First blocking gate: 없음.
- Research MCP: SEC EDGAR pass, FRED preflight pass, Yahoo Finance pass, Alpha Vantage cancelled, Firecrawl wrapper_error. Research usable count는 3개다.
- Universe gate: 62개 metadata universe와 `SPY`, `QQQ` 포함.
- 주문 계획/실행: `AAPL` 1주 paper validation buy 제출. 첫 submit call은 cancelled였고, same client id reconciliation 후 같은 client id로 1회 재시도했다. Retry order는 open `new`, 아직 미체결이다.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 근거 | 차단/주의 |
| ---: | --- | --- | --- | --- |
| 1 | AAPL | submit candidate | refreshed quote, spread 0.0097%, SEC company/recent filing 확인, Yahoo news/recommendation pass, FRED macro preflight pass | 당일 momentum은 반도체보다 낮아 1주 validation size만 허용 |
| 2 | SMH | recheck | 반도체 ETF momentum과 spread 0.043% | 기존 AI semiconductor cluster 집중이 큼 |
| 3 | INTC | recheck | spread 0.114%, AI capex/semiconductor news 노출 | high-volatility laggard 성격, confidence가 AAPL보다 낮음 |
| 4 | AMZN | recheck | mega-cap quality 분산 후보, spread 양호 | 이번 run에서는 AAPL의 SEC/Yahoo confirmation이 더 직접적 |
| 5 | MU | skip | 강한 당일 momentum | spread 0.765%로 risk policy 상한 0.50% 초과 |

## 주문 계획

| 티커 | Side | Qty | Type | Limit | Reference | Spread | Rationale |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| AAPL | buy | 1 | limit/day | 309.46 | 309.445 | 0.0097% | AAPL은 active/tradable US equity이고 같은 거래일 buy 중복이 없다. SEC 최근 10-Q/Form 4, Yahoo AI strategy/news와 analyst recommendation, FRED macro preflight가 최소 research confirmation 3개를 충족한다. 반도체 cluster 추가가 아니라 mega-cap quality/AI optionality 관찰용 1주 validation order라 cluster 분산에도 낫다. |

## 제출/스킵

- Validator: universe strict PASS, MCP strict PASS, risk policy PASS.
- Same-day fills: `LLY`, `FCX`, `NOK`, `NVDA` 각 buy. 해당 종목 추가 buy는 same-day duplicate/conflict 회피로 skip했다.
- `SMH`, `INTC`, `AMZN`은 recheck 후보로 유지한다.
- `MU`는 spread fail로 skip했다.
- Active trim triggers: 개별 ticker 15% cap, speculative 12% cap, cash 20% floor, invested 80% cap은 현재 위반하지 않는다. thesis-break나 stale-thesis underperformance만으로 즉시 trim할 보유 종목은 없다.
- 제출: AAPL 1주 day limit buy, limit 309.46, client_order_id `hourly-20260527-0251-aapl-buy-1`.
- Submit retry: 첫 `place_stock_order` call은 cancelled였다. `get_orders(status=all, symbols=AAPL)`와 `get_all_positions`에서 같은 client id/order/position이 없음을 확인한 뒤 같은 client id로 한 번 재시도했다.
- Post-trade: Alpaca order id `dda2173a-f512-4ee1-80a9-7e99a4bdfd7c`, status `new`, filled_qty 0, submitted_at `2026-05-26T18:00:09.297012573Z`.
- Reconciliation: `get_orders(status=all, symbols=AAPL)` 및 `get_orders(status=open, symbols=AAPL)`에서 same client_order_id의 open order를 확인했다. `get_account_activities(FILL, after=17:55Z)`는 신규 fill 0건, `get_all_positions`는 AAPL position 없음이다. Post-submit `get_account_info`는 MCP wrapper safety cancellation으로 `gap_category=cancelled` 기록했다.

## MCP Coverage

| MCP | Outcome | Used | Gap category | Note |
| --- | --- | --- | --- | --- |
| alpaca | pass | yes | not_applicable | scheduler preflight hard gate pass, AAPL quote refresh <20분 |
| sec-edgar | pass | yes | not_applicable | local CIK cache로 `AAPL -> 0000320193`, company info/recent filings pass |
| alpha-vantage | failed | no | cancelled | health check pass 후 `TOOL_GET("NEWS_SENTIMENT")` cancelled, 후보 데이터 호출 중단 |
| fred | pass | yes | not_applicable | scheduler preflight `get_macro_snapshot` pass |
| firecrawl | failed | no | wrapper_error | Codex tool catalog에 registered Firecrawl MCP tool 미노출 |
| yahoo-finance | pass | yes | not_applicable | AAPL news/recommendations pass |

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`. Risk policy의 submit 상한은 0.50%다.
- `quote_age_minutes`: 주문 제출 후보는 quote/snapshot 기준 20분 이내여야 한다.
- `first_blocking_gate`: 주문 제출을 중단시킨 첫 hard gate다. 이번 run은 없음이다.
- `research MCP confirmation`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass인 provider 수다. 이번 run은 SEC/FRED/Yahoo 3개가 pass다.
- `validation floor`: paper 검증 목적의 1주 소액 주문이다. 수익 극대화가 아니라 후속 1D/5D/20D 회고용 evidence 수집이 목적이다.

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-0251-hourly-autopilot-sources.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0251-hourly-autopilot.json`

## 회고 대기

- AAPL order는 open `new` 상태라 체결 회고는 아직 생성하지 않는다. 체결되면 1D/5D/20D `회고 대기`로 기록한다.
- LLY/FCX/NOK/NVDA 및 2026-05-22 체결분도 계속 `회고 대기`다.
