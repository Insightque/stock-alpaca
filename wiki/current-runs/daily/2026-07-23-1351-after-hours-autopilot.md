# 2026-07-23-1351-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Wednesday, July 22, 2026 EDT`
- Scheduler file label used: `2026-07-23-1351` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1351` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca continuity는 정상 응답했고 same-session after-hours submitted/fills `2/2`, open orders `0`, live overnight `NOK 11.07/11.09`, `WMT 109.41/109.60`, `MCD 263.85/264.48`를 재확인했다. 다만 separate after-hours session budget이 이미 `0/2 remaining` 상태였고 `SO 94.64/95.97`는 stale + spread cap fail이었다. `NOK` sell trim과 `WMT`/`MCD` 1주 buy fallback은 quote/spread 기준으로 executable이었지만 session budget이 닫혀 있어 신규 `place_stock_order` 없이 reconcile-only로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-1351-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-1351-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1351-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote rows는 scheduler-owned `1351` Alpaca core preflight를 사용했다.
- Direct live continuity 기준 `2026-07-23T04:52:48.997500058-04:00` regular market closed, account `ACTIVE`, cash `29,027.15 USD`, portfolio value `98,700.87 USD`, buying power `298,816.43 USD`, positions `31`, open orders `0`, watchlists `0`였다.
- Recent activities에는 `NOK` after-hours sell `2건`이 유지됐다. `ah-20260722-0931-sell-nok-01`은 `filled_avg_price=10.95 USD`, `filled_at=2026-07-23T01:16:18.201349781Z`, `ah-20260722-1211-sell-nok-01`은 `filled_avg_price=10.78 USD`, `filled_at=2026-07-23T03:18:44.891868059Z`다. same-session after-hours submitted/fills는 `2/2`로 기록했다.
- Post-run focus는 `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=399`, `NOK qty_available=399`이다.

## 후보 평가

- `NOK` sell/trim: live overnight quote `11.07/11.09`, spread `0.1803%`, freshness `5분 이하`로 executable이었지만 separate after-hours session budget 소진으로 blocked 처리됐다.
- `SO` sell/trim: live overnight quote `94.64/95.97`, spread `1.3858%`, quote age 약 `21.09분`으로 stale + spread cap fail이다.
- `WMT`: live overnight quote `109.41/109.60`, spread `0.1734%`, freshness `5분 이하`, per-order notional cap PASS로 executable buy fallback이다.
- `MCD`: live overnight quote `263.85/264.48`, spread `0.2382%`, freshness `5분 이하`, per-order notional cap PASS로 executable buy fallback이다.
- `QQQ`, `SPY`: freshness/spread는 통과했지만 1주 ask 기준 after-hours per-order cap fail이다.
- `SMH`: freshness는 통과했지만 spread cap과 per-order cap을 함께 fail했다.
- `NEE`: stale + spread cap fail이다.
- `CVX`: freshness는 통과했지만 spread cap fail이다.
- `GS`: stale + spread cap + per-order cap fail이다.

## Submit And Reconcile

- Pre-submit gate summary는 생성되지 않았다. submit branch 진입 전에 `separate_after_hours_order_budget` 게이트가 fail했기 때문이다.
- Submitted order this cycle: 없음
- Immediate reconciliation: same-session `ah-` fill stack `2건`과 open orders `0`를 live Alpaca continuity와 scheduler-owned `1351` recent-activity rows로 함께 재확인했다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-23-1351-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-1351-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-1351-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1351-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-1351-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1351-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1351-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-1351-after-hours-autopilot.json`
