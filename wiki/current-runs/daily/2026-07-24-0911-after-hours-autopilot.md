# 2026-07-24-0911-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Thursday, July 23, 2026 EDT`
- Scheduler file label used: `2026-07-24-0911` (`Asia/Seoul` next-day file label; actual market date anchor for this run is `Thursday, July 23, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned future-labeled KST artifact path `2026-07-24-0911` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 `0911` preflight는 passing account/positions/open-orders/asset/quote/spread rows와 `orders_submitted=0`을 제공했고, live continuity `2026-07-23T20:14:03.814221805-04:00`에서도 regular market closed, positions `31`, watchlists `0`를 재확인했다. 다만 submit boundary는 계속 같은 `0911` source-of-record quote/spread rows에 고정했고 모든 executable 후보가 stale, one-sided, spread fail, 또는 per-order cap fail이라 신규 `place_stock_order` 없이 reconcile-only run으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-24-0911-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-24-0911-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-24-0911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote / spread rows는 scheduler-owned future-labeled KST artifact path `2026-07-24-0911` Alpaca core preflight를 사용했다.
- Live continuity는 Alpaca MCP `get_clock/get_all_positions/get_watchlists/get_stock_snapshot(feed=overnight)`로 닫았다. `2026-07-23T20:14:03.814221805-04:00` 기준 regular market closed, positions `31`, watchlists `0`였다.
- direct runtime `get_account_info`, `get_orders(status=open)`, `get_orders(status=all, after=2026-07-23T20:00:00Z)`는 HTTP 500이 났다. 이번 cycle에서는 submit path가 열리지 않았고 `0911` preflight가 이미 passing account/open-order/session-count evidence를 제공하고 있었으므로 이 오류들은 비차단 continuity gap으로만 기록했다.
- `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=399`를 재확인했다.

## 후보 평가

- `NOK` sell/trim: source-of-record quote `9.73/9.82`, quote age 약 `192.00분`, spread 약 `0.9207%`로 stale + spread hard gate fail이다.
- `SO` sell/trim: source-of-record quote `91.44/100.57`, quote age 약 `251.98분`, spread 약 `9.5099%`로 stale + spread hard gate fail이다.
- `QQQ`: spread 자체는 `0.0144%`로 좁았지만 quote age가 약 `196.33분`으로 stale이고 1주 ask 기준 `after_hours_policy.max_notional_pct_per_order=0.005` cap도 넘는다.
- `WMT`와 `MCD`는 one-sided quote, `SPY/SMH/NEE/CVX/GS`는 stale + spread 또는 cap fail, `NOK` buy fallback은 stale/spread fail에 더해 `blocked_add_symbols` 유지로 executable after-hours path를 만들지 못했다.
- 이번 cycle의 first blocking gate는 `fresh_quote`였다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Pre-submit gate summary: 신규 `place_stock_order` 호출이 없어서 작성하지 않았다. submit branch 진입 전 `fresh_quote` 게이트가 fail했다.
- Reconciled same-session client_order_id: 없음. `0911` source-of-record preflight `orders_submitted=0` 기준 이번 after-hours 세션에 새 주문 경로는 열리지 않았다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-24-0911-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-24-0911-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-24-0911-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-24-0911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-24-0911-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-24-0911-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-24-0911-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-24-0911-after-hours-autopilot.json`
