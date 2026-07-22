# 2026-07-22-1451-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date: `2026-07-21 EDT`
- Scheduler artifact date: `2026-07-22 KST`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1451` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live Alpaca MCP continuity에서는 regular market closed, account `ACTIVE`, positions `31`, open orders `0`, watchlists `0`, same-session after-hours submitted orders `1`, fills `1`를 재확인했다. 기존 `client_order_id=ah-20260722-0911-sell-avgo-01` `AVGO` sell은 계속 `filled` 상태로 유지됐고 `AVGO position 없음`이 확인됐다. 이번 `1451` cycle에서는 신규 `place_stock_order` 호출을 하지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-22-1451-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-22-1451-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-1451-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle의 run id는 KST scheduler 파일명 `2026-07-22-1451-after-hours-autopilot`를 유지하지만, 실제 미국 장 판단과 continuity는 `2026-07-21 EDT` clock 기준으로 기록했다.

## Alpaca MCP 확인

- Regular market: closed. live `get_clock` 기준 `timestamp=2026-07-22T01:53:05.371042019-04:00`였다.
- Account: live `get_account_info` 기준 account `ACTIVE`, portfolio value `97,994.30 USD`, cash `28,995.09 USD`, buying power `297,156.74 USD`였다.
- Orders / fills: live `get_orders(status=open)` 기준 open orders는 `0`건이었다. `get_orders(status=all, after=2026-07-21T20:00:00-04:00)`와 `get_account_activities(activity_types=[FILL], after=2026-07-21T20:00:00-04:00)` 기준 same-session after-hours order/fill은 `AVGO` sell `1건`뿐이며 `filled_avg_price=384.14 USD`, `filled_at=2026-07-22T01:48:58.933755903Z`였다.
- Positions: live `get_all_positions` 기준 positions `31`건이었다. `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=402`였다.
- Watchlists: live `get_watchlists` 기준 `0`건이었다.

## 후보 평가

- Submit boundary는 scheduler-owned `1451` Alpaca core preflight의 asset/quote/spread rows로 고정했다. 이 source-of-record quote rows는 모두 `iex` close snapshot 기반이라 after-hours submit 시점 기준 freshness gate를 통과하지 못했다.
- `SO` sell/trim: source-of-record quote `89.08/99.75`, spread 약 `11.9780%`, quote age 약 `591.58분`으로 stale + spread hard gate fail이다.
- `WMT` buy fallback: source-of-record quote는 bid `105.89`만 있고 ask가 비어 있어 two-sided quote gate fail이다. quote age 약 `591.55분`이고 `review_backlog_pending_1d_count=17`도 buy throttle을 유지한다.
- `MCD` buy fallback: source-of-record quote `253.03/280.25`, spread 약 `10.7576%`, quote age 약 `591.58분`으로 stale + spread fail이며 backlog throttle도 남아 있다.
- `QQQ` / `SPY`: spread 자체는 좁았지만 quote age가 각각 약 `539.93분`, `591.24분`으로 stale이고 1주 ask 기준 `after_hours_policy.max_notional_pct_per_order=0.005` cap도 넘는다.
- `SMH`: quote age 약 `591.58분`, spread 약 `6.2162%`, 1주 ask도 per-order cap을 넘어 stale + spread + cap fail이다.
- `NOK`: quote `10.78/10.92`, spread 약 `1.2987%`, quote age 약 `531.60분`으로 stale + spread fail이며 `review-due-index.json`의 `blocked_add_symbols`와 review backlog throttle 때문에 add-block이다.
- `NEE` / `CVX` / `GS`: 세 종목 모두 quote age가 약 `591분`대로 stale이며 spread가 각각 약 `11.9105%`, `10.9798%`, `9.1835%`로 after-hours spread gate를 통과하지 못했다. `GS`는 1주 ask도 per-order cap을 넘는다.
- `AVGO`: source-of-record quote도 stale/spread fail이지만 무엇보다 same-session fill로 포지션이 이미 닫혀 reconcile-only다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Reconciled prior after-hours order: `AVGO` sell `1` share, `limit_price=384.13`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-0911-sell-avgo-01`
- Immediate readback / same-session fill ledger: same `client_order_id`는 `status=filled`, `filled_qty=1`, `filled_avg_price=384.14`였다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았고 기존 주문의 fill 상태만 continuity로 재확인했다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-22-1451-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-22-1451-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-22-1451-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-1451-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-22-1451-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-1451-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-1451-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-22-1451-after-hours-autopilot.json` -> PASS (`orders is empty` warning)
