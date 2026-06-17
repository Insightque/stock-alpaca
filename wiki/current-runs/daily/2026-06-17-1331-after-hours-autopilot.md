# 2026-06-17-1331-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1331` core/research preflight를 사용했고, sparse Alpaca core preflight는 direct Alpaca MCP continuity로 보강했다. strict universe/MCP/risk gate가 모두 PASS였고 fresh overnight quote가 열리면서 `RGTI` 1주 trim sell이 `client_order_id=ah-20260617-1331-sell-rgti-01`로 제출되어 `filled_avg_price=20.96 USD`에 즉시 체결됐다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-17-1331-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-17-1331-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-1331-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity note: `wiki/evidence-store/sources/2026-06-17-1331-after-hours-autopilot-runtime-alpaca-spot-check.json`
- `1331` Alpaca core preflight는 regular-market closed clock row만 남겼기 때문에 direct Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders/get_watchlists/get_asset/get_stock_latest_quote(feed=overnight)`로 missing submit-boundary evidence를 한 번만 보강했다.

## Alpaca MCP 확인

- Regular market: direct `get_clock`=`2026-06-17T00:34:06.896234831-04:00` 기준 regular market closed였다.
- Account: submit 전 direct `get_account_info` 기준 account `ACTIVE`, cash `30,344.81 USD`, portfolio value `101,176.88 USD`, buying power `303,781.80 USD`였다. 체결 후 `get_account_info` 기준 cash `30,365.77 USD`, portfolio value `101,133.79 USD`, buying power `303,720.06 USD`로 갱신됐다.
- Positions/Open orders/Watchlists: submit 전 direct `get_all_positions` 기준 positions `33`건, `get_orders(status=open)` `0`건, `get_watchlists` `0`건이었다. 체결 후 `get_orders(status=open)`는 여전히 `0`건이고 `RGTI` 보유 수량은 `28주 -> 27주`로 감소했다.
- Same-session after-hours orders/fills: submit 전 `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`는 `0`건이었고, 체결 후에는 same-session after-hours submitted orders/fills 모두 `1`건이다. separate after-hours session budget은 `1/2` 사용 상태다.

## 후보 평가

- `RGTI` sell/trim: overnight latestQuote `20.94/20.99`, spread `0.2385%`, quote age 약 `0.30분`, held qty `28`, speculative loss-control residual sleeve rationale, active/tradable NASDAQ stock, same-session duplicate `0`이라 executable sell-first candidate로 선택했다.
- `PFE`: overnight latestQuote `25.98/26.04`, spread `0.2307%`로 gate는 통과했지만 recent portfolio review에서 trim timing이 약하게 남아 lower-priority trim으로 유지했다.
- `AVGO`: overnight latestQuote `379.76/380.58`, spread `0.2157%`로 gate는 통과했지만 잔여 보유가 `1주`라 minimum remaining qty 해석상 추가 trim을 열지 않았다.
- `QQQ`: overnight latestQuote `733.30/733.49`와 fresh quote는 확보됐지만 1주 ask가 after-hours per-order cap 약 `505.88 USD`를 넘었다.

## Gate 결과

- `ALPACA_PAPER_TRADE=true`: PASS
- Regular market open check: PASS (`market_closed`는 after-hours expected nonblocking)
- Alpaca core account/clock/positions/orders/asset/quote/spread: PASS (scheduler sparse preflight를 direct Alpaca continuity로 보강)
- `after_hours_policy` profile/session/review bucket/order budget separation: PASS
- Universe strict gate: PASS (`62` symbols screened, `SPY/QQQ` benchmarks 포함)
- MCP strict gate: PASS (`sec-edgar`, `fred`, `yahoo-finance` pass; `alpha-vantage` provider_error, `firecrawl` credits 부족 gap 기록)
- Risk gate: PASS (`check-risk-policy.py --json`)
- Fresh quote gate: PASS (`RGTI` overnight quote age 약 `0.30분`)
- Spread gate: PASS (`RGTI` spread `0.2385%` <= `0.25%`)
- Submit/reconcile path: PASS (`client_order_id` same-id reconciliation filled)

## 주문 및 리스크 검증

- 주문 계획: `wiki/trade-ledger/orders/2026-06-17-1331-after-hours-autopilot.json`
- 제출된 주문: `RGTI` sell `1` share, `limit=20.94`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260617-1331-sell-rgti-01`
- 체결 결과: `filled_avg_price=20.96 USD`, `filled_at=2026-06-17T04:39:27.02715194Z`
- `risk_inputs.after_hours_new_orders_submitted_today=0`로 separate after-hours budget 입력을 사용했고, submit 후 same-session actual count는 `1/2`로 기록했다.

## 산출물

- Run manifest: `wiki/evidence-store/run-manifests/2026-06-17-1331-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-1331-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot-check: `wiki/evidence-store/sources/2026-06-17-1331-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-1331-after-hours-autopilot.json`
- Post-trade note: `wiki/trade-ledger/positions/2026-06-17-1331-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-1331-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-1331-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-17-1331-after-hours-autopilot.json`: PASS
