---
id: 2026-06-08-0622-analyst-review-cycle-sources
created_at: 2026-06-07T21:22:00Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-08 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-07 17:22 ET` 기준 market closed, next open `2026-06-08 09:30 ET`.
- Account: ACTIVE, portfolio value `98,156.33 USD`, cash `29,947.79 USD`, buying power `294,276.14 USD`, long market value `68,208.54 USD`.
- Open US equity orders: 0.
- Current positions: 33 symbols.
- Recent orders: `get_orders(status=all, after=2026-06-04T00:00:00Z)`로 `INTC/JPM/AVGO/SO/PFE/AMZN/COP/SLB/NVDA/V/AAPL/PLTR/FCX/WMT/BAC` fill과 `NKE/CVX/NEE/JNJ` cancel을 cross-check했다.
- Direct FILL activities: `get_account_activities(FILL, after=2026-06-04T00:00:00Z, page_size=100)` 성공. `AVGO` partial fills, `INTC` exit fill, `2026-06-05 ET` buy cohort fills를 direct ledger로 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## Review-due scan

- `2026-06-07 ET` close 기준 새로 maturity에 도달한 `1D/5D/20D` horizon은 없다.
- `2026-06-05 ET` fill cohort `JPM/SO/PFE/AMZN/COP/SLB/NVDA/V/AAPL/PLTR/FCX/WMT/BAC` 1D는 `2026-06-08 ET` regular close 이후에만 평가 가능하다.
- `2026-06-04 ET` fill cohort `QQQ/SPY/SLB/AAPL/XOM/WMT/FCX/COP/GOOGL/MSFT/NEE/V/NKE/SO/BAC/PLTR` 5D는 `2026-06-11 ET` regular close 이후다.
- `NOK` 20D add-block review는 기존 일정대로 `2026-06-18 ET` regular close 이후다.

## Alpaca position snapshot references

| Ticker | Avg entry | 2026-06-07 ET close/current | Unrealized | Note |
| --- | ---: | ---: | ---: | --- |
| AVGO | 414.940833 | 385.73 | -7.04% | post-earnings drawdown 유지, 이미 4주 trim 완료 |
| JPM | 311.81 | 312.37 | +0.18% | first-close positive 유지, 공식 1D 전 |
| SO | 92.696 | 92.60 | -0.10% | defensive hold thesis 대기 |
| NOK | 15.044527 | 14.38 | -4.42% | add-block 유지 |
| PFE | 26.17 | 26.04 | -0.50% | 1D horizon 전이라 waiting |
| NVDA | 215.031579 | 205.10 | -4.62% | AI/semiconductor de-risking 영향 지속 |

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | not_applicable | 0 | account/orders/positions/fill ledger usable. |
| sec-edgar | gap | cancelled | 2 | `get_insider_summary(AVGO, 30)` initial + 2 retries 모두 cancelled. 추가 probing 없이 종료했다. |
| alpha-vantage | usable | not_applicable | 0 | Required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check 성공 후 `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:AVGO})`도 성공했다. |
| fred | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다. shell/curl probe는 수행하지 않았다. |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 이 runtime에 노출되지 않았다. shell/curl probe는 수행하지 않았다. |
| yahoo-finance | usable | not_applicable | 0 | `AVGO/JPM/SO/NOK` news와 `JPM` recommendations query 성공. |

## Research context

- Alpha Vantage `EARNINGS(AVGO)`는 latest quarter `fiscalDateEnding=2026-04-30`, `reportedDate=2026-06-03`, `reportedEPS=2.44`, `estimatedEPS=2.39`, `surprise=0.05`, `surprisePercentage=2.0921`, `reportTime=post-market`를 반환했다.
- Yahoo Finance `AVGO` news는 AI/semiconductor selloff, rate-jitters, Broadcom earnings 해석 악화를 반복적으로 언급했다.
- Yahoo Finance `JPM` news는 stress-test 이후 capital return narrative와 broad financials context가 주를 이뤘고, recommendations breadth는 `strongBuy 4 / buy 8 / hold 12 / sell 0 / strongSell 0`였다.
- Yahoo Finance `SO` news는 explicit catalyst 부재 속 utility defensive/valuation/rate sensitivity narrative가 계속 유지됨을 보여줬다.
- Yahoo Finance `NOK` news는 AI infrastructure 기대와 급등 후 valuation re-rating 논쟁이 혼재돼 있었고, recent tape weakness를 상쇄할 새 확정 촉매는 보이지 않았다.

## Skipped recommendation evidence

- `JNJ` canceled limit `229.25 USD` 대비 `2026-06-05` close `232.71 USD`, change `+1.51%`.
- `NKE` close-race canceled limit `43.20 USD` 대비 `2026-06-05` close `42.98 USD`, change `-0.51%`.
- `CVX` same-session canceled limit `187.68 USD` 대비 `2026-06-05` close `187.31 USD`, change `-0.20%`.
- `NEE` same-session canceled limit `85.47 USD` 대비 `2026-06-05` close `85.825 USD`, change `+0.42%`.

## Data gaps

- SEC EDGAR filing-grounded refresh is incomplete because the current-run query remained cancelled after the allowed retry count.
- FRED and Firecrawl were not exposed as callable namespaces in this runtime and were classified as `wrapper_error`.
- No new due horizon closed in this run, so current review remains a waiting/monitoring cycle rather than a fresh decision-quality closeout.
