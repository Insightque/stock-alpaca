# 2026-06-12-1131-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1131` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 earlier `1011` `PFE` trim fill 이후 `1/2`가 남아 있었지만, `1131` submit-boundary quote stack에서는 모든 executable candidate가 5분 freshness cap 또는 after-hours spread cap에 막혀 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-12-1131-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-12-1131-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/quote/spread rows는 그대로 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-11T22:31:05.040417902-04:00`, scheduler-owned `get_clock`)
- Account/positions: scheduler-owned `get_account_info` / `get_all_positions` 기준 account `ACTIVE`, portfolio value `99,897.29 USD`, cash `31,311.19 USD`, buying power `301,212.28 USD`, positions `33`건이었다.
- Open orders: scheduler-owned `get_orders_open` 기준 `0`건이었다.
- Same-session after-hours fills: scheduler-owned `get_account_activities(activity_types=FILL)`를 `2026-06-11T20:00:00Z` cutoff로 재해석하면 same-session fill은 `PFE` 1건이었다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=1`, session cap은 `1/2`다.
- Asset / quote / spread evidence: scheduler-owned `1131` core preflight asset rows와 IEX quote/snapshot rows를 submit-boundary source-of-record로 유지했다.

## 후보 평가

- `ADBE`: IEX quote `207.77/207.88`, spread `0.0529%`, 1주 ask `207.88 USD`로 notional cap 이내였지만 quote age가 `336.34`분이라 fresh-quote gate를 통과하지 못했다.
- `PLTR`: IEX quote `131.39/131.49`, spread `0.0761%`, 1주 ask `131.49 USD`로 fallback buy shape는 가능했지만 quote age `344.82`분으로 stale였다.
- `QQQ` / `SPY`: spread는 각각 `0.035%`, `0.1709%`로 양호했지만 quote age가 `345.30`분, `364.21`분 stale였고 1주 ask `715.38 USD`, `738.09 USD`가 after-hours per-order cap 약 `499.49 USD`를 넘었다.
- `PFE` sell/trim: earlier `1011` trim fill 이후 같은 세션 budget `1/2`가 이미 사용된 상태였고, `1131` preflight quote `24.87/27.58`, spread `10.3337%`, quote age `391.38`분이 동시에 blocker였다.
- `RGTI` / `AVGO` / `SO` sell/trim: allowed sell side 재평가 대상이었지만 spread가 각각 `6.2368%`, `11.8296%`, `11.3638%`로 크게 벌어져 있었고 quote도 모두 stale였다.
- `ORCL` / `KLAC` / `TSLA` / `SMH`: ORCL spread `10.1656%`, KLAC `0.4724%`, TSLA `0.5425%`, SMH `5.9416%` 또는 stale quote 때문에 executable fallback이 되지 못했다.
- Review backlog: `review-due-index` 기준 `pending_1d_count=14`, `pending_5d_count=13`, `pending_20d_count=1`이었다. 이번 cycle은 backlog throttle보다 fresh-quote hard gate가 직접 차단 요인이었다.

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
| risk_policy | fail_no_eligible_order_survived_after_hours_fresh_quote_gate |
| fresh_quote | fail_scheduler_preflight_quotes_stale_336.34_to_391.38_minutes |
| spread_within_after_hours_policy | fail_only_adbe_pltr_qqq_spy_tight_but_stale |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## 주문 계획

- `market.session=after_hours`, `risk_inputs.after_hours_new_orders_submitted_today=1`, `session=after_hours`, `review_bucket=after_hours_validation`를 기록한 submit-mode order plan을 생성했다.
- review backlog는 `14/13/1`로 반영했다. 별도 after-hours 주문 예산은 `1/2`가 남아 있었지만 모든 executable candidate가 fresh-quote, spread, 또는 per-order notional cap gate에서 차단돼 `orders=[]`로 유지했다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-12-1131-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-12-1131-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-12-1131-after-hours-autopilot.json`

## Submit And Reconcile

- 이번 cycle에서는 신규 `place_stock_order`, `cancel_order_by_id` 호출이 없었다.
- submit attempt는 없었고, scheduler-owned account/positions/open-order snapshot 기준 포지션 수량 변화는 없었다. same-session after-hours fill ledger에는 earlier `PFE` trim 1건이 유지됐다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-12-1131-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-12-1131-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-12-1131-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-12-1131-after-hours-autopilot-post-trade.json`
