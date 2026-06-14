# 2026-06-14-1431-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1431` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence 기준 freshest shortlisted candidate `QQQ`조차 `2026-06-12T20:57:37.534220888Z`로 `1431` scheduler clock 대비 약 `1953.51`분 stale이었다. live Alpaca MCP continuity spot check도 account `ACTIVE`, positions `33`, open orders `0`, watchlists `0`, same-session after-hours orders/fills `0`, 그리고 shortlist IEX quote parity를 재확인했지만 fresh-quote hard gate를 다시 열지 못해 이번 cycle은 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-14-1431-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-14-1431-after-hours-autopilot-research-mcp-preflight.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-14-1431-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/open-order/asset/quote/snapshot/trade-state rows는 그대로 사용했다. 이번 turn에서는 scheduler-owned `1431` `get_clock`와 `get_orders_open`를 market-clock/open-order source-of-record로 유지하면서 live Alpaca MCP continuity probe를 별도로 재실행했다.

## Alpaca MCP 확인

- Regular market: closed (scheduler-owned `1431` preflight `get_clock`=`2026-06-14T01:31:08.416339082-04:00` 기준)
- Account: live `get_account_info` + scheduler-owned `1431` preflight `get_account_info` 기준 account `ACTIVE`, portfolio value `100415.12 USD`, cash `31950.34 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다.
- Positions: live `get_all_positions` + scheduler-owned `1431` preflight `get_all_positions` 기준 positions `33`건이었다.
- Open orders: live `get_orders(status=open)` + scheduler-owned `1431` preflight `get_orders_open` 기준 `0`건이었다.
- Same-session after-hours orders: live `get_orders(status=all, after=2026-06-13T20:00:00Z)` 결과가 빈 배열이었고 scheduler-owned `1431` `orders_submitted=0`도 유지돼 신규 same-session after-hours order는 `0`건이었다. `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다.
- Same-session fills: live `mcp__alpaca.get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)` 결과가 빈 배열이라 신규 same-session after-hours fill도 `0`건이었다.

## 후보 평가

- `QQQ`: IEX quote `722.00/722.21`, spread 약 `0.0291%`로 양호했지만 timestamp가 `2026-06-12T20:57:37.534220888Z`라 `1431` scheduler clock 기준 약 `1953.51`분 stale이었다. 동시에 1주 ask `722.21 USD`는 after-hours per-order cap 약 `502.08 USD`를 넘었다.
- `MSFT`: IEX quote `390.76/390.99`, spread 약 `0.0588%`와 1주 ask `390.99 USD`는 cap 이내였지만 timestamp가 `2026-06-12T20:42:33.3236562Z`라 약 `1968.58`분 stale이었다.
- `SMH`: quote `619.72/624.79`, spread `0.8148%`, ask `624.79 USD`, age 약 `1956.51`분으로 spread/freshness/notional이 모두 blocker였다.
- `SPY`: quote `718.43/762.94`, spread `6.0093%`, age 약 `2011.14`분, ask `762.94 USD`로 benchmark fallback submit path에 진입하지 못했다.
- `AVGO` sell/trim: sell side 허용 정책에 따라 우선 재평가했지만 IEX quote `364.15/397.47`, spread `8.7498%`, age 약 `2011.14`분으로 after-hours hard gate를 통과하지 못했다.
- `SO` sell/trim: IEX quote `89.83/98.54`, spread `9.2478%`, age 약 `2011.14`분이었다.
- `INTC` / `MU`: both quotes were older than `2011.14` / `2011.12` minutes and spread `9.6733%`, `9.8224%`로 cap을 크게 넘겼다. `MU`는 1주 ask `1040.42 USD`로 per-order cap도 초과했다. `INTC`는 current position이 없어 sell/trim executable path에도 진입하지 못했다.
- Runtime continuity scope: live Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-13T20:00:00Z)`, `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=iex|overnight)`, `get_stock_snapshot(feed=overnight)`로 continuity를 재확인했다. scheduler-owned `1431` core preflight submit-boundary rows와 live IEX quotes는 일치했고, overnight readback은 전 종목에서 더 오래된 timestamp만 반환했다.
- Review backlog: `review-due-index` 기준 `pending_1d_count=1`, `pending_5d_count=16`, `pending_20d_count=1`였다. 이번 cycle은 backlog throttle보다 fresh-quote hard gate가 직접 차단 요인이었다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS_empty_order_plan_warning_only |
| fresh_quote | fail_scheduler_and_live_iex_quotes_stale_1953.51_to_2011.14_minutes |
| spread_within_after_hours_policy | fail_only_qqq_msft_inside_spread_cap_but_stale_or_over_notional |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-14-1431-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-14-1431-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-14-1431-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-14-1431-after-hours-autopilot.md`
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-14-1431-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-14-1431-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-14-1431-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-14-1431-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade: `wiki/trade-ledger/positions/2026-06-14-1431-after-hours-autopilot-post-trade.json`
