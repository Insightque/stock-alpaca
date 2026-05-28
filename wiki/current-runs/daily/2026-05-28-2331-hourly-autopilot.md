# 2026-05-28-2331-hourly-autopilot scheduled paper autopilot

## 요약

- Paper mode: `ALPACA_PAPER_TRADE=true`. 정규장 clock은 `2026-05-28T10:38:43.224155208-04:00` 기준 open=true.
- Scheduler stale cleanup: `wiki/evidence-store/sources/2026-05-28-2331-hourly-autopilot-stale-order-cleanup.json`에서 NEE stale unfilled order 취소를 시도했고, 직후 파일에는 remaining open으로 남았지만 등록 Alpaca MCP `get_orders(status=open, asset_class=us_equity)` 재조정은 open order `[]`를 반환했다. 따라서 `risk_open_order_lifecycle` 차단은 해소로 기록했다.
- Alpaca core gate: PASS. scheduler core preflight의 clock/account/positions/orders/activities/assets/quotes/snapshots/trades가 모두 pass이고 quote row는 20분 freshness 한도 안이다.
- Research MCP gate: SEC EDGAR, FRED, Firecrawl, Yahoo Finance PASS; Alpha Vantage는 `empty_response` gap. 4개 usable/pass로 submit 기준 3개를 충족했다.
- 계획 결과: GOOGL, SO, HOOD 각 1주 regular-session day limit paper validation buy 후보.

## 후보 및 주문 계획

| Symbol | Action | Qty | Limit | Spread % | 근거 |
| --- | --- | ---: | ---: | ---: | --- |
| GOOGL | buy | 1 | 389.00 | 0.1674 | Mega-cap tech growth_quality 1주 검증. 오늘 같은 symbol/side regular buy가 없고 AI semiconductor cluster를 직접 늘리지 않는다. |
| SO | buy | 1 | 93.55 | 0.0535 | Utilities defensive_yield 1주 추가. 방어 클러스터로 포트폴리오 고베타 노출을 희석하며 ticker/cluster cap에 여유가 있다. |
| HOOD | buy | 1 | 77.26 | 0.0518 | Medium-source speculative_growth 후보라 1주 validation floor로만 제한. speculative cap과 quote/spread gate는 통과했다. |

## 게이트

- Universe strict: PASS. 62개 metadata universe, SPY/QQQ 포함, pre-MCP shortlist 10개, final candidates 3개.
- MCP strict: PASS. Alpaca core PASS + research usable/pass 4개. Alpha Vantage gap은 `empty_response`로 기록하고 점수에는 미사용.
- Risk validator: PASS. 계획 buy notional은 559.81달러, post-cash 39,245.83달러, post-invested 62,181.64달러로 medium-risk-v1.1 한도 안이다.
- Open-order lifecycle: PASS. cleanup file의 NEE stale order는 등록 Alpaca MCP open-order 재조정에서 더 이상 open이 아니었다.

## 지표 설명

- `spread_pct`: Alpaca latest quote의 bid/ask 중간값 대비 스프레드. 0.50% 이하여야 제출 가능하다.
- `quote_age_minutes`: 주문 계획 생성 시점 기준 quote 경과 시간. 정책상 20분 이하여야 한다.
- `research confirmations`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass로 확인된 provider 수. Buy 제출은 3개 이상이 필요하다.
- `risk_open_order_lifecycle`: stale unfilled autopilot order가 취소 또는 조정되지 않아 새 주문을 막는 상태. 이번 run에서는 재조정으로 open order가 없어 차단하지 않았다.

## 제출 및 사후 점검

| Symbol | Client order id | Status | Filled qty | Fill price | 비고 |
| --- | --- | --- | ---: | ---: | --- |
| GOOGL | `hourly-20260528-2331-googl-buy-01` | new/open | 0 |  | Alpaca MCP submit accepted |
| SO | `hourly-20260528-2331-so-buy-01` | filled | 1 | 93.38 | 첫 submit `cancelled`, same client id reconciliation 404 후 같은 id 재시도 filled |
| HOOD | `hourly-20260528-2331-hood-buy-01` | not submitted | 0 |  | 첫 submit `cancelled`, reconciliation 404, same-id retry가 runtime safety monitor에서 cancelled |

- Post-trade reconciliation: order-by-client-id PASS for GOOGL/SO, open orders PASS with GOOGL open, fill activities PASS with SO fill, positions PASS. Fresh account refresh는 runtime에서 두 번 `cancelled`되어 gap으로 기록했다.
- Review due: SO `회고 대기`; GOOGL open-order lifecycle follow-up 필요.
