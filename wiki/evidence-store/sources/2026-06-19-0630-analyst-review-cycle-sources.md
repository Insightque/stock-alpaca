---
id: 2026-06-19-0630-analyst-review-cycle-sources
created_at: 2026-06-18T21:30:00Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-19 06:30 KST analyst review cycle sources

## Alpaca MCP reconciliation

- `get_clock`: `2026-06-18T17:21:19.55996717-04:00`, `is_open=false`, next open `2026-06-22T09:30:00-04:00`
- `get_account_info`: status `ACTIVE`, cash `28,610.97`, portfolio value `101,755.32`, buying power `303,996.18`, long market value `73,144.35`
- `get_orders(status=open, asset_class=[us_equity])`: `0건`
- `get_all_positions`: `34건`
- `get_watchlists`: `0건`
- `get_account_activities(after=2026-06-12T00:00:00Z, page_size=100)`: recent fill/fee ledger usable
- `get_account_activities(activity_types=[FILL], after=2026-06-12T00:00:00Z, page_size=100)`: usable
- `get_account_activities_by_type(activity_type=FILL, after=2026-06-12T00:00:00Z, page_size=100)`: cancelled
- `get_stock_snapshot(feed=iex)`: `SPY,QQQ,NOK,NVDA,MRK,SO,AAPL,GOOGL,AMZN,MSFT,XOM,COP,SLB,FCX,WMT,BAC,PFE,RGTI,NEE,NKE` close-to-close 확인
- `get_asset(symbol_or_asset_id=NOK|MRK|NVDA)`: active tradable US equity 확인
- `get_portfolio_history(period=1M,timeframe=1D,intraday_reporting=market_hours,pnl_reset=no_reset)`: cancelled

## Direct Alpaca continuity vs source-of-record gap

- direct current run:
  - account `ACTIVE`
  - open orders `0`
  - positions `34`
  - watchlists `0`
- recent source-of-record:
  - `[[2026-06-19-0451-hourly-autopilot]]`: positions `32`, account `ACTIVE`, open orders `0`
  - `[[2026-06-19-0611-after-hours-autopilot]]`: positions `32`, account `ACTIVE`, open orders `0`
- 해석:
  - account/open-order continuity는 일치한다.
  - position count는 direct `34`와 scheduler source-of-record `32`가 어긋난다.
  - 이번 analyst review는 order mutation이 없으므로 이 차이는 정책 변경이 아니라 reconciliation gap으로만 기록한다.

## Due review scan status

- closeout due now:
  - `2026-06-17 ET` fill cohort `1D` `17건`
  - `NOK` `20D` add-block review
- not due yet:
  - `PFE/AVGO` after-hours trim `5D`: `2026-06-19 ET` close 이후
  - `2026-06-15 ET` fill cohort `18건` `5D`: `2026-06-22 ET` close 이후
- due-index update target summary:
  - prior `pending_1d_count=17`, `pending_5d_count=23`, `pending_20d_count=15`
  - post-closeout target `pending_1d_count=17`, `pending_5d_count=40`, `pending_20d_count=14`
  - `blocked_add_symbols=[NOK]`

## 2026-06-17 ET fill cohort 1D closeout metrics

| symbol | side | fill | 2026-06-18 close | return |
| --- | --- | --- | --- | --- |
| `PFE` | sell | `25.97` | `25.22` | `-2.89%` |
| `RGTI` | sell | `20.75` | `21.34` | `+2.84%` |
| `BAC` | buy | `57.57` | `56.15` | `-2.47%` |
| `WMT` | buy | `119.83` | `117.19` | `-2.20%` |
| `FCX` | buy | `71.40` | `68.66` | `-3.84%` |
| `NKE` | buy | `45.30` | `45.195` | `-0.23%` |
| `NEE` | buy | `86.38` | `86.735` | `+0.41%` |
| `AMZN` | buy | `240.44` | `244.61` | `+1.73%` |
| `MSFT` | buy | `385.40` | `379.08` | `-1.64%` |
| `XOM` | buy | `141.54` | `137.81` | `-2.64%` |
| `AAPL` | buy | `298.42` | `297.86` | `-0.19%` |
| `GOOGL` | buy | `365.24` | `367.93` | `+0.74%` |
| `COP` | buy | `110.83` | `107.735` | `-2.79%` |
| `SO` | buy | `93.24` | `93.12` | `-0.13%` |
| `SLB` | buy | `51.32` | `48.095` | `-6.28%` |
| `MRK` | buy | `115.19` | `113.895` | `-1.12%` |
| `NVDA` | buy | `206.23` | `210.38` | `+2.01%` |

## Benchmark closeout context

- `SPY`: `741.02 -> 746.75`, `+0.77%`
- `QQQ`: `722.48 -> 739.82`, `+2.40%`

## NOK 20D add-block evidence

- Alpaca snapshot/current:
  - avg entry `15.044527`
  - `2026-06-18 ET` close `13.49`
  - current `13.55`
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
  - recommendation summary: `2026-06-12` JP Morgan `Overweight`, PT `14 -> 21`
  - news: Pennsylvania chip facility expansion, AI network-services framing, valuation caution 기사 혼재
- SEC EDGAR:
  - recent filings: `2026-06-09`, `2026-06-05`, `2026-06-01`, `2026-05-26` `6-K`

## NVDA and MRK review context

- `NVDA`
  - Yahoo recommendation summary: recent bullish reiterations와 PT 상향 다수
  - Yahoo news: AI/chip demand와 valuation/competition headline이 혼재하지만 tone은 전반적으로 constructive
  - SEC EDGAR recent filings: `2026-06-18` `8-K`, `2026-06-18` `Form 4`
- `MRK`
  - Yahoo recommendation summary: recent row 없음
  - Yahoo news: Keytruda/FDA, AI drug discovery collaboration 관련 headline
  - SEC EDGAR recent filings: `2026-06-02` `Form 4` 다수

## Provider coverage

| provider | outcome | gap_category | note |
| --- | --- | --- | --- |
| `alpaca` | usable | `not_applicable` | core reconciliation usable, `get_account_activities_by_type(FILL)`와 `portfolio_history`만 cancelled |
| `sec-edgar` | usable | `not_applicable` | recent filings/company info usable, 일부 deeper call cancelled |
| `alpha-vantage` | usable | `not_applicable` | required health-check 후 `EARNINGS(NOK)` success |
| `fred` | gap | `wrapper_error` | 등록 MCP callable surface 미노출 |
| `firecrawl` | gap | `wrapper_error` | 등록 MCP callable surface 미노출 |
| `yahoo-finance` | usable | `not_applicable` | recommendation/news usable, 일부 per-symbol timeout 존재 |

## Data gaps

- `alpaca get_account_activities_by_type(FILL)` cancelled
- `alpaca get_portfolio_history` cancelled
- `fred`, `firecrawl` callable MCP tool surface 미노출
- recent source-of-record 대비 live position count mismatch `32 vs 34`
