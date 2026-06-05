# 2026-06-05-1251-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1251` core/research preflight를 우선 사용했고, Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다. stale `ah-20260605-1231-buy-wmt`를 먼저 취소한 뒤 strict universe/MCP/risk gate와 fresh overnight quote/spread gate를 통과한 `WMT` 1주 after-hours buy를 Alpaca MCP로 제출했고, 같은 `client_order_id` 기준 즉시 `filled`로 체결됐다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-05-1251-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-05-1251-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태로, 단독 차단 사유로 보지 않았다. 같은 preflight의 account, positions, open_orders, asset, latest_quote, snapshot, latest_trade pass row를 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-04T23:54:52.17674704-04:00`)
- Account/positions: runtime Alpaca MCP `get_account_info/get_all_positions` 기준 account `ACTIVE`, positions `33`건에서 `34`건이 아니라 `WMT` 수량 증가만 반영되고 총 포지션 종목 수는 그대로 유지됐다.
- Open orders: stale `ah-20260605-1231-buy-wmt` 취소 후 `get_orders(status=open)`는 0건, 신규 `ah-20260605-1251-buy-wmt`도 즉시 fill되어 open order로 남지 않았다.
- After-hours session order count: `risk_inputs.after_hours_new_orders_submitted_today=1`로 시작했고, 이번 run이 `WMT` 1건을 추가해 별도 장외 session budget `2/2`를 채웠다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 먼저 재평가했지만 `2026-06-05-portfolio-review`가 earnings-event repricing 이후 trim policy 승격을 보류했고 `review-due-index`도 add 차단 상태를 유지해 executable sell trigger로 승격하지 못했다.
- `QQQ`/`SPY`: fresh overnight quote와 tight spread는 확인됐지만 1주 ask가 장외 per-order cap `510.82 USD`를 초과했다.
- `PFE`: 1주 notional은 작았지만 spread 자체는 통과했고, 최종 우선순위에서 기존 actionable holding `WMT`보다 낮았다.
- `SMH`: 1주 ask가 장외 per-order cap을 초과했다.
- `XOM`/`MA`/`GE`: spread 또는 freshness gate 실패.
- `WMT`: runtime overnight quote `118.16/118.39`, spread `0.1944%`, quote age `0.77`분, 1주 ask `118.39 USD`로 after-hours submit stack을 통과했다. 기존 defensive-quality holding이며 stale prior open order를 정리한 뒤 duplicate/open-order conflict가 없고 separate session budget 마지막 1슬롯도 남아 있어 floor-size policy-learning order로 선택했다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-1251-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-1251-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-05-1251-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-1251-after-hours-autopilot-post-trade.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_one_submitted_today_one_slot_remaining |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass_submit_candidate_ready |
| fresh_quote | pass_wmt_and_avgo_runtime_quotes_fresh |
| spread_within_after_hours_policy | pass_wmt_runtime_spread_within_cap |
| whole_share_day_limit_extended_hours_order | pass_wmt_order_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_reconciled_filled_by_client_order_id |

## 주문 계획

- `WMT` 1주 buy limit `118.39 USD`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260605-1251-buy-wmt`.
- Submit은 strict universe/MCP/risk validation 통과 후에만 진행했다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-05-1251-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-05-1251-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-05-1251-after-hours-autopilot.json`: PASS

## Submit And Reconcile

- Pre-submit summary를 `place_stock_order` 직전에 기록했다. `ALPACA_PAPER_TRADE=true`, regular market closed, strict universe/MCP/risk gate PASS, stale prior open order cancelled, after-hours session budget `1/2`, order shape `day limit + extended_hours=true + session=after_hours`를 확인했다.
- `place_stock_order(symbol=WMT, side=buy, qty=1, limit=118.39, extended_hours=true, client_order_id=ah-20260605-1251-buy-wmt)`는 Alpaca MCP에서 실제 `order_id=6bc7b899-df65-463e-bee9-b671d20c2126`를 반환했다.
- 같은 `client_order_id`로만 reconciliation 했고, `get_order_by_client_id`는 `status=filled`, `filled_qty=1`, `filled_avg_price=118.38`, `filled_at=2026-06-05T03:59:25.256343803Z`를 반환했다.
- `get_orders(status=open)`는 0건이었고 `get_orders(status=all, after=2026-06-04T20:00:00Z)`는 `1231` WMT cancel과 `1251` WMT fill을 함께 보여 동일 session lifecycle을 확인했다.
- 다른 `client_order_id`로 retry하지 않았다.
