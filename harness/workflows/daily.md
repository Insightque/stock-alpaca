# Workflow: Daily Trading Run

Use this when the user says `Run daily trading workflow`.

## Goal

Produce one daily report, refresh the trading wiki, create a risk-checked order plan, and submit automatic Alpaca paper orders only when every safety condition passes.

## Inputs

- Alpaca MCP account, clock, positions, watchlists, assets, stock data, and news.
- Web sources for current company, earnings, sector, and macro context.
- Existing wiki pages: `wiki/index.md`, `wiki/log.md`, ticker pages, portfolio pages, and recent reports.

## Required Outputs

- `wiki/reports/daily/YYYY-MM-DD.md`
- Updated ticker pages in `wiki/tickers/`
- New immutable raw source notes in `wiki/raw/sources/`
- Updated `wiki/portfolio/current.md`
- Order plan JSON in `wiki/portfolio/order-plans/YYYY-MM-DD-daily.json`
- Updated `wiki/index.md`
- Appended `wiki/log.md` entry

## Procedure

1. Coordinator Agent
   - Read `AGENTS.md`, `wiki/index.md`, and the last 10 entries of `wiki/log.md`.
   - Confirm `.env` has `ALPACA_PAPER_TRADE=true`.
   - Use Alpaca MCP to get account info, market clock, open orders, current positions, and watchlists.
   - If MCP is unavailable, switch to research-only mode and record the blocker.

2. Universe Agent
   - Build the candidate universe from Alpaca watchlists plus any tickers explicitly requested by the user.
   - Use Alpaca MCP asset lookup to keep only active, tradable US stocks/ETFs.
   - Exclude options, crypto, inactive assets, non-tradable assets, and anything requiring fractional shares.

3. Market Data Agent
   - For each candidate, gather daily bars for roughly 5 trading days, 20 trading days, and 63 trading days when available.
   - Gather latest snapshot, quote/trade, most active/movers context, and Alpaca news.
   - Record source timestamps so quote freshness can be checked.

4. Web Research Agent
   - Browse for current company, earnings, guidance, analyst, sector, and macro context.
   - Capture each useful source as `wiki/raw/sources/YYYY-MM-DD-source-slug.md` using `harness/templates/raw-source.md`.
   - Keep summaries concise and include source URLs.

5. Trend Agent
   - Compute daily, weekly, and monthly trend using price direction, volume, momentum, volatility, drawdown, and relative strength.
   - Use this scoring model:
     - Trend and relative strength: 35 points.
     - Current news/fundamental context: 25 points.
     - Risk/liquidity/volatility quality: 20 points.
     - Portfolio fit/diversification: 20 points.
   - Assign each ticker a 0-100 score and confidence: low, medium, or high.

6. Ticker Thesis Agent
   - Create or update `wiki/tickers/SYMBOL.md`.
   - Include current thesis, D/W/M trend, catalysts, risks, portfolio context, confidence, and source links.
   - Flag contradictions or stale claims instead of erasing them silently.

7. Portfolio/Risk Agent
   - Propose target allocations using the medium risk policy in `harness/risk-policy.md`.
   - Keep at least 20% cash reserve and at most 80% invested.
   - Keep each ticker at or below 20% of portfolio value.
   - Create a concrete JSON order plan in `wiki/portfolio/order-plans/YYYY-MM-DD-daily.json`.
   - Validate it with `python3 scripts/check-risk-policy.py wiki/portfolio/order-plans/YYYY-MM-DD-daily.json`.

8. Executor Agent
   - If the order plan fails validation, submit nothing.
   - If the market is closed, submit nothing and mark orders as planned/skipped.
   - If quote data is older than 20 minutes in submit mode, submit nothing for that ticker.
   - If validation passes and the market is open, submit paper orders through Alpaca MCP only.
   - Use stock/ETF day limit orders only; do not use custom REST calls.

9. Post-Trade Agent
   - Use Alpaca MCP to verify submitted orders, fills, open orders, current positions, cash, and buying power.
   - Update `wiki/portfolio/current.md`.
   - Add submitted/skipped order tables to the daily report.

10. Wiki Curator Agent
    - Update `wiki/index.md` with new/changed pages.
    - Append a `wiki/log.md` entry with run status, tickers, submitted orders, skipped orders, and report path.

## Stop Conditions

- Live trading detected.
- Alpaca MCP unavailable for submit-mode order execution.
- Market closed for US equities.
- Risk-policy validation fails.
- Any order would be options, crypto, short, fractional, non-US, or non-tradable.

