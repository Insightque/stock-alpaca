---
id: 2026-06-07-0623-analyst-review-cycle-sources
created_at: 2026-06-06T21:23:41Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-07 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-06 17:21 ET` 기준 market closed, next open `2026-06-08 09:30 ET`.
- Account: ACTIVE, portfolio value `98,156.33 USD`, cash `29,947.79 USD`, buying power `294,276.14 USD`, long market value `68,208.54 USD`.
- Open US equity orders: 0.
- Current positions: 33 symbols.
- Recent orders: `get_orders(status=all, after=2026-06-04T00:00:00Z)`로 `INTC/JPM/AVGO/SO/PFE/AMZN/COP/SLB/NVDA/V/AAPL/PLTR/FCX/WMT/BAC` fill과 `NKE/CVX/NEE/JNJ` cancel을 cross-check했다.
- Direct FILL activities: `get_account_activities(FILL, after=2026-06-04T00:00:00Z, page_size=100)` 성공. `AVGO` partial fills, `INTC` exit fill, `2026-06-05 ET` buy cohort fills를 direct ledger로 재확인했다.
- Portfolio history: `get_portfolio_history(period=1M, timeframe=1D)` initial + 2 retries 모두 cancelled라 account-path evidence에서는 제외했다.
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## Review-due scan

- `2026-06-06` 미국 정규장 close 기준 새로 maturity에 도달한 `1D/5D/20D` horizon은 없다.
- `2026-06-05 ET` fill cohort `JPM/SO/PFE/AMZN/COP/SLB/NVDA/V/AAPL/PLTR/FCX/WMT/BAC` 1D는 `2026-06-08` 미국 정규장 close 이후에만 평가 가능하다.
- `NOK` 20D add-block review는 기존 일정대로 `2026-06-18` 미국 정규장 close 이후다.

## Alpaca snapshot references

`get_stock_snapshot(feed=iex)` 기준 주요 monitoring reference:

| Ticker | Prev close | 2026-06-05 close | Return | Note |
| --- | ---: | ---: | ---: | --- |
| AVGO | 418.955 | 385.73 | -7.93% | post-earnings drawdown 유지 |
| JPM | 310.89 | 312.38 | +0.48% | first-close positive, but 1D horizon not due |
| SO | 91.62 | 92.64 | +1.11% | shock-day defense follow-through 유지 |
| NOK | 16.61 | 14.35 | -13.61% | overheat unwind 지속, add-block 유지 |
| JNJ | 228.27 | 232.71 | +1.95% | close-race cancel 후 rebound |
| NKE | 43.60 | 42.98 | -1.42% | canceled retry was not a miss |
| CVX | 188.34 | 187.31 | -0.55% | same-session cancel recheck |
| NEE | 85.66 | 85.825 | +0.19% | same-session cancel recheck |
| SPY | 756.97 | 737.45 | -2.58% | market-wide risk-off baseline |
| QQQ | 740.50 | 705.375 | -4.74% | AI/tech de-risking baseline |
| XLU | 43.95 | 44.36 | +0.93% | utilities reference |
| XLF | 52.20 | 52.295 | +0.18% | financials reference |
| SMH | 628.51 | 569.82 | -9.34% | semis reference |
| XLE | 58.77 | 57.67 | -1.87% | energy reference |
| XLY | 117.24 | 114.85 | -2.04% | consumer reference |
| XLK | 193.12 | 180.26 | -6.66% | tech reference |

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | cancelled | 2 | account/orders/positions/snapshots/fill ledger usable. `portfolio_history`만 cancelled gap. |
| sec-edgar | gap | cancelled | 2 | `get_insider_summary(AVGO, 30)` initial + 2 retries 모두 cancelled. 추가 probing 없이 gap으로 종료했다. |
| alpha-vantage | gap | provider_error | 0 | Required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check는 성공. 이어 `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:AVGO})`는 daily-rate-limit payload를 반환해 provider_error로 분류했다. |
| fred | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다. shell/curl probe는 수행하지 않았다. |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다. shell/curl probe는 수행하지 않았다. |
| yahoo-finance | usable | not_applicable | 0 | `AVGO/JPM/SO` news와 `JPM` recommendations query 성공. |

## Yahoo Finance context

- `AVGO` news는 `2026-06-06` 기준 semiconductor-wide selloff, stronger-than-expected jobs data, and AVGO earnings overhang을 반복적으로 언급했다.
- `JPM` news는 financial-sector mixed tape와 Tesla/SpaceX client-event narrative가 섞여 있었고, recommendation breadth는 `strongBuy 4 / buy 8 / hold 12 / sell 0 / strongSell 0`였다.
- `SO` news는 explicit catalyst 부재 속에서도 defensive utility valuation/rate sensitivity narrative가 계속 유지됨을 보여줬다.

## Skipped recommendation evidence

- `JNJ` canceled limit `229.25 USD` 대비 `2026-06-05` close `232.71 USD`, change `+1.51%`.
- `NKE` close-race canceled limit `43.20 USD` 대비 `2026-06-05` close `42.98 USD`, change `-0.51%`.
- `CVX` same-session canceled limit `187.68 USD` 대비 `2026-06-05` close `187.31 USD`, change `-0.20%`.
- `NEE` same-session canceled limit `85.47 USD` 대비 `2026-06-05` close `85.825 USD`, change `+0.42%`.

## Data gaps

- Alpaca account-path metrics are incomplete because `get_portfolio_history` remained cancelled after the allowed retry count.
- SEC EDGAR filing-grounded refresh is incomplete because the only current-run query remained cancelled after the allowed retry count.
- Alpha Vantage candidate-data path is incomplete because the first non-PING call returned a daily-rate-limit payload and no second function was attempted.
- FRED and Firecrawl were not exposed as callable namespaces in this runtime and were classified as `wrapper_error`.
