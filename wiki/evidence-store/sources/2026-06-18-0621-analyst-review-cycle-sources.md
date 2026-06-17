---
id: 2026-06-18-0621-analyst-review-cycle-sources
created_at: 2026-06-17T21:21:45Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-18 06:21 KST analyst review cycle sources

## Alpaca MCP reconciliation

- `get_clock`: `2026-06-17T17:21:45.175964983-04:00`, `is_open=false`, next open `2026-06-18T09:30:00-04:00`
- `get_account_info`: status `ACTIVE`, cash `28,003.45`, portfolio value `100,569.73`, buying power `299,508.51`, long market value `72,566.28`
- `get_all_positions`: `34건`
- `get_orders(status=open)`: `0건`
- `get_orders(status=all, after=2026-06-11T00:00:00Z, limit=200)`: `2026-06-10 ET` due cohort `14건`, `2026-06-17 ET` overnight/regular fill cohort `17건`, `SBUX` canceled `1건` 확인
- `get_account_activities_by_type(activity_type=FILL, after=2026-06-11T00:00:00Z, page_size=100)`: initial + retry 1 + retry 2 모두 cancelled
- `get_stock_snapshot(feed=iex)`: `WMT,AVGO,RGTI,BAC,PFE,XOM,JNJ,COP,SLB,AMZN,FCX,NEE,NKE,MSFT,NOK,SPY,QQQ,AAPL,GOOGL,MRK,NVDA,SO` daily close 확인
- `get_portfolio_history(period=1M,timeframe=1D,intraday_reporting=market_hours,pnl_reset=no_reset)`: initial + retry 1 + retry 2 모두 cancelled

## Review scan status

- closeout due now:
  - `2026-06-10 ET` fill cohort `5D` `14건`
- not due yet:
  - `NOK` `20D` add-block review: `2026-06-18 ET` close 이후
  - `2026-06-17 ET` overnight/regular fill cohort `17건` `1D`: `2026-06-18 ET` close 이후
  - `PFE/AVGO` after-hours trim `5D`: `2026-06-19 ET` close 이후
- due-index update target summary:
  - prior `pending_1d_count=0`, `pending_5d_count=37`, `pending_20d_count=1`
  - post-closeout target `pending_1d_count=17`, `pending_5d_count=23`, `pending_20d_count=15`
  - `blocked_add_symbols=[NOK]`

## 2026-06-10 ET fill cohort 5D closeout metrics

| symbol | side | fill | 2026-06-17 close | return |
| --- | --- | --- | --- | --- |
| `WMT` | buy | `118.49` | `118.185` | `-0.26%` |
| `AVGO` | sell | `373.25` | `392.91` | `+5.27%` |
| `RGTI` | sell | `20.38` | `20.25` | `-0.64%` |
| `BAC` | buy | `54.77` | `56.54` | `+3.23%` |
| `PFE` | sell | `25.94` | `25.93` | `-0.04%` |
| `XOM` | buy | `141.54` | `140.79` | `-0.53%` |
| `JNJ` | buy | `237.54` | `233.92` | `-1.52%` |
| `COP` | buy | `121.05` | `111.19` | `-8.15%` |
| `SLB` | buy | `56.45` | `50.33` | `-10.84%` |
| `AMZN` | buy | `245.40` | `237.57` | `-3.19%` |
| `FCX` | buy | `68.40` | `69.03` | `+0.92%` |
| `NEE` | buy | `85.22` | `85.74` | `+0.61%` |
| `NKE` | buy | `43.98` | `44.19` | `+0.48%` |
| `MSFT` | buy | `398.38` | `379.05` | `-4.85%` |

## Benchmark closeout context

- `SPY`: `750.58 -> 741.02`, `-1.27%`
- `QQQ`: `729.87 -> 722.48`, `-1.01%`

## Open-position monitor metrics

- `AAPL`: qty `7`, avg `301.458571`, close/current `296.07`, unrealized 약 `-1.79%`
- `AVGO`: qty `1`, avg `461.26`, close/current `392.91`, unrealized 약 `-14.82%`
- `NOK`: qty `402`, avg `15.044527`, close/current `13.81`, unrealized 약 `-8.21%`
- `RGTI`: qty `27`, avg `25.569583`, close/current `20.25`, unrealized 약 `-20.80%`
- `FCX`: qty `7`, avg `66.492857`, close/current `69.03`, unrealized 약 `+3.82%`

## Provider coverage

| provider | outcome | gap_category | note |
| --- | --- | --- | --- |
| `alpaca` | usable | `not_applicable` | core reconciliation usable, `FILL` activity와 `portfolio_history`만 cancelled |
| `sec-edgar` | gap | `cancelled` | `analyze_form4_transactions(AVGO)`와 `get_financials(NOK,income)` 모두 cancelled |
| `alpha-vantage` | usable | `not_applicable` | required health-check 후 `EARNINGS(NOK)` success |
| `fred` | gap | `wrapper_error` | 등록 MCP callable surface 미노출 |
| `firecrawl` | gap | `wrapper_error` | 등록 MCP callable surface 미노출 |
| `yahoo-finance` | usable | `not_applicable` | `NOK/WMT/FCX` contextual signals usable |

## Research context

### Alpha Vantage

- health check sequence:
  - `TOOL_LIST` pass
  - `TOOL_GET(PING)` pass
  - `TOOL_CALL(PING,{})` -> `pong`
- candidate call:
  - `TOOL_GET(EARNINGS)` pass
  - `TOOL_CALL(EARNINGS,{symbol:"NOK"})` success
  - latest quarterly row: `fiscalDateEnding=2026-03-31`, `reportedDate=2026-04-23`, `reportedEPS=0.06`, `estimatedEPS=0.05`, `surprisePercentage=20`, `reportTime=pre-market`

### SEC EDGAR

- `analyze_form4_transactions(identifier="AVGO", days=30, limit=10)` -> cancelled
- `get_financials(identifier="NOK", statement_type="income")` -> cancelled

### Yahoo Finance

- `NOK` recommendation summary:
  - `2026-06-12` JP Morgan `Overweight`, PT `14 -> 21`
  - `2026-04-27` Argus Research `Hold -> Buy`, PT `15`
- `WMT` 뉴스: fair value 소폭 상향, consumer pressure와 e-commerce/Walmart+ 기대가 혼재
- `FCX` 뉴스: copper tariff uncertainty와 materials/copper rotation 맥락이 지속

## Skipped recommendation evidence

- `SBUX`: `2026-06-17T20:01:40.378968Z` submit, `2026-06-17T20:02:04.050880Z` canceled, fill 없음
- `NOK`: add-block 유지. latest close `13.81`와 weak tape가 unblock 근거를 주지 못함
- `FCX`: backlog-throttle 기간 missed-upside 사례는 유지되지만 이번 5D absolute gain은 `+0.92%`로 과도한 throttle 완화 근거까진 아님

## Data gaps

- `alpaca get_account_activities_by_type(FILL)` 3회 취소로 fill cross-check gap
- `alpaca get_portfolio_history` 3회 취소로 계좌 curve/MFE-MAE 확인 불가
- `sec-edgar` callable runs 2종 모두 취소
- `fred`, `firecrawl` callable MCP tool surface 미노출로 `wrapper_error`
