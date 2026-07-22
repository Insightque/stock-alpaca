---
id: 2026-07-22-analyst-review-cycle-sources
created_at: 2026-07-22T21:30:00Z
workflow: analyst-review-cycle
paper: true
---

# 2026-07-22 analyst review cycle sources

## Alpaca MCP reconciliation

- `get_clock`: `2026-07-22T17:21:54.761339741-04:00`, `is_open=false`, next open `2026-07-23T09:30:00-04:00`
- `get_account_info`: status `ACTIVE`, cash `29,005.42`, portfolio value `98,526.58`, buying power `298,711.89`, long market value `69,521.16`
- `get_orders(status=open)`: `0건`
- `get_orders(status=all, after=2026-06-19T00:00:00Z)`: recent fills 중 review 대상 신규 row `AVGO`, `NOK` 확인
- `get_all_positions`: `31건`
- `get_account_activities(activity_types=[FILL], after=2026-06-17T00:00:00Z, page_size=100)`: June 17 buy cohort, `RGTI/PFE` trims, July 22 `AVGO/NOK` trims ledger usable
- `get_stock_bars(feed=iex, timeframe=1Day)`: `AAPL,AMZN,BAC,COP,FCX,GOOGL,MRK,MSFT,NEE,NKE,NVDA,SLB,SO,WMT,XOM,SPY,QQQ,PFE,RGTI,AVGO,NOK,IONQ`
- `get_stock_snapshot`: same symbol set의 current/close cross-check
- `get_news(symbols=NOK,AVGO,IONQ,GOOGL)`: July headline context 보강

## Due review closeout status

- closeout completed in this run:
  - `2026-06-17 ET` buy cohort aged closeout
  - `RGTI/PFE` trim aged closeout
  - `NOK` add-block re-check
  - material open-position monitor
- not due yet:
  - `2026-07-22 ET` `AVGO/NOK` after-hours trim `1D`: `2026-07-23 US regular-session close` 이후
  - same `AVGO/NOK` trim `5D`: `2026-07-29 US regular-session close` 이후

## 2026-06-17 ET buy cohort aged closeout metrics

| symbol | fill | 2026-07-22 close | return |
| --- | --- | --- | --- |
| `AAPL` | `298.42` | `325.88` | `+9.20%` |
| `AMZN` | `240.44` | `244.82` | `+1.82%` |
| `BAC` | `57.57` | `61.65` | `+7.09%` |
| `COP` | `110.83` | `118.83` | `+7.22%` |
| `FCX` | `71.40` | `64.99` | `-8.98%` |
| `GOOGL` | `365.24` | `342.06` | `-6.35%` |
| `MRK` | `115.19` | `127.51` | `+10.70%` |
| `MSFT` | `385.40` | `390.24` | `+1.26%` |
| `NEE` | `86.38` | `89.43` | `+3.53%` |
| `NKE` | `45.30` | `42.21` | `-6.82%` |
| `NVDA` | `206.23` | `212.07` | `+2.83%` |
| `SLB` | `51.32` | `47.66` | `-7.13%` |
| `SO` | `93.24` | `95.79` | `+2.74%` |
| `WMT` | `119.83` | `109.34` | `-8.75%` |
| `XOM` | `141.54` | `154.49` | `+9.15%` |

## Benchmark context

- `SPY`: `+0.87%`
- `QQQ`: `-2.39%`

## Trim closeout metrics

- `PFE` after-hours trim `26.03 -> 24.83`, `-4.61%`
- `PFE` regular trim `25.28 -> 24.83`, `-1.78%`
- `RGTI` after-hours trim `20.96 -> 15.24`, `-27.29%`
- `RGTI` after-hours trim 2 `20.75 -> 15.24`, `-26.55%`
- `RGTI` regular trim `20.56 -> 15.24`, `-25.88%`
- `AVGO` after-hours trim `384.14 -> 396.88`, `+3.32%`
- `NOK` after-hours trim `10.33 -> 10.30`, `-0.29%`

## NOK evidence bundle

- Alpaca snapshot/current:
  - position `401주`
  - avg entry `15.044527`
  - `2026-07-22 ET` close `10.30`
  - current `10.66`
- Alpha Vantage:
  - required health check sequence pass:
    - `TOOL_LIST`
    - `TOOL_GET(PING)`
    - `TOOL_CALL(PING,{}) -> pong`
  - candidate call:
    - `TOOL_GET(EARNINGS)`
    - `TOOL_CALL(EARNINGS,{symbol:"NOK"})`
  - latest quarterly row: `fiscalDateEnding=2026-03-31`, `reportedDate=2026-04-23`, `reportedEPS=0.06`, `estimatedEPS=0.05`, `surprisePercentage=20`
- Yahoo Finance:
  - `2026-06-12` JP Morgan `Overweight`, PT `14 -> 21`
  - `2026-04-27` Argus Research `Buy`, PT `15`
- SEC EDGAR:
  - recent `6-K`: `2026-07-10`, `2026-07-09`, `2026-06-30`, `2026-06-09`, `2026-06-05`

## AVGO and open-position context

- `AVGO`
  - `2026-07-22 ET` after-hours trim fill `384.14`
  - same-day close `396.88`
  - recent SEC: `2026-07-06 8-K`, July Form 4 / 144 흐름
  - Yahoo recommendation summary: June 다수 bullish reiteration, `2026-07-07` Erste `Hold` downgrade
- `GOOGL`
  - Yahoo recommendation summary: `2026-07-21` Wells Fargo `Overweight`, `PT 438`; `2026-07-22` Citizens `Market Outperform`, `PT 515 유지`
- `IONQ`
  - Yahoo recommendation summary `3개월` window에서 신규 row 없음

## Provider coverage

| provider | outcome | gap_category | note |
| --- | --- | --- | --- |
| `alpaca` | usable | `not_applicable` | account/order/fill/position/bars/snapshot/news usable |
| `sec-edgar` | usable | `not_applicable` | `NOK`, `AVGO` company info와 recent filings usable |
| `alpha-vantage` | usable | `not_applicable` | required health-check 후 `EARNINGS(NOK)` success |
| `fred` | gap | `wrapper_error` | registered callable tool surface 미노출 |
| `firecrawl` | gap | `wrapper_error` | registered callable tool surface 미노출 |
| `yahoo-finance` | usable | `not_applicable` | recommendation summary usable |

## Data gaps

- `fred`, `firecrawl` callable MCP tool surface 미노출
- `alpaca portfolio_history` current surface 미노출
- `IONQ` analyst data는 Yahoo recommendation summary 공백으로 보강 한계가 있다
