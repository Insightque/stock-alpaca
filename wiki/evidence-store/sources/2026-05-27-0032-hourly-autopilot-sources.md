---
id: 2026-05-27-0032-hourly-autopilot-sources
created_at: 2026-05-26T15:43:00Z
timezone: Asia/Seoul
source_type: mcp-run-summary
immutable: true
---

# 2026-05-27 00:32 KST hourly autopilot sources

## 조회 범위

- Workflow: `harness/workflows/hourly-autopilot.md`
- 기준 시각: 2026-05-26 11:33-11:41 EDT / 2026-05-27 00:33-00:41 KST
- Universe: `harness/symbol-metadata.yaml` 62개 + 현재 보유 종목 + Alpaca watchlists + `SPY`, `QQQ`
- Alpaca watchlists: `[]`
- Pre-MCP shortlist: `MU`, `AMD`, `KLAC`, `SMH`, `INTC`, `AAPL`, `LLY`, `NOK`, `ASML`, `AMAT`
- Final candidates: `LLY`, `AMD`, `MU`

## Alpaca MCP

| Check | Tool | Outcome | Evidence |
| --- | --- | --- | --- |
| paper mode | `.env` 확인 | pass | `ALPACA_PAPER_TRADE=true` 존재. 키 값은 출력하지 않음 |
| market clock | `get_clock` | pass | `is_open=true`, timestamp `2026-05-26T11:33:01.929849596-04:00`, next close `2026-05-26T16:00:00-04:00` |
| account | `get_account_info` | pass | ACTIVE, portfolio value 101264.45 USD, cash 44030.58 USD, buying power 138855.03 USD |
| open orders | `get_orders(status=open, asset_class=us_equity)` | pass | `[]` |
| positions | `get_all_positions` | pass | 10개 long positions, long market value 57233.87 USD |
| same-day fills | `get_account_activities(activity_types=FILL, date=2026-05-26)` | pass | `[]` |
| watchlists | `get_watchlists` | pass | `[]` |
| broad snapshot | `get_stock_snapshot(62 symbols, IEX)` | pass | 62개 metadata universe 대상으로 current quote, daily bar, previous daily bar 수신 |
| shortlist bars | `get_stock_bars(MU,AMD,KLAC,SMH,INTC,AAPL,LLY,ASML,SPY,QQQ, 1Day, 45d, IEX, adjusted)` | pass | daily/weekly/monthly trend 계산에 사용 |
| candidate quotes | `get_stock_latest_quote(MU,AMD,KLAC,SMH,INTC,AAPL,LLY,NOK,ASML,AMAT,LRCX,ETN)` | pass | quote timestamp `2026-05-26T15:35:22Z`-`15:35:39Z` |
| asset checks | `get_asset(LLY/AMD/MU)` | pass | 세 후보 모두 active/tradable US equity. Whole-share stock order만 허용 가능 |
| market movers | `get_market_movers(stocks, top=10)` | usable | 2026-05-26T15:41:00Z 기준 top gainers는 대부분 저가/투기 종목이라 제외 |
| most active | `get_most_active_stocks(volume, top=10)` | usable | `NOK`가 most active에 포함됐지만 이미 보유 중이며 신규 buy 우선순위는 낮음 |
| news | `get_news(LLY,AMD,MU,AAPL,SMH,INTC)` | usable | MU/AMD/INTC AI 반도체, LLY gene therapy headline 확인 |

## Quote and spread evidence

| Symbol | quote_time_utc | bid | ask | mid | spread_pct | Gate |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| MU | 2026-05-26T15:35:39Z | 876.64 | 877.07 | 876.855 | 0.049 | pass |
| AMD | 2026-05-26T15:35:39Z | 491.27 | 493.00 | 492.135 | 0.352 | pass |
| KLAC | 2026-05-26T15:35:22Z | 1968.93 | 1984.14 | 1976.535 | 0.770 | fail |
| SMH | 2026-05-26T15:35:39Z | 597.46 | 597.89 | 597.675 | 0.072 | pass |
| INTC | 2026-05-26T15:35:39Z | 122.65 | 122.72 | 122.685 | 0.057 | pass |
| AAPL | 2026-05-26T15:35:39Z | 311.50 | 311.54 | 311.520 | 0.013 | pass |
| LLY | 2026-05-26T15:35:37Z | 1077.04 | 1080.00 | 1078.520 | 0.274 | pass |
| NOK | 2026-05-26T15:35:38Z | 16.05 | 16.06 | 16.055 | 0.062 | pass |
| ASML | 2026-05-26T15:35:29Z | 1607.12 | 1628.10 | 1617.610 | 1.297 | fail |
| AMAT | 2026-05-26T15:35:24Z | 449.24 | 454.00 | 451.620 | 1.054 | fail |
| LRCX | 2026-05-26T15:35:39Z | 303.85 | 326.00 | 314.925 | 7.034 | fail |
| ETN | 2026-05-26T15:35:39Z | 407.15 | 412.00 | 409.575 | 1.184 | fail |

## Trend evidence from Alpaca bars

| Symbol | daily_return | 5D/near-week | 20D/near-month | 45D window | Note |
| --- | ---: | ---: | ---: | ---: | --- |
| MU | +16.77% | +25.46% | +73.9% | +105.5% | 최고 모멘텀이나 과열/되돌림 위험도 가장 큼 |
| AMD | +5.09% | +18.65% | +52.1% | +99.1% | 이미 보유 중인 AI semiconductor 핵심 exposure |
| LLY | +1.10% | +5.50% | +23.5% | +16.1% | 헬스케어 성장주로 cluster 분산 효과 |
| SMH | +3.75% | +9.87% | +21.6% | +34.7% | spread는 좋지만 기존 semiconductor cluster와 중복 |
| AAPL | +0.85% | +4.11% | +15.1% | +20.3% | 안정적이나 당일 catalyst 강도는 낮음 |
| SPY | +0.57% | +2.19% | +5.37% | +9.31% | broad benchmark |
| QQQ | +1.50% | +3.81% | +10.74% | +17.97% | growth benchmark |

## SEC EDGAR MCP

- Local ticker-to-CIK cache `harness/sec-ticker-cik-map.json` was checked before SEC lookup classification.
- Cache rows: `LLY=0000059478`, `AMD=0000002488`, `MU=0000723125`; `SMH` is absent because it is an ETF and is treated as ticker lookup `empty_response`, not provider failure.
- `get_company_info(LLY)` returned success for ELI LILLY & Co, CIK 59478.
- `get_recent_filings(LLY, days=90, limit=5)` returned 5 filings, including 2026-05-20 8-K, Form 144, and Form 4 filings.
- `get_company_info(AMD)` returned success for ADVANCED MICRO DEVICES INC, CIK 2488.
- `get_recent_filings(AMD, days=90, limit=5)` returned recent Form 4 and Form 144 filings, including 2026-05-22 Form 4.
- `get_company_info(MU)` returned success for MICRON TECHNOLOGY INC, CIK 723125.
- `get_recent_filings(MU, days=90, limit=5)` returned recent SD, Schedule 13G/A, Form 4, and Form 144 filings.

## Alpha Vantage MCP

- Required sequence was followed: `TOOL_LIST` -> `TOOL_GET(EARNINGS)` -> `TOOL_CALL(EARNINGS, LLY)`.
- `TOOL_LIST` returned available tools including `EARNINGS`, `COMPANY_OVERVIEW`, `EARNINGS_CALENDAR`, `GLOBAL_QUOTE`, `NEWS_SENTIMENT`, and macro functions.
- `TOOL_GET(EARNINGS)` returned schema requiring `symbol`.
- `TOOL_CALL(EARNINGS, {"symbol":"LLY"})` was cancelled by the MCP safety wrapper, which incorrectly reported that `TOOL_GET` had not been performed.
- Retry sequence used `TOOL_GET(COMPANY_OVERVIEW)` then `TOOL_CALL(COMPANY_OVERVIEW, {"symbol":"LLY"})`; the call was also cancelled by the wrapper for the same sequence-detection reason.
- Gap classification: `gap_category=cancelled`, `retry_count=2`.

## Yahoo Finance MCP

- `get_stock_info(LLY)` returned usable company, valuation, analyst, and market fields. Key fields: Healthcare / Drug Manufacturers - General, current price around 1076.675 USD, forward PE 24.211088, recommendation key `buy`, 29 analyst opinions, target mean price 1211.0344, market state `REGULAR`.
- `get_recommendations(LLY, recommendations, 12)` returned current-period analyst mix: strongBuy 6, buy 18, hold 6, sell 1, strongSell 0.
- `get_yahoo_finance_news(LLY)` returned current/news context including vaccine-developer acquisitions, GLP-1 competitive context, and LLY investor-attention headlines.
- `get_stock_info(AMD)` returned usable Technology / Semiconductors fields, recommendation key `strong_buy`, 48 analyst opinions, and market state `REGULAR`.
- `get_recommendations(AMD, recommendations, 12)` returned current-period analyst mix: strongBuy 5, buy 36, hold 10, sell 0, strongSell 0.
- `get_yahoo_finance_news(AMD)` returned AI semiconductor and Micron-led chip rally context.
- `get_stock_info(MU)` returned usable Technology / Semiconductors fields, recommendation key `strong_buy`, 40 analyst opinions, and market state `REGULAR`.
- `get_recommendations(MU, recommendations, 12)` returned current-period analyst mix: strongBuy 9, buy 30, hold 4, sell 1, strongSell 0.
- `get_yahoo_finance_news(MU)` returned UBS/AI-memory rally and $1T market-cap headlines.

## FRED MCP

- `scripts/mcp-fred.sh --health-check` was attempted 3 times.
- All attempts failed with `curl: (6) Could not resolve host: api.stlouisfed.org`.
- Read-only probe to `https://api.stlouisfed.org/fred/series?series_id=DGS10` also failed DNS resolution.
- Gap classification: `gap_category=dns`, `retry_count=2`.

## Firecrawl MCP

- `scripts/mcp-firecrawl.sh --health-check` was attempted 3 times.
- All attempts failed with `curl: (6) Could not resolve host: api.firecrawl.dev`.
- Read-only probe to `https://api.firecrawl.dev/v2` also failed DNS resolution.
- Gap classification: `gap_category=dns`, `retry_count=2`.

## Decision note

- Alpaca core gate passed and the market was open.
- Research MCP usable confirmations were SEC EDGAR and Yahoo Finance only. Alpha Vantage, FRED, and Firecrawl were attempted but unusable.
- The first blocking gate for submission was `mcp_research_min_confirmations`: 2 usable/pass research providers, below the required 3.
- No Alpaca order submission tool was called.
