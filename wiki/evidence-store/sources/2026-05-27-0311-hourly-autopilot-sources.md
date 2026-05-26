# 2026-05-27-0311-hourly-autopilot sources

## Run context

- 실행 시각: 2026-05-27 03:11 KST scheduled paper autopilot.
- Paper mode: `.env`에서 `ALPACA_PAPER_TRADE=true` 확인. API key 값은 출력하거나 기록하지 않음.
- Workflow: `harness/workflows/hourly-autopilot.md`.
- Scheduler Alpaca core preflight: `wiki/evidence-store/sources/2026-05-27-0311-hourly-autopilot-alpaca-core-preflight.json`. SHA256 `9a1b8b41205ceb23361897ed4b600ceb8810097903099ed8a2e212e424589cb7`.
- Scheduler research preflight: `wiki/evidence-store/sources/2026-05-27-0311-hourly-autopilot-research-mcp-preflight.json`. SHA256 `31a434aed3effe5282ae6d73ef7dea142a0e4cff758369a96552eb5269465aae`.

## Alpaca MCP core evidence

- Preflight hard gate: pass.
- Market clock: `2026-05-26T14:11:10.836217373-04:00` 기준 open=`True`, next close `2026-05-26T16:00:00-04:00`.
- Account: portfolio value `101639.85`, cash `42657.04`, buying power `137384.96`.
- Positions: 12개.
- Open orders: 1개. AAPL open buy order `hourly-20260527-0251-aapl-buy-1`, status `new`, qty 1, limit 309.46.
- Recent fills: same-day LLY, FCX, NOK, NVDA buy fills present in preflight account activities.
- Quote rows: preflight latest quote rows are captured at `2026-05-26T18:11:34Z` to `2026-05-26T18:11:35Z`, less than 20 minutes old at decision time.

## Shortlist quote/spread evidence

| Ticker | Bid | Ask | Spread % | Quote time | Decision |
| --- | ---: | ---: | ---: | --- | --- |
| AMZN | 263.04 | 263.08 | 0.0152 | 2026-05-26T18:11:34.188261533Z | recheck |
| INTC | 122.58 | 122.63 | 0.0408 | 2026-05-26T18:11:34.097563488Z | recheck |
| SMH | 599.42 | 599.7 | 0.0467 | 2026-05-26T18:11:34.721573468Z | recheck |
| AAPL | 309.66 | 309.69 | 0.0097 | 2026-05-26T18:11:34.366705084Z | skip: existing open buy order |
| MU | 896.49 | 900.8 | 0.4796 | 2026-05-26T18:11:34.339342451Z | recheck, near spread ceiling |

## Research MCP evidence and gaps

- FRED: scheduler-owned research preflight row `get_macro_snapshot` pass. Used as macro evidence.
- Alpha Vantage: `TOOL_LIST` pass, `TOOL_GET("PING")` pass, `TOOL_CALL("PING", {})` returned `pong`. `TOOL_GET("NEWS_SENTIMENT")` immediately preceded the candidate call. First non-PING `TOOL_CALL("NEWS_SENTIMENT", {"tickers":"AMZN,INTC","sort":"LATEST","limit":10})` was cancelled by the wrapper, so Alpha retries stopped and `gap_category=cancelled`.
- SEC EDGAR: local CIK fallback checked before provider classification. `AMZN -> 0001018724`, `INTC -> 0000050863`, `SMH` absent as ETF/lookup gap. SEC MCP `get_financials` for AMZN/INTC cancelled, with one retry for AMZN also cancelled. `gap_category=cancelled`.
- Yahoo Finance: `get_recommendations(AMZN, recommendations, 3 months)` pass. Current row shows 15 strongBuy, 47 buy, 4 hold, 0 sell, 0 strongSell. `get_yahoo_finance_news(AMZN)` cancelled, but provider has a usable recommendations row.
- Firecrawl: no registered Firecrawl MCP tool was exposed in Codex tool catalog; local wrapper/curl was not called. `gap_category=wrapper_error`.

## Data gap classification

| Provider | Outcome | Gap category | Retry count | Detail |
| --- | --- | --- | ---: | --- |
| alpaca | pass | not_applicable | 2 | preflight hard gate pass |
| sec-edgar | failed | cancelled | 1 | local CIK fallback succeeded for AMZN/INTC, MCP calls cancelled |
| alpha-vantage | failed | cancelled | 0 | first non-PING candidate call cancelled after health pass |
| fred | pass | not_applicable | 0 | research preflight macro snapshot pass |
| firecrawl | failed | wrapper_error | 0 | registered tool not exposed; shell/curl prohibited |
| yahoo-finance | usable | not_applicable | 0 | AMZN recommendations pass, news call cancelled |
