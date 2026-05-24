# Workflow: Daily Trading Run

Use this when the user says `오늘 분석해줘` or asks for the daily trading workflow.

## Goal

Produce one daily report, refresh the trading wiki, and create a risk-checked order plan. Submit Alpaca paper orders only when this workflow is explicitly invoked in submit mode through a command such as `paper 주문까지 실행해줘`.

Default simple-command mode:

- `오늘 분석해줘` means no-submit mode.
- In no-submit mode, create recommendations and order candidates, but do not submit orders.

## Inputs

- Alpaca MCP account, clock, positions, watchlists, assets, stock data, and news.
- Research MCPs from `harness/mcp-source-map.md` for SEC filings, earnings calendar, analyst context, company IR capture, and macro indicators when available.
- Web sources for current company, earnings, sector, and macro context when MCP coverage is missing or needs source-page capture.
- Existing wiki pages: `wiki/index.md`, `wiki/log.md`, `wiki/policy-book/recommendation-policy.md`, ticker pages, portfolio pages, trade reviews, and recent reports.

## Required Outputs

- `wiki/current-runs/daily/YYYY-MM-DD.md`
- Updated ticker pages in `wiki/research-notes/tickers/`
- New immutable raw source notes in `wiki/evidence-store/sources/`
- Updated `wiki/trade-ledger/positions/current.md`
- Order plan JSON in `wiki/trade-ledger/orders/YYYY-MM-DD-daily.json`
- Updated `wiki/index.md`
- Appended `wiki/log.md` entry

For any report or cross-ticker analysis that includes calculated metrics, add a Korean `## 지표 설명` section near the bottom. Define each non-obvious metric in user-friendly language, especially return windows, hit rate, excess return, drawdown, relative strength, VWAP, spread, confidence, and policy-learning fields.

## Procedure

1. Coordinator Agent
   - Read `AGENTS.md`, `wiki/index.md`, and the last 10 entries of `wiki/log.md`.
   - Read `wiki/policy-book/recommendation-policy.md` when present and apply its current lessons to candidate scoring.
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
   - Read `harness/mcp-source-map.md`.
   - Use Alpaca news first, then enrich event context with research MCPs:
     - `sec-edgar` for recent 10-K, 10-Q, 8-K, Form 4, XBRL financials, and filing risks.
     - `alpha-vantage` for earnings calendar and earnings surprise when the API key is present.
     - `fred` for macro regime indicators when the API key is present.
     - `firecrawl` for company IR pages, press releases, and earnings presentation capture when the API key is present.
     - `yahoo-finance` for analyst recommendations, Yahoo news, holders, insider, and supplemental actions.
   - Browse for current company, earnings, guidance, analyst, sector, and macro context only when MCP data is insufficient or a source URL needs capture.
   - Capture each useful source as `wiki/evidence-store/sources/YYYY-MM-DD-source-slug.md` using `harness/templates/raw-source.md`.
   - Keep summaries concise and include source URLs, MCP names, query periods, and any missing-key/data-gap notes.

5. Trend Agent
   - Compute daily, weekly, and monthly trend using price direction, volume, momentum, volatility, drawdown, and relative strength.
   - Before final scoring, apply the news-price lead/lag policy from `wiki/policy-book/recommendation-policy.md`.
     - Classify each meaningful news event as earnings, theme/policy, mega-cap expectation, analyst, macro, or unknown.
     - Compare pre-news 3D/5D return, event-day return, and available post-news return.
     - If good news follows a large pre-news run-up, mark `price-led` or `sell-the-news-risk` and reduce new-buy confidence.
     - For theme/policy news, prefer next-session follow-through confirmation over same-day chase entries.
   - Use this scoring model:
     - Trend and relative strength: 35 points.
     - Current news/fundamental context: 25 points.
     - Risk/liquidity/volatility quality: 20 points.
     - Portfolio fit/diversification: 20 points.
   - Assign each ticker a 0-100 score and confidence: low, medium, or high.
   - Note any scoring adjustment caused by prior trade reviews or recommendation policy.

6. Ticker Thesis Agent
   - Create or update `wiki/research-notes/tickers/SYMBOL.md`.
   - Include current thesis, D/W/M trend, catalysts, risks, portfolio context, confidence, and source links.
   - Flag contradictions or stale claims instead of erasing them silently.

7. Portfolio/Risk Agent
   - Propose target allocations using the medium risk policy in `harness/risk-policy.yaml` and `harness/risk-policy.md`.
   - Keep at least 20% cash reserve and at most 80% invested.
   - Keep each ticker at or below 15% of portfolio value.
   - Create a concrete JSON order plan in `wiki/trade-ledger/orders/YYYY-MM-DD-daily.json`.
   - Include `schema_version`, `risk_policy_version`, `recommendation_policy_sha`, `created_at`, root `source_refs`, and per-order `quote_captured_at`, `asset_checked_at`, `source_refs`.
   - Validate it with `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/YYYY-MM-DD-daily.json`.
   - Create a run manifest in `wiki/evidence-store/run-manifests/YYYY-MM-DD-HHMM-run-id.json` using `harness/templates/run-manifest.json`.

8. Executor Agent
   - If the order plan fails validation, submit nothing.
   - If the run is no-submit mode, submit nothing and mark orders as planned/skipped.
   - If the market is closed, submit nothing and mark orders as planned/skipped.
   - If quote data is older than 20 minutes in submit mode, submit nothing for that ticker.
   - If validation passes and the market is open, submit paper orders through Alpaca MCP only.
   - Use stock/ETF day limit orders only; do not use custom REST calls.

9. Post-Trade Agent
   - Use Alpaca MCP to verify submitted orders, fills, open orders, current positions, cash, and buying power.
   - Update `wiki/trade-ledger/positions/current.md`.
   - Add submitted/skipped order tables to the daily report.

10. Wiki Curator Agent
    - Update `wiki/index.md` with new/changed pages.
    - Append a `wiki/log.md` entry with run status, tickers, submitted orders, skipped orders, manifest path, and report path.

## Stop Conditions

- Live trading detected.
- Alpaca MCP unavailable for submit-mode order execution.
- Market closed for US equities.
- Risk-policy validation fails.
- Any order would be options, crypto, short, fractional, non-US, or non-tradable.
