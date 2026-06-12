---
id: 2026-06-13-0622-analyst-review-cycle-sources
created_at: 2026-06-12T21:22:12Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-13 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-12 17:22 ET` 기준 market closed, next open `2026-06-15 09:30 ET`.
- Account: ACTIVE, portfolio value `100,506.96 USD`, cash `31,950.36 USD`, buying power `303,033.51 USD`, long market value `68,556.60 USD`.
- Open US equity orders: 0.
- Current positions: 33 symbols.
- Direct FILL activities:
  - `get_account_activities(FILL, after=2026-06-06T00:00:00Z, direction=asc, page_size=100)`
  - due closeout cross-check는 `get_orders(status=all, after=2026-06-10T00:00:00Z, direction=asc, limit=200)`와 함께 사용했다.
- Portfolio history:
  - `get_portfolio_history(period=1M, timeframe=1D, intraday_reporting=market_hours, pnl_reset=per_day)`
  - initial + retry 1 + retry 2 모두 `user cancelled MCP tool call`
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## Review closeout metrics

- `2026-06-11 ET` after-hours trim 1D closeout:
  - `PFE` trim `26.13 -> 26.21` (`+0.31%`)
  - `AVGO` trim `387.06 -> 381.95` (`-1.32%`)
- `2026-06-05 ET` fill cohort 5D closeout:
  - `JPM` `311.81 -> 320.71` (`+2.85%`)
  - `SO` `93.32 -> 94.015` (`+0.74%`)
  - `PFE` `26.09 -> 26.21` (`+0.46%`)
  - `AMZN` `253.17 -> 238.56` (`-5.77%`)
  - `COP` `117.42 -> 116.965` (`-0.39%`)
  - `SLB` `55.67 -> 56.17` (`+0.90%`)
  - `NVDA` `208.73 -> 205.17` (`-1.71%`)
  - `V` `321.90 -> 322.39` (`+0.15%`)
  - `AAPL` `313.27 -> 291.085` (`-7.08%`)
  - `PLTR` `138.53 -> 127.98` (`-7.62%`)
  - `FCX` `65.15 -> 68.40` (`+4.99%`)
  - `WMT` `119.78 -> 121.05` (`+1.06%`)
  - `BAC` `53.83 -> 55.99` (`+4.01%`)
- Benchmark reference:
  - 1D `SPY 737.67 -> 741.67` (`+0.54%`), `QQQ 716.63 -> 721.31` (`+0.65%`)
  - 5D `SPY 737.45 -> 741.67` (`+0.57%`), `QQQ 705.375 -> 721.31` (`+2.26%`)

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | not_applicable | 0 | account, positions, orders, fill ledger, daily bars usable |
| sec-edgar | gap | cancelled | 0 | `get_insider_summary(AVGO, 30d)`가 cancelled되어 insider overlay incomplete |
| alpha-vantage | usable | not_applicable | 0 | required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` pass, `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:"AVGO"})` pass |
| fred | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| yahoo-finance | usable | not_applicable | 0 | `AVGO/AAPL/NOK/PFE` news와 `AVGO/AAPL/NOK` analyst summary query 성공 |

## Research context

- Alpha Vantage `EARNINGS(AVGO)`:
  - latest quarter `fiscalDateEnding=2026-04-30`
  - `reportedDate=2026-06-03`
  - `reportedEPS=2.44`
  - `estimatedEPS=2.39`
  - `surprisePercentage=2.0921`
  - `reportTime=post-market`
- Yahoo Finance `AVGO`:
  - recent news는 AI capex 수혜 narrative와 동시에 chip-stock selloff, post-earnings skepticism을 함께 보여줬다.
  - recent analyst actions는 `2026-06-04` 목표가 상향 다수와 `Macquarie Neutral` downgrade가 병존했다.
- Yahoo Finance `AAPL`:
  - recent news는 AI memory cost, pricing dilemma, WWDC 이후 hardware/services focus 재평가를 함께 보여줬다.
  - recent analyst actions는 `2026-06-09` target raise 다수와 `Rosenblatt Neutral`, `Needham Hold`가 같이 잡혔다.
- Yahoo Finance `NOK`:
  - recent news는 AI networking, optical demand, quantum-safe networking narrative를 보여줬다.
  - analyst action은 `2026-06-12 JP Morgan Overweight`, `currentPriceTarget=21.0`, `priorPriceTarget=14.0`가 최신이다.
- Yahoo Finance `PFE`:
  - recent news는 obesity/oncology pipeline 데이터와 safe-haven 성격 재평가가 혼재했다.

## Skipped recommendation evidence

- `2026-06-13-0611-after-hours-autopilot`에서는 freshest `QQQ 722.00/722.21`도 stale quote cap을 넘었고, `MSFT`도 약 31분 stale이었다.
- same after-hours cycle에서 `AVGO/SO` sell reevaluation은 spread 또는 stale gate에 막혔다.
- `2026-06-13-0451-hourly-autopilot`에서는 `review_backlog_pending_1d_count=14`가 여전히 buy throttle을 유지해 `FCX/NEE` 신규 buy path를 막았다.

## Data gaps

- Alpaca `get_portfolio_history`는 workflow 요구에 맞춰 2회 재시도했지만 모두 cancelled였다.
- SEC EDGAR insider summary 1회 호출이 cancelled되어 filing-based insider overlay는 partial gap이다.
- FRED/Firecrawl은 namespace 미노출 상태였고 shell/curl probe는 수행하지 않았다.
