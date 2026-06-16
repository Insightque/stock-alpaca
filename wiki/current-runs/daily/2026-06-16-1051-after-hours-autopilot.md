# 2026-06-16-1051-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1051` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca MCP continuity는 `overnight` feed에서 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE` fresh quote를 다시 확보했지만, sell-first 후보 `AVGO/RGTI/PFE`는 same-day duplicate sell discipline에 막혔고 buy fallback은 `review_backlog_pending_1d_count=18`, `blocked_add_symbols=['NOK']`, `QQQ/SPY/SMH` after-hours per-order cap 또는 spread cap, `MSFT` same-day duplicate buy, `TSLA` watch-only thesis 때문에 모두 차단돼 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-1051-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-1051-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1051-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `1051` preflight는 passing account/positions/open-order/asset/quote/snapshot/trade rows를 유지했고, direct continuity는 여기에 fresh overnight quote stack만 추가했다.

## Alpaca MCP 확인

- Regular market: closed. direct `get_clock.timestamp=2026-06-15T21:53:27.245765015-04:00`.
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `102285.31 USD`, cash `29836.36 USD`, buying power `305734.97 USD`였다.
- Positions / watchlists: direct `get_all_positions`, `get_watchlists` 기준 positions `33`건, watchlists `0`건이었다.
- Same-session after-hours orders: direct `get_orders(status=open)=0`, direct `get_orders(status=all, after=2026-06-15T20:00:00Z)=0`, direct `get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)=0`으로 확인돼 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다. regular validation count는 재사용하지 않았다.
- Quote boundary: direct `get_stock_latest_quote(feed=overnight)`는 `QQQ 741.96/742.06`, `RGTI 22.50/22.51`, `NOK 14.59/14.65`, `TSLA 404.79/405.21`, `SMH 641.68/643.31`, `SLB 53.64/54.07`, `AVGO 392.35/392.50`, `GE 336.42/342.31`, `SPY 753.12/753.59`, `MSFT 400.03/400.25`, `PFE 26.02/26.07`를 모두 5분 이내로 갱신했다. 다만 spread gate는 `AVGO/RGTI/MSFT/PFE/QQQ/SPY/TSLA`만 통과했고 `NOK/SLB/SMH/GE`는 after-hours cap을 넘었다.

## 후보 평가

- `AVGO`: overnight quote `392.35/392.50`, spread 약 `0.0382%`로 after-hours spread gate를 통과했지만 `2026-06-15 11:18 ET` regular-session trim fill 이후 `duplicate_symbol_side_same_day`가 남아 추가 sell이 차단됐다.
- `RGTI`: overnight quote `22.50/22.51`, spread 약 `0.0444%`로 execution quality는 회복됐지만 `2026-06-15 09:41 ET` same-day filled sell 9주가 남아 duplicate sell discipline이 유지됐다.
- `PFE`: repeated weak-review trim precedent는 유지됐고 overnight quote `26.02/26.07`, spread 약 `0.1920%`로 cap 안에 들어왔지만 `2026-06-15 15:59 ET` regular-session trim fill 때문에 추가 sell이 차단됐다.
- `MSFT`: overnight quote `400.03/400.25`, spread 약 `0.0550%`, 1주 ask `400.25 USD`로 execution quality는 충분했지만 `review_backlog_pending_1d_count=18`가 stop threshold를 넘고 same-day regular-session buy가 이미 있어 신규 buy path가 닫혔다.
- `NOK`: overnight quote `14.59/14.65`, 1주 notional은 cap 이내였지만 spread 약 `0.4104%`가 cap을 다시 넘었고 `review-due-index`의 `blocked_add_symbols=['NOK']`와 review backlog throttle이 신규 buy를 차단했다.
- `QQQ/SPY/SMH`: fresh benchmark/diversifier quote는 확보됐지만 1주 ask `742.06/753.59/643.31 USD`가 after-hours per-order cap 약 `511.43 USD`를 넘어 fallback buy가 열리지 않았다. `SMH`는 spread 약 `0.2537%`로 spread cap도 미세하게 재위반했다.
- `TSLA`: overnight quote `404.79/405.21`, spread 약 `0.1037%`, 1주 ask `405.21 USD`로 pure execution gate는 통과했지만 [[TSLA]]가 여전히 이벤트성 optionality를 이유로 `watchlist, 이번 주문 제외`를 유지해 executable fallback으로 승격되지 않았다.

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
| fresh_quote | pass_runtime_overnight_quotes_0_to_2_00_minutes_for_qqq_rgti_nok_tsla_smh_slb_avgo_ge_spy_msft_pfe |
| spread_within_after_hours_policy | pass_subset_avgo_rgti_msft_pfe_qqq_spy_tsla_but_fail_nok_slb_smh_ge |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_duplicate_sells_buy_backlog_or_watch_only_thesis |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었고 fresh overnight quote도 회복됐지만, 실행 가능한 sell은 duplicate discipline에 막히고 buy는 review backlog throttle, add-block, after-hours per-order cap, spread cap, TSLA watch-only thesis에 막혀 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 scheduler-owned preflight rows와 direct Alpaca MCP continuity check 기준 same-session after-hours orders `0`건, open orders `0`건, positions `33`건, watchlists `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1051-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1051-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-1051-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-1051-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-1051-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-1051-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1051-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-1051-after-hours-autopilot-post-trade.json`
