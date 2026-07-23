# 2026-07-23-1151-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `2026-07-22 EDT`
- Scheduler file label used: `2026-07-23-1151` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1151` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. same preflight clock row `2026-07-22T22:51:08.668399435-04:00` 기준 regular market은 closed였고, recent-activity rows에는 earlier `NOK` trim `client_order_id=ah-20260722-0931-sell-nok-01`이 `filled_avg_price=10.95 USD`로 유지돼 open-order lifecycle blocker가 없었다. 다만 submit boundary를 같은 `1151` preflight asset/quote/spread rows에 고정했을 때 `NOK/SO/WMT/MCD/QQQ/SPY/SMH/NEE/CVX/GS` shortlist quote가 모두 after-hours fresh-quote cap `5분`을 넘겼고, 여러 종목은 one-sided, spread cap, 또는 per-order-cap도 동시에 fail이어서 신규 `place_stock_order` 없이 reconcile-only로 종료했다. 이번 세션의 direct Alpaca MCP continuity readback은 DNS 수준 wrapper error로 실패했으므로 diagnostic continuity는 source-of-record preflight를 넘어서 확장하지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-1151-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-1151-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote rows는 scheduler-owned `1151` Alpaca core preflight를 사용했다.
- Same preflight 기준 account `ACTIVE`, cash `29,016.37 USD`, portfolio value `98,525.80 USD`, buying power `298,573.47 USD`, positions `31`, open orders `0`, watchlists `0`이었다.
- Recent activities에는 earlier `NOK` sell `1주`, `client_order_id=ah-20260722-0931-sell-nok-01`, `order_id=87eea18c-86c7-47b6-8565-4e5b56fef08b`, `filled_avg_price=10.95 USD`, `filled_at=2026-07-23T01:16:18.20135Z`가 유지됐다. same-session after-hours submitted/fills는 `1/1`로 기록했다.
- Post-run source-of-record focus는 `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=400`, `NOK qty_available=400`이다.
- Direct live continuity readback은 `2026-07-23 11:53:06 KST` around this session에 Alpaca MCP wrapper `ConnectError: nodename nor servname provided, or not known`로 실패했다. required after-hours rows는 이미 scheduler-owned `1151` preflight에 있으므로 이 오류는 diagnostic-only로 기록했고 first blocking gate로 승격하지 않았다.

## 후보 평가

- `NOK` sell/trim: source-of-record preflight quote `10.60/10.85`는 quote age 약 `351.16분`, spread 약 `2.3041%`로 freshness/spread hard gate fail이다.
- `SO` sell/trim: source-of-record preflight quote `88.45/99.75`, quote age 약 `411.10분`, spread 약 `11.3283%`로 fail이다.
- `WMT`: source-of-record quote `104.20/115.28`, quote age 약 `411.14분`, spread 약 `9.6114%`라 stale+wide spread fail이다.
- `MCD`: source-of-record quote는 ask가 비어 있는 one-sided stale quote라 fail이다.
- `QQQ`, `SPY`, `SMH`, `GS`: source-of-record quote는 stale이고, `QQQ/SPY/SMH/GS`는 1주 ask 기준 after-hours per-order cap도 함께 fail이다.
- `NEE`, `CVX`: source-of-record quote는 stale이고 spread cap fail을 동반했다.

## Submit And Reconcile

- Pre-submit gate summary는 생성되지 않았다. submit branch 진입 전에 source-of-record quote freshness gate가 fail했기 때문이다.
- Submitted order this cycle: 없음
- Immediate reconciliation: same `client_order_id=ah-20260722-0931-sell-nok-01` fill continuity를 scheduler-owned `1151` recent-activity rows로 재확인했다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-23-1151-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-1151-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-1151-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-1151-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1151-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1151-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-1151-after-hours-autopilot.json`
