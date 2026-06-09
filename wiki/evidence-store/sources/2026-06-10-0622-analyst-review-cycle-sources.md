---
id: 2026-06-10-0622-analyst-review-cycle-sources
created_at: 2026-06-09T21:22:00Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-10 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-09 17:21 ET` 기준 market closed, next open `2026-06-10 09:30 ET`.
- Account: ACTIVE, portfolio value `98,985.02 USD`, cash `31,951.54 USD`, buying power `299,921.59 USD`, long market value `67,033.48 USD`.
- Open US equity orders: 0.
- Current positions: 33 symbols.
- Orders: `get_orders(status=open)` 0건, `get_orders(status=all, after=2026-06-04T00:00:00Z)`로 recent fill/cancel history 확인.
- Direct FILL activities: `get_account_activities(FILL, after=2026-06-04T00:00:00Z, page_size=100)` 성공. `2026-06-09 ET` 신규 fill 11건과 `2026-06-08 ET` sell/trim cohort를 direct ledger로 재확인했다.
- Latest quotes: `get_stock_latest_quote(AVGO,NOK,AAPL,RGTI,TSLA,JNJ,XOM,SPY,QQQ, feed=iex)` 사용.
- Daily bars: `get_stock_bars(..., timeframe=1Day, days=5, feed=iex)`로 `2026-06-08 ET` 및 `2026-06-09 ET` close 비교값 확보.
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## Review closeout metrics

- `2026-06-08 ET` sell/trim next-close follow-up:
  - `AVGO` trim `391.27 -> 392.765` (`+0.38%`)
  - `AVGO` trim `392.80 -> 392.765` (`-0.01%`)
  - `RGTI` trim `21.48 -> 19.69` (`-8.33%`)
  - `TSLA` exit `398.59 -> 396.56` (`-0.51%`)
- `2026-06-09 ET` new fills awaiting 1D:
  - buys: `BAC 54.07`, `PFE 25.82`, `WMT 118.70`, `SLB 55.11`, `COP 116.05`, `AMZN 245.40`, `JNJ 237.54`, `FCX 63.75`, `XOM 148.35`
  - sells/trims: `AVGO 375.47`, `RGTI 22.298182`

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | not_applicable | 0 | account, positions, orders, fills, latest quote, daily bars usable |
| sec-edgar | gap | cancelled | 0 | `analyze_form4_transactions(AVGO, 30)` current-run call cancelled |
| alpha-vantage | usable | not_applicable | 0 | required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check 성공, `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:AVGO})` 성공 |
| fred | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| yahoo-finance | usable | not_applicable | 0 | `AVGO/NOK` news, `AVGO/NOK` upgrades-downgrades query 성공 |

## Research context

- Alpha Vantage `EARNINGS(AVGO)`:
  - latest quarter `fiscalDateEnding=2026-04-30`
  - `reportedDate=2026-06-03`
  - `reportedEPS=2.44`
  - `estimatedEPS=2.39`
  - `surprisePercentage=2.0921`
  - `reportTime=post-market`
- Yahoo Finance `AVGO`:
  - recent news는 post-earnings AI selloff, financing platform, multiple target revisions를 함께 보여줬다.
  - recent analyst actions는 `2026-06-04`에 buy/overweight 유지와 목표가 상향이 다수였고, 일부 `Neutral` downgrade도 병존했다.
- Yahoo Finance `NOK`:
  - recent news는 AI & Cloud revenue growth, Nvidia backing narrative, valuation debate를 함께 보여줬다.
  - analyst update는 최근 3개월 범위에서 `2026-04-27 Argus Research Hold -> Buy` 1건이 확인됐다.

## Skipped recommendation evidence

- `2026-06-10-0611` after-hours `QQQ`: runtime ask `708.11 USD`, policy per-order cap `495.39 USD` 초과.
- `2026-06-10-0611` after-hours `AAPL/JNJ/WMT/INTC`: after-hours freshness cap 초과.
- `2026-06-10-0611` after-hours held sell reevaluation `AVGO/RGTI/SO`: bid-only stale quote 또는 duplicate/metric gate.

## Data gaps

- Alpaca `get_portfolio_history(period=1M,timeframe=1D,market_hours)`는 initial + 2 retries 모두 cancelled였다. 계좌 equity path와 exact MFE/MAE는 current-run에서 incomplete다.
- SEC EDGAR current-run call은 cancelled였다.
- FRED/Firecrawl은 namespace 미노출 상태였고 shell/curl probe는 수행하지 않았다.
