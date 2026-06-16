# 2026-06-16-0931-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0931` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca MCP continuity는 `overnight` feed에서 `QQQ/MSFT/NOK/PFE/AVGO/TSLA/SPY/SMH` fresh quote를 회복했지만, sell-first 후보 `AVGO/RGTI/PFE`는 same-day duplicate sell discipline 또는 spread cap에 막혔고 buy fallback은 `review_backlog_pending_1d_count=18`, `blocked_add_symbols=['NOK']`, `SPY/QQQ/SMH` after-hours per-order cap, `MSFT` same-day duplicate buy 때문에 모두 차단돼 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-0931-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-0931-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-0931-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `0931` preflight는 passing account/positions/open-order/asset/quote/snapshot/trade rows를 유지했고, direct continuity는 여기에 fresh overnight quote stack만 추가했다.

## Alpaca MCP 확인

- Regular market: closed. direct `get_clock.timestamp=2026-06-15T20:33:31.978999582-04:00`.
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `102338.12 USD`, cash `29836.36 USD`, buying power `305927.86 USD`였다.
- Positions / watchlists: direct `get_all_positions`, `get_watchlists` 기준 positions `33`건, watchlists `0`건이었다.
- Same-session after-hours orders: direct `get_orders(status=open)=0`, direct `get_orders(status=all, after=2026-06-15T20:00:00Z)=0`으로 확인돼 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다. regular validation count는 재사용하지 않았다.
- Quote boundary: direct `get_stock_latest_quote(feed=overnight)`는 `QQQ 743.32/743.50`, `MSFT 399.38/400.16`, `NOK 14.59/14.61`, `PFE 26.05/26.06`, `AVGO 392.62/393.15`, `TSLA 406.76/406.88`, `SPY 754.54/755.01`, `SMH 645.60/646.02`를 모두 5분 이내로 갱신했다. 반면 `RGTI/SLB/GE`는 spread cap `0.25%`를 넘었다.

## 후보 평가

- `AVGO`: overnight quote `392.62/393.15`, spread 약 `0.1349%`로 after-hours spread gate는 PASS였지만 `2026-06-15 11:18 ET` regular-session trim fill 이후 `duplicate_symbol_side_same_day`가 남아 추가 sell이 차단됐다.
- `RGTI`: overnight quote `22.56/22.64`, spread 약 `0.3540%`로 cap 초과였고 `2026-06-15 09:41 ET` same-day filled sell 9주도 남아 있었다.
- `PFE`: repeated weak-review trim precedent는 유지됐고 overnight quote `26.05/26.06`, spread 약 `0.0384%`로 cap 안에 들어왔지만 `2026-06-15 15:59 ET` regular-session trim fill 때문에 추가 sell이 차단됐다.
- `MSFT`: overnight quote `399.38/400.16`, spread 약 `0.1951%`, 1주 ask `400.16 USD`로 execution quality는 충분했지만 `review_backlog_pending_1d_count=18`가 stop threshold를 넘고 same-day regular-session buy가 이미 있어 신규 buy path가 닫혔다.
- `NOK`: overnight quote `14.59/14.61`, spread 약 `0.1370%`, 1주 notional도 cap 이내였지만 `review-due-index`의 `blocked_add_symbols=['NOK']`와 review backlog throttle이 신규 buy를 차단했다.
- `QQQ/SPY/SMH`: fresh benchmark/diversifier quote는 확보됐지만 1주 ask `743.50/755.01/646.02 USD`가 after-hours per-order cap 약 `511.69 USD`를 넘어 fallback buy가 열리지 않았다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_plus_runtime_overnight_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with expected `orders is empty` warning |
| fresh_quote | pass_runtime_overnight_quotes_0_to_1_74_minutes |
| spread_within_after_hours_policy | pass_subset_avgo_msft_nok_pfe_qqq_smh_spy_tsla_but_fail_rgti_slb_ge |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_duplicate_sells_or_buy_backlog |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었고 fresh overnight quote도 회복됐지만, 실행 가능한 sell은 same-day duplicate 규율에 막히고 buy는 review backlog throttle 및 add-block에 막혀 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 scheduler-owned preflight rows와 direct Alpaca MCP continuity check 기준 same-session after-hours orders `0`건, open orders `0`건, positions `33`건, watchlists `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-0931-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-0931-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-0931-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-0931-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-0931-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-0931-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-0931-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-0931-after-hours-autopilot-post-trade.json`
