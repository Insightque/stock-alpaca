# 2026-06-10-1031-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1031` core/research preflight를 source-of-record로 사용했고 Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. runtime Alpaca MCP cross-check와 fresh `overnight` quote 재평가 결과 `AAPL` 1주 buy가 strict universe/MCP/risk gate와 after-hours quote/spread/notional cap을 모두 통과했고, `place_stock_order` 1회 제출 뒤 `client_order_id=ah-20260610-1031-aapl-buy-01` 기준 즉시 체결을 확인했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-10-1031-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-10-1031-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight는 `first_blocking_gate=market_closed`만 regular-session blocker로 남겼다. after-hours run에서는 이를 nonblocking으로 처리했고 runtime Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_account_activities`, `get_watchlists`, `get_asset`, `get_stock_quotes(feed=boats)`, `get_stock_latest_quote(feed=overnight)`로 submit boundary를 다시 확인했다.

## Alpaca MCP 확인

- Regular market: closed (`get_clock.timestamp=2026-06-09T21:35:15.188535451-04:00`)
- Account/positions: reconciliation 직후 `get_account_info`, `get_all_positions` 기준 account `ACTIVE`, portfolio value `98,845.90 USD`, cash `31,368.65 USD`, buying power `298,877.61 USD`, positions `33`건이었다. `AAPL`은 `4주 -> 5주`, `avg_entry_price=303.136`, `qty_available=5`로 증가했다.
- Open orders / activities: `get_orders(status=open, symbols=AAPL)`는 `0`건, `get_orders(status=all, symbols=AAPL, after=2026-06-10T01:34:30Z)`는 `ah-20260610-1031-aapl-buy-01` 1건을 반환했고, `get_account_activities(activity_types=FILL, after=2026-06-10T01:34:30Z)`는 같은 주문의 `filled_avg_price=291.49 USD` fill 1건을 반환했다.
- Watchlists: runtime `get_watchlists`는 `0`건이었다.

## 후보 평가

- 선택 주문 `AAPL` buy 1주: runtime `overnight` quote `291.48/291.54`, spread `0.0206%`, quote age 약 `0.0`분으로 after-hours quote/spread gate를 통과했고 1주 notional도 per-order cap 아래였다. AAPL은 scheduler shortlist 안의 existing actionable holding이며 wiki thesis와 review trail이 이미 존재했다.
- 제외 후보 `QQQ`, `SPY`, `SMH`: fresh and liquid였지만 1주 ask가 after-hours per-order 0.5% cap `494.05 USD`를 초과했다.
- 제외 후보 `AVGO` sell/trim: sell side 허용 정책에 따라 먼저 재평가했지만 fresh overnight spread가 after-hours cap `0.25%`를 넘었다.
- 제외 후보 `RGTI` sell/trim: fresh overnight quote와 spread는 통과했지만 `2026-06-09` regular-session filled sell로 same-day duplicate discipline이 유지됐다.
- 제외 후보 `WMT`, `BA`, `JNJ`: fresh quote는 있었지만 spread가 after-hours cap을 넘었다.
- 제외 후보 `INTC`: spread `0.2330%`로 cap 안이었지만 shortlist 내 우선순위와 liquidity quality가 `AAPL`보다 낮았다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_runtime_core_backfill_after_sparse_preflight |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_one_remaining_then_exhausted |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass |
| fresh_quote | pass_runtime_overnight_quote_under_5_minutes |
| spread_within_after_hours_policy | pass_runtime_overnight_spread_0_0206pct |
| whole_share_day_limit_extended_hours_order | pass |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_reconciled_filled_by_client_order_id |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-10-1031-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-10-1031-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-10-1031-after-hours-autopilot.json`
  - 결과: PASS
  - 경고: `post-order cash 31368.60 remains above target maximum 9881.07; continue staged deployment on later runs when hard gates pass`

## Submit And Reconcile

- Pre-submit gate summary를 남긴 뒤 `place_stock_order`를 정확히 1회 호출했다.
- 제출 파라미터: `AAPL` / `buy` / `qty=1` / `limit_price=291.54` / `time_in_force=day` / `extended_hours=true` / `client_order_id=ah-20260610-1031-aapl-buy-01`
- Reconciliation: `get_order_by_client_id(client_order_id=ah-20260610-1031-aapl-buy-01)`와 `get_orders(status=all, symbols=AAPL, after=2026-06-10T01:34:30Z)`에서 동일 `client_order_id` 주문을 찾아 `order_id=49e4052f-3e00-44ad-9296-4d1c41033e01`, `status=filled`, `filled_qty=1`, `filled_avg_price=291.49 USD`, `filled_at=2026-06-10T01:35:02.497251991Z`를 확인했다.
- 추가 취소나 다른 `client_order_id` 재시도는 수행하지 않았다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-1031-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-1031-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-10-1031-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-1031-after-hours-autopilot-post-trade.json`
