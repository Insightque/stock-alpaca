---
id: 2026-05-26-2124-hourly-autopilot-sources
source_type: alpaca|mcp|manual
captured_at: 2026-05-26T12:24:09Z
source_url: ""
tool: "Alpaca MCP, SEC EDGAR MCP, Alpha Vantage MCP, FRED MCP, Firecrawl MCP, Yahoo Finance MCP"
tickers: [LLY, LRCX, ASML, AAPL, SMH, SPY, QQQ, AMD, AVGO, ETN, IONQ, NOK, NVDA, RGTI, TSM, UNH]
immutable: true
---

# 2026-05-26 21:24 KST hourly autopilot 원천

## 요약

- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했다. API key 값은 출력하거나 기록하지 않았다.
- `.locks/hourly-autopilot.lock`은 이미 존재했다. 현재 invocation 시각과 맞아 scheduled wrapper가 잡은 lock으로 보고 workflow를 계속했다.
- Alpaca MCP 성공:
  - `get_all_positions`: 10개 long 포지션 확인. 총 long market value는 57,234.123 USD, 총 미실현 손익은 약 1,264.703 USD.
  - `get_stock_bars`: `harness/symbol-metadata.yaml` 62개 심볼 전체에 대해 IEX adjusted 1Day bar를 요청했고 응답을 받았다. `SPY`, `QQQ` 포함.
  - `get_asset`: `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH` 중 retry 후 전부 `status=active`, `tradable=true`, `class=us_equity` 확인.
  - `get_market_movers`: 마지막 갱신 `2026-05-22T23:59:00.130378898Z`, 저가/투기 mover 다수 확인.
  - `get_news`: `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH` 관련 Alpaca/Benzinga 뉴스 20건 수집.
  - `get_stock_quotes`: `SPY`는 2026-05-26T12:20:41Z 전후 IEX bid/ask가 있었지만, `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH`는 최근 20분 후보별 quote 응답이 비어 있었다.
- Alpaca MCP 실패 또는 unusable:
  - in-session `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_watchlists`, `get_calendar`, `get_stock_latest_quote`, `get_stock_snapshot`, `get_stock_latest_bar`, `get_most_active_stocks`는 `user cancelled MCP tool call`.
  - repo-local Alpaca MCP fallback은 현재 Python environment에 `mcp` package가 없어 실행하지 못했다. 직접 REST 호출은 하지 않았다.
- Research MCP 실패:
  - SEC EDGAR direct MCP `get_financials`와 `get_insider_summary`는 retry 후에도 `user cancelled MCP tool call`.
  - Alpha Vantage direct MCP `TOOL_LIST`는 retry 후에도 `user cancelled MCP tool call`.
  - FRED local MCP `get_macro_snapshot`은 `api.stlouisfed.org` DNS resolution failure.
  - Firecrawl local MCP `firecrawl_scrape`은 `api.firecrawl.dev` DNS resolution failure.
  - Yahoo Finance direct MCP `get_stock_info`, `get_yahoo_finance_news`, `get_recommendations`는 `user cancelled MCP tool call`.
- 따라서 Alpaca core MCP gate, MCP strict gate, quote gate, spread gate, account/order reconciliation gate가 실패했다. 주문 후보와 제출 주문은 0건이다.

## Alpaca 포지션

| ticker | qty | current_price | market_value | unrealized_pl |
| --- | ---: | ---: | ---: | ---: |
| AMD | 14 | 482.00 | 6748.00 | 269.78 |
| AVGO | 15 | 416.7258 | 6250.887 | 89.937 |
| ETN | 15 | 399.20 | 5988.00 | 169.50 |
| IONQ | 45 | 64.78 | 2915.10 | 58.50 |
| LRCX | 20 | 314.00 | 6280.00 | 121.80 |
| NOK | 400 | 15.71 | 6284.00 | 268.00 |
| NVDA | 35 | 218.08 | 7632.80 | 96.60 |
| RGTI | 120 | 26.2553 | 3150.636 | 82.28604 |
| TSM | 15 | 412.00 | 6180.00 | 102.00 |
| UNH | 15 | 386.98 | 5804.70 | 6.30 |

Account cash와 buying power는 이번 run에서 Alpaca account MCP가 실패해 새로 확인하지 못했다. Empty-order validation에는 최근 wiki/account snapshot의 cash 44,030.58 USD와 buying power 138,261.25 USD를 보수적으로 재사용했고, submit 근거로 사용하지 않았다.

## Universe와 시그널

- Universe source: `harness/symbol-metadata.yaml` 62개 심볼 + 보유 포지션 + `SPY`/`QQQ`.
- Pre-MCP shortlist: `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH`.
- Final research candidates: `LLY`, `LRCX`, `ASML`.
- `QBTS`, `RGTI`, `IONQ`, `NOK` 등 고모멘텀/투기 후보는 overheat/speculative guard로 신규 buy 후보에서 제외했다.

| ticker | 2026-05-15 close | 2026-05-22 close | signal | confidence | notes |
| --- | ---: | ---: | --- | --- | --- |
| LLY | 1004.695 | 1065.60 | price momentum + Alpaca biotech headlines | medium | Research MCP와 fresh quote/spread 실패로 주문 불가 |
| LRCX | 284.37 | 305.43 | semicap momentum | medium | 기존 보유 20주, AI semiconductor cluster 노출 |
| ASML | 1501.52 | 1632.98 | semicap/ADR momentum | medium | ADR/semicap 후보, filing/IR/analyst 확인 실패 |
| AAPL | 300.19 | 308.81 | mega-cap momentum | low | 최종 후보 제외, news catalyst 혼재 |
| SMH | 556.85 | 575.91 | semiconductor ETF momentum | low | 기존 반도체 노출과 중복 |
| SPY | 739.10 | 745.67 | benchmark | medium | Universe benchmark |
| QQQ | 708.91 | 717.49 | benchmark | medium | Universe benchmark |

## Alpaca News Highlights

- `LLY`: 2026-05-26 Eli Lilly의 Curevo, LimmaTech 등 백신 개발사 인수 headline, 2026-05-25 VERVE-102 Phase 1b data headline.
- `AAPL`: 2026-05-26 iPhone 17e 일본 판매 둔화, Apple peer comparison, Ferrari EV/Jony Ive 관련 headline.
- `ASML`: Alpaca 20건 응답 내 직접 headline은 제한적이었다. 가격/섹터 momentum 중심 시그널이므로 research MCP 공백 시 confidence를 낮춘다.
- `SMH`: Alpaca 20건 응답 내 직접 headline은 제한적이었다. 기존 AI semiconductor cluster와 중복된다.
- `LRCX`: direct recent Alpaca news in the 20-row response was sparse; thesis remains price/sector-led and therefore lower confidence without research MCP confirmation.

## 데이터 공백

- Alpaca clock/account/orders/fills/watchlist/latest quote/snapshot/latest bar reads were not usable, so submit mode is blocked.
- Latest quote, bid, ask, quote age, and spread are missing for all order candidates.
- SEC EDGAR, Alpha Vantage, Yahoo Finance, FRED, and Firecrawl coverage are not usable in this run.
- Market clock is recorded as unavailable. Order plan uses `is_open=false` as a safety default, not as a sourced market-clock assertion.
- Candidate quotes were empty even though `SPY` had fresh IEX quote rows. This blocks buy and sell submissions because per-symbol spread could not be validated.

## 위키 반영 메모

- `wiki/current-runs/daily/2026-05-26-2124-hourly-autopilot.md`에 blocked 결과와 gate failures를 기록한다.
- `wiki/trade-ledger/orders/2026-05-26-2124-hourly-autopilot.json`은 empty-order dry-run plan이다.
- `wiki/evidence-store/run-manifests/2026-05-26-2124-hourly-autopilot.json`은 universe pass, MCP strict fail을 기록한다.
