# 2026-06-18-0611-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0611` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 live Alpaca continuity `get_stock_latest_quote(feed=iex)` 기준 freshest `MSFT`도 `2026-06-17T20:00:16.205552018Z`로 약 `73.32`분 stale이었다. `PFE/RGTI/AVGO/WMT/JPM/NVDA/GOOGL/SPY`는 stale에 더해 spread hard gate도 동시에 위반했고, `QQQ`만 spread는 통과했지만 freshness와 per-order notional cap에 막혀 executable stack을 만들지 못해 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-18-0611-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-18-0611-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-0611-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle은 같은 preflight의 passing account, positions, open-orders, asset, quote rows를 source-of-record로 유지하고, live Alpaca continuity는 regular market closed 확인, same-session budget 확인, current executable quote freshness 확인에만 제한했다.

## Alpaca MCP 확인

- Regular market: closed (direct `get_clock.timestamp=2026-06-17T17:13:35.371119702-04:00`)
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `100,545.82 USD`, cash `28,003.45 USD`, buying power `299,481.20 USD`
- Positions / open orders / watchlists: direct `get_all_positions` 기준 positions `34`건, direct `get_orders(status=open)` 기준 open orders `0`건이었다. same source-of-record preflight와 충돌은 없었다.
- Same-session after-hours orders: direct `get_orders(status=all, after=2026-06-17T16:00:00-04:00)`에서는 regular-session `SBUX` cancel 1건만 보였고 `ah-` prefix after-hours submit은 없었다. direct `get_account_activities(activity_types=[FILL], after=2026-06-17T16:00:00-04:00)` 기준 same-session after-hours fills도 `0`건이라 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다.
- Quote boundary: live Alpaca `get_stock_latest_quote(feed=iex)` 기준 freshest `MSFT`가 약 `73.32`분 stale였고 `QQQ`는 약 `73.52`분 stale, `PFE/RGTI/AVGO/WMT/JPM/NVDA/GOOGL/SPY`는 약 `73.50-73.59`분 stale였다. 추가 `get_stock_latest_quote(feed=boats)`는 subscription `403`으로 실패했지만, 이미 IEX freshness hard gate가 닫혀 submit 가능성에는 영향이 없었다.

## 후보 평가

- `PFE` sell/trim: live IEX quote `24.70/27.38`, spread 약 `10.2897%`, age 약 `73.56`분. prior weak-review trim precedent는 유지됐지만 freshness/spread 동시 fail.
- `RGTI` sell/trim: live IEX quote `17.57/23.11`, spread 약 `27.2152%`, age 약 `73.57`분. residual speculative sleeve trim rationale는 있으나 executable sell gate는 닫힘.
- `AVGO` sell/trim: live IEX quote `377.01/416.43`, spread 약 `9.9318%`, age 약 `73.58`분. sell-side 허용 policy는 유지됐지만 remaining qty `1주`와 quote quality 모두 불리했다.
- `QQQ` buy fallback: live IEX quote `722.87/723.00`, spread 약 `0.0180%`로 양호했지만 age 약 `73.52`분으로 stale이고 1주 ask `723.00 USD`가 after-hours per-order cap 약 `502.73 USD`를 넘었다.
- `MSFT` buy fallback: live IEX quote는 freshest였지만 ask가 비어 있었고 age 약 `73.32`분으로 stale였다.

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
| fresh_quote | fail_live_iex_quotes_stale_73_32_to_73_59_minutes |
| spread_within_after_hours_policy | fail_only_qqq_inside_spread_cap_but_stale_and_over_notional |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 fresh quote hard gate가 먼저 닫혀 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 direct Alpaca continuity 기준 open orders `0`, positions `34`, same-session after-hours submitted/fill `0/0` 확인으로 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-0611-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-0611-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-18-0611-after-hours-autopilot.json` PASS with expected `orders is empty` warning

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-18-0611-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0611-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0611-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-0611-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0611-after-hours-autopilot-post-trade.json`
