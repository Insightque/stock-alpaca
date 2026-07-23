# 2026-07-24-0631-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Thursday, July 23, 2026 EDT`
- Scheduler file label used: `2026-07-24-0631` (`Asia/Seoul` next-day file label; actual market date anchor for this run is `Thursday, July 23, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned future-labeled KST artifact path 2026-07-24-0631 core preflight는 `first_blocking_gate=market_closed`까지만 기록하고 after-hours-required detail row를 남기지 않았다. 이번 run은 이를 expected nonblocking으로 처리한 뒤 direct Alpaca MCP continuity와 direct asset check로 missing account/order/position/watchlist/asset/quote/spread rows를 한 번 보강했다. 하지만 보강된 overnight quote 10개가 모두 `2026-07-23T08:00:00Z`에 멈춰 있어 `fresh_quote`가 first blocking gate로 남았고 신규 `place_stock_order` 없이 reconcile-only로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-24-0631-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-24-0631-after-hours-autopilot-research-mcp-preflight.json`
- Runtime continuity supplement: `wiki/evidence-store/sources/2026-07-24-0631-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-24-0631-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Scheduler-owned `wiki/evidence-store/sources/2026-07-24-0631-after-hours-autopilot-alpaca-core-preflight.json`는 `market_closed`만 기록하고 passing row detail을 남기지 않아 submit-boundary required rows를 직접 보강했다.
- Direct Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open|all)/get_account_activities(activity_types=[FILL])/get_watchlists/get_stock_latest_quote(feed=overnight)/get_asset`로 한 번씩만 호출했다. `2026-07-23T17:33:06.808049822-04:00` 기준 regular market closed, account `ACTIVE`, positions `31`, open orders `0`, watchlists `0`, same-session after-hours submitted orders/fills `0/0`였다.
- `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=399`, `NOK qty_available=399`를 재확인했다.
- Shortlist `SO/WMT/MCD/QQQ/SPY/SMH/NOK/NEE/CVX/GS`의 direct asset rows는 모두 active tradable US stock/ETF였다.

## 후보 평가

- `NOK` sell/trim: live overnight quote `10.53/10.64`, quote age 약 `813.09분`, spread 약 `1.0338%`로 stale + spread hard gate fail이다.
- `SO` sell/trim: live overnight quote `93.29/96.54`, quote age 약 `813.09분`, spread 약 `3.3665%`로 stale + spread hard gate fail이다.
- `QQQ`: quote age 약 `813.09분`, spread `0.7844%`, 1주 ask 기준 notional `0.7233%`로 stale + spread + per-order cap fail이다.
- `WMT/MCD/SPY/SMH/NEE/CVX/GS`도 모두 같은 stale timestamp를 공유했고 spread cap 또는 per-order cap fail을 함께 남겼다. `NOK` buy fallback은 stale/spread fail에 더해 `blocked_add_symbols` 유지로 executable path를 만들지 못했다.
- 이번 cycle의 first blocking gate는 `fresh_quote`였다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Pre-submit gate summary: 신규 `place_stock_order` 호출이 없어서 작성하지 않았다. submit branch 진입 전 `fresh_quote` 게이트가 fail했다.
- Reconciled same-session client_order_id: 없음. `get_orders(status=all, after=2026-07-23T20:00:00Z)`와 `get_account_activities(activity_types=[FILL], after=2026-07-23T20:00:00Z)` 기준 이번 after-hours 세션 주문/체결은 `0건`이었다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-24-0631-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-24-0631-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-24-0631-after-hours-autopilot.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-07-24-0631-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-24-0631-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-24-0631-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-24-0631-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-24-0631-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-24-0631-after-hours-autopilot.json` PASS with warning `orders is empty`
