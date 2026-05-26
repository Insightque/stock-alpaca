---
id: 2026-05-27-0012-hourly-autopilot-sources
created_at: 2026-05-26T15:24:00Z
timezone: Asia/Seoul
source_type: mcp-run-summary
immutable: true
---

# 2026-05-27 00:12 KST hourly autopilot sources

## 조회 범위

- Workflow: `harness/workflows/hourly-autopilot.md`
- 기준 시각: 2026-05-26 11:14-11:21 EDT / 2026-05-27 00:14-00:21 KST
- Universe: `harness/symbol-metadata.yaml` 62개 + 현재 보유 종목 + `SPY`, `QQQ`
- Pre-MCP shortlist: `ASML`, `LLY`, `AAPL`, `SMH`, `FCX`
- Final candidates: `ASML`, `LLY`, `AAPL`

## Alpaca MCP

| Check | Tool | Outcome | Evidence |
| --- | --- | --- | --- |
| paper mode | `.env` 확인 | pass | `ALPACA_PAPER_TRADE=true` 존재. 키 값은 출력하지 않음 |
| market clock | `get_clock` | pass | `is_open=true`, timestamp `2026-05-26T11:14:12.925797058-04:00`, next close `2026-05-26T16:00:00-04:00` |
| account | `get_account_info` | pass | ACTIVE, portfolio value 101301.19 USD, cash 44030.58 USD, buying power 138895.81 USD |
| open orders | `get_orders(status=open, asset_class=us_equity)` | pass | `[]` |
| positions | `get_all_positions` | pass | 10개 long positions, long market value 57270.61 USD |
| same-day fills | `get_account_activities(activity_types=FILL, after=2026-05-26)` | pass | `[]` |
| watchlists | `get_watchlists` | pass | `[]` |
| broad bars | `get_stock_bars(62 symbols, 1Day, IEX)` | partial usable | direct MCP call returned bars but response was too large for durable capture in this run |
| broad snapshot | `get_stock_snapshot(62 symbols, IEX)` | pass after retry | first attempt ConnectError, retry returned quote/snapshot rows |
| candidate quotes | `get_stock_latest_quote` | pass | quote timestamp around `2026-05-26T15:17:49Z`-`15:17:51Z` |
| asset checks | `get_asset` | pass | `ASML`, `LLY`, `SMH`, `FCX` active/tradable US equity |
| market movers | `get_market_movers(stocks, top=10)` | pass | updated `2026-05-26T15:21:00.284202584Z`; top movers were mostly low-price/speculative and excluded |
| most active | `get_most_active_stocks(volume, top=10)` | pass | updated `2026-05-26T15:21:00.284202584Z`; `NOK` appeared among most active |
| news | `get_news(ASML,AAPL,LLY,SMH,FCX)` | usable | AAPL and LLY Benzinga items returned; no strong ASML-specific Alpaca item in the returned batch |

## Quote and spread evidence

| Symbol | quote_time_utc | bid | ask | mid | spread_pct | Gate |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| ASML | 2026-05-26T15:17:50.623704536Z | 1614.35 | 1620.36 | 1617.355 | 0.372 | pass |
| LLY | 2026-05-26T15:17:51.237736660Z | 1076.95 | 1080.00 | 1078.475 | 0.283 | pass |
| AAPL | 2026-05-26T15:17:51.485688894Z | 311.24 | 311.26 | 311.25 | 0.006 | pass |
| SMH | 2026-05-26T15:17:51.461547511Z | 597.47 | 597.61 | 597.54 | 0.023 | pass |
| FCX | 2026-05-26T15:17:51.282983883Z | 64.27 | 64.29 | 64.28 | 0.031 | pass |
| AMD | 2026-05-26T15:17:51.288539576Z | 490.49 | 493.00 | 491.745 | 0.510 | fail |
| KLAC | 2026-05-26T15:17:49.732198618Z | 1871.20 | 1989.08 | 1930.14 | 6.107 | fail |
| AMAT | 2026-05-26T15:17:51.278089593Z | 451.19 | 454.00 | 452.595 | 0.621 | fail |
| LRCX | 2026-05-26T15:17:51.280807642Z | 303.85 | 326.00 | 314.925 | 7.034 | fail |
| MU | 2026-05-26T15:17:51.472911282Z | 870.00 | 874.46 | 872.23 | 0.511 | fail |

## SEC EDGAR MCP

- Local ticker-to-CIK cache `harness/sec-ticker-cik-map.json` was checked before SEC lookup classification.
- Cache rows: `ASML=0000937966`, `LLY=0000059478`, `AAPL=0000320193`; `SMH` is absent because it is an ETF and is treated as ticker lookup `empty_response`, not provider failure.
- `get_company_info(ASML)` returned success for ASML HOLDING NV, CIK 937966.
- `get_recent_filings(ASML, days=90, limit=5)` returned 5 filings, including 2026-04-23 6-K and 2026-02-25 20-F.
- `get_company_info(LLY)` returned success for ELI LILLY & Co, CIK 59478.
- `get_recent_filings(LLY, days=90, limit=5)` returned recent 144, 8-K, and Form 4 filings, including 2026-05-20 8-K.
- `get_company_info(AAPL)` returned success for Apple Inc., CIK 320193.
- `get_recent_filings(AAPL, days=90, limit=5)` returned recent Form 4/Form 144 filings and 2026-05-01 10-Q.

## Alpha Vantage MCP

- Required sequence was followed: `TOOL_LIST` -> `TOOL_GET(EARNINGS)` -> `TOOL_CALL(EARNINGS, ASML)`.
- `TOOL_LIST` returned available tools, including `EARNINGS`, `COMPANY_OVERVIEW`, `EARNINGS_CALENDAR`, `GLOBAL_QUOTE`, and macro functions.
- `TOOL_GET(EARNINGS)` returned schema requiring `symbol`.
- `TOOL_CALL(EARNINGS, {"symbol":"ASML"})` was cancelled by the MCP safety wrapper.
- Retry sequence used `TOOL_GET(COMPANY_OVERVIEW)` then `TOOL_CALL(COMPANY_OVERVIEW, {"symbol":"ASML"})`; the call was also cancelled.
- Gap classification: `gap_category=cancelled`, `retry_count=2`.

## Yahoo Finance MCP

- `get_stock_info(ASML)` returned usable company, valuation, analyst, and market fields.
- Key ASML fields used: Technology / Semiconductor Equipment & Materials; current price around 1623.22 USD; forward PE 34.075027; recommendation key `strong_buy`; 15 analyst opinions; target mean price 1662.6018; regular market state `REGULAR`.
- `get_recommendations(ASML, recommendations, 12)` returned current-period analyst mix: strongBuy 6, buy 32, hold 5, sell 1, strongSell 0.
- `get_yahoo_finance_news(ASML)` returned current/news context including ASML valuation momentum, Huawei chip-development headlines, and AI analyst/top-pick items.

## FRED MCP

- `scripts/mcp-fred.sh --health-check` was attempted 3 times.
- All attempts failed with `curl: (6) Could not resolve host: api.stlouisfed.org`.
- Read-only probe to `https://api.stlouisfed.org/fred/series?series_id=DGS10` also failed DNS resolution.
- Gap classification: `gap_category=dns`, `retry_count=2`.

## Firecrawl MCP

- `scripts/mcp-firecrawl.sh --health-check` was attempted 3 times.
- All attempts failed with `curl: (6) Could not resolve host: api.firecrawl.dev`.
- Read-only probe to `https://api.firecrawl.dev/v2` also failed DNS resolution.
- Gap classification: `gap_category=dns`, `retry_count=2`.

## Decision note

- Alpaca core gate passed and the market was open.
- Research MCP usable confirmations were SEC EDGAR and Yahoo Finance only. Alpha Vantage, FRED, and Firecrawl were attempted but unusable.
- The first blocking gate for submission was `mcp_research_min_confirmations`: 2 usable/pass research providers, below the required 3.
- No Alpaca order submission tool was called.
