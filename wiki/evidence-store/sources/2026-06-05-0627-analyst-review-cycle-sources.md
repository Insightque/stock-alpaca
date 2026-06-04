---
id: 2026-06-05-0627-analyst-review-cycle-sources
created_at: 2026-06-04T21:27:37Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-05 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: `2026-06-04 17:21 ET` 기준 market closed, next open `2026-06-05 09:30 ET`.
- Account: ACTIVE, portfolio value `102,944.26 USD`, cash `30,487.94 USD`, buying power `253,654.69 USD`, long market value `72,456.32 USD`.
- Open US equity orders: 0.
- Current positions: 33 symbols.
- Recent orders: `get_orders(status=closed)`와 symbol/date-window cross-check로 `2026-05-26`, `2026-05-27`, `2026-05-28`, `2026-06-04` cohort fills와 cancels를 복원했다.
- Direct FILL activities: `get_account_activities_by_type(FILL, after=2026-05-22)` initial + 2 retries 모두 cancelled라 direct ledger read는 gap 처리했다.
- Portfolio history: `get_portfolio_history(period=1M, timeframe=1D)` initial + 2 retries 모두 cancelled라 account-level path 증거에서는 제외했다.
- Orders submitted/replaced/cancelled/closed by this workflow: `0 / 0 / 0 / 0`.

## Daily bar evidence

Alpaca MCP `get_stock_bars` with `feed=iex`, `timeframe=1Day`, `start=2026-05-26T00:00:00Z`, `end=2026-06-05T23:00:00Z` was used for 5D closeout and skipped-recommendation follow-up.

Benchmark closes used in this run:

| Reference | Start close | 2026-06-04 close | Return |
| --- | ---: | ---: | ---: |
| SPY from 2026-05-26 cohort | 754.68 | 756.97 | +0.30% |
| QQQ from 2026-05-26 cohort | 735.64 | 740.50 | +0.66% |
| SPY from 2026-05-27 cohort | 756.34 | 756.97 | +0.08% |
| QQQ from 2026-05-27 cohort | 738.21 | 740.50 | +0.31% |
| SPY from 2026-05-28 cohort | 758.44 | 756.97 | -0.19% |
| QQQ from 2026-05-28 cohort | 742.60 | 740.50 | -0.28% |

Relevant ETF references:

| ETF | Start close | 2026-06-04 close | Return | Usage |
| --- | ---: | ---: | ---: | --- |
| XLV | 148.52 | 152.04 | +2.37% | `LLY` healthcare compare |
| XLF | 51.57 / 51.43 | 52.20 | +1.22% / +1.50% | `BAC` financials compare |
| XLE | 56.31 / 57.29 | 58.77 | +4.37% / +2.58% | `XOM/CVX/SLB/COP` energy compare |
| XLU | 44.42 / 43.085 | 43.95 | -1.06% / +2.01% | `SO/NEE` utilities compare |
| XLY | 120.93 / 118.20 | 117.24 | -3.05% / -0.81% | `NKE/WMT/AMZN/TSLA` consumer compare |
| SMH | 600.01 | 628.51 | +4.75% | `NVDA/INTC/AI-adjacent` semiconductor compare |

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | cancelled | 2 | account/orders/positions/news/bars usable. `portfolio_history`와 direct `FILL` activities only cancelled. |
| sec-edgar | gap | cancelled | 1 | `get_financials(AVGO, income)` initial + retry 모두 cancelled. filing-grounded refresh는 이번 run에서 미사용. |
| alpha-vantage | gap | cancelled | 1 | Required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check는 성공. 이어 `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:AVGO})`가 cancelled되어 hard requirement대로 Alpha retries를 즉시 중단했다. |
| fred | gap | wrapper_error | 0 | registered callable namespace가 노출되지 않아 shell/curl probe 없이 wrapper error로 분류했다. |
| firecrawl | gap | wrapper_error | 0 | registered callable namespace가 노출되지 않아 shell/curl probe 없이 wrapper error로 분류했다. |
| yahoo-finance | usable | not_applicable | 0 | `AVGO`, `PLTR`, `WMT` news 조회 성공. AVGO post-earnings selloff와 PLTR/Google partnership 흐름을 보조 컨텍스트로 사용했다. |

## News and event context

- Yahoo Finance `AVGO` news는 `2026-06-04` earnings 이후 Broadcom sell-off가 megacap history급 drawdown으로 인식되고 있음을 보여줬다.
- Alpaca `AVGO` news는 mixed Q2 results, AI revenue surge narrative, analyst PT revision, 그리고 semiconductor risk-off session을 함께 보여줬다.
- Yahoo Finance와 Alpaca `PLTR` news는 Google Cloud partnership 및 AIPCon announcements로 software/AI momentum이 완전히 꺾이지 않았음을 시사했다.
- Yahoo Finance `WMT` news는 loyalty rollout과 price-warning narrative가 혼재했다. `WMT` 5D 결과가 benchmark 초과로 이어지지 못한 점과 정합적이다.
- HOOD skipped-candidate follow-up은 Alpaca daily bars로만 판단했다. `2026-05-28` plan limit `77.26` 대비 `2026-06-04` close `88.315`다.

## Data gaps

- Alpaca account-level path metrics are incomplete because `get_portfolio_history` remained cancelled after the allowed retry count.
- Direct fill-ledger confirmation is incomplete because `get_account_activities_by_type(FILL)` remained cancelled after the allowed retry count.
- SEC EDGAR and Alpha Vantage both ended in cancelled gaps, so filing/earnings detail was not promoted into policy evidence.
- FRED and Firecrawl were not exposed as callable namespaces in this runtime and were classified as `wrapper_error`.
