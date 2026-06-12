# 2026-06-12-1711-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1711` core/research preflight를 우선 사용했다. `1711` Alpaca core preflight는 expected `first_blocking_gate=market_closed`를 남겼지만 account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade passing rows도 함께 제공했다. after-hours run에서는 `market_closed`를 expected nonblocking으로 처리했고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id`로 same-session fill과 open-order continuity만 재확인했다. same-session after-hours filled orders가 여전히 `PFE`, `AVGO` 두 건으로 유지되어 separate session budget `2/2`가 계속 닫혀 있었고, 이번 cycle은 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-12-1711-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-12-1711-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight는 regular-session 기준 `market_closed`를 첫 blocker로 기록했지만, after-hours required rows인 account/positions/open orders/account activities/watchlists/asset/quote/snapshot/trade는 pass 상태로 제공했다. 이번 run은 그 passing rows를 source-of-record로 사용했고, runtime Alpaca MCP readback은 same-session fill ledger와 open-order continuity 확인에만 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`get_clock.timestamp=2026-06-12T04:12:26.672809028-04:00`)
- Account/positions: runtime `get_account_info`, `get_all_positions` 기준 account `ACTIVE`, portfolio value `99,719.74 USD`, cash `31,698.25 USD`, buying power `301,066.49 USD`, positions `33`건이었다.
- Open orders / same-session fills: `get_orders(status=open)`는 `0`건, `get_orders(status=all, after=2026-06-11T20:00:00Z)`는 same-session after-hours filled sell `2`건을 반환했다.
- Reconciled fills:
  - `ah-20260612-1011-sell-pfe-01` -> `filled_avg_price=26.13 USD`
  - `ah-20260612-1411-sell-avgo-01` -> `filled_avg_price=387.06 USD`
- Watchlists: runtime `get_watchlists`는 `0`건이었다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_plus_runtime_reconciliation |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | block_after_hours_session_budget_exhausted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | not_actionable_budget_exhausted_before_submit_path |
| spread_within_after_hours_policy | not_actionable_budget_exhausted_before_submit_path |
| whole_share_day_limit_extended_hours_order | not_applicable_no_order |
| immediate_reconcile_and_cancel_or_lifecycle_record | not_applicable_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `after_hours_new_orders_submitted_today=2`로 `after_hours_policy.max_new_orders_per_session=2`에 도달한 상태를 유지해 1711 submit path 진입 전에 차단됐다.
- 이번 cycle의 reconciliation은 scheduler-owned 1711 preflight passing rows와 runtime Alpaca MCP readback을 함께 사용해 earlier same-session fills `PFE`, `AVGO` 두 건의 exact readback 유지 여부와 positions/open-orders continuity 확인에 집중했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-12-1711-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-12-1711-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-12-1711-after-hours-autopilot.json`
  - 결과: PASS
  - 경고: `orders is empty`

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-12-1711-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-12-1711-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-12-1711-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-12-1711-after-hours-autopilot-post-trade.json`
