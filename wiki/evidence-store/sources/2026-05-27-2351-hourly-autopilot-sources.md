---
id: 2026-05-27-2351-hourly-autopilot-sources
created_at: 2026-05-27T14:59:22Z
source_type: scheduled-autopilot-source-note
immutable: true
---

# 2026-05-27 23:51 KST Hourly Autopilot Sources

- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-alpaca-core-preflight.json`. Scheduler-owned read-only Alpaca MCP evidence. Hard gate pass; clock/account/positions/open orders/recent fills/assets/quotes/snapshots/trades pass.
- Stale order cleanup: `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-stale-order-cleanup.json`. Scheduler-owned Alpaca MCP cleanup canceled stale GOOGL order `hourly-20260527-2311-googl-buy-1`; direct `get_order_by_id` reconciliation in nested Codex confirmed status `canceled`, `canceled_at=2026-05-27T14:51:09.572225237Z`.
- Research MCP preflight: `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-research-mcp-preflight.json`. SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage gap `empty_response` because `NEWS_SENTIMENT` returned no candidate news items.
- Supplemental registered Alpaca MCP `get_orders(status=open)` retry returned `cancelled`; this is recorded as a non-scoring supplemental Alpaca gap because scheduler preflight open-order row and direct canceled-order reconciliation were available.

## 후보 근거

`V`는 Alpaca asset check에서 active/tradable US equity이고, quote `2026-05-27T14:51:34.409818476Z` 기준 bid 329.91, ask 330.01, spread 0.0303%다. 현재 보유 및 동일일 buy 체결이 없어 duplicate/open-order gate를 피하며, 1주 notional은 cash reserve와 validation sizing 안에 있다.
