# 2026-07-23-1011-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `2026-07-22 EDT`
- Scheduler file label used: `2026-07-23-1011` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1011` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 다만 기존 `NOK` after-hours sell `client_order_id=ah-20260722-0931-sell-nok-01`이 이미 open 상태로 `30분` lifecycle limit을 넘겨 `check-risk-policy.py`가 `open_order_lifecycle`로 FAIL했다. submit boundary를 같은 `1011` preflight asset/quote/spread rows에 고정했을 때 shortlist quote도 모두 stale, one-sided, 또는 spread/per-order-cap fail이어서 quote/spread gate 역시 추가로 막혔다. live continuity는 해당 `NOK` order가 여전히 `status=new` open 상태임만 재확인했고, 신규 `place_stock_order` 없이 reconcile-only로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-1011-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-1011-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1011-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote rows는 scheduler-owned `1011` Alpaca core preflight를 사용했다.
- Live continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open|all)/get_order_by_client_id`로 닫았다. `2026-07-22T21:13:03.995881426-04:00` 기준 regular market은 계속 closed였다.
- Open order continuity 기준 `NOK` sell `1주`, `limit_price=10.95 USD`, `extended_hours=true`, `status=new`, `expires_at=2026-07-24T00:00:00Z`가 유지됐다.
- Post-run continuity는 account `ACTIVE`, positions `31`, open orders `1`, same-session after-hours submitted/fills `1/0`, `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=401`, `NOK qty_available=400`로 기록했다.

## 후보 평가

- `NOK` sell/trim: source-of-record preflight quote `10.60/10.85`는 quote age 약 `11.5분`, spread 약 `2.3041%`로 freshness/spread hard gate fail이다. 동시에 기존 `ah-20260722-0931-sell-nok-01` open order age가 약 `33분`으로 risk-policy lifecycle limit `30분`도 넘겼다.
- `SO` sell/trim: source-of-record preflight quote `88.45/99.75`, quote age 약 `71.4분`, spread 약 `11.3283%`로 fail이다.
- `WMT`, `NEE`, `CVX`, `GS`: source-of-record quote가 stale이면서 spread cap도 크게 초과했다.
- `MCD`: source-of-record quote가 stale이고 ask가 `0`인 one-sided row라 submit-grade quote로 쓸 수 없다.
- `QQQ`, `SPY`: source-of-record spread는 작지만 quote freshness가 이미 `5분`을 크게 넘었고, 1주 ask 기준 `after_hours_policy.max_notional_pct_per_order=0.005` cap도 넘는다.
- `SMH`: source-of-record quote가 stale이고 spread cap + per-order cap을 모두 fail했다.

## Submit And Reconcile

- Pre-submit gate summary는 생성되지 않았다. submit branch 진입 전에 risk validator가 `open_order_lifecycle`로 FAIL했기 때문이다.
- Submitted order this cycle: 없음
- Immediate reconciliation: same `client_order_id=ah-20260722-0931-sell-nok-01` readback 기준 `status=new`, `filled_qty=0`, `filled_avg_price=null` 유지.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-23-1011-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-1011-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-1011-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1011-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-1011-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1011-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1011-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-1011-after-hours-autopilot.json` -> FAIL (`NOK: open order age 33.0 minutes exceeds lifecycle limit 30.0`), warning `orders is empty`
