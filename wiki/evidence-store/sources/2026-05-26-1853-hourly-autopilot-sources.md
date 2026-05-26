---
id: 2026-05-26-1853-hourly-autopilot-sources
source_type: alpaca|mcp|manual
captured_at: 2026-05-26T09:54:00Z
source_url: ""
tool: "Alpaca MCP, SEC EDGAR MCP, Alpha Vantage MCP, FRED MCP, Firecrawl MCP, Yahoo Finance MCP"
tickers: [LLY, LRCX, ASML, AAPL, SMH, SPY, QQQ, AMD, AVGO, ETN, IONQ, NOK, NVDA, RGTI, TSM, UNH]
immutable: true
---

# 2026-05-26 18:53 KST hourly autopilot 원천

## 요약

- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했다. API key 값은 출력하거나 기록하지 않았다.
- shell wrapper가 만든 것으로 보이는 `.locks/hourly-autopilot.lock`이 존재해 wrapper lock이 이미 잡힌 상태로 간주했다.
- Alpaca MCP 성공:
  - `get_all_positions`: 10개 long 포지션 확인. 총 long market value는 57073.20 USD, 총 미실현 손익은 1103.78 USD.
  - `get_market_movers`: 마지막 갱신 `2026-05-22T23:59:00Z`, 저가/투기 mover 다수 확인.
  - `get_stock_bars`: `harness/symbol-metadata.yaml` 62개 심볼 전체에 대해 2026-05-15~2026-05-22 IEX adjusted 1Day bar를 수집. `SPY`, `QQQ` 포함.
  - `get_asset`: `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH` 모두 `status=active`, `tradable=true`, `class=us_equity` 확인.
  - `get_news`: `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH` 관련 Benzinga/Alpaca 뉴스 20건 수집.
- Alpaca MCP 실패 또는 unusable:
  - in-session `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_watchlists`, `get_stock_latest_quote`, `get_stock_snapshot`, `get_stock_latest_bar`는 `user cancelled MCP tool call`.
  - repo-local stdio Alpaca MCP는 동일 도구 호출에서 DNS 오류 `nodename nor servname provided, or not known`을 반환했다.
- Research MCP 실패:
  - SEC EDGAR MCP `get_recent_filings`/`get_company_info`, Alpha Vantage MCP `TOOL_LIST`, Yahoo Finance MCP `get_stock_info`는 in-session tool call이 취소되어 usable data가 없었다.
  - FRED local MCP `get_macro_snapshot`은 `api.stlouisfed.org` DNS resolution failure.
  - Firecrawl local MCP `firecrawl_scrape`은 `api.firecrawl.dev` DNS resolution failure.
- 따라서 MCP strict gate, quote gate, spread gate, account/order reconciliation gate가 실패했다. 주문 후보와 제출 주문은 0건이다.

## 핵심 근거

- Alpaca positions:
  - `AMD` 14주, current price 479.85, market value 6717.90, unrealized P/L 239.68.
  - `AVGO` 15주, current price 416.44, market value 6246.60, unrealized P/L 85.65.
  - `ETN` 15주, current price 397.45, market value 5961.75, unrealized P/L 143.25.
  - `IONQ` 45주, current price 65.13, market value 2930.85, unrealized P/L 74.25.
  - `LRCX` 20주, current price 311.54, market value 6230.80, unrealized P/L 72.60.
  - `NOK` 400주, current price 15.59, market value 6236.00, unrealized P/L 220.00.
  - `NVDA` 35주, current price 217.35, market value 7607.25, unrealized P/L 71.05.
  - `RGTI` 120주, current price 26.33, market value 3159.60, unrealized P/L 91.25004.
  - `TSM` 15주, current price 411.84, market value 6177.60, unrealized P/L 99.60.
  - `UNH` 15주, current price 386.99, market value 5804.85, unrealized P/L 6.45.
- Alpaca broad-universe bars:
  - 62개 metadata universe 심볼 전체가 recent bar 응답에 포함됐다.
  - 2026-05-15~2026-05-22 구간 단순 가격 모멘텀에서 `QBTS`, `RGTI`, `IONQ`, `NOK`, `AMD`, `ASML`, `LRCX`, `LLY`, `AAPL`, `SMH` 등이 강했다.
  - 투기/과열 guard 때문에 `QBTS`, `RGTI`, `IONQ`, `NOK`는 신규 buy 후보에서 제외했다.
  - pre-MCP shortlist: `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH`.
  - final research candidates: `LLY`, `LRCX`, `ASML`.
- Alpaca news highlights:
  - `LLY`: 2026-05-25 VERVE-102 Phase 1b data headline, 2026-05-22 Foundayo Phase 3 ATTAIN-1/ATTAIN-2 headline.
  - `AAPL`: 2026-05-25 Mag-7/market commentary and Apple competitor analysis headlines.
  - `ASML`: 2026-05-22 China semiconductor export/AI demand headline.
  - `SMH`: 2026-05-22 Dow/AI rally and quantum ETF headlines.
  - `LRCX`: direct recent Alpaca news in the 20-row response was sparse; thesis remains price/sector-led and therefore lower confidence without research MCP confirmation.

## 구조화 시그널

| ticker | asof | signal_type | value | confidence | source_ref | notes |
| --- | --- | --- | --- | --- | --- | --- |
| LLY | 2026-05-26T09:54:00Z | news_event | Benzinga/Alpaca recent positive biotech headlines | medium | Alpaca MCP `get_news` | SEC/Alpha/Yahoo/Firecrawl failed, not actionable |
| LRCX | 2026-05-26T09:54:00Z | price_momentum | 2026-05-15 close 284.37 -> 2026-05-22 close 305.43 | medium | Alpaca MCP `get_stock_bars` | Existing semiconductor exposure limits new buy |
| ASML | 2026-05-26T09:54:00Z | price_momentum | 2026-05-15 close 1501.52 -> 2026-05-22 close 1632.98 | medium | Alpaca MCP `get_stock_bars` | ADR/semicap candidate, research MCP gap blocks order |
| AAPL | 2026-05-26T09:54:00Z | price_momentum | 2026-05-15 close 300.19 -> 2026-05-22 close 308.81 | low | Alpaca MCP `get_stock_bars` | News mixed; not final candidate |
| SMH | 2026-05-26T09:54:00Z | price_momentum | 2026-05-15 close 556.85 -> 2026-05-22 close 575.91 | low | Alpaca MCP `get_stock_bars` | ETF candidate, overlaps existing semicap cluster |
| SPY | 2026-05-26T09:54:00Z | benchmark | 2026-05-22 close 745.67 | medium | Alpaca MCP `get_stock_bars` | Universe benchmark included |
| QQQ | 2026-05-26T09:54:00Z | benchmark | 2026-05-22 close 717.49 | medium | Alpaca MCP `get_stock_bars` | Universe benchmark included |

## 언급된 티커

- LLY, LRCX, ASML, AAPL, SMH, SPY, QQQ.
- 보유 포지션: AMD, AVGO, ETN, IONQ, LRCX, NOK, NVDA, RGTI, TSM, UNH.

## 데이터 공백

- Alpaca clock/account/orders/fills/watchlist/quote/snapshot reads were not usable, so submit mode is blocked.
- Latest quote, bid, ask, quote age, and spread are missing for all order candidates.
- SEC EDGAR, Alpha Vantage, Yahoo Finance, FRED, and Firecrawl coverage are not usable in this run.
- Account cash and buying power were not refreshed; any account-level numbers in the order plan use the last confirmed wiki/account snapshot only to satisfy empty-order validation, not as a submit basis.

## 위키 반영 메모

- `wiki/current-runs/daily/2026-05-26-1853-hourly-autopilot.md`에 non-actionable 결과와 gate failures를 기록했다.
- `wiki/trade-ledger/orders/2026-05-26-1853-hourly-autopilot.json`은 empty-order dry-run plan이다.
- `wiki/evidence-store/run-manifests/2026-05-26-1853-hourly-autopilot.json`은 MCP strict gate failure를 기록한다.
