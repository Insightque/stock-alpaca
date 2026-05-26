---
id: 2026-05-27-0032-hourly-autopilot
created_at: 2026-05-26T15:43:00Z
timezone: Asia/Seoul
paper: true
mode: hourly_autopilot
orders_submitted: 0
---

# 2026-05-27 00:32 KST hourly paper autopilot

## 결론

- 이번 run은 `blocked`다.
- `.env`의 `ALPACA_PAPER_TRADE=true`를 확인했다.
- Alpaca core는 통과했다. 미국 동부 2026-05-26 11:33 기준 시장은 열려 있었고, 계좌 ACTIVE, 미체결 US equity 주문 0건, 당일 fill 0건, long position 10개를 확인했다.
- Universe strict gate는 통과했다. `harness/symbol-metadata.yaml`의 62개 metadata universe와 `SPY`/`QQQ`를 포함했다.
- Quote/spread는 최종 후보 `LLY`, `AMD`, `MU` 모두 20분 이내 fresh quote와 0.50% 이하 spread였다.
- 하지만 research MCP usable/pass가 SEC EDGAR와 Yahoo Finance 2개뿐이었다. Alpha Vantage `TOOL_CALL`은 schema 확인 후에도 cancelled, FRED/Firecrawl은 DNS 실패였다.
- 첫 차단 gate는 `mcp_research_min_confirmations`다. 최소 3개 research MCP usable/pass가 필요하므로 주문 계획은 빈 주문(`orders: []`)이고 Alpaca `place_stock_order`는 호출하지 않았다.

## Gate 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에 `ALPACA_PAPER_TRADE=true` 존재 |
| Automation lock | PASS | scheduled wrapper lock으로 판단 |
| Alpaca market clock | PASS | `is_open=true`, `2026-05-26T11:33:01-04:00` |
| Account/order/fill reconciliation | PASS | account ACTIVE, open orders 0, same-day fills 0 |
| Universe coverage | PASS | 62개 loaded, `SPY`/`QQQ` 포함 |
| MCP coverage strict | FAIL | research usable/pass 2개로 최소 3개 미달 |
| Quote freshness | PASS | 후보 quote `2026-05-26T15:35:37Z`-`15:35:39Z` |
| Spread | PASS for final candidates | LLY 0.274%, AMD 0.352%, MU 0.049% |
| Risk policy | PASS for empty plan | 신규 주문 0건 |
| Submit | BLOCKED | MCP strict fail 때문에 제출 금지 |

## Coordinator Agent

- Account value: 101264.45 USD.
- Cash: 44030.58 USD.
- Buying power: 138855.03 USD.
- Long market value: 57233.87 USD.
- Current positions: `AMD`, `AVGO`, `ETN`, `IONQ`, `LRCX`, `NOK`, `NVDA`, `RGTI`, `TSM`, `UNH`.
- Open orders and same-day fills were both empty.

## Universe Agent

- Universe source: `harness/symbol-metadata.yaml` 62개 심볼 + 현재 보유 종목 + Alpaca watchlists + `SPY`/`QQQ`.
- Alpaca watchlists는 비어 있었다.
- Pre-MCP shortlist: `MU`, `AMD`, `KLAC`, `SMH`, `INTC`, `AAPL`, `LLY`, `NOK`, `ASML`, `AMAT`.
- Final candidates: `LLY`, `AMD`, `MU`.
- `KLAC`, `ASML`, `AMAT`, `LRCX`, `ETN`은 current IEX spread가 0.50%를 넘어 자동 buy 후보에서 제외했다. `SMH`는 spread는 좋지만 기존 AI semiconductor cluster와 중복되고 ETF라 validation 우선순위를 낮췄다.

## Market Data Agent

| 티커 | quote_time_utc | bid | ask | spread_pct | 판단 |
| --- | --- | ---: | ---: | ---: | --- |
| LLY | 2026-05-26T15:35:37Z | 1077.04 | 1080.00 | 0.274 | spread pass, final candidate |
| AMD | 2026-05-26T15:35:39Z | 491.27 | 493.00 | 0.352 | spread pass, final candidate, existing holding |
| MU | 2026-05-26T15:35:39Z | 876.64 | 877.07 | 0.049 | spread pass, final candidate, overheat risk |
| SMH | 2026-05-26T15:35:39Z | 597.46 | 597.89 | 0.072 | spread pass, ETF overlap으로 보류 |
| INTC | 2026-05-26T15:35:39Z | 122.65 | 122.72 | 0.057 | spread pass, lower-quality semiconductor turnaround risk |
| AAPL | 2026-05-26T15:35:39Z | 311.50 | 311.54 | 0.013 | spread pass, catalyst priority 낮음 |
| KLAC | 2026-05-26T15:35:22Z | 1968.93 | 1984.14 | 0.770 | spread fail |
| ASML | 2026-05-26T15:35:29Z | 1607.12 | 1628.10 | 1.297 | spread fail |
| AMAT | 2026-05-26T15:35:24Z | 449.24 | 454.00 | 1.054 | spread fail |
| LRCX | 2026-05-26T15:35:39Z | 303.85 | 326.00 | 7.034 | spread fail |

## Web Research Agent

Research MCPs were all attempted.

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | retry_count | gap_reason |
| --- | --- | --- | --- | --- | ---: | --- |
| Alpaca | true | true | pass | not_applicable | 0 | core checks, quotes, assets, news, movers usable |
| SEC EDGAR | true | true | pass | not_applicable | 0 | LLY/AMD/MU company info and filings usable; `SMH` ETF lookup empty_response noted separately |
| Alpha Vantage | true | false | failed | cancelled | 2 | `TOOL_LIST` and `TOOL_GET` succeeded, but `TOOL_CALL` cancelled twice |
| FRED | true | false | failed | dns | 2 | `api.stlouisfed.org` DNS failure after wrapper retries and probe |
| Firecrawl | true | false | failed | dns | 2 | `api.firecrawl.dev` DNS failure after wrapper retries and probe |
| Yahoo Finance | true | true | pass | not_applicable | 0 | LLY/AMD/MU stock info, recommendations, and news usable |

## Trend Agent

| 순위 | 티커 | confidence | 판단 |
| ---: | --- | --- | --- |
| 1 | LLY | medium | 20D 추세가 SPY/QQQ를 앞서고 healthcare growth로 portfolio cluster를 분산한다. Alpaca/Yahoo news는 vaccine acquisition과 LDL gene-therapy context를 제공한다. 자동 validation 후보였지만 MCP confirmations 미달로 주문 불가 |
| 2 | AMD | medium | AI semiconductor 보유 핵심 종목이고 5D/20D momentum이 강하다. 다만 이미 보유 중이고 cluster exposure가 높아 추가매수는 MCP/risk gate가 완전히 열릴 때만 가능 |
| 3 | MU | medium-low | 가장 강한 momentum과 Yahoo/Alpaca AI-memory catalyst가 있으나 45D +100% 이상, 당일 +16%대라 adverse move 위험이 커서 1주 validation 외 추격은 부적합 |
| 4 | SMH | low | spread와 semiconductor beta는 양호하나 기존 AI semiconductor cluster 노출과 중복된다 |
| 5 | AAPL | low | quote/spread는 가장 깨끗하지만 current catalyst가 약하고 final thesis priority가 낮다 |

## Portfolio/Risk Agent

- 신규 buy 주문: 없음.
- 신규 sell/trim 주문: 없음.
- AI semiconductor complex는 현재 약 33.26k USD 수준이고 hard cap 45.57k USD 안쪽이다.
- Speculative exposure는 `IONQ` + `RGTI` 약 5.74k USD로 hard cap 12.15k USD 안쪽이다.
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
| LLY | buy | MCP research confirmations 2/3 | spread와 asset gate는 통과했고 SEC/Yahoo/Alpaca catalyst는 usable하지만 Alpha/FRED/Firecrawl 실패로 자동 validation buy 제출 금지 |
| AMD | buy | MCP gate fail + existing holding | trend와 spread는 통과했지만 이미 14주 보유하고 있고 research confirmation 미달 |
| MU | buy | MCP gate fail + overheat risk | AI-memory catalyst와 spread는 강하지만 당일/45D 급등으로 adverse move risk가 커서 gate 완전 통과 전 추격 금지 |
| SMH | buy | ETF overlap + MCP gate fail | spread는 좋지만 기존 semiconductor cluster 노출과 중복되고 SEC ETF lookup은 empty_response |
| INTC | buy | final candidate 제외 | spread는 좋지만 turnaround/quality risk가 LLY/AMD/MU보다 커 final 후보에서 제외 |
| AAPL | buy | 낮은 catalyst priority + MCP gate fail | quote/spread는 우수하나 current catalyst strength가 낮고 research confirmation 미달 |
| KLAC | buy | spread fail | current quote spread 0.770%로 정책 한도 0.50% 초과 |
| ASML | buy | spread fail | current quote spread 1.297%로 정책 한도 초과 |
| AMAT | buy | spread fail | current quote spread 1.054%로 정책 한도 초과 |
| LRCX | buy | spread fail + existing holding | current quote spread 7.034%로 한도 초과이고 이미 20주 보유 |
| 보유 전 종목 | sell | no valid sell catalyst | thesis-break, risk-limit, cap exceed가 확인되지 않았고 임의 trim 금지 |

## No-action diagnostics

- First blocking gate: `mcp_research_min_confirmations`.
- Next safe recheck: Alpha Vantage `TOOL_CALL` cancellation recovery. SEC EDGAR와 Yahoo Finance는 이미 usable이므로 Alpha가 복구되면 research count가 3이 될 수 있다.
- Top recheck candidates: `LLY`, `AMD`, `MU`.
- Relaxation candidate: 없음. 현재 정책상 research minimum 3개는 hard gate이므로 이 run에서 완화하지 않는다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-27-0032-hourly-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-27-0032-hourly-autopilot.json`: FAIL
  - `research MCP gate requires at least 3 usable/pass research providers; got 2 (sec-edgar, yahoo-finance)`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-27-0032-hourly-autopilot.json`: PASS with `orders is empty`

## 산출물

- Raw source: [[2026-05-27-0032-hourly-autopilot-sources]]
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0032-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0032-hourly-autopilot.json`
- Portfolio snapshot: [[portfolio-current]]

## 지표 설명

- `universe coverage`: 추천 전 넓은 후보군을 실제로 살펴봤는지 보는 검증이다. 이번 run은 62개 metadata 심볼과 `SPY`/`QQQ`를 포함했다.
- `MCP coverage`: Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance가 의사결정 원천으로 usable한지 보는 gate다. 자동 buy는 Alpaca core pass와 research provider 3개 이상 pass가 필요하다.
- `quote freshness`: submit mode에서 주문 기준 quote가 20분 이내인지 보는 조건이다.
- `spread`: ask와 bid 차이를 중간가격으로 나눈 비율이다. 정책 한도는 0.50%다.
- `confidence`: 가격 추세, 뉴스/filing/analyst 확인, 리스크, 포트폴리오 적합성을 종합한 판단 신뢰도다. MCP 공백이 있으면 자동으로 낮춘다.
- `cluster exposure`: 비슷한 테마나 factor 종목이 포트폴리오에 과도하게 몰렸는지 보는 제한이다.
