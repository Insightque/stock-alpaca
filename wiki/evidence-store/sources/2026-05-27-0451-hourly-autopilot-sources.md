---
id: 2026-05-27-0451-hourly-autopilot-sources
created_at: 2026-05-26T19:53:30Z
run_id: 2026-05-27-0451-hourly-autopilot
paper: true
---

# 2026-05-27 04:51 KST Hourly Autopilot Sources

## Alpaca Core MCP

- Source ref: `wiki/evidence-store/sources/2026-05-27-0451-hourly-autopilot-alpaca-core-preflight.json`
- Scheduler-owned read-only Alpaca MCP stdio preflight was read before any Alpaca read-only call.
- Hard gate summary: `pass`; first blocking Alpaca core gate: none.
- Clock: market open, timestamp `2026-05-26T15:51:09.581579613-04:00`, next close `2026-05-26T16:00:00-04:00`.
- Account: portfolio value 101738.22 USD, cash 42347.59 USD, buying power 137240.29 USD, long market value 59390.63 USD.
- Positions: 13 long US equity positions.
- Open orders: AMZN buy 1 share, limit 263.10, client_order_id `hourly-20260527-0411-amzn-buy-1`, status `new`, filled_qty 0, submitted_at `2026-05-26T19:19:07.535085886Z`.
- Same-day fills visible in the preflight: LLY, FCX, NOK, NVDA, AAPL validation buys.
- Quote rows were captured around `2026-05-26T19:51:31Z` to `2026-05-26T19:51:34Z`; decision time quote age was under 20 minutes.

## Universe Screen

- Universe source: `harness/symbol-metadata.yaml`, current Alpaca positions, Alpaca preflight universe, `SPY`, `QQQ`.
- Symbols considered/loaded: 62/62.
- Pre-MCP shortlist: MU, AMD, KLAC, NOK, LRCX, AMAT, SMH, FCX, GE, INTC.
- Final candidates: INTC, SMH, AMAT.
- Candidate quote/spread examples from Alpaca preflight:
  - INTC bid 123.30, ask 123.38, spread 0.0649%, quote time `2026-05-26T19:51:32.634964759Z`.
  - SMH bid 602.47, ask 602.55, spread 0.0133%, quote time `2026-05-26T19:51:33.718043501Z`.
  - AMAT bid 454.87, ask 455.08, spread 0.0462%, quote time `2026-05-26T19:51:31.669250974Z`.

## SEC EDGAR MCP

- Local ticker-to-CIK fallback was checked first: `INTC -> 0000050863` in `harness/sec-ticker-cik-map.json`.
- Registered SEC EDGAR MCP `get_company_info(identifier="0000050863")` returned `INTEL CORP`, CIK 50863, ticker INTC.
- Registered SEC EDGAR MCP `get_recent_filings(identifier="0000050863", days=30, limit=5)` returned 5 recent filings, including Form 3 filings dated 2026-05-22 and Form 4 filings dated 2026-05-15.
- Coverage outcome: pass.

## Yahoo Finance MCP

- Registered Yahoo Finance MCP `get_yahoo_finance_news(ticker="INTC")` returned current INTC-related news, including Intel foundry/government-windfall coverage and Nvidia competitive-risk coverage.
- Registered Yahoo Finance MCP `get_recommendations(ticker="INTC", recommendation_type="recommendations", months_back=12)` returned current recommendation distribution: strongBuy 2, buy 11, hold 30, sell 2, strongSell 3.
- Coverage outcome: usable.

## Alpha Vantage MCP

- Registered Alpha Vantage MCP sequence:
  - `TOOL_LIST`: pass.
  - `TOOL_GET("PING")`: pass.
  - `TOOL_CALL("PING", {})`: pass, returned `pong`.
  - `TOOL_GET("NEWS_SENTIMENT")`: cancelled by wrapper before candidate `TOOL_CALL`.
- Per workflow instruction, no additional Alpha candidate function was attempted after the cancellation.
- Coverage outcome: failed; `gap_category=cancelled`.

## FRED MCP

- Source ref: `wiki/evidence-store/sources/2026-05-27-0451-hourly-autopilot-research-mcp-preflight.json`
- Scheduler-owned research MCP preflight contained passing FRED `get_macro_snapshot` evidence.
- Snapshot included DGS10 4.57 on 2026-05-21, DGS2 4.08 on 2026-05-21, FEDFUNDS 3.64 for 2026-04-01, CPIAUCSL 332.407 for 2026-04-01, UNRATE 4.3 for 2026-04-01, and NFCI -0.52300 for 2026-05-15.
- Coverage outcome: pass.

## Firecrawl MCP

- Codex tool catalog search did not expose a registered Firecrawl MCP tool.
- Shell/curl/local wrapper use was prohibited for this run, so `scripts/mcp-firecrawl.sh` and `curl` were not called.
- Coverage outcome: failed; `gap_category=wrapper_error`.

## Decision And Risk Gate

- Research confirmations usable/pass: SEC EDGAR, FRED, Yahoo Finance = 3.
- Alpaca core, universe, quote freshness, and candidate spread passed.
- Risk gate blocked submit because existing AMZN open order age was about 34.4 minutes at decision time, exceeding `risk_policy.order_lifecycle.max_open_order_age_minutes=30`.
- No `place_stock_order` call was made.
