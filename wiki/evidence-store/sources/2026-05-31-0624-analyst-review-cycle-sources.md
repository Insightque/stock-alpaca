---
id: 2026-05-31-0624-analyst-review-cycle-sources
source_type: mcp-reconciliation
created_at: 2026-05-30T21:24:00Z
workflow: harness/workflows/analyst-review-cycle.md
paper: true
---

# 2026-05-31 06:24 KST analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: 2026-05-30 17:21:46 ET 기준 market closed, next open 2026-06-01 09:30 ET, next close 2026-06-01 16:00 ET.
- Account: status ACTIVE, portfolio value 101,975.35 USD, cash 34,800.26 USD, buying power 130,809.93 USD, long market value 67,175.09 USD.
- Open US equity orders: 0.
- Positions: 32 long positions, no short positions observed.
- Recent closed orders after 2026-05-27: 2026-05-29 regular-session filled buys 10건, same window canceled unfilled orders include MRK, BAC, SPY, and earlier stale/cleanup/probe orders. No sell fill observed in the queried window.
- FILL activities after 2026-05-27: buy fills only. Latest 2026-05-29 cohort: NKE, PFE, SO, SLB, AMZN, QQQ, V, GOOGL, WMT, NEE.
- Portfolio history: `get_portfolio_history` initial call plus 2 retries were cancelled. This is recorded as `gap_category=cancelled`, `retry_count=2`; account-level MFE/MAE and portfolio P/L path were not used for policy changes.

## Alpaca market-data snapshot

Snapshot source: Alpaca MCP `get_stock_snapshot(feed=iex)` for `AMZN,NKE,PFE,SO,SLB,QQQ,V,GOOGL,WMT,NEE,SPY`.

| Symbol | 2026-05-29 close/current reference | Same-session note |
| --- | ---: | --- |
| AMZN | 270.61 close, 270.64 position current | Below 2026-05-29 add fill 272.76. |
| NKE | 46.22 close, 46.23 position current | Below 2026-05-29 add fill 46.59. |
| PFE | 26.17 close, 26.18 position current | Slightly above 2026-05-29 add fill 26.09. |
| SO | 92.03 close, 92.05 position current | Above 2026-05-29 add fill 91.55. |
| SLB | 54.55 close/current | Below 2026-05-29 add fill 54.79. |
| QQQ | 738.21 close, 738.31 position current | Slightly above 2026-05-29 add fill 737.62. |
| V | 326.46 close, 326.36 position current | Below 2026-05-29 add fill 331.00. |
| GOOGL | 380.38 close, 380.34 position current | Below 2026-05-29 add fill 383.13. |
| WMT | 115.71 close, 115.75 position current | Above 2026-05-29 add fill 115.00. |
| NEE | 86.97 close, 87.01 position current | Above 2026-05-29 add fill 86.46. |
| SPY | 756.34 close, 756.48 position current | Broad benchmark reference only in this cycle. |

Because the 2026-05-29 fills occurred during the last completed regular session and the next U.S. regular close is 2026-06-01, this snapshot is a same-session/provisional mark, not a completed 1D horizon.

## Alpaca news context

Alpaca MCP news for 2026-05-29 showed an AI-led/risk-on tape rather than broad sector participation:

- S&P 500 hit a record while 8 of 11 sectors fell; Dell AI server sales and AI infrastructure headlines dominated the tape.
- QQQ/SPY-related news emphasized AI megacap strength and Nasdaq/AI ETF leadership.
- AMZN/GOOGL appeared in AI infrastructure, hyperscaler, and photonics supply-chain headlines.
- NKE appeared in rebound-stock coverage, but not as a strong market-wide leadership theme.
- PFE appeared in defensive/high-dividend healthcare analyst coverage.

## SEC EDGAR MCP

Recent filing checks were run on representative 2026-05-29 cohort symbols:

- AMZN: 2026-05-29 SD filing and several 2026-05-26 Form 4 filings.
- GOOGL: 2026-05-29 Form 144 and several 2026-05-27 Form 4 filings accepted 2026-05-28 UTC.
- WMT: several 2026-05-29 Form 4 filings and one Form 144.
- NKE: 2026-05-29 SD filing; older Form 4/13G entries also returned.

No SEC filing result in this cycle was used as a positive buy signal or policy-promotion signal. The checks only support review context.

## Alpha Vantage MCP

- `TOOL_LIST` succeeded.
- `TOOL_GET("PING")` succeeded.
- `TOOL_CALL("PING", {})` returned healthy.
- Candidate data `TOOL_GET("NEWS_SENTIMENT")` was cancelled before a matching non-PING `TOOL_CALL`; no Alpha candidate data was used. Recorded as `gap_category=cancelled`, `retry_count=0`.

## Yahoo Finance MCP

Yahoo Finance MCP was attempted for the review context. Parallel calls for AMZN, GOOGL, and NKE were cancelled by the tool safety layer; WMT news succeeded and showed retail pullback/buy-the-dip and healthcare/logistics expansion coverage. The usable Yahoo evidence is therefore partial and not sufficient for policy promotion.

## FRED and Firecrawl MCP

Registered FRED and Firecrawl callable tools were not exposed by tool discovery in this runtime. Per workflow instruction, no shell/curl probe was run. Both providers are recorded as `gap_category=wrapper_error`, `retry_count=0`.

## Mutation audit

No Alpaca order submission, replacement, cancellation, or position-closing tool was called in this workflow. The only Alpaca tools used were read-only reconciliation, account/activity/order/position/history, news, and market-data tools.
