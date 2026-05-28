# 2026-05-29 08:31 after-hours autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: submit eligible only if all gates pass; this run submitted nothing.

## Gate Summary

| Gate | Result | Note |
|---|---:|---|
| `ALPACA_PAPER_TRADE=true` | PASS | 환경 변수 확인 |
| Regular market not open | PASS | scheduler Alpaca MCP preflight clock `is_open=false`, timestamp `2026-05-28T19:31:15.438695754-04:00`; `market_closed` is expected and nonblocking for after-hours |
| Alpaca core MCP | PASS | scheduler preflight account, positions, open orders, assets, quotes, spreads, and activities rows usable; fresh account/positions/open-order/order-session checks returned |
| Universe strict | PASS | 62 symbols, `SPY`/`QQQ` 포함 |
| MCP strict | PASS | sec-edgar/FRED/firecrawl/yahoo pass, alpha-vantage empty_response gap; submit 기준 3개 이상 충족 |
| Separate after-hours budget | PASS | `risk_inputs.after_hours_new_orders_submitted_today=0`, same after-hours session order query after `2026-05-28T20:00:00Z` returned `[]` |
| Quote freshness | FAIL | scheduler IEX quote timestamps were `2026-05-28T20:00:00Z` to `20:59:59Z`, exceeding 5 minutes at the scheduler clock |
| Spread | PARTIAL | only `QQQ` was within the 0.25% after-hours spread cap; all other shortlisted symbols failed |
| Risk policy | PASS_EMPTY_PLAN | empty plan validator used; no order eligible |

## Candidate Diagnostics

| Symbol | Decision | Quote timestamp | Spread % | Spread gate |
|---|---|---:|---:|---|
| QQQ | skip, stale quote | 2026-05-28T20:44:11.568144727Z | 0.0122 | pass |
| NOK | skip, stale quote | 2026-05-28T20:59:59.217574313Z | 0.6485 | fail |
| SMH | skip, stale quote | 2026-05-28T20:00:00.003012715Z | 5.9753 | fail |
| SPY | skip, stale quote | 2026-05-28T20:00:00.004066085Z | 6.0058 | fail |
| NVDA | skip, stale quote | 2026-05-28T20:00:01.385857787Z | 6.6999 | fail |
| ADBE | skip, stale quote | 2026-05-28T20:00:00.000648436Z | 8.3139 | fail |
| LIN | skip, stale quote | 2026-05-28T20:00:00.013587475Z | 8.3371 | fail |
| XOM | skip, stale quote | 2026-05-28T20:00:00.003213168Z | 8.4148 | fail |

## Submit/Reconcile

No `place_stock_order` call was made. Because the first blocking gate was `fresh_quote`, no pre-submit gate summary was emitted and no `client_order_id` was created. There was no reconcile step to run.

## Validators

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-0831-after-hours-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-0831-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-29-0831-after-hours-autopilot.json`: PASS with `orders is empty` warning

## Artifacts

- Order plan: `wiki/trade-ledger/orders/2026-05-29-0831-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-05-29-0831-after-hours-autopilot.json`
- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-29-0831-after-hours-autopilot-alpaca-core-preflight.json`
- Research preflight: `wiki/evidence-store/sources/2026-05-29-0831-after-hours-autopilot-research-mcp-preflight.json`
