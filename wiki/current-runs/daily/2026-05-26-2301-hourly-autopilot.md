---
id: 2026-05-26-2301-hourly-autopilot
created_at: 2026-05-26T14:01:10Z
timezone: Asia/Seoul
paper: true
mode: hourly_autopilot
orders_submitted: 0
---

# 2026-05-26 23:01 KST hourly paper autopilot

## 결론

- 이번 run은 `blocked`다.
- `.env`의 `ALPACA_PAPER_TRADE=true`는 확인했다.
- Alpaca MCP로 포지션, expanded universe 일봉, asset checks, candidate IEX quotes, market movers, Alpaca news는 일부 확인했다.
- 하지만 Alpaca core gate의 `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_watchlists`가 retry 후에도 `cancelled`였고 첫 차단 gate는 `alpaca_clock`이다.
- `LLY`, `LRCX`, `ASML`은 fresh quote가 있었지만 spread가 각각 10.46%, 9.16%, 0.66%로 정책 한도 0.50%를 넘었다.
- SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance는 usable confirmation을 만들지 못했다.
- 따라서 market-clock, Alpaca core, MCP strict, spread, account/order reconciliation gate가 실패했다. 주문 계획은 빈 주문(`orders: []`)이며 실제 paper 주문, 취소, 포지션 변경은 없다.

## Gate 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에 `ALPACA_PAPER_TRADE=true` 존재 |
| Automation lock | PASS | wrapper prompt와 동일한 invocation의 `.locks/hourly-autopilot.lock` 존재 |
| Alpaca market clock | FAIL | `get_clock` cancelled after retries |
| Account/order/fill reconciliation | FAIL | `get_account_info`, `get_orders`, `get_account_activities`, `get_watchlists` cancelled |
| Universe coverage | PASS | metadata universe 62개 loaded, `SPY`/`QQQ` 포함 |
| MCP coverage strict | FAIL | Alpaca core 실패, research provider usable count 0 |
| Quote freshness | PASS for checked candidates | 후보 5개 IEX quote는 약 2-3분 이내 |
| Spread | FAIL | `LLY`, `LRCX`, `ASML`이 0.50% 한도 초과 |
| Risk policy | PASS for empty plan | 신규 주문 0건 |
| Submit | BLOCKED | 위 실패 gate 때문에 주문 제출 금지 |

## Coordinator Agent

- 최근 위키와 정책을 확인했다.
- 최신 확인 가능한 Alpaca 포지션은 10개 long이다.
- `get_all_positions` 기준 long market value는 57,089.424 USD다.
- account cash/buying power는 이번 run에서 Alpaca account MCP가 실패해 새로 확인하지 못했다. Empty order plan에는 최근 위키 cash snapshot을 재사용했지만 submit 근거로 쓰지 않았다.

## Universe Agent

- universe source: `harness/symbol-metadata.yaml` 62개 심볼 + 보유 종목 + `SPY`/`QQQ`.
- 필수 benchmark `SPY`, `QQQ` 포함.
- Alpaca MCP `get_stock_bars`로 62개 심볼의 최근 IEX adjusted 일봉 응답을 확인했다.
- Pre-MCP shortlist: `LLY`, `LRCX`, `ASML`, `SMH`, `AAPL`.
- Final research candidates: `LLY`, `LRCX`, `ASML`.
- `RGTI`, `QBTS`, `IONQ`, `NOK`는 speculative/overheat guard로 신규 buy 후보에서 제외했다.

## Market Data Agent

| 티커 | quote_time_utc | bid | ask | spread_pct | 판단 |
| --- | --- | ---: | ---: | ---: | --- |
| LLY | 2026-05-26T13:58:13Z | 1021.25 | 1134.00 | 10.46 | fresh but spread fail |
| LRCX | 2026-05-26T13:58:24Z | 297.44 | 326.00 | 9.16 | fresh but spread fail |
| ASML | 2026-05-26T13:58:29Z | 1620.32 | 1631.01 | 0.66 | fresh but spread fail |
| SMH | 2026-05-26T13:58:40Z | 596.91 | 597.37 | 0.077 | quote/spread pass, final 제외 |
| AAPL | 2026-05-26T13:58:45Z | 310.49 | 310.54 | 0.016 | quote/spread pass, final 제외 |

Fresh quote가 있어도 `get_clock`와 account/order reconciliation이 실패하면 submit은 금지된다.

## Web Research Agent

이번 run은 required research MCP coverage가 실패했다. Alpaca news만 usable하다.

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | retry_count | gap_reason |
| --- | --- | --- | --- | --- | ---: | --- |
| Alpaca | true | false | failed | cancelled | 2 | positions/bars/assets/news/quotes 일부 usable, clock/account/orders/fills/watchlists/latest quote/snapshot 실패 |
| SEC EDGAR | true | false | failed | cancelled | 2 | CIK cache 사용 후 direct filing calls cancelled; `SMH` lookup은 `empty_response` |
| Alpha Vantage | true | false | failed | cancelled | 2 | `TOOL_LIST` cancelled |
| FRED | true | false | failed | dns | 2 | `api.stlouisfed.org` DNS failure |
| Firecrawl | true | false | failed | dns | 2 | `api.firecrawl.dev` DNS failure |
| Yahoo Finance | true | false | failed | cancelled | 2 | stock info/news/recommendations cancelled |

## Trend Agent

| 순위 | 티커 | confidence | 판단 |
| ---: | --- | --- | --- |
| 1 | LLY | medium | Alpaca biotech headline은 긍정적이나 spread와 all-MCP confirmation 부재로 자동 주문 불가 |
| 2 | LRCX | medium | 가격/섹터 흐름 우수, 기존 20주 보유와 AI semiconductor cluster 노출 때문에 추가 매수 보류 |
| 3 | ASML | medium | semicap/ADR momentum은 유지되지만 research MCP gap과 spread fail |
| 4 | SMH | low | spread는 양호하나 기존 반도체 exposure와 중복 |
| 5 | AAPL | low | spread는 양호하나 catalyst quality가 혼재하고 final candidate 제외 |

## Portfolio/Risk Agent

- 신규 buy 주문: 없음.
- 신규 sell/trim 주문: 없음.
- Sell/trim은 thesis-break, risk-limit, stale-thesis, position-sizing, portfolio-fit 근거가 필요하다. 이번 run은 Alpaca clock/account/open-order/fill 확인이 부족하므로 매도 판단도 제출하지 않는다.
- 기존 보유 종목 중 `RGTI`, `IONQ`, `NOK`는 고변동 상태라 추격 매수 금지다. 다만 자동 trim도 quote/order gate와 thesis-break 근거가 없어 보류한다.
- Empty order plan risk check는 PASS했다.

## Executor Agent

주문 제출 없음. Alpaca MCP `place_stock_order`를 호출하지 않았다.

## Post-Trade Agent

주문 제출 시도가 없었다. open order/fill reconciliation MCP가 실패했으므로 post-trade reconciliation은 제한적으로만 수행했다.

- 포지션은 Alpaca MCP `get_all_positions` 성공 결과로 확인했다.
- account cash, buying power, open orders, same-day fills는 이번 run에서 미확인이다.
- 실제 주문, 취소, 포지션 변경은 없다.

## Submitted Orders

| 티커 | side | qty | 결과 |
| --- | --- | ---: | --- |
| 없음 | - | 0 | 모든 hard gate 통과 전 제출 금지 |

## Skipped Order Rationale

| 티커 | side | skip reason | 세부 rationale |
| --- | --- | --- | --- |
| LLY | buy | Alpaca core/MCP/spread gate fail | Alpaca biotech headline은 긍정적이나 account/clock/order 및 SEC/Alpha/FRED/Firecrawl/Yahoo 확인이 없고 spread 10.46%라 자동 주문 불가 |
| LRCX | buy | Alpaca core/MCP/spread + concentration | 이미 20주 보유, semicap/AI semiconductor cluster 노출이 높고 spread 9.16%라 추가 매수 불가 |
| ASML | buy | Alpaca core/MCP/spread gate fail | 가격/섹터 흐름은 강하지만 filing/IR/analyst/macro 확인 실패, spread 0.66%로 정책 초과 |
| SMH | buy | final candidate 제외 + concentration | quote/spread는 통과했지만 ETF이고 기존 반도체 exposure와 중복되어 validation buy 후보에서 제외 |
| AAPL | buy | final candidate 제외 | quote/spread는 통과했지만 catalyst 혼재와 낮은 relative priority 때문에 제외 |
| 보유 전 종목 | sell | no valid sell catalyst | thesis-break 또는 risk-limit 근거를 Alpaca clock/order/fill state로 확인하지 못해 자동 매도 금지 |

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-26-2301-hourly-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-26-2301-hourly-autopilot.json`: FAIL
  - `alpaca: core MCP gate requires usable/pass outcome`
  - `research MCP gate requires at least 3 usable/pass research providers; got 0 (none)`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-26-2301-hourly-autopilot.json`: PASS with `orders is empty`

## 산출물

- Raw source: [[2026-05-26-2301-hourly-autopilot-sources]]
- Manifest: `wiki/evidence-store/run-manifests/2026-05-26-2301-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-26-2301-hourly-autopilot.json`

## 지표 설명

- `universe coverage`: 추천 전 넓은 후보군을 실제로 살펴봤는지 보는 검증이다. 이번 run은 62개 metadata 심볼과 `SPY`/`QQQ`를 포함했다.
- `MCP coverage`: Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance가 모두 usable한지 확인하는 gate다. 자동 주문은 Alpaca core pass와 buy 후보 기준 research provider 3개 이상 pass가 필요하다.
- `quote freshness`: submit mode에서는 quote/snapshot이 정책상 20분 이내여야 한다.
- `spread`: bid/ask 차이를 중간가격으로 나눈 비율이다. 정책 한도는 0.50%다.
- `confidence`: 가격, 뉴스/펀더멘털, 리스크/유동성, 포트폴리오 적합성을 합친 판단 신뢰도다. MCP 공백이 있으면 자동으로 낮춘다.
- `cluster exposure`: 비슷한 테마 종목이 포트폴리오에 과도하게 몰리는지 보는 제한이다.
