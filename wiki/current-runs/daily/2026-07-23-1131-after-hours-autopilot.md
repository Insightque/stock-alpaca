# 2026-07-23-1131-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `2026-07-22 EDT`
- Scheduler file label used: `2026-07-23-1131` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1131` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live continuity 기준 regular market은 `2026-07-22T22:33:01.686285742-04:00`에도 closed였고 earlier `NOK` trim `client_order_id=ah-20260722-0931-sell-nok-01`은 이미 `filled_avg_price=10.95 USD`로 닫혀 open-order lifecycle blocker가 없었다. 다만 submit boundary를 같은 `1131` preflight asset/quote/spread rows에 고정했을 때 `NOK/SO/WMT/MCD/QQQ/SPY/SMH/NEE/CVX/GS` shortlist quote가 모두 after-hours fresh-quote cap `5분`을 넘겼고, 여러 종목은 one-sided, spread cap, 또는 per-order-cap도 동시에 fail이어서 신규 `place_stock_order` 없이 reconcile-only로 종료했다. live overnight continuity에서는 `WMT 109.39/109.56`가 spread/notional 기준을 진단상 통과했지만, 이번 workflow는 scheduler-owned `1131` quote/spread row를 submit boundary로 유지해야 하므로 diagnostic-only로 남겼다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-1131-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-1131-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1131-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote rows는 scheduler-owned `1131` Alpaca core preflight를 사용했다.
- Live continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open|all)/get_account_activities(activity_types=[FILL])/get_watchlists/get_stock_snapshot(feed=overnight)`로 닫았다. `2026-07-22T22:33:01.686285742-04:00` 기준 regular market은 계속 closed였다.
- Earlier `NOK` sell `1주`, `limit_price=10.95 USD`, `extended_hours=true`는 same `client_order_id=ah-20260722-0931-sell-nok-01` readback 기준 `filled`, `filled_qty=1`, `filled_avg_price=10.95 USD`, `filled_at=2026-07-23T01:16:18.20135Z`로 유지됐다.
- Post-run continuity는 account `ACTIVE`, positions `31`, open orders `0`, same-session after-hours submitted/fills `1/1`, `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=400`, `NOK qty_available=400`으로 기록했다.

## 후보 평가

- `NOK` sell/trim: source-of-record preflight quote `10.60/10.85`는 quote age 약 `331.48분`, spread 약 `2.3041%`로 freshness/spread hard gate fail이다. live overnight quote `10.77/10.81`는 freshness는 보강됐지만 spread 약 `0.3700%`로 여전히 cap `0.25%`를 넘는다.
- `SO` sell/trim: source-of-record preflight quote `88.45/99.75`, quote age 약 `391.42분`, spread 약 `11.3283%`로 fail이다. live continuity도 `94.63/96.72`로 spread 약 `2.1610%`라 여전히 fail이다.
- `WMT`: source-of-record quote `104.20/115.28`는 stale+wide spread라 fail이다. live continuity `109.39/109.56`는 spread 약 `0.1552%`, 1주 ask notional 약 `0.1111%`로 진단상 통과했지만, submit boundary를 scheduler-owned `1131` quote/spread rows에 고정했기 때문에 이번 cycle에서는 diagnostic-only로 유지했다.
- `MCD`, `NEE`, `CVX`, `GS`: source-of-record quote는 stale이고 spread cap 또는 one-sided 문제를 동반했다. live continuity도 각각 spread cap 또는 spread+cap fail로 남았다.
- `QQQ`, `SPY`, `SMH`: live continuity에서 freshness와 spread는 개선됐지만 1주 ask 기준이 `after_hours_policy.max_notional_pct_per_order=0.005` cap을 계속 초과했다.

## Submit And Reconcile

- Pre-submit gate summary는 생성되지 않았다. submit branch 진입 전에 source-of-record quote freshness gate가 fail했기 때문이다.
- Submitted order this cycle: 없음
- Immediate reconciliation: same `client_order_id=ah-20260722-0931-sell-nok-01` readback 기준 `status=filled`, `filled_qty=1`, `filled_avg_price=10.95` 상태를 재확인했다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-23-1131-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-1131-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-1131-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1131-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-1131-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1131-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1131-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-1131-after-hours-autopilot.json`
