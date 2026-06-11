# 2026-06-11-1011-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1011` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. submit 직전 `AVGO` overnight spread가 cap을 다시 넘겨 탈락했고, runtime overnight quote `19.77/19.78` 기준 `RGTI`가 잔여 speculative sleeve de-risking floor-size trim 후보로 승격됐다. `client_order_id=ah-20260611-1011-sell-rgti` 1주 sell을 제출했고 immediate reconciliation 기준 `status=new` open order로 남아 lifecycle tracking 대상으로 기록했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-11-1011-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-11-1011-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing clock/account/positions/open-order/recent-activity/asset rows는 그대로 사용했다. runtime Alpaca MCP는 `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-10T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)`, `get_stock_snapshot(feed=overnight)`, `place_stock_order`, `get_order_by_client_id` 교차 확인만 수행했다.

## Alpaca MCP 확인

- Regular market: runtime `get_clock` 기준 closed (`2026-06-10T21:17:48.145055906-04:00`)
- Account/positions: submit 직전 `get_account_info` 기준 account `ACTIVE`, portfolio value `97644.23 USD`, cash `30884.87 USD`, buying power `295382.65 USD`, positions `33`건이었다. immediate reconciliation account는 portfolio value `97622.11 USD`, cash `30884.87 USD`, buying power `295320.71 USD`였고 `RGTI`는 `qty=50`, `qty_available=49`, `avg_entry_price=25.569583`으로 확인됐다.
- Open orders: submit 전 `get_orders(status=open)` 기준 `0`건이었다. submit 후 `get_order_by_client_id`와 `get_orders(status=open, symbols=RGTI)` 기준 `ah-20260611-1011-sell-rgti` 1건이 `status=new`로 남아 있다.
- Watchlists: runtime `get_watchlists` 기준 `0`건이었다.
- Same-session after-hours orders: `get_orders(status=all, after=2026-06-10T20:00:00Z)` 기준 이번 submit 전에는 `0951`의 `RGTI` fill 1건만 있었고, 이번 submit 후에는 `0951` fill 1건 + `1011` open sell 1건으로 separate after-hours session budget이 `1/2 -> 2/2`가 됐다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 먼저 재평가했고 한때 executable했지만, submit 직전 runtime overnight quote `375.17/376.53`의 spread가 약 `0.3625%`로 다시 after-hours cap `0.25%`를 넘었다.
- `RGTI` sell/trim: runtime overnight quote `19.77/19.78`, spread 약 `0.0506%`, quote age 약 `0.02`분, held qty `50`, residual speculative sleeve de-risking rationale를 충족해 최종 executable trim 후보가 됐다.
- `SO` sell/trim: runtime overnight quote `84.95/95.07`는 stale + asymmetric 상태라 executable two-sided trim order를 만들지 못했다.
- `ORCL`: runtime overnight quote `180.93/181.24`, spread 약 `0.1713%`, 1주 notional `181.24 USD`로 buy fallback까지는 가능했지만 `review_backlog_pending_1d_count=14` 때문에 신규 after-hours buy 슬롯은 여전히 닫혀 있었다.
- `IONQ`/`NOK`: 둘 다 freshness와 spread는 양호했지만 `IONQ`는 speculative 우선순위가 낮았고 `NOK`는 review-due add-block이 유지됐다.
- `SPY`/`QQQ`: runtime overnight quote는 fresh였지만 1주 ask가 각각 `728.18 USD`, `698.64 USD`로 after-hours per-order cap 약 `488.22 USD`를 넘었다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-1011-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-1011-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-11-1011-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-1011-after-hours-autopilot-post-trade.json`
- Deterministic submit artifact: `wiki/evidence-store/sources/2026-06-11-1011-after-hours-autopilot-deterministic-submit.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_one_of_two_submitted_one_remaining_before_submit |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass_rgti_sell_trim_candidate_ready |
| fresh_quote | pass_runtime_overnight_quotes_fresh_for_rgti_orcl_ionq_nok_and_benchmark_cross_check |
| spread_within_after_hours_policy | pass_rgti_orcl_ionq_nok_runtime_spreads_within_cap_avgo_so_fail |
| whole_share_day_limit_extended_hours_order | pass_rgti_sell_order_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_reconciled_open_order_lifecycle_recorded |

## 주문 계획 및 제출

- `market.session=after_hours`, `risk_inputs.after_hours_new_orders_submitted_today=1`, `session=after_hours`, `review_bucket=after_hours_validation`를 기록한 submit-mode order plan을 생성했다.
- validators는 모두 PASS였다: universe strict PASS, MCP strict PASS, `check-risk-policy.py --json` PASS.
- Pre-submit gate summary: `session=after_hours`, paper mode true, regular market closed, universe strict PASS, MCP strict PASS, risk PASS, separate after-hours budget `1/2`, selected order `RGTI sell 1 @ 19.77 day limit extended_hours=true`, latest overnight quote `19.77/19.78`.
- `place_stock_order`는 `client_order_id=ah-20260611-1011-sell-rgti`로 1회만 호출했고 다른 client order id로 재시도하지 않았다.
- submit 응답 `order_id=e725c081-8287-4484-9323-15349194c375`는 initial `pending_new`였고, same client id reconciliation 기준 현재 `status=new`, `filled_qty=0` open order다.

## Reconcile And Lifecycle

- `get_order_by_client_id`와 `get_orders(status=open, symbols=RGTI)` 기준 open extended-hours sell 1건이 남아 있다.
- `get_orders(status=all, symbols=RGTI, after=2026-06-10T20:00:00Z)` 기준 same-session records는 `0951` fill 1건과 `1011` open order 1건이다.
- `get_all_positions` 기준 `RGTI` 총 보유수량은 아직 `50주`이며 `qty_available=49`로 1주가 예약돼 있다.
- 이번 cycle에서는 cancel을 강제하지 않고 after-hours policy의 lifecycle tracking 대상으로 남긴다. 다음 stale/lifecycle check에서 동일 client order id를 계속 추적해야 한다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-1011-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-1011-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-11-1011-after-hours-autopilot.json`
  - 결과: PASS
