# 2026-05-27-0331-hourly-autopilot sources

- 조회 시각: 2026-05-26T18:34:56Z
- 실행 유형: scheduled hourly-autopilot, no-submit failure path
- Paper mode gate: nested shell에서 `ALPACA_PAPER_TRADE=true`가 확인되지 않아 첫 hard blocking gate를 `paper_mode_env_missing`으로 기록했다. 주문 제출 도구는 호출하지 않았다.

## Alpaca MCP preflight

- Source ref: `wiki/evidence-store/sources/2026-05-27-0331-hourly-autopilot-alpaca-core-preflight.json`
- Scheduler-owned read-only MCP stdio preflight hard gate: `pass`
- Market clock: `2026-05-26T14:31:10.242063192-04:00`, is_open `True`, next_close `2026-05-26T16:00:00-04:00`
- Account: portfolio_value 101621.09, cash 42657.04, buying_power 137380.24
- Positions: 12개
- Open orders: 1개. AAPL buy open order `hourly-20260527-0251-aapl-buy-1` 유지.
- Quote capture: `2026-05-26T18:31:33Z`. AMZN/INTC/SMH quote rows were less than 20 minutes old at decision time.

## Research MCP attempts

- SEC EDGAR: local CIK fallback에서 AMZN `0001018724`, INTC `0000050863` 확인. SMH는 ETF로 local CIK cache에 없음. Registered SEC EDGAR MCP `get_recommended_tools` attempt가 `user cancelled MCP tool call`을 반환해 `gap_category=cancelled`로 분류했다.
- Alpha Vantage: `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` health check pass. `TOOL_GET("NEWS_SENTIMENT")` 후 첫 non-PING `TOOL_CALL("NEWS_SENTIMENT")`이 cancelled되어 `gap_category=cancelled`로 분류하고 추가 Alpha function은 시도하지 않았다.
- FRED: scheduler-owned research preflight `wiki/evidence-store/sources/2026-05-27-0331-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable macro evidence로 사용했다.
- Firecrawl: Codex tool catalog에 registered Firecrawl MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 분류했다. shell/curl/local wrapper는 호출하지 않았다.
- Yahoo Finance: registered MCP `get_yahoo_finance_news(AMZN)` returned usable news headlines, including current AMZN growth/AI-market context. Used only as supplemental source evidence.

## Candidate quote rows

| Symbol | Bid | Ask | Spread % | Quote time | Gate |
| --- | ---: | ---: | ---: | --- | --- |
| AMZN | 263.26 | 263.29 | 0.0114 | 2026-05-26T18:31:31.02721451Z | pass |
| INTC | 122.39 | 122.42 | 0.0245 | 2026-05-26T18:31:32.126892757Z | pass |
| SMH | 600.18 | 600.47 | 0.0483 | 2026-05-26T18:31:32.580431757Z | pass |
| AAPL | 309.6 | 310.2 | 0.1936 | 2026-05-26T18:31:32.324221533Z | pass |
| MU | 906.81 | 912.5 | 0.6255 | 2026-05-26T18:31:32.617881386Z | fail |
| NVDA | 213.74 | 213.77 | 0.014 | 2026-05-26T18:31:32.658801539Z | pass |
| FCX | 64.17 | 64.19 | 0.0312 | 2026-05-26T18:31:31.246506057Z | pass |
| NOK | 16.42 | 16.43 | 0.0609 | 2026-05-26T18:31:32.506175072Z | pass |
| LLY | 1073 | 1081.96 | 0.8316 | 2026-05-26T18:31:32.400101831Z | fail |
| AMD | 498.51 | 500 | 0.2984 | 2026-05-26T18:31:30.823815325Z | pass |

## Data gaps

- `paper_mode_env_missing`: nested Codex environment did not expose `ALPACA_PAPER_TRADE=true`; this blocks all submit action regardless of market, quote, universe, or research evidence.
- `sec-edgar`: cancelled.
- `alpha-vantage`: cancelled on first non-PING candidate data call.
- `firecrawl`: wrapper_error because no registered Codex Firecrawl tool was exposed.
