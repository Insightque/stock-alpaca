# 2026-06-16-0651-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0651` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 direct Alpaca MCP continuity check 기준 freshest direct IEX quote `QQQ 742.78/743.24`도 `2026-06-15T20:50:31.060889197Z`로 약 `62.84`분 stale이었다. `RGTI`는 spread 약 `0.3513%`, `NOK`는 `0.4051%`, `SLB/AVGO/PFE/MSFT/TSLA/GE/SMH`는 spread가 크게 벌어져 after-hours quote/spread hard gate를 넘지 못했고 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-0651-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-0651-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-0651-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `0651` preflight는 passing account/positions/open-order/asset/quote/snapshot/trade rows를 유지했고, direct Alpaca MCP continuity는 same-session fill/account/position/quote 상태 재확인에만 사용했다.

## Alpaca MCP 확인

- Regular market: closed (direct `get_clock.timestamp=2026-06-15T17:53:21.438063828-04:00`)
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `102577.82 USD`, cash `29836.36 USD`, buying power `306351.29 USD`였다.
- Positions / watchlists: direct `get_all_positions`, `get_watchlists` 기준 positions `33`건, watchlists `0`건이었다.
- Same-session after-hours fills: direct `get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)`와 scheduler-owned core preflight `orders_submitted=0`을 함께 사용해 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다. regular validation count는 재사용하지 않았다.
- Quote boundary: direct `get_stock_latest_quote(feed=iex)` 기준 freshest `QQQ`가 이미 `62.84`분 stale였고 `SLB`는 `82.85`분, `RGTI/NOK`는 `100.67-105.09`분, `AVGO/PFE/MSFT/TSLA/GE/SMH/SPY`는 `113.26-113.36`분 stale였다. `SPY`는 bid-only quote였고 submit-boundary evidence로 채택할 수 없었다.

## 후보 평가

- `QQQ`: direct IEX quote `742.78/743.24`, spread 약 `0.0619%`로 양호했지만 quote age가 약 `62.84`분으로 5분 cap을 넘었고 1주 ask `743.24 USD`는 after-hours per-order cap 약 `512.89 USD`도 초과했다.
- `RGTI`: residual speculative sleeve trim rationale는 유지됐지만 quote `22.73/22.81`, spread 약 `0.3513%`, age 약 `100.67`분으로 spread/freshness gate를 동시에 위반했다.
- `AVGO`: post-earnings staged de-risking trim 후보였지만 quote `375.72/408.22`, spread 약 `8.2915%`, age 약 `113.32`분으로 executable sell gate를 열지 못했다.
- `PFE`: repeated weak-review trim precedent가 남아 있었지만 quote `24.89/27.58`, spread 약 `10.2535%`, age 약 `113.33`분으로 blocked였다.
- `MSFT`: 1주 ask `424.01 USD`는 notional cap 이내였지만 spread 약 `11.8091%`, age 약 `113.30`분으로 buy fallback이 닫혔다.
- `NOK/SLB/TSLA/GE/SMH`: 모두 spread cap `0.25%`를 크게 넘기거나 freshness cap을 동시에 위반했다.
- Review backlog: `review-due-index` 기준 `pending_1d_count=18`, `pending_5d_count=19`, `pending_20d_count=1`이었다. 이번 cycle은 backlog throttle보다 fresh quote / spread hard gate가 직접 차단 요인이었다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_plus_direct_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with empty-order warning |
| fresh_quote | fail_direct_iex_quotes_stale_62_84_to_113_36_minutes |
| spread_within_after_hours_policy | fail_only_qqq_inside_spread_cap_but_stale_and_over_notional |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 fresh quote / spread hard gate가 먼저 닫혀 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 scheduler-owned preflight rows와 direct Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_watchlists`, `get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)`, `get_stock_latest_quote(feed=iex)` readback 기준 same-session after-hours fills `0`건, positions `33`건, watchlists `0`건, executable quote stack 부재를 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-0651-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-0651-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-0651-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-0651-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-0651-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-0651-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-0651-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-0651-after-hours-autopilot-post-trade.json`
