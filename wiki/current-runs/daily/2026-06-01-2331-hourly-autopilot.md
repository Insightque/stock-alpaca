# 2026-06-01-2331-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler stale cleanup은 stale/open autopilot order 없이 `pass`였다. Alpaca core preflight는 clock/account/positions/open orders/recent activities/quotes를 모두 통과했고, market clock은 `2026-06-01T10:31:16.748418151-04:00` 기준 regular market open이었다.

이번 run은 `submit` mode였지만 주문은 제출하지 않았다. Universe strict와 tiered MCP coverage는 통과 가능한 상태였고, SEC EDGAR/Firecrawl/Yahoo Finance 3개 research confirmation을 사용했다. 다만 주문 후보에 필요한 registered Alpaca MCP runtime quote refresh가 `cancelled`로 끝나 order-level quote/spread metric gate를 통과하지 못했다. Alpha Vantage는 `empty_response`, FRED는 429 `provider_error` gap으로 기록했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | Alpaca preflight clock `2026-06-01T10:31:16.748418151-04:00`, regular market open |
| Stale order cleanup | PASS | stale/open autopilot order 없음: `wiki/evidence-store/sources/2026-06-01-2331-hourly-autopilot-stale-order-cleanup.json` |
| Alpaca core MCP | PASS | account ACTIVE, positions 32건, open orders 0건, scheduler quote hard gate pass |
| Runtime quote refresh | BLOCK | registered Alpaca MCP `get_stock_latest_quote` 1회 호출이 `cancelled`; 주문 수준 quote/spread metric 미확보 |
| Research MCP | PASS tiered | SEC EDGAR/Firecrawl/Yahoo 3개 positive; Alpha empty_response, FRED provider_error 기록 |
| Universe strict | PASS | metadata/preflight universe 62개, SPY/QQQ 포함 |
| Risk plan | PASS expected empty-order warning | 주문 0건, 현재 포지션 포함 |

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| BAC | watch | 금융 분산 후보지만 rate-sensitive thesis는 FRED 429 gap 때문에 watch로 강등했고, runtime quote refresh도 cancelled였다. |
| GOOGL | watch | 기존 mega-cap growth 보유와 비교한 portfolio contribution/replacement rank 개선이 충분하지 않다. |
| NKE | watch | consumer rebound 후보지만 우선순위와 포트폴리오 기여도가 신규 validation buy에 부족하다. |
| NEE | watch | 유틸리티/전력 방어 노출은 이미 있고 rate-sensitive thesis에는 FRED macro gap이 남아 있다. |
| COP | watch | energy/commodity 분산 후보지만 due validation lifecycle review가 추가매수를 차단한다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AMD | watch | alpaca_quote_refresh_cancelled | AI semiconductor target-band 경고권과 intraday 약세는 재점검 사유지만, 주문 수준 quote/spread refresh가 cancelled되어 trim 불가. |
| TSLA | watch | alpaca_quote_refresh_cancelled | 약한 prior review와 intraday 약세가 있지만 현재 order-grade spread/expected-excess metric이 없어 trim/order로 승격하지 않음. |
| INTC | hold_watch | sell_trigger_none | 1-share validation position이고 active trim trigger가 확인되지 않았다. quote refresh cancellation도 주문 생성을 차단했다. |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Post-trade reconciliation: submit attempt는 없었지만 preflight open orders 0건, positions 32건, recent activities snapshot을 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | 주문 0건 경고만 발생 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-01-2331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-01-2331-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-01-2331-hourly-autopilot-post-trade.json`
- Runtime quote refresh evidence: `wiki/evidence-store/sources/2026-06-01-2331-hourly-autopilot-runtime-quote-refresh.json`

## 지표 설명

- `spread_pct`: bid/ask 중간값 대비 스프레드다. 이번 runtime quote refresh가 cancelled되어 주문 후보에는 metric gap으로 처리했다.
- `mcp_coverage`: Alpaca core와 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 확인 상태다. submit mode에서는 core pass와 research positive 3개 이상이 필요하다.
- `sell_candidate_diagnostics`: 보유 종목을 새 매수보다 먼저 점검한 결과다. trigger가 없거나 sell gate/metric이 막으면 주문하지 않고 재점검 후보로만 남긴다.
- `validation_lifecycle`: validation buy 이후 1D/5D/20D 회고가 필요한지와 추가매수 차단 여부를 기록한다.
- `portfolio_construction_policy`: 새 매수가 기존 보유와 비교해 분산, 대체 순위, 포트폴리오 기여를 개선하는지 보는 계층이다.
