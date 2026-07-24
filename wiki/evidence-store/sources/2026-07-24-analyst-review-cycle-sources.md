---
id: 2026-07-24-analyst-review-cycle-sources
created_at: 2026-07-24T21:25:08Z
workflow: analyst-review-cycle
paper: true
---

# 2026-07-24 analyst review cycle sources

## Alpaca MCP reconciliation

- `get_clock`: `2026-07-24T17:21:45.830491374-04:00`, `is_open=false`, next open `2026-07-27T09:30:00-04:00`
- `get_account_info`: status `ACTIVE`, cash `29,036.78`, portfolio value `96,255.96`, buying power `294,264.37`, long market value `67,219.18`, last equity `97,419.55`
- `get_orders(status=open)`: `0건`
- `get_orders(status=all, after=2026-07-23T20:00:00Z)`: `NOK` filled order `1건`
- `get_all_positions`: `31건`
- `get_account_activities(activity_types=[FILL], after=2026-07-01)`: `AVGO` trim `1건`, `NOK` trim `4건` continuity usable
- `get_watchlists`: `0건`
- `get_stock_snapshot(feed=iex, symbols=SPY,QQQ,NOK,AVGO,SO,WMT)`: `2026-07-24 ET` close/current benchmark cross-check usable
- `get_portfolio_history`: cancelled `3회`. account curve 기반 attribution은 이번 run에서 보강하지 못했다.

## Due review closeout status

- review registration completed in this run:
  - `2026-07-24 ET` `NOK` trim fill waiting marker
  - `NOK`, `IONQ`, `GOOGL`, `AMD` open-position monitor
  - skipped recommendation re-check
- next due:
  - `2026-07-27 US regular-session close`: `NOK` `1D`
  - `2026-07-29 US regular-session close`: `AVGO`, `NOK` `5D` from `2026-07-22 ET` trim cohort
  - `2026-07-31 US regular-session close`: `NOK` `5D` from `2026-07-24 ET` trim
  - `2026-08-21 US regular-session close`: `NOK` `20D` from `2026-07-24 ET` trim

## 2026-07-24 ET fill metrics

| symbol | fill timestamp | fill | 2026-07-24 close | same-day move |
| --- | --- | --- | --- | --- |
| `NOK` | `2026-07-24T13:17:49.876154Z` | `9.67` | `9.07` | `-6.20%` |

## Benchmark context

- `SPY`: `738.06 -> 738.90`, `+0.11%`
- `QQQ`: `691.98 -> 684.33`, `-1.11%`
- `AVGO`: `392.61 -> 381.84`, `-2.74%`
- `NOK`: `9.72 -> 9.07`, `-6.69%`
- `SO`: `96.51 -> 97.285`, `+0.80%`
- `WMT`: `108.39 -> 109.46`, `+0.99%`

## NOK evidence bundle

- Alpaca order/fill:
  - `client_order_id=ah-20260723-2151-sell-nok-01`
  - `order_id=e91d0b66-f1b4-49a1-bcd8-7c2283132857`
  - `filled_avg_price=9.67`
  - `filled_at=2026-07-24T13:17:49.876154Z`
- Alpaca position/snapshot:
  - position `398주`
  - avg entry `15.044561`
  - `2026-07-24 ET` close `9.07`
  - latest trade `9.09`
  - latest quote `9.05 / 9.10`
- Alpha Vantage:
  - required health check sequence pass:
    - `TOOL_LIST`
    - `TOOL_GET(PING)`
    - `TOOL_CALL(PING,{}) -> pong`
  - candidate call:
    - `TOOL_GET(EARNINGS)`
    - `TOOL_CALL(EARNINGS,{symbol:"NOK"})`
  - latest quarterly row:
    - `fiscalDateEnding=2026-06-30`
    - `reportedDate=2026-07-23`
    - `reportedEPS=0.05`
    - `estimatedEPS=0.07`
    - `surprisePercentage=-28.5714`
    - `reportTime=pre-market`
- Yahoo Finance:
  - `get_yahoo_finance_news(NOK)`: timeout `curl (28)`
  - `get_recommendations(NOK, upgrades_downgrades, 3mo)`: timeout `curl (28)`
- SEC EDGAR:
  - `get_recommended_tools(8-K)` initial call cancelled
  - `get_recommended_tools(8-K)` retry cancelled
  - 이번 run의 SEC 보강은 prior ticker note continuity에 의존

## Open-position monitor bundle

- `IONQ`: `45주`, avg `63.48`, current `33.1592`, unrealized about `-47.76%`
- `GOOGL`: `5주`, avg `376.204`, current `319.66`, unrealized about `-15.03%`
- `AMD`: `14주`, avg `462.73`, current `522.35`, unrealized about `+12.88%`
- `IONQ` Yahoo recommendation summary `3mo`: timeout `curl (28)`
- `GOOGL` Yahoo recommendation summary `3mo`: timeout `curl (28)`

## Provider coverage

| provider | outcome | gap_category | note |
| --- | --- | --- | --- |
| `alpaca` | usable | `not_applicable` | account/order/fill/position/snapshot usable, portfolio history cancelled |
| `sec-edgar` | gap | `cancelled` | callable surface 2회 모두 cancelled |
| `alpha-vantage` | usable | `not_applicable` | required health check 후 `EARNINGS(NOK)` success |
| `fred` | gap | `wrapper_error` | registered callable tool surface 미노출 |
| `firecrawl` | gap | `wrapper_error` | registered callable tool surface 미노출 |
| `yahoo-finance` | gap | `timeout` | `NOK/IONQ/GOOGL` queries timed out |

## Data gaps

- `alpaca get_portfolio_history` cancelled `3회`
- `sec-edgar get_recommended_tools(8-K)` cancelled `2회`
- `yahoo-finance` query timeouts:
  - `get_yahoo_finance_news(NOK)`
  - `get_recommendations(NOK, upgrades_downgrades, 3mo)`
  - `get_recommendations(IONQ, upgrades_downgrades, 3mo)`
  - `get_recommendations(GOOGL, upgrades_downgrades, 3mo)`
- `fred`, `firecrawl` callable MCP tool surface 미노출
