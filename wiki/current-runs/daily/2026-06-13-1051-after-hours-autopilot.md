# 2026-06-13-1051-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1051` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence 기준 freshest shortlisted candidate `QQQ`조차 `2026-06-12T20:57:37.534220888Z`로 scheduler clock 대비 약 `293.54`분 stale이었다. 이번 cycle은 user-mandated scheduler-owned preflight만 사용했고, 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-13-1051-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-13-1051-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/quote/snapshot/trade rows는 그대로 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-12T21:51:09.744886254-04:00` scheduler-owned `get_clock`)
- Account/positions: scheduler-owned `get_account_info`, `get_all_positions` 기준 account `ACTIVE`, portfolio value `100646.86 USD`, cash `31950.36 USD`, buying power `303392.01 USD`, long market value `68696.50 USD`, positions `33`건이었다.
- Open orders: scheduler-owned `get_orders(status=open)` 기준 `0`건이었다.
- Same-session after-hours orders: same preflight의 open-order/account-activity snapshot에는 `2026-06-12T20:00:00Z` 이후 same-session after-hours order/fill evidence가 없었다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap은 `0/2`로 유지했다.
- Watchlists: scheduler-owned `get_watchlists`는 `0`건이었다.
- Quote/spread boundary: scheduler-owned `1051` Alpaca core preflight의 passing asset/quote/spread rows를 submit-boundary evidence로 유지했다. 해당 rows만으로도 freshest `QQQ/MSFT/SMH`가 각각 `293.54/308.61/296.53`분 stale이었고 `SPY/AVGO/SO/INTC/MU`는 약 `351.16`~`351.14`분 stale 또는 spread/notional cap fail이라 submit path를 열 수 없었다.

## 후보 평가

- `QQQ`: IEX quote `722.00/722.21`, spread 약 `0.0291%`로 양호했지만 timestamp가 `2026-06-12T20:57:37.534220888Z`라 scheduler clock 기준 약 `293.54`분 stale이었다. 동시에 1주 ask `722.21 USD`는 after-hours per-order cap 약 `503.23 USD`를 넘었다.
- `MSFT`: IEX quote `390.76/390.99`, spread 약 `0.0588%`와 1주 ask `390.99 USD`는 cap 이내였지만 timestamp가 `2026-06-12T20:42:33.3236562Z`라 약 `308.61`분 stale이었다.
- `SMH`: quote `619.72/624.79`, spread `0.8148%`, ask `624.79 USD`, age 약 `296.53`분으로 spread/freshness/notional이 모두 blocker였다.
- `SPY`: quote `718.43/762.94`, spread `6.0093%`, age 약 `351.16`분, ask `762.94 USD`로 benchmark fallback submit path에 진입하지 못했다.
- `AVGO` sell/trim: sell side 허용 정책에 따라 우선 재평가했지만 IEX quote `364.15/397.47`, spread `8.7498%`, age 약 `351.16`분으로 after-hours hard gate를 통과하지 못했다.
- `SO` sell/trim: IEX quote `89.83/98.54`, spread `9.2478%`, age 약 `351.16`분이며 기존 trim decision-grade metric gap도 유지됐다.
- `INTC` / `MU`: both quotes were older than `351.14` minutes and spread `9.6733%`, `9.8224%`로 cap을 크게 넘겼다. `MU`는 1주 ask `1040.42 USD`로 per-order cap도 초과했다.
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
| risk_policy | fail_no_eligible_order_survived_after_hours_fresh_quote_gate |
| fresh_quote | fail_scheduler_iex_quotes_stale_293.54_to_351.16_minutes |
| spread_within_after_hours_policy | fail_only_qqq_msft_inside_spread_cap_but_stale_or_over_notional |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Validators

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-13-1051-after-hours-autopilot.json`
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-13-1051-after-hours-autopilot.json`
- `/usr/local/bin/python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-13-1051-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-13-1051-after-hours-autopilot.md`
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-13-1051-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-13-1051-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-13-1051-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade: `wiki/trade-ledger/positions/2026-06-13-1051-after-hours-autopilot-post-trade.json`
