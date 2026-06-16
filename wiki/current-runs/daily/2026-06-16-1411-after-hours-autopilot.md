# 2026-06-16-1411-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1411` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca MCP continuity는 `overnight` feed에서 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE` quote를 재확인했다. 하지만 `AVGO`는 spread+duplicate sell, `RGTI/PFE`는 duplicate sell, `MSFT/NOK`는 review backlog/add discipline, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `SLB/GE`는 freshness/spread fail 때문에 executable after-hours order가 남지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-1411-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-1411-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1411-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `1411` preflight는 passing account/positions/open-order/asset/quote/snapshot/trade rows를 유지했고, direct continuity는 여기에 refreshed overnight quote stack만 추가했다.

## Alpaca MCP 확인

- Regular market: closed. direct `get_clock.timestamp=2026-06-16T01:13:04.723701774-04:00`.
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `102408.34 USD`, cash `29836.36 USD`, buying power `306011.92 USD`였다.
- Positions / watchlists: direct `get_all_positions` 기준 positions `33`건을 재확인했고, watchlists `0`건은 direct `get_watchlists`와 scheduler-owned core preflight row가 일치했다.
- Same-session after-hours orders: direct `get_orders(status=open)=0`, direct `get_orders(status=all, after=2026-06-15T20:00:00Z)=0`, scheduler-owned core preflight `orders_submitted=0`을 함께 사용해 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다. regular validation count는 재사용하지 않았다.
- Quote boundary: direct `get_stock_latest_quote(feed=overnight)` 기준 `QQQ 742.50/742.63`, `RGTI 22.63/22.68`, `NOK 14.68/14.71`, `TSLA 403.95/404.52`, `SMH 644.85/645.88`, `SLB 53.78/54.04`, `AVGO 391.93/393.58`, `GE 340.50/349.07`, `SPY 753.69/754.90`, `MSFT 399.14/399.26`, `PFE 26.00/26.03`를 재확인했다. freshness는 `SLB` 약 `9.75`분, `GE` 약 `12.58`분 stale였고 나머지는 `0.00-0.58`분 범위였다.

## 후보 평가

- `AVGO`: overnight quote `391.93/393.58`, spread 약 `0.4201%`로 after-hours cap을 넘었고 `2026-06-15 11:18 ET` regular-session trim fill 이후 `duplicate_symbol_side_same_day`도 남아 추가 sell이 차단됐다.
- `RGTI`: overnight quote `22.63/22.68`, spread 약 `0.2207%`는 cap 이내지만 `2026-06-15 09:41 ET` same-cycle filled sell 9주에 따른 duplicate sell discipline이 계속 남아 추가 trim이 차단됐다.
- `PFE`: repeated weak-review trim precedent는 유지됐고 overnight quote `26.00/26.03`, spread 약 `0.1153%`도 cap 이내지만 `2026-06-15 15:59 ET` regular-session trim fill 때문에 추가 sell이 차단됐다.
- `MSFT`: overnight quote `399.14/399.26`, spread 약 `0.0301%`, 1주 ask `399.26 USD`로 execution quality는 충분했지만 `review_backlog_pending_1d_count=18`가 stop threshold를 넘어 신규 buy path가 닫혔다.
- `NOK`: overnight quote `14.68/14.71`, 1주 notional은 cap 이내였고 spread도 `0.2042%`로 cap 안에 있었지만 `review-due-index`의 `blocked_add_symbols=['NOK']`와 review backlog throttle이 신규 buy를 차단했다.
- `QQQ/SPY/SMH`: fresh benchmark/diversifier quote는 확보됐지만 1주 ask `742.63/754.90/645.88 USD`가 after-hours per-order cap 약 `512.04 USD`를 넘어 fallback buy가 열리지 않았다.
- `TSLA`: overnight quote `403.95/404.52`, spread 약 `0.1410%`, 1주 ask `404.52 USD`로 pure execution gate는 통과했지만 [[TSLA]]가 여전히 watch-only event optionality note를 유지해 executable fallback으로 승격되지 않았다.
- `SLB/GE`: `SLB`는 freshness 약 `9.75`분 stale와 spread 약 `0.4823%`를 동시에 위반했고, `GE`는 freshness 약 `12.58`분 stale와 spread 약 `2.4856%`가 계속 fail이었다.

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
| fresh_quote | pass_runtime_overnight_quotes_0_00_to_0_58_minutes_for_avgo_msft_nok_pfe_qqq_rgti_smh_spy_tsla_and_fail_slb_9_75m_ge_12_58m |
| spread_within_after_hours_policy | pass_subset_msft_nok_pfe_qqq_rgti_smh_spy_tsla_and_fail_avgo_ge_slb |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_duplicate_sells_buy_backlog_add_block_watch_only_or_notional_or_quote_spread_or_freshness_caps |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었고 fresh overnight quote도 확보됐지만, 실행 가능한 sell은 duplicate discipline 또는 spread cap에 막히고 buy는 review backlog throttle, add-block, after-hours per-order cap, watch-only thesis, freshness/spread fail에 막혀 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 scheduler-owned preflight rows와 direct Alpaca MCP continuity check 기준 same-session after-hours orders `0`건, fills `0`건, open orders `0`건, positions `33`건, watchlists `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1411-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1411-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-1411-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-1411-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-1411-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-1411-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1411-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-1411-after-hours-autopilot-post-trade.json`
