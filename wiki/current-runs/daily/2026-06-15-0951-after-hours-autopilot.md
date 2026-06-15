# 2026-06-15-0951-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0951` core/research preflight를 source-of-record로 사용했다. `0951` Alpaca core preflight는 expected `first_blocking_gate=market_closed`만 남기고 passing row를 비워 두었으므로, after-hours workflow 지침대로 missing after-hours-required row만 direct Alpaca MCP continuity pass로 보강했다. direct overnight latestQuote 기준 `AVGO`가 fresh/spread/notional/asset/session-budget gate를 모두 통과한 유일한 sell-first executable trim 후보여서 1주 trim sell을 제출했고, immediate reconciliation 결과 same `client_order_id`가 `status=new` open order로 남아 있다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-15-0951-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-15-0951-after-hours-autopilot-research-mcp-preflight.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-15-0951-after-hours-autopilot-runtime-alpaca-spot-check.json`
- `0951` Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다. 다만 passing row가 없었기 때문에 account/positions/open-orders/asset/quote/snapshot/watchlists는 direct Alpaca MCP read-only call로 한 번만 보강했다.

## Alpaca MCP 확인

- Regular market: direct `get_clock`=`2026-06-14T20:53:15.380822258-04:00` 기준 closed였다.
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `101911.69 USD`, cash `31950.34 USD`, buying power `306437.69 USD`였다.
- Positions: direct `get_all_positions` 기준 positions `33`건이었다. submit 후에도 total `AVGO qty=4`는 유지됐고 `qty_available=3`로 감소해 1주 open sell reservation이 반영됐다.
- Open orders: submit 전 direct `get_orders(status=open)`는 `0`건이었고, submit 후 same `client_order_id=ah-20260615-0951-sell-avgo-01` readback은 `status=new` open order `1`건이다.
- Same-session after-hours orders/fills: direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` 기준 submit 전에는 모두 `0`건이었다. submit 후 same-session after-hours submitted orders는 `1`, fills는 아직 `0`이다. separate after-hours session budget은 `1/2`가 남는다.
- Watchlists: direct `get_watchlists` 기준 `0`건이었다.

## 후보 평가

- `AVGO` sell/trim: direct overnight latestQuote `391.91/392.07`, spread `0.0408%`, quote age 약 `0.32`분, held qty `4`, asset `active/tradable`, same-session duplicate `0`이라 sell-first executable trim 후보로 선택했다. `[[AVGO]]`, `[[2026-06-15-portfolio-review]]`, `[[2026-06-13-portfolio-review]]`, `[[2026-06-12-1411-after-hours-autopilot]]`에는 staged de-risking과 ai_semiconductor warning-band 유지 판단이 누적돼 있다.
- `MSFT`: direct overnight latestQuote `395.25/395.51`, spread `0.0658%`, quote age 약 `0.32`분으로 buy fallback 조건은 통과했지만, learning-trade directive가 executable sell trim을 우선하므로 fallback으로만 유지했다.
- `QQQ` / `SPY` / `SMH` / `MU`: fresh overnight quote는 확보됐지만 1주 notional이 after-hours per-order cap 약 `509.56 USD`를 넘었다.
- `SO`: overnight quote `88.06/96.14`, spread `8.7764%`, quote age 약 `5.25`분으로 hard gate fail이다.
- `INTC`: overnight quote는 fresh했지만 held position이 없어 sell/trim executable path에 진입하지 못했다.
- Review backlog: `wiki/trade-ledger/reviews/review-due-index.json` 기준 `pending_1d_count=1`, `pending_5d_count=16`, `pending_20d_count=1`이다. 이번 cycle에서는 buy throttle보다 sell-first `AVGO` trim path가 먼저 열렸다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours_missing_preflight_rows_supplemented_by_direct_mcp |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted_then_one_open |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | pass_runtime_overnight_quote_under_5_minutes |
| spread_within_after_hours_policy | pass_runtime_overnight_spread_0.0408pct |
| whole_share_day_limit_extended_hours_order | pass_avgo_sell_order_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_client_order_id_reconciled_open_new_lifecycle_recorded |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-15-0951-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-15-0951-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-15-0951-after-hours-autopilot.json` -> PASS

## Submit And Reconcile

- Submitted order: `AVGO` sell `1` share, `limit_price=391.91`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260615-0951-sell-avgo-01`
- Alpaca MCP `place_stock_order` returned `order_id=b1ee30b8-92d8-4d0e-a9a1-a66c02c136a2`, initial `status=pending_new`, `submitted_at=2026-06-15T00:59:05.194515367Z`.
- Immediate `get_order_by_client_id`와 `get_orders(status=all|open, symbols=AVGO)` readback은 same `client_order_id`를 `status=new`, `filled_qty=0`로 재확인했다.
- `get_all_positions` cross-check에서는 total `AVGO qty=4`가 유지됐고 `qty_available=3`로 감소해 open sell reservation을 확인했다. `get_account_activities(...FILL...)`는 아직 빈 결과였다.
- policy `cancel_unfilled_after_minutes=5`는 후속 scheduler lifecycle에서 처리하도록 남기고, 이번 cycle은 no-retry open order lifecycle record로 종료한다. 다른 `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-15-0951-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-15-0951-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-15-0951-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-15-0951-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-15-0951-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade: `wiki/trade-ledger/positions/2026-06-15-0951-after-hours-autopilot-post-trade.json`
