---
id: 2026-05-27-0012-hourly-autopilot
created_at: 2026-05-26T15:24:00Z
timezone: Asia/Seoul
paper: true
mode: hourly_autopilot
orders_submitted: 0
---

# 2026-05-27 00:12 KST hourly paper autopilot

## 결론

- 이번 run은 `blocked`다.
- `.env`의 `ALPACA_PAPER_TRADE=true`를 확인했다.
- Alpaca core는 이번에는 통과했다. 미국 동부 2026-05-26 11:14 기준 시장은 열려 있었고, 계좌 ACTIVE, 미체결 US equity 주문 0건, 당일 fill 0건, long position 10개를 확인했다.
- Universe strict gate는 통과했다. `harness/symbol-metadata.yaml`의 62개 metadata universe와 `SPY`/`QQQ`를 포함했다.
- Quote/spread는 최종 후보 `ASML`, `LLY`, `AAPL` 모두 20분 이내 fresh quote와 0.50% 이하 spread였다.
- 하지만 research MCP usable/pass가 SEC EDGAR와 Yahoo Finance 2개뿐이었다. Alpha Vantage `TOOL_CALL`은 schema 확인 후에도 cancelled, FRED/Firecrawl은 DNS 실패였다.
- 첫 차단 gate는 `mcp_research_min_confirmations`다. 최소 3개 research MCP usable/pass가 필요하므로 주문 계획은 빈 주문(`orders: []`)이고 Alpaca `place_stock_order`는 호출하지 않았다.

## Gate 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에 `ALPACA_PAPER_TRADE=true` 존재 |
| Automation lock | PASS | scheduled wrapper lock으로 판단 |
| Alpaca market clock | PASS | `is_open=true`, `2026-05-26T11:14:12-04:00` |
| Account/order/fill reconciliation | PASS | account ACTIVE, open orders 0, same-day fills 0 |
| Universe coverage | PASS | 62개 loaded, `SPY`/`QQQ` 포함 |
| MCP coverage strict | FAIL | research usable/pass 2개로 최소 3개 미달 |
| Quote freshness | PASS | 후보 quote `2026-05-26T15:17:50Z`-`15:17:51Z` |
| Spread | PASS for final candidates | ASML 0.372%, LLY 0.283%, AAPL 0.006% |
| Risk policy | PASS for empty plan | 신규 주문 0건 |
| Submit | BLOCKED | MCP strict fail 때문에 제출 금지 |

## Coordinator Agent

- Account value: 101301.19 USD.
- Cash: 44030.58 USD.
- Buying power: 138895.81 USD.
- Long market value: 57270.61 USD.
- Current positions: `AMD`, `AVGO`, `ETN`, `IONQ`, `LRCX`, `NOK`, `NVDA`, `RGTI`, `TSM`, `UNH`.
- Open orders and same-day fills were both empty.

## Universe Agent

- Universe source: `harness/symbol-metadata.yaml` 62개 심볼 + 현재 보유 종목 + `SPY`/`QQQ`.
- Alpaca snapshot retry 후 current quote/snapshot을 확인했다.
- Pre-MCP shortlist: `ASML`, `LLY`, `AAPL`, `SMH`, `FCX`.
- Final candidates: `ASML`, `LLY`, `AAPL`.
- `KLAC`, `LRCX`, `AMAT`, `MU`, `AMD`, `AVGO`는 semicap/AI 흐름이 강했지만 현재 IEX spread가 0.50%를 넘거나 기존 cluster 노출과 겹쳐 자동 buy 후보에서 제외했다.

## Market Data Agent

| 티커 | quote_time_utc | bid | ask | spread_pct | 판단 |
| --- | --- | ---: | ---: | ---: | --- |
| ASML | 2026-05-26T15:17:50Z | 1614.35 | 1620.36 | 0.372 | spread pass, final candidate |
| LLY | 2026-05-26T15:17:51Z | 1076.95 | 1080.00 | 0.283 | spread pass, final candidate |
| AAPL | 2026-05-26T15:17:51Z | 311.24 | 311.26 | 0.006 | spread pass, final candidate |
| SMH | 2026-05-26T15:17:51Z | 597.47 | 597.61 | 0.023 | spread pass, ETF overlap으로 보류 |
| FCX | 2026-05-26T15:17:51Z | 64.27 | 64.29 | 0.031 | spread pass, final에서 제외 |
| AMD | 2026-05-26T15:17:51Z | 490.49 | 493.00 | 0.510 | spread fail |
| KLAC | 2026-05-26T15:17:49Z | 1871.20 | 1989.08 | 6.107 | spread fail |
| AMAT | 2026-05-26T15:17:51Z | 451.19 | 454.00 | 0.621 | spread fail |
| LRCX | 2026-05-26T15:17:51Z | 303.85 | 326.00 | 7.034 | spread fail |
| MU | 2026-05-26T15:17:51Z | 870.00 | 874.46 | 0.511 | spread fail |

## Web Research Agent

Research MCPs were all attempted.

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | retry_count | gap_reason |
| --- | --- | --- | --- | --- | ---: | --- |
| Alpaca | true | true | pass | not_applicable | 1 | core checks, quotes, assets, news, movers usable |
| SEC EDGAR | true | true | pass | not_applicable | 0 | ASML/LLY/AAPL company info and filings usable; `SMH` ETF lookup empty_response noted separately |
| Alpha Vantage | true | false | failed | cancelled | 2 | `TOOL_LIST` and `TOOL_GET` succeeded, but `TOOL_CALL` cancelled twice |
| FRED | true | false | failed | dns | 2 | `api.stlouisfed.org` DNS failure after wrapper retries and probe |
| Firecrawl | true | false | failed | dns | 2 | `api.firecrawl.dev` DNS failure after wrapper retries and probe |
| Yahoo Finance | true | true | pass | not_applicable | 0 | ASML stock info, recommendations, and news usable |

## Trend Agent

| 순위 | 티커 | confidence | 판단 |
| ---: | --- | --- | --- |
| 1 | ASML | medium | Yahoo analyst mix는 strong-buy skew이고 SEC filings는 usable. 52주 고점 부근이라 추격 리스크가 있어 1주 validation 후보였지만 MCP confirmations 미달로 주문 불가 |
| 2 | LLY | medium | Alpaca news에 LDL gene-therapy Phase 1b headline이 있었고 spread는 양호. 최근 Form 144/Form 4/8-K 확인이 있어 catalyst와 filing risk를 같이 봐야 함 |
| 3 | AAPL | medium-low | quote/spread는 가장 깨끗하지만 Benzinga news는 mixed consumer/product context라 validation 우선순위는 낮음 |
| 4 | SMH | low | spread와 semiconductor beta는 양호하나 기존 AI semiconductor cluster 노출과 중복됨 |
| 5 | FCX | low | materials/mining 분산 후보지만 final thesis evidence가 ASML/LLY/AAPL보다 약함 |

## Portfolio/Risk Agent

- 신규 buy 주문: 없음.
- 신규 sell/trim 주문: 없음.
- AI semiconductor complex는 현재 대략 33.4k USD 수준이고 hard cap 45.6k USD 안쪽이다.
- Speculative exposure는 `IONQ` + `RGTI` 약 5.68k USD로 hard cap 12.16k USD 안쪽이다.
- 자동 trim 사유인 thesis-break, risk-limit, speculative cap exceed, cluster cap exceed, overheat profit protection은 이번 run에서 확인되지 않았다.
- Empty order plan risk check는 PASS했다.

## Executor Agent

주문 제출 없음. Alpaca MCP `place_stock_order`를 호출하지 않았다.

## Post-Trade Agent

제출 시도가 없고 open orders/fills도 없어서 주문 후 체결 대조는 발생하지 않았다. 다만 Alpaca MCP로 account, open orders, same-day fills, positions를 확인했고 `wiki/trade-ledger/positions/current.md`를 최신 계좌/포지션 값으로 갱신했다.

## Submitted Orders

| 티커 | side | qty | 결과 |
| --- | --- | ---: | --- |
| 없음 | - | 0 | research MCP hard gate 미통과 |

## Skipped Order Rationale

| 티커 | side | skip reason | 세부 rationale |
| --- | --- | --- | --- |
| ASML | buy | MCP research confirmations 2/3 | spread와 asset gate는 통과했고 Yahoo/SEC는 긍정적이나 Alpha/FRED/Firecrawl 실패로 자동 validation buy 제출 금지 |
| LLY | buy | MCP research confirmations 2/3 | Alpaca biotech headline과 SEC filings는 확인됐지만 3개 research MCP confirmation 미달 |
| AAPL | buy | 낮은 catalyst priority + MCP gate fail | quote/spread는 우수하나 news quality가 mixed이고 research confirmation 미달 |
| SMH | buy | ETF overlap + MCP gate fail | spread는 좋지만 기존 semiconductor cluster 노출과 중복되고 SEC ETF lookup은 empty_response |
| FCX | buy | final candidate 제외 | spread와 분산효과는 양호하나 current evidence가 ASML/LLY/AAPL보다 약함 |
| KLAC | buy | spread fail | current quote spread 6.107%로 정책 한도 0.50% 초과 |
| AMD | buy | spread fail + existing holding | current quote spread 0.510%로 한도 초과이고 이미 14주 보유 |
| LRCX | buy | spread fail + existing holding | current quote spread 7.034%로 한도 초과이고 이미 20주 보유 |
| AMAT | buy | spread fail | current quote spread 0.621%로 한도 초과 |
| MU | buy | spread fail | current quote spread 0.511%로 한도 초과 |
| 보유 전 종목 | sell | no valid sell catalyst | thesis-break, risk-limit, cap exceed가 확인되지 않았고 full research gate 미달 상태에서 임의 trim 금지 |

## No-action diagnostics

- First blocking gate: `mcp_research_min_confirmations`.
- Next safe recheck: Alpha Vantage `TOOL_CALL` cancellation recovery. SEC EDGAR와 Yahoo Finance는 이미 usable이므로 Alpha가 복구되면 research count가 3이 될 수 있다.
- Top recheck candidates: `ASML`, `LLY`, `AAPL`.
- Relaxation candidate: 없음. 현재 정책상 research minimum 3개는 hard gate이므로 이 run에서 완화하지 않는다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-27-0012-hourly-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-27-0012-hourly-autopilot.json`: FAIL
  - `research MCP gate requires at least 3 usable/pass research providers; got 2 (sec-edgar, yahoo-finance)`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-27-0012-hourly-autopilot.json`: PASS with `orders is empty`

## 산출물

- Raw source: [[2026-05-27-0012-hourly-autopilot-sources]]
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0012-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0012-hourly-autopilot.json`
- Portfolio snapshot: [[portfolio-current]]

## 지표 설명

- `universe coverage`: 추천 전 넓은 후보군을 실제로 살펴봤는지 보는 검증이다. 이번 run은 62개 metadata 심볼과 `SPY`/`QQQ`를 포함했다.
- `MCP coverage`: Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance가 의사결정 원천으로 usable한지 보는 gate다. 자동 buy는 Alpaca core pass와 research provider 3개 이상 pass가 필요하다.
- `quote freshness`: submit mode에서 주문 기준 quote가 20분 이내인지 보는 조건이다.
- `spread`: ask와 bid 차이를 중간가격으로 나눈 비율이다. 정책 한도는 0.50%다.
- `confidence`: 가격 추세, 뉴스/filing/analyst 확인, 리스크, 포트폴리오 적합성을 종합한 판단 신뢰도다. MCP 공백이 있으면 자동으로 낮춘다.
- `cluster exposure`: 비슷한 테마나 factor 종목이 포트폴리오에 과도하게 몰렸는지 보는 제한이다.
