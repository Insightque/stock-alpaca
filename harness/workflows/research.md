# Workflow: Research Tickers Only

Use this when the user says `관심종목 분석해줘`, `AAPL 분석해줘`, or asks to research tickers only.

## Goal

Research the requested tickers, update the llm-wiki, and make no orders.

## Required Outputs

- Updated ticker pages in `wiki/tickers/`
- New immutable raw source notes in `wiki/raw/sources/`
- Optional cross-ticker analysis in `wiki/analyses/`
- Updated `wiki/index.md`
- Appended `wiki/log.md` entry

## Procedure

1. Read `AGENTS.md`, `wiki/index.md`, and recent `wiki/log.md`.
2. Parse the requested ticker list. If the user did not provide tickers, use Alpaca watchlists as the universe.
3. Use Alpaca MCP asset lookup to confirm each ticker is an active tradable US stock/ETF.
4. Use Alpaca MCP stock bars, snapshots, quotes/trades, and news to collect market context.
5. Browse current web sources for company events, earnings, sector context, and relevant macro factors.
6. Capture each useful source as an immutable raw source note.
7. Update each ticker page with:
   - Current thesis.
   - Daily, weekly, and monthly trend.
   - Catalysts and risks.
   - Source-backed confidence.
   - Portfolio relevance if positions exist.
8. If comparing tickers, create or update a page under `wiki/analyses/`.
9. Update `wiki/index.md` and append `wiki/log.md`.

## Hard Rule

Do not create an order plan and do not submit orders in this workflow.
