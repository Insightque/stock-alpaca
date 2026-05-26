# Stock Alpaca Trading Harness

This repository is a Codex-first paper-trading harness. Use Alpaca MCP for all account, market data, watchlist, position, and order operations. Use web research only to enrich current context and capture sources into the wiki.

The persistent knowledge layer follows the llm-wiki pattern: raw sources are immutable, generated wiki pages are maintained by the agent, and `wiki/index.md` plus `wiki/log.md` are updated on every meaningful run.

Additional research MCPs may be available for SEC filings, earnings calendars, company IR capture, analyst context, and macro data. Read `harness/mcp-source-map.md` before current-market research, historical simulations, or policy-learning work that depends on news/events beyond Alpaca.

## Non-Negotiables

- Paper trading only. Abort any trading workflow if `ALPACA_PAPER_TRADE` is missing or not `true`.
- Never place live orders, options orders, crypto orders, short orders, or fractional-share orders.
- Never call Alpaca trading REST endpoints directly from scripts. Orders must be submitted only through the `alpaca` MCP server.
- Never print, copy, summarize, or commit Alpaca API keys.
- Automatic paper orders are allowed only after the risk gate passes.
- If Alpaca MCP is unavailable, continue with research and wiki updates, but do not submit orders.
- Current market/news claims must cite Alpaca MCP output, a dedicated research MCP output, a captured web source, or an explicit source URL in a raw wiki note.
- Accuracy takes priority over quick recommendations. Current recommendation runs must record `mcp_coverage` for Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, and Yahoo Finance. Alpaca is the core MCP gate; SEC EDGAR, Alpha Vantage, FRED, Firecrawl, and Yahoo Finance are research MCPs that must all be attempted, with at least 3 usable/pass for actionable buy candidates. Actionable recommendations and submit-mode runs must pass `python3 scripts/check-mcp-coverage.py --strict <run-manifest>`.
- Unless the user explicitly asks for a limited ticker set, current recommendation runs must first screen the broad metadata universe in `harness/symbol-metadata.yaml`, include `SPY` and `QQQ`, record `universe_coverage`, and pass `python3 scripts/check-universe-coverage.py --strict <run-manifest>` before any recommendation can be actionable.
- Never print, summarize, or commit third-party API keys such as Alpha Vantage, FRED, Firecrawl, Octagon, or similar research-provider keys.

## Simple User Commands

Read `harness/simple-commands.md` before interpreting user-facing trading commands. Users are expected to use short Korean commands; route them to the matching workflow exactly:

- `오늘 분석해줘`: use `harness/workflows/daily.md` in no-submit mode.
- `관심종목 분석해줘`: use `harness/workflows/research.md` with Alpaca watchlist.
- `AAPL 분석해줘` or `AAPL MSFT 분석해줘`: use `harness/workflows/research.md` for the requested tickers.
- `포트폴리오 점검해줘`: use `harness/workflows/post-trade.md`.
- `리밸런싱 계획 짜줘`: use `harness/workflows/rebalance.md` in no-submit mode.
- `paper 주문까지 실행해줘`: use the latest validated order plan or `harness/workflows/rebalance.md` in submit mode, then run post-trade check.
- `시간 단위로 자동 운영해줘`, `자동으로 매입/매도해줘`: use `harness/workflows/hourly-autopilot.md` through `scripts/run-hourly-autopilot-codex.sh`. This is Alpaca paper-only automation; submit only when market, universe, MCP, quote, spread, and risk gates all pass.
- `거래 후 점검해줘`: use `harness/workflows/post-trade.md`.
- `거래 회고해줘`: use `harness/workflows/trade-review.md`.
- Scheduled analyst reviews use `harness/workflows/analyst-review-cycle.md` through `scripts/run-analyst-review-codex.sh`; this workflow never submits orders.
- `YYYY-MM-DD 기준 추천 시뮬레이션해줘`: use `harness/workflows/historical-decision-sim.md` in dry-run mode only.
- `YYYY-MM-DD 추천 회고해줘`: use `harness/workflows/historical-decision-review.md`; do not submit orders.
- `위키 정리해줘`: use `harness/workflows/wiki-lint.md`.

If a user command does not explicitly include `주문`, `매수`, `매도`, `실행`, or `submit`, do not submit orders. If the user asks for a custom variant, keep the same safety rules and record the deviation in `wiki/log.md`.

## Agent Roles

- Coordinator Agent: starts the run, reads `wiki/index.md` and recent `wiki/log.md`, confirms paper mode, checks market clock, account, positions, orders, and watchlists.
- Universe Agent: builds the candidate universe from Alpaca watchlists plus user-specified tickers, then filters to active tradable US stocks/ETFs.
- Market Data Agent: gathers Alpaca bars, snapshots, latest quote/trade, market movers, and Alpaca news for candidate tickers.
- Web Research Agent: gathers current company, earnings, SEC filing, analyst, macro, and event context from Alpaca plus the research MCPs listed in `harness/mcp-source-map.md`; writes immutable raw source notes and records unavailable keys or failed tools as data gaps.
- Trend Agent: computes daily, weekly, and monthly trend views from price action, volume, momentum, volatility, drawdown, and relative strength.
- Ticker Thesis Agent: updates ticker pages with thesis, catalysts, risks, stale claims, and confidence.
- Portfolio/Risk Agent: creates target allocations and validates a JSON order plan with `scripts/check-risk-policy.py`.
- Executor Agent: submits approved paper orders through Alpaca MCP only, using day limit stock orders.
- Wiki Curator Agent: updates cross-links, `wiki/index.md`, and `wiki/log.md`; flags contradictions instead of silently resolving them.
- Post-Trade Agent: verifies submitted orders, fills, positions, and buying power; writes execution outcomes back to the wiki.
- Trade Review Agent: reviews closed trades and still-held traded stocks against the original thesis, order plan, market context, and later outcomes; records what was right, what was wrong, and how recommendation policy should improve.
- Historical Decision Agent: recreates an as-of-date recommendation using only information available at that historical point, creates dry-run orders, and schedules 1D/5D/20D review horizons.
- Historical Review Agent: evaluates historical recommendations with later prices, benchmark-relative returns, and policy-learning signals while preserving the original recommendation unchanged.

Use actual sub-agents when the runtime and user instruction allow parallel agent work. Otherwise, perform the roles sequentially and label the sections in the report.

## Risk Policy

The default policy is medium risk. The machine-readable source of truth is `harness/risk-policy.yaml`; `harness/risk-policy.md` explains the same values for humans.

- Maximum invested after new orders: 80% of account portfolio value.
- Minimum cash reserve after new buy orders: 20% of account portfolio value.
- Maximum target exposure per ticker: 15% of account portfolio value.
- Maximum new orders per run: 10.
- Allowed assets: active tradable US stocks and ETFs only.
- Allowed order shape: long-only, whole-share, day limit orders.
- Quote freshness: for submit-mode runs, use quote/snapshot data captured within 20 minutes.
- Limit guardrail: buy/sell limit prices must be within 0.5% of the recorded reference price.
- Do not rely on same-run sell proceeds to fund buy orders.

Always create or update an order-plan JSON before submitting orders, then run:

```bash
python3 scripts/check-risk-policy.py path/to/order-plan.json
```

Use `python3 scripts/check-risk-policy.py --json path/to/order-plan.json` when a workflow or CI needs a machine-readable result. New order plans must conform to `harness/order-plan.schema.json` and include `schema_version`, `risk_policy_version`, `recommendation_policy_sha`, `created_at`, `quote_captured_at`, `asset_checked_at`, and `source_refs`.

If validation fails, do not submit orders. Write skipped orders and reasons into the daily report.

## Wiki Conventions

- Record all future wiki content, daily reports, ticker analyses, portfolio notes, raw-source summaries, and log entries in Korean by default. Keep ticker symbols, source titles, field names, tool names, and quoted source text in their original language when that improves traceability.
- `wiki/evidence-store/sources/`: immutable source notes. Do not edit raw source pages after initial capture except to fix formatting that blocks parsing.
- `wiki/research-notes/tickers/`: one page per ticker, named `SYMBOL.md`.
- `wiki/research-notes/portfolio/`: reusable portfolio interpretation and allocation notes.
- `wiki/current-runs/daily/`: current-account/current-market trading workflow reports named `YYYY-MM-DD.md`.
- `wiki/trade-ledger/orders/`: actual paper orders and dry-run order plans.
- `wiki/trade-ledger/positions/`: actual paper positions and account-state snapshots.
- `wiki/trade-ledger/reviews/`: post-trade review notes for actual paper trades, named `YYYY-MM-DD-SYMBOL-review.md` or `YYYY-MM-DD-portfolio-review.md`.
- `wiki/backtest-runs/`: historical experiments, simulated decisions, and outcome validation.
- `wiki/backtest-runs/decisions/`: historical as-of recommendation simulations, named `YYYY-MM-DD-historical-decision.md`; do not include future outcomes here.
- `wiki/backtest-runs/results/`: all backtest results that use later outcomes, including individual historical reviews, multi-date policy backtests, event studies, and validation summaries.
- `wiki/policy-book/recommendation-policy.md`: living policy distilled from trade reviews and historical backtest reviews. Update it only with evidence-backed lessons, not one-off hindsight.
- `wiki/research-notes/analyses/`: reusable cross-ticker or thematic analyses.
- `wiki/evidence-store/run-manifests/`: machine-readable run manifests for meaningful runs.
- `wiki/index.md`: content-oriented catalog. Read it first and update it after each run.
- `wiki/log.md`: append-only chronological log. Add a new `## [YYYY-MM-DD HH:MM TZ] type | title` entry for every run.

Use wiki links such as `[[AAPL]]`, `[[portfolio-current]]`, and `[[2026-05-22]]` where helpful, but keep plain Markdown readable without Obsidian.

## Trade Review And Policy Learning

- After any filled paper trade exists, future `거래 후 점검해줘`, `포트폴리오 점검해줘`, `리밸런싱 계획 짜줘`, and `오늘 분석해줘` runs should check whether a trade review is due.
- Review both closed positions and still-held traded stocks. For open positions, mark conclusions as interim.
- Compare the original recommendation with the actual later outcome using the wiki state that existed at decision time: ticker page, daily report, order plan, raw sources, account snapshot, market data, and risk policy.
- Record what worked, what failed, what was unknowable, and what should change in future recommendations.
- Do not rewrite old thesis pages to look smarter in hindsight. Add dated review sections or separate review pages.
- A single trade can suggest a hypothesis, but update `wiki/policy-book/recommendation-policy.md` only when the lesson is evidence-backed and clearly useful for future recommendations.

## Research MCP Source Policy

- Use Alpaca MCP first for account/order/position/watchlist/market data and Alpaca news.
- Use `sec-edgar` for SEC filings, 10-K, 10-Q, 8-K, XBRL financials, Form 4, insider activity, and filing-grounded risk/fundamental checks when `SEC_EDGAR_USER_AGENT` is present.
- Use `alpha-vantage` for earnings calendar, earnings history/surprise, and supplemental market/fundamental data when `ALPHA_VANTAGE_API_KEY` is present.
- Use `fred` for macro regime checks such as CPI, unemployment, Treasury yields, yield curve, Fed-related series, and economic releases when `FRED_API_KEY` is present.
- Use `firecrawl` for company IR pages, press releases, earnings presentations, and source-page capture when `FIRECRAWL_API_KEY` is present.
- Use `yahoo-finance` for Yahoo Finance news, analyst recommendation summaries, holders, insider, actions, and supplemental financial data.
- If a research MCP is unavailable or missing a key, do not fabricate the missing context. Record the gap in the raw source note and continue with available sources.

## Historical Decision Simulation And Policy Learning

- A user may ask for a recommendation from a specific past date or timestamp. Treat that as a historical simulation, not as a live trading request.
- Historical simulations must use strict leakage control: recommendation artifacts may include only data available at or before the historical as-of point.
- If the user gives only a date, use that US regular trading day close as the default as-of point. If the date is a market holiday, use the closest prior regular trading day and record the adjustment.
- The default review horizons are 1D, 5D, and 20D after the as-of point.
- The default historical universe is symbols that appeared in the as-of wiki state, raw sources, order plans, portfolio records, or watchlist records. Current watchlists are not valid strict-mode evidence unless they were captured at the historical point.
- Historical simulations may create only dry-run order plans. They must never call Alpaca order submission, replacement, cancellation, or position-closing tools.
- Historical reviews may use later prices and benchmark returns, but only in separate review documents. Do not edit the original simulation to include future outcomes.
- Run `scripts/check-leakage.py` on new or materially changed historical simulation/order-plan artifacts when practical; if it cannot run, record the reason in `wiki/log.md`.
- Use accumulated review evidence to update `wiki/policy-book/recommendation-policy.md` with `evidence_count`, `hit_rate`, `avg_excess_return`, and status. Single examples stay as hypotheses unless impact is clearly material.

## Trading Execution Contract

Before submitting any paper order:

1. Confirm `ALPACA_PAPER_TRADE=true`.
2. Confirm Alpaca market clock is open for US equities.
3. Confirm the candidate asset is active, tradable, and a US stock/ETF.
4. Confirm trend/thesis/risk evidence exists in the wiki for the ticker.
5. Confirm `scripts/check-risk-policy.py` passes.
6. Submit only through Alpaca MCP, normally `place_stock_order` with `type=limit` and `time_in_force=day`.
7. Immediately run a post-trade check and update the wiki.

If any step is uncertain, skip submission and record the uncertainty.

## Automation

- Hourly paper autopilot is allowed only through `harness/workflows/hourly-autopilot.md`.
- The hourly autopilot must create a detailed recommendation report, run manifest, and order plan on every run, even when it submits nothing.
- The hourly autopilot may submit Alpaca paper buy/sell orders only if all strict gates pass and the market is open.
- The hourly autopilot should run on a fixed minute-31 calendar schedule. The 22:31 KST run is also the US regular market-open validation run. It may prefer a tiny 1-share validation order only when every hard gate passes; it must not force orders through missing Alpaca core, stale quote, spread, MCP, universe, or risk evidence.
- The analyst review cycle runs through `harness/workflows/analyst-review-cycle.md` and never mutates account/order/position state.
- Buy/sell rationale must be detailed enough for later 1D/5D/20D analyst review and policy-learning updates.
