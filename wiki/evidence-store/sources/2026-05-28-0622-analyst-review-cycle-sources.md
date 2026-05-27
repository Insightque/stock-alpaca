---
id: 2026-05-28-0622-analyst-review-cycle-sources
created_at: 2026-05-27T21:22:00Z
workflow: harness/workflows/analyst-review-cycle.md
paper: true
---

# 2026-05-28 06:22 KST analyst review cycle 원천

## 실행 범위

- 목적: paper trades, open positions, skipped recommendations, 1D/5D/20D review horizon 점검.
- 주문 관련 mutation: 없음. `place_stock_order`, `replace_order_by_id`, `cancel_order_by_id`, `cancel_all_orders`, `close_position`, `close_all_positions`는 호출하지 않았다.
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인. API key 값은 출력하거나 기록하지 않았다.

## Alpaca MCP reconciliation

사용 도구:

- `get_clock`: pass. `2026-05-27T17:22:12-04:00` 기준 market closed, next open `2026-05-28T09:30:00-04:00`.
- `get_account_info`: pass.
- `get_all_positions`: pass.
- `get_orders(status=open, asset_class=us_equity)`: pass, open orders 0건.
- `get_orders(status=closed, after=2026-05-22T00:00:00Z, asset_class=us_equity)`: pass.
- `get_account_activities(activity_types=[FILL], after=2026-05-22T00:00:00Z)`: pass.
- `get_stock_bars(..., timeframe=1Day, 2026-05-22~2026-05-27, feed=iex)`: pass.
- `get_stock_snapshot(LLY,FCX,NOK,NVDA,AAPL,NKE,PFE,SO,WMT,NEE,AMZN,BAC,XOM,V,SPY,QQQ, feed=iex)`: pass.
- `get_news(LLY,FCX,NOK,NVDA,AAPL, 2026-05-26~2026-05-27)`: pass.
- `get_portfolio_history(period=1W, timeframe=1D)`: 2회 cancelled. `gap_category=cancelled`, `retry_count=1`.

핵심 reconciliation 결과:

- Account: portfolio_value 101515.43 USD, cash 41175.98 USD, buying_power 136375.98 USD, long_market_value 60339.45 USD.
- Current positions: 22개, 모두 long US equity.
- Open orders: 0건.
- 2026-05-26 fills: LLY, FCX, NOK, NVDA, AAPL 각 1주 buy. 이번 run의 1D 회고 대상.
- 2026-05-27 fills: NKE, PFE, SO, WMT, NEE, AMZN, BAC, XOM, V 각 1주 buy. 이번 run에서는 신규 체결/대기 대상으로만 기록.
- 2026-05-27 GOOGL order: canceled, filled_qty 0. 체결 회고 대상 아님.
- 2026-05-26 AMZN order: expired, filled_qty 0. 체결 회고 대상 아님.

## Alpaca price/news observations

- 2026-05-26 close -> 2026-05-27 close: SPY 750.46 -> 750.59, +0.02%; QQQ 730.11 -> 729.48, -0.09%.
- 2026-05-26 validation 1D: LLY +0.45%, FCX -0.49%, NOK -4.97%, NVDA -0.54%, AAPL +0.48% from fill to 2026-05-27 close.
- 2026-05-27 same-day validation fills: NKE -0.39%, PFE -0.49%, SO -0.57%, WMT +0.19%, NEE +0.35%, AMZN +0.67%, BAC -1.84%, XOM +0.66%, V -0.72% from fill to 2026-05-27 close. 1D horizon은 아직 완료되지 않았다.
- Alpaca/Benzinga news examples: LLY infectious disease/vaccine pipeline M&A, NOK 52-week high/AI infrastructure, NVDA mixed AI capex/valuation/IPO competition, AAPL agentic AI valuation/analyst headline.

## SEC EDGAR MCP

사용 도구: `get_recent_filings`.

- LLY: pass. Recent Form 144 2026-05-22, 8-K 2026-05-20, Form 4 2026-05-19.
- NVDA: pass. Recent Form 144 2026-05-27, 10-Q and 8-K 2026-05-20.
- Other candidate SEC calls were not expanded in this cycle because the review target was 1D outcome quality, and prior run manifests already held submit-time SEC coverage.

## Alpha Vantage MCP

- `TOOL_LIST`: pass.
- `TOOL_GET("PING")`: pass.
- `TOOL_CALL("PING", {})`: cancelled by runtime.
- Candidate data: not called. Because the required health check did not complete, Alpha Vantage is classified as `gap_category=cancelled` for this run.

## Yahoo Finance MCP

사용 도구: `get_yahoo_finance_news`.

- LLY: pass. Yahoo headlines included obesity-pill competitive risk, Trump Q1 ownership discussion, vaccine/infectious disease buyouts, and momentum-stock framing.
- NVDA: pass. Yahoo headlines included Goldman AI winner framing, Micron/AI memory context, and broader market items.

## FRED and Firecrawl catalog status

- Codex tool catalog search did not expose registered FRED or Firecrawl MCP tools.
- Per hard requirement, no shell/curl/local wrapper probing was performed.
- FRED: `gap_category=wrapper_error`.
- Firecrawl: `gap_category=wrapper_error`.

## Local decision artifacts

- `wiki/trade-ledger/orders/2026-05-27-0052-hourly-autopilot.json`
- `wiki/trade-ledger/orders/2026-05-27-0131-hourly-autopilot.json`
- `wiki/trade-ledger/orders/2026-05-27-0211-hourly-autopilot.json`
- `wiki/trade-ledger/orders/2026-05-27-0226-hourly-autopilot.json`
- `wiki/trade-ledger/orders/2026-05-27-0251-hourly-autopilot.json`
- [[2026-05-27-portfolio-review]]
- [[recommendation-policy]]
