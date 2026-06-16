# 2026-06-17-0611-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0611` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-16T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex|overnight)` 범위에서 regular market closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours submitted orders `0`, same-session fills `0`, watchlists `0`를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 모든 runtime submit-boundary quote가 `5분` freshness cap을 넘겨 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-17-0611-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-17-0611-after-hours-autopilot-research-mcp-preflight.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-17-0611-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/open-order/asset/quote/spread rows는 그대로 사용했다. live continuity는 account/orders/activities/watchlists/quote freshness만 재확인했고, asset evidence는 동일 preflight row를 유지했다.

## Alpaca MCP 확인

- Regular market: live `get_clock`=`2026-06-16T17:12:49.871615149-04:00` 기준 closed였다.
- Account: live `get_account_info` 기준 account `ACTIVE`, cash `30,344.81 USD`, portfolio value `100,701.96 USD`, buying power `302,542.06 USD`였다.
- Positions: live `get_all_positions` 기준 positions `33`건이었다.
- Open orders: live `get_orders(status=open)` 기준 `0`건이었다.
- Same-session after-hours orders/fills: live `get_orders(status=all, after=2026-06-16T20:00:00Z)` 기준 `0`건, live `get_account_activities(activity_types=FILL, after=2026-06-16T20:00:00Z)` 기준 fill `0`건이었다. `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다.
- Watchlists: live `get_watchlists` 기준 `0`건이었다.

## 후보 평가

- `QQQ`: IEX quote `729.73/729.83`, spread 약 `0.0137%`, age 약 `21.26분`으로 freshest candidate였지만 quote freshness fail이었고 1주 ask `729.83 USD`는 after-hours per-order cap 약 `503.38 USD`를 넘었다.
- `IONQ`: IEX quote `56.51/56.56`, spread 약 `0.0884%`, notional은 cap 이내였지만 age 약 `41.84분`으로 fresh-quote hard gate를 통과하지 못했다.
- `QBTS`: IEX quote `24.11/24.26`, age 약 `50.66분`, spread 약 `0.6202%`로 freshness와 spread가 모두 blocker였다.
- `JPM`: IEX quote `329.45/330.99`, age 약 `69.01분`, spread 약 `0.4662%`였다.
- `PFE`: IEX quote `26.01/26.13`, age 약 `71.83분`, spread 약 `0.4602%`였다.
- `MSFT`: IEX quote `392.89/424.01`, age 약 `21.02분`, spread 약 `7.6197%`였다.
- `AVGO` sell/trim: sell side 허용 정책에 따라 재평가했지만 IEX quote `362.60/402.11`, age 약 `72.83분`, spread 약 `10.3349%`로 after-hours hard gate를 통과하지 못했다.
- `SO` sell/trim: IEX quote `88.70/99.36`, age 약 `72.83분`, spread 약 `11.3361%`였다.
- `RGTI` sell/trim: IEX quote `17.65/23.66`, age 약 `72.81분`, spread 약 `29.0765%`였다. 같은 날짜 regular-session canceled sell history도 남아 있어 freshness 문제가 풀려도 duplicate-side discipline 재검토가 필요하다.
- Review backlog: `wiki/trade-ledger/reviews/review-due-index.json` 기준 `pending_1d_count=18`, `pending_5d_count=19`, `pending_20d_count=1`였다. 이번 cycle은 backlog throttle보다 fresh-quote hard gate가 직접 차단 요인이었다.

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
| fresh_quote | fail_live_iex_and_overnight_quotes_older_than_5_minutes |
| spread_within_after_hours_policy | fail_no_candidate_met_fresh_and_spread_and_notional_together |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-0611-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-0611-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-17-0611-after-hours-autopilot.json` PASS with expected `orders is empty` warning

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-17-0611-after-hours-autopilot.md`
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-17-0611-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-0611-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-0611-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-17-0611-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade: `wiki/trade-ledger/positions/2026-06-17-0611-after-hours-autopilot-post-trade.json`

