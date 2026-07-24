# 2026-07-24-2151-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Thursday, July 23, 2026 EDT`
- Scheduler file label used: `2026-07-24-2151-` (`Asia/Seoul` next-day file label; actual market date anchor for this run is `Thursday, July 23, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned future-labeled KST artifact path `2026-07-24-2151-` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 `2026-07-24-2151-` preflight는 passing account/positions/open-orders/asset/quote/spread rows와 `orders_submitted=0`을 제공했다. 이번 cycle에서는 같은 source-of-record quote row에서 `NOK`가 `9.67/9.68`, spread `0.1034%`, quote age 약 `1.22분`으로 submit boundary를 통과했고 same-session after-hours submitted/fills가 `0/0`이어서 sell-first floor-size trim 경로가 열렸다. Alpaca는 `client_order_id=ah-20260723-2151-sell-nok-01`를 수락했고 immediate reconciliation 기준 `status=new`, `filled_qty=0`이다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-24-2151-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-24-2151-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-24-2151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote / spread rows는 scheduler-owned future-labeled KST artifact path `2026-07-24-2151-` Alpaca core preflight를 사용했다.
- Source-of-record preflight 기준 account `ACTIVE`, positions `31`, watchlists `0`, open orders `0`, `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=399`, `NOK qty_available=399`였다.
- submit/reconcile 직후 Alpaca MCP 기준 open orders `1`, same-session after-hours fills `0`, `NOK qty_available=398`로 갱신됐다.
- source-of-record account snapshot은 `status=ACTIVE`, `cash=29027.11 USD`, `portfolio_value=97495.93 USD`, `buying_power=297006.96 USD`였다. submit quote는 같은 preflight row의 `NOK bid/ask = 9.67/9.68`, spread `0.1034%`, quote timestamp `2026-07-24T12:50:16.605683908Z`다.

## 후보 평가

- `NOK` sell/trim: source-of-record quote `9.67/9.68`, spread `0.1034%`, quote age 약 `1.22분`으로 after-hours freshness/spread cap을 통과했다. `[[NOK]]`와 `[[2026-07-23-portfolio-review]]`는 same US-date prior trim follow-through가 양호했고 residual `399주` 포지션이 평균단가 `15.044561 USD` 대비 깊은 손실 구간임을 기록하고 있어 sell-first floor-size trim 근거가 충분했다.
- `SO` sell/trim: source-of-record quote age stale + spread `9.5099%`로 executable sell gate fail이다.
- `QQQ`: source-of-record quote는 fresh지만 1주 ask 기준 `after_hours_policy.max_notional_pct_per_order=0.005` cap를 넘는다.
- `WMT`와 `MCD`는 source-of-record quote가 one-sided이고 stale이다.
- `SPY/SMH/NEE/CVX/GS`는 source-of-record 기준 stale + spread 또는 cap fail, `NOK` buy fallback은 `blocked_add_symbol_review_queue`로 executable after-hours buy path를 만들지 못했다.

## Submit And Reconcile

- Pre-submit gate summary: paper mode / `market_closed_expected_nonblocking_after_hours` / universe strict PASS / MCP strict PASS / risk PASS / `NOK` quote freshness PASS / spread PASS / whole-share day limit extended-hours order shape PASS를 확인한 뒤 submit했다.
- Submitted order this cycle: `NOK` sell `1` share, `limit_price=9.67`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260723-2151-sell-nok-01`
- Immediate reconciliation: Alpaca MCP `get_orders(status=all, after=2026-07-23T20:00:00Z)` 기준 `order_id=e91d0b66-f1b4-49a1-bcd8-7c2283132857`, `status=new`, `filled_qty=0`, `filled_avg_price=null`, `expires_at=2026-07-25T00:00:00Z`였다.
- Same-session fills: `get_account_activities(activity_types=[FILL], after=2026-07-23T20:00:00Z)` 기준 신규 fill 없음.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-24-2151-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-24-2151-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-24-2151-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-24-2151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-24-2151-after-hours-autopilot-post-trade.json`
- Prompt: `wiki/evidence-store/sources/2026-07-24-2151-after-hours-autopilot-prompt.txt`

## Validators

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-24-2151-after-hours-autopilot.json` -> PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-24-2151-after-hours-autopilot.json` -> PASS
- `PYTHONPATH=/private/tmp/yamlshim python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-24-2151-after-hours-autopilot.json` -> PASS
