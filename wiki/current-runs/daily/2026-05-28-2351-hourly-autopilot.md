# 2026-05-28-2351-hourly-autopilot scheduled paper autopilot

## 요약

- Paper mode: `ALPACA_PAPER_TRADE=true`. 정규장 clock은 `2026-05-28T10:51:19.851725879-04:00` 기준 open=true이고, 계획 생성 시각은 `2026-05-28T14:57:48Z`이다.
- Scheduler stale cleanup: `wiki/evidence-store/sources/2026-05-28-2351-hourly-autopilot-stale-order-cleanup.json` status=`pass`이며 remaining open orders는 `[]`로 새 주문을 막는 `risk_open_order_lifecycle` 차단은 없다.
- Alpaca core gate: PASS. scheduler core preflight의 clock/account/positions/orders/activities/assets/quotes/snapshots/trades가 모두 pass이고 quote row는 20분 freshness 한도 안이다.
- Research MCP gate: SEC EDGAR, FRED, Firecrawl, Yahoo Finance PASS; Alpha Vantage는 `empty_response` gap. 4개 usable/pass로 submit 기준 3개를 충족했다.
- 계획 결과: SPY, AAPL, SLB 각 1주 regular-session day limit paper validation buy 후보.

## 후보 및 주문 계획

| Symbol | Action | Qty | Limit | Spread % | 근거 |
| --- | --- | ---: | ---: | ---: | --- |
| SPY | buy | 1 | 752.67 | 0.0226 | Broad-index ETF 1주 검증. 특정 단일 섹터 집중을 키우지 않고 시장 베타를 관찰한다. |
| AAPL | buy | 1 | 311.29 | 0.0064 | Mega-cap growth_quality 1주 추가. AI semiconductor 직접 노출을 늘리지 않는 대형 현금흐름 검증이다. |
| SLB | buy | 1 | 55.67 | 0.0359 | Energy services 1주 검증. 대형 기술/AI semiconductor 집중과 다른 return driver를 관찰한다. |


## 게이트

- Universe strict: PASS. 62개 metadata universe, SPY/QQQ 포함, pre-MCP shortlist 10개(SPY/AAPL/NVDA/GOOGL/WMT/AMZN/INTC/SO/QQQ/SLB), final candidates 3개.
- MCP strict: PASS. Alpaca core PASS + research usable/pass 4개. Alpha Vantage gap은 `empty_response`로 기록하고 점수에는 미사용.
- Quote freshness/spread: PASS. SPY 6.11분/0.0226%, AAPL 6.12분/0.0064%, SLB 6.11분/0.0359%.
- Open-order lifecycle: PASS. cleanup file과 Alpaca core preflight 모두 open order 없음.
- Risk validator: PASS. Buy notional 1,119.63달러, post-cash 38,203.63달러, post-invested 63,464.32달러로 medium-risk-v1.1 한도 안이다.

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | source_refs |
| --- | --- | --- | --- | --- | --- |
| alpaca | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-28-2351-hourly-autopilot-alpaca-core-preflight.json |
| sec-edgar | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-28-2351-hourly-autopilot-research-mcp-preflight.json |
| alpha-vantage | true | false | gap | empty_response | wiki/evidence-store/sources/2026-05-28-2351-hourly-autopilot-research-mcp-preflight.json |
| fred | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-28-2351-hourly-autopilot-research-mcp-preflight.json |
| firecrawl | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-28-2351-hourly-autopilot-research-mcp-preflight.json |
| yahoo-finance | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-28-2351-hourly-autopilot-research-mcp-preflight.json |


## 제출 및 사후 점검

| Symbol | Client order id | Status | Filled qty | Fill price | 비고 |
| --- | --- | --- | ---: | ---: | --- |
| SPY | `hourly-20260528-2351-spy-buy-01` | not found | 0 |  | 첫 submit `cancelled`, same-id retry `timeout`, reconciliation 404로 실제 주문 없음 |
| AAPL | `hourly-20260528-2351-aapl-buy-01` | new/open | 0 |  | 첫 submit `cancelled`, reconciliation 404 후 같은 id 재시도 accepted |
| SLB | `hourly-20260528-2351-slb-buy-01` | filled | 1 | 55.48 | Alpaca MCP submit accepted and filled |

- Post-trade reconciliation: client-order-id checks completed for SPY/AAPL/SLB, open orders PASS with AAPL open, positions PASS and includes SLB. Fresh account and fill activity refresh were cancelled by the runtime monitor and recorded as `gap_category=cancelled`.
- Review due: SLB `회고 대기`; AAPL open-order lifecycle follow-up 필요.

## 지표 설명

- `spread_pct`: Alpaca latest quote의 bid/ask 중간값 대비 스프레드. 0.50% 이하여야 제출 가능하다.
- `quote_age_minutes`: 주문 계획 생성 시점 기준 quote 경과 시간. 정책상 20분 이하여야 한다.
- `research confirmations`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass로 확인된 provider 수. Buy 제출은 3개 이상이 필요하다.
- `risk_open_order_lifecycle`: stale unfilled autopilot order가 취소 또는 조정되지 않아 새 주문을 막는 상태. 이번 run에서는 remaining open order가 없어 차단하지 않았다.
