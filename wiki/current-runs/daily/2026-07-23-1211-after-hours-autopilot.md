# 2026-07-23-1211-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `2026-07-22 EDT`
- Scheduler file label used: `2026-07-23-1211` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1211` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca continuity는 이번 cycle에서 정상 응답했고 regular market closed, account `ACTIVE`, positions `31`, open orders `0`, same-session after-hours submitted/fills `1/1`를 재확인했다. live overnight quote supplement 기준 `NOK 10.78/10.80` spread `0.1852%`, `WMT 109.40/109.67` spread `0.2462%`가 executable이었지만 정책상 sell-first가 우선이므로 `NOK` 1주 trim `client_order_id=ah-20260722-1211-sell-nok-01`만 제출했고, same `client_order_id` reconciliation 기준 즉시 `filled_avg_price=10.78 USD`로 체결됐다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-1211-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-1211-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1211-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / research rows는 scheduler-owned `1211` Alpaca core preflight를 사용했다.
- Direct live continuity 기준 `2026-07-23T03:14:39.642027553Z` regular market closed, account `ACTIVE`, positions `31`, open orders `0`, watchlists `0`, same-session after-hours submitted/fills `1/1`였다.
- Recent activities에는 earlier `NOK` sell `1주`, `client_order_id=ah-20260722-0931-sell-nok-01`, `filled_avg_price=10.95 USD`가 유지됐고, 이번 cycle submit 후 `ah-20260722-1211-sell-nok-01`도 `2026-07-23T03:18:44.891868059Z`에 `filled_avg_price=10.78 USD`로 닫혔다.
- Post-trade focus는 `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=399`, `NOK qty_available=399`다.

## 후보 평가

- `NOK` sell/trim: live overnight quote `10.78/10.80`, spread `0.1852%`, freshness `5분 이하`, after-hours per-order cap PASS, qty_available `400`로 executable이었다.
- `WMT` buy fallback: live overnight quote `109.40/109.67`, spread `0.2462%`, freshness `5분 이하`, per-order notional cap PASS로 executable이었다.
- `SO` sell/trim: live overnight quote `94.62/95.65`, spread `1.0769%`로 spread cap fail이다.
- `MCD` buy fallback: live overnight quote `263.79/264.59`, spread `0.3024%`로 spread cap fail이다.
- `QQQ`, `SPY`, `SMH`, `GS`: spread는 일부 통과했지만 after-hours per-order cap fail이다.
- `NEE`, `CVX`: spread cap fail이다.

## Submit And Reconcile

- Pre-submit gate summary를 주문 직전에 기록했다. paper mode, session budget, universe/MCP/risk strict PASS, `NOK` live quote/spread PASS, open orders `0`, sell-first 우선 순위를 모두 명시했다.
- Submitted order: `NOK` sell `1주`, `limit_price=10.78 USD`, `extended_hours=true`, `time_in_force=day`, `client_order_id=ah-20260722-1211-sell-nok-01`
- Immediate reconciliation: same `client_order_id` 기준 `order_id=d249fed3-33a1-4b84-b84d-4902851737c9`, `status=filled`, `filled_qty=1`, `filled_avg_price=10.78 USD`, `filled_at=2026-07-23T03:18:44.891868059Z`
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-23-1211-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-1211-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-1211-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1211-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-1211-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1211-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1211-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-1211-after-hours-autopilot.json`
