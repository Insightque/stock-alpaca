# 2026-07-23-1611-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Wednesday, July 22, 2026 EDT`
- Scheduler file label used: `2026-07-23-1611` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1611` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 preflight의 passing account/order/position/quote/spread rows와 recent fill rows를 사용한 결과 regular market closed, account `ACTIVE`, positions `31`, open orders `0`, watchlists `0`, same-session after-hours submitted/fills `2/2`를 재확인했다. 이번 cycle의 first blocking gate는 `separate_after_hours_order_budget`였고 신규 `place_stock_order` 없이 reconcile-only로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-1611-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-1611-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1611-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.
- `1611` core preflight의 passing account/positions/open-orders/recent-activity/asset/quote rows만 사용했다.

## Alpaca MCP 확인

- Source-of-record는 scheduler-owned `1611` Alpaca core preflight다. `get_clock`, `get_account_info`, `get_all_positions`, `get_orders_open`, `get_account_activities`, `get_watchlists`, `get_asset`, `get_stock_latest_quote` rows가 기록돼 있다.
- Source-of-record 기준 `2026-07-23T03:11:07.727031565-04:00` regular market closed, account `ACTIVE`, cash `29027.15 USD`, portfolio value `98444.95 USD`, buying power `29027.15 USD`, positions `31`, open orders `0`, watchlists `0`였다.
- Recent activities 기준 same-session after-hours fill은 `NOK` sell `2건`이다. `ah-20260722-0931-sell-nok-01`은 `filled_avg_price=10.95 USD`, `filled_at=2026-07-23T01:16:18.20135Z`, `ah-20260722-1211-sell-nok-01`은 `filled_avg_price=10.78 USD`, `filled_at=2026-07-23T03:18:44.891868Z`다. same-session after-hours submitted/fills는 `2/2`로 기록했다.
- Post-run focus는 `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=399`, `NOK qty_available=399`이다.

## 후보 평가

- `NOK` sell/trim: preflight IEX quote `10.60/10.85`, quote age `611.51분`, spread `2.3310%`다. after-hours quote/spread gate도 fail이고, 별도로 separate after-hours session budget이 이미 `0/2 remaining` 상태다.
- `SO` sell/trim: preflight IEX quote `88.45/99.75`, quote age `671.46분`, spread `12.0085%`로 stale + spread cap fail이다.
- `WMT`: preflight IEX quote `104.20/115.28`, quote age `671.50분`, spread `10.0966%`로 stale + spread cap fail이다.
- `MCD`: preflight IEX quote `251.75/0.00`, quote age `671.44분`, one-sided quote라 submit 불가다.
- `QQQ`: preflight IEX quote `706.51/706.68`, quote age `670.49분`, spread `0.0241%`이지만 stale이며 1주 ask 기준 after-hours per-order cap `0.5%`도 초과한다.
- `SPY`: preflight IEX quote `748.37/748.99`, quote age `640.37분`, spread `0.0828%`이지만 stale이며 1주 ask 기준 per-order cap도 초과한다.
- `SMH`: preflight IEX quote `571.72/607.38`, quote age `671.50분`, spread `6.0487%`와 per-order cap을 함께 fail한다.
- `NEE`, `CVX`, `GS`: 모두 stale이며 spread cap fail이다. `GS`는 per-order cap도 함께 fail이다.

## Submit And Reconcile

- Pre-submit gate summary는 생성되지 않았다. submit branch 진입 전에 `separate_after_hours_order_budget` 게이트가 fail했기 때문이다.
- Submitted order this cycle: 없음
- Immediate reconciliation: source-of-record recent activity 기준 same-session `ah-` fill stack `2건`과 open orders `0`를 재확인했다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Prompt source: `wiki/evidence-store/sources/2026-07-23-1611-after-hours-autopilot-prompt.txt`
- Report: `wiki/current-runs/daily/2026-07-23-1611-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-1611-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-1611-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1611-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-1611-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1611-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1611-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-1611-after-hours-autopilot.json`
