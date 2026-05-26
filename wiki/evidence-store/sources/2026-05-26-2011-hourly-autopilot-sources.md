---
id: 2026-05-26-2011-hourly-autopilot-sources
source_type: alpaca|mcp|manual
captured_at: 2026-05-26T11:11:14Z
source_url: ""
tool: "Alpaca MCP, SEC EDGAR MCP, Alpha Vantage MCP, FRED MCP, Firecrawl MCP, Yahoo Finance MCP"
tickers: [LLY, LRCX, ASML, AAPL, SMH, SPY, QQQ, AMD, AVGO, ETN, IONQ, NOK, NVDA, RGTI, TSM, UNH]
immutable: true
---

# 2026-05-26 20:11 KST hourly autopilot 원천

## 요약

- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했다. API key 값은 출력하거나 기록하지 않았다.
- `.locks/hourly-autopilot.lock`은 이미 존재했다. wrapper가 잡은 lock으로 보이는 시각이라 workflow를 계속했다.
- Alpaca MCP 성공:
  - `get_all_positions`: 10개 long 포지션 확인. 총 long market value는 57,209.83 USD, 총 미실현 손익은 1,240.41 USD.
  - `get_market_movers`: 마지막 갱신 `2026-05-22T23:59:00.130378898Z`, 저가/투기 mover 다수 확인.
  - `get_stock_bars`: `harness/symbol-metadata.yaml` 62개 심볼 전체에 대해 IEX adjusted 1Day bar를 요청했고 응답을 받았다. `SPY`, `QQQ` 포함.
  - `get_asset`: `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH`, `SPY`, `QQQ` 모두 `status=active`, `tradable=true`, `class=us_equity` 확인.
  - `get_news`: `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH` 관련 Benzinga/Alpaca 뉴스 20건 수집.
- Alpaca MCP 실패 또는 unusable:
  - in-session `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_watchlists`, `get_stock_latest_quote`, `get_stock_snapshot`, `get_stock_latest_bar`, `get_calendar`는 `user cancelled MCP tool call`.
  - repo-local stdio Alpaca MCP `get_clock`는 DNS 오류 `nodename nor servname provided, or not known`을 반환했다.
- Research MCP 실패:
  - SEC EDGAR direct MCP는 취소됐고, repo-local SEC EDGAR MCP `get_recent_filings`는 `LLY` ticker에 대해 `Company 'LLY' not found`를 반환했다.
  - Alpha Vantage local MCP는 `TOOL_LIST`와 `TOOL_GET(EARNINGS)`까지 성공했지만 `TOOL_CALL(EARNINGS, LLY)`에서 DNS 오류 `[Errno 8] nodename nor servname provided, or not known`을 반환했다.
  - FRED local MCP `get_macro_snapshot`은 `api.stlouisfed.org` DNS resolution failure.
  - Firecrawl local MCP `firecrawl_scrape`은 `api.firecrawl.dev` DNS resolution failure.
  - Yahoo Finance direct MCP는 취소됐고, repo-local wrapper는 `Git operation failed`로 dependency fetch가 실패했다.
- 따라서 Alpaca core MCP gate, MCP strict gate, quote gate, spread gate, account/order reconciliation gate가 실패했다. 주문 후보와 제출 주문은 0건이다.

## Alpaca 포지션

| ticker | qty | current_price | market_value | unrealized_pl |
| --- | ---: | ---: | ---: | ---: |
| AMD | 14 | 480.88 | 6732.32 | 254.10 |
| AVGO | 15 | 416.19 | 6242.85 | 81.90 |
| ETN | 15 | 397.60 | 5964.00 | 145.50 |
| IONQ | 45 | 65.54 | 2949.30 | 92.70 |
| LRCX | 20 | 313.00 | 6260.00 | 101.80 |
| NOK | 400 | 15.6804 | 6272.16 | 256.16 |
| NVDA | 35 | 217.68 | 7618.80 | 82.60 |
| RGTI | 120 | 26.46 | 3175.20 | 106.85004 |
| TSM | 15 | 411.88 | 6178.20 | 100.20 |
| UNH | 15 | 387.80 | 5817.00 | 18.60 |

Account cash와 buying power는 이번 run에서 Alpaca account MCP가 실패해 새로 확인하지 못했다. Empty-order validation에는 최근 위키에서 확인된 cash 44,030.58 USD와 buying power 138,261.25 USD를 보수적으로 재사용했고, submit 근거로 사용하지 않았다.

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

- `LLY`: 2026-05-25 VERVE-102 Phase 1b data headline, 2026-05-22 Foundayo Phase 3 ATTAIN-1/ATTAIN-2 headline.
- `AAPL`: 2026-05-25 Mag-7/market commentary, Apple competitor analysis, Google/Apple default-deal legal headline.
- `ASML`: 2026-05-22 China semiconductor export/AI demand headline.
- `SMH`: 2026-05-22 Dow/AI rally and quantum ETF headlines.
- `LRCX`: direct recent Alpaca news in the 20-row response was sparse; thesis remains price/sector-led and therefore lower confidence without research MCP confirmation.

## 데이터 공백

- Alpaca clock/account/orders/fills/watchlist/latest quote/snapshot/latest bar reads were not usable, so submit mode is blocked.
- Latest quote, bid, ask, quote age, and spread are missing for all order candidates.
- SEC EDGAR, Alpha Vantage, Yahoo Finance, FRED, and Firecrawl coverage are not usable in this run.
- Market clock is recorded as unavailable. Order plan uses `is_open=false` as a safety default, not as a sourced market-clock assertion.

## 위키 반영 메모

- `wiki/current-runs/daily/2026-05-26-2011-hourly-autopilot.md`에 blocked 결과와 gate failures를 기록한다.
- `wiki/trade-ledger/orders/2026-05-26-2011-hourly-autopilot.json`은 empty-order dry-run plan이다.
- `wiki/evidence-store/run-manifests/2026-05-26-2011-hourly-autopilot.json`은 universe pass, MCP strict fail을 기록한다.
