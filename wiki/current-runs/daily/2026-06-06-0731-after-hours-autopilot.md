# 2026-06-06-0731-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0731` core/research preflight를 우선 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. runtime Alpaca MCP `get_stock_latest_quote(feed=iex)`, `get_stock_latest_quote(feed=overnight)`, `get_stock_snapshot(feed=iex)` 교차 확인 기준 separate after-hours order budget은 `0/2`로 남아 있었지만, executable two-sided quote freshness/spread gate를 만족한 후보가 없어 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-06-0731-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-06-0731-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/quote rows는 그대로 사용했다. runtime Alpaca MCP는 execution boundary에서 quote freshness, spread, quote completeness, overnight fallback, BOATS subscription availability만 재확인했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-05T18:31:07.009059321-04:00`)
- Account/positions: scheduler-owned `0731` core preflight 기준 account `ACTIVE`, portfolio value `97,951.40 USD`, cash `29,947.81 USD`, buying power `293,953.95 USD`, long market value `68,003.59 USD`, positions `33`건이다.
- Open orders: scheduler-owned `0731` core preflight `get_orders(status=open)` 기준 open order `0`건.
- After-hours session order count: runtime submit은 없었고 이번 cycle에서 `ah-` prefix 또는 `extended_hours=true` 주문을 새로 만들지 않았다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=0`이다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 우선 재평가했다. 그러나 runtime IEX quote는 `bid=386.40`, `ask` 없음, timestamp `2026-06-05T20:00:55.167085571Z`로 약 `152.90`분 stale였고, 같은 날 regular-session trim fill이 이미 있었다. `2026-06-05-portfolio-review`는 아직 catalyst-risk alert와 due-review discipline 단계라 두 번째 장외 trim을 강제하지 않았다.
- `QQQ`: 가장 강한 fallback benchmark였다. runtime IEX quote `700.15/700.26`는 spread 약 `0.0157%`로 양호했지만 timestamp가 `2026-06-05T20:48:07.458456075Z`라 2026-06-06 07:33 KST runtime check 기준 약 `105.69`분 stale였다. `overnight` feed도 `2026-06-05T08:00:00.406190958Z` stale quote만 반환했고 `boats`는 subscription 403이라 hard gate를 열지 못했다.
- `SMH`: runtime IEX quote `557.43/588.52`, quote age 약 `153.82`분, spread 약 `5.4261%`로 장외 fresh-quote/spread cap을 동시에 위반했다.
- `SPY`: runtime IEX quote `714.79/759.97`, quote age 약 `153.82`분, spread 약 `6.1271%`, 1주 ask `759.97 USD`로 quote freshness/spread/per-order-cap을 동시에 위반했다.
- `WMT`: runtime IEX quote `114.76/124.61`, quote age 약 `153.80`분, spread 약 `8.2299%`로 장외 fresh-quote/spread cap을 동시에 위반했다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0731-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0731-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-06-0731-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0731-after-hours-autopilot-post-trade.json`

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
| fresh_quote | fail_runtime_iex_and_overnight_quotes_stale_over_5_minutes_for_qqq_smh_spy_avgo_pfe_wmt_so_bac_xom_googl_tsla |
| spread_within_after_hours_policy | fail_runtime_iex_spread_cap_or_missing_ask_and_boats_unavailable_for_smh_spy_avgo_pfe_wmt_so_bac_xom_googl_tsla |
| whole_share_day_limit_extended_hours_order | pass_candidate_shape_confirmed_but_not_executed |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit_reconciled_by_preflight_and_runtime_quote_snapshot |

## 주문 계획

- `market.session=after_hours`, `risk_inputs.after_hours_new_orders_submitted_today=0`를 기록한 submit-mode order plan을 생성했다.
- review backlog는 `13/0/1`로 반영했다. after-hours 정책 run당 주문 cap은 열려 있었지만 어떤 후보도 fresh-quote gate를 넘지 못했다.
- after-hours budget은 열려 있었지만 fresh-quote/spread hard gate가 닫혀 `orders=[]`로 유지했다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-06-0731-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-06-0731-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-06-0731-after-hours-autopilot.json`

## Submit And Reconcile

- `place_stock_order`, `cancel_order_by_id`는 이번 cycle에서 호출하지 않았다. `boats` feed는 subscription 403이라 보조 확인만 실패로 기록했고, 실행 게이트는 runtime `iex`와 `overnight` quote completeness/freshness로 판단했다.
- scheduler-owned `0731` core preflight와 runtime quote/snapshot cross-check 기준 신규 after-hours fill 없음, standing extended-hours order 없음, 포지션 수량 변화 없음.
