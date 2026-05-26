---
id: 2026-05-26-2351-hourly-autopilot-sources
source_type: alpaca|mcp|local-wrapper
captured_at: 2026-05-26T15:00:24Z
source_url: ""
tool: "Alpaca MCP, SEC EDGAR MCP, Alpha Vantage MCP, FRED MCP wrapper, Firecrawl MCP wrapper, Yahoo Finance MCP"
tickers: [LLY, LRCX, ASML, SMH, AAPL, SPY, QQQ]
immutable: true
---

# 2026-05-26 23:51 KST hourly autopilot 원천

## 요약

- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했다. Alpaca 및 research provider API key 값은 출력하거나 기록하지 않았다.
- `.locks/hourly-autopilot.lock`은 이미 존재했다. 현재 invocation이 scheduled wrapper prompt와 동일하므로 wrapper가 잡은 lock으로 보고 계속했다.
- Alpaca MCP core checks는 독립 호출로 수행했다.
  - `get_clock`: PASS. `is_open=true`, timestamp `2026-05-26T10:51:43.945589201-04:00`, next close `2026-05-26T16:00:00-04:00`.
  - `get_account_info`: PASS. account status `ACTIVE`, portfolio value `101521.71`, cash `44030.58`, buying power `139092.57`.
  - `get_orders(status=open, asset_class=us_equity)`: PASS. open orders `0`.
  - `get_all_positions`: PASS. 10개 long equity positions 확인.
  - `get_account_activities(activity_types=FILL, after=2026-05-26)`: PASS. same-day fills `0`.
  - `get_watchlists`: PASS. watchlists `0`.
- Alpaca MCP broad universe `get_stock_bars`는 `harness/symbol-metadata.yaml` 62개 universe에 대해 IEX adjusted 1Day bar 응답을 반환했다. 응답은 대용량이라 별도 JSON 원자료로 쓰지 않고 이 source note와 manifest에 coverage를 기록한다.
- Alpaca MCP `get_stock_latest_quote`, `get_stock_snapshot`, `get_asset`, `get_news`는 후보 5개에 대해 usable했다.
- Alpaca MCP `get_most_active_stocks`는 3회 시도 모두 `cancelled`였다. core gate는 통과했지만 market mover 보강은 점수에 쓰지 않았다.
- Alpaca core first blocking gate: none. Overall first blocking gate: `mcp_research_min_confirmations`.
- Research MCP 결과:
  - SEC EDGAR: 로컬 `harness/sec-ticker-cik-map.json`으로 `LLY=0000059478`, `LRCX=0000707549`, `ASML=0000937966`, `AAPL=0000320193` 확인 후 최근 filings 조회가 usable했다. `SMH`는 SEC company ticker cache에 없어 ETF lookup `empty_response`로 분리했다.
  - Alpha Vantage: `TOOL_LIST`와 `PING`은 응답했지만 `TOOL_GET` schema/data 준비 호출은 3회 cancelled였고, schema 없이 `TOOL_CALL(GLOBAL_QUOTE)`을 직접 호출하려 한 시도는 wrapper safety error로 거부됐다. 점수에 쓸 earnings/fundamental data는 없다.
  - Yahoo Finance: `get_stock_info` for `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH`, `get_recommendations(AAPL)`, `get_yahoo_finance_news(AAPL)` usable.
  - FRED wrapper/API health check: 3회 모두 `api.stlouisfed.org` DNS 실패.
  - Firecrawl wrapper/API health check: 3회 모두 `api.firecrawl.dev` DNS 실패.
- Research MCP usable count는 SEC EDGAR와 Yahoo Finance 2개다. 정책상 buy 후보는 3개 이상 usable/pass research MCP가 필요하므로 자동 주문은 차단된다.

## Universe와 시그널

- Universe source: `harness/symbol-metadata.yaml` 62개 심볼 + 보유 포지션 + `SPY`/`QQQ`.
- Pre-MCP shortlist: `LRCX`, `SMH`, `ASML`, `AAPL`, `LLY`.
- Final research candidates: `AAPL`, `ASML`, `LLY`.
- `LRCX`는 가격 모멘텀은 강하지만 이미 20주 보유 중이고 AI semiconductor cluster 노출과 spread가 부담이다.
- `SMH`는 ETF로 분산 효과는 있지만 기존 반도체 cluster와 중복되고 SEC company ticker lookup은 ETF 특성상 empty response다.

## Quote와 spread

Quote age는 `2026-05-26T15:00:24Z` 기준이다. Submit mode 정책상 fresh quote는 20분 이내여야 하고 spread는 0.50% 이하여야 한다.

| ticker | quote_time_utc | bid | ask | spread_pct | quote_gate | spread_gate |
| --- | --- | ---: | ---: | ---: | --- | --- |
| LLY | 2026-05-26T14:53:52Z | 1072.25 | 1134.00 | 5.598 | PASS | FAIL |
| LRCX | 2026-05-26T14:53:58Z | 303.85 | 320.05 | 5.193 | PASS | FAIL |
| ASML | 2026-05-26T14:53:49Z | 1630.36 | 1639.54 | 0.562 | PASS | FAIL |
| SMH | 2026-05-26T14:53:58Z | 601.77 | 602.13 | 0.060 | PASS | PASS |
| AAPL | 2026-05-26T14:53:58Z | 311.06 | 311.09 | 0.010 | PASS | PASS |

## Alpaca snapshot

| ticker | last_trade | day_close | prev_close | day_change | note |
| --- | ---: | ---: | ---: | ---: | --- |
| LLY | 1073.15 | 1071.59 | 1065.60 | +0.56% | Benzinga reported VERVE-102 LDL reduction commentary; spread failed |
| LRCX | 319.26 | 319.29 | 305.43 | +4.54% | 강한 semicap momentum, 기존 보유, spread failed |
| ASML | 1633.85 | 1634.98 | 1632.98 | +0.12% | Yahoo strong-buy 보강, Alpaca spread 0.562%로 cap 초과 |
| SMH | 602.00 | 602.27 | 575.91 | +4.58% | tight Alpaca spread but semiconductor cluster overlap |
| AAPL | 311.08 | 311.03 | 308.81 | +0.72% | tight Alpaca spread, mixed Apple news |

## SEC EDGAR MCP

- `LLY` recent filings: 2026-05-22 Form 144, 2026-05-20 8-K, 2026-05-19 Form 4 등 5건 확인.
- `LRCX` recent filings: 2026-05-14 Form 144, 2026-05-04 Form 4, 2026-04-30 Schedule 13G 등 5건 확인.
- `ASML` recent filings: 2026-04-23 6-K, 2026-04-15 6-K, 2026-02-25 20-F 등 5건 확인.
- `AAPL` recent filings: 2026-05-12 Form 4, 2026-05-08 Form 4, 2026-05-01 10-Q 등 5건 확인.
- `SMH`: local SEC company ticker cache에 없음. ETF lookup gap은 `empty_response`로 분류하고 provider failure로 처리하지 않는다.

## Alpaca/Yahoo 뉴스와 보강

- Alpaca News 2026-05-26:
  - AAPL/INTC/NVDA/TSM: Intel foundry 관련 Benzinga 기사.
  - AAPL/TSLA/RACE: Ferrari EV와 Jony Ive 관련 Benzinga 기사.
  - AAPL: Japan iPhone 17e sales slowdown 기사.
  - LLY: VERVE-102 LDL cholesterol reduction 관련 Benzinga 기사.
- Yahoo Finance:
  - `LLY`: Healthcare, current price around `1074.21`, target mean `1211.03`, recommendation key `buy`.
  - `LRCX`: Technology/Semiconductor Equipment, current price around `318.43`, target mean `312.13`, recommendation key `buy`; current price가 target mean을 웃돌아 overheat risk를 기록한다.
  - `ASML`: Technology/Semiconductor Equipment, current price around `1631.96`, target mean `1663.18`, recommendation key `strong_buy`.
  - `AAPL`: Technology/Consumer Electronics, current price around `311.24`, target mean `308.65`, recommendation key `buy`; target mean 대비 upside가 제한적이다.
  - `SMH`: Semiconductor ETF, current price around `601.12`, trailing three-month return `25.6554`, non-diversified ETF 설명 확인.

## MCP Gap 분류

| MCP | gap_category | retry_count | provider_probe | 메모 |
| --- | --- | ---: | --- | --- |
| Alpaca | cancelled | 2 | not_run | core gate는 PASS. `get_most_active_stocks`만 3회 cancelled라 mover 보강 미사용 |
| SEC EDGAR | empty_response | 0 | local CIK cache | issuer filings usable. `SMH` ETF lookup만 empty_response |
| Alpha Vantage | wrapper_error | 2 | PING ok | `TOOL_GET` data/schema calls cancelled, schema-less direct data call wrapper safety rejection |
| FRED | dns | 2 | dns_failed | `api.stlouisfed.org` host resolution 실패 |
| Firecrawl | dns | 2 | dns_failed | `api.firecrawl.dev` host resolution 실패 |
| Yahoo Finance | - | 0 | MCP usable | stock info/news/recommendations usable, no gap |

## 데이터 공백

- Buy research MCP confirmation count는 2/5라 정책 최소값 3에 미달한다.
- Alpha Vantage earnings calendar/earnings surprise를 점수에 반영하지 못했다.
- FRED macro regime과 Firecrawl IR/press capture는 DNS 문제로 usable하지 않았다.
- LLY/LRCX/ASML은 fresh quote라도 Alpaca spread cap 0.50%를 넘어서 buy validation order를 제출할 수 없다.
- AAPL/SMH는 spread가 통과했지만 research MCP minimum confirmation과 포트폴리오 우선순위 때문에 주문 후보로 승격하지 않는다.

## 위키 반영 메모

- `wiki/current-runs/daily/2026-05-26-2351-hourly-autopilot.md`에 blocked 결과와 gate failures를 기록한다.
- `wiki/trade-ledger/orders/2026-05-26-2351-hourly-autopilot.json`은 empty-order dry-run plan이다.
- `wiki/evidence-store/run-manifests/2026-05-26-2351-hourly-autopilot.json`은 universe strict PASS, MCP strict FAIL을 기록한다.
