# 2026-06-12-1411-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1411` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. runtime `overnight` quote가 fresh하게 돌아와 `AVGO` 1주 trim sell submit path를 열었고, 계획한 `client_order_id`로 한 번만 제출했다. immediate post-trade `get_all_positions`에서 `AVGO 5주 -> 4주`가 확인돼 filled reconciliation으로 기록한다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-12-1411-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-12-1411-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset rows는 그대로 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-12T01:11:05.12095294-04:00` scheduler-owned clock)
- Account/positions: scheduler-owned account snapshot은 account `ACTIVE`, portfolio value `99,971.25 USD`, cash `31,311.19 USD`, buying power `301,295.55 USD`, positions `33`건이었다. submit 직후 exposed readback surface는 post-account 전용 조회를 제공하지 않았지만, immediate `get_all_positions`에서 `AVGO 5주 -> 4주`와 positions `33` 유지가 확인됐다.
- Open orders/watchlists: scheduler-owned preflight open orders `0`, watchlists `0`를 유지했고 이번 runtime `get_watchlists`도 `0`이었다.
- Same-session after-hours fills: earlier `1011` `PFE` trim 1건이 있었고, 이번 `1411` `AVGO` trim을 추가해 separate after-hours session budget은 `2/2`가 됐다.

## 후보 평가

- `AVGO` sell/trim: runtime overnight quote `386.79/387.61`, spread `0.2119%`, quote age `0.51`분, held qty `5` 조건에서 post-earnings staged de-risking 1주 trim 후보로 승격했다. `[[AVGO]]`, `[[2026-06-12-portfolio-review]]`, `[[2026-06-11-portfolio-review]]`, `[[2026-06-10-portfolio-review]]`에는 validation add failure와 staged de-risking 유지 판단이 누적돼 있다.
- `ADBE` / `PLTR`: fresh overnight quote와 spread는 통과했지만 `review_backlog_pending_1d_count=14`로 buy path가 닫혀 제외했다.
- `QQQ` / `SPY`: fresh and liquid였지만 1주 ask가 after-hours per-order cap `499.86 USD`를 초과했다.
- `PFE`: same-session `1011` trim fill이 이미 존재해 이번 cycle은 다른 sell-side observation을 우선했다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_one_of_two_submitted -> submit 후 `2/2` 소진 |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | pass_runtime_overnight_quote_under_5_minutes |
| spread_within_after_hours_policy | pass_runtime_overnight_spread_0.2119pct |
| whole_share_day_limit_extended_hours_order | pass_avgo_sell_order_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_reconciled_by_client_order_id_submit_record_plus_position_delta |

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-12-1411-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-12-1411-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-12-1411-after-hours-autopilot.json` -> PASS

## Submit And Reconcile

- Submitted order: `AVGO` sell `1` share, `limit_price=386.79`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260612-1411-sell-avgo-01`
- Alpaca MCP `place_stock_order` returned `order_id=ecdd85cb-0b94-410c-b9f8-5e29f4a8ee2b`, `status=pending_new`, `submitted_at=2026-06-12T05:18:34.074577545Z`.
- Exposed readback surface in this runtime did not provide `get_order_by_client_id`/`get_orders` query tools, so immediate reconciliation used the same submitted `client_order_id` plus post-trade Alpaca MCP `get_all_positions` delta. `AVGO` 보유수량이 `5주 -> 4주`로 즉시 감소했고 retry 또는 alternate client order id는 사용하지 않았다.
- Exact `filled_avg_price`는 이번 runtime surface에서 확인하지 못해 기록하지 않는다. post-trade account cash/buying power delta는 limit price 기준 추정치로만 post-trade snapshot에 남긴다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-12-1411-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-12-1411-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-12-1411-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-12-1411-after-hours-autopilot-post-trade.json`
