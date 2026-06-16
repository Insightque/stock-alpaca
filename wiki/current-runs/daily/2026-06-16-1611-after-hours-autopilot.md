# 2026-06-16-1611-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1611` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca MCP continuity는 `overnight` feed에서 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE` quote stack을 2026-06-16 16:12 KST에 재확인했다. 하지만 `AVGO/RGTI/PFE` sell-first 후보는 same-day duplicate discipline에 막혔고, buy fallback은 `review_backlog_pending_1d_count=18`, `blocked_add_symbols=['NOK']`, `QQQ/SPY/SMH` after-hours per-order cap, `MSFT` same-day duplicate buy, `TSLA` watch-only thesis, `SLB/GE/NOK` spread cap 때문에 executable after-hours order가 남지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-1611-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-1611-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1611-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `1611` preflight는 passing account/positions/open-order/quote rows를 유지했고, direct continuity는 여기에 refreshed overnight quote stack만 추가했다.

## Alpaca MCP 확인

- Regular market: closed. direct `get_clock.timestamp=2026-06-16T03:12:43.178044132-04:00`.
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `102510.24 USD`, cash `29836.36 USD`, buying power `306038.35 USD`였다.
- Positions / watchlists: direct `get_all_positions` 기준 positions `33`건을 유지했고, direct `get_watchlists` 기준 watchlists `0`건이었다.
- Same-session after-hours orders: direct `get_orders(status=open)=0`, direct `get_orders(status=all, after=2026-06-15T20:00:00Z)=0`, direct `get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)=0` 기준 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다. regular validation count는 재사용하지 않았다.
- Duplicate discipline cross-check: direct `get_orders(status=all, after=2026-06-15T13:30:00Z, symbols=AVGO,RGTI,PFE,MSFT,NOK,QQQ,SPY,SMH,TSLA,SLB,GE)` 기준 `RGTI` sell fill `2026-06-15 09:41 ET`, `AVGO` sell fill `11:18 ET`, `PFE` sell fill `15:59 ET`, `MSFT` buy fill `14:39 ET`, `SLB` buy fill `12:41 ET`가 확인됐다.
- Quote boundary: direct `get_stock_latest_quote(feed=overnight)` / `get_stock_snapshot(feed=overnight)` 기준 `QQQ 742.46/743.24`, `RGTI 22.68/22.70`, `NOK 14.91/14.95`, `TSLA 405.67/405.81`, `SMH 644.05/645.62`, `SLB 53.50/54.03`, `AVGO 392.67/393.13`, `GE 340.61/344.19`, `SPY 753.96/754.02`, `MSFT 399.86/400.34`, `PFE 26.03/26.06`를 재확인했다. freshness는 모두 5분 cap 안이었고, spread cap `0.25%`는 `AVGO/MSFT/PFE/QQQ/RGTI/SMH/SPY/TSLA`에서 PASS였지만 `GE/NOK/SLB`에서는 FAIL이었다.

## 후보 평가

- `AVGO`: overnight quote `392.67/393.13`, spread 약 `0.1171%`로 after-hours cap 안이었지만 `2026-06-15 11:18 ET` regular-session trim fill 이후 `duplicate_symbol_side_same_day`가 남아 추가 sell이 차단됐다.
- `RGTI`: overnight quote `22.68/22.70`, spread 약 `0.0882%`로 cap 안이었지만 `2026-06-15 09:41 ET` filled sell에 따른 duplicate sell discipline이 계속 남았다.
- `PFE`: repeated weak-review trim precedent는 유지됐고 overnight quote `26.03/26.06`, spread 약 `0.1152%`도 cap 안이었지만 `2026-06-15 15:59 ET` regular-session trim fill 때문에 추가 sell이 차단됐다.
- `MSFT`: overnight quote `399.86/400.34`, spread 약 `0.1200%`, 1주 ask `400.34 USD`로 execution quality는 충분했지만 `review_backlog_pending_1d_count=18`가 stop threshold를 넘고 same-day regular-session buy가 이미 있어 신규 buy path가 닫혔다.
- `NOK`: overnight quote `14.91/14.95`, 1주 notional은 cap 이내였지만 `review-due-index`의 `blocked_add_symbols=['NOK']`, review backlog throttle, spread 약 `0.2680%` cap 초과가 동시에 남아 신규 buy를 차단했다.
- `QQQ/SPY/SMH`: fresh benchmark/diversifier quote는 확보됐지만 1주 ask `743.24/754.02/645.62 USD`가 after-hours per-order cap 약 `512.55 USD`를 넘어 fallback buy가 열리지 않았다.
- `TSLA`: overnight quote `405.67/405.81`, spread 약 `0.0345%`, 1주 ask `405.81 USD`로 pure execution gate는 통과했지만 [[TSLA]]가 여전히 watch-only event optionality note를 유지해 executable fallback으로 승격되지 않았다.
- `SLB/GE`: freshness는 회복됐지만 `SLB` spread 약 `0.9854%`, `GE` spread 약 `1.0456%`가 계속 fail이었다.

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
| fresh_quote | pass for all shortlisted symbols |
| spread_within_after_hours_policy | pass for `AVGO/MSFT/PFE/QQQ/RGTI/SMH/SPY/TSLA`, fail for `GE/NOK/SLB` |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_duplicate_sells_buy_backlog_add_block_watch_only_or_notional_or_quote_spread_caps |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었고 fresh overnight quote도 다수 확보됐지만, 실행 가능한 sell은 duplicate discipline에 막히고 buy는 review backlog throttle, add-block, after-hours per-order cap, watch-only thesis, spread cap 때문에 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 scheduler-owned preflight rows와 direct Alpaca MCP continuity check 기준 same-session after-hours orders `0`건, open orders `0`건, positions `33`건, watchlists `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1611-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1611-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-1611-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-1611-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-1611-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-1611-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1611-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-1611-after-hours-autopilot-post-trade.json`
