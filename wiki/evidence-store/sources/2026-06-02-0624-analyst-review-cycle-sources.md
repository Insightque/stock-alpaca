---
id: 2026-06-02-0624-analyst-review-cycle-sources
created_at: 2026-06-01T21:24:13Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-02 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: 2026-06-01 17:21 ET 기준 market closed, next open 2026-06-02 09:30 ET, next close 2026-06-02 16:00 ET.
- Account: ACTIVE, portfolio value 103,380.11 USD, cash 34,339.00 USD, buying power 131,106.21 USD, long market value 69,041.11 USD.
- Open US equity orders: 0.
- Current positions: 32 symbols.
- Recent FILL activities after 2026-05-22: buy fills only in the reviewed scope; no sell fill found in the queried page.
- Portfolio history: initial call + 2 retries all returned cancelled, so account-level MFE/MAE and cashflow-adjusted path are data gaps.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.

## Daily bar evidence

Alpaca MCP `get_stock_bars` with `feed=iex`, `timeframe=1Day`, `start=2026-05-22T00:00:00Z`, `end=2026-06-02T00:00:00Z` was used for the due 1D and 5D calculations.

Benchmark closes:

| Symbol | 2026-05-22 close | 2026-05-29 close | 2026-06-01 close |
| --- | ---: | ---: | ---: |
| SPY | 745.67 | 756.34 | 758.44 |
| QQQ | 717.49 | 738.21 | 742.60 |

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | cancelled | 2 | core reconciliation and daily bars usable; portfolio history cancelled after 3 total attempts. |
| sec-edgar | usable | not_applicable | 0 | AVGO recent filings checked; latest 2026-06-01 SD filing noted as event context, not a thesis upgrade. |
| alpha-vantage | gap | cancelled | 1 | Required `TOOL_LIST -> TOOL_GET("PING") -> TOOL_CALL("PING", {})` sequence attempted. PING call cancelled twice, so non-PING Alpha calls were not attempted. |
| fred | gap | wrapper_error | 0 | Registered callable namespace was not exposed; no shell/curl probing. |
| firecrawl | gap | wrapper_error | 0 | Registered callable namespace was not exposed; no shell/curl probing. |
| yahoo-finance | usable | not_applicable | 0 | AVGO news queried; AI bottleneck/earnings-preview headlines used as context only. |

## News and event context

- Alpaca news for 2026-05-29 to 2026-06-01 showed an AI-led tape, including Dell/AI server momentum, AI infrastructure ETF/news flow, Broadcom earnings-preview headlines, and macro/oil headlines around Iran/Hormuz.
- Alpaca news also showed weaker or cautionary context for several defensive/diversification names: SO had a Truist Hold/lower target headline, SLB had a mixed shelf filing headline and acquisition headline, WMT had a target raise but price still lagged benchmarks on 2026-06-01.
- Yahoo Finance AVGO news showed Broadcom, Micron, Nvidia, and AI bottleneck/earnings-preview context. This supports event awareness for the new AVGO after-hours validation fill but does not by itself justify a policy change.

## Data gaps

- Alpaca portfolio history remained cancelled after the allowed retry count, so the review uses position/order/fill reconciliation and symbol daily bars rather than account-level path metrics.
- Alpha Vantage health check did not complete because PING calls were cancelled. No Alpha candidate data was used.
- FRED and Firecrawl were not exposed as registered callable tools in this runtime and were classified as wrapper errors.
