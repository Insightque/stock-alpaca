# 2026-06-18-0631-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0631` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 preflight의 passing account/positions/open-orders/asset/quote/spread rows를 submit-boundary evidence로 유지했고, separate after-hours order budget은 `0/2`로 열려 있었지만 freshest scheduler-owned quote `MS`도 `2026-06-17T20:20:00.57860736Z` 기준 약 `73.21`분 stale이었다. `QQQ`는 spread는 통과했지만 stale+per-order notional cap에, `MS/PFE/RGTI/AVGO/NVDA/SPY/TSLA/GOOGL/WMT/JPM`은 stale+spread gate에 막혀 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-18-0631-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-18-0631-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-0631-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-18-0631-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle은 사용자가 scheduler-owned quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 direct Alpaca continuity는 regular market closed, account/positions/open-orders parity, watchlists, same-session order budget 확인에만 제한했다.

## Alpaca MCP 확인

- Regular market: closed (direct `get_clock.timestamp=2026-06-17T17:33:13.152917931-04:00`)
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `100,524.49 USD`, cash `28,003.45 USD`, buying power `299,437.89 USD`
- Positions / open orders / watchlists: direct `get_all_positions` 기준 positions `34`건, direct `get_orders(status=open)` 기준 open orders `0`건, direct `get_watchlists` 기준 watchlists `0`건이었다.
- Same-session after-hours orders: direct `get_orders(status=all, after=2026-06-17T20:00:00Z)`에서는 regular-session `SBUX` cancel 1건만 보였고 `ah-` prefix after-hours submit은 없었다. 노출된 Alpaca 도구셋에는 `get_account_activities`가 없어 fill count는 별도 조회하지 못했지만, same-session `ah-` prefix order 부재와 open orders `0`을 근거로 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다.
- Quote boundary: 이번 cycle의 submit-boundary quote/spread evidence는 scheduler-owned `0631` preflight의 `get_stock_latest_quote(feed=iex)` row를 그대로 사용했다. freshest quote는 `MS` `2026-06-17T20:20:00.57860736Z`였고 나머지 evaluated stack은 약 `73.21`분에서 `93.22`분 stale이었다.

## 후보 평가

- `PFE` sell/trim: scheduler quote `24.70/27.38`, spread 약 `10.2897%`, age 약 `93.19`분. repeated weak-review trim rationale는 유지됐지만 freshness/spread 동시 fail.
- `RGTI` sell/trim: scheduler quote `17.57/23.11`, spread 약 `27.2152%`, age 약 `93.2`분. residual speculative sleeve trim rationale는 유지됐지만 freshness/spread 동시 fail.
- `AVGO` sell/trim: scheduler quote `377.01/416.43`, spread 약 `9.9318%`, age 약 `93.21`분. sell side 허용 policy는 유지됐지만 executable sell gate는 닫혀 있었다.
- `QQQ` buy fallback: scheduler quote `722.87/723.00`, spread 약 `0.0180%`로 양호했지만 age 약 `93.15`분으로 stale이고 1주 ask `723.00 USD`가 after-hours per-order cap 약 `502.70 USD`를 넘었다.
- `MS` buy fallback: scheduler quote `220.00/231.46`, spread 약 `5.0777%`, age 약 `73.21`분. freshest scheduler research-shortlist quote였지만 spread/freshness가 모두 fail했다.
- Review backlog: `wiki/trade-ledger/reviews/review-due-index.json` 기준 `pending_1d_count=0`, `pending_5d_count=37`, `pending_20d_count=1`, `blocked_add_symbols=["NOK"]`였다. 이번 cycle은 backlog throttle보다 fresh-quote hard gate가 직접 차단 요인이었다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_plus_live_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with expected `orders is empty` warning |
| fresh_quote | fail_scheduler_owned_submit_boundary_quotes_stale_73.21_to_93.22_minutes |
| spread_within_after_hours_policy | fail_no_candidate_met_fresh_and_spread_and_notional_together |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 fresh quote hard gate가 먼저 닫혀 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 direct Alpaca continuity 기준 open orders `0`, positions `34`, same-session `ah-` prefix submitted `0` 확인으로 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-0631-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-0631-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-18-0631-after-hours-autopilot.json` PASS with expected `orders is empty` warning

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-18-0631-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0631-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0631-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-0631-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-18-0631-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0631-after-hours-autopilot-post-trade.json`
