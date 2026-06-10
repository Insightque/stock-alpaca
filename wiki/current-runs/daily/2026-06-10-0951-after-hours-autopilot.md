# 2026-06-10-0951-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0951` core/research preflight를 우선 사용했다. Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours에서 expected nonblocking으로 처리했고, runtime Alpaca MCP cross-check로 account/positions/orders/watchlists/same-day duplicate/boats quote를 재확인했다. 다만 runtime `boats` quote 최신 시각도 `2026-06-10T00:38:42Z`~`00:40:22Z`에 머물러 current clock `2026-06-09T20:52:39.717814753-04:00` 대비 약 `12.3-13.9`분 stale였다. 따라서 fresh-quote hard gate가 실패했고 주문은 제출하지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-10-0951-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-10-0951-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight는 `first_blocking_gate=market_closed`만 regular-session blocker로 남겼다. after-hours run에서는 이것을 nonblocking으로 처리했고 runtime Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_account_activities`, `get_watchlists`, `get_asset`, `get_stock_quotes(feed=boats)`로 after-hours-required row를 다시 확인했다.

## Alpaca MCP 확인

- Regular market: closed (`get_clock.timestamp=2026-06-09T20:52:39.717814753-04:00`)
- Account/positions: runtime `get_account_info`, `get_all_positions` 기준 account `ACTIVE`, portfolio value `98,690.30 USD`, cash `31,951.54 USD`, buying power `299,276.47 USD`, positions `33`건이었다.
- Open orders / activities: runtime `get_orders(status=open)`는 `0`건, `get_orders(status=all, after=2026-06-09T20:00:00Z)`는 `0`건, `get_account_activities(activity_types=FILL, after=2026-06-09T20:00:00Z)`도 `0`건이었다. same-session after-hours submitted count는 `0/2`로 남았다.
- Duplicate context: runtime `get_orders(status=all, symbols=RGTI,AVGO, after=2026-06-09T00:00:00Z)` 기준 `RGTI`는 `2026-06-09T13:40:55Z` regular-session filled sell이 남아 same-day sell duplicate discipline이 유지됐다. `AVGO`는 same-day regular-session sell fill이 있었지만 이번 cycle에서는 stale/wide after-hours quote가 먼저 trim submit을 막았다.
- Quotes: runtime `boats` quote는 `QQQ`, `SPY`, `WMT`, `AVGO`, `RGTI`에 two-sided row를 제공했지만 freshest row도 모두 5분 cap을 초과했다. `SO`는 여전히 two-sided `boats` quote를 만들지 못했다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 우선 재평가했다. runtime `boats` quote `387.50/388.90`, spread 약 `0.3601%`로 after-hours spread cap `0.25%`를 넘었고, quote age도 약 `13.9`분 stale라 floor-size trim submit으로 승격하지 못했다.
- `RGTI` sell/trim: runtime `boats` quote `19.80/19.84`, spread 약 `0.2016%`였지만 same-day sell duplicate discipline과 약 `13.9`분 stale quote가 함께 남아 submit 후보가 되지 못했다.
- `QQQ`, `SPY`: spread는 각각 약 `0.0127%`, `0.0190%`로 양호했지만 1주 ask `706.58 USD`, `735.22 USD`가 after-hours per-order cap 약 `493.45 USD`를 초과했고 quote도 stale였다.
- `WMT`: runtime `boats` quote `118.88/119.42`가 잡혔지만 spread 약 `0.4522%`와 stale quote가 같이 남아 fallback buy 후보가 되지 못했다.
- `SO`: runtime `boats` quote 미존재와 trim metric gap이 동시에 남았다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0951-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0951-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-10-0951-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0951-after-hours-autopilot-post-trade.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_runtime_core_backfill_after_sparse_preflight |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | fail_no_eligible_order_survived_after_hours_freshness_caps |
| fresh_quote | fail_runtime_boats_quotes_stale_12_3_to_13_9_minutes |
| spread_within_after_hours_policy | mixed_pass_spread_not_enough_without_fresh_quotes |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-10-0951-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-10-0951-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-10-0951-after-hours-autopilot.json`
  - 결과: PASS (`orders is empty` warning only)

## Submit And Reconcile

- 이번 cycle에서는 `place_stock_order` 호출 직전까지 갈 수 있는 candidate가 없었다. 따라서 pre-submit gate summary 출력이나 submit/reconcile sequence는 실행하지 않았다.
- Post-trade reconciliation은 no-submit 기준으로만 수행했다. runtime Alpaca MCP cross-check는 closed market, ACTIVE account, positions `33`, open orders `0`, same-session orders `0`, same-session fills `0`, watchlists `0`를 재확인했다.
