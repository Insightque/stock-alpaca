# 2026-06-18-1351-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1351` Alpaca core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live Alpaca continuity에서는 same-session prior after-hours trim `ah-20260618-1111-sell-pfe-01`, `ah-20260618-1131-sell-rgti-01`가 모두 filled이고 open orders `0`임을 재확인했다. live overnight quote continuity에서는 `WMT`, `QQQ`, `NVDA`, `TSLA`, `GOOGL`, `JPM`, `SPY`, `MSFT`가 fresh였지만 separate after-hours submitted orders가 이미 `2/2`라 이번 cycle 신규 submit은 없었다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-18-1351-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-18-1351-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1351-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1351-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1351-after-hours-autopilot-post-trade.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했고, 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary source-of-record로 유지했다.

## Alpaca MCP 확인

- Regular market: closed (`live get_clock.timestamp=2026-06-18T00:52:48.077864202-04:00`), after-hours workflow 계속 진행
- Account: source-of-record preflight 기준 account `ACTIVE`, cash `28050.17 USD`, portfolio value `100847.24 USD`, buying power `300364.13 USD`; live `get_account_info` continuity는 `portfolio_value=100831.08 USD`, `buying_power=300318.88 USD`로 소폭 drift만 확인했다.
- Positions / watchlists: live `get_all_positions` 기준 positions `34`, `get_watchlists` 기준 watchlists `0`
- Orders / fills: live `get_orders(status=open)` 기준 open after-hours order는 `0`건이다. live `get_orders(status=all, after=2026-06-17T20:00:00-04:00)` 및 `get_account_activities(activity_types=[FILL])`, `get_order_by_client_id` readback 기준 same-session after-hours submitted orders는 `PFE`, `RGTI` 총 `2건`, fills도 `2건`이다.
- Quote continuity: live overnight quote path에서 `WMT`는 `118.20/118.37`, spread 약 `0.1437%`, age 약 `4.72분`으로 after-hours quote/spread cap을 통과했다. 반면 `PFE`는 spread 약 `0.3080%`, `RGTI`는 약 `0.2900%`, `AVGO`는 약 `0.2897%`, `MS`는 약 `2.9495%`로 spread gate를 다시 넘지 못했다.

## 후보 평가

- `RGTI` sell/trim: live overnight quote `20.66/20.72`, spread 약 `0.2900%`로 after-hours spread cap을 다시 초과했고, `client_order_id=ah-20260618-1131-sell-rgti-01`가 이미 filled라 same-session budget도 더 이상 남지 않았다.
- `PFE` sell/trim: live overnight quote `25.93/26.01`, spread 약 `0.3080%`로 after-hours spread cap을 초과했고 prior trim으로 잔여 수량이 `1주`라 `keep_minimum_remaining_qty`에도 막혔다.
- `AVGO` sell/trim: live overnight quote `399.82/400.98`, spread 약 `0.2897%`로 after-hours spread cap을 초과했고 잔여 수량 `1주` 때문에 `keep_minimum_remaining_qty`도 충돌했다.
- `WMT` 1주 buy fallback: live overnight quote `118.20/118.37`, spread 약 `0.1437%`로 fresh-quote/spread/per-order-cap 경로는 열렸지만 separate after-hours session budget이 이미 `2/2`였다.
- `QQQ` buy fallback: live spread는 양호했지만 1주 ask `731.48 USD`가 after-hours per-order cap 약 `504.24 USD`를 초과했다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_reused_and_live_order_reconciliation_confirmed |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | FAIL `2/2` |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS (warning `orders is empty`) |
| fresh_quote | PASS live overnight quotes remained fresh for `WMT/QQQ/NVDA/TSLA/GOOGL/JPM/SPY/MSFT` |
| spread_within_after_hours_policy | PASS executable `WMT` quote existed but budget stayed primary blocker |
| whole_share_day_limit_extended_hours_order | pass_no_new_order_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | PASS_client_order_ids_reconciled_without_retry |

## Submit And Reconcile

- 이번 cycle에서는 `place_stock_order`를 호출하지 않았다. separate after-hours submitted order count가 이미 `2/2`였기 때문이다.
- alternate `client_order_id` retry나 `cancel_order_by_id` 호출도 없었다. 두 after-hours `client_order_id` 모두 체결 상태로 reconciliation이 끝났고 다른 `client_order_id`를 새로 만들지 않았다.
- `get_order_by_client_id(ah-20260618-1111-sell-pfe-01)` 기준 `PFE` trim은 `filled_avg_price=25.97 USD`, `filled_at=2026-06-18T02:58:29.784751618Z`로 체결 완료다.
- `get_order_by_client_id(ah-20260618-1131-sell-rgti-01)` 기준 `RGTI` trim은 `filled_avg_price=20.75 USD`, `filled_at=2026-06-18T03:31:57.099382354Z`로 체결 완료다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1351-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1351-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-18-1351-after-hours-autopilot.json` PASS (warning `orders is empty`)

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-18-1351-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-1351-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-1351-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1351-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1351-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1351-after-hours-autopilot-post-trade.json`
