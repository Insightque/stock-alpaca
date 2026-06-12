# 2026-06-12-1011-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1011` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. buy fallback은 `review_backlog_pending_1d_count=14`에 따른 risk backlog throttle로 차단됐지만, sell-first 재평가에서 `PFE`가 repeated weak-review trim rationale와 fresh overnight quote/spread를 모두 충족해 `client_order_id=ah-20260612-1011-sell-pfe-01` 1주 sell을 제출했고 same client id reconciliation 기준 `filled_avg_price=26.13 USD`로 즉시 체결됐다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-12-1011-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-12-1011-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/quote/spread rows는 그대로 사용했다. runtime Alpaca MCP는 `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_account_activities`, `get_watchlists`, `get_stock_latest_quote(feed=iex)`, `get_stock_snapshot(feed=iex)`, `get_stock_latest_quote(feed=overnight)` 교차 확인과 direct submit/reconcile만 수행했다.

## Alpaca MCP 확인

- Regular market: runtime `get_clock` 기준 closed (`2026-06-11T21:20:38.959215227-04:00`)
- Account/positions: pre-submit runtime `get_account_info` 기준 account `ACTIVE`, portfolio value `100039.27 USD`, cash `31285.06 USD`, buying power `301364.60 USD`, positions `33`건이었다. 체결 후 account는 portfolio value `99948.23 USD`, cash `31311.19 USD`, buying power `301276.12 USD`로 갱신됐고 `PFE` 보유수량은 `6주 -> 5주`로 감소했다.
- Open orders: pre-submit runtime `get_orders(status=open)` 기준 `0`건이었고, submit 후 `get_orders(status=open, symbols=PFE)`도 `0`건이었다.
- Watchlists: runtime `get_watchlists` 기준 `0`건이었다.
- Same-session after-hours orders: pre-submit `get_orders(status=all, after=2026-06-11T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-11T20:00:00Z)` 기준 신규 after-hours order/fill은 `0`건이었고, submit 후 동일 조회에서는 `PFE` fill 1건이 확인됐다. 따라서 separate after-hours session budget은 submit 직전 `0/2`, submit 후 `1/2`다.

## 후보 평가

- `PFE` sell/trim: sell side 허용 정책에 따라 우선 재평가했다. `[[PFE]]`, `[[2026-06-09-portfolio-review]]`, `[[2026-06-05-portfolio-review]]`, `[[2026-06-04-portfolio-review]]`에는 defensive-diversification validation이 반복적으로 약했고 replacement-quality margin rule이 부족하다는 근거가 남아 있다. runtime overnight quote `26.12/26.16`, spread `0.1529%`, quote age `0.6`분, held qty `6`, open-order duplicate 없음 조건에서 floor-size 1주 trim이 executable path로 승격됐다.
- `PLTR` buy fallback: runtime overnight quote는 fresh했고 spread도 통과했지만 `review_backlog_pending_1d_count=14`가 신규 buy 허용치 `0`으로 계산돼 risk gate에서 차단됐다.
- `QQQ`: fresh and liquid였지만 1주 ask가 after-hours per-order cap 약 `500.20 USD`를 초과했다.
- `RGTI` / `AVGO` / `SO`: sell-first 후보로 재평가했지만 overnight spread가 각각 `0.4280%`, `0.3151%`, `3.6528%`로 after-hours cap `0.25%`를 넘었다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_one_of_two_submitted |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass_sell_trim_candidate_ready |
| fresh_quote | pass_runtime_overnight_quote_under_5_minutes |
| spread_within_after_hours_policy | pass_runtime_overnight_spread_0_1529pct |
| whole_share_day_limit_extended_hours_order | pass_pfe_sell_order_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_reconciled_filled_by_client_order_id |

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-12-1011-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-12-1011-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-12-1011-after-hours-autopilot.json`
  - 결과: PASS

## Submit And Reconcile

- Pre-submit gate summary: `session=after_hours`, paper mode true, regular market closed, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, separate after-hours budget `0/2`, selected order `PFE sell 1 @ 26.12 day limit extended_hours=true`, runtime overnight quote `26.12/26.16`.
- `place_stock_order`는 `client_order_id=ah-20260612-1011-sell-pfe-01`로 정확히 1회 호출했다. 다른 client order id로 재시도하지 않았다.
- Same client id reconciliation 기준 주문은 `filled`로 닫혔고 `filled_avg_price=26.13 USD`, `filled_qty=1`, `filled_at=2026-06-12T01:21:39.341022113Z`였다.
- Post-trade `get_orders(status=open, symbols=PFE)`는 빈 결과였고, `get_all_positions` 기준 `PFE` 보유수량은 `5주`로 감소했다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-12-1011-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-12-1011-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-12-1011-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-12-1011-after-hours-autopilot-post-trade.json`
