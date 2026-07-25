---
id: 2026-07-25-analyst-review-cycle-sources
created_at: 2026-07-25T21:24:00Z
workflow: analyst-review-cycle
paper: true
---

# 2026-07-25 analyst review cycle sources

## Runtime anchor

- current runtime date: `Saturday, July 25, 2026`
- evaluated market session: `Friday, July 24, 2026 ET`
- workflow checksum: `708359c29439dea1f8707dbbaa74de24d1502359`

## Alpaca MCP reconciliation

- `get_clock`: `2026-07-25T17:22:15.243194776-04:00`, `is_open=false`, next open `2026-07-27T09:30:00-04:00`
- `get_account_info`: status `ACTIVE`, cash `29,036.76`, portfolio value `96,284.29`, buying power `294,299.08`, long market value `67,247.53`, last equity `96,284.29`
- `get_orders(status=open)`: `0건`
- `get_orders(status=all, after=2026-07-22T20:00:00Z)`: recent filled orders `NOK` 3건 (`10.95`, `10.78`, `9.67`)
- `get_account_activities(activity_types=[FILL], after=2026-07-22T20:00:00Z)`: same recent `NOK` fill continuity usable
- `get_all_positions`: `31건`
- `get_watchlists`: `0건`
- `get_stock_snapshot(feed=iex, symbols=NOK,IONQ,GOOGL,AMD,AVGO,SPY,QQQ,SO,WMT,MCD)`: benchmark / skip candidate / open-position cross-check usable
- `get_portfolio_history`: cancelled `3회`. account curve 기반 attribution은 이번 run에서 보강하지 못했다.

## Due review closeout status

- immediate due now: none
- pending horizons carried forward:
  - `2026-07-27 US regular-session close`: `NOK` `1D`
  - `2026-07-29 US regular-session close`: `AVGO`, `NOK` `5D` from `2026-07-22 ET` trim cohort
  - `2026-07-31 US regular-session close`: `NOK` `5D` from `2026-07-24 ET` trim
  - `2026-08-21 US regular-session close`: `NOK` `20D` from `2026-07-24 ET` trim

## Recent fill continuity

| symbol | fill timestamp | fill | order id | client order id |
| --- | --- | ---: | --- | --- |
| `NOK` | `2026-07-24T13:17:49.876154Z` | `9.67` | `e91d0b66-f1b4-49a1-bcd8-7c2283132857` | `ah-20260723-2151-sell-nok-01` |
| `NOK` | `2026-07-23T03:18:44.891868Z` | `10.78` | `d249fed3-33a1-4b84-b84d-4902851737c9` | `ah-20260722-1211-sell-nok-01` |
| `NOK` | `2026-07-23T01:16:18.20135Z` | `10.95` | `87eea18c-86c7-47b6-8565-4e5b56fef08b` | `ah-20260722-0931-sell-nok-01` |

## Snapshot bundle

- `NOK`: daily close `9.07`, prev close `9.72`, latest trade `9.09`, latest quote `9.05 / 9.10`
- `IONQ`: daily close `32.83`, prev close `34.11`, latest trade `32.83`
- `GOOGL`: daily close `319.725`, prev close `317.73`, latest trade `319.31`
- `AMD`: daily close `522.03`, prev close `539.50`
- `AVGO`: daily close `381.84`, prev close `392.61`
- `SPY`: `738.06 -> 738.90`
- `QQQ`: `691.98 -> 684.33`
- `WMT`: `108.39 -> 109.46`
- `MCD`: `262.83 -> 264.715`

## NOK evidence bundle

- Alpha Vantage required health check:
  - `TOOL_LIST`
  - `TOOL_GET(PING)`
  - `TOOL_CALL(PING,{}) -> pong`
- Alpha Vantage candidate call:
  - `TOOL_GET(EARNINGS)`
  - `TOOL_CALL(EARNINGS,{symbol:"NOK"})`
- latest quarterly row:
  - `fiscalDateEnding=2026-06-30`
  - `reportedDate=2026-07-23`
  - `reportedEPS=0.08`
  - `estimatedEPS=0.07`
  - `surprisePercentage=14.2857`
  - `reportTime=pre-market`
- Yahoo Finance:
  - `get_yahoo_finance_news(NOK)` success
  - `get_recommendations(NOK, recommendations, 3mo)` success
  - latest recommendation snapshot `0m`: `strongBuy=4`, `buy=4`, `hold=2`, `sell=0`, `strongSell=1`

## Open-position monitor bundle

- `IONQ`: `45주`, avg `63.48`, current `32.84`, unrealized about `-48.27%`
- `GOOGL`: `5주`, avg `376.204`, current `319.74`, unrealized about `-15.01%`
- `AMD`: `14주`, avg `462.73`, current `521.95`, unrealized about `+12.80%`
- Yahoo recommendation summary:
  - `IONQ 0m`: `strongBuy=1`, `buy=9`, `hold=2`, `sell=0`, `strongSell=0`
  - `GOOGL 0m`: `strongBuy=14`, `buy=44`, `hold=6`, `sell=0`, `strongSell=0`
- Yahoo news:
  - `IONQ`: bullish thematic coverage persisted, but tape stayed weak into `2026-07-24 ET` close

## Friday, July 24, 2026 ET after-hours skip continuity

- latest reviewed no-submit runs: `2026-07-25-2011`, `2026-07-25-2031`, `2026-07-25-2151` after-hours-autopilot
- repeated candidate blockers:
  - `NOK`: source-of-record `9.05/9.10`, spread about `0.55%`, stale
  - `WMT`: one-sided quote
  - `MCD`: stale plus spread about `2.27%`
  - `QQQ/SPY`: stale or per-order cap

## Provider coverage

| provider | outcome | gap_category | note |
| --- | --- | --- | --- |
| `alpaca` | usable | `not_applicable` | account/order/fill/position/snapshot usable, portfolio history cancelled |
| `sec-edgar` | gap | `cancelled` | `get_insider_summary(IONQ, 90d)` initial call and retry both cancelled |
| `alpha-vantage` | usable | `not_applicable` | required health check 후 `EARNINGS(NOK)` success |
| `fred` | gap | `wrapper_error` | registered callable tool surface 미노출 |
| `firecrawl` | gap | `wrapper_error` | registered callable tool surface 미노출 |
| `yahoo-finance` | usable | `not_applicable` | `NOK` news + `NOK/IONQ/GOOGL` recommendation summary success |

## Data gaps

- `alpaca get_portfolio_history` cancelled `3회`
- `sec-edgar get_insider_summary(IONQ, 90d)` cancelled `2회`
- `fred`, `firecrawl` callable MCP tool surface 미노출
