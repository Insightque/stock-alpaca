---
name: stock-alpaca-research-thesis
description: Build and maintain stock-alpaca ticker research and investment thesis pages. Use for ticker analysis, watchlist research, daily recommendation context, catalyst/risk/stale-claim updates, or source-backed current market/company research.
---

# Stock Alpaca Research Thesis

Use this skill for current ticker and portfolio research.

## Boundary

This skill owns thesis content and source-backed research. Use `stock-alpaca-mcp-research-gate` for coverage pass/fail decisions and `stock-alpaca-risk-order-plan` before any actionable order plan.

## Workflow

1. Read `AGENTS.md`, `harness/mcp-source-map.md`, and the relevant workflow.
2. Use Alpaca MCP first for watchlists, assets, market data, and Alpaca news.
3. Use research MCPs for SEC filings, earnings, macro, IR pages, analyst context, and supplemental financial data.
4. Capture current source context into immutable raw source notes when claims affect recommendations.
5. Update ticker pages under `wiki/research-notes/tickers/`.

## Thesis Page Content

Track:

- Current thesis
- Catalysts
- Risks
- Stale claims or invalidated assumptions
- Data gaps
- Source references
- Confidence and review needs

## Recommendation Discipline

- Do not fabricate missing context.
- Cite Alpaca MCP, research MCP, or captured source URLs for current claims.
- Keep broad universe coverage requirements when the user did not limit tickers.
- Hand off to `stock-alpaca-risk-order-plan` before any actionable order plan.
