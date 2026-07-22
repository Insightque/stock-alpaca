# 2026-07-22-0951-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date: `2026-07-21 EDT`
- Scheduler artifact date: `2026-07-22 KST`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0951` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live Alpaca continuity에서 regular market closed, account `ACTIVE`, positions `32`, open orders `1`, same-session after-hours submitted orders `1`, fills `0`를 재확인했다. 기존 `client_order_id=ah-20260722-0911-sell-avgo-01` `AVGO` sell은 여전히 `status=new` open order였고 `AVGO qty_available=0`가 유지되어 같은 주문의 lifecycle만 기록했다. 이번 `0951` cycle에서는 신규 `place_stock_order` 호출을 하지 않았다. 다만 risk validator는 기존 `AVGO` open order age `32.6분`이 lifecycle limit `30.0분`을 넘어 FAIL했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-22-0951-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-22-0951-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-0951-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle의 run id는 KST scheduler 파일명 `2026-07-22-0951-*`를 유지하지만, 실제 미국 장 판단과 continuity는 `2026-07-21 EDT` clock 기준으로 기록했다.

## Alpaca MCP 확인

- Regular market: closed. live `get_clock` 기준 `timestamp=2026-07-21T20:53:36.571038915-04:00`였다.
- Account: live `get_account_info` 기준 account `ACTIVE`, portfolio value `98,491.59 USD`, cash `28,610.95 USD`, buying power `297,671.72 USD`였다.
- Positions / orders: live `get_all_positions` 기준 positions `32`건이었다. `get_orders(status=open)`와 `get_orders(status=all, after=2026-07-21T20:00:00Z)`는 모두 `AVGO` after-hours sell `1건`만 반환했고, `get_account_activities(activity_types=[FILL], after=2026-07-21T20:00:00Z)` 기준 same-session fills는 `0`건이다.
- Existing order lifecycle: `get_order_by_client_id(ah-20260722-0911-sell-avgo-01)` readback은 `order_id=aea04b7c-a44e-470d-b6a0-bfa05827fd4a`, `status=new`, `filled_qty=0`, `limit_price=384.13`, `extended_hours=true`를 유지했다. `get_all_positions` 기준 `AVGO qty=1`, `qty_available=0`라 동일 1주가 여전히 open sell order에 예약된 상태다.
- Quote boundary: live `get_stock_latest_quote(feed=overnight)` 기준 `AVGO`는 `383.51/384.51`, spread 약 `0.2604%`, quote age 약 `0.15`분으로 여전히 fresh했다. 그러나 동일 `client_order_id` open order가 이미 살아 있으므로 재제출은 금지됐다. `SO`는 `87.31/95.78`, spread 약 `9.25%`, quote age 약 `9.19`분으로 fail이다.

## 후보 평가

- `AVGO` sell/exit: 가격과 spread는 여전히 strict after-hours gate 안쪽이지만, `0911` cycle에서 이미 제출된 같은 residual exit이 `status=new` open order로 살아 있다. `qty_available=0`이고 workflow contract가 `client_order_id` 재사용 외 다른 retry를 금지하므로 이번 cycle에서 새 `AVGO` sell을 다시 제출하지 않았다.
- `SO` sell/trim: live overnight quote가 stale + wide spread라 hard gate fail이다.
- `WMT` / `MCD` buy fallback: `WMT 109.91/110.14`, `MCD 264.09/264.28`로 quote shape 자체는 양호했지만 `review_backlog_pending_1d_count=17` 때문에 review backlog throttle이 submit-mode new buy를 막았다.
- `QQQ` / `SPY` benchmark fallback: quote freshness와 spread는 pass였지만 `after_hours_policy.max_notional_pct_per_order=0.005` cap을 넘는다.
- `NOK`: quote는 fresh했지만 `review-due-index.json`의 `blocked_add_symbols`에 남아 있어 add path를 열지 않았다.
- `SMH` / `NEE` / `CVX` / `GS`: `SMH`는 spread `0.2727%` + per-order cap, `NEE/CVX/GS`는 stale 또는 spread cap fail이다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_source_of_record_plus_live_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_one_of_two_already_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | FAIL_open_order_age_exceeds_lifecycle_limit |
| fresh_quote | PASS_avgo_wmt_mcd_nok_qqq_spy_fresh_but_so_stale |
| spread_within_after_hours_policy | FAIL_remaining_sell_or_buy_candidates_hit_spread_cap_or_buy_policy_blockers |
| whole_share_day_limit_extended_hours_order | fail_no_new_eligible_order_beyond_existing_avgo_open_order |
| immediate_reconcile_and_cancel_or_lifecycle_record | PASS_existing_client_order_id_reconciled_without_retry |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-0951-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-0951-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-22-0951-after-hours-autopilot.json` -> FAIL (`AVGO` open order age `32.6분` > lifecycle limit `30.0분`; warning `orders is empty`)

## Submit And Reconcile

- Submitted order this cycle: 없음
- Existing after-hours order: `AVGO` sell `1` share, `limit_price=384.13`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-0911-sell-avgo-01`
- Immediate readback: same `client_order_id`는 여전히 `status=new`, `filled_qty=0` open order다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았고, 기존 주문을 바꾸거나 중복 제출하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-22-0951-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-22-0951-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-22-0951-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-0951-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-22-0951-after-hours-autopilot-post-trade.json`
