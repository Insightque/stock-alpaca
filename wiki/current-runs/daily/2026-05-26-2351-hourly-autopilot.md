---
id: 2026-05-26-2351-hourly-autopilot
created_at: 2026-05-26T15:00:24Z
timezone: Asia/Seoul
paper: true
mode: hourly_autopilot
orders_submitted: 0
---

# 2026-05-26 23:51 KST hourly paper autopilot

## 결론

- 이번 run은 `blocked`다.
- `.env`의 `ALPACA_PAPER_TRADE=true`는 확인했다.
- Alpaca core MCP는 clock/account/orders/positions/fills/watchlists/quotes/snapshots/assets/news가 usable했다.
- 미국 주식 시장은 `2026-05-26T10:51:43-04:00` 기준 open이었다.
- 하지만 buy 제출에 필요한 research MCP usable count가 2개(SEC EDGAR, Yahoo Finance)로 정책 최소값 3개에 미달했다.
- Alpaca core의 첫 차단 gate는 없다. 전체 submit first blocking gate는 `mcp_research_min_confirmations`다.
- `LLY`, `LRCX`, `ASML`은 fresh quote가 있었지만 Alpaca spread cap 0.50%를 초과했다.
- `AAPL`과 `SMH`는 spread가 통과했지만 research MCP minimum confirmation과 우선순위/포트폴리오 fit 때문에 validation buy로 승격하지 않았다.
- 주문 계획은 빈 주문(`orders: []`)이며 실제 paper 주문, 취소, 포지션 변경은 없다.

## Gate 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에 `ALPACA_PAPER_TRADE=true` 존재 |
| Automation lock | PASS | wrapper prompt와 동일한 invocation의 `.locks/hourly-autopilot.lock` 존재 |
| Alpaca market clock | PASS | `is_open=true`, next close `2026-05-26 16:00 ET` |
| Account/order/fill/position reconciliation | PASS | active account, open orders 0, same-day fills 0, 10개 long positions |
| Universe coverage | PASS | metadata universe 62개 loaded, `SPY`/`QQQ` 포함 |
| MCP coverage strict | FAIL | research provider usable count 2, 최소 3 필요 |
| Quote freshness | PASS | 후보 5개 quote 모두 20분 이내 |
| Spread | MIXED | `AAPL`, `SMH` pass; `LLY`, `LRCX`, `ASML` fail |
| Risk policy | PASS for empty plan | 신규 주문 0건 |
| Submit | BLOCKED | research MCP minimum + candidate spread gate 실패 |

## Coordinator Agent

- 최근 위키와 정책을 확인했다.
- Alpaca account/clock/open orders/fills/positions/watchlists를 이번 run에서 새로 확인했다.
- Account value `101,521.71`, cash `44,030.58`, buying power `139,092.57`.
- Open equity orders는 0건이고 2026-05-26 same-day fills도 0건이다.

## Universe Agent

- universe source: `harness/symbol-metadata.yaml` 62개 심볼 + 보유 종목 + `SPY`/`QQQ`.
- 필수 benchmark `SPY`, `QQQ` 포함.
- Alpaca MCP `get_stock_bars`로 62개 심볼의 최근 IEX adjusted 일봉 응답을 확인했다.
- Pre-MCP shortlist: `LRCX`, `SMH`, `ASML`, `AAPL`, `LLY`.
- Final research candidates: `AAPL`, `ASML`, `LLY`.
- `RGTI`, `QBTS`, `IONQ`는 speculative/overheat guard로 신규 buy 후보에서 제외한다.

## Market Data Agent

| 티커 | quote_time_utc | bid | ask | spread_pct | 판단 |
| --- | --- | ---: | ---: | ---: | --- |
| LLY | 2026-05-26T14:53:52Z | 1072.25 | 1134.00 | 5.598 | fresh but spread fail |
| LRCX | 2026-05-26T14:53:58Z | 303.85 | 320.05 | 5.193 | fresh but spread fail, already held |
| ASML | 2026-05-26T14:53:49Z | 1630.36 | 1639.54 | 0.562 | fresh but just above spread cap |
| SMH | 2026-05-26T14:53:58Z | 601.77 | 602.13 | 0.060 | fresh, spread pass, cluster overlap |
| AAPL | 2026-05-26T14:53:58Z | 311.06 | 311.09 | 0.010 | fresh, spread pass, limited upside |

Fresh quote가 있어도 research MCP minimum confirmation이 3개 미만이면 buy submit은 금지된다.

## Web Research Agent

이번 run은 Alpaca News, SEC EDGAR, Yahoo Finance는 usable했지만 Alpha Vantage, FRED, Firecrawl이 usable하지 않았다.

- Alpaca News: AAPL/INTC/NVDA/TSM foundry 기사, AAPL Ferrari EV/Jony Ive 기사, AAPL Japan iPhone 17e sales slowdown 기사, LLY VERVE-102 LDL reduction 기사 확인.
- SEC EDGAR: `LLY`, `LRCX`, `ASML`, `AAPL` 최근 filings 확인. `SMH`는 ETF라 local SEC company ticker cache에 없고 `empty_response`로 분류.
- Yahoo Finance: `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH` stock/ETF info와 AAPL recommendation/news 확인.
- Alpha Vantage: `TOOL_LIST`와 `PING`은 됐지만 data schema/call이 usable하지 않아 점수 미반영.
- FRED/Firecrawl: local wrapper health check가 DNS 실패.

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | retry_count | gap_reason |
| --- | --- | --- | --- | --- | ---: | --- |
| Alpaca | true | true | pass | cancelled | 2 | core pass, `get_most_active_stocks`만 cancelled |
| SEC EDGAR | true | true | usable | empty_response | 0 | issuer filings usable; `SMH` ETF lookup empty_response |
| Alpha Vantage | true | false | failed | wrapper_error | 2 | schema/data calls cancelled, schema-less direct call rejected |
| FRED | true | false | failed | dns | 2 | `api.stlouisfed.org` DNS failure |
| Firecrawl | true | false | failed | dns | 2 | `api.firecrawl.dev` DNS failure |
| Yahoo Finance | true | true | usable | - | 0 | stock info/news/recommendations usable, no gap |

## Trend Agent

| 순위 | 티커 | confidence | 판단 |
| ---: | --- | --- | --- |
| 1 | AAPL | medium | tight spread와 SEC/Yahoo 확인은 있으나 target mean 대비 upside가 제한적이고 Apple news가 혼재 |
| 2 | ASML | medium | semicap/ADR momentum과 Yahoo strong-buy는 긍정적이나 Alpaca spread 0.562%로 cap 초과 |
| 3 | LLY | medium | VERVE-102 catalyst와 Yahoo buy는 긍정적이나 Alpaca spread 5.598%로 validation buy 불가 |
| 4 | SMH | low | trend와 spread는 양호하지만 ETF이고 기존 반도체 exposure와 중복 |
| 5 | LRCX | low | 강한 momentum이나 이미 20주 보유, target mean 대비 overheat risk와 spread failure |

## Portfolio/Risk Agent

- 신규 buy 주문: 없음.
- 신규 sell/trim 주문: 없음.
- Sell/trim은 thesis-break, risk-limit, stale-thesis, position-sizing, portfolio-fit 근거가 필요하다. 이번 run에서 보유 종목의 cap 위반 또는 thesis-break를 확인하지 못했다.
- AI semiconductor cluster와 quantum speculative cluster는 기존 포지션 기준 정책 한도를 넘지 않는다.
- Empty order plan risk check는 PASS했다.

## Executor Agent

주문 제출 없음. Alpaca MCP `place_stock_order`를 호출하지 않았다.

## Post-Trade Agent

주문 제출 시도가 없었고 open orders/fills가 0건이라 post-trade reconciliation 제출 후 단계는 발생하지 않았다.

- account cash, buying power, current positions, open orders, same-day fills는 이번 run에서 확인했다.
- 실제 주문, 취소, 포지션 변경은 없다.

## Submitted Orders

| 티커 | side | qty | 결과 |
| --- | --- | ---: | --- |
| 없음 | - | 0 | 모든 hard gate 통과 전 제출 금지 |

## Skipped Order Rationale

| 티커 | side | skip reason | 세부 rationale |
| --- | --- | --- | --- |
| AAPL | buy | research MCP minimum fail | spread 0.010%와 SEC/Yahoo는 통과했지만 Alpha/FRED/Firecrawl 공백으로 research confirmation 2/5, target mean 대비 upside 제한 |
| ASML | buy | research MCP + spread fail | Yahoo strong-buy와 SEC filings는 확인했지만 spread 0.562%로 정책 cap 초과, research confirmation 2/5 |
| LLY | buy | research MCP + spread fail | LLY catalyst와 SEC/Yahoo 확인은 있으나 spread 5.598%로 validation buy 불가, research confirmation 2/5 |
| SMH | buy | final candidate 제외 + concentration | spread는 0.060%로 통과했지만 ETF/반도체 cluster 중복, SEC ETF lookup empty_response, research confirmation 부족 |
| LRCX | buy | spread + existing concentration | 이미 20주 보유, AI semiconductor cluster 노출, spread 5.193%, Yahoo target mean 대비 overheat risk |
| 보유 전 종목 | sell | no valid sell catalyst | thesis-break, risk-limit, stale-thesis, position-sizing 위반이 확인되지 않아 자동 매도 금지 |

## 검증

- `python3 scripts/check-universe-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-26-2351-hourly-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-26-2351-hourly-autopilot.json`: FAIL
  - `research MCP gate requires at least 3 usable/pass research providers; got 2 (sec-edgar, yahoo-finance)`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-26-2351-hourly-autopilot.json`: PASS with `orders is empty`

## 산출물

- Raw source: [[2026-05-26-2351-hourly-autopilot-sources]]
- Manifest: `wiki/evidence-store/run-manifests/2026-05-26-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-26-2351-hourly-autopilot.json`

## 지표 설명

- `universe coverage`: 추천 전 넓은 후보군을 실제로 살펴봤는지 보는 검증이다. 이번 run은 62개 metadata 심볼과 `SPY`/`QQQ`를 포함했다.
- `MCP coverage`: Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance가 모두 usable한지 확인하는 gate다. 자동 buy 주문은 Alpaca core pass와 research provider 3개 이상 pass가 필요하다.
- `quote freshness`: submit mode에서는 quote/snapshot이 정책상 20분 이내여야 한다.
- `spread`: bid/ask 차이를 중간가격으로 나눈 비율이다. 정책 한도는 0.50%다.
- `confidence`: 가격, 뉴스/펀더멘털, 리스크/유동성, 포트폴리오 적합성을 합친 판단 신뢰도다. MCP 공백이 있으면 자동으로 낮춘다.
- `cluster exposure`: 비슷한 테마 종목이 포트폴리오에 과도하게 몰리는지 보는 제한이다.
