# 2026-06-17-1351-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1351` core/research preflight를 source-of-record로 사용했다. Alpaca core의 regular-session `market_closed`는 after-hours expected nonblocking으로 처리했고, strict universe/MCP/risk gate가 모두 PASS였다. sell-first 재평가에서 `PFE` 1주 trim이 가장 직접적인 executable candidate로 남아 `client_order_id=ah-20260617-1351-sell-pfe-01`로 제출했다. immediate same-id reconciliation 기준 상태는 `new` open order이며 아직 fill은 없다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-17-1351-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-17-1351-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-1351-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity note: `wiki/evidence-store/sources/2026-06-17-1351-after-hours-autopilot-runtime-alpaca-spot-check.json`
- 이번 cycle은 사용자가 요구한 대로 `1351` preflight의 account/positions/orders/asset rows를 source-of-record로 유지했다. 다만 after-hours quote/spread 실행 품질은 preflight IEX surface보다 live overnight two-sided quote가 더 직접적이어서, direct Alpaca MCP `get_clock/get_account_info/get_orders/get_all_positions/get_watchlists/get_stock_latest_quote(feed=overnight)` continuity 한 번으로 submit-boundary quote freshness만 보강했다.

## Alpaca MCP 확인

- Regular market: direct `get_clock`=`2026-06-17T00:58:37.141801522-04:00` 기준 regular market closed였다.
- Account: source-of-record preflight 기준 account `ACTIVE`, cash `30,365.77 USD`, portfolio value `101,162.81 USD`, buying power `303,778.81 USD`였다. post-submit live `get_account_info` 기준 cash는 동일 `30,365.77 USD`, portfolio value `101,180.22 USD`, buying power `303,793.79 USD`였다.
- Positions/Open orders/Watchlists: submit 전 source-of-record positions `33`건, open orders `0`, watchlists `0`였다. post-submit live `get_orders(status=open)` 기준 `PFE` open order `1`건이 생겼고 `get_all_positions` 기준 `PFE qty=3`은 유지되지만 `qty_available=2`로 1주가 예약됐다.
- Same-session after-hours orders/fills: submit 전 `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` 기준 earlier same-session order/fill은 `RGTI` trim 1건뿐이었다. submit 후 same-session after-hours submitted orders는 `2`, filled orders는 `1`이다. separate after-hours session budget은 사실상 `2/2`를 사용 중이다.

## 후보 평가

- `RGTI` sell/trim: overnight latestQuote `20.98/21.00`, spread `0.0953%`, fresh quote 자체는 통과했지만 같은 after-hours 세션에 `ah-20260617-1331-sell-rgti-01` fill이 이미 있어 duplicate sell discipline에 막혔다.
- `PFE` sell/trim: overnight latestQuote `26.01/26.07`, spread `0.2307%`, quote age 약 `4.81분`, held qty `3`, same-session duplicate `0`, open order `0`, repeated weak-review defensive holding trim rationale가 유지돼 이번 cycle의 selected sell-first candidate가 됐다.
- `AVGO` sell/trim: overnight latestQuote `380.41/380.90`, spread `0.1288%`로 gate는 통과했지만 잔여 보유가 `1주`라 minimum remaining qty 해석을 유지했다.
- `MSFT`: overnight latestQuote `394.40/394.47`, spread `0.0177%`, 1주 notional `394.47 USD`로 fallback buy는 가능했지만, 이번 cycle에는 eligible sell/trim `PFE`가 먼저 열려 buy fallback으로 내려가지 않았다.
- `QQQ/SMH/LLY`: fresh quote는 있었지만 1주 ask가 after-hours per-order cap 약 `505.81 USD`를 넘었다.
- `JPM`: quote freshness는 통과했지만 overnight spread가 `0.6376%`로 cap을 넘었다.

## Gate 결과

- `ALPACA_PAPER_TRADE=true`: PASS
- Regular market open check: PASS (`market_closed`는 after-hours expected nonblocking)
- Alpaca core account/clock/positions/orders/asset evidence: PASS (`1351` scheduler preflight 유지)
- `after_hours_policy` profile/session/review bucket/order budget separation: PASS
- Universe strict gate: PASS (`62` symbols screened, `SPY/QQQ` benchmarks 포함)
- MCP strict gate: PASS (`sec-edgar`, `fred`, `yahoo-finance` pass; `alpha-vantage` provider_error, `firecrawl` credits 부족 gap 기록)
- Risk gate: PASS (`check-risk-policy.py --json`)
- Fresh quote gate: PASS (`PFE` overnight quote age 약 `4.81분`)
- Spread gate: PASS (`PFE` spread `0.2307%` <= `0.25%`)
- Submit/reconcile path: PASS (`client_order_id` same-id reconciliation completed with open lifecycle state)

## 주문 및 리스크 검증

- 주문 계획: `wiki/trade-ledger/orders/2026-06-17-1351-after-hours-autopilot.json`
- 제출된 주문: `PFE` sell `1` share, `limit=26.01`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260617-1351-sell-pfe-01`
- immediate reconciliation: `order_id=c96904a2-deab-415b-9b27-a20660a043e4`, `status=new`, `filled_qty=0`, `filled_avg_price=null`
- `risk_inputs.after_hours_new_orders_submitted_today=1`로 separate after-hours budget 입력을 사용했고, submit 후 same-session actual submitted count는 `2/2`로 증가했다.
- 이번 cycle은 policy의 `cancel_unfilled_after_minutes=5`에 도달하지 않았으므로 즉시 취소 대신 lifecycle-record로 남긴다.

## 산출물

- Run manifest: `wiki/evidence-store/run-manifests/2026-06-17-1351-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-1351-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot-check: `wiki/evidence-store/sources/2026-06-17-1351-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-1351-after-hours-autopilot.json`
- Post-trade note: `wiki/trade-ledger/positions/2026-06-17-1351-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-1351-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-1351-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-17-1351-after-hours-autopilot.json`: PASS
