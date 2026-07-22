# 2026-07-22-1251-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date: `2026-07-21 EDT`
- Scheduler artifact date: `2026-07-22 KST`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1251` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live Alpaca continuity에서는 regular market closed, account `ACTIVE`, positions `31`, open orders `0`, same-session after-hours submitted orders `1`, fills `1`를 재확인했다. 기존 `client_order_id=ah-20260722-0911-sell-avgo-01` `AVGO` sell은 계속 `filled` 상태로 유지됐고 `AVGO position 없음`이 확인됐다. 이번 `1251` cycle에서는 신규 `place_stock_order` 호출을 하지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-22-1251-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-22-1251-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-1251-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle의 run id는 KST scheduler 파일명 `2026-07-22-1251-*`를 유지하지만, 실제 미국 장 판단과 continuity는 `2026-07-21 EDT` clock 기준으로 기록했다.

## Alpaca MCP 확인

- Regular market: closed. live `get_clock` 기준 `timestamp=2026-07-21T23:54:09.653716103-04:00`였다.
- Account: live `get_account_info` 기준 account `ACTIVE`, portfolio value `98246.85 USD`, cash `28995.09 USD`, buying power `297593.74 USD`였다.
- Orders / fills: live `get_orders(status=open)` 기준 open orders는 `0`건이었다. `get_orders(status=all, after=2026-07-21T20:00:00Z)`와 `get_account_activities(activity_types=[FILL], after=2026-07-21T20:00:00Z)` 기준 same-session after-hours order/fill은 `AVGO` sell `1건`뿐이며 `filled_avg_price=384.14 USD`, `filled_at=2026-07-22T01:48:58.933756Z`였다.
- Positions: live `get_all_positions` 기준 positions `31`건이었다. `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=402`였다.
- Watchlists: live `get_watchlists` 기준 `0`건이었다.

## 후보 평가

- `SO` sell/trim: overnight quote `88.59/95.8`, spread 약 `8.1386%`, quote age 약 `111.0분`으로 after-hours spread/freshness hard gate fail이다.
- `WMT` buy fallback: quote `110.22/110.34`, spread 약 `0.1089%`, quote age 약 `1.65분`으로 quote/spread와 per-order cap은 pass지만 `review_backlog_pending_1d_count=17` backlog throttle 때문에 submit-mode buy를 열 수 없었다.
- `MCD` buy fallback: quote `264.08/264.99`, spread 약 `0.3446%`, quote age 약 `3.02분`으로 backlog throttle 이전에 spread cap fail이다.
- `QQQ` / `SPY`: quote freshness와 spread는 pass였지만 `after_hours_policy.max_notional_pct_per_order=0.005` cap을 1주 기준으로 넘는다.
- `SMH`: quote는 fresh지만 spread 약 `0.3322%`와 1주 notional cap을 동시에 넘는다.
- `NOK`: quote `10.91/10.96`, spread 약 `0.4583%`, quote age 약 `0.59분`으로 spread fail이고 `review-due-index.json`의 `blocked_add_symbols`에 남아 있어 add-block이다.
- `NEE` / `CVX` / `GS`: `NEE`와 `GS`는 spread cap fail이고 `CVX`는 spread는 pass했지만 quote age 약 `8.86분`으로 freshness fail이다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Reconciled prior after-hours order: `AVGO` sell `1` share, `limit_price=384.13`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-0911-sell-avgo-01`
- Immediate readback / same-session fill ledger: same `client_order_id`는 `status=filled`, `filled_qty=1`, `filled_avg_price=384.14`였다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았고 기존 주문의 fill 상태만 continuity로 재확인했다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-22-1251-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-22-1251-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-22-1251-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-1251-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-22-1251-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-1251-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-1251-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-22-1251-after-hours-autopilot.json` -> PASS (`orders is empty` warning)
