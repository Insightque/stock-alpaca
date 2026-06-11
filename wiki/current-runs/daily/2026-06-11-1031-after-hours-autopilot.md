# 2026-06-11-1031-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1031` core/research preflight를 source-of-record로 사용했고 Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)` cross-check 기준 regular market은 계속 closed였고, `ah-20260611-1011-sell-rgti`가 `2026-06-11T01:20:06.981355496Z`에 `19.78 USD`로 이미 체결돼 same-session after-hours budget이 `2/2`로 닫힌 상태가 재확인됐다. 따라서 이번 `1031` cycle은 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-11-1031-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-11-1031-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight는 `first_blocking_gate=market_closed`만 regular-session blocker로 남겼다. after-hours run에서는 이를 nonblocking으로 처리했고 scheduler-owned clock/account/position/open-order rows를 유지했다.

## Alpaca MCP 확인

- Regular market: scheduler preflight 기준 closed (`timestamp=2026-06-10T21:31:09.849568244-04:00`, `next_open=2026-06-11T09:30:00-04:00`); runtime Alpaca MCP `get_clock`도 `timestamp=2026-06-10T21:33:17.486485602-04:00`로 여전히 closed였다.
- Account/positions: runtime `get_account_info/get_all_positions` cross-check에서는 account `ACTIVE`, portfolio value `97,637.81 USD`, cash `30,904.65 USD`, buying power `295,422.18 USD`, positions `33`건이 유지됐다. `RGTI`는 `49주`, `qty_available=49`, `avg_entry_price=25.569583 USD`로 확인됐다.
- Open orders / same-session orders / watchlists: runtime `get_orders(status=open)`는 `0`건, `get_orders(status=all, after=2026-06-10T20:00:00Z)`는 `ah-20260611-1011-sell-rgti`, `ah-20260611-0951-sell-rgti` 두 건의 `filled` record만 남겼고 `get_watchlists`도 `0`건이었다.

## 후보 평가

- `ORCL` buy fallback: runtime overnight quote `181.15/181.29`, spread 약 `0.0772%`, 1주 ask `181.29 USD`로 freshness/spread/notional/asset gate를 모두 통과한 최상위 executable buy fallback이었지만, separate after-hours session budget이 이미 `2/2`라 submit path에 진입하지 못했다.
- `IONQ` buy fallback: runtime overnight quote `57.37/57.51`, spread 약 `0.2434%`로 hard gate를 가까스로 통과했지만 speculative 우선순위와 session budget block 때문에 후순위로 남았다.
- `AVGO` sell/trim: runtime overnight quote `375.02/376.06`, spread 약 `0.2765%`로 after-hours cap `0.25%`를 다시 넘겨 탈락했다.
- `RGTI` sell/trim: `0951`, `1011` same-session trim 두 건이 모두 filled로 닫혔고 runtime overnight quote `19.79/19.85`의 spread도 약 `0.3023%`로 cap을 넘겨 추가 sell candidate가 되지 못했다.
- `SPY`/`QQQ`: spread와 freshness는 양호했지만 1주 ask가 각각 `728.50 USD`, `698.31 USD`로 after-hours per-order cap 약 `488.19 USD`를 초과했다.
- `SO`: runtime overnight quote `85.01/95.05`는 stale + asymmetric 상태라 executable two-sided trim order를 만들지 못했다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_runtime_core_and_scheduler_preflight |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | block_after_hours_session_budget_exhausted |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass_empty_order_plan |
| fresh_quote | pass_runtime_overnight_quotes_fresh_for_orcl_ionq_qqq_spy_avgo_rgti |
| spread_within_after_hours_policy | mixed_runtime_screen_orcl_ionq_qqq_spy_pass_avgo_rgti_nok_so_smh_v_fail |
| whole_share_day_limit_extended_hours_order | not_applicable_no_order_due_budget_block |
| immediate_reconcile_and_cancel_or_lifecycle_record | not_applicable_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `after_hours_new_orders_submitted_today=2`로 `after_hours_policy.max_new_orders_per_session=2`에 도달해 submit path 진입 전에 차단됐다. regular validation count는 재사용하지 않았고, `risk_inputs.after_hours_new_orders_submitted_today`만 별도 세션 예산 근거로 사용했다.
- Reconciliation은 기존 same-session client order id `ah-20260611-0951-sell-rgti`, `ah-20260611-1011-sell-rgti`가 모두 filled 상태임을 확인하는 용도로 수행했다. 이 과정에서 `1011` fill이 `19.78 USD`로 닫혔고 `RGTI` 보유수량이 `50주 -> 49주`로 감소한 상태를 current portfolio에 반영했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-1031-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-1031-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-11-1031-after-hours-autopilot.json`
  - 결과: PASS
  - 경고: `orders is empty`

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-1031-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-1031-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-11-1031-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-1031-after-hours-autopilot-post-trade.json`
