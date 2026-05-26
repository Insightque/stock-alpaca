# 2026-05-27 02:26 KST hourly autopilot

## 요약

- 실행 모드: scheduled Alpaca paper autopilot, submit gate 검증.
- Paper mode: `.env`의 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: 2026-05-26 13:26:42 ET 기준 open, next close 16:00 ET.
- Alpaca core: pass. Scheduler-owned preflight의 clock/account/open orders/positions/fills/watchlist/asset/quote/snapshot/latest trade가 usable했다.
- First blocking gate: 없음.
- Research MCP: SEC EDGAR pass, FRED preflight pass, Yahoo Finance pass, Alpha Vantage cancelled, Firecrawl wrapper_error. Research usable count는 3개다.
- Universe gate: 62개 metadata universe와 `SPY`, `QQQ` 포함.
- 주문 계획/실행: `NVDA` 1주 paper validation buy 제출, filled.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 근거 | 차단/주의 |
| ---: | --- | --- | --- | --- |
| 1 | NVDA | submit candidate | fresh quote, spread 0.112%, SEC 10-Q/8-K recent filing 확인, Yahoo recommendation/news pass, FRED macro preflight pass | 이미 35주 보유, AI semiconductor cluster 집중. 그래서 1주 validation size만 허용 |
| 2 | SMH | recheck | 반도체 ETF momentum과 spread 0.050% | ETF라 SEC/issuer 확인은 더 느슨하지만 기존 반도체 cluster 집중이 큼 |
| 3 | AAPL | recheck | spread 0.019%, mega-cap quality 분산 후보 | 이번 run의 최상위 momentum/AI thesis는 NVDA가 더 강함 |
| 4 | INTC | recheck | spread 0.033%, 반도체 laggard 회복 후보 | high-volatility, thesis confidence가 NVDA보다 낮음 |
| 5 | MU | skip | 강한 당일 momentum | spread 0.846%로 risk policy 상한 0.50% 초과 |

## 주문 계획

| 티커 | Side | Qty | Type | Limit | Reference | Spread | Rationale |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| NVDA | buy | 1 | limit/day | 213.72 | 213.60 | 0.112% | NVDA는 기존 보유 종목이지만 ticker cap과 AI semiconductor cluster cap 아래에 있고, 2026-05-20 10-Q/8-K, Yahoo analyst/news, FRED macro preflight가 같은 방향의 research confirmation을 제공한다. 같은 거래일 신규 buy가 없으며 1주만 추가해 paper validation evidence를 늘린다. |

## 제출/스킵

- Validator: universe strict PASS, MCP strict PASS, risk policy PASS.
- Same-day fills: `LLY`, `FCX`, `NOK` 각 1주 buy. 해당 종목 추가 buy는 same-day duplicate/conflict 회피로 skip했다.
- `SMH`, `AAPL`, `INTC`는 recheck 후보로 유지한다.
- `MU`는 spread fail로 skip했다.
- Active trim triggers: 개별 ticker 15% cap, speculative 12% cap, cash 20% floor, invested 80% cap은 현재 위반하지 않는다. thesis-break나 stale-thesis underperformance만으로 즉시 trim할 보유 종목은 없다.
- 제출: NVDA 1주 day limit buy, limit 213.72, client_order_id `hourly-20260527-0226-nvda-buy-1`.
- Post-trade: Alpaca order id `e4c49769-2341-404e-8ee9-15a20809bdfd`, status filled, filled_qty 1, filled_avg_price 213.72, filled_at `2026-05-26T17:34:00.662457Z`.
- Reconciliation: `get_orders(status=all, symbols=NVDA)`로 같은 client_order_id/order_id의 fill을 확인했고, `get_orders(status=open)`은 open orders 0건을 반환했다. `get_order_by_client_id`, post-fill `get_all_positions`, post-fill `get_account_activities`는 wrapper cancelled로 기록했다.

## MCP Coverage

| MCP | Outcome | Used | Gap category | Note |
| --- | --- | --- | --- | --- |
| alpaca | pass | yes | not_applicable | scheduler preflight hard gate pass, quotes <20분 |
| sec-edgar | pass | yes | not_applicable | local CIK cache로 `NVDA -> 0001045810`, company info/recent filings pass |
| alpha-vantage | failed | no | cancelled | `TOOL_CALL("PING", {})` cancelled 후 후보 데이터 호출 중단 |
| fred | pass | yes | not_applicable | scheduler preflight `get_macro_snapshot` pass |
| firecrawl | failed | no | wrapper_error | Codex tool catalog에 registered Firecrawl MCP tool 미노출 |
| yahoo-finance | pass | yes | not_applicable | NVDA news/recommendations pass |

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`. Risk policy의 submit 상한은 0.50%다.
- `quote_age_minutes`: 주문 제출 후보는 quote/snapshot 기준 20분 이내여야 한다.
- `first_blocking_gate`: 주문 제출을 중단시킨 첫 hard gate다. 이번 run은 없음이다.
- `research MCP confirmation`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass인 provider 수다. 이번 run은 SEC/FRED/Yahoo 3개가 pass다.
- `validation floor`: paper 검증 목적의 1주 소액 주문이다. 수익 극대화가 아니라 후속 1D/5D/20D 회고용 evidence 수집이 목적이다.

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-0226-hourly-autopilot-sources.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0226-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0226-hourly-autopilot.json`

## 회고 대기

- 신규 NVDA fill은 1D/5D/20D `회고 대기`다.
- LLY/FCX/NOK 및 2026-05-22 체결분도 계속 `회고 대기`다.
