---
id: 2026-05-27-2331-hourly-autopilot-sources
created_at: 2026-05-27T14:35:00Z
workflow: hourly-autopilot
paper: true
---

# 2026-05-27-2331-hourly-autopilot 원천 요약

- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-alpaca-core-preflight.json`. Scheduler-owned Alpaca MCP read-only evidence이며 clock/account/positions/open orders/recent fills/assets/quotes/snapshots/trades hard gate가 pass다.
- Stale order cleanup: `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-stale-order-cleanup.json`. stale candidate 0건, cancel attempt 0건, remaining open autopilot order는 fresh GOOGL buy 1건이다.
- Research MCP preflight: `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-research-mcp-preflight.json`. SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 `empty_response` gap으로 분류됐다.
- 후보 universe: scheduler Alpaca preflight `universe_symbols` 62개와 `SPY`, `QQQ` benchmark 포함.
- 주문 후보 quote: AMZN/BAC/XOM 모두 Alpaca IEX quote 기준 2026-05-27T14:31:38Z~14:31:40Z 캡처, spread 0.0111%~0.0204%.

## 데이터 공백

- Alpha Vantage: `NEWS_SENTIMENT returned no candidate news items for the shortlisted symbols.`, `gap_category=empty_response`, `retry_count=0`.
- Alpaca core: blocking gap 없음.
