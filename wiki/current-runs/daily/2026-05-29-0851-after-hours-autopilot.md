# 2026-05-29 08:51 after-hours autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: submit eligible only if all gates pass; this run submitted nothing.

## Gate Summary

| Gate | Result | Note |
|---|---:|---|
| `ALPACA_PAPER_TRADE=true` | PASS | 환경 변수 확인 |
| Regular market not open | PASS | live Alpaca MCP clock `is_open=false`, timestamp `2026-05-28T19:52:56.886023063-04:00`; scheduler preflight `market_closed` is expected and nonblocking for after-hours |
| Alpaca core MCP | PASS | scheduler preflight account, positions, open orders, assets, quotes, spreads, and activities rows usable; live clock/account/positions/QQQ asset/overnight quote checks returned |
| Universe strict | PASS | 62 symbols, `SPY`/`QQQ` 포함 |
| MCP strict | PASS | sec-edgar/firecrawl/yahoo pass; alpha-vantage empty_response gap; FRED 504 provider_error; submit 기준 3개 이상 충족 |
| Separate after-hours budget | PASS | `risk_inputs.after_hours_new_orders_submitted_today=0`; 정규장 validation order count를 재사용하지 않음 |
| Quote freshness | FAIL | live overnight quote timestamps were around `2026-05-28T08:00:00Z`, exceeding 5 minutes at the live Alpaca clock |
| Spread | FAIL | all live overnight quote rows exceeded the 0.25% after-hours spread cap |
| Risk policy | PASS_EMPTY_PLAN | empty plan validator used; no order eligible |

## Candidate Diagnostics

| Symbol | Decision | Quote timestamp | Spread % | Spread gate |
|---|---|---:|---:|---|
| QQQ | skip, stale quote | 2026-05-28T08:00:00.395114157Z | 0.5038 | fail |
| NOK | skip, stale quote | 2026-05-28T08:00:00.400591937Z | 7.8538 | fail |
| SMH | skip, stale quote | 2026-05-28T08:00:00.363332271Z | 3.2790 | fail |
| SPY | skip, stale quote | 2026-05-28T08:00:00.392695489Z | 0.3189 | fail |
| NVDA | skip, stale quote | 2026-05-28T08:00:00.398909979Z | 5.5668 | fail |
| ADBE | skip, stale quote | 2026-05-28T08:00:00.386648870Z | 16.4344 | fail |
| LIN | skip, stale quote | 2026-05-28T08:00:00.325235053Z | 3.9077 | fail |
| XOM | skip, stale quote | 2026-05-28T08:00:00.391609286Z | 10.1786 | fail |

## Submit/Reconcile

No `place_stock_order` call was made. Because the first blocking gate was `fresh_quote`, no pre-submit gate summary was emitted and no `client_order_id` was created. There was no reconcile step to run.

## Validators

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-0851-after-hours-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-0851-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-29-0851-after-hours-autopilot.json`: PASS with `orders is empty` warning

## Artifacts

- Order plan: `wiki/trade-ledger/orders/2026-05-29-0851-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-05-29-0851-after-hours-autopilot.json`
- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-29-0851-after-hours-autopilot-alpaca-core-preflight.json`
- Research preflight: `wiki/evidence-store/sources/2026-05-29-0851-after-hours-autopilot-research-mcp-preflight.json`
