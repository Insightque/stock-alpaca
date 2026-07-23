---
id: 2026-07-23-analyst-review-cycle-sources
created_at: 2026-07-23T21:23:54Z
workflow: analyst-review-cycle
paper: true
---

# 2026-07-23 analyst review cycle sources

## Alpaca MCP reconciliation

- `get_clock`: `2026-07-23T17:22:10.193931346-04:00`, `is_open=false`, next open `2026-07-24T09:30:00-04:00`
- `get_account_info`: status `ACTIVE`, cash `29,027.15`, portfolio value `97,620.71`, buying power `29,027.15`, long market value `68,593.56`
- `get_orders(status=open)`: `0건`
- `get_orders(status=all, after=2026-07-22T20:00:00Z)`: `NOK` fills `2건` usable
- `get_all_positions`: `31건`
- `get_account_activities(activity_types=[FILL], after=2026-07-22T20:00:00Z)`: `NOK` fill ledger `2건` usable
- `get_watchlists`: `0건`
- `get_stock_snapshot(feed=iex, symbols=AVGO,NOK,SPY,QQQ,SMH)`: `2026-07-23 ET` close/current benchmark cross-check usable
- `get_portfolio_history`: cancelled `3회`. 이번 run에서는 account curve 기반 attribution을 보강하지 못했다.
- `get_order_by_client_id(ah-20260722-0911-sell-avgo-01)`: cancelled `3회`. `AVGO` fill fact는 [[2026-07-22-1051-after-hours-autopilot]]와 [[2026-07-22-portfolio-review]]의 same-session fill ledger로 보강했다.

## Due review closeout status

- closeout completed in this run:
  - `2026-07-22 ET` `AVGO` after-hours residual trim `1D`
  - `2026-07-22 ET` `NOK` after-hours trim `1D`
  - `NOK`, `IONQ`, `GOOGL`, `AMD` open-position monitor
  - skipped recommendation re-check
- next due:
  - `2026-07-29 US regular-session close`: `AVGO`, `NOK` `5D`

## 2026-07-23 ET closeout metrics

| symbol | fill | 2026-07-23 close | return |
| --- | --- | --- | --- |
| `AVGO` | `384.14` | `392.61` | `+2.20%` |
| `NOK` trim 1 | `10.95` | `9.72` | `-11.23%` |
| `NOK` trim 2 | `10.78` | `9.72` | `-9.83%` |
| `NOK` trim avg | `10.865` | `9.72` | `-10.53%` |

## Benchmark context

- `SPY`: `747.49 -> 738.06`, `-1.26%`
- `QQQ`: `705.19 -> 691.98`, `-1.87%`
- `SMH`: `586.90 -> 580.34`, `-1.12%`
- `AVGO` vs benchmark:
  - vs `SPY`: `+3.47%p`
  - vs `QQQ`: `+4.08%p`
  - vs `SMH`: `+3.32%p`
- `NOK` avg trim vs benchmark:
  - vs `SPY`: `-9.27%p`
  - vs `QQQ`: `-8.66%p`

## NOK evidence bundle

- Alpaca snapshot/current:
  - position `399주`
  - avg entry `15.044539`
  - `2026-07-23 ET` close `9.72`
  - latest trade `9.78`
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
    - `reportedEPS=0.0799`
    - `estimatedEPS=0.07`
    - `surprisePercentage=14.1429`
    - `reportTime=pre-market`
- Yahoo Finance recommendations:
  - `2026-06-12` JP Morgan `Overweight`, PT `14 -> 21`
  - `2026-04-27` Argus Research `Buy`, PT `15`
- Yahoo Finance news:
  - `2026-07-23` 실적 beat 및 AI/data-center demand headline 다수
- SEC EDGAR:
  - 이번 run의 direct callable surface는 cancelled여서 신규 filing row를 확정하지 못했다.
  - 직전 artifact [[2026-07-22-analyst-review-cycle-sources]]는 recent `6-K` continuity `2026-07-10`, `2026-07-09`, `2026-06-30`, `2026-06-09`, `2026-06-05`를 기록했다.

## AVGO evidence bundle

- Alpaca/local artifact continuity:
  - `client_order_id=ah-20260722-0911-sell-avgo-01`
  - `filled_avg_price=384.14`
  - `filled_at=2026-07-22T01:48:58.933756Z`
  - source refs: [[2026-07-22-1051-after-hours-autopilot]], [[2026-07-22-portfolio-review]]
- Alpaca `2026-07-23 ET` snapshot:
  - close `392.61`
  - latest trade `393.95`
  - previous close `396.88`
- Yahoo Finance recommendations:
  - `2026-07-07` Erste Group `Hold` downgrade
  - `2026-06-04` 다수 bullish reiteration/price-target raise
- Yahoo Finance news:
  - `2026-07-23` Broadcom AI infrastructure 경쟁력 언급 기사 다수

## Provider coverage

| provider | outcome | gap_category | note |
| --- | --- | --- | --- |
| `alpaca` | usable | `not_applicable` | account/order/fill/position/snapshot usable, 일부 surface cancelled |
| `sec-edgar` | gap | `cancelled` | direct callable surface `2회` cancelled |
| `alpha-vantage` | usable | `not_applicable` | required health-check 후 `EARNINGS(NOK)` success |
| `fred` | gap | `wrapper_error` | registered callable tool surface 미노출 |
| `firecrawl` | gap | `wrapper_error` | registered callable tool surface 미노출 |
| `yahoo-finance` | usable | `not_applicable` | recommendation summary와 news usable |

## Data gaps

- `fred`, `firecrawl` callable MCP tool surface 미노출
- `alpaca get_portfolio_history` cancelled `3회`
- `alpaca get_order_by_client_id(ah-20260722-0911-sell-avgo-01)` cancelled `3회`
- `sec-edgar get_insider_summary(NOK, 60d)` cancelled `2회`
