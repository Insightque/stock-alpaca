# 2026-07-22-1751-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date: `2026-07-22 EDT`
- Scheduler artifact date: `2026-07-22 KST`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1751` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 이번 cycle의 submit boundary는 같은 `1751` preflight asset/quote/spread rows에 고정했다. same-session prior order `client_order_id=ah-20260722-0911-sell-avgo-01`은 그대로 `filled` 상태였고 `AVGO position 없음`, open orders `0`, positions `31`, same-session after-hours orders `1`, fills `1`, watchlists `0` continuity를 유지했다. 신규 `place_stock_order` 호출은 없었다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-22-1751-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-22-1751-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-1751-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote / spread rows는 scheduler-owned `1751` Alpaca core preflight를 사용했다.
- Live continuity는 Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-07-21T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-07-21T20:00:00-04:00)/get_watchlists/get_order_by_client_id(client_order_id=ah-20260722-0911-sell-avgo-01)`로 닫았다. regular market은 `2026-07-22T04:52:59.096465251-04:00`에 여전히 closed였고, account `ACTIVE`, positions `31`, open orders `0`, watchlists `0`였다.
- Same-session reconciliation 기준 `AVGO` sell은 `status=filled`, `filled_qty=1`, `filled_avg_price=384.14 USD`, `filled_at=2026-07-22T01:48:58.933756Z`였다.
- Workflow 계약상 submit eligibility는 refreshed runtime quote로 다시 열지 않고 `1751` preflight quote rows를 그대로 submit boundary로 유지했다.

## 후보 평가

- `SO` sell/trim: source-of-record quote `89.08/99.75`, quote age 약 `771.17`분, spread 약 `11.3012%`로 stale + spread hard gate fail이다.
- `WMT`: source-of-record quote는 bid `105.89`만 있고 ask가 비어 있어 two-sided quote gate fail이다. quote age 약 `771.14`분이고 `review_backlog_pending_1d_count=17`도 buy throttle을 유지한다.
- `MCD`: source-of-record quote `253.03/280.25`, quote age 약 `771.17`분, spread 약 `10.2085%`로 stale + spread fail이며 backlog throttle도 남아 있다.
- `QQQ` / `SPY`: spread 자체는 좁았지만 quote age가 각각 약 `719.52`분, `770.83`분으로 stale이고 1주 ask 기준 `after_hours_policy.max_notional_pct_per_order=0.005` cap도 넘는다.
- `SMH` / `NOK` / `NEE` / `CVX` / `GS`: 모두 stale 또는 spread 또는 review/per-order-cap gate에 막혀 executable after-hours path를 만들지 못했다.
- 이번 cycle의 first blocking gate는 `fresh_quote`였다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Reconciled prior after-hours order: `AVGO` sell `1` share, `limit_price=384.13`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-0911-sell-avgo-01`
- Retry discipline: alternate `client_order_id`는 사용하지 않았고 기존 주문의 fill 상태만 continuity로 재확인했다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-22-1751-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-22-1751-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-22-1751-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-1751-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-22-1751-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-1751-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-1751-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-22-1751-after-hours-autopilot.json`
