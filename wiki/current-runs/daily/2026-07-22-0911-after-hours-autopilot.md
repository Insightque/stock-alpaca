# 2026-07-22-0911-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date: `2026-07-21 EDT`
- Scheduler artifact date: `2026-07-22 KST`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0911` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live Alpaca continuity에서 same-session after-hours orders/fills `0/0`, open orders `0`를 다시 확인한 뒤 sell-first 경로를 재평가했다. `AVGO` overnight quote가 `384.13/384.52`, spread `0.1014%`, quote age 약 `0.01`분으로 회복되어 strict universe/MCP/risk gate를 모두 통과했고, `client_order_id=ah-20260722-0911-sell-avgo-01`로 1주 after-hours sell을 1회 제출했다. immediate reconciliation 기준 주문은 `status=new` open order이며 fill은 아직 없다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-22-0911-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-22-0911-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-0911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle의 run id는 KST scheduler 파일명 `2026-07-22-0911-*`를 유지하지만, 실제 미국 장 판단과 continuity는 `2026-07-21 EDT` clock 기준으로 기록했다.

## Alpaca MCP 확인

- Regular market: closed. live `get_clock` 기준 `timestamp=2026-07-21T20:19:26.690133916-04:00`였다.
- Account: live `get_account_info` 기준 account `ACTIVE`, portfolio value `98632.89 USD`, cash `28610.95 USD`, buying power `297988.57 USD`였다.
- Positions / orders: live `get_all_positions` 기준 positions `32`건이었다. submit 전 `get_orders(status=open)` 기준 open orders `0`건이었고, submit 후 same readback은 `AVGO` open order `1`건을 반환했다. `get_orders(status=all, after=2026-07-21T20:00:00Z)` 기준 same-session after-hours submitted orders는 `1`건, `get_account_activities(activity_types=[FILL], after=2026-07-21T20:00:00Z)` 기준 same-session fills는 `0`건이다.
- Quote boundary: live `get_stock_latest_quote(feed=overnight)` 기준 `AVGO`는 `384.13/384.52`, spread `0.1014%`, quote age 약 `0.01`분이었다. `SO`는 `84.54/98.25`, spread 약 `13.95%`로 여전히 fail이다. `QQQ/SPY`는 spread와 freshness는 pass였지만 sell-first 경로가 이미 열렸고 benchmark buy fallback은 필요하지 않았다.

## 후보 평가

- `AVGO` sell/exit: residual `1주` 보유이며 `AVGO` 위키와 `2026-06-19` portfolio review는 post-earnings staged de-risking과 recovery confirmation 부족을 계속 기록하고 있다. live overnight quote `384.13/384.52`, spread `0.1014%`, quote age 약 `0.01`분, open orders `0`, same-session fills `0`, after-hours session budget `0/2`, allowed sell side 조건을 모두 통과해 제출 후보로 승격했다.
- `SO` sell/trim: live overnight quote `84.54/98.25`, spread 약 `13.95%`라 hard gate fail이다. note에 남아 있는 `trim metric gap`도 계속 해소되지 않았다.
- `WMT` buy fallback: quote `109.82/110.04`, spread `0.1999%`로 shape 자체는 양호했지만 `review_backlog_pending_1d_count=17` 때문에 risk validator의 review backlog throttle이 submit-mode new buy를 막았다.
- `QQQ/SPY` benchmark fallback: fresh quote는 있었지만 buy-side backlog throttle이 그대로 적용되고, sell-first directive에서 이미 `AVGO` executable exit이 확보되어 이번 cycle submit 후보에서는 제외했다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_source_of_record_plus_live_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_submit_used_first_of_two_slots |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | pass_avgo_0.0065_minutes |
| spread_within_after_hours_policy | pass_avgo_0.1014pct |
| whole_share_day_limit_extended_hours_order | pass_avgo_sell_exit_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_client_order_id_reconciled_open_new_lifecycle_recorded |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-0911-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-0911-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-22-0911-after-hours-autopilot.json` -> PASS

## Submit And Reconcile

- Submitted order: `AVGO` sell `1` share, `limit_price=384.13`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-0911-sell-avgo-01`
- Alpaca MCP `place_stock_order` returned `order_id=aea04b7c-a44e-470d-b6a0-bfa05827fd4a`, initial `status=pending_new`.
- Immediate `get_order_by_client_id`와 `get_orders(status=all|open)` readback은 same `client_order_id`를 `status=new`, `filled_qty=0`로 재확인했다.
- `get_all_positions` cross-check에서는 `AVGO qty=1`, `qty_available=0`가 보여 해당 1주가 open sell order로 예약된 상태임을 확인했다. `get_account_activities(...FILL...)`는 이번 `AVGO` submit에 대한 신규 fill을 아직 반환하지 않았다.
- policy `cancel_unfilled_after_minutes=5`는 후속 scheduler lifecycle에서 처리하도록 남기고, 이번 cycle은 no-retry open order lifecycle record로 종료한다. 다른 `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-22-0911-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-22-0911-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-22-0911-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-0911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-22-0911-after-hours-autopilot-post-trade.json`
