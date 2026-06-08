# 2026-06-08-0931-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0931` core/research preflight를 우선 사용했지만 core preflight는 regular-market-closed clock row만 남기고 account/positions/orders/quote gate row가 비어 있었다. 이 sparse preflight는 장외 세션에서 blocking으로 승격하지 않고, runtime Alpaca MCP가 required core evidence를 보강했다. strict universe/MCP/risk gate와 separate after-hours budget `1/2`를 통과한 뒤, buy backlog throttle을 피할 수 있는 허용 sell side에서 `AVGO` 1주 trim을 선택했다. runtime `overnight` quote `392.73/392.78`, spread `0.012731%`, quote age `0.06`분 기준으로 장외 quote/spread cap을 통과했고, Alpaca MCP `place_stock_order`는 `AVGO` 1주 sell을 생성한 뒤 same client id reconciliation에서 `392.80 USD` 체결로 닫혔다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-08-0931-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-08-0931-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight는 `first_blocking_gate`를 남기지 않았지만 clock row만 기록한 sparse artifact였다. after-hours run에서는 이것만으로 block하지 않고 runtime Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_account_activities`, `get_asset`, `get_stock_latest_quote(feed=overnight)`로 required core rows를 보강했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-07T20:31:08.388870633-04:00` scheduler-owned clock, runtime `get_clock`도 `2026-06-07T20:35:36.957789009-04:00` 기준 closed)
- Account/positions: runtime `get_account_info`, `get_all_positions` 기준 pre-submit account `ACTIVE`, portfolio value `98,976.70 USD`, cash `30,339.06 USD`, buying power `296,723.86 USD`, positions `33`건이었다. 체결 후 account는 cash `30,731.86 USD`, buying power `297,347.98 USD`, portfolio value `99,043.85 USD`로 갱신됐고 `AVGO` 보유수량은 `11주 -> 10주`로 줄었다.
- Open orders / activities: pre-submit runtime `get_orders(status=open)`는 `0`건이었고 after-hours submitted count는 `1/2`였다. submit 후 `get_order_by_client_id`, `get_orders(status=all, symbols=AVGO, after=2026-06-08T00:00:00Z)`, `get_account_activities(activity_types=FILL, after=2026-06-08T00:00:00Z)`가 동일 `client_order_id=ah-20260608-0931-sell-avgo`, `order_id=1fcbc469-1e8e-466f-9881-4b5538eecef1`, `filled_avg_price=392.80`, `filled_at=2026-06-08T00:37:53.182189418Z`를 확인했다. post-trade open AVGO order는 `0`건이다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 우선 재평가했다. `2026-06-08` portfolio review는 `validation add 실패 + core thesis 완전 폐기 아님`과 `post-earnings risk watch`를 유지했고, `0911` after-hours trim 이후에도 추가 floor-size de-risking 근거가 남아 있었다. runtime `overnight` quote `392.73/392.78`, spread `0.012731%`, quote age `0.06`분, `AVGO` asset active/tradable/overnight_tradable, trim 후 보유 `10주` 유지 조건을 모두 만족해 floor-size 1주 trim으로 승격했다.
- `QQQ`, `SPY`: overnight quote quality는 양호했지만 1주 ask가 after-hours per-order `0.5%` cap을 초과했다.
- `GOOGL`, `PFE`, `XOM`: buy fallback 후보로는 유효했지만 review backlog throttle이 새 after-hours buy를 차단했고, 이번 cycle은 allowed sell side `AVGO` trim이 우선이었다.
- `BAC`, `WMT`: overnight spread가 after-hours cap `0.25%`를 넘었다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-08-0931-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-08-0931-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-08-0931-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-08-0931-after-hours-autopilot-post-trade.json`
- Deterministic submit artifact: `wiki/evidence-store/sources/2026-06-08-0931-after-hours-autopilot-deterministic-submit.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_runtime_core_backfill_after_sparse_preflight |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_one_of_two_submitted |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass_sell_trim_candidate_ready |
| fresh_quote | pass |
| spread_within_after_hours_policy | pass |
| whole_share_day_limit_extended_hours_order | pass_avgo_sell_order_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_reconciled_filled |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-08-0931-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-08-0931-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-08-0931-after-hours-autopilot.json`
  - 결과: PASS

## Submit And Reconcile

- Pre-submit gate summary: `session=after_hours`, paper mode true, regular market closed, strict universe/MCP/risk PASS, separate after-hours budget `1/2`, selected order `AVGO sell 1 @ 392.73 day limit extended_hours=true`, runtime overnight quote `392.73/392.78`.
- `place_stock_order`는 `client_order_id=ah-20260608-0931-sell-avgo`로 호출했다. 다른 client id로 재시도하지 않았다.
- Same client id reconciliation 기준 주문은 `filled`로 닫혔고 `filled_avg_price=392.80 USD`, `filled_qty=1`이었다.
- Post-trade `get_orders(status=open, symbols=AVGO)`는 빈 결과였고, `get_all_positions` 기준 AVGO 보유수량은 `10주`로 감소했다.
