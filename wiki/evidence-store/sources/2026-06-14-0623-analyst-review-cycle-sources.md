---
id: 2026-06-14-0623-analyst-review-cycle-sources
created_at: 2026-06-13T21:23:31Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-14 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-13 17:22 ET` 기준 market closed, next open `2026-06-15 09:30 ET`, next close `2026-06-15 16:00 ET`.
- Account: ACTIVE, portfolio value `100,415.12 USD`, cash `31,950.34 USD`, buying power `302,843.86 USD`, long market value `68,464.78 USD`.
- Open US equity orders: 0.
- Current positions: 33 symbols.
- Direct FILL activities:
  - `get_account_activities(FILL, after=2026-06-12T00:00:00Z, direction=asc, page_size=100)`
  - 최근 usable fills는 `PFE` trim 1주, `AVGO` trim 1주, `RGTI` trim 12주다.
- Orders ledger cross-check:
  - `get_orders(status=all, after=2026-06-12T00:00:00Z, direction=desc, limit=200)`
  - `PFE/AVGO/RGTI` 3건 모두 filled, 새 open order 없음.
- Portfolio history:
  - `get_portfolio_history(period=1M, timeframe=1D, intraday_reporting=market_hours, pnl_reset=per_day)`
  - initial + retry 1 + retry 2 모두 `user cancelled MCP tool call`
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## Review scan status

- 새 미국 정규장 close 없음. live Alpaca clock이 토요일 `2026-06-13 17:22 ET`라 지난 cycle 이후 새 `1D/5D/20D` closeout 추가 없음.
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
| alpaca | usable | not_applicable | 0 | clock, account, positions, orders, fill ledger, watchlists usable |
| sec-edgar | gap | cancelled | 0 | current runtime exposed surface가 partial이었고 `get_recommended_tools(form_type=4)` probe도 cancelled |
| alpha-vantage | usable | not_applicable | 0 | required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` pass, `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:\"AAPL\"})` pass |
| fred | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| yahoo-finance | usable | not_applicable | 0 | `AAPL` news와 `NOK` analyst action summary query 성공 |

## Research context

- Alpha Vantage `EARNINGS(AAPL)`:
  - latest quarter `fiscalDateEnding=2026-03-31`
  - `reportedDate=2026-04-30`
  - `reportedEPS=2.01`
  - `estimatedEPS=1.94`
  - `surprisePercentage=3.6082`
  - `reportTime=post-market`
- Yahoo Finance `AAPL`:
  - recent news는 AI spending restraint를 강점으로 보는 기사와 pricing/supply-chain 부담을 지적하는 기사, billionaire ownership narrative가 혼재했다.
- Yahoo Finance `NOK` upgrades/downgrades:
  - `2026-06-12T14:42:59` `JP Morgan Overweight`
  - `priceTargetAction=Raises`
  - `currentPriceTarget=21.0`
  - `priorPriceTarget=14.0`

## Skipped recommendation evidence

- `2026-06-13-0451-hourly-autopilot` 기준 `FCX`와 `NEE`는 executable quote/spread였지만 `review_backlog_pending_1d_count=14`가 신규 buy 슬롯을 `0`으로 계산해 buy path를 막았다.
- `2026-06-14-0611-after-hours-autopilot` 기준 `QQQ/MSFT`는 stale overnight quote가 유지돼 buy path가 열리지 않았다.

## Data gaps

- Alpaca `get_portfolio_history`는 workflow 요구에 맞춰 2회 재시도했지만 모두 cancelled였다.
- SEC EDGAR는 현재 runtime surface가 partial이었고 exposed lightweight probe도 cancelled라 issuer-level filing refresh를 수행하지 못했다.
- FRED/Firecrawl은 namespace 미노출 상태였고 shell/curl probe는 수행하지 않았다.
