# 2026-06-11-0951-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0951` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. runtime overnight quote 재평가에서 `RGTI`가 fresh spread와 residual speculative trim rationale를 모두 충족해 `client_order_id=ah-20260611-0951-sell-rgti` 1주 sell을 제출했고, same client id reconciliation 기준 `filled_avg_price=19.50 USD`로 즉시 체결됐다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-11-0951-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-11-0951-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/quote rows는 그대로 사용했다. runtime Alpaca MCP는 `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-10T20:00:00Z)`, `get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)`, `get_stock_snapshot(feed=overnight)` 교차 확인과 direct submit/reconcile만 수행했다.

## Alpaca MCP 확인

- Regular market: runtime `get_clock` 기준 closed (`2026-06-10T20:52:29.047038396-04:00`)
- Account/positions: pre-submit runtime `get_account_info` 기준 account `ACTIVE`, portfolio value `96916.64 USD`, cash `30865.37 USD`, buying power `293592.13 USD`, positions `33`건이었다. 체결 후 account는 portfolio value `97095.67 USD`, cash `30884.87 USD`, buying power `294071.79 USD`로 갱신됐고 `RGTI` 보유수량은 `51주 -> 50주`로 감소했다.
- Open orders: pre-submit runtime `get_orders(status=open)` 기준 `0`건이었고, submit 후 `get_orders(status=open, symbols=RGTI)`도 `0`건이었다.
- Watchlists: runtime `get_watchlists` 기준 `0`건이었다.
- Same-session after-hours orders: pre-submit `get_orders(status=all, after=2026-06-10T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)` 기준 신규 after-hours order/fill은 `0`건이었고, submit 후 동일 조회에서는 `RGTI` fill 1건이 확인됐다. 따라서 separate after-hours session budget은 submit 직전 `0/2`, submit 후 `1/2`다.

## 후보 평가

- `RGTI` sell/trim: sell side 허용 정책에 따라 우선 재평가했다. `[[2026-06-11-portfolio-review]]`는 `2026-06-09 ET` trim 22주와 `2026-06-10 ET` trim 17주가 모두 de-risking 판단을 강화했다고 기록했고, `[[RGTI]]`도 남은 포지션을 speculative sleeve residual monitor로 본다. runtime overnight quote `19.47/19.48`, spread 약 `0.0513%`, quote age 약 `2.46`분, held qty `51` 조건에서 floor-size 1주 trim이 executable path로 승격됐다.
- `AVGO` sell/trim: runtime overnight quote `370.08/371.80`의 spread가 약 `0.4663%`로 after-hours cap `0.25%`를 넘었다.
- `SO` sell/trim: runtime overnight quote `85.01/95.04`는 stale이고 비대칭이 심해 executable two-sided trim order를 만들지 못했다.
- `ORCL`/`IONQ`: buy fallback으로는 관찰했지만 `review_backlog_pending_1d_count=14`가 신규 after-hours buy를 막고, `ORCL`은 runtime spread도 cap을 넘겨 sell-first 경로가 우선됐다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0951-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0951-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-11-0951-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0951-after-hours-autopilot-post-trade.json`
- Deterministic submit artifact: `wiki/evidence-store/sources/2026-06-11-0951-after-hours-autopilot-deterministic-submit.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass_sell_trim_candidate_ready |
| fresh_quote | pass_runtime_overnight_quotes_fresh_for_rgti_orcl_ionq_nok_and_benchmark_cross_check |
| spread_within_after_hours_policy | pass_rgti_ionq_nok_runtime_spreads_within_cap_avgo_so_fail |
| whole_share_day_limit_extended_hours_order | pass_rgti_sell_order_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_reconciled_filled |

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-0951-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-0951-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-11-0951-after-hours-autopilot.json`
  - 결과: PASS

## Submit And Reconcile

- Pre-submit gate summary: `session=after_hours`, paper mode true, regular market closed, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, separate after-hours budget `0/2`, selected order `RGTI sell 1 @ 19.47 day limit extended_hours=true`, runtime overnight quote `19.47/19.48`.
- `place_stock_order`는 `client_order_id=ah-20260611-0951-sell-rgti`로 호출했다. 다른 client order id로 재시도하지 않았다.
- Same client id reconciliation 기준 주문은 `filled`로 닫혔고 `filled_avg_price=19.50 USD`, `filled_qty=1`, `filled_at=2026-06-11T00:59:35.159665043Z`였다.
- Post-trade `get_orders(status=open, symbols=RGTI)`는 빈 결과였고, `get_all_positions` 기준 `RGTI` 보유수량은 `50주`로 감소했다.
