# 2026-06-09-2151-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2151` core/research preflight를 우선 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만, fresh two-sided under-cap quote를 가진 후보는 `NOK` 1건뿐이었고 이 후보도 pending 20D validation review로 add exposure가 차단돼 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-09-2151-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-09-2151-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/quote/spread rows는 그대로 사용했다. runtime Alpaca MCP cross-check는 closed market, ACTIVE account, positions `32`, open orders `0`, watchlists `0`, same-session orders `0`을 재확인했다. 다만 source of record는 scheduler-owned `2151` preflight의 account/positions/open-order/asset/quote/spread rows로 유지했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-09T08:51:08.987896458-04:00`)
- Account/positions: scheduler-owned core preflight를 주 원천으로 사용했다. account `ACTIVE`, portfolio value `100692.27 USD`, cash `31774.83 USD`, buying power `303409.27 USD`, positions `32`건이다.
- Open orders: scheduler-owned `get_orders_open` 기준 `0`건이었다.
- Watchlists: scheduler-owned Alpaca MCP `get_watchlists` 기준 `0`건이었다.
- Same-session after-hours orders: 이번 cycle은 `place_stock_order` 호출이 없었고 `client_order_id`도 생성되지 않았다. deterministic submit path도 `orders=[]`로 `status=no_orders`를 기록한다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap은 `0/2`다.

## 후보 평가

- `NOK`: scheduler-owned IEX quote `14.79/14.80`는 age 약 `0.05`분, spread 약 `0.0676%`, 1주 ask `14.80 USD`로 after-hours quote/spread/notional gate를 통과했다. 그러나 `review-due-index`에서 `NOK`는 pending 20D validation review 때문에 add-block 상태여서 floor-size fallback buy를 만들지 않았다.
- `QQQ`: scheduler-owned research shortlist의 강한 fallback benchmark였지만 IEX quote `722.64/722.74`가 spread 약 `0.0138%`로 양호해도 decision clock 기준 age 약 `13.46`분으로 stale였고 1주 ask `722.74 USD`도 after-hours per-order cap 약 `503.46 USD`를 넘었다.
- `SPY`: scheduler-owned IEX quote `743.08/743.16`는 spread 약 `0.0108%`로 양호했지만 age 약 `13.47`분으로 5분 cap을 넘었고 1주 ask `743.16 USD`도 after-hours per-order cap 약 `503.46 USD`를 넘었다.
- `AVGO` sell/trim: sell side 허용 정책에 따라 우선 재평가했다. 그러나 scheduler-owned IEX quote는 bid-only `374.07`이고 timestamp `2026-06-08T20:00:02.048843518Z`로 약 `1011.45`분 stale였다.
- `PFE/BAC/RGTI`: IEX quote가 bid-only라 two-sided extended-hours order shape를 만들 수 없었다.
- `NVDA/NKE/ADBE/SMH/XOM`: research shortlist 또는 held fallback 후보였지만 previous-session quote age와 각각 `8.1632%`, `8.3871%`, `8.6932%`, `6.0522%`, `7.1875%` spread로 after-hours cap `0.25%`를 크게 초과했다.
- Review backlog: `review-due-index` 기준 `pending_1d_count=0`, `pending_5d_count=13`, `pending_20d_count=1`였다. 이번 cycle은 backlog throttle 전체가 아니라 `NOK`의 symbol-specific add block과 나머지 후보의 quote freshness/spread 제약이 직접 차단 요인이었다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-09-2151-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-09-2151-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-09-2151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-09-2151-after-hours-autopilot-post-trade.json`
- Deterministic submit artifact: `wiki/evidence-store/sources/2026-06-09-2151-after-hours-autopilot-deterministic-submit.json`

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
| risk_policy | fail_no_eligible_order_survived_notional_freshness_and_validation_lifecycle |
| fresh_quote | fail_only_nok_was_fresh_0_03_minutes_while_qqq_spy_were_13_44_13_46_minutes_and_others_were_previous_session_quotes |
| spread_within_after_hours_policy | pass_nok_qqq_spy_two_sided_but_only_nok_was_fresh_and_under_cap |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## 주문 및 제출

- 제출 전 요약: 실행 가능한 after-hours 후보군이 없었다. `NOK`만 fresh two-sided under-cap quote를 가졌지만 pending 20D validation review로 add-block 상태였다. `QQQ/SPY`는 spread는 양호해도 stale이며 1주 ask가 after-hours per-order cap을 넘었고, `AVGO/PFE/BAC/RGTI`는 bid-only였으며 나머지 후보는 stale 또는 spread cap 초과였다.
- `place_stock_order`: 호출하지 않음
- `cancel_order_by_id`: 호출하지 않음
- 결정적 제출 경로: `scripts/submit-validated-order-plan-mcp.py --execute`는 `orders=[]` plan으로 실행되고 `wiki/evidence-store/sources/2026-06-09-2151-after-hours-autopilot-deterministic-submit.json`에 `status=no_orders`를 기록한다.

## Reconciliation

- Submit attempted: 아니오
- Open orders after run: `0`
- Same-session new fills detected: `0`
- Position delta: `none`
- Source of record: scheduler-owned core preflight `get_orders_open`, `get_account_activities(activity_types=FILL)`, `get_all_positions`, `get_watchlists`; 이번 cycle은 after-hours-required row가 모두 preflight에 포함되어 있어 추가 runtime Alpaca MCP retry가 필요하지 않았다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-09-2151-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-09-2151-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-09-2151-after-hours-autopilot.json`: PASS (`orders is empty` warning only)
- `PATH=/usr/local/bin:$PATH python3 scripts/submit-validated-order-plan-mcp.py --run-id 2026-06-09-2151-after-hours-autopilot --order-plan wiki/trade-ledger/orders/2026-06-09-2151-after-hours-autopilot.json --output-json wiki/evidence-store/sources/2026-06-09-2151-after-hours-autopilot-deterministic-submit.json --execute`: completed with `status=no_orders`
