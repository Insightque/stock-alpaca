---
id: 2026-05-26-2331-hourly-autopilot
created_at: 2026-05-26T14:35:23Z
timezone: Asia/Seoul
paper: true
mode: hourly_autopilot
orders_submitted: 0
---

# 2026-05-26 23:31 KST hourly paper autopilot

## 결론

- 이번 run은 `blocked`다.
- `.env`의 `ALPACA_PAPER_TRADE=true`는 확인했다.
- Alpaca MCP로 broad universe 일봉과 후보 IEX historical quote는 확인했다.
- 하지만 Alpaca core gate의 `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, `get_stock_latest_quote`, `get_stock_snapshot`이 retry 후에도 `cancelled`였고 첫 차단 gate는 `alpaca_clock`이다.
- `LLY`, `ASML`, `SMH`, `AAPL`은 fresh quote와 spread가 통과했지만, clock/account/order/position reconciliation과 research MCP gate가 실패해 validation buy도 제출할 수 없다.
- `LRCX`는 fresh quote가 있었지만 spread 9.16%로 정책 한도 0.50%를 넘었다.
- 주문 계획은 빈 주문(`orders: []`)이며 실제 paper 주문, 취소, 포지션 변경은 없다.

## Gate 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에 `ALPACA_PAPER_TRADE=true` 존재 |
| Automation lock | PASS | wrapper prompt와 동일한 invocation의 `.locks/hourly-autopilot.lock` 존재 |
| Alpaca market clock | FAIL | `get_clock` cancelled after retries |
| Account/order/fill/position reconciliation | FAIL | `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists` cancelled |
| Universe coverage | PASS | metadata universe 62개 loaded, `SPY`/`QQQ` 포함 |
| MCP coverage strict | FAIL | Alpaca core 실패, research provider usable count 0 |
| Quote freshness | PASS for checked candidates | 후보 5개 IEX quote는 약 3분 이내 |
| Spread | MIXED | `LLY`, `ASML`, `SMH`, `AAPL` pass; `LRCX` fail |
| Risk policy | PASS for empty plan | 신규 주문 0건 |
| Submit | BLOCKED | 위 실패 gate 때문에 주문 제출 금지 |

## Coordinator Agent

- 최근 위키와 정책을 확인했다.
- 이번 run에서 Alpaca account/positions/open orders/fills는 새로 확인하지 못했다.
- Empty order plan에는 23:01 same-day wiki snapshot의 account/positions를 보수적으로 재사용했지만, submit 근거로 쓰지 않았다.
- Market clock은 sourced confirmation이 없으므로 order plan에서 `market.is_open=false` safety default로 처리했다.

## Universe Agent

- universe source: `harness/symbol-metadata.yaml` 62개 심볼 + 보유 종목 + `SPY`/`QQQ`.
- 필수 benchmark `SPY`, `QQQ` 포함.
- Alpaca MCP `get_stock_bars`로 62개 심볼의 최근 IEX adjusted 일봉 응답을 확인했다.
- Pre-MCP shortlist: `LLY`, `LRCX`, `ASML`, `SMH`, `AAPL`.
- Final research candidates: `LLY`, `LRCX`, `ASML`.
- `RGTI`, `QBTS`, `IONQ`, `NOK`는 speculative/overheat guard로 신규 buy 후보에서 제외한다.

## Market Data Agent

| 티커 | quote_time_utc | bid | ask | spread_pct | 판단 |
| --- | --- | ---: | ---: | ---: | --- |
| LLY | 2026-05-26T14:32:29Z | 1063.26 | 1064.65 | 0.131 | fresh, spread pass, core/MCP fail |
| LRCX | 2026-05-26T14:32:35Z | 297.44 | 326.00 | 9.16 | fresh but spread fail |
| ASML | 2026-05-26T14:32:39Z | 1635.51 | 1641.34 | 0.356 | fresh, spread pass, core/MCP fail |
| SMH | 2026-05-26T14:32:42Z | 601.68 | 601.74 | 0.010 | quote/spread pass, final 제외 |
| AAPL | 2026-05-26T14:32:48Z | 311.60 | 311.62 | 0.006 | quote/spread pass, final 제외 |

Fresh quote가 있어도 `get_clock`와 account/order/position reconciliation이 실패하면 submit은 금지된다.

## Web Research Agent

이번 run은 required research MCP coverage가 실패했다. Alpaca news도 23:31 재조회에서는 cancelled였으므로, 새로운 이벤트 근거를 점수에 반영하지 않았다.

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | retry_count | gap_reason |
| --- | --- | --- | --- | --- | ---: | --- |
| Alpaca | true | false | failed | cancelled | 2 | broad bars/quotes 일부 usable, clock/account/orders/positions/fills/watchlists/latest quote/snapshot/asset/news/movers 실패 |
| SEC EDGAR | true | false | failed | cancelled | 2 | CIK cache 사용 후 direct filing calls cancelled; `SMH` lookup은 `empty_response` |
| Alpha Vantage | true | false | failed | cancelled | 2 | `TOOL_LIST` cancelled |
| FRED | true | false | failed | dns | 2 | `api.stlouisfed.org` DNS failure |
| Firecrawl | true | false | failed | dns | 2 | `api.firecrawl.dev` DNS failure |
| Yahoo Finance | true | false | failed | cancelled | 2 | `get_stock_info(LLY)` cancelled |

## Trend Agent

| 순위 | 티커 | confidence | 판단 |
| ---: | --- | --- | --- |
| 1 | LLY | medium | quote/spread는 개선됐지만 SEC/Alpha/FRED/Firecrawl/Yahoo confirmation과 Alpaca account/clock/order state가 없어 자동 주문 불가 |
| 2 | ASML | medium | semicap/ADR momentum은 유지되고 spread도 통과했지만 research MCP gap과 core gate 실패 |
| 3 | LRCX | medium | 가격/섹터 흐름 우수, 기존 20주 보유와 AI semiconductor cluster 노출, spread 9.16%로 추가 매수 불가 |
| 4 | SMH | low | spread는 양호하나 기존 반도체 exposure와 중복 |
| 5 | AAPL | low | spread는 양호하나 catalyst quality가 혼재하고 final candidate 제외 |

## Portfolio/Risk Agent

- 신규 buy 주문: 없음.
- 신규 sell/trim 주문: 없음.
- Sell/trim은 thesis-break, risk-limit, stale-thesis, position-sizing, portfolio-fit 근거가 필요하다. 이번 run은 Alpaca clock/account/open-order/fill/position 확인이 부족하므로 매도 판단도 제출하지 않는다.
- `LLY`와 `ASML`은 quote/spread만 보면 validation buy recheck 후보지만, Alpaca core와 최소 3개 research MCP confirmation이 회복되기 전까지 `blocked`다.
- Empty order plan risk check는 PASS했다.

## Executor Agent

주문 제출 없음. Alpaca MCP `place_stock_order`를 호출하지 않았다.

## Post-Trade Agent

주문 제출 시도가 없었다. open order/fill/account/position reconciliation MCP가 실패했으므로 post-trade reconciliation은 수행하지 못했다.

- account cash, buying power, current positions, open orders, same-day fills는 이번 run에서 미확인이다.
- 실제 주문, 취소, 포지션 변경은 없다.

## Submitted Orders

| 티커 | side | qty | 결과 |
| --- | --- | ---: | --- |
| 없음 | - | 0 | 모든 hard gate 통과 전 제출 금지 |

## Skipped Order Rationale

| 티커 | side | skip reason | 세부 rationale |
| --- | --- | --- | --- |
| LLY | buy | Alpaca core/MCP gate fail | spread는 0.131%로 통과했지만 clock/account/order/position 및 SEC/Alpha/FRED/Firecrawl/Yahoo 확인이 없어 자동 주문 불가 |
| ASML | buy | Alpaca core/MCP gate fail | spread는 0.356%로 통과했지만 filing/IR/analyst/macro 확인 실패, account/order state 미확인 |
| LRCX | buy | Alpaca core/MCP/spread + concentration | 이미 20주 보유, semicap/AI semiconductor cluster 노출이 높고 spread 9.16%라 추가 매수 불가 |
| SMH | buy | final candidate 제외 + concentration | quote/spread는 통과했지만 ETF이고 기존 반도체 exposure와 중복되어 validation buy 후보에서 제외 |
| AAPL | buy | final candidate 제외 | quote/spread는 통과했지만 catalyst 혼재와 낮은 relative priority 때문에 제외 |
| 보유 전 종목 | sell | no valid sell catalyst | thesis-break 또는 risk-limit 근거를 Alpaca clock/order/fill/position state로 확인하지 못해 자동 매도 금지 |

## 검증

- `python3 scripts/check-universe-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-26-2331-hourly-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-26-2331-hourly-autopilot.json`: FAIL
  - `alpaca: core MCP gate requires usable/pass outcome`
  - `research MCP gate requires at least 3 usable/pass research providers; got 0 (none)`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-26-2331-hourly-autopilot.json`: PASS with `orders is empty`

## 산출물

- Raw source: [[2026-05-26-2331-hourly-autopilot-sources]]
- Manifest: `wiki/evidence-store/run-manifests/2026-05-26-2331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-26-2331-hourly-autopilot.json`

## 지표 설명

- `universe coverage`: 추천 전 넓은 후보군을 실제로 살펴봤는지 보는 검증이다. 이번 run은 62개 metadata 심볼과 `SPY`/`QQQ`를 포함했다.
- `MCP coverage`: Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance가 모두 usable한지 확인하는 gate다. 자동 주문은 Alpaca core pass와 buy 후보 기준 research provider 3개 이상 pass가 필요하다.
- `quote freshness`: submit mode에서는 quote/snapshot이 정책상 20분 이내여야 한다.
- `spread`: bid/ask 차이를 중간가격으로 나눈 비율이다. 정책 한도는 0.50%다.
- `confidence`: 가격, 뉴스/펀더멘털, 리스크/유동성, 포트폴리오 적합성을 합친 판단 신뢰도다. MCP 공백이 있으면 자동으로 낮춘다.
- `cluster exposure`: 비슷한 테마 종목이 포트폴리오에 과도하게 몰리는지 보는 제한이다.
