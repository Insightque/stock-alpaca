# 2026-06-18-0831-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0831` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca continuity는 clock/account/positions/open-orders/fills/watchlists parity를 재확인했지만 submit-boundary quote timestamp는 여전히 `2026-06-17 20:00~20:20 ET`에 머물렀다. separate after-hours order budget은 `0/2`로 열려 있었지만 freshest continuity quote `MS`도 약 `192.62`분 stale이었다. `QQQ`는 spread는 통과했지만 stale+per-order notional cap에, `MS/NVDA/SPY/TSLA/GOOGL/WMT/JPM/PFE/RGTI/AVGO`는 stale+spread gate에 막혀 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-18-0831-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-18-0831-after-hours-autopilot-research-mcp-preflight.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-18-0831-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-0831-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle은 같은 preflight의 passing account/positions/open-orders/account-activities/asset/quote/spread rows를 submit-boundary evidence로 유지했고, direct continuity는 그 상태를 뒤집지 못한 채 stale quote carry-forward만 재확인했다.

## Alpaca MCP 확인

- Regular market: closed (direct `get_clock.timestamp=2026-06-17T19:32:37.734467787-04:00`)
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `100836.98 USD`, cash `28003.45 USD`, buying power `300267.85 USD`
- Positions / open orders / watchlists: direct `get_all_positions` 기준 positions `34`건, direct `get_orders(status=open)` 기준 open orders `0`건, direct `get_watchlists` 기준 watchlists `0`건이었다.
- Same-session after-hours orders / fills: direct `get_account_activities(activity_types=[FILL], after=2026-06-17T20:00:00Z)`와 `get_orders(status=all, after=2026-06-17T20:00:00Z)` continuity 기준 same-session after-hours submit `0`, fills `0`이었다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`다.
- Quote boundary: direct `get_stock_latest_quote(feed=iex)`도 preflight와 같은 timestamp를 반환했다. freshest quote는 `MS` `2026-06-17T20:20:00.57860736Z`였고 evaluated stack은 약 `192.62`분에서 `212.62`분 stale이었다.

## 후보 평가

- `PFE` sell/trim: direct quote `24.70/27.38`, spread 약 `10.8502%`, age 약 `212.60`분. repeated weak-review trim rationale는 유지됐지만 freshness/spread 동시 fail.
- `RGTI` sell/trim: direct quote `17.57/23.11`, spread 약 `31.5310%`, age 약 `212.61`분. residual speculative sleeve trim rationale는 유지됐지만 freshness/spread 동시 fail.
- `AVGO` sell/trim: direct quote `377.01/416.43`, spread 약 `10.4560%`, age 약 `212.62`분. sell side 허용 policy는 유지됐지만 executable sell gate는 닫혀 있었다.
- `QQQ` buy fallback: direct quote `722.87/723.00`, spread 약 `0.0180%`로 양호했지만 age 약 `212.56`분으로 stale이고 1주 ask `723.00 USD`가 after-hours per-order cap 약 `504.18 USD`를 넘었다.
- `MS` buy fallback: direct quote `220.00/231.46`, spread 약 `5.2091%`, age 약 `192.62`분. freshest research-shortlist quote였지만 spread/freshness가 모두 fail했다.
- Review backlog: `wiki/trade-ledger/reviews/review-due-index.json` 기준 `pending_1d_count=17`, `pending_5d_count=23`, `pending_20d_count=15`, `blocked_add_symbols=['NOK']`였다. 이번 cycle은 backlog throttle보다 fresh-quote hard gate가 직접 차단 요인이었다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_and_runtime_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with expected `orders is empty` warning |
| fresh_quote | fail_scheduler_owned_submit_boundary_quotes_stale_192.62_to_212.62_minutes |
| spread_within_after_hours_policy | fail_no_candidate_met_fresh_and_spread_and_notional_together |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 fresh quote hard gate가 먼저 닫혀 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 direct continuity 기준 open orders `0`, same-session after-hours submitted `0`, same-session fills `0`, positions `34` 확인으로 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-0831-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-0831-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-18-0831-after-hours-autopilot.json` PASS with expected `orders is empty` warning

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-18-0831-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0831-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0831-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-0831-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-18-0831-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0831-after-hours-autopilot-post-trade.json`
