---
id: 2026-06-01-0623-analyst-review-cycle-sources
source_type: mcp-reconciliation
created_at: 2026-05-31T21:23:00Z
workflow: harness/workflows/analyst-review-cycle.md
paper: true
---

# 2026-06-01 06:23 KST analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Account: status ACTIVE, portfolio value 101,975.35 USD, cash 34,800.26 USD, buying power 130,809.93 USD, long market value 67,175.09 USD.
- Open US equity orders: 0.
- Positions: 32 long positions, no short positions observed.
- Recent closed orders after 2026-05-22: filled buy orders only for actual positions; no sell fill observed in the queried FILL activities.
- Recent FILL activities after 2026-05-22: buy fills only. Latest 2026-05-29 cohort remains AMZN, NKE, PFE, SO, SLB, QQQ, V, GOOGL, WMT, NEE.
- Portfolio history: `get_portfolio_history` initial call plus 2 retries were cancelled. This is recorded as `gap_category=cancelled`, `retry_count=2`; account-level MFE/MAE and portfolio P/L path were not used for policy changes.
- Calendar/clock proxy: Alpaca `get_calendar(start=2026-06-01,end=2026-06-01)` initial call plus 2 retries were cancelled. The review therefore uses the prior analyst-review next-open marker and current local timestamp, and treats the 2026-06-01 U.S. regular close as not yet complete.

## Alpaca market data

Alpaca MCP `get_stock_bars(feed=iex,timeframe=1Day,start=2026-05-22,end=2026-05-30)` returned daily bars for review candidates and benchmarks. Because the run time was 2026-06-01 06:23 KST, the latest completed U.S. regular bar remained 2026-05-29.

### 2026-05-29 validation cohort

| Symbol | Fill price | 2026-05-29 close/current reference | Provisional return | Review state |
| --- | ---: | ---: | ---: | --- |
| AMZN | 272.76 | 270.64 | -0.78% | 1D 대기 |
| NKE | 46.59 | 46.23 | -0.77% | 1D 대기 |
| PFE | 26.09 | 26.18 | +0.34% | 1D 대기 |
| SO | 91.55 | 92.05 | +0.55% | 1D 대기 |
| SLB | 54.79 | 54.55 | -0.44% | 1D 대기 |
| QQQ | 737.62 | 738.31 | +0.09% | 1D 대기 |
| V | 331.00 | 326.36 | -1.40% | 1D 대기 |
| GOOGL | 383.13 | 380.34 | -0.73% | 1D 대기 |
| WMT | 115.00 | 115.75 | +0.65% | 1D 대기 |
| NEE | 86.46 | 87.01 | +0.64% | 1D 대기 |

These are same-session or weekend marks, not completed 1D outcomes. The next completed regular-session close is still required before judgment.

### 2026-05-22 stock-only cohort

The 2026-05-22 paper stock-only cohort remains scheduled for 5D review after the 2026-06-01 regular close. As of the latest completed 2026-05-29 bar, AMD, IONQ, AVGO, LRCX, TSM, and ETN were positive versus entry, while NVDA, NOK, UNH, and RGTI were weak or flat. This is recorded only as a pre-5D state because the planned 5D horizon is not complete at this run time.

## Alpaca news context

Alpaca MCP news for 2026-05-29 through 2026-06-01 continued to show an AI-led/risk-on market context rather than broad participation:

- S&P 500 and Nasdaq-related headlines emphasized record levels, AI server sales, Dell/Micron/Snowflake momentum, and AI infrastructure.
- AMZN and GOOGL appeared in AI infrastructure and hyperscaler context.
- WMT had an analyst price-target raise headline after the 2026-05-29 close.
- SLB had a mixed shelf filing headline on 2026-05-29.
- SO had a Truist hold/price-target reduction headline on 2026-05-29.
- NKE appeared in rebound-stock coverage rather than a confirmed broad leadership signal.

## SEC EDGAR MCP

SEC EDGAR MCP `get_recent_filings(identifier=ADBE,days=7,limit=5)` succeeded. It returned recent ADBE Form 4, Form 144, Schedule 13G, and S-8 entries, including a 2026-05-01 Form 4 accepted 2026-05-02. No SEC result in this cycle was used as a positive buy signal or policy-promotion signal.

## Alpha Vantage MCP

- `TOOL_LIST` succeeded.
- `TOOL_GET("PING")` succeeded.
- `TOOL_CALL("PING", {})` returned healthy.
- Candidate data `TOOL_GET("MARKET_STATUS")` was called immediately before the matching `TOOL_CALL("MARKET_STATUS", {})`, but the non-PING `TOOL_CALL` was cancelled by the tool safety layer. Per workflow instruction, no second Alpha function was attempted. Recorded as `gap_category=cancelled`, `retry_count=0`.

## Yahoo Finance MCP

Yahoo Finance MCP `get_yahoo_finance_news(ticker=ADBE)` succeeded. Usable context included software buyback coverage, Adobe AI shopping/referral and Firefly/AI-agent narrative, AI stock-photo cannibalization risk, and cautiously optimistic analyst framing. This was used only as review context for the existing ADBE validation position, not as a policy-promotion signal.

## FRED and Firecrawl MCP

Registered FRED and Firecrawl callable tools were not exposed by tool discovery in this runtime. Per workflow instruction, no shell/curl probe was run. Both providers are recorded as `gap_category=wrapper_error`, `retry_count=0`.

## Mutation audit

No Alpaca order submission, replacement, cancellation, or position-closing tool was called in this workflow. The only Alpaca tools used were read-only reconciliation, account/activity/order/position/history/calendar, news, and market-data tools.
