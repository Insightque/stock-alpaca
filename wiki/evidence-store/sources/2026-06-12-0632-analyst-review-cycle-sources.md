---
id: 2026-06-12-0632-analyst-review-cycle-sources
created_at: 2026-06-11T21:32:08Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-12 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-11 17:11 ET` 기준 market closed, next open `2026-06-12 09:30 ET`.
- Account: ACTIVE, portfolio value `99,643.36 USD`, cash `31,285.06 USD`, buying power `300,548.92 USD`, long market value `68,358.30 USD`.
- Open US equity orders: 0.
- Current positions: 33 symbols.
- Post-close snapshot source-of-record: `wiki/trade-ledger/positions/2026-06-12-0611-after-hours-autopilot-post-trade.json`.
- Current prices and position basis reference: `wiki/evidence-store/sources/2026-06-12-0611-after-hours-autopilot-alpaca-core-preflight.json`의 `get_all_positions.payload.result`.
- Direct FILL activities:
  - `get_account_activities(FILL, after=2026-06-10T00:00:00Z, until=2026-06-12T00:00:00Z, direction=asc, page_size=100)`
  - `get_account_activities(FILL, after=2026-06-05T00:00:00Z, until=2026-06-06T23:59:59Z, direction=asc, page_size=100)`
  - broader reconciliation용 `2026-06-04T00:00:00Z` 이후 fill scan
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## Review closeout metrics

- `2026-06-10 ET` fill cohort 1D closeout:
  - `WMT` `118.49 -> 120.3782` (`+1.59%`)
  - `AVGO` trim `373.25 -> 384.25` (`+2.95%`)
  - `RGTI` trim `20.38 -> 20.72` (`+1.67%`)
  - `BAC` `54.77 -> 55.20` (`+0.79%`)
  - `PFE` `25.70 -> 26.13` (`+1.67%`)
  - `XOM` `151.41 -> 146.81` (`-3.04%`)
  - `JNJ` `239.23 -> 236.5421` (`-1.12%`)
  - `COP` `121.05 -> 115.7518` (`-4.38%`)
  - `SLB` `56.45 -> 56.03` (`-0.74%`)
  - `AMZN` `239.33 -> 241.49` (`+0.90%`)
  - `FCX` `62.21 -> 66.24` (`+6.48%`)
  - `NEE` `85.22 -> 84.97` (`-0.29%`)
  - `NKE` `43.98 -> 45.625` (`+3.74%`)
  - `MSFT` `398.38 -> 391.10` (`-1.83%`)
- `2026-06-05 ET` fill cohort 5D closeout:
  - `JPM` `311.81 -> 313.50` (`+0.54%`)
  - `SO` `93.32 -> 93.40` (`+0.09%`)
  - `PFE` `26.09 -> 26.13` (`+0.15%`)
  - `AMZN` `253.17 -> 241.49` (`-4.61%`)
  - `COP` `117.42 -> 115.7518` (`-1.42%`)
  - `SLB` `55.67 -> 56.03` (`+0.65%`)
  - `NVDA` `208.73 -> 205.13` (`-1.72%`)
  - `V` `321.90 -> 319.69` (`-0.69%`)
  - `AAPL` `313.27 -> 295.50` (`-5.67%`)
  - `PLTR` `138.53 -> 131.6007` (`-5.00%`)
  - `FCX` `65.15 -> 66.24` (`+1.67%`)
  - `WMT` `119.78 -> 120.3782` (`+0.50%`)
  - `BAC` `53.83 -> 55.20` (`+2.55%`)
- Benchmark reference:
  - 1D `SPY 725.43 -> 737.90` (`+1.72%`), `QQQ 693.69 -> 716.39` (`+3.27%`)
  - 5D `SPY 737.45 -> 737.90` (`+0.06%`), `QQQ 705.375 -> 716.39` (`+1.56%`)

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | not_applicable | 0 | account, positions, open orders, fill ledger, latest quotes, post-close reconciliation usable |
| sec-edgar | usable | not_applicable | 0 | `get_company_info(AVGO)` 성공, `get_insider_summary(AVGO, 30d)`는 cancelled라 insider overlay incomplete |
| alpha-vantage | gap | wrapper_error | 0 | required `TOOL_CALL` entrypoint가 runtime에 노출되지 않아 `TOOL_LIST -> TOOL_GET(PING)` 뒤 필수 health check를 완료할 수 없었다 |
| fred | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다 |
| yahoo-finance | usable | not_applicable | 0 | `AVGO/AAPL/NOK` news와 recommendation summary query 성공 |

## Research context

- SEC EDGAR `get_company_info(AVGO)`:
  - `cik=1730168`
  - exchange/industry identity 확인 가능
- Yahoo Finance `AVGO`:
  - recent news는 post-earnings AI semiconductor selloff와 `great isn't good enough` 성격의 AI-stock de-risking narrative를 반영했다.
  - recent analyst actions는 `2026-06-04` 다수 목표가 상향과 `Macquarie Neutral` downgrade가 병존했다.
- Yahoo Finance `AAPL`:
  - recent news는 WWDC/Siri AI reset과 big-tech weakness를 함께 보여줬다.
  - recent analyst actions는 `2026-06-09` target raise 다수와 `Rosenblatt Neutral` 유지가 함께 잡혔다.
- Yahoo Finance `NOK`:
  - recent news는 AI & Cloud revenue growth, Nvidia-backed networking narrative, valuation debate를 함께 보여줬다.
  - recent analyst action은 최근 3개월 범위에서 `2026-04-27 Argus Research Hold -> Buy`가 확인됐다.

## Skipped recommendation evidence

- `2026-06-12-0431-hourly-autopilot`와 `2026-06-12-0451-hourly-autopilot`에서 `review_backlog_pending_1d_count=14`가 YAML `stop_new_buys_at_pending_1d=12`를 초과해 신규 validation buy가 차단됐다.
- 같은 runtime gate evaluation에서 `WMT`와 `NEE`는 executable quote/cap 조건을 충족했지만 최종 blocker는 `review_backlog_throttle`이었다.
- blocked-vs-current hindsight:
  - `WMT` blocked quote 약 `120.93/120.94`, current `120.3782`
  - `NEE` blocked quote 약 `85.27/85.29`, current `84.97`
- `2026-06-12-0611-after-hours-autopilot`에서는 `ADBE/PLTR` freshness fail, `QQQ/SPY` stale plus notional cap fail, `RGTI/AVGO/SO` spread 또는 same-day sell discipline fail로 after-hours skip이 유지됐다.

## Data gaps

- Alpha Vantage는 user-required `TOOL_CALL("PING", {})` 경로를 이 runtime에서 실행할 수 없었다. `FETCH` 같은 우회 경로는 사용하지 않았다.
- FRED/Firecrawl은 namespace 미노출 상태였고 shell/curl probe는 수행하지 않았다.
- SEC insider summary 1회 호출이 cancelled되어 insider overlay는 partial gap으로 남는다.
