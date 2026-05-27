---
id: 2026-05-27-2246-hourly-autopilot-sources
created_at: 2026-05-27T13:49:30Z
source_type: scheduler_mcp_preflight_summary
workflow: hourly-autopilot
paper: true
---

# 2026-05-27 22:46 KST hourly autopilot sources

## Scheduler Alpaca core preflight

- Source ref: `wiki/evidence-store/sources/2026-05-27-2246-hourly-autopilot-alpaca-core-preflight.json`
- Market clock: open at `2026-05-27T09:46:40.303390074-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Account: portfolio value 100985.47 USD, cash 42347.59 USD, buying power 137078.27 USD, long market value 58637.88 USD.
- Positions: 13 long US-equity positions, no shorts in the preflight.
- Open orders: 0 after scheduler stale-order cleanup.
- Quote universe: 62 symbols via Alpaca IEX latest quote/snapshot/trade rows.

## Stale order cleanup

- Source ref: `wiki/evidence-store/sources/2026-05-27-2246-hourly-autopilot-stale-order-cleanup.json`
- Status: `pass`. Initial open orders 0, stale candidates 0, remaining open orders 0.
- No stale unfilled autopilot order remained, so `risk_open_order_lifecycle` did not block this cycle.

## Scheduler research MCP preflight

- Source ref: `wiki/evidence-store/sources/2026-05-27-2246-hourly-autopilot-research-mcp-preflight.json`
- Symbols: NKE, AMZN, SPY, PLTR, PFE, RGTI, NVDA, SO, NOK, SLB, QBTS, FCX.
- Coverage: SEC EDGAR pass, Alpha Vantage gap/empty_response, FRED pass, Firecrawl pass, Yahoo Finance pass.
- Usable research confirmations: 4 of 5, above the tiered gate minimum of 3.

## Shortlist quote table

| Symbol | Day change % | Bid | Ask | Spread % | Quote timestamp | Note |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| NKE | 2.90 | 46.24 | 46.25 | 0.0216 | `2026-05-27T13:47:04.911676934Z` | consumer discretionary breadth and low spread; no existing position |
| PFE | 2.44 | 26.45 | 26.46 | 0.0378 | `2026-05-27T13:47:04.92045847Z` | defensive healthcare diversification and low spread; no existing position |
| SO | 0.32 | 94.46 | 94.52 | 0.0635 | `2026-05-27T13:47:04.73683734Z` | utility defensive diversification and low spread; no existing position |
| AMZN | 0.59 | 266.86 | 266.94 | 0.0300 | `2026-05-27T13:47:04.304389311Z` | strong research confirmation but same-day canceled/expired validation history; deprioritized for new diversification |
| SPY | -0.12 | 749.67 | 749.69 | 0.0027 | `2026-05-27T13:47:05.813777219Z` | benchmark only |
| PLTR | -2.83 | 132.89 | 132.95 | 0.0451 | `2026-05-27T13:47:05.126160278Z` | speculative flag and negative intraday move |
| SLB | -2.98 | 56.18 | 56.24 | 0.1067 | `2026-05-27T13:47:05.687987657Z` | energy candidate but negative intraday move |
| FCX | -1.48 | 63.31 | 63.36 | 0.0789 | `2026-05-27T13:47:04.332858001Z` | already bought today and negative intraday move |
| NVDA | -1.73 | 211.06 | 211.14 | 0.0379 | `2026-05-27T13:47:05.004257842Z` | already bought today and AI semiconductor exposure already high |
| NOK | -5.29 | 15.58 | 15.59 | 0.0642 | `2026-05-27T13:47:04.679019344Z` | already large position and sharp negative intraday move |

## Data gaps

- Alpha Vantage returned an `empty_response` gap for candidate `NEWS_SENTIMENT`; it was queried and not used in score.
- SEC EDGAR provider row is accepted from the scheduler-owned preflight per workflow instruction; local CIK fallback was available for the listed company symbols.
- No shell/curl/local network helper was used for current-market data in nested Codex.
