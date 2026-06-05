---
id: 2026-06-06-0626-analyst-review-cycle-sources
created_at: 2026-06-05T21:26:55Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-06 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-05 17:21 ET` 기준 market closed, next open `2026-06-08 09:30 ET`.
- Account: ACTIVE, portfolio value `97,974.00 USD`, cash `29,947.81 USD`, buying power `293,831.53 USD`, long market value `68,026.19 USD`.
- Open US equity orders: 0.
- Current positions: 33 symbols.
- Recent orders: `get_orders(status=all, after=2026-06-04T00:00:00Z)`로 `JPM/INTC/AVGO/SO/PFE/AMZN/COP/SLB/NVDA/V/AAPL/PLTR/FCX/WMT/BAC` fill과 `NKE/CVX/NEE/JNJ` cancel을 cross-check했다.
- Direct FILL activities: `get_account_activities(FILL, after=2026-06-04T00:00:00Z, page_size=100)` 성공. `AVGO` partial fills, `INTC` exit fill, `JPM` 신규 buy fill을 포함한 direct ledger read를 사용했다.
- Portfolio history: `get_portfolio_history(period=1M, timeframe=1D)` initial + 2 retries 모두 cancelled라 account-level path 증거에서는 제외했다.
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## 1D review close evidence

Alpaca snapshot daily bar `2026-06-05` close를 사용했다. `2026-06-04 ET` fill cohort 1D benchmark는 `SPY -2.16%`, `QQQ -4.06%`다.

Relevant ETF/day references:

| Ticker | 2026-06-04 close | 2026-06-05 close | Return | Usage |
| --- | ---: | ---: | ---: | --- |
| XLF | 52.20 | 52.295 | +0.18% | `BAC/JPM` financials |
| XLE | 58.77 | 57.67 | -1.87% | `XOM/COP/CVX/SLB` energy |
| XLU | 43.95 | 44.36 | +0.93% | `SO/NEE` utilities |
| XLY | 117.24 | 114.85 | -2.04% | `NKE/WMT/AMZN` consumer |
| XLK | 193.12 | 180.26 | -6.66% | `AAPL/MSFT/GOOGL` tech |
| SMH | 628.51 | 569.82 | -9.34% | `AVGO/NVDA/INTC` semis |
| JNJ | 228.27 | 232.71 | +1.95% | close-race cancel recheck |
| CVX | 188.34 | 187.31 | -0.55% | same-session cancel recheck |

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | cancelled | 2 | account/orders/positions/news/snapshot usable. `portfolio_history`만 cancelled gap. |
| sec-edgar | usable | not_applicable | 0 | `AVGO`, `INTC`, `JPM` recent filings 조회 성공. `AVGO` 8-K acceptance `2026-06-03T20:21:35+00:00`, `INTC` recent Form 4 cluster, `JPM` recent 424B2/FWP refresh를 확인했다. |
| alpha-vantage | gap | cancelled | 1 | Required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check는 성공. 이어 `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:AVGO})`가 cancelled되어 hard requirement대로 Alpha retries를 즉시 중단했다. |
| fred | gap | wrapper_error | 0 | registered callable namespace가 노출되지 않아 shell/curl probe 없이 wrapper error로 분류했다. |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 노출되지 않아 shell/curl probe 없이 wrapper error로 분류했다. |
| yahoo-finance | usable | not_applicable | 0 | `AVGO`, `JPM` news와 `JPM` recommendations query 성공. `AVGO` recommendations query는 safety cancellation으로 usable set에서 제외했다. |

## News and filing context

- Alpaca news와 Yahoo Finance `AVGO` 컨텍스트는 `2026-06-04` earnings 이후 guidance disappointment, analyst downgrade, semiconductor-wide de-risking을 공통으로 보여줬다.
- SEC EDGAR `AVGO` recent filings는 `2026-06-03` 8-K acceptance를 확인해 earnings-event timing을 filing-grounded로 고정했다.
- SEC EDGAR `INTC` recent filings는 `2026-06-02` Form 4 cluster를 보여줬지만, 이번 run에서 단기 positive catalyst로 해석할 근거는 없었다.
- Yahoo Finance `JPM` news는 financials rotation과 Tesla analyst-call narrative를, recommendations는 `strongBuy 4 / buy 8 / hold 12 / sell 0 / strongSell 0` breadth를 보여줬다.

## Skipped recommendation evidence

- `JNJ` canceled limit `229.25 USD` 대비 `2026-06-05` close `232.71 USD`, change `+1.51%`.
- `NKE` close-race canceled limit `43.20 USD` 대비 `2026-06-05` close `42.98 USD`, change `-0.51%`.
- `CVX` same-session canceled limit `187.68 USD` 대비 `2026-06-05` close `187.31 USD`, change `-0.20%`.
- `NEE` same-session canceled limit `85.47 USD` 대비 `2026-06-05` close `85.825 USD`, change `+0.42%`.

## Data gaps

- Alpaca account-level path metrics are incomplete because `get_portfolio_history` remained cancelled after the allowed retry count.
- Alpha Vantage candidate-data path is incomplete because the first non-PING `TOOL_CALL` was cancelled once and retries were forbidden by workflow.
- FRED and Firecrawl were not exposed as callable namespaces in this runtime and were classified as `wrapper_error`.
