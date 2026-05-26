---
id: 2026-05-27-0159-hourly-autopilot-sources
created_at: 2026-05-26T17:02:00Z
paper: true
run_id: 2026-05-27-0159-hourly-autopilot
---

# 2026-05-27 01:59 KST hourly autopilot sources

## 공통 확인

- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했다. API key 값은 출력하거나 기록하지 않았다.
- Scheduler research MCP preflight: `wiki/evidence-store/sources/2026-05-27-0159-hourly-autopilot-research-mcp-preflight.json`.
- FRED preflight row: `get_macro_snapshot` pass, checked_at `2026-05-26T16:59:29+00:00`.
- Firecrawl은 Codex tool catalog 검색에서 registered MCP tool이 노출되지 않았다. workflow 지시에 따라 shell/curl/local wrapper를 호출하지 않았고 `wrapper_error`로 분류했다.

## Alpaca MCP

| Core check | Tool | Outcome | Time / evidence | Gap category | Retry count | Note |
| --- | --- | --- | --- | --- | ---: | --- |
| clock | `get_clock` | pass | `2026-05-26T13:00:24.142399574-04:00`, `is_open=true`, next_close `2026-05-26T16:00:00-04:00` | not_applicable | 0 | 시장은 open으로 확인됐다. |
| account | `get_account_info` | failed | 2회 모두 MCP safety cancellation | cancelled | 1 | 첫 Alpaca core blocking gate. |
| positions | `get_all_positions` | failed | 2회 모두 MCP safety cancellation | cancelled | 1 | 현재 run의 submit gate에서 usable position state 없음. |
| open orders | `get_orders(status=open, asset_class=us_equity)` | failed | 2회 모두 MCP safety cancellation | cancelled | 1 | duplicate/open-order check를 확정할 수 없어 주문 금지. |
| recent activities | `get_account_activities(activity_types=[FILL], date=2026-05-26)` | pass | LLY buy 1주 filled `2026-05-26T16:02:35.719698Z`, FCX buy 1주 filled `2026-05-26T16:41:44.795048Z` | not_applicable | 0 | same-day fills 확인. |
| watchlists | `get_watchlists` | failed | `user cancelled MCP tool call` | cancelled | 0 | universe는 metadata + 기존 wiki position snapshot + benchmarks로 보수적으로 구성. |
| latest quotes | `get_stock_latest_quote(feed=iex)` | pass | quote time `2026-05-26T17:01:30Z` for requested symbols | not_applicable | 0 | fresh quote usable. |
| snapshot | `get_stock_snapshot(feed=iex)` | failed | `user cancelled MCP tool call` | cancelled | 0 | latest quote와 daily bars로만 판단. |
| daily bars | `get_stock_bars(feed=iex,timeframe=1Day,days=40,adjustment=all)` | pass | `SPY, QQQ, LLY, FCX, NOK, SMH, MU, AAPL, NVDA, AVGO, INTC, PLTR` | not_applicable | 0 | trend screen에 사용. |
| asset tradability | `get_asset(NOK)`, `get_asset(SMH)` | failed | MCP safety cancellation | cancelled | 0 | active/tradable hard gate 미확정. |
| latest trade | `get_stock_latest_trade(feed=iex)` | failed | `user cancelled MCP tool call` | cancelled | 0 | quote 기준 가격만 사용. |
| news | `get_news(symbols=NOK,SMH,FCX,LLY)` | pass | Benzinga NOK 52-week high, LLY vaccine acquisition/gene therapy, SMH/AI market context | not_applicable | 0 | current catalyst context. |

### Quote snapshot

| Symbol | Bid | Ask | Mid | Spread % | Quote time | Gate |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| SPY | 749.30 | 749.33 | 749.315 | 0.0040 | 2026-05-26T17:01:30Z | pass |
| QQQ | 728.05 | 728.09 | 728.070 | 0.0055 | 2026-05-26T17:01:30Z | pass |
| NOK | 16.54 | 16.55 | 16.545 | 0.0604 | 2026-05-26T17:01:30Z | pass |
| SMH | 597.56 | 597.71 | 597.635 | 0.0251 | 2026-05-26T17:01:30Z | pass |
| FCX | 63.90 | 63.91 | 63.905 | 0.0156 | 2026-05-26T17:01:30Z | pass |
| NVDA | 213.76 | 213.78 | 213.770 | 0.0094 | 2026-05-26T17:01:30Z | pass |
| AAPL | 310.02 | 310.20 | 310.110 | 0.0580 | 2026-05-26T17:01:30Z | pass |
| INTC | 121.16 | 121.19 | 121.175 | 0.0248 | 2026-05-26T17:01:30Z | pass |
| MU | 878.00 | 885.83 | 881.915 | 0.8878 | 2026-05-26T17:01:30Z | fail |
| LLY | 1079.15 | 1104.40 | 1091.775 | 2.3127 | 2026-05-26T17:01:30Z | fail |
| AVGO | 422.27 | 435.00 | 428.635 | 2.9699 | 2026-05-26T17:01:30Z | fail |
| PLTR | 133.70 | 137.29 | 135.495 | 2.6495 | 2026-05-26T17:01:30Z | fail |

## Research MCP

### SEC EDGAR

- Local CIK fallback used before lookup gap classification: `NOK -> 0000924613`.
- `get_company_info(identifier=0000924613)` pass: company `NOKIA CORP`, ticker `NOK`, fiscal year end `1231`.
- `get_recent_filings(identifier=0000924613, days=30, limit=5)` pass: recent filings include `6-K` on `2026-05-26`, `SD` on `2026-05-21`, `6-K` on `2026-05-20`, `6-K` on `2026-05-18`, `6-K` on `2026-05-13`.

### Yahoo Finance

- `get_yahoo_finance_news(ticker=NOK)` pass. Returned current headlines about Nokia stock more than doubling, AI infrastructure positioning, an AI networking lab, AI comeback valuation, and analyst AI moves.
- `get_recommendations(ticker=NOK, recommendation_type=recommendations, months_back=12)` pass. Current row: strongBuy 4, buy 4, hold 2, sell 1, strongSell 0.

### Alpha Vantage

- `TOOL_LIST` pass.
- `TOOL_GET("PING")` pass.
- `TOOL_CALL("PING", {})` pass: `pong`.
- Candidate data call followed required `TOOL_GET("NEWS_SENTIMENT")` immediately before `TOOL_CALL("NEWS_SENTIMENT", {"tickers":"NOK", ...})`, but the non-PING call was cancelled once. Per workflow, Alpha retries stopped and Alpha Vantage is classified `cancelled`.

### FRED

- Scheduler-owned preflight source exists at `wiki/evidence-store/sources/2026-05-27-0159-hourly-autopilot-research-mcp-preflight.json`.
- Provider row `fred` has `outcome=pass` for `get_macro_snapshot`; this run counted it as queried/usable FRED macro evidence.
- Snapshot included DGS10 `4.57` on `2026-05-21`, DGS2 `4.08` on `2026-05-21`, FEDFUNDS `3.64` for `2026-04-01`, CPIAUCSL `332.407` for `2026-04-01`, UNRATE `4.3` for `2026-04-01`, and NFCI `-0.52300` on `2026-05-15`.

## Universe and decision notes

- Broad metadata universe: 62 symbols from `harness/symbol-metadata.yaml`, plus `SPY` and `QQQ`.
- Alpaca watchlists could not be queried because `get_watchlists` was cancelled, so watchlist contribution is recorded as an Alpaca core data gap.
- Pre-MCP shortlist: `NOK`, `SMH`, `FCX`, `NVDA`, `AAPL`, `INTC`, `MU`, `LLY`, `AVGO`, `PLTR`.
- Final research candidates: `NOK`, `SMH`, `FCX`.
- First blocking gate: `alpaca_account`. Because account, positions, open orders, and asset tradability were not usable, no order was submitted even though market clock and quotes were fresh.
