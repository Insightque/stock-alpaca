# 2026-05-29 02:51 KST hourly autopilot

## 실행 요약

- Workflow: `harness/workflows/hourly-autopilot.md`
- Run ID: `2026-05-29-0251-hourly-autopilot`
- Paper mode: `ALPACA_PAPER_TRADE=true`
- Market clock: Alpaca scheduler preflight 기준 `2026-05-28T13:51:17.830653788-04:00`, regular session open.
- 결과: 주문 없음. 같은 ET 세션의 신규 주문 수가 이미 `20/20`으로 `risk_daily_new_orders_budget` gate가 첫 차단 조건이다.

## MCP 및 게이트

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | 환경 변수 `ALPACA_PAPER_TRADE=true` |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-05-29-0251-hourly-autopilot-stale-order-cleanup.json`; stale candidate 0, remaining open orders 0 |
| Alpaca core | PASS | `wiki/evidence-store/sources/2026-05-29-0251-hourly-autopilot-alpaca-core-preflight.json`; clock/account/positions/open orders/recent activities/quotes pass |
| Universe | PASS | 62개 metadata universe + SPY/QQQ 포함 |
| Research MCP | PASS | SEC EDGAR/FRED/Firecrawl/Yahoo usable, Alpha Vantage `empty_response` gap |
| Quote/spread | PASS | Alpaca core preflight quote rows가 decision time 기준 20분 이내이고 shortlist spread가 0.50% 한도 이내 |
| Risk | PASS for empty plan | 신규 주문 예산 `20/20`으로 주문 후보를 계획하지 않음 |

## 추천 후보와 차단 사유

Scheduler research preflight shortlist는 `SPY`, `QQQ`, `AAPL`, `AMZN`, `NEE`, `NVDA`, `INTC`, `BAC`, `NKE`, `JNJ`, `HD`, `MA`였다. 이 중 universe와 MCP tier는 통과했고 quote/spread도 submit freshness window 안에 있었지만, regular-session daily new-order cap이 이미 소진되어 모든 신규 validation buy를 차단했다.

Top recheck candidates: `SPY`, `QQQ`, `AAPL`, `AMZN`, `NEE`. 다음 regular-session ET 거래일 또는 daily order budget reset 이후 재평가한다. 같은 세션 내 relaxation candidate는 없다. 예산 제한은 hard risk gate라 완화하지 않는다.

## 주문 계획

| Symbol | Side | Qty | 상태 | 사유 |
| --- | --- | ---: | --- | --- |
| - | - | 0 | skipped | `risk_daily_new_orders_budget` 20/20 |

제출 전 gate summary는 주문 후보가 없으므로 작성하지 않았다. `place_stock_order` 호출도 없고 post-trade reconciliation 대상 신규 주문도 없다. Scheduler Alpaca core preflight의 open orders row는 empty로 lifecycle gate를 충족했다.

## 데이터 공백

- `alpha-vantage`: `NEWS_SENTIMENT`가 shortlist에 대해 candidate news item 0건을 반환했다. `gap_category=empty_response`, `retry_count=0`, blocking=false.
- SEC EDGAR는 scheduler preflight가 local `harness/sec-ticker-cik-map.json` CIK fallback과 lightweight company/filing rows를 사용한 evidence로 기록했다.

## 지표 설명

- `daily new-order cap`: `harness/risk-policy.yaml`의 `daily_limits.max_new_orders_per_day`로, 같은 세션에서 새 주문 수가 한도에 도달하면 추가 주문을 막는다.
- `MCP confirmations`: Alpaca core와 보강 research MCP 중 주문 판단에 사용할 수 있는 provider 수다. Buy submit에는 research provider 3개 이상이 필요하다.
- `quote freshness`: 제출 후보 quote가 `order_limits.max_quote_age_minutes_submit` 안에 있어야 한다.
- `spread_pct`: bid/ask 차이를 중간값으로 나눈 비율이다. regular session 제출은 `liquidity_limits.max_spread_pct` 이하여야 한다.
