# Stock Alpaca Trading Harness

This repository is a Codex-first paper-trading harness. Use Alpaca MCP for all account, market data, watchlist, position, and order operations. Use web research only to enrich current context and capture sources into the wiki.

The persistent knowledge layer follows the llm-wiki pattern: raw sources are immutable, generated wiki pages are maintained by the agent, and `wiki/index.md` plus `wiki/log.md` are updated on every meaningful run.

## Non-Negotiables

- Paper trading only. Abort any trading workflow if `ALPACA_PAPER_TRADE` is missing or not `true`.
- Never place live orders, options orders, crypto orders, short orders, or fractional-share orders.
- Never call Alpaca trading REST endpoints directly from scripts. Orders must be submitted only through the `alpaca` MCP server.
- Never print, copy, summarize, or commit Alpaca API keys.
- Automatic paper orders are allowed only after the risk gate passes.
- If Alpaca MCP is unavailable, continue with research and wiki updates, but do not submit orders.
- Current market/news claims must cite either Alpaca MCP output, a captured web source, or an explicit source URL in a raw wiki note.

## Simple User Commands

Read `harness/simple-commands.md` before interpreting user-facing trading commands. Users are expected to use short Korean commands; route them to the matching workflow exactly:

- `오늘 분석해줘`: use `harness/workflows/daily.md` in no-submit mode.
- `관심종목 분석해줘`: use `harness/workflows/research.md` with Alpaca watchlist.
- `AAPL 분석해줘` or `AAPL MSFT 분석해줘`: use `harness/workflows/research.md` for the requested tickers.
- `포트폴리오 점검해줘`: use `harness/workflows/post-trade.md`.
- `리밸런싱 계획 짜줘`: use `harness/workflows/rebalance.md` in no-submit mode.
- `paper 주문까지 실행해줘`: use the latest validated order plan or `harness/workflows/rebalance.md` in submit mode, then run post-trade check.
- `거래 후 점검해줘`: use `harness/workflows/post-trade.md`.
- `거래 회고해줘`: use `harness/workflows/trade-review.md`.
- `위키 정리해줘`: use `harness/workflows/wiki-lint.md`.

If a user command does not explicitly include `주문`, `매수`, `매도`, `실행`, or `submit`, do not submit orders. If the user asks for a custom variant, keep the same safety rules and record the deviation in `wiki/log.md`.

## Agent Roles

- Coordinator Agent: starts the run, reads `wiki/index.md` and recent `wiki/log.md`, confirms paper mode, checks market clock, account, positions, orders, and watchlists.
- Universe Agent: builds the candidate universe from Alpaca watchlists plus user-specified tickers, then filters to active tradable US stocks/ETFs.
- Market Data Agent: gathers Alpaca bars, snapshots, latest quote/trade, market movers, and Alpaca news for candidate tickers.
- Web Research Agent: gathers current company, earnings, macro, and event context from web sources and writes immutable raw source notes.
- Trend Agent: computes daily, weekly, and monthly trend views from price action, volume, momentum, volatility, drawdown, and relative strength.
- Ticker Thesis Agent: updates ticker pages with thesis, catalysts, risks, stale claims, and confidence.
- Portfolio/Risk Agent: creates target allocations and validates a JSON order plan with `scripts/check-risk-policy.py`.
- Executor Agent: submits approved paper orders through Alpaca MCP only, using day limit stock orders.
- Wiki Curator Agent: updates cross-links, `wiki/index.md`, and `wiki/log.md`; flags contradictions instead of silently resolving them.
- Post-Trade Agent: verifies submitted orders, fills, positions, and buying power; writes execution outcomes back to the wiki.
- Trade Review Agent: reviews closed trades and still-held traded stocks against the original thesis, order plan, market context, and later outcomes; records what was right, what was wrong, and how recommendation policy should improve.

Use actual sub-agents when the runtime and user instruction allow parallel agent work. Otherwise, perform the roles sequentially and label the sections in the report.

## Risk Policy

The default policy is medium risk:

- Maximum invested after new orders: 80% of account portfolio value.
- Minimum cash reserve after new buy orders: 20% of account portfolio value.
- Maximum target exposure per ticker: 20% of account portfolio value.
- Maximum new orders per run: 10.
- Allowed assets: active tradable US stocks and ETFs only.
- Allowed order shape: long-only, whole-share, day limit orders.
- Quote freshness: for submit-mode runs, use quote/snapshot data captured within 20 minutes.
- Limit guardrail: buy/sell limit prices must be within 0.5% of the recorded reference price.

Always create or update an order-plan JSON before submitting orders, then run:

```bash
python3 scripts/check-risk-policy.py path/to/order-plan.json
```

If validation fails, do not submit orders. Write skipped orders and reasons into the daily report.

## Wiki Conventions

- Record all future wiki content, daily reports, ticker analyses, portfolio notes, raw-source summaries, and log entries in Korean by default. Keep ticker symbols, source titles, field names, tool names, and quoted source text in their original language when that improves traceability.
- `wiki/raw/sources/`: immutable source notes. Do not edit raw source pages after initial capture except to fix formatting that blocks parsing.
- `wiki/tickers/`: one page per ticker, named `SYMBOL.md`.
- `wiki/portfolio/`: account snapshots, allocation plans, and order plans.
- `wiki/reports/daily/`: daily run reports named `YYYY-MM-DD.md`.
- `wiki/reviews/trades/`: trade review notes, named `YYYY-MM-DD-SYMBOL-review.md` or `YYYY-MM-DD-portfolio-review.md`.
- `wiki/policies/recommendation-policy.md`: living policy distilled from trade reviews. Update it only with evidence-backed lessons, not one-off hindsight.
- `wiki/analyses/`: reusable cross-ticker or thematic analyses.
- `wiki/index.md`: content-oriented catalog. Read it first and update it after each run.
- `wiki/log.md`: append-only chronological log. Add a new `## [YYYY-MM-DD HH:MM TZ] type | title` entry for every run.

Use wiki links such as `[[AAPL]]`, `[[portfolio-current]]`, and `[[2026-05-22]]` where helpful, but keep plain Markdown readable without Obsidian.

## Trade Review And Policy Learning

- After any filled paper trade exists, future `거래 후 점검해줘`, `포트폴리오 점검해줘`, `리밸런싱 계획 짜줘`, and `오늘 분석해줘` runs should check whether a trade review is due.
- Review both closed positions and still-held traded stocks. For open positions, mark conclusions as interim.
- Compare the original recommendation with the actual later outcome using the wiki state that existed at decision time: ticker page, daily report, order plan, raw sources, account snapshot, market data, and risk policy.
- Record what worked, what failed, what was unknowable, and what should change in future recommendations.
- Do not rewrite old thesis pages to look smarter in hindsight. Add dated review sections or separate review pages.
- A single trade can suggest a hypothesis, but update `wiki/policies/recommendation-policy.md` only when the lesson is evidence-backed and clearly useful for future recommendations.

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
