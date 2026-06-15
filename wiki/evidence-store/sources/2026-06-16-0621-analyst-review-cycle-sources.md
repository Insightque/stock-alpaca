---
id: 2026-06-16-0621-analyst-review-cycle-sources
created_at: 2026-06-15T21:21:56Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-16 06:21 KST analyst review cycle sources

## Alpaca MCP reconciliation

- `get_clock`: `2026-06-15T17:22:00.816784721-04:00`, `is_open=false`, next open `2026-06-16T09:30:00-04:00`
- `get_account_info`: status `ACTIVE`, cash `29,836.36`, portfolio value `102,566.01`, buying power `306,318.33`, long market value `72,729.65`
- `get_all_positions`: `33건`
- `get_orders(status=open)`: `0건`
- `get_orders(status=all, after=2026-06-10T00:00:00Z, limit=500)`: 2026-06-12 ET `RGTI` trim, 2026-06-14 ET after-hours `AVGO/MSFT`, 2026-06-15 ET regular fills `18건` 확인
- `get_account_activities(activity_types=FILL, after=2026-06-10T00:00:00Z, page_size=100)`: fill cross-check 완료
- `get_stock_snapshot(feed=iex)`: `RGTI/AVGO/PFE/AAPL/AMZN/GOOGL/MSFT/SO/V/COP/NKE/XOM/SLB/FCX/JPM/NEE/WMT/BAC/NOK/SPY/QQQ` daily close 확인
- `get_watchlists`: `0건`
- `get_portfolio_history(period=1M,timeframe=1D,intraday_reporting=market_hours,pnl_reset=per_day)`: 3회 모두 cancelled

## Review scan status

- closeout due now:
  - `RGTI` 2026-06-12 ET trim `1D`
  - `AVGO` 2026-06-14 ET after-hours trim `1D`
  - `MSFT` 2026-06-14 ET after-hours add `1D`
- new waiting reviews:
  - 2026-06-15 ET `RGTI,BAC,WMT,AVGO,NEE,JPM,FCX,SLB,XOM,NKE,COP,V,SO,MSFT,GOOGL,AMZN,AAPL,PFE`
- due-index target summary:
  - `pending_1d_count=18`
  - `pending_5d_count=19`
  - `pending_20d_count=1`
  - `blocked_add_symbols=[NOK]`

## Review closeout metrics

| symbol | fill | close | return |
| --- | --- | --- | --- |
| `RGTI` | `21.010833` | `22.72` | `+8.14%` |
| `AVGO` | `391.92` | `393.97` | `+0.52%` |
| `MSFT` | `395.87` | `400.05` | `+1.06%` |
| `SPY` | `741.67` | `754.75` | `+1.76%` |
| `QQQ` | `721.31` | `743.81` | `+3.12%` |

## Open-position monitor metrics

- `AAPL`: qty `6`, avg `301.965`, close `296.53`, unrealized 약 `-1.80%`
- `AVGO`: qty `2`, avg `423.3625`, close `393.97`, unrealized 약 `-6.94%`
- `NOK`: qty `402`, avg `15.044527`, close `14.83`, unrealized 약 `-1.43%`
- `FCX`: qty `6`, avg `65.675`, close `70.10`, unrealized 약 `+6.74%`

## Provider coverage

| provider | outcome | gap_category | note |
| --- | --- | --- | --- |
| `alpaca` | usable | `not_applicable` | core reconciliation usable, `portfolio_history`만 cancelled |
| `sec-edgar` | usable | `not_applicable` | `AAPL`, `AVGO`, `RGTI` recent filings usable |
| `alpha-vantage` | usable | `not_applicable` | required health-check sequence + `AAPL EARNINGS` pass |
| `fred` | gap | `wrapper_error` | 등록 MCP callable surface 미노출 |
| `firecrawl` | gap | `wrapper_error` | 등록 MCP callable surface 미노출 |
| `yahoo-finance` | usable | `not_applicable` | `AAPL`, `NOK`, `FCX` contextual signals usable |

## Research context

### Alpha Vantage

- `AAPL` `EARNINGS`
  - latest quarter `fiscalDateEnding=2026-03-31`
  - `reportedDate=2026-04-30`
  - `reportedEPS=2.01`
  - `estimatedEPS=1.94`
  - `surprisePercentage=3.6082`
  - `reportTime=post-market`

### SEC EDGAR

- `AAPL`: recent `2026-05-29 Form 4`, `2026-05-28 SD`, `2026-05-27 144`
- `AVGO`: recent `2026-06-15 Form 4`, `2026-06-11 8-K`, `2026-06-09 10-Q`
- `RGTI`: recent `2026-06-11 144`, `2026-06-11 8-K`, `2026-06-10 Form 4` 다수

### Yahoo Finance

- `AAPL` 뉴스: Mag 7 valuation headwind, memory cost pressure, supplier/data-center infra 맥락이 혼재
- `NOK` 추천 변경: `2026-06-12` JP Morgan `Overweight`, PT `14 -> 21`; `2026-04-27` Argus `Hold -> Buy`
- `FCX` 뉴스: 구리 민감도와 원자재 강세 맥락 지속

## Skipped recommendation evidence

- `FCX`: missed-upside 사례가 강화됐지만 backlog-throttle 완화 증거로는 불충분
- `NEE`: 방어주 특성 대비 실현 초과수익이 미미해 skip 판단 무효화 근거 없음

## Data gaps

- `fred`, `firecrawl` callable MCP tool surface 미노출로 `wrapper_error`
- `alpaca get_portfolio_history` 3회 취소로 히스토리 기반 일간 곡선 확인 불가
