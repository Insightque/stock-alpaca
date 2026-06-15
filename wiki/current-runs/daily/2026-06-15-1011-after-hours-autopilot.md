# 2026-06-15-1011-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1011` core/research preflight를 source-of-record로 유지했고 same-session after-hours continuity는 direct Alpaca MCP readback으로 보강했다. `0951` `AVGO` trim 1주는 이미 체결되어 sell-first duplicate-side risk가 생겼으므로, hard gate와 strict validator를 모두 통과한 `MSFT` 1주 buy fallback을 같은 `client_order_id`로 1회만 제출했다. immediate reconciliation 결과 same `client_order_id`는 `status=new` open order이며 아직 fill은 없다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-15-1011-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-15-1011-after-hours-autopilot-research-mcp-preflight.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-15-1011-after-hours-autopilot-runtime-alpaca-spot-check.json`
- `1011` Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Regular market: direct `get_clock`=`2026-06-14T21:18:47.61942745-04:00` 기준 closed였다.
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `101941.13 USD`, cash `32342.26 USD`, buying power `307001.68 USD`였다.
- Positions: direct `get_all_positions` 기준 positions `33`건이었고 immediate post-submit에도 `MSFT qty=2`, `qty_available=2`, `AVGO qty=3`, `qty_available=3`를 재확인했다.
- Open orders: direct `get_orders(status=open)` 기준 submit 후 `MSFT` open order `1`건이다.
- Same-session after-hours orders/fills: direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` 기준 `0951` `AVGO` trim fill `1`건과 이번 `1011` `MSFT` open order `1`건이 확인됐다. separate after-hours session budget은 이번 cycle submit 후 `2/2`가 됐다.
- Watchlists: direct `get_watchlists` 기준 `0`건이었다.

## 후보 평가

- `AVGO` sell/trim: `0951` `client_order_id=ah-20260615-0951-sell-avgo-01`이 `2026-06-15T01:02:13Z`에 `filled_avg_price=391.92 USD`로 이미 체결되어 same-day duplicate sell 리스크가 남았다. fresh quote는 양호했지만 이번 cycle submit 후보에서는 제외했다.
- `SO` sell/trim: overnight quote `88.06/96.14`, spread `8.7764%`로 hard gate fail이다.
- `MSFT` buy fallback: overnight latest quote `395.83/395.96`, spread `0.0328%`, quote age 약 `0.8`분, 1주 notional `395.96 USD`로 after-hours per-order cap 약 `509.71 USD` 아래다. existing actionable holding이며 review backlog add-block도 없다.
- `QQQ` / `SPY` / `SMH` / `MU`: 1주 notional이 after-hours cap을 초과한다.
- `INTC`: executable price는 가능하지만 same shortlist 내 existing-holding continuity와 source confidence에서 `MSFT`보다 뒤다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_submit_used_second_of_two_slots |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | pass_msft_0.8_minutes |
| spread_within_after_hours_policy | pass_msft_0.0328pct |
| whole_share_day_limit_extended_hours_order | pass_msft_buy_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_client_order_id_reconciled_open_new_lifecycle_recorded |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-15-1011-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-15-1011-after-hours-autopilot.json` -> PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-15-1011-after-hours-autopilot.json` -> PASS
  - non-blocking warning: `post-order cash 31946.30 remains above target maximum 10194.11; continue staged deployment on later runs when hard gates pass`

## Submit And Reconcile

- Submitted order: `MSFT` buy `1` share, `limit_price=395.96`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260615-1011-buy-msft-01`
- Alpaca MCP `place_stock_order` returned `order_id=76daf360-f7e6-443a-8af8-d61b4696267b`, initial `status=pending_new`.
- Immediate `get_order_by_client_id`와 `get_orders(status=all|open)` readback은 same `client_order_id`를 `status=new`, `filled_qty=0`로 재확인했다.
- `get_all_positions` cross-check에서는 `MSFT qty=2`, `qty_available=2`가 유지돼 아직 fill이 없음을 확인했다. `get_account_activities(...FILL...)`는 이번 `MSFT` submit에 대한 신규 fill을 아직 반환하지 않았다.
- policy `cancel_unfilled_after_minutes=5`는 후속 scheduler lifecycle에서 처리하도록 남기고, 이번 cycle은 no-retry open order lifecycle record로 종료한다. 다른 `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-15-1011-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-15-1011-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-15-1011-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-15-1011-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-15-1011-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade: `wiki/trade-ledger/positions/2026-06-15-1011-after-hours-autopilot-post-trade.json`
