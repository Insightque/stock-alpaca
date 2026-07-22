# 2026-07-22-1351-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date: `2026-07-21 EDT`
- Scheduler artifact date: `2026-07-22 KST`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1351` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live Alpaca continuity에서는 regular market closed, account `ACTIVE`, positions `31`, open orders `0`, same-session after-hours submitted orders `1`, fills `1`를 재확인했다. 기존 `client_order_id=ah-20260722-0911-sell-avgo-01` `AVGO` sell은 계속 `filled` 상태로 유지됐고 `AVGO position 없음`이 확인됐다. 이번 `1351` cycle에서는 신규 `place_stock_order` 호출을 하지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-22-1351-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-22-1351-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-1351-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle의 run id는 KST scheduler 파일명 `2026-07-22-1351-after-hours-autopilot`를 유지하지만, 실제 미국 장 판단과 continuity는 `2026-07-21 EDT` clock 기준으로 기록했다.

## Alpaca MCP 확인

- Regular market: closed. live `get_clock` 기준 `timestamp=2026-07-22T00:53:24.329280205-04:00`였다.
- Account: live `get_account_info` 기준 account `ACTIVE`, portfolio value `98213.11 USD`, cash `28995.09 USD`, buying power `297578.06 USD`였다.
- Orders / fills: live `get_orders(status=open)` 기준 open orders는 `0`건이었다. `get_orders(status=all, after=2026-07-21T20:00:00-04:00)` 기준 same-session after-hours order/fill은 `AVGO` sell `1건`뿐이며 `filled_avg_price=384.14 USD`, `filled_at=2026-07-22T01:48:58.933756Z`였다.
- Positions: live `get_all_positions` 기준 positions `31`건이었다. `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=402`였다.
- Watchlists: live `get_watchlists` 기준 `0`건이었다.

## 후보 평가

- `SO` sell/trim: overnight quote `88.59/95.80`, spread 약 `8.1386%`, quote age 약 `171.65분`으로 after-hours spread/freshness hard gate fail이다.
- `WMT` buy fallback: quote `110.03/110.44`, spread 약 `0.3726%`, quote age 약 `1.66분`으로 freshness는 pass지만 spread cap과 review backlog throttle 둘 다 fail이다.
- `MCD` buy fallback: quote `264.73/264.99`, spread 약 `0.0982%`, quote age 약 `1.98분`으로 quote/spread/notional은 pass지만 `review_backlog_pending_1d_count=17`이 `stop_new_buys_at_pending_1d=12`를 넘어 backlog throttle fail이다.
- `QQQ` / `SPY`: quote freshness와 spread는 pass였지만 `after_hours_policy.max_notional_pct_per_order=0.005` cap을 1주 기준으로 넘는다.
- `SMH`: quote는 fresh지만 spread 약 `0.3067%`와 1주 notional cap을 동시에 넘는다.
- `NOK`: quote `10.83/10.87`, spread 약 `0.3693%`, quote age 약 `1.44분`이지만 spread fail이며 `review-due-index.json`의 `blocked_add_symbols`와 review backlog throttle 때문에 add-block이다.
- `NEE` / `CVX` / `GS`: `NEE`와 `GS`는 spread gate를 통과하지 못했고 `CVX`는 spread와 freshness를 모두 통과하지 못했다.
- `AVGO`: overnight quote `382.10/382.72`, quote는 fresh했지만 same-session fill로 포지션이 이미 닫혀 reconcile-only다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Reconciled prior after-hours order: `AVGO` sell `1` share, `limit_price=384.13`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-0911-sell-avgo-01`
- Immediate readback / same-session fill ledger: same `client_order_id`는 `status=filled`, `filled_qty=1`, `filled_avg_price=384.14`였다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았고 기존 주문의 fill 상태만 continuity로 재확인했다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-22-1351-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-22-1351-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-22-1351-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-1351-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-22-1351-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-1351-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-1351-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-22-1351-after-hours-autopilot.json` -> PASS (`orders is empty` warning)
