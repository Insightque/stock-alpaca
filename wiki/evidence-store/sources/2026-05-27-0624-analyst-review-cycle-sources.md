---
id: 2026-05-27-0624-analyst-review-cycle-sources
created_at: 2026-05-26T21:24:00Z
workflow: harness/workflows/analyst-review-cycle.md
paper: true
---

# 2026-05-27 06:24 KST analyst review cycle 원천

## 실행 범위

- 목적: paper trades, open positions, skipped recommendations, 1D/5D/20D review horizon 점검.
- 주문 관련 mutation: 없음. `place_stock_order`, `replace_order_by_id`, `cancel_order_by_id`, `cancel_all_orders`, `close_position`, `close_all_positions`는 호출하지 않았다.
- Paper mode: `.env`에서 `ALPACA_PAPER_TRADE=true` 확인. API key 값은 출력하거나 기록하지 않았다.

## Alpaca MCP reconciliation

사용 도구:

- `get_account_info`: pass.
- `get_all_positions`: pass.
- `get_orders(status=open, asset_class=us_equity)`: pass, open orders 0건.
- `get_orders(status=all, after=2026-05-22T00:00:00Z, asset_class=us_equity)`: pass, 2026-05-22 이후 stock/ETF orders 확인.
- `get_account_activities(activity_types=[FILL], after=2026-05-22T00:00:00Z)`: pass.
- `get_stock_snapshot(AAPL,AMD,AVGO,ETN,FCX,IONQ,LLY,LRCX,NOK,NVDA,RGTI,TSM,UNH,SPY,QQQ,SMH, feed=iex)`: pass.
- `get_stock_bars(..., timeframe=1Day, 2026-05-22~2026-05-27, feed=iex)`: pass.
- `get_news(..., 2026-05-22~2026-05-27)`: pass.
- `get_stock_bars(PLTR,TSLA,QBTS, timeframe=1Day, 2026-05-22~2026-05-27, feed=iex)`: pass.
- `get_portfolio_history(period=1W, timeframe=1D)`: 3회 모두 cancelled. `gap_category=cancelled`, `retry_count=2`.

핵심 reconciliation 결과:

- Account: portfolio_value 101779.63 USD, cash 42347.59 USD, buying_power 137406.46 USD, long_market_value 59432.04 USD.
- Current positions: 13개, 모두 long US equity.
- Open orders: 0건.
- AMZN order `hourly-20260527-0411-amzn-buy-1`: status `expired`, filled_qty 0, expired_at `2026-05-26T20:00:45.025036Z`.
- 2026-05-26 fills: LLY, FCX, NOK, NVDA, AAPL 각 1주 buy.
- 2026-05-22 fills: AMD, AVGO, LRCX, TSM, NOK, UNH, ETN, RGTI, IONQ, NVDA.

## Alpaca price/news observations

- 2026-05-26 daily close 기준 benchmarks: SPY 750.46, QQQ 730.11, SMH 602.09.
- 2026-05-22 close 대비 2026-05-26 close: SPY +0.64%, QQQ +1.76%, SMH +4.55%.
- Alpaca/Benzinga news examples:
  - AMD/NVDA/TSM: AI CPU, China/Huawei, AI capex, semiconductor ETF strength headlines.
  - NOK: 52-week high and AI infrastructure demand headline.
  - RGTI/IONQ: quantum rally warning and policy/valuation gap headline.
  - UNH/LLY: healthcare options/analyst/M&A headlines.

## SEC EDGAR MCP

사용 도구: `get_recent_filings`.

- NVDA: pass. Recent 10-Q and 8-K filed 2026-05-20, acceptance times `2026-05-20T20:35:52+00:00` and `2026-05-20T20:21:19+00:00`.
- UNH: pass. Recent DEFA14A 2026-05-15, 8-K 2026-05-11, 10-Q 2026-05-05.
- RGTI: pass. Recent Form 4 and Form 144 filings on 2026-05-22 and 2026-05-26; several acceptance times occurred after the 2026-05-22 recommendation, so they are review-only evidence.
- LLY: pass. Recent Form 144, 8-K, and Form 4 filings from 2026-05-19~2026-05-22.
- AMD: registered MCP call was cancelled by runtime safety guard while querying `get_recent_filings`; recorded as `gap_category=cancelled`. No shell/curl fallback used.

## Alpha Vantage MCP

Required health sequence:

- `TOOL_LIST`: pass.
- `TOOL_GET("PING")`: pass.
- `TOOL_CALL("PING", {})`: pass, returned `pong`.
- Candidate data: `TOOL_GET("NEWS_SENTIMENT")` pass, then first non-PING `TOOL_CALL("NEWS_SENTIMENT", {tickers: "AMD,NVDA,NOK,UNH,RGTI", ...})` was cancelled by the tool runtime. Per hard requirement, Alpha retries stopped and `alpha-vantage` is classified as `gap_category=cancelled`.

## Yahoo Finance MCP

사용 도구: `get_recommendations`, `get_yahoo_finance_news`.

- AMD recommendations: pass. Current row: strongBuy 5, buy 36, hold 10, sell 0, strongSell 0.
- NOK recommendations: pass. Current row: strongBuy 4, buy 4, hold 2, sell 1, strongSell 0.
- UNH recommendations: pass. Current row: strongBuy 6, buy 16, hold 5, sell 1, strongSell 0.
- RGTI recommendations: pass. Current row: strongBuy 1, buy 8, hold 3, sell 1, strongSell 0.
- NOK news: pass. Yahoo/Trefis/Bloomberg headlines emphasized AI infrastructure demand, Nvidia partnership, AI networking lab, and valuation puzzle.
- NVDA recommendations call was cancelled by runtime safety guard; recorded as `gap_category=cancelled`.

## FRED and Firecrawl catalog status

- Codex tool catalog search for FRED/Firecrawl returned 0 exposed tools.
- Per hard requirement, no shell/curl/local wrapper probing was performed.
- FRED: `gap_category=wrapper_error`.
- Firecrawl: `gap_category=wrapper_error`.

## Local decision artifacts

- [[2026-05-22]]
- [[2026-05-22-stock-only-trade-proposal]]
- `wiki/trade-ledger/orders/2026-05-22-stock-only-proposal.json`
- Current ticker notes under `wiki/research-notes/tickers/`
- [[recommendation-policy]]

