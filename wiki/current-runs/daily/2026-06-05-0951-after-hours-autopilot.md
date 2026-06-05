# 2026-06-05-0951-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0951` core/research preflight는 strict universe/MCP gate를 유지했고, runtime Alpaca MCP는 `QQQ` quote freshness를 회복시켰다. 그러나 `QQQ` 1주 ask가 장외 per-order cap을 넘고 나머지 후보는 stale/wide quote에 머물러 주문 제출 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-05-0951-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-05-0951-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태로, 단독 차단 사유로 보지 않았다. 같은 preflight의 account, positions, open_orders, asset, latest_quote, snapshot, latest_trade pass row를 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-04T20:51:10.793970778-04:00`)
- Account/positions: scheduler-owned Alpaca core preflight `get_account_info/get_all_positions` 기준 `ACTIVE`, positions `33`건을 유지했다. runtime Alpaca MCP `get_all_positions` 보조 확인에서도 신규 fill이나 수량 변화는 없었다.
- Open orders: scheduler-owned core preflight `get_orders(status=open)` 결과 `0`건. 이번 cycle은 submit boundary까지 가지 못했으므로 장외 `ah-` prefix 신규 주문도 생성되지 않았다.
- After-hours session order count: `risk_inputs.after_hours_new_orders_submitted_today=0`; 정규장 validation order count는 재사용하지 않았다.
- Submit/reconcile: candidate gate failure로 `place_stock_order`를 호출하지 않았다.

## 후보 평가

- `QQQ`: runtime Alpaca MCP latest quote 기준 quote age `3.04`분, spread `0.0122%`로 quote/spread gate는 통과했다. 하지만 1주 ask `738.73 USD`가 장외 per-order cap `510.52 USD`를 넘어서 floor-size buy 생성 불가.
- `PFE`: quote age `51.16`분, spread `5.5955%`로 quote/spread gate 실패.
- `SMH`: quote age `51.18`분, spread `5.9019%`, ask `650.82 USD`로 spread/notional gate 동시 실패.
- `JNJ`: regular close race로 취소된 뒤 장외 fallback diversifier로 다시 봤지만 scheduler quote row 기준 stale `51.18`분, spread `10.6582%`라 재진입 불가.
- `AVGO` sell/trim: sell side 허용 정책에 따라 재평가했지만 `review-due-index`의 due-review blocking discipline이 남아 있고, latest quote도 stale `51.18`분과 spread `9.9199%`라 실제 장외 trim으로 승격하지 못했다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0951-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0951-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-05-0951-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0951-after-hours-autopilot-post-trade.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_with_market_closed_expected_nonblocking |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | block |
| fresh_quote | block |
| spread_within_after_hours_policy | block |
| whole_share_day_limit_extended_hours_order | not_applicable_no_orders |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit_attempt |

## Validators

- Universe strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-05-0951-after-hours-autopilot.json`)
- MCP strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-05-0951-after-hours-autopilot.json`)
- Risk policy: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-05-0951-after-hours-autopilot.json`); warning: `orders is empty`

## Submit/Reconcile

- Pre-submit gate summary: not written because no candidate survived the after-hours hard gates to a `place_stock_order` call boundary.
- Submitted through Alpaca MCP only: not applicable this run.
- Reconciled by `client_order_id`: not applicable because submit was skipped.
- No alternate client order id was introduced.
