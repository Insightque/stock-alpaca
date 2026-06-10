# 2026-06-11-0711-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0711` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 executable fresh two-sided quote stack이 끝내 만들어지지 않아 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-11-0711-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-11-0711-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/quote/spread rows는 그대로 사용했다. runtime Alpaca MCP는 `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-10T20:00:00Z)`, `get_watchlists` 교차 확인만 수행했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-10T18:12:55.4523646-04:00` runtime `get_clock`)
- Account/positions: scheduler-owned core preflight를 주 원천으로 사용했다. account `ACTIVE`, portfolio value `96705.97 USD`, cash `30865.37 USD`, buying power `292979.74 USD`, positions `33`건이다. runtime `get_account_info` 교차 확인은 portfolio value `96689.29 USD`, cash `30865.37 USD`, buying power `292955.57 USD`였다.
- Open orders: scheduler-owned `get_orders_open` 기준 `0`건이었고 runtime `get_orders(status=open)`도 `0`건이었다.
- Watchlists: scheduler-owned preflight broad universe는 유지했고 runtime `get_watchlists`는 `0`건이었다.
- Same-session after-hours orders: runtime `get_orders(status=all, after=2026-06-10T20:00:00Z)` 기준 신규 after-hours order는 `0`건이었다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap은 `0/2`다.

## 후보 평가

- `SPY`: scheduler-owned research shortlist benchmark였다. IEX quote `723.51/723.68`는 spread 약 `0.0235%`로 양호했지만 timestamp가 `2026-06-10T20:47:58.423956950Z`라 source-of-record cutoff 기준 약 `83.44`분 stale였고, 1주 ask `723.68 USD`도 after-hours per-order cap `483.53 USD`를 넘었다.
- `QQQ`: IEX quote `692.30/692.65`는 spread 약 `0.0505%`로 양호했지만 timestamp가 `2026-06-10T20:58:25.330349820Z`라 source-of-record cutoff 기준 약 `72.99`분 stale였고, 1주 ask `692.65 USD`도 per-order cap을 넘었다.
- `NOK`: IEX quote `13.38/13.40`는 spread `0.1493%`로 정상 범위였지만 timestamp가 `2026-06-10T20:01:00.056089762Z`라 약 `130.42`분 stale였다. 동시에 validation lifecycle의 `NOK` add-block도 유지됐다.
- `ORCL/IONQ/SMH/V/CRM`: shortlist에 남았지만 scheduler-owned IEX quote age가 `102.17-131.42`분 stale였고 spread도 `0.6810%-8.2521%` 수준으로 after-hours cap `0.25%`를 초과했다.
- `AVGO` sell/trim: sell side 허용 정책에 따라 held risk-trim을 우선 재평가했다. 그러나 scheduler-owned IEX quote는 age 약 `131.40`분 stale이고 spread `9.7937%`라 executable extended-hours trim order를 만들지 못했다.
- `RGTI/SO`: `RGTI`는 spread `13.7064%`가 과도했고, `SO`는 bid-only `85.84` quote와 two-sided quote 부재가 동시에 blocker였다.
- Review backlog: `review-due-index` 기준 `pending_1d_count=14`, `pending_5d_count=13`, `pending_20d_count=1`이었다. 이번 cycle은 backlog throttle 자체보다 fresh-quote/spread hard gate가 직접 차단 요인이었다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0711-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0711-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-11-0711-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0711-after-hours-autopilot-post-trade.json`

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
| risk_policy | fail_no_eligible_order_survived_after_hours_quote_freshness_and_notional_caps |
| fresh_quote | fail_scheduler_iex_quotes_stale_72_99_to_131_42_minutes |
| spread_within_after_hours_policy | fail_only_spy_qqq_nok_inside_0_25pct_but_not_executable |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## 주문 계획

- `market.session=after_hours`, `risk_inputs.after_hours_new_orders_submitted_today=0`, `session=after_hours`, `review_bucket=after_hours_validation`를 기록한 submit-mode order plan을 생성했다.
- review backlog는 `14/13/1`로 반영했다. 별도 after-hours 주문 예산은 열려 있었지만 모든 executable candidate가 fresh-quote, spread, two-sided quote, validation lifecycle, 또는 per-order notional cap gate에서 차단돼 `orders=[]`로 유지했다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-0711-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-0711-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-11-0711-after-hours-autopilot.json` PASS with `orders is empty` warning

## Submit And Reconcile

- `place_stock_order`, `cancel_order_by_id`는 이번 cycle에서 호출하지 않았다.
- scheduler-owned `0711` core preflight와 runtime Alpaca MCP cross-check 기준 신규 after-hours order/fill 없음, standing extended-hours order 없음, 포지션 수량 변화 없음.
