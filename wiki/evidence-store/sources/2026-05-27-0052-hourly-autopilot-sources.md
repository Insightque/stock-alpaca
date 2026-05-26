# 2026-05-27 00:52 KST hourly autopilot sources

이 원천 노트는 2026-05-27 00:52 KST hourly paper autopilot 실행의 불변 캡처 요약이다. API key 값은 기록하지 않았다.

## Paper mode

- `.env`: `ALPACA_PAPER_TRADE=true`
- Workflow: `harness/workflows/hourly-autopilot.md`
- Preflight: `wiki/evidence-store/sources/2026-05-27-0051-hourly-autopilot-research-mcp-preflight.json`

## Alpaca core MCP

- `get_clock`: pass. `timestamp=2026-05-26T11:52:30.285714984-04:00`, `is_open=true`, `next_close=2026-05-26T16:00:00-04:00`.
- `get_account_info`: pass. `portfolio_value=101003.86`, `cash=44030.58`, `buying_power=138599.44`, `status=ACTIVE`, `trading_blocked=false`.
- `get_orders(status=open, asset_class=us_equity)`: pass. Open equity orders 0.
- `get_all_positions`: first attempt cancelled, retry pass. Positions 10: AMD, AVGO, ETN, IONQ, LRCX, NOK, NVDA, RGTI, TSM, UNH. Retry count 1.
- `get_account_activities(activity_types=FILL, after=2026-05-26)`: pass. Same-day fills 0.
- `get_watchlists`: pass. Watchlists 0.
- First Alpaca core blocking gate: none.

## Universe and market data

- Universe source: `harness/symbol-metadata.yaml` plus current positions, Alpaca watchlists, `SPY`, `QQQ`.
- Symbols loaded/screened: 62. Required benchmarks `SPY` and `QQQ` included.
- Alpaca `get_stock_bars` IEX adjusted 1Day, 40-day lookback: pass for the broad universe.
- Alpaca `get_most_active_stocks(by=volume, top=20)`: pass. Notable metadata-universe names in the returned most-active set included `NOK`, `NVDA`, `INTC`, and `RGTI`.
- Pre-MCP shortlist: `MU`, `AMD`, `LLY`, `NOK`, `FCX`, `SMH`, `INTC`, `AAPL`, `LRCX`, `NVDA`.
- Final research candidates: `LLY`, `FCX`, `NOK`.

## Candidate quote/spread gate

Alpaca `get_stock_latest_quote` and `get_stock_snapshot` used IEX feed. Quote freshness was within 20 minutes.

| Symbol | Bid | Ask | Mid/ref | Spread % | Gate |
| --- | ---: | ---: | ---: | ---: | --- |
| LLY | 1078.87 | 1080.00 | 1079.435 | 0.105 | pass |
| FCX | 63.89 | 63.91 | 63.90 | 0.031 | pass |
| NOK | 16.00 | 16.01 | 16.005 | 0.062 | pass |
| SMH | 592.07 | 592.43 | 592.25 | 0.061 | pass |
| INTC | 120.00 | 121.06 | 120.53 | 0.879 | fail |
| AAPL | 310.20 | 310.22 | 310.21 | 0.006 | pass |
| MU | 868.71 | 872.00 | 870.355 | 0.378 | pass |
| AMD | 470.62 | 485.98 | 478.30 | 3.211 | fail |
| LRCX | 297.56 | 326.00 | 311.78 | 9.122 | fail |
| NVDA | 212.38 | 212.65 | 212.515 | 0.127 | pass |

`LLY` was selected as the highest-ranked validation candidate because it combined a fresh pass spread, not currently held status, high source confidence, low concentration impact, and three usable research confirmations.

## Alpaca asset and news MCP

- `get_asset(LLY)`: first attempt cancelled, retry pass. Asset class `us_equity`, status `active`, tradable `true`, exchange `NYSE`.
- `get_asset(FCX)`: pass. Asset class `us_equity`, status `active`, tradable `true`, exchange `NYSE`.
- `get_asset(NOK)`: pass. Asset class `us_equity`, status `active`, tradable `true`, exchange `NYSE`.
- `get_news(LLY,FCX,NOK, start=2026-05-19)`: pass. LLY news included VERVE-102 LDL reduction coverage on 2026-05-26 and retatrutide obesity trial coverage on 2026-05-21. NOK news included AI Networking Innovation Lab and 52-week high momentum coverage. No FCX item appeared in the returned 20-item page.

## SEC EDGAR MCP

- Local cache `harness/sec-ticker-cik-map.json` used before MCP lookup:
  - `LLY -> 0000059478`
  - `FCX -> 0000831259`
  - `NOK -> 0000924613`
- `sec-edgar.get_company_info(identifier=0000059478)`: pass. SEC company `ELI LILLY & Co`, CIK 59478, ticker LLY, SIC 2834, fiscal year end 1231.
- `sec-edgar.get_recent_filings(identifier=0000059478, days=30, limit=5)`: pass. Returned 2026-05-22 Form 144, 2026-05-20 8-K, 2026-05-20 Form 144, and 2026-05-19 Form 4 filings.

## Yahoo Finance MCP

- `yahoo-finance.get_yahoo_finance_news(LLY)`: pass. Returned current LLY-related news including acquisition and GLP-1/cancer-related headlines, plus broader market headlines.
- `yahoo-finance.get_recommendations(LLY, recommendations, months_back=12)`: pass. Current row: strongBuy 6, buy 18, hold 6, sell 1, strongSell 0.

## Alpha Vantage MCP

- Required sequence followed:
  - `TOOL_LIST`: pass.
  - `TOOL_GET("PING")`: pass.
  - `TOOL_CALL("PING", {})`: cancelled.
- Classification: `gap_category=cancelled`, `retry_count=0`, not used in score. No non-PING candidate call was attempted after the health check cancellation.

## FRED MCP

- Scheduler-owned preflight existed at `wiki/evidence-store/sources/2026-05-27-0051-hourly-autopilot-research-mcp-preflight.json`.
- Provider row `fred` had `outcome=pass` for `get_macro_snapshot`, so it was counted as queried/usable FRED macro evidence.
- Latest preflight macro fields included DGS10 4.57 on 2026-05-21, DGS2 4.08 on 2026-05-21, FEDFUNDS 3.64 for 2026-04-01, CPIAUCSL 332.407 for 2026-04-01, UNRATE 4.3 for 2026-04-01, and NFCI -0.52300 for 2026-05-15.

## Firecrawl MCP

- `tool_search` did not expose a registered Firecrawl MCP namespace/tool in this Codex session.
- Per workflow, no shell/curl/local Firecrawl wrapper was called.
- Classification: `gap_category=wrapper_error`, not used in score.

## Decision notes

- Proposed order: LLY 1 share day limit buy at 1080.00.
- Rationale: LLY passed fresh quote/spread, tradability, SEC filing/company check, Yahoo analyst/news check, and FRED macro preflight; Alpaca news showed near-term GLP-1/gene-therapy catalysts. Sizing is deliberately a 1-share paper validation order, below the 2% per-order validation cap and well inside ticker/cash/invested limits.
- Skipped buys: FCX and NOK were valid recheck candidates but lower ranked than LLY. NOK was already held and FCX had weaker same-run company-event evidence. MU had strong momentum but was not selected because the validation slot was limited to one order and LLY had cleaner multi-provider non-semiconductor confirmation. AMD and LRCX failed spread. INTC failed spread in the later snapshot. Existing holdings had no workflow-approved sell/trim rationale.

## Submission and reconciliation

- First `place_stock_order` attempt was cancelled by the MCP safety wrapper before order creation.
- Retry used the same idempotent `client_order_id=hourly-20260527-0052-lly-buy-1`.
- Alpaca MCP `place_stock_order`: submitted LLY buy 1 share, day limit, limit 1079.78, order id `f2626164-9d01-4134-97ab-5e73748fc790`, initial status `pending_new`.
- Alpaca MCP `get_orders(status=all, symbols=LLY)`: final observed status `filled`, filled qty 1, filled average price 1079.38, filled at `2026-05-26T16:02:35.719698Z`.
- Alpaca MCP `get_account_activities(activity_types=FILL, after=2026-05-26)`: returned no rows immediately after fill; order endpoint and position endpoint confirmed fill.
- Alpaca MCP `get_all_positions`: LLY position present, qty 1, average entry 1079.38, current price 1078.6501, market value 1078.6501.
- Alpaca MCP `get_account_info`: post-submit portfolio value 101200.17, cash 44030.58, buying power 137631.37, long market value 57169.59.
