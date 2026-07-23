# 2026-07-23-0931-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `2026-07-22 EDT`
- Scheduler file label used: `2026-07-23-0931` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0931` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. same preflight account/positions/open-orders/asset rows를 유지한 채, submit boundary는 `NOK` 한 종목에 한해 live overnight quote `10.95/10.96` (`2026-07-23T00:38:02.690193367Z`)로 freshness를 보강했다. strict universe/MCP/risk gate가 모두 PASS여서 `NOK` 1주 after-hours trim을 제출했고 immediate reconciliation 기준 `client_order_id=ah-20260722-0931-sell-nok-01`, `status=new`, `filled_qty=0`이다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-0931-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-0931-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-0931-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset rows는 scheduler-owned `0931` Alpaca core preflight를 사용했다.
- Live supplement는 `NOK` one-symbol overnight quote refresh와 same `client_order_id` reconciliation에만 사용했다. submit quote는 `bid/ask = 10.95/10.96`, spread `0.0913%`, quote timestamp `2026-07-23T00:38:02.690193367Z`였다.
- Immediate reconciliation 기준 order id `87eea18c-86c7-47b6-8565-4e5b56fef08b`, status `new`, filled_qty `0`, extended_hours `true`, expires_at `2026-07-24T00:00:00Z`였다.
- Post-submit continuity는 account `ACTIVE`, positions `31`, same-session after-hours submitted/fills `1/0`, `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=401`, `NOK qty_available=400`로 기록했다.

## 후보 평가

- `NOK` sell/trim: live overnight quote `10.95/10.96`, spread `0.0913%`, quote age submit 시점 약 `2분` 미만으로 after-hours freshness/spread cap을 통과했다. 기존 thesis page와 `2026-07-22` portfolio review는 add-block 유지와 underperformance를 기록하고 있어 sell-first floor-size trim 근거가 충분했다.
- `SO` sell/trim: live overnight quote `94.28/96.68`, spread 약 `2.5131%`로 spread hard gate fail이다.
- `SPY` / `QQQ` / `SMH`: live after-hours spread는 통과했지만 1주 ask 기준 `after_hours_policy.max_notional_pct_per_order=0.005` cap을 넘는다.
- `WMT` / `MCD`: fresh quote는 있었지만 spread가 각각 약 `0.3382%`, `0.4187%`로 cap 초과다.
- `NEE` / `CVX` / `GS`: stale 또는 spread/cap fail이라 buy fallback으로 승격되지 못했다.

## Submit And Reconcile

- Pre-submit gate summary: paper mode / `market_closed_expected_nonblocking_after_hours` / universe strict PASS / MCP strict PASS / risk PASS / `NOK` quote freshness PASS / spread PASS / whole-share day limit extended-hours order shape PASS를 확인한 뒤 submit했다.
- Submitted order this cycle: `NOK` sell `1` share, `limit_price=10.95`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-0931-sell-nok-01`
- Immediate reconciliation: Alpaca MCP `get_order_by_client_id` 기준 `status=new`, `filled_qty=0`, `filled_avg_price=null`.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-23-0931-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-0931-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-0931-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-0931-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-0931-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-0931-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-0931-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-0931-after-hours-autopilot.json` -> PASS
