---
id: 2026-05-27-0226-hourly-autopilot-sources
created_at: 2026-05-26T17:31:00Z
paper: true
run_id: 2026-05-27-0226-hourly-autopilot
---

# 2026-05-27 02:26 KST hourly autopilot sources

## Alpaca MCP core preflight

- Source ref: `wiki/evidence-store/sources/2026-05-27-0226-hourly-autopilot-alpaca-core-preflight.json`
- Scheduler-owned read-only Alpaca MCP stdio preflight.
- Hard gate: pass.
- Clock: `2026-05-26T13:26:42.969065887-04:00`, market open, next close `2026-05-26T16:00:00-04:00`.
- Account: portfolio value `101643.29`, cash `42870.76`, buying power `137899.56`, long market value `58772.53`, short market value `0`.
- Open orders: 0.
- Recent same-day fills: LLY 1주 buy, FCX 1주 buy, NOK 1주 buy.
- Current positions: AMD, AVGO, ETN, FCX, IONQ, LLY, LRCX, NOK, NVDA, RGTI, TSM, UNH.
- Asset checks: 62/62 symbols active/tradable US equities or ETFs.
- Quote feed: Alpaca MCP IEX latest quote/snapshot/latest trade, 62/62 symbols pass.

## 후보 quote/spread

| 티커 | Bid | Ask | Mid | Spread | Quote time | 판단 |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| NVDA | 213.48 | 213.72 | 213.60 | 0.1124% | 2026-05-26T17:27:05.819127537Z | pass |
| SMH | 597.16 | 597.46 | 597.31 | 0.0502% | 2026-05-26T17:27:06.402267931Z | pass |
| AAPL | 309.27 | 309.33 | 309.30 | 0.0194% | 2026-05-26T17:27:05.715758558Z | pass |
| INTC | 120.99 | 121.03 | 121.01 | 0.0331% | 2026-05-26T17:27:03.486939328Z | pass |
| MU | 887.46 | 895.00 | 891.23 | 0.8460% | 2026-05-26T17:27:06.099399925Z | spread fail |
| FCX | 63.96 | 63.98 | 63.97 | 0.0313% | 2026-05-26T17:27:06.030963942Z | same-day duplicate buy skip |
| NOK | 16.46 | 16.47 | 16.465 | 0.0607% | 2026-05-26T17:27:05.680914117Z | same-day duplicate buy skip |
| LLY | 1077.00 | 1078.39 | 1077.695 | 0.1290% | 2026-05-26T17:27:04.527227087Z | same-day duplicate buy skip |

## SEC EDGAR MCP

- Local ticker map fallback: `harness/sec-ticker-cik-map.json` contains `NVDA -> 0001045810`.
- `get_company_info(identifier=0001045810)`: pass. Company `NVIDIA CORP`, CIK `1045810`, ticker `NVDA`, SIC `3674`, fiscal year end `0131`.
- `get_recent_filings(identifier=0001045810, days=30, limit=5)`: pass. Recent filings include 2026-05-20 `10-Q` accession `0001045810-26-000052`, 2026-05-20 `8-K` accession `0001045810-26-000051`, 2026-05-15 `SD`, 2026-05-15 `13F-HR`, and 2026-05-14 Form `3`.

## Alpha Vantage MCP

- `TOOL_LIST`: pass.
- `TOOL_GET("PING")`: first attempt cancelled, second attempt pass.
- `TOOL_CALL("PING", {})`: cancelled.
- Per workflow, Alpha Vantage is recorded as `outcome=failed`, `gap_category=cancelled`, `retry_count=1`, and not used in the score. No non-PING candidate `TOOL_CALL` was attempted after cancelled health check.

## FRED MCP

- Source ref: `wiki/evidence-store/sources/2026-05-27-0226-hourly-autopilot-research-mcp-preflight.json`
- Scheduler-owned research preflight has `fred` `get_macro_snapshot` pass at `2026-05-26T17:27:08+00:00`.
- Latest rows in the preflight: DGS10 4.57 on 2026-05-21, DGS2 4.08 on 2026-05-21, FEDFUNDS 3.64 for 2026-04-01, CPIAUCSL 332.407 for 2026-04-01, UNRATE 4.3 for 2026-04-01, NFCI -0.52300 for 2026-05-15.

## Firecrawl MCP

- Codex tool catalog did not expose a registered Firecrawl MCP namespace.
- Per workflow, no shell wrapper, helper script, or curl fallback was used.
- Coverage row: `outcome=failed`, `gap_category=wrapper_error`.

## Yahoo Finance MCP

- `get_yahoo_finance_news(ticker=NVDA)`: pass. Returned current technology/AI-market news including Nvidia-related market momentum and AI boom context.
- `get_recommendations(ticker=NVDA, recommendation_type=recommendations, months_back=12)`: pass. Current period row returned `strongBuy=10`, `buy=49`, `hold=2`, `sell=1`, `strongSell=0`.

## 데이터 공백

| MCP | Gap category | Retry count | 설명 |
| --- | --- | ---: | --- |
| alpha-vantage | cancelled | 1 | `TOOL_CALL("PING", {})` cancelled. Health check 미통과라 후보 데이터 호출 중단. |
| firecrawl | wrapper_error | 0 | 등록 MCP tool이 Codex tool catalog에 노출되지 않음. |

