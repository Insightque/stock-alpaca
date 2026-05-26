# 2026-05-27 01:31 KST hourly autopilot sources

## 실행 조건

- 실행 시각: 2026-05-27 01:31 KST / 2026-05-26 12:31 ET.
- `.env` 확인: `ALPACA_PAPER_TRADE=true`. API key 값은 출력하거나 기록하지 않았다.
- Shell 환경 변수는 export되어 있지 않았지만, workflow의 paper-mode source인 `.env`에 true가 있어 진행했다.
- Firecrawl: Codex tool catalog에서 registered Firecrawl MCP tool이 노출되지 않았다. workflow 지시에 따라 `scripts/mcp-firecrawl.sh`, curl, local network helper는 호출하지 않았다.
- FRED: scheduler-owned preflight `wiki/evidence-store/sources/2026-05-27-0131-hourly-autopilot-research-mcp-preflight.json`를 사용했다. `fred` provider row는 `outcome=pass`, `tool=get_macro_snapshot`이다.

## Alpaca MCP core

- `get_clock`: pass. `timestamp=2026-05-26T12:32:08.495972825-04:00`, `is_open=true`, `next_close=2026-05-26T16:00:00-04:00`, `next_open=2026-05-27T09:30:00-04:00`.
- `get_account_info`: pass. `status=ACTIVE`, `portfolio_value=101605.13`, `cash=42951.20`, `buying_power=137932.33`, `trading_blocked=false`, `account_blocked=false`.
- `get_orders(status=open, asset_class=us_equity)`: pass. Open US equity orders 0건.
- `get_all_positions`: pass. Long positions 11개: AMD, AVGO, ETN, IONQ, LLY, LRCX, NOK, NVDA, RGTI, TSM, UNH. Short positions 없음.
- `get_account_activities(activity_types=FILL, date=2026-05-26)`: pass. Same-day fill 1건: LLY buy 1주, `filled_avg_price=1079.38`, `order_id=f2626164-9d01-4134-97ab-5e73748fc790`.
- `get_watchlists`: pass. Account watchlists 0건.
- `get_most_active_stocks`: pass. NOK가 volume most active 목록에 포함됐다.
- `get_market_movers`: pass. Broad market movers는 저가/워런트성 종목이 많아 추천 후보에는 직접 반영하지 않았다.

## Universe and market data

- Universe source: `harness/symbol-metadata.yaml` 62개 symbol, 현재 보유 11개, Alpaca watchlists 0개, benchmarks `SPY`, `QQQ`.
- Symbols loaded: 62/62.
- Screening method: 62개 broad metadata universe의 snapshot/daily bar/quote를 확인하고, fresh quote, spread, 당일/20거래일 가격 모멘텀, 보유/클러스터 한도, source confidence를 사용해 pre-MCP shortlist를 만들었다.
- Pre-MCP shortlist: `MU`, `NOK`, `FCX`, `SMH`, `AMD`, `INTC`, `AAPL`, `AVGO`, `PLTR`, `NVDA`.
- Final candidates: `FCX`, `NOK`, `SMH`.
- Benchmarks: `SPY`, `QQQ` 모두 포함.

### Candidate quotes

| Symbol | Bid | Ask | Mid | Spread % | Quote time | Gate |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| FCX | 64.09 | 64.12 | 64.105 | 0.047 | 2026-05-26T16:33:41.974817327Z | pass |
| NOK | 16.52 | 16.53 | 16.525 | 0.061 | 2026-05-26T16:33:43.862327118Z | pass |
| SMH | 597.06 | 597.38 | 597.22 | 0.054 | 2026-05-26T16:33:43.870595087Z | pass |
| MU | 883.89 | 887.00 | 885.445 | 0.351 | 2026-05-26T16:33:43.924775578Z | pass, but overheat/semiconductor concentration caution |
| AMD | 470.62 | 498.00 | 484.31 | 5.653 | 2026-05-26T16:33:43.497225939Z | spread fail |
| LLY | 1080.61 | 1134.00 | 1107.305 | 4.822 | 2026-05-26T16:33:40.787404513Z | spread fail for new add |
| AAPL | 310.52 | 310.56 | 310.54 | 0.013 | 2026-05-26T16:33:44.057623155Z | pass, lower current catalyst |
| NVDA | 213.30 | 213.33 | 213.315 | 0.014 | 2026-05-26T16:33:43.913251834Z | pass, already held/cluster concentration |
| AVGO | 422.65 | 422.79 | 422.72 | 0.033 | 2026-05-26T16:33:43.168214638Z | pass, already held |
| INTC | 121.64 | 121.67 | 121.655 | 0.025 | 2026-05-26T16:33:44.091309516Z | pass, source confidence lower than FCX |
| PLTR | 137.16 | 137.20 | 137.18 | 0.029 | 2026-05-26T16:33:44.07636756Z | pass, speculative growth caution |

## Alpaca asset/news

- `get_asset(FCX)`: first attempt cancelled, retry pass. `class=us_equity`, `exchange=NYSE`, `status=active`, `tradable=true`, `symbol=FCX`, `name=Freeport-McMoran Inc.`
- `get_news(FCX,NOK,SMH,MU,AMD,LLY,AAPL,NVDA,AVGO,ETN,PLTR,HOOD,INTC)`: pass. Recent relevant items included:
  - NOK: "Nokia Stock Rallies To New 52-Week High: What's Driving The Action?"
  - MU/NVDA/AMD/INTC: multiple AI semiconductor analyst/news items.
  - PLTR: Ondas/defense software acquisition related item.
  - FCX-specific Alpaca headline was not in the first 20 returned items, so FCX catalyst confirmation used Yahoo Finance.

## SEC EDGAR MCP

- Local CIK fallback before MCP lookup: `harness/sec-ticker-cik-map.json` maps `FCX -> 0000831259` (`FREEPORT-MCMORAN INC`).
- `get_company_info(identifier=0000831259)`: pass. CIK 831259, name FREEPORT-MCMORAN INC, ticker FCX, fiscal year end 1231.
- `get_recent_filings(identifier=0000831259, days=30, limit=5)`: pass. Recent filings included:
  - `0000831259-26-000027`, 8-K, filing date 2026-05-20, period 2026-05-14.
  - `0000831259-26-000025`, 10-Q, filing date 2026-05-08, period 2026-03-31.

## Yahoo Finance MCP

- `get_yahoo_finance_news(FCX)`: pass. Returned FCX-specific news:
  - "FCX Leads Metal And Mining Stocks Near Buy Points On Peace Hopes"
  - "Barclays Initiates Coverage of Freeport-McMoRan (FCX) with Overweight Rating"
  - "How The Freeport-McMoRan (FCX) Story Is Shifting With New Copper Views And Targets"
  - "What Freeport-McMoRan (FCX)'s New US$3 Billion Credit Facility Means For Shareholders"
- `get_recommendations(FCX)`: attempted after the news call but cancelled by MCP wrapper. Yahoo was still usable because the news call returned FCX-specific evidence.

## Alpha Vantage MCP

- Required health sequence followed:
  - `TOOL_LIST`: pass.
  - `TOOL_GET("PING")`: pass.
  - `TOOL_CALL("PING", {})`: cancelled.
- Per workflow instruction, after the cancelled `PING` call no further Alpha Vantage candidate functions were attempted. Coverage row uses `outcome=failed`, `gap_category=cancelled`, `retry_count=0`.

## FRED

- Used scheduler preflight only: `wiki/evidence-store/sources/2026-05-27-0131-hourly-autopilot-research-mcp-preflight.json`.
- Passing macro evidence included DGS10 4.57, DGS2 4.08, FEDFUNDS 3.64, CPIAUCSL 332.407, UNRATE 4.3, NFCI -0.52300.

## Firecrawl

- Codex tool catalog search did not expose a Firecrawl MCP namespace/tool.
- Classified as `gap_category=wrapper_error`; no shell/curl/local wrapper retry was used.

## 주문 판단 근거

- FCX buy rationale: unheld active/tradable NYSE equity, fresh quote, 0.047% spread, current price above 2026-05-22 close and recovering from 5월 중순 pullback, Yahoo FCX-specific copper/mining and analyst context, SEC recent 8-K/10-Q evidence, FRED macro preflight pass. Commodity cyclicality and macro sensitivity keep size at one share only.
- NOK recheck rationale: strong price/news momentum and most-active confirmation, but already held 400 shares and adding would raise single-name and communications-infrastructure exposure without better diversification than FCX.
- SMH recheck rationale: broad semiconductor ETF momentum and clean spread, but current portfolio already has high semiconductor complex exposure through AMD, AVGO, LRCX, NVDA, and TSM.
- No sell/trim rationale passed: no thesis-break, risk-limit breach, stale-thesis trigger, position-sizing breach, portfolio-fit trim, speculative cap breach, cluster cap breach, theme/factor breach, or overheat profit-protection trigger was strong enough for a paper sell order.

## Pre-submit refresh

- `get_clock`: pass. `timestamp=2026-05-26T12:40:50.822522943-04:00`, `is_open=true`.
- `get_orders(status=open, asset_class=us_equity)`: pass. Open US equity orders 0건.
- `get_stock_latest_quote(FCX)`: pass. `bid=63.95`, `ask=63.97`, midpoint 63.96, spread 0.031%, quote time `2026-05-26T16:40:36.660525545Z`.
- Order plan was updated to the refreshed quote before final risk validation and submission.

## Submission and post-trade reconciliation

- `place_stock_order(FCX buy 1 limit day, client_order_id=hourly-20260527-0131-fcx-buy-1)`: pass. Alpaca order id `6c6a31ab-2a07-4da1-9e2e-c1dfb57ccee1`, initial status `pending_new`, submitted at `2026-05-26T16:41:44.072749206Z`, limit 63.97.
- `get_order_by_client_id`: two attempts cancelled by MCP wrapper.
- `get_order_by_id`: cancelled by MCP wrapper.
- `get_orders(status=all, symbols=FCX)`: first attempt cancelled, retry pass. Order `6c6a31ab-2a07-4da1-9e2e-c1dfb57ccee1` status `filled`, `filled_qty=1`, `filled_avg_price=63.94`, `filled_at=2026-05-26T16:41:44.795047598Z`.
- `get_all_positions`: first reconciliation attempt cancelled, retry pass. FCX position present: qty 1, avg entry 63.94, current price 63.935, market value 63.935.
- `get_account_info`: pass after fill. Portfolio value 101535.19, cash 42887.26, buying power 137824.45, long market value 58647.93.
- `get_account_activities(activity_types=FILL, date=2026-05-26)`: cancelled by MCP safety wrapper during post-trade reconciliation. Fill evidence therefore uses order endpoint and position endpoint.
