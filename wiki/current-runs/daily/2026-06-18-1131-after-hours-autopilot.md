# 2026-06-18-1131-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1131` Alpaca core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca overnight continuity로 fresh spread path를 다시 열어 `RGTI` 1주 after-hours trim sell을 제출했다. immediate reconciliation 기준 새 `client_order_id=ah-20260618-1131-sell-rgti-01`과 기존 `ah-20260618-1111-sell-pfe-01`은 모두 `status=new` open order이며 same-session after-hours session budget은 `2/2`가 됐다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-18-1131-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-18-1131-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1131-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1131-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1131-after-hours-autopilot-post-trade.json`

## Alpaca MCP 확인

- Regular market: closed (`scheduler preflight clock.timestamp=2026-06-17T22:40:05-04:00`), after-hours workflow 계속 진행
- Account: direct `get_account_info` 기준 account `ACTIVE`, cash `28003.45 USD`, portfolio value `101135.95 USD`, buying power `301037.66 USD`
- Positions / watchlists: direct `get_all_positions` 기준 positions `34`, `RGTI qty=27 -> qty_available=26`, `PFE qty=2 -> qty_available=1`; direct `get_watchlists` source-of-record는 `0`
- Orders: direct `get_orders(status=open)`와 `get_orders(status=all, after=2026-06-17T20:00:00-04:00)` 기준 open after-hours sell 2건이 확인됐다. `RGTI` 새 주문과 `PFE` 기존 주문 모두 `status=new`, `filled_qty=0`이다.

## 후보 평가

- `RGTI` sell/trim 선택: direct overnight quote `20.74/20.76`, spread 약 `0.0964%`, quote age 약 `0.15`분, held qty `27`, same-session `RGTI` duplicate `0`, open `RGTI` orders `0`. residual speculative sleeve staged de-risking rationale를 유지해 floor-size trim으로 선택했다.
- `PFE` sell/trim 보류: direct overnight quote `25.97/26.02`, spread 약 `0.1924%`로 executable이지만 same-session open sell `ah-20260618-1111-sell-pfe-01`이 아직 살아 있어 same-symbol 추가 trim을 막았다.
- `AVGO` sell/trim 보류: direct overnight quote `402.82/403.06`, spread 약 `0.0596%`로 정상화됐지만 잔여 `1주`라 `keep_minimum_remaining_qty` 해석을 유지했다.
- `QQQ` buy fallback 차단: direct overnight quote `732.73/733.20`, spread는 양호했지만 1주 ask notional이 after-hours per-order cap을 넘고 review backlog throttle도 buy를 열지 않았다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_reused_plus_live_overnight_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_one_of_two_submitted_before_submit |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | PASS |
| spread_within_after_hours_policy | PASS |
| whole_share_day_limit_extended_hours_order | PASS |
| immediate_reconcile_and_cancel_or_lifecycle_record | PASS_open_order_lifecycle_recorded_by_client_order_id |

## Submit And Reconcile

- Pre-submit gate summary 후 `mcp__alpaca.place_stock_order`로 `RGTI` 1주 sell을 제출했다.
- 주문 파라미터: `type=limit`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `limit_price=20.74`, `client_order_id=ah-20260618-1131-sell-rgti-01`
- Immediate reconciliation: `get_order_by_client_id` 기준 `order_id=896febc8-8857-4dcb-9f8f-ea082e740a15`, `status=new`, `filled_qty=0`, `filled_avg_price=null`
- Open-order state: same reconciliation 시점에 prior `PFE` trim `client_order_id=ah-20260618-1111-sell-pfe-01`도 계속 `status=new`로 남아 있다. after-hours session 신규 주문 수는 `2/2`가 되어 이번 session budget은 닫혔다.
- Retry discipline: 다른 `client_order_id`로 재시도하지 않았다. `cancel_unfilled_after_minutes` 후속 lifecycle은 다음 scheduler cycle에서 추적한다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1131-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1131-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-18-1131-after-hours-autopilot.json` PASS

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-18-1131-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-1131-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-1131-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1131-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1131-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1131-after-hours-autopilot-post-trade.json`
