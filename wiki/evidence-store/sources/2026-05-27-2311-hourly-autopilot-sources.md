---
id: 2026-05-27-2311-hourly-autopilot-sources
created_at: 2026-05-27T14:15:30Z
run_id: 2026-05-27-2311-hourly-autopilot
---

# 2026-05-27-2311-hourly-autopilot 원천 요약

- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-27-2311-hourly-autopilot-alpaca-core-preflight.json`. Scheduler-owned read-only Alpaca MCP evidence. Hard gate `pass`, market open, account/positions/open orders/recent fills/asset/quote/snapshot/trade checks usable.
- Stale order cleanup: `wiki/evidence-store/sources/2026-05-27-2311-hourly-autopilot-stale-order-cleanup.json`. Status `pass`, stale autopilot candidates 0, remaining open orders 0.
- Research MCP preflight: `wiki/evidence-store/sources/2026-05-27-2311-hourly-autopilot-research-mcp-preflight.json`. Symbols: QQQ, AAPL, BAC, NEE, GOOGL, WMT, PFE, SPY, NKE, FCX, NOK, IONQ. SEC EDGAR, FRED, Firecrawl, Yahoo Finance `pass`; Alpha Vantage `gap` with `gap_category=empty_response`.
- Registered Alpaca quote refresh attempt: `mcp__alpaca__.get_stock_latest_quote(GOOGL,WMT,NEE, feed=iex)` returned `cancelled`. It was recorded as a non-blocking refresh gap because scheduler preflight quote rows were present, passed, and fresh under the 20-minute policy at decision time.

## 데이터 공백

- Alpha Vantage: `NEWS_SENTIMENT returned no candidate news items for the shortlisted symbols`, `gap_category=empty_response`, `retry_count=0`.
- Optional Alpaca quote refresh: `gap_category=cancelled`; preflight quote evidence was used instead.
