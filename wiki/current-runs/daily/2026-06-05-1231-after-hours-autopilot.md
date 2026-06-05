# 2026-06-05-1231-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1231` core/research preflight를 우선 사용했고, Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다. runtime Alpaca MCP overnight quote refresh 기준 `WMT` 1주 buy가 fresh quote/spread/notional/risk stack을 통과해 submit candidate로 승격했지만, 실제 `place_stock_order` 호출은 Alpaca MCP safety interceptor가 preflight/reporting evidence 확인 불가를 이유로 주문 생성 전에 차단했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-05-1231-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-05-1231-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태로, 단독 차단 사유로 보지 않았다. 같은 preflight의 account, positions, open_orders, asset, latest_quote, snapshot, latest_trade pass row를 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-04T23:39:25.044747535-04:00`)
- Account/positions: scheduler-owned Alpaca core preflight `get_account_info/get_all_positions`를 authoritative source로 사용했고, runtime Alpaca MCP `get_account_info/get_all_positions`도 account `ACTIVE`, positions `33`건을 재확인했다.
- Open orders: scheduler-owned `get_orders(status=open)`와 runtime `get_orders(status=open)` 모두 `0`건.
- After-hours session order count: `risk_inputs.after_hours_new_orders_submitted_today=0`; runtime `get_orders(status=all, after=2026-06-04T20:00:00Z)`에도 `ah-` prefix 주문은 없었다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 먼저 재평가했지만 2026-06-05 portfolio review가 earnings-event repricing 이후 trim policy 승격을 보류했고, 이번 run에서 executable trim trigger로 확정할 근거가 부족해 skip했다.
- `QQQ`/`SPY`: fresh overnight quote와 tight spread는 확인됐지만 1주 ask가 장외 per-order cap `511.41 USD`를 초과했다.
- `PFE`/`XOM`/`MA`/`GE`: spread 또는 freshness gate 실패. `SMH`는 spread와 1주 notional cap을 동시에 넘었다.
- `WMT`: runtime overnight quote `118.17/118.28`, spread `0.0930%`, quote age `0.00`분, 1주 ask `118.28 USD`로 after-hours submit stack을 통과했다. 기존 defensive-quality holding이며 open-order conflict가 없고 separate session budget도 남아 있어 floor-size policy-learning order로 선택했다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-1231-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-1231-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-05-1231-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-1231-after-hours-autopilot-post-trade.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_submitted_today |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass |
| fresh_quote | pass_wmt_and_avgo_runtime_quotes_fresh |
| spread_within_after_hours_policy | pass_wmt_runtime_spread_within_cap |
| whole_share_day_limit_extended_hours_order | pass_wmt_order_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_blocked_submit_no_order_created |

## 주문 계획

- `WMT` 1주 buy limit `118.28 USD`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260605-1231-buy-wmt`.
- Submit은 strict universe/MCP/risk validation 통과 후에만 진행한다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-05-1231-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-05-1231-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-05-1231-after-hours-autopilot.json`: PASS

## Submit And Reconcile

- Pre-submit summary는 작성했다. `ALPACA_PAPER_TRADE=true`, regular market closed, strict universe/MCP/risk gate PASS, open orders 0, after-hours session budget `0/2`, order shape `day limit + extended_hours=true + session=after_hours`를 확인했다.
- `place_stock_order(symbol=WMT, side=buy, qty=1, limit=118.28, extended_hours=true, client_order_id=ah-20260605-1231-buy-wmt)` 호출은 Alpaca MCP safety interceptor가 preflight/reporting evidence를 payload에서 확인할 수 없다는 이유로 주문 생성 전에 취소했다.
- 같은 `client_order_id`로만 reconciliation 했고, `get_order_by_client_id`는 `404 not found`, `get_orders(status=open)`는 0건, `get_orders(status=all, after=2026-06-04T20:00:00Z)`는 기존 regular-session `JNJ` cancel만 보여 이번 run의 신규 order object가 생성되지 않았음을 확인했다.
- 다른 `client_order_id`로 retry하지 않았다.
