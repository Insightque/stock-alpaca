---
id: 2026-05-29-0625-analyst-review-cycle-sources
created_at: 2026-05-29T06:25:00+09:00
workflow: analyst-review-cycle
paper: true
---

# 2026-05-29 analyst review cycle sources

## MCP reconciliation

- Paper mode: local environment `ALPACA_PAPER_TRADE=true`.
- Alpaca account: `get_account_info` PASS at runtime. Account status `ACTIVE`, portfolio value 102374.13, cash 37187.61, buying power 133318.68, long market value 65186.52.
- Alpaca clock: `get_clock` PASS. Timestamp `2026-05-28T17:21:29.381974951-04:00`, market open `false`, next open `2026-05-29T09:30:00-04:00`.
- Alpaca positions: `get_all_positions` PASS. 31 long US equity positions, open orders 0.
- Alpaca orders: `get_orders(status=open)` PASS with `[]`; `get_orders(status=closed, after=2026-05-22)` PASS and reconciled recent filled/canceled/expired paper orders.
- Alpaca activities: `get_account_activities(activity_types=[FILL], after=2026-05-22)` PASS and reconciled fills from 2026-05-22 through 2026-05-28.
- Alpaca market data: `get_stock_bars` PASS for open positions plus SPY/QQQ from 2026-05-22 through 2026-05-28 using `feed=iex`.
- Alpaca news: `get_news` PASS for review symbols and benchmarks from 2026-05-27 through 2026-05-28.
- Alpaca portfolio history: `get_portfolio_history` cancelled 3 times. Classified as `gap_category=cancelled`, `retry_count=2`. Account-level time-series drawdown is incomplete, so this run does not mutate policy.

## Research MCP coverage

| Provider | Tool use | Outcome | gap_category | Notes |
| --- | --- | --- | --- | --- |
| sec-edgar | `get_recent_filings` for NKE, XOM, BAC, AMZN | usable | not_applicable | Recent filings checked for due review context. BAC had multiple 424B2 filings on 2026-05-28; XOM had Form 4 and DEFA14A; AMZN/NKE had Form 4/13G style activity. |
| alpha-vantage | `TOOL_LIST`, `TOOL_GET("PING")`, `TOOL_CALL("PING", {})`, then `TOOL_GET("EARNINGS_CALENDAR")`, `TOOL_CALL("EARNINGS_CALENDAR", {"symbol":"NKE","horizon":"3month"})` | gap | cancelled | PING returned `pong`; first non-PING call was cancelled once. Per workflow, Alpha retries stopped and provider classified `cancelled`. |
| fred | tool discovery only | gap | wrapper_error | Registered FRED MCP tools were unexpectedly not exposed in this runtime. No shell/curl probe was attempted. |
| firecrawl | tool discovery only | gap | wrapper_error | Registered Firecrawl MCP tools were unexpectedly not exposed in this runtime. No shell/curl probe was attempted. |
| yahoo-finance | `get_recommendations` for NKE/BAC/XOM, `get_yahoo_finance_news` for PLTR | usable | not_applicable | Used as analyst/news context only, not as order evidence. |

## Outcome basis

- 1D due fills reviewed in detail: NKE, PFE, SO, WMT, NEE, AMZN, BAC, XOM, V from 2026-05-27 fills.
- Newly filled or same-day 2026-05-28 orders were reconciled and left as `회고 대기`: INTC, NOK, PLTR, QQQ, CVX, NKE, PFE, WMT, GOOGL, SO, SLB, SPY, BAC, NEE, NVDA, COP, TSLA, AMZN, XOM.
- Skipped recommendation review covered no-submit runs blocked by `risk_daily_new_orders_budget` and after-hours `fresh_quote` failure. No skipped candidate has a full 1D outcome horizon yet.
