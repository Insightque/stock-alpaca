# 2026-06-10-0931-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0931` core/research preflight를 우선 사용했다. Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours에서 expected nonblocking으로 처리했고, 누락된 account/positions/orders/asset/quote rows는 runtime Alpaca MCP로 보강했다. 다만 runtime `boats` quote의 freshest timestamp가 `2026-06-10T00:17:32Z`~`2026-06-10T00:18:36Z`에 머물러 current clock `2026-06-09T20:33:01.45157813-04:00` 대비 약 `17.8-18.9`분 stale였다. 따라서 fresh-quote hard gate가 실패했고 주문은 제출하지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-10-0931-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-10-0931-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight는 `mcp_coverage_hint.outcome=failed`, `gap_reason=market_closed did not pass`, `first_blocking_gate=market_closed`만 남긴 sparse artifact였다. after-hours run에서는 이것만으로 block하지 않고 runtime Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_account_activities`, `get_watchlists`, `get_asset`, `get_stock_quotes(feed=boats)`로 after-hours-required row를 보강했다.

## Alpaca MCP 확인

- Regular market: closed (`get_clock.timestamp=2026-06-09T20:33:01.45157813-04:00`)
- Account/positions: runtime `get_account_info`, `get_all_positions` 기준 account `ACTIVE`, portfolio value `98,794.61 USD`, cash `31,951.54 USD`, buying power `299,433.47 USD`, positions `33`건이었다.
- Open orders / activities: runtime `get_orders(status=open)`는 `0`건, `get_orders(status=all, after=2026-06-09T20:00:00Z)`는 `0`건, `get_account_activities(activity_types=FILL, after=2026-06-09T20:00:00Z)`도 `0`건이었다. same-session after-hours submitted count는 `0/2`로 남았다.
- Quotes: runtime `boats` quote는 `QQQ/SMH/SPY/JNJ/BA/AAPL/INTC/WMT/AVGO/RGTI`에서 two-sided row를 주었지만 freshest row가 모두 5분 cap을 초과했다. `SO`는 two-sided `boats` quote를 만들지 못했다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 우선 재평가했다. runtime `boats` quote `389.00/389.90`, spread `0.2311%`로 spread cap은 통과했지만 quote age가 약 `17.8`분 stale라 floor-size trim submit으로 승격하지 못했다.
- `RGTI` sell/trim: runtime `boats` quote `19.78/19.81`, spread `0.1515%`에도 불구하고 same-day sell duplicate discipline과 stale quote가 함께 남아 submit 후보가 되지 못했다.
- `QQQ`, `SPY`, `SMH`: `QQQ`와 `SPY`는 spread는 양호했지만 1주 ask가 after-hours per-order `0.5%` cap을 초과했다. `SMH`는 spread와 1주 ask 둘 다 부담이었다.
- `AAPL`, `INTC`, `WMT`: runtime `boats` spread는 각각 약 `0.0550%`, `0.0744%`, `0.2431%`로 cap 안에 들어왔지만 latest quote가 stale라 fresh-quote gate를 통과하지 못했다.
- `SO`: runtime `boats` quote 미존재와 trim metric gap이 동시에 남았다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0931-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0931-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-10-0931-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0931-after-hours-autopilot-post-trade.json`

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
| fresh_quote | fail_runtime_boats_quotes_stale_17_8_to_18_9_minutes |
| spread_within_after_hours_policy | mixed_pass_spread_not_enough_without_fresh_quotes |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-10-0931-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-10-0931-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-10-0931-after-hours-autopilot.json`
  - 결과: PASS (`orders is empty` warning only)

## Submit And Reconcile

- 이번 cycle에서는 `place_stock_order` 호출 직전까지 갈 수 있는 candidate가 없었다. 따라서 pre-submit gate summary 출력이나 submit/reconcile sequence는 실행하지 않았다.
- Post-trade reconciliation은 no-submit 기준으로만 수행했다. runtime Alpaca MCP cross-check는 closed market, ACTIVE account, positions `33`, open orders `0`, same-session orders `0`, same-session fills `0`, watchlists `0`를 재확인했다.
