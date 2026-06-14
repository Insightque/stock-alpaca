---
id: 2026-06-15-0624-analyst-review-cycle-sources
created_at: 2026-06-14T21:24:10Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-15 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-14 17:21 ET` 기준 market closed, next open `2026-06-15 09:30 ET`, next close `2026-06-15 16:00 ET`.
- Account: ACTIVE, portfolio value `100,415.12 USD`, cash `31,950.34 USD`, buying power `302,843.86 USD`, long market value `68,464.78 USD`.
- Open US equity orders: 0.
- Current positions: 33 symbols.
- Direct FILL activities:
  - `get_account_activities(FILL, after=2026-06-01T00:00:00Z, direction=desc, page_size=100)`
  - 최근 fill ledger에는 `PFE/AVGO/RGTI` trim과 `2026-06-10 ET` fill cohort가 모두 포함돼 있었고, prior analyst cycle 이후 신규 fill은 없었다.
- Orders ledger cross-check:
  - `get_orders(status=all, after=2026-06-01T00:00:00Z, direction=desc, limit=500)`
  - `get_orders(status=open, direction=desc, limit=200)`
  - open order 없음, 최근 주문 장부는 prior review와 동일했다.
- Snapshot cross-check:
  - `get_stock_snapshot(symbols=AAPL,AVGO,NOK,RGTI,FCX,NEE,SPY,QQQ,MSFT,PFE, feed=iex)`
  - `AAPL` close `291.085`, `AVGO` `381.95`, `NOK` `14.78`, `RGTI` `20.98`, `FCX` `68.40`, `NEE` `85.94`, `SPY` `741.67`, `QQQ` `721.31`.
- Portfolio history:
  - `get_portfolio_history(period=1M, timeframe=1D, intraday_reporting=market_hours, pnl_reset=per_day)`
  - initial + retry 1 + retry 2 모두 `user cancelled MCP tool call`
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## Review scan status

- 새 미국 정규장 close 없음. live Alpaca clock이 일요일 `2026-06-14 17:21 ET`라 지난 cycle 이후 새 `1D/5D/20D` closeout 추가 없음.
- `review-due-index` carry-forward:
  - `pending_1d_count=1`
  - `pending_5d_count=16`
  - `pending_20d_count=1`
  - `blocked_add_symbols=["NOK"]`

## Open-position monitor metrics

- `AAPL`: `5주`, avg entry `303.136`, current `291.13`, unrealized `-3.961%`
- `AVGO`: `4주`, avg entry `423.3625`, current `382.07`, unrealized `-9.753%`
- `NOK`: `402주`, avg entry `15.044527`, current `14.80`, unrealized `-1.625%`
- `RGTI`: `37주`, avg entry `25.569583`, current `20.98`, unrealized `-17.949%`
- skipped recommendation context:
  - `FCX`: current `68.41`, avg entry `64.912`, unrealized `+5.389%`
  - `NEE`: current `85.99`, avg entry `86.44`, unrealized `-0.521%`

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | not_applicable | 0 | clock, account, positions, orders, fill ledger, watchlists, snapshots usable |
| sec-edgar | usable | not_applicable | 0 | `get_recent_filings(identifier=AAPL|AVGO, days=60, limit=5)` 성공 |
| alpha-vantage | usable | not_applicable | 0 | required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` pass, `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:"AAPL"})` pass |
| fred | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| yahoo-finance | usable | not_applicable | 0 | `AAPL` news, `NOK` analyst action summary, `FCX` news query 성공 |

## Research context

- Alpha Vantage `EARNINGS(AAPL)`:
  - latest quarter `fiscalDateEnding=2026-03-31`
  - `reportedDate=2026-04-30`
  - `reportedEPS=2.01`
  - `estimatedEPS=1.94`
  - `surprisePercentage=3.6082`
  - `reportTime=post-market`
- SEC EDGAR `AAPL` recent filings:
  - latest filing `2026-05-29` Form 4, acceptance `2026-05-29T22:30:27Z`
  - additional recent `SD` on `2026-05-28`, `144` on `2026-05-27`
- SEC EDGAR `AVGO` recent filings:
  - `2026-06-11` Form `8-K`
  - `2026-06-09` Form `10-Q`, acceptance `2026-06-09T13:06:09Z`
  - `2026-06-03` Form `8-K`
- Yahoo Finance `AAPL`:
  - recent news는 iOS/AI narrative 개선 기대, India supplier pollution probe, WWDC 이후 valuation reset 논쟁이 혼재했다.
- Yahoo Finance `NOK` upgrades/downgrades:
  - `2026-06-12T14:42:59` `JP Morgan` `Overweight`
  - `priceTargetAction=Raises`
  - `currentPriceTarget=21.0`
  - `priorPriceTarget=14.0`
- Yahoo Finance `FCX`:
  - recent news는 copper leverage, US policy support, copper price rally 둔화가 혼재해 있다.

## Skipped recommendation evidence

- `2026-06-13-0451-hourly-autopilot` 기준 `FCX`와 `NEE`는 executable quote/spread였지만 `review_backlog_pending_1d_count=14`가 신규 buy 슬롯을 `0`으로 계산해 buy path를 막았다.
- `2026-06-14-0611-after-hours-autopilot` 기준 `QQQ/MSFT`는 stale overnight quote가 유지돼 buy path가 열리지 않았다.

## Data gaps

- Alpaca `get_portfolio_history`는 workflow 요구에 맞춰 2회 재시도했지만 모두 cancelled였다.
- FRED/Firecrawl은 namespace 미노출 상태였고 shell/curl probe는 수행하지 않았다.
