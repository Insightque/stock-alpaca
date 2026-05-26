---
id: 2026-05-27-0211-hourly-autopilot-sources
created_at: 2026-05-26T17:17:03Z
paper: true
run_id: 2026-05-27-0211-hourly-autopilot
---

# 2026-05-27 02:11 KST hourly autopilot sources

## Alpaca MCP

- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했다. API key 값은 출력하거나 기록하지 않았다.
- `get_clock`: 2026-05-26T13:12:13.814059747-04:00 기준 `is_open=true`, next close 2026-05-26T16:00:00-04:00.
- `get_account_info`: account `ACTIVE`, trading blocked false, portfolio value 101680.85 USD, cash 42887.26 USD, buying power 137946.11 USD, long market value 58793.59 USD.
- `get_orders(status=open, asset_class=us_equity)`: `[]`.
- `get_all_positions`: 12개 long US equity positions. 주요 보유: NOK 400주, LLY 1주, FCX 1주, AMD/AVGO/LRCX/NVDA/TSM 반도체 cluster, RGTI/IONQ speculative quantum.
- `get_account_activities(activity_types=FILL, after=2026-05-26T00:00:00Z)`: LLY buy 1주 fill at 1079.38, FCX buy 1주 fill at 63.94.
- `get_watchlists`: empty.
- `get_stock_bars(62-symbol metadata universe, 1Day, 90d, IEX, adjusted)`: 62개 metadata universe와 SPY/QQQ broad screen에 사용했다.
- `get_stock_latest_quote(NOK,SMH,FCX,NVDA,AAPL,INTC,MU,LLY,AVGO,PLTR,AMD,LRCX,ETN,RGTI,IONQ,SPY,QQQ, IEX)`: 2026-05-26T17:13:35Z~17:13:41Z quote. NOK bid 16.54, ask 16.55, spread 약 0.0604%.
- Pre-submit refresh: `get_clock` at 2026-05-26T13:20:55.139534731-04:00 still open, `get_orders(status=open, asset_class=us_equity)` still `[]`, and `get_stock_latest_quote(NOK, IEX)` returned bid 16.50, ask 16.51, spread 약 0.0606%, quote time 2026-05-26T17:20:40.787261576Z.
- `get_asset(NOK)`: Nokia Corporation, class `us_equity`, exchange NYSE, status active, tradable true, marginable true, fractionable true. Order plan uses whole-share only.
- `get_news(NOK, 2026-05-20..2026-05-26T17:14Z)`: Benzinga 2026-05-26 headline says NOK reached a new 52-week high; 2026-05-21 item says Nokia launched an AI Networking Innovation Lab with partners including AMD and Keysight; 2026-05-20 item says FCC approval supported US broadband device deployment momentum.

## Research MCP

- SEC EDGAR: local `harness/sec-ticker-cik-map.json` cache resolved `NOK -> 0000924613`. `get_company_info(0000924613)` pass: NOKIA CORP, CIK 924613, SIC 3663. `get_recent_filings(0000924613, days=30, limit=5)` pass: recent 6-K filings on 2026-05-26, 2026-05-20, 2026-05-18, 2026-05-13 and SD on 2026-05-21.
- Alpha Vantage: `TOOL_LIST` pass, `TOOL_GET("PING")` pass, `TOOL_CALL("PING", {})` returned `pong`. `TOOL_GET("NEWS_SENTIMENT")` immediately preceded `TOOL_CALL("NEWS_SENTIMENT", {"tickers":"NOK","time_from":"20260520T0000","limit":5,"sort":"LATEST"})`. Candidate call pass with 6 items, including Stock Titan/SEC filing coverage of a Nokia senior manager share purchase, Finviz/TradingKey bullish AI networking context, and MarketWatch/price-momentum items. This was used as research confirmation.
- FRED: scheduler preflight `wiki/evidence-store/sources/2026-05-27-0211-hourly-autopilot-research-mcp-preflight.json` existed and included provider row `fred`, `outcome=pass`, `tool=get_macro_snapshot`; counted as usable macro evidence. Latest preflight values included DGS10 4.57, DGS2 4.08, FEDFUNDS 3.64, CPIAUCSL 332.407, UNRATE 4.3, NFCI -0.52300.
- Firecrawl: Codex tool catalog search did not expose a registered Firecrawl MCP tool. Per workflow, no shell/curl/local wrapper was called. Gap category `wrapper_error`.
- Yahoo Finance: registered MCP `get_yahoo_finance_news(NOK)` was attempted and cancelled by the MCP wrapper. Gap category `cancelled`; no retry was used because the cancellation was a wrapper safety cancellation rather than provider data.

## Candidate Rationale Inputs

- Pre-MCP shortlist: NOK, SMH, FCX, NVDA, AAPL, AMD, MU, INTC, LLY, PLTR.
- Final candidates: NOK, SMH, NVDA. FCX and LLY were excluded from submit consideration because same-day buy fills already existed. SMH/NVDA were de-emphasized because the account already has large AI semiconductor cluster exposure.
- NOK buy thesis: fresh tight quote, active/tradable NYSE ADR, positive current Alpaca news around 52-week high and AI networking lab, SEC filing recency, Alpha Vantage news/sentiment confirmation, FRED macro preflight pass, and non-semiconductor communications infrastructure diversification.
- NOK risks: already held 400 shares, medium source confidence, high volatility bucket, ADR/international factor, rapid post-breakout move may reverse, and Yahoo/Firecrawl gaps reduce source breadth.

## Execution And Reconciliation

- Pre-submit summary was written before the order call: paper mode true, market open, order plan path, universe/MCP/risk PASS, fresh NOK quote/spread, whole-share day limit order, no open US equity orders, no same-day NOK buy, and source refs.
- `place_stock_order(NOK buy 1 limit 16.51 day, client_order_id=hourly-20260527-0211-nok-buy-1)` returned order id `63e51a21-cbff-429c-82dc-9651d9756426`, initial status `pending_new`.
- `get_order_by_client_id(hourly-20260527-0211-nok-buy-1)` was cancelled by the wrapper, gap category `cancelled`.
- `get_orders(status=all, symbols=NOK)` confirmed the same client order id filled: filled qty 1, filled avg price 16.50, filled at 2026-05-26T17:21:49.961677153Z.
- `get_account_activities(activity_types=FILL, after=2026-05-26T17:20:00Z)` confirmed fill row for NOK buy 1 at 16.50, order id `63e51a21-cbff-429c-82dc-9651d9756426`.
- `get_all_positions` first retry was cancelled, then pass; NOK position is now 401 shares, avg entry 15.043641, market value 6614.495, unrealized P/L 581.994959.
- Post-fill `get_account_info` was attempted twice and cancelled by the wrapper; position and order/fill endpoints confirmed execution state.
