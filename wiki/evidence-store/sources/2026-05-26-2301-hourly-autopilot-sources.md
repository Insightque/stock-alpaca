---
id: 2026-05-26-2301-hourly-autopilot-sources
source_type: alpaca|mcp|local-wrapper|manual
captured_at: 2026-05-26T14:01:10Z
source_url: ""
tool: "Alpaca MCP, SEC EDGAR MCP, Alpha Vantage MCP, FRED MCP wrapper, Firecrawl MCP wrapper, Yahoo Finance MCP"
tickers: [LLY, LRCX, ASML, SMH, AAPL, SPY, QQQ, AMD, AVGO, ETN, IONQ, NOK, NVDA, RGTI, TSM, UNH]
immutable: true
---

# 2026-05-26 23:01 KST hourly autopilot 원천

## 요약

- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했다. Alpaca 및 research provider API key 값은 출력하거나 기록하지 않았다.
- `.locks/hourly-autopilot.lock`은 이미 존재했다. 현재 invocation이 shell wrapper prompt와 동일하므로 wrapper가 잡은 lock으로 보고 계속했다.
- Alpaca MCP 성공:
  - `get_all_positions`: 10개 long 포지션 확인. 최신 응답 기준 long market value 합계 57,089.424 USD.
  - `get_stock_bars`: `harness/symbol-metadata.yaml` 62개 전체 universe에 IEX adjusted 1Day bar를 요청했고 응답을 받았다. `SPY`, `QQQ` 포함.
  - `get_asset`: `LLY`, `LRCX`, `ASML`, `SMH`, `AAPL` 모두 `status=active`, `tradable=true`, `class=us_equity`.
  - `get_stock_quotes`: 후보 5개에 대해 IEX historical quote를 개별 조회했다.
  - `get_news`: `LLY`, `LRCX`, `ASML`, `SMH`, `AAPL` 관련 Alpaca/Benzinga 뉴스 20건 응답.
  - `get_market_movers`: 마지막 갱신 `2026-05-26T13:58:00Z`, 초저가/투기 mover 다수 확인.
- Alpaca MCP 실패 또는 unusable:
  - `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_watchlists`, `get_stock_latest_quote`, `get_stock_snapshot`은 retry 후에도 `user cancelled MCP tool call`.
  - 첫 hard blocking gate는 `alpaca_clock`이다.
- Research MCP 실패:
  - SEC EDGAR: 로컬 `harness/sec-ticker-cik-map.json`으로 `LLY=0000059478`, `LRCX=0000707549`, `ASML=0000937966`, `AAPL=0000320193` 확인. `SMH`는 SEC company ticker cache에 없어 ETF lookup `empty_response`로 분리. 직접 `get_recent_filings` 호출은 retry 후 `cancelled`.
  - Alpha Vantage: `TOOL_LIST`가 retry 후 `cancelled`.
  - Yahoo Finance: `get_stock_info`, `get_yahoo_finance_news`, `get_recommendations`가 retry 후 `cancelled`.
  - FRED wrapper: `scripts/mcp-fred.sh --health-check`와 read-only probe 모두 `api.stlouisfed.org` DNS 실패.
  - Firecrawl wrapper: `scripts/mcp-firecrawl.sh --health-check`와 read-only probe 모두 `api.firecrawl.dev` DNS 실패.
- 따라서 Alpaca core MCP gate, MCP strict gate, market-clock gate, account/order reconciliation gate가 실패했다. 주문 후보와 제출 주문은 0건이다.

## Alpaca 포지션

| ticker | qty | current_price | market_value | unrealized_pl |
| --- | ---: | ---: | ---: | ---: |
| AMD | 14 | 490.64 | 6868.96 | 390.74 |
| AVGO | 15 | 427.37 | 6410.55 | 249.60 |
| ETN | 15 | 403.29 | 6049.35 | 230.85 |
| IONQ | 45 | 61.235 | 2755.575 | -101.025 |
| LRCX | 20 | 315.72 | 6314.40 | 156.20 |
| NOK | 400 | 15.8398 | 6335.92 | 319.92 |
| NVDA | 35 | 215.6534 | 7547.869 | 11.669 |
| RGTI | 120 | 24.37 | 2924.40 | -143.94996 |
| TSM | 15 | 414.10 | 6211.50 | 133.50 |
| UNH | 15 | 378.06 | 5670.90 | -127.50 |

Account cash와 buying power는 이번 run에서 Alpaca account MCP가 실패해 새로 확인하지 못했다. Empty-order risk validation에는 최근 wiki/account snapshot의 cash 44,030.58 USD와 buying power 138,261.25 USD를 보수적으로 재사용했고, submit 근거로 사용하지 않았다.

## Universe와 시그널

- Universe source: `harness/symbol-metadata.yaml` 62개 심볼 + 보유 포지션 + `SPY`/`QQQ`.
- Pre-MCP shortlist: `LLY`, `LRCX`, `ASML`, `SMH`, `AAPL`.
- Final research candidates: `LLY`, `LRCX`, `ASML`.
- `RGTI`, `QBTS`, `IONQ`, `NOK` 등 고모멘텀/투기 후보는 overheat/speculative guard로 신규 buy 후보에서 제외했다.

| ticker | signal | confidence | notes |
| --- | --- | --- | --- |
| LLY | biotech headline + 방어적 헬스케어 growth 후보 | medium | Alpaca news는 긍정적이나 SEC/Alpha/Yahoo/FRED/Firecrawl confirmation 실패, IEX spread 10.46% |
| LRCX | semicap momentum, 기존 보유 thesis 유지 | medium | 이미 20주 보유, AI semiconductor cluster 노출 높음, IEX spread 9.16% |
| ASML | semicap/ADR momentum | medium | 가격 흐름은 강하나 research MCP gap, latest IEX spread 0.66%로 정책 한도 초과 |
| SMH | semiconductor ETF momentum | low | IEX spread 0.077%는 통과지만 기존 반도체 cluster와 중복되고 ETF라 SEC company lookup은 empty_response |
| AAPL | mega-cap momentum | low | IEX spread 0.016%는 통과지만 뉴스 catalyst 혼재, 최종 후보 제외 |

## Quote와 spread

Quote age는 `2026-05-26T14:01:10Z` 기준이다. Submit mode 정책상 fresh quote는 20분 이내여야 하고 spread는 0.50% 이하여야 한다.

| ticker | quote_time_utc | bid | ask | spread_pct | quote_gate | spread_gate |
| --- | --- | ---: | ---: | ---: | --- | --- |
| LLY | 2026-05-26T13:58:13Z | 1021.25 | 1134.00 | 10.46 | PASS | FAIL |
| LRCX | 2026-05-26T13:58:24Z | 297.44 | 326.00 | 9.16 | PASS | FAIL |
| ASML | 2026-05-26T13:58:29Z | 1620.32 | 1631.01 | 0.66 | PASS | FAIL |
| SMH | 2026-05-26T13:58:40Z | 596.91 | 597.37 | 0.077 | PASS | PASS |
| AAPL | 2026-05-26T13:58:45Z | 310.49 | 310.54 | 0.016 | PASS | PASS |

Fresh historical quote rows alone are not enough for submit. `get_clock`, account, open-order, and full core reconciliation failed.

## Alpaca News Highlights

- `LLY`: VERVE-102 Phase 1b LDL cholesterol headline and healthcare/options activity headlines.
- `AAPL`: iPhone 17e Japan sales, peer comparison, Ferrari/Jony Ive EV, and market breadth headlines.
- `LRCX`, `ASML`, `SMH`: 직접 headline은 제한적이어서 가격/섹터 momentum 중심 시그널로만 사용한다.

## MCP Gap 분류

| MCP | gap_category | retry_count | provider_probe | 메모 |
| --- | --- | ---: | --- | --- |
| Alpaca | cancelled | 2 | not_applicable | positions/bars/assets/news/quotes 일부 usable, core clock/account/orders cancelled |
| SEC EDGAR | cancelled | 2 | not_run | CIK cache 사용 후 direct filing calls cancelled; `SMH` lookup gap은 `empty_response` |
| Alpha Vantage | cancelled | 2 | not_run | `TOOL_LIST` cancelled |
| FRED | dns | 2 | dns_failed | `api.stlouisfed.org` host resolution 실패 |
| Firecrawl | dns | 2 | dns_failed | `api.firecrawl.dev` host resolution 실패 |
| Yahoo Finance | cancelled | 2 | not_run | stock info/news/recommendations cancelled |

## 데이터 공백

- Market clock은 unavailable이다. Order plan의 `market.is_open=false`는 safety default이며 sourced market-clock assertion이 아니다.
- Account cash/buying power/open orders/same-day fills는 이번 run에서 새로 확인하지 못했다.
- SEC EDGAR, Alpha Vantage, Yahoo Finance, FRED, Firecrawl confirmation이 모두 usable하지 않아 research confirmation count는 0이다.
- `LLY`, `LRCX`, `ASML`은 fresh quote가 있어도 spread gate를 통과하지 못했다.

## 위키 반영 메모

- `wiki/current-runs/daily/2026-05-26-2301-hourly-autopilot.md`에 blocked 결과와 gate failures를 기록한다.
- `wiki/trade-ledger/orders/2026-05-26-2301-hourly-autopilot.json`은 empty-order dry-run plan이다.
- `wiki/evidence-store/run-manifests/2026-05-26-2301-hourly-autopilot.json`은 universe strict PASS, MCP strict FAIL을 기록한다.
