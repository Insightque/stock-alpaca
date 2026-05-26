---
id: 2026-05-26-2011-hourly-autopilot
created_at: 2026-05-26T11:11:14Z
timezone: Asia/Seoul
paper: true
mode: hourly_autopilot
orders_submitted: 0
---

# 2026-05-26 20:11 KST hourly paper autopilot

## 결론

- 이번 run은 `blocked`다.
- `.env`의 `ALPACA_PAPER_TRADE=true`는 확인했다.
- Alpaca MCP로 포지션, broad universe bars, asset checks, Alpaca news 일부는 확인했다.
- 하지만 Alpaca clock/account/open orders/fills/watchlists/latest quote/snapshot/latest bar가 usable하지 않았다.
- SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance도 usable confirmation을 만들지 못했다.
- 따라서 Alpaca core MCP gate, MCP strict gate, quote gate, spread gate, account/order reconciliation gate가 실패했다.
- 주문 계획은 빈 주문(`orders: []`)이며 실제 paper 주문, 취소, 포지션 변경은 없다.

## Gate 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에 `ALPACA_PAPER_TRADE=true` 존재 |
| Automation lock | PASS | wrapper lock으로 보이는 `.locks/hourly-autopilot.lock` 존재 |
| Alpaca market clock | FAIL | `get_clock` unusable/cancelled, local Alpaca MCP DNS failure |
| Account/order/fill reconciliation | FAIL | `get_account_info`, `get_orders`, `get_account_activities`, `get_watchlists` unusable |
| Universe coverage | PASS | metadata universe 62개 loaded, `SPY`/`QQQ` 포함 |
| MCP coverage strict | FAIL | Alpaca core 일부와 research MCP confirmation 실패 |
| Quote freshness | FAIL | latest quote/snapshot/latest bar unusable |
| Spread | FAIL | bid/ask/spread 없음 |
| Risk policy | PASS for empty plan | 신규 주문 0건 |
| Submit | BLOCKED | 위 실패 gate 때문에 주문 제출 금지 |

## Coordinator Agent

- 최근 위키와 정책을 확인했다.
- 최신 확인 가능한 Alpaca 포지션은 10개 long이다.
- `get_all_positions` 기준 long market value는 57,209.83 USD, 총 미실현 손익은 1,240.41 USD다.
- account cash/buying power는 이번 run에서 Alpaca account MCP가 실패해 새로 확인하지 못했다. Empty order plan에는 최근 위키 cash snapshot을 재사용했지만 submit 근거로 쓰지 않았다.

## Universe Agent

- universe source: `harness/symbol-metadata.yaml` 62개 심볼 + 보유 종목 + `SPY`/`QQQ`.
- 필수 benchmark `SPY`, `QQQ` 포함.
- Alpaca MCP `get_stock_bars`로 62개 심볼의 최근 일봉 응답을 확인했다.
- Pre-MCP shortlist: `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH`.
- Final research candidates: `LLY`, `LRCX`, `ASML`.
- `QBTS`, `RGTI`, `IONQ`, `NOK`는 speculative/overheat guard로 신규 buy 후보에서 제외했다.

## Market Data Agent

| 티커 | 2026-05-15 종가 | 2026-05-22 종가 | 최근 흐름 | 메모 |
| --- | ---: | ---: | --- | --- |
| LLY | 1004.695 | 1065.60 | 상승 | 헬스케어 성장주, Alpaca 뉴스 catalyst 있음 |
| LRCX | 284.37 | 305.43 | 상승 | semicap momentum, 이미 보유 중 |
| ASML | 1501.52 | 1632.98 | 상승 | semicap/ADR momentum |
| AAPL | 300.19 | 308.81 | 상승 | 대형 기술주 후보이나 최종 3위 밖 |
| SMH | 556.85 | 575.91 | 상승 | 반도체 ETF, 기존 AI 반도체 cluster와 중복 |
| SPY | 739.10 | 745.67 | 상승 | benchmark |
| QQQ | 708.91 | 717.49 | 상승 | benchmark |

Quote freshness와 spread는 확인하지 못했다. 이 이유만으로도 submit은 금지된다.

## Web Research Agent

이번 run은 required research MCP coverage가 실패했다. Alpaca news만 usable하다.

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | source_refs | gap_reason |
| --- | --- | --- | --- | --- | --- |
| Alpaca | true | false | failed | [[2026-05-26-2011-hourly-autopilot-sources]] | positions/bars/assets/news 일부는 성공했지만 clock/account/orders/fills/quotes/spread가 실패 |
| SEC EDGAR | true | false | failed | [[2026-05-26-2011-hourly-autopilot-sources]] | direct call cancelled, local recent-filings query returned ticker lookup gap |
| Alpha Vantage | true | false | failed | [[2026-05-26-2011-hourly-autopilot-sources]] | local MCP `TOOL_CALL(EARNINGS, LLY)` DNS failure |
| FRED | true | false | failed | [[2026-05-26-2011-hourly-autopilot-sources]] | local MCP DNS failure to `api.stlouisfed.org` |
| Firecrawl | true | false | failed | [[2026-05-26-2011-hourly-autopilot-sources]] | local MCP DNS failure to `api.firecrawl.dev` |
| Yahoo Finance | true | false | failed | [[2026-05-26-2011-hourly-autopilot-sources]] | direct call cancelled, local wrapper dependency fetch failed |

## Trend Agent

| 순위 | 티커 | 점수 | confidence | 판단 |
| ---: | --- | ---: | --- | --- |
| 1 | LLY | 72 | medium | 가격 추세와 Alpaca biotech headline은 긍정적이지만 all-MCP confirmation 부재 |
| 2 | LRCX | 69 | medium | 가격 추세 우수, 기존 보유와 semicap cluster 노출 때문에 추가 매수 보류 |
| 3 | ASML | 67 | medium | 가격 추세 우수, ADR/semicap exposure와 research MCP gap 때문에 보류 |
| 4 | AAPL | 61 | low | 대형주 안정성은 있으나 catalyst quality가 약하고 final candidate 제외 |
| 5 | SMH | 59 | low | sector ETF momentum은 있으나 기존 반도체 exposure와 중복 |

## Portfolio/Risk Agent

- 신규 buy 주문: 없음.
- 신규 sell/trim 주문: 없음.
- Sell/trim은 thesis-break, risk-limit, stale-thesis, position-sizing, portfolio-fit 근거가 필요하다. 이번 run은 Alpaca quote/order/fill 확인이 부족하므로 매도 판단도 제출하지 않는다.
- 기존 보유 종목 중 `RGTI`, `IONQ`, `NOK`는 급등/고변동 상태라 추격 매수 금지다. 다만 자동 trim도 quote/order gate와 thesis-break 근거가 없어 보류한다.
- Empty order plan risk check는 PASS했다.

## Executor Agent

주문 제출 없음. Alpaca MCP `place_stock_order`를 호출하지 않았다.

## Post-Trade Agent

주문 제출 시도가 없었다. open order/fill reconciliation MCP가 실패했으므로 post-trade reconciliation은 제한적으로만 수행했다.

- 포지션은 Alpaca MCP `get_all_positions` 성공 결과로 확인했다.
- account cash, buying power, open orders, same-day fills는 이번 run에서 미확인이다.
- 실제 주문, 취소, 포지션 변경은 없다.

## Skipped Order Rationale

| 티커 | side | skip reason | 세부 rationale |
| --- | --- | --- | --- |
| LLY | buy | Alpaca core/MCP/quote/spread gate fail | 추세와 Alpaca news는 긍정적이나 account/clock/order/quote/spread 및 SEC/Alpha/FRED/Firecrawl/Yahoo 확인이 없어 자동 주문 불가 |
| LRCX | buy | Alpaca core/MCP/quote/spread + concentration | 이미 20주 보유, semicap/AI semiconductor cluster 노출이 높고 fresh spread가 없어 추가 매수 불가 |
| ASML | buy | Alpaca core/MCP/quote/spread gate fail | 가격 추세는 강하지만 ADR/semicap 후보에 대한 filing/IR/analyst/macro 확인이 실패 |
| 보유 전 종목 | sell | no valid sell catalyst | thesis-break 또는 risk-limit 근거를 Alpaca quote/order state로 확인하지 못해 자동 매도 금지 |

## 산출물

- Raw source: [[2026-05-26-2011-hourly-autopilot-sources]]
- Manifest: `wiki/evidence-store/run-manifests/2026-05-26-2011-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-26-2011-hourly-autopilot.json`

## 지표 설명

- `universe coverage`: 추천 전 넓은 후보군을 실제로 살펴봤는지 보는 검증이다. 이번 run은 62개 metadata 심볼과 `SPY`/`QQQ`를 포함했다.
- `MCP coverage`: Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance가 모두 usable한지 확인하는 gate다. 자동 주문은 Alpaca core pass와 buy 후보 기준 research provider 3개 이상 pass가 필요하다.
- `quote freshness`: submit mode에서는 quote/snapshot이 정책상 20분 이내여야 한다.
- `spread`: bid/ask 차이를 중간가격으로 나눈 비율이다. 이번 run은 bid/ask가 없어 측정 불가다.
- `confidence`: 가격, 뉴스/펀더멘털, 리스크/유동성, 포트폴리오 적합성을 합친 판단 신뢰도다. MCP 공백이 있으면 자동으로 낮춘다.
- `cluster exposure`: 비슷한 테마 종목이 포트폴리오에 과도하게 몰리는지 보는 제한이다.
