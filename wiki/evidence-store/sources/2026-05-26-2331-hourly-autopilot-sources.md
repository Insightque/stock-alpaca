---
id: 2026-05-26-2331-hourly-autopilot-sources
source_type: alpaca|mcp|local-wrapper|manual
captured_at: 2026-05-26T14:35:23Z
source_url: ""
tool: "Alpaca MCP, SEC EDGAR MCP, Alpha Vantage MCP, FRED MCP wrapper, Firecrawl MCP wrapper, Yahoo Finance MCP"
tickers: [LLY, LRCX, ASML, SMH, AAPL, SPY, QQQ]
immutable: true
---

# 2026-05-26 23:31 KST hourly autopilot 원천

## 요약

- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했다. Alpaca 및 research provider API key 값은 출력하거나 기록하지 않았다.
- `.locks/hourly-autopilot.lock`은 이미 존재했다. 현재 invocation이 scheduled wrapper prompt와 동일하므로 wrapper가 잡은 lock으로 보고 계속했다.
- Alpaca MCP `get_stock_bars`는 `harness/symbol-metadata.yaml` 62개 universe에 대해 IEX adjusted 1Day bar 응답을 반환했다. 응답은 대용량이라 별도 JSON 원자료로 쓰지 못했고, 이 source note와 manifest에 coverage를 기록했다.
- Alpaca MCP `get_stock_quotes`는 후보 5개에 대해 fresh IEX historical quote를 반환했다.
- Alpaca MCP core 실패:
  - `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, `get_stock_latest_quote`, `get_stock_snapshot`, `get_asset`, `get_news`, `get_market_movers`는 retry 후에도 `user cancelled MCP tool call`.
  - 첫 hard blocking gate는 `alpaca_clock`이다.
- Research MCP 실패:
  - SEC EDGAR: 로컬 `harness/sec-ticker-cik-map.json`으로 `LLY=0000059478`, `LRCX=0000707549`, `ASML=0000937966`, `AAPL=0000320193` 확인. `SMH`는 SEC company ticker cache에 없어 ETF lookup `empty_response`로 분리. 직접 `get_recent_filings` 호출은 retry 후 `cancelled`.
  - Alpha Vantage: `TOOL_LIST`가 retry 후 `cancelled`.
  - Yahoo Finance: `get_stock_info(LLY)`가 retry 후 `cancelled`.
  - FRED wrapper/API endpoint probe: `api.stlouisfed.org` DNS 실패.
  - Firecrawl wrapper/API endpoint probe: `api.firecrawl.dev` DNS 실패.
- 따라서 Alpaca core MCP gate, market-clock gate, account/order reconciliation gate, MCP strict gate가 실패했다. 주문 후보와 제출 주문은 0건이다.

## Universe와 시그널

- Universe source: `harness/symbol-metadata.yaml` 62개 심볼 + 보유 포지션 + `SPY`/`QQQ`.
- Pre-MCP shortlist: `LLY`, `LRCX`, `ASML`, `SMH`, `AAPL`.
- Final research candidates: `LLY`, `LRCX`, `ASML`.
- Broad screen은 23:01 same-day autopilot의 확장 universe 결과를 이어받고, 23:31 run에서 Alpaca MCP broad bars와 candidate quote를 재확인했다.

| ticker | signal | confidence | notes |
| --- | --- | --- | --- |
| LLY | biotech headline/quality healthcare 후보 | medium | 23:31 IEX spread는 0.131%로 개선됐지만 Alpaca clock/account/order 및 research MCP gate 실패 |
| LRCX | semicap momentum, 기존 보유 thesis 유지 | medium | 이미 20주 보유, AI semiconductor cluster 노출 높음, IEX spread 9.16%로 실패 |
| ASML | semicap/ADR momentum | medium | 23:31 IEX spread는 0.356%로 통과했지만 research MCP gap과 core gate 실패 |
| SMH | semiconductor ETF momentum | low | spread는 0.010%로 통과하지만 ETF/cluster 중복이고 final buy 후보 제외 |
| AAPL | mega-cap momentum | low | spread는 0.006%로 통과하지만 catalyst quality가 혼재되어 final 후보 제외 |

## Quote와 spread

Quote age는 `2026-05-26T14:35:23Z` 기준이다. Submit mode 정책상 fresh quote는 20분 이내여야 하고 spread는 0.50% 이하여야 한다.

| ticker | quote_time_utc | bid | ask | spread_pct | quote_gate | spread_gate |
| --- | --- | ---: | ---: | ---: | --- | --- |
| LLY | 2026-05-26T14:32:29Z | 1063.26 | 1064.65 | 0.131 | PASS | PASS |
| LRCX | 2026-05-26T14:32:35Z | 297.44 | 326.00 | 9.16 | PASS | FAIL |
| ASML | 2026-05-26T14:32:39Z | 1635.51 | 1641.34 | 0.356 | PASS | PASS |
| SMH | 2026-05-26T14:32:42Z | 601.68 | 601.74 | 0.010 | PASS | PASS |
| AAPL | 2026-05-26T14:32:48Z | 311.60 | 311.62 | 0.006 | PASS | PASS |

Fresh historical quote rows alone are not enough for submit. `get_clock`, account, open-order, position, and activity reconciliation failed.

## MCP Gap 분류

| MCP | gap_category | retry_count | provider_probe | 메모 |
| --- | --- | ---: | --- | --- |
| Alpaca | cancelled | 2 | not_applicable | broad bars와 historical quotes 일부 usable, core clock/account/orders/positions/activities cancelled |
| SEC EDGAR | cancelled | 2 | not_run | CIK cache 사용 후 direct filing calls cancelled; `SMH` lookup gap은 `empty_response` |
| Alpha Vantage | cancelled | 2 | not_run | `TOOL_LIST` cancelled |
| FRED | dns | 2 | dns_failed | `api.stlouisfed.org` host resolution 실패 |
| Firecrawl | dns | 2 | dns_failed | `api.firecrawl.dev` host resolution 실패 |
| Yahoo Finance | cancelled | 2 | not_run | `get_stock_info(LLY)` cancelled |

## 데이터 공백

- Market clock은 unavailable이다. Order plan의 `market.is_open=false`는 safety default이며 sourced market-clock assertion이 아니다.
- Account cash/buying power/open orders/same-day fills/current positions는 이번 run에서 새로 확인하지 못했다.
- Empty-order risk validation에는 최신 위키/order-plan snapshot의 account와 position 값을 보수적으로 재사용했고, submit 근거로 사용하지 않았다.
- SEC EDGAR, Alpha Vantage, Yahoo Finance, FRED, Firecrawl confirmation이 모두 usable하지 않아 research confirmation count는 0이다.
- `LLY`와 `ASML`은 spread가 통과했지만 Alpaca core와 research MCP gate 실패 때문에 validation buy도 금지된다.

## 위키 반영 메모

- `wiki/current-runs/daily/2026-05-26-2331-hourly-autopilot.md`에 blocked 결과와 gate failures를 기록한다.
- `wiki/trade-ledger/orders/2026-05-26-2331-hourly-autopilot.json`은 empty-order dry-run plan이다.
- `wiki/evidence-store/run-manifests/2026-05-26-2331-hourly-autopilot.json`은 universe strict PASS, MCP strict FAIL을 기록한다.
