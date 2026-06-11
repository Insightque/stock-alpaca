# 2026-06-12-0751-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0751` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote가 모두 5분 freshness cap을 크게 넘겨 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-12-0751-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-12-0751-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/quote/spread rows는 그대로 사용했다. runtime Alpaca MCP는 `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-11T20:00:00Z)` 교차 확인만 수행했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-11T18:53:17.218392266-04:00` runtime `get_clock`)
- Account/positions: runtime `get_account_info` / `get_all_positions` 교차 확인 기준 account `ACTIVE`, portfolio value `99,990.49 USD`, cash `31,285.06 USD`, buying power `301,337.63 USD`, positions `33`건이었다.
- Open orders: runtime `get_orders(status=open)` 기준 `0`건이었다.
- Same-session after-hours orders: runtime `get_orders(status=all, after=2026-06-11T20:00:00Z)` 기준 신규 after-hours order는 `0`건이었다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap은 `0/2`다.
- Watchlists / asset / quote / spread evidence: 이 run에서는 scheduler-owned `0751` Alpaca core preflight rows를 source-of-record로 재사용했다.

## 후보 평가

- `ADBE`: scheduler-owned IEX quote `207.77/207.88`는 spread 약 `0.0529%`로 양호했고 1주 ask `207.88 USD`도 after-hours per-order cap 약 `499.95 USD` 이내였다. 그러나 quote timestamp가 `2026-06-11T20:55:03.360834505Z`라 runtime cutoff 기준 약 `118.23`분 stale이었다.
- `PLTR`: IEX quote `131.39/131.49`, spread `0.0761%`, 1주 ask `131.49 USD`로 fallback buy shape는 가능했지만 timestamp가 `2026-06-11T20:46:34.541886154Z`라 약 `126.71`분 stale이었다.
- `QQQ` / `SPY`: spread는 각각 `0.0350%`, `0.1709%`로 양호했지만 quote age가 약 `127.19`분, `146.10`분 stale였고 1주 ask `715.38 USD`, `738.09 USD`가 after-hours per-order cap을 넘었다.
- `RGTI` sell/trim: allowed sell side에 따라 우선 재평가했다. asset은 `active/tradable/overnight_tradable`였지만 IEX quote `20.66/21.99` spread `6.2368%`와 quote age 약 `118.46`분이 동시에 blocker였다.
- `AVGO` sell/trim: same-day regular-session trim fill이 이미 존재했고 IEX quote `361.80/407.29` spread `11.8296%`도 cap을 크게 넘었다.
- `SO`: IEX quote `88.56/99.23` spread `11.3638%` fail에 기존 trim metric gap이 그대로 남았다.
- `KLAC` / `TSLA` / `SMH`: shortlist에는 남았지만 KLAC spread `0.4724%`, TSLA spread `0.5425%`, SMH spread `5.9416%`로 after-hours spread cap을 넘었고 stale 문제도 함께 남았다.
- Review backlog: `review-due-index` 기준 `pending_1d_count=14`, `pending_5d_count=13`, `pending_20d_count=1`이었다. 이번 cycle은 backlog throttle보다 fresh-quote hard gate가 직접 차단 요인이었다.

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
| risk_policy | fail_no_eligible_order_survived_after_hours_fresh_quote_gate |
| fresh_quote | fail_scheduler_preflight_quotes_stale_118.23_to_158.62_minutes |
| spread_within_after_hours_policy | fail_only_adbe_pltr_qqq_spy_tight_but_stale |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## 주문 계획

- `market.session=after_hours`, `risk_inputs.after_hours_new_orders_submitted_today=0`, `session=after_hours`, `review_bucket=after_hours_validation`를 기록한 submit-mode order plan을 생성했다.
- review backlog는 `14/13/1`로 반영했다. 별도 after-hours 주문 예산은 열려 있었지만 모든 executable candidate가 fresh-quote, spread, same-day sell discipline, 또는 per-order notional cap gate에서 차단돼 `orders=[]`로 유지했다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-12-0751-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-12-0751-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-12-0751-after-hours-autopilot.json`

## Submit And Reconcile

- `place_stock_order`, `cancel_order_by_id`는 이번 cycle에서 호출하지 않았다.
- runtime Alpaca MCP cross-check 기준 신규 after-hours order/fill 없음, standing extended-hours order 없음, 포지션 수량 변화 없음.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-12-0751-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-12-0751-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-12-0751-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-12-0751-after-hours-autopilot-post-trade.json`
