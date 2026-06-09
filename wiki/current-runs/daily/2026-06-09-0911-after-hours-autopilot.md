# 2026-06-09-0911-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0911` core/research preflight를 우선 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만, scheduler-owned Alpaca MCP quote/order/fill cross-check 기준 executable two-sided fresh quote stack을 만들지 못해 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-09-0911-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-09-0911-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/quote/spread rows는 그대로 사용했다. 이번 cycle은 after-hours-required row가 모두 preflight에 포함되어 추가 runtime Alpaca MCP 호출 없이 scheduler evidence만으로 submit boundary를 평가했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-08T20:11:09.4469609-04:00`)
- Account/positions: scheduler-owned core preflight를 주 원천으로 사용했다. account `ACTIVE`, portfolio value `99,853.38 USD`, cash `31,774.85 USD`, buying power `301,341.81 USD`, positions `32`건이다.
- Open orders: scheduler-owned `get_orders(status=open)` 기준 `0`건이었다.
- Watchlists: scheduler-owned Alpaca MCP `get_watchlists` 기준 `0`건이었다.
- Same-session after-hours orders: scheduler-owned `get_account_activities(activity_types=FILL)`와 open-order state 기준 신규 after-hours order/fill은 `0`건이었다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap은 `0/2`다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 우선 재평가했다. 그러나 scheduler-owned IEX quote는 bid-only `374.07`이고 timestamp `2026-06-08T20:00:02.048843518Z`로 약 `251.47`분 stale였다. executable trim order를 만들지 못했다.
- `QQQ`: scheduler-owned research shortlist의 가장 강한 fallback benchmark였다. IEX quote `714.93/715.02`는 spread 약 `0.0126%`로 양호했지만 timestamp가 `2026-06-08T20:22:05.194321373Z`라 decision clock 기준 약 `229.41`분 stale였다.
- `NVDA/NKE/ADBE/AMAT/XOM`: research shortlist에 포함됐지만 scheduler-owned IEX quote age가 `251.48-251.50`분 stale였고 spread도 각각 `8.1632%`, `8.3871%`, `8.6932%`, `8.8421%`, `7.1875%`로 after-hours cap `0.25%`를 크게 초과했다.
- `SPY/SMH`: benchmark/sector fallback으로 유지했지만 spread가 각각 약 `6.0052%`, `6.0522%` 수준으로 과도했고 quote age도 약 `251.50`분 stale였다.
- `PFE/BAC/RGTI`: IEX quote가 bid-only라 two-sided extended-hours order shape를 만들 수 없었다.
- Review backlog: `review-due-index` 기준 `pending_1d_count=0`, `pending_5d_count=13`, `pending_20d_count=1`이었다. 이번 cycle은 backlog throttle이 아니라 fresh-quote/spread hard gate가 직접 차단 요인이었다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-09-0911-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-09-0911-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-09-0911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-09-0911-after-hours-autopilot-post-trade.json`
- Deterministic submit artifact: `wiki/evidence-store/sources/2026-06-09-0911-after-hours-autopilot-deterministic-submit.json`

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
| risk_policy | pass_no_submit_quote_gate_block |
| fresh_quote | fail_scheduler_iex_quotes_stale_over_5_minutes_for_qqq_229.41_minutes_and_other_candidates_250.78_to_251.50_minutes |
| spread_within_after_hours_policy | fail_only_qqq_inside_0_25pct_but_stale_and_rest_spread_over_cap_or_bid_only |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## 주문 계획

- `market.session=after_hours`, `risk_inputs.after_hours_new_orders_submitted_today=0`, `session=after_hours`, `review_bucket=after_hours_validation`를 기록한 submit-mode order plan을 생성했다.
- review backlog는 `0/13/1`로 반영했다. 별도 after-hours 주문 예산은 열려 있었지만 모든 executable candidate가 fresh-quote 또는 spread/two-sided quote gate에서 차단돼 `orders=[]`로 유지했다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-09-0911-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-09-0911-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-09-0911-after-hours-autopilot.json` PASS with expected `orders is empty` warning

## Submit And Reconcile

- `place_stock_order`, `cancel_order_by_id`는 이번 cycle에서 호출하지 않았다.
- scheduler-owned `0911` core preflight 기준 신규 after-hours fill 없음, standing extended-hours order 없음, 포지션 수량 변화 없음.
