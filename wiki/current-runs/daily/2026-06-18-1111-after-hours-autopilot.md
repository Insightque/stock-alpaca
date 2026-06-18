# 2026-06-18-1111-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1111` Alpaca core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca overnight continuity로 stale `iex` 대신 fresh overnight quote path를 복구했고, strict universe/MCP/risk gate가 모두 `PASS`해 `PFE` 1주 after-hours trim sell을 제출했다. immediate reconciliation 기준 `client_order_id=ah-20260618-1111-sell-pfe-01`은 `status=new` open order이며 fill은 아직 없다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-18-1111-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-18-1111-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1111-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1111-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1111-after-hours-autopilot-post-trade.json`

## Alpaca MCP 확인

- Regular market: closed (`get_clock.timestamp=2026-06-17T22:13:21.122450966-04:00`), after-hours workflow 계속 진행
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `101055.97 USD -> 101090.32 USD`, cash `28003.45 USD`, buying power `300836.23 USD -> 300921.15 USD`
- Positions / watchlists: direct `get_all_positions` 기준 positions `34`, `PFE qty=2`, submit 직후 `qty_available=1`; direct `get_watchlists` 기준 watchlists `0`
- Orders / fills: submit 전 open orders `0`, same-session after-hours orders `0`; submit 후 `get_order_by_client_id`와 `get_orders(status=open)` 기준 `PFE` trim 1건이 `status=new` open order로 확인됐고 same-session fill은 아직 `0`

## 후보 평가

- `PFE` sell/trim 선택: direct overnight quote `25.97/25.98`, spread `0.0385%`, quote age `5분 이하`, held qty `2`, same-session duplicate `0`, open orders `0`. repeated weak-review defensive holding trim rationale를 유지해 floor-size trim으로 선택했다.
- `RGTI` sell/trim 대안: direct overnight quote `20.72/20.76`, spread 약 `0.193%`, freshness 통과. residual speculative sleeve de-risking rationale는 유효했지만 이번 cycle은 defensive weak-review trim 표본을 우선했다.
- `AVGO` sell/trim 보류: spread/freshness는 통과했지만 잔여 `1주`라 `keep_minimum_remaining_qty` 해석을 유지했다.
- `QQQ` buy fallback 차단: direct overnight quote `733.27/733.55`, spread는 양호했지만 1주 ask notional이 after-hours per-order cap을 넘었다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_reused_plus_live_overnight_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted_before_submit |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | PASS |
| spread_within_after_hours_policy | PASS |
| whole_share_day_limit_extended_hours_order | PASS |
| immediate_reconcile_and_cancel_or_lifecycle_record | PASS_open_order_lifecycle_recorded_by_client_order_id |

## Submit And Reconcile

- Pre-submit gate summary 후 `mcp__alpaca.place_stock_order`로 `PFE` 1주 sell을 제출했다.
- 주문 파라미터: `type=limit`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `limit_price=25.97`, `client_order_id=ah-20260618-1111-sell-pfe-01`
- Immediate reconciliation: `get_order_by_client_id` 기준 `order_id=d3b37f0b-4efa-406a-994f-432ae6b8b8a0`, `status=new`, `filled_qty=0`, `filled_avg_price=null`
- Retry discipline: 다른 `client_order_id`로 재시도하지 않았다. 이번 cycle은 open-order lifecycle 기록으로 종료한다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1111-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1111-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-18-1111-after-hours-autopilot.json` PASS

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-18-1111-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-1111-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-1111-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1111-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1111-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1111-after-hours-autopilot-post-trade.json`
