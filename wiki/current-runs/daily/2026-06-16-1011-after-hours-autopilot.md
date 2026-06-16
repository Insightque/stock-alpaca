# 2026-06-16-1011-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1011` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca MCP continuity는 `overnight` feed에서 `QQQ/RGTI/NOK/TSLA/SMH/AVGO/SPY/MSFT/PFE` fresh quote를 다시 확보했지만, sell-first 후보 `AVGO/RGTI/PFE`는 same-day duplicate sell discipline에 막혔고 buy fallback은 `review_backlog_pending_1d_count=18`, `blocked_add_symbols=['NOK']`, `QQQ/SPY/SMH` after-hours per-order cap, `MSFT` same-day duplicate buy 때문에 모두 차단돼 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-1011-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-1011-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1011-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `1011` preflight는 passing account/positions/open-order/asset/quote/snapshot/trade rows를 유지했고, direct continuity는 여기에 fresh overnight quote stack만 추가했다.

## Alpaca MCP 확인

- Regular market: closed. direct `get_clock.timestamp=2026-06-15T21:13:06.292872166-04:00`.
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `102117.86 USD`, cash `29836.36 USD`, buying power `305378.67 USD`였다.
- Positions / watchlists: direct `get_all_positions`, `get_watchlists` 기준 positions `33`건, watchlists `0`건이었다.
- Same-session after-hours orders: direct `get_orders(status=open)=0`, direct `get_orders(status=all, after=2026-06-15T20:00:00Z)=0`으로 확인돼 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다. regular validation count는 재사용하지 않았다.
- Quote boundary: direct `get_stock_snapshot(feed=overnight)`는 `QQQ 741.62/742.05`, `RGTI 22.29/22.37`, `TSLA 404.59/405.21`, `SMH 640.27/641.54`, `AVGO 391.36/392.02`, `SPY 752.72/753.55`, `MSFT 399.85/400.17`, `PFE 26.00/26.04`, `NOK 14.52/14.54`를 모두 5분 이내로 갱신했다. 다만 `SLB/GE`는 stale+wide spread로 submit boundary를 충족하지 못했고 `RGTI`는 direct continuity quote 기준 spread 약 `0.3582%`로 after-hours cap을 다시 넘었다.

## 후보 평가

- `AVGO`: overnight quote `391.36/392.02`, spread 약 `0.1684%`로 after-hours spread gate는 PASS였지만 `2026-06-15 11:18 ET` regular-session trim fill 이후 `duplicate_symbol_side_same_day`가 남아 추가 sell이 차단됐다.
- `RGTI`: overnight quote `22.29/22.37`는 freshness를 통과했지만 `2026-06-15 09:41 ET` same-day filled sell 9주가 남아 duplicate sell discipline이 첫 blocker였다. 이번 direct quote spread 약 `0.3582%`도 after-hours cap을 다시 넘었다.
- `PFE`: repeated weak-review trim precedent는 유지됐고 overnight quote `26.00/26.04`, spread 약 `0.1537%`로 cap 안에 들어왔지만 `2026-06-15 15:59 ET` regular-session trim fill 때문에 추가 sell이 차단됐다.
- `MSFT`: overnight quote `399.85/400.17`, spread 약 `0.0800%`, 1주 ask `400.17 USD`로 execution quality는 충분했지만 `review_backlog_pending_1d_count=18`가 stop threshold를 넘고 same-day regular-session buy가 이미 있어 신규 buy path가 닫혔다.
- `NOK`: overnight quote `14.52/14.54`, spread 약 `0.1376%`, 1주 notional은 cap 이내였지만 `review-due-index`의 `blocked_add_symbols=['NOK']`와 review backlog throttle이 신규 buy를 차단했다.
- `QQQ/SPY/SMH`: fresh benchmark/diversifier quote는 확보됐지만 1주 ask `742.05/753.55/641.54 USD`가 after-hours per-order cap 약 `510.59 USD`를 넘어 fallback buy가 열리지 않았다.

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
| fresh_quote | pass_runtime_overnight_quotes_0_to_0_50_minutes_for_qqq_rgti_nok_tsla_smh_avgo_spy_msft_pfe_but_fail_slb_ge |
| spread_within_after_hours_policy | pass_subset_avgo_msft_nok_pfe_qqq_smh_spy_tsla_but_fail_rgti_slb_ge |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_duplicate_sells_or_buy_backlog |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었고 fresh overnight quote도 회복됐지만, 실행 가능한 sell은 same-day duplicate 규율에 막히고 buy는 review backlog throttle, add-block, after-hours per-order cap에 막혀 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 scheduler-owned preflight rows와 direct Alpaca MCP continuity check 기준 same-session after-hours orders `0`건, open orders `0`건, positions `33`건, watchlists `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1011-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1011-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-1011-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-1011-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-1011-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-1011-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1011-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-1011-after-hours-autopilot-post-trade.json`
