# 2026-07-23-1531-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Wednesday, July 22, 2026 EDT`
- Scheduler file label used: `2026-07-23-1531` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1531` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 다만 `1531` core preflight에는 passing account/order/position/quote row detail이 비어 있어 registered Alpaca read-only continuity로 missing rows를 보강했다. live continuity 기준 regular market closed, account `ACTIVE`, positions `31`, open orders `0`, watchlists `0`, same-session after-hours submitted/fills `2/2`를 재확인했다. live overnight `NOK 10.99/11.01`, `WMT 109.42/109.59`는 executable이었지만 separate after-hours session budget이 이미 `0/2 remaining` 상태였다. `MCD`/`CVX`/`GS`는 spread gate, `SO`는 stale+spread gate, `NEE`는 spread gate, `QQQ`/`SPY`/`SMH`/`GS`는 per-order cap에 막혀 신규 `place_stock_order` 없이 reconcile-only로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-1531-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-1531-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1531-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.
- 다만 `1531` core preflight는 passing row detail이 비어 있어 after-hours-required missing rows는 registered Alpaca read-only continuity로 보강했다.

## Alpaca MCP 확인

- Source-of-record priority는 scheduler-owned `1531` Alpaca core preflight였고, missing detail rows는 registered Alpaca `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_watchlists`, `get_account_activities`, `get_stock_latest_quote(feed=overnight)`로 채웠다.
- Direct live continuity 기준 `2026-07-23T02:33:17.917750314-04:00` regular market closed, account `ACTIVE`, cash `29,027.15 USD`, portfolio value `98,650.13 USD`, buying power `298,774.92 USD`, positions `31`, open orders `0`, watchlists `0`였다.
- Recent activities와 orders readback에는 `NOK` after-hours sell `2건`이 유지됐다. `ah-20260722-0931-sell-nok-01`은 `filled_avg_price=10.95 USD`, `filled_at=2026-07-23T01:16:18.20135Z`, `ah-20260722-1211-sell-nok-01`은 `filled_avg_price=10.78 USD`, `filled_at=2026-07-23T03:18:44.891868059Z`다. same-session after-hours submitted/fills는 `2/2`로 기록했다.
- Post-run focus는 `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=399`, `NOK qty_available=399`이다.

## 후보 평가

- `NOK` sell/trim: live overnight quote `10.99/11.01`, spread `0.1817%`, quote age 약 `0.03분`으로 sell execution quality는 통과했다. 다만 separate after-hours session budget이 이미 소진돼 submit 불가였다.
- `SO` sell/trim: live overnight quote `94.67/95.91`, spread `1.2939%`, quote age 약 `33.72분`으로 stale + spread cap fail이다.
- `WMT`: live overnight quote `109.42/109.59`, spread `0.1551%`, quote age 약 `0.36분`으로 live buy fallback 기준 executable이었다. 다만 separate after-hours session budget이 이미 소진돼 submit 불가였다.
- `MCD`: live overnight quote `263.30/264.30`, spread `0.3784%`, quote age 약 `1.37분`으로 spread cap fail이다.
- `QQQ`, `SPY`, `SMH`: freshness/spread는 submit-grade였지만 1주 ask 기준 after-hours per-order cap fail이다.
- `NEE`: quote age 약 `3.38분`으로 freshness는 통과했지만 spread `1.8176%`가 fail이다.
- `CVX`: freshness는 충분하지만 spread `0.2836%`가 cap 초과다.
- `GS`: freshness는 충분하지만 spread `1.2380%`와 per-order cap을 동시에 fail했다.

## Submit And Reconcile

- Pre-submit gate summary는 생성되지 않았다. submit branch 진입 전에 `separate_after_hours_order_budget` 게이트가 fail했기 때문이다.
- Submitted order this cycle: 없음
- Immediate reconciliation: same-session `ah-` fill stack `2건`과 open orders `0`를 live Alpaca continuity와 scheduler-owned `1531` preflight 보강 evidence로 함께 재확인했다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Prompt source: `wiki/evidence-store/sources/2026-07-23-1531-after-hours-autopilot-prompt.txt`
- Report: `wiki/current-runs/daily/2026-07-23-1531-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-1531-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-1531-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1531-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-1531-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1531-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1531-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-1531-after-hours-autopilot.json`
