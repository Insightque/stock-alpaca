---
id: 2026-06-09-0623-analyst-review-cycle-sources
created_at: 2026-06-08T21:23:17Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-09 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-08 17:23 ET` 기준 market closed, next open `2026-06-09 09:30 ET`.
- Account: ACTIVE, portfolio value `100,068.19 USD`, cash `31,774.85 USD`, buying power `301,909.49 USD`, long market value `68,293.34 USD`.
- Open US equity orders: 0.
- Current positions: 32 symbols.
- Same-day closed/fill scope: `get_orders(status=all, after=2026-06-08T00:00:00Z)` 기준 `ah-20260608-0911-sell-avgo`, `ah-20260608-0931-sell-avgo`, `hourly-20260608-2231-sell-tsla`, `hourly-20260608-2251-sell-rgti` 4건 filled.
- Direct FILL activities: `get_account_activities(FILL, after=2026-06-05T00:00:00Z, page_size=100)` 성공. `2026-06-05 ET` 13-symbol buy cohort와 `2026-06-08 ET` sell/trim fills를 direct ledger로 재확인했다.
- Snapshots: `get_stock_snapshot(AVGO,RGTI,TSLA,JPM,SO,PFE,AMZN,COP,SLB,NVDA,V,AAPL,PLTR,FCX,WMT,BAC,NOK,SPY,QQQ,XLF,XLU,JNJ)`로 2026-06-08 ET close/prev close를 확보했다.
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## Review closeout metrics

- Benchmarks:
  - `SPY`: `737.45 -> 739.235`, `+0.24%`
  - `QQQ`: `705.375 -> 716.05`, `+1.51%`
  - `XLF`: `52.295 -> 51.985`, `-0.59%`
  - `XLU`: `44.36 -> 43.50`, `-1.94%`
- `2026-06-05 ET` fill cohort 1D returns:
  - `JPM -0.22%`, `SO -2.19%`, `PFE -1.84%`, `AMZN -3.14%`, `COP +1.28%`, `SLB +1.58%`, `NVDA -0.03%`, `V -0.68%`, `AAPL -3.73%`, `PLTR -1.49%`, `FCX -1.95%`, `WMT +0.04%`, `BAC -0.45%`.
- `2026-06-08 ET` sell/trim outcome checks:
  - `AVGO` trim fills `391.27` and `392.80`; same-day close `396.72`.
  - `TSLA` exit fill `398.59`; same-day close `408.95`; original entry `441.40`.
  - `RGTI` trim fill `21.48`; same-day close `21.77`; original avg entry `25.569583`.

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | not_applicable | 0 | account, orders, positions, activity, snapshots usable. |
| sec-edgar | gap | cancelled | 0 | `analyze_form4_transactions(AVGO, 30)` 및 `analyze_form4_transactions(JPM, 30)` current-run call이 모두 cancelled. |
| alpha-vantage | gap | provider_error | 0 | Required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check 성공. `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:AVGO})`는 daily-rate-limit payload 반환. |
| fred | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다. shell/curl probe는 수행하지 않았다. |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다. shell/curl probe는 수행하지 않았다. |
| yahoo-finance | usable | not_applicable | 0 | `AVGO/JPM/SO/NOK` news와 `JPM` recommendations query 성공. |

## Research context

- Alpaca news `AVGO/JPM/SO/NOK` query는 Benzinga 기반으로 AI drawdown, financials rotation, utility valuation/rate sensitivity, Nokia tape weakness 맥락을 보강했다.
- Yahoo Finance `JPM` recommendation breadth: latest `strongBuy 4 / buy 8 / hold 12 / sell 0 / strongSell 0`.
- Yahoo Finance `AVGO` news는 chip selloff, downgrade, AI-bubble warning, macro rate-jitters를 반복적으로 언급했다.
- Yahoo Finance `SO` news는 explicit catalyst보다 utility defensive narrative와 valuation/rate sensitivity를 보여줬다.
- Yahoo Finance `NOK` news는 AI infrastructure 기대와 급등 후 valuation debate가 혼재돼 있음을 보여줬다.

## Skipped recommendation evidence

- `JNJ`: `2026-06-08` close `232.15 USD` vs canceled limit `229.25 USD`, `+1.26%`.
- `NKE`: `2026-06-08` close/current `43.26 USD` vs canceled limit `43.20 USD`, `+0.14%`.
- `CVX`: `2026-06-08` close/current `189.10 USD` vs canceled limit `187.68 USD`, `+0.76%`.
- `NEE`: `2026-06-08` close/current `84.24 USD` vs canceled limit `85.47 USD`, `-1.44%`.

## Data gaps

- Alpaca `get_portfolio_history(period=1M,timeframe=1D,market_hours)`는 initial + 2 retries 모두 cancelled였다. 계좌 equity path와 max adverse/favorable move는 current-run에서 incomplete다.
- Alpha Vantage는 first non-PING call이 provider_error로 닫혀 추가 Alpha function은 호출하지 않았다.
- SEC EDGAR current-run call은 cancelled였고, FRED/Firecrawl은 namespace 미노출 상태였다.
