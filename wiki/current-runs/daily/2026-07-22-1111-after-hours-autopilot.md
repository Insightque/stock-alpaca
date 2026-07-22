# 2026-07-22-1111-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date: `2026-07-21 EDT`
- Scheduler artifact date: `2026-07-22 KST`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1111` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live Alpaca continuity에서는 regular market closed, account `ACTIVE`, positions `31`, open orders `0`, same-session after-hours submitted orders `1`, fills `1`를 재확인했다. 기존 `client_order_id=ah-20260722-0911-sell-avgo-01` `AVGO` sell은 계속 `filled` 상태로 유지됐고 `AVGO position 없음`이 확인됐다. 이번 `1111` cycle에서는 신규 `place_stock_order` 호출을 하지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-22-1111-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-22-1111-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-1111-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle의 run id는 KST scheduler 파일명 `2026-07-22-1111-*`를 유지하지만, 실제 미국 장 판단과 continuity는 `2026-07-21 EDT` clock 기준으로 기록했다.

## Alpaca MCP 확인

- Regular market: closed. live `get_clock` 기준 `timestamp=2026-07-21T22:13:22.634832149-04:00`였다.
- Account: live `get_account_info` 기준 account `ACTIVE`, portfolio value `98421.39 USD`, cash `28995.09 USD`, buying power `298003.67 USD`였다.
- Orders / fills: live `get_orders(status=open)` 기준 open orders는 `0`건이었다. `get_orders(status=all, after=2026-07-21T20:00:00Z)`와 `get_account_activities(activity_types=[FILL], after=2026-07-21T20:00:00Z)` 기준 same-session after-hours order/fill은 `AVGO` sell `1건`뿐이며 `filled_avg_price=384.14 USD`, `filled_at=2026-07-22T01:48:58.933756Z`였다.
- Positions: live `get_all_positions` 기준 positions `31`건이었다. `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=402`였다.
- Existing order lifecycle: same-session `AVGO` sell `client_order_id=ah-20260722-0911-sell-avgo-01`는 `status=filled`, `filled_qty=1`, `extended_hours=true`, `session=after_hours` lifecycle close를 유지했다. retry나 alternate client order id는 사용하지 않았다.

## 후보 평가

- `SO` sell/trim: overnight quote `88.59/95.80`, spread 약 `8.1386%`, quote age 약 `10.9분`으로 after-hours spread/freshness hard gate fail이다.
- `WMT` buy fallback: quote `110.02/110.44`, spread 약 `0.3817%`, quote age 약 `1.5분`으로 freshness는 pass지만 spread가 `after_hours_policy.max_spread_pct=0.25%`를 넘는다. `review_backlog_pending_1d_count=17` backlog throttle도 계속 남아 있다.
- `MCD` buy fallback: quote `264.60/264.79`, spread 약 `0.0718%`, quote age 약 `1.0분`으로 spread와 notional cap은 pass였지만 `review_backlog_pending_1d_count=17`이 `stop_new_buys_at_pending_1d=12`를 넘고 `required_for_submit_buys=true`라 submit-mode buy를 열 수 없었다.
- `QQQ` / `SPY` benchmark fallback: quote freshness와 spread는 pass였지만 `after_hours_policy.max_notional_pct_per_order=0.005` cap을 1주 기준으로 넘는다.
- `SMH`: spread 약 `0.2804%`로 spread cap fail이며 notional cap도 넘는다.
- `NOK`: quote는 fresh했지만 spread 약 `0.4562%`로 cap을 넘고 `review-due-index.json`의 `blocked_add_symbols`에도 남아 있다.
- `NEE` / `CVX` / `GS`: spread cap fail이고 `CVX`, `GS`는 freshness까지 fail이다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_source_of_record_plus_live_continuity_after_fill |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_one_of_two_already_submitted_and_filled |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | PASS_mcd_qqq_spy_smh_nok_wmt_fresh_but_so_cvx_gs_stale_and_nee_near_limit |
| spread_within_after_hours_policy | FAIL_sell_side_so_and_buy_side_wmt_smh_nok_nee_cvx_gs_fail_or_buy_throttle_blocks_only_remaining_spread_pass_mcd |
| whole_share_day_limit_extended_hours_order | fail_no_new_eligible_order_due_to_mcd_review_backlog_and_remaining_candidate_spread_or_cap_fail |
| immediate_reconcile_and_cancel_or_lifecycle_record | PASS_avgo_client_order_id_reconciled_filled_without_retry |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-1111-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-1111-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-22-1111-after-hours-autopilot.json`

## Submit And Reconcile

- Submitted order this cycle: 없음
- Reconciled prior after-hours order: `AVGO` sell `1` share, `limit_price=384.13`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-0911-sell-avgo-01`
- Immediate readback / same-session fill ledger: same `client_order_id`는 `status=filled`, `filled_qty=1`, `filled_avg_price=384.14`였다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았고 기존 주문의 fill 상태만 continuity로 재확인했다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-22-1111-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-22-1111-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-22-1111-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-1111-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-22-1111-after-hours-autopilot-post-trade.json`
