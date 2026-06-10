---
id: 2026-06-11-0622-analyst-review-cycle-sources
created_at: 2026-06-10T21:22:00Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-11 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-10 17:22 ET` 기준 market closed, next open `2026-06-11 09:30 ET`.
- Account: ACTIVE, portfolio value `96,923.68 USD`, cash `30,865.37 USD`, buying power `293,521.79 USD`, long market value `66,058.31 USD`.
- Open US equity orders: 0.
- Current positions: 33 symbols.
- Orders: `get_orders(status=open)` 0건, `get_orders(status=all, after=2026-06-04T00:00:00Z)`로 recent fill/cancel history 확인.
- Direct FILL activities: `get_account_activities(FILL, after=2026-06-04T00:00:00Z, page_size=100)` 성공. `2026-06-09 ET` fill cohort 13건 closeout과 `2026-06-10 ET` 신규 fill 14건 waiting scan을 direct ledger로 재확인했다.
- Latest quotes: `get_stock_latest_quote(BAC,PFE,WMT,SLB,COP,AMZN,JNJ,FCX,XOM,AVGO,RGTI,AAPL,NEE,NKE,MSFT,NOK,SPY,QQQ, feed=iex)` 사용.
- Daily bars: `get_stock_bars(..., timeframe=1Day, days=7, feed=iex)`로 `2026-06-09 ET`와 `2026-06-10 ET` close 비교값 확보.
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## Review closeout metrics

- `2026-06-09 ET` regular-session fill cohort 1D:
  - `BAC` `54.07 -> 54.54` (`+0.87%`)
  - `PFE` `25.82 -> 25.61` (`-0.81%`)
  - `WMT` `118.70 -> 120.56` (`+1.57%`)
  - `SLB` `55.11 -> 55.52` (`+0.74%`)
  - `COP` `116.05 -> 119.91` (`+3.33%`)
  - `AMZN` `245.40 -> 237.97` (`-3.03%`)
  - `JNJ` `237.54 -> 238.52` (`+0.41%`)
  - `FCX` `63.75 -> 62.07` (`-2.64%`)
  - `XOM` `148.35 -> 150.68` (`+1.57%`)
  - `AVGO` trim `375.47 -> 371.88` (`-0.96%`)
  - `RGTI` trim `22.298182 -> 19.445` (`-12.80%`)
- `2026-06-09 ET` after-hours `AAPL` add 1D:
  - `291.40 -> 291.48` (`+0.03%`)
  - `291.49 -> 291.48` (`-0.00%`)
- Benchmark close-to-close:
  - `SPY` `737.07 -> 725.58` (`-1.56%`)
  - `QQQ` `707.86 -> 693.70` (`-2.00%`)
- `2026-06-10 ET` new fills awaiting 1D:
  - buys: `WMT 118.49`, `BAC 54.77`, `PFE 25.70`, `XOM 151.41`, `JNJ 239.23`, `COP 121.05`, `SLB 56.45`, `AMZN 239.33`, `FCX 62.21`, `NEE 85.22`, `NKE 43.98`, `MSFT 398.38`
  - sells/trims: `AVGO 373.25`, `RGTI 20.38`

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | not_applicable | 0 | account, positions, orders, fills, latest quote, daily bars usable |
| sec-edgar | usable | not_applicable | 0 | `get_recent_filings(AVGO, 14d)` 성공, `2026-06-09` 10-Q와 `2026-06-03` 8-K 확인 |
| alpha-vantage | usable | not_applicable | 0 | required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check 성공, `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:AVGO})` 성공 |
| fred | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| yahoo-finance | usable | not_applicable | 0 | `AVGO/NOK/AAPL` news와 recommendation summary query 성공 |

## Research context

- Alpha Vantage `EARNINGS(AVGO)`:
  - latest quarter `fiscalDateEnding=2026-04-30`
  - `reportedDate=2026-06-03`
  - `reportedEPS=2.44`
  - `estimatedEPS=2.39`
  - `surprisePercentage=2.0921`
  - `reportTime=post-market`
- SEC EDGAR `get_recent_filings(AVGO, 14d)`:
  - latest `10-Q` filing date `2026-06-09`, acceptance time `2026-06-09T13:06:09+00:00`
  - recent `8-K` filing date `2026-06-03`, acceptance time `2026-06-03T20:21:35+00:00`
- Yahoo Finance `AVGO`:
  - recent news는 post-earnings AI semiconductor selloff, Citigroup top-pick commentary, Anthropic compute financing headline을 함께 보여줬다.
  - recent analyst actions는 `2026-06-04`에 다수 `Buy/Overweight` 유지 또는 목표가 상향이 있었고, `Macquarie Neutral` downgrade가 병존했다.
- Yahoo Finance `NOK`:
  - recent news는 AI & Cloud revenue growth, Nvidia backing narrative, networking valuation debate를 함께 보여줬다.
  - analyst update는 최근 3개월 범위에서 `2026-04-27 Argus Research Hold -> Buy` 1건이 확인됐다.
- Yahoo Finance `AAPL`:
  - recent news는 WWDC/Siri AI reset 이후 mixed reaction과 big-tech selloff 맥락을 함께 보여줬다.
  - recent analyst actions는 `2026-06-09`에 `TD Cowen`, `Maxim`, `Morgan Stanley`의 target raise와 `Rosenblatt Neutral` 유지가 병존했다.

## Skipped recommendation evidence

- `2026-06-11-0451` `UNH`: final submit boundary에서 live Alpaca clock `2026-06-10T16:00:30.547773652-04:00`로 regular market close 확인.
- `2026-06-11-0611` after-hours `SPY`: ask `723.68 USD`, per-order cap `484.18 USD` 초과.
- `2026-06-11-0611` after-hours `QQQ`: ask `692.65 USD`, per-order cap `484.18 USD` 초과.
- `2026-06-11-0611` after-hours `NOK`: quote `13.38/13.40`는 spread 정상이나 age 약 `70.43`분 stale, validation add-block 유지.
- `2026-06-11-0611` after-hours held sell reevaluation `AVGO/RGTI/SO`: stale/wide-spread 또는 duplicate/metric gate.

## Data gaps

- Alpaca `get_portfolio_history(period=1M,timeframe=1D,market_hours)`는 initial + 2 retries 모두 cancelled였다. 계좌 equity path와 exact MFE/MAE는 current-run에서 incomplete다.
- FRED/Firecrawl은 namespace 미노출 상태였고 shell/curl probe는 수행하지 않았다.
