# 2026-07-23-0951-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `2026-07-22 EDT`
- Scheduler file label used: `2026-07-23-0951` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0951` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live continuity 기준 기존 `NOK` after-hours sell `client_order_id=ah-20260722-0931-sell-nok-01`이 여전히 `status=new` open 상태라 same symbol/side duplicate-open-order gate가 유지됐고, 나머지 shortlist는 spread 또는 after-hours per-order cap을 통과하지 못해 신규 `place_stock_order` 없이 reconcile-only로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-0951-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-0951-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-0951-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset rows는 scheduler-owned `0951` Alpaca core preflight를 사용했다.
- Live continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open|all)/get_stock_latest_quote`로 닫았다. `2026-07-22T20:53:03.712291455-04:00` 기준 regular market은 계속 closed였다.
- Open order continuity 기준 `NOK` sell `1주`, `limit_price=10.95 USD`, `extended_hours=true`, `status=new`, `expires_at=2026-07-24T00:00:00Z`가 유지됐다.
- Post-run continuity는 account `ACTIVE`, positions `31`, open orders `1`, same-session after-hours submitted/fills `1/0`, `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=401`, `NOK qty_available=400`로 기록했다.

## 후보 평가

- `NOK` sell/trim: live overnight quote `10.89/10.91`, spread `0.1833%`, quote freshness PASS였다. 다만 기존 open order `ah-20260722-0931-sell-nok-01`이 아직 살아 있어 same symbol/side duplicate-open-order gate로 신규 submit을 막았다.
- `SO` sell/trim: live overnight quote `94.28/96.68`, spread 약 `2.5131%`, quote age 약 `51.7분`으로 spread/freshness hard gate fail이다.
- `WMT`: live quote `109.23/109.51`, spread 약 `0.2557%`로 cap `0.25%`를 소폭 초과했다.
- `MCD`, `NEE`, `CVX`, `GS`: spread cap fail이고, `GS`는 stale + per-order cap도 함께 fail이다.
- `SPY`, `QQQ`, `SMH`: quote freshness는 통과했지만 1주 ask 기준 `after_hours_policy.max_notional_pct_per_order=0.005` cap을 넘는다.

## Submit And Reconcile

- Pre-submit gate summary는 생성되지 않았다. submit branch 진입 전에 `existing_open_order_same_symbol_side`가 first blocking gate가 됐기 때문이다.
- Submitted order this cycle: 없음
- Immediate reconciliation: same `client_order_id=ah-20260722-0931-sell-nok-01` readback 기준 `status=new`, `filled_qty=0`, `filled_avg_price=null` 유지.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-23-0951-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-0951-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-0951-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-0951-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-0951-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-0951-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-0951-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-0951-after-hours-autopilot.json` -> PASS with warning `orders is empty`
