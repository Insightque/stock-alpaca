---
id: 2026-05-24-mcp-policy-history-reaudit-sources
created_at: 2026-05-24T11:25:00+09:00
source_type: mcp-reaudit
paper: true
immutable: true
---

# 남은 정책 시뮬레이션 이력 MCP 재감사 원천

## 목적

이 원천 노트는 2026-05-08 표본 MCP 비교 이후, 나머지 과거 추천/정책 시뮬레이션 이력의 정책 결론이 추가 MCP 정보로 달라지는지 확인하기 위해 캡처한 자료를 요약한다.

실제 주문, 취소, 포지션 변경은 없었다.

## 재감사 대상

- [[2026-04-23-to-2026-05-08-historical-decision-batch]]
- [[2026-04-23-to-2026-05-08-historical-decision-batch-v2]]
- [[2026-05-11-to-2026-05-15-historical-validation-decision]]
- [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-decision]]
- [[2026-05-18-to-2026-05-22-recent-7d-historical-decision]]
- [[2026-05-23-news-price-lead-lag-simulation]]
- [[2026-05-23-intraday-scalping-feature-filter-simulation]]
- [[2026-05-23-long-term-feb-mar-apr-may-simulation]]
- [[2026-05-24-short-long-policy-feb-mar-apr-may-review]]
- 선행 비교: [[2026-05-24-mcp-comparison-2026-05-08-historical-simulation]]

## 사용 MCP와 호출 요약

| MCP | 호출/확인 | 결과 |
| --- | --- | --- |
| Alpaca MCP | `get_stock_bars` 2026-04-20~2026-05-23, `NVDA, AMD, AVGO, LRCX, TSM, NOK, UNH, ETN, IONQ, QBTS, RGTI, PLTR, TSLA, SPY, QQQ, SMH`, `1Day`, IEX | 5월 중순/말 가격 반응과 벤치마크 동행 확인 |
| Alpaca MCP | `get_news` 2026-05-11~05-16, 2026-05-18~05-23 | AMD, NVDA, IONQ, RGTI, NOK, LRCX, UNH 등 이벤트 뉴스 확인 |
| Alpha Vantage MCP | `EARNINGS` for `AMD`, `NOK`, `RGTI`, `QBTS` | 실적 surprise와 report time 확인 |
| Alpha Vantage MCP | `NEWS_SENTIMENT` for `IONQ`, `RGTI`, `QBTS`; broad `IONQ,RGTI,QBTS,NOK` | 개별 ticker 조회는 결과가 있었지만 broad 묶음 조회는 0건 |
| SEC EDGAR MCP | `get_recent_filings` with `identifier` for `IONQ`, `AMD`, `RGTI`, `QBTS`, `NOK` | 핵심 filing과 acceptance time 확인. `symbol` 인자는 필터링되지 않아 `identifier`로 재조회 |
| Firecrawl MCP | 공식 IR/뉴스룸 검색 for AMD, Rigetti, D-Wave, Nokia | 공식 출처 URL과 요약 확인 |
| FRED MCP | `scripts/mcp-fred.sh` tools/list | 응답 지연으로 중단. macro MCP operational gap으로 기록 |

## Alpaca 가격/뉴스 확인

Alpaca `1Day` IEX bars는 최근 이벤트 구간의 가격 반응을 기존 회고와 일치하게 재확인했다.

| 이벤트 구간 | 가격 반응 |
| --- | --- |
| RGTI 2026-05-20→05-21→05-22 | 16.87 → 22.04 → 26.41, 1D +30.65%, 다음 1D +19.83% |
| QBTS 2026-05-20→05-21→05-22 | 19.285 → 25.72 → 29.34, 1D +33.36%, 다음 1D +14.07% |
| IONQ 2026-05-20→05-21→05-22 | 52.49 → 58.87 → 63.58, 1D +12.15%, 다음 1D +8.00% |
| NOK 2026-05-20→05-21→05-22 | 13.63 → 14.18 → 15.455, 1D +4.03%, 다음 1D +8.99% |
| AMD 2026-05-15→05-22 | 423.97 → 467.64, +10.30% |
| NVDA 2026-05-18→05-22 | 222.35 → 215.34, -3.15% |

Alpaca news에서 확인된 대표 항목:

- 2026-05-11: AMD 52-week high, AI infrastructure rally 관련 기사.
- 2026-05-11: IONQ Q1 revenue/guidance 관련 기사.
- 2026-05-11: RGTI Q1 earnings 대기 및 이후 Q1 결과 기사.
- 2026-05-11: NOK Lockheed Martin deal/Q4 outlook 기사.
- 2026-05-18: NVDA earnings preview, AI capex 부담, hedge fund trimming, sell-the-news risk 관련 기사.
- 2026-05-18: LRCX analyst upgrade.
- 2026-05-18: UNH pre-market weakness 및 Berkshire 관련 기사.

## Alpha Vantage 실적/뉴스 확인

| 티커 | Alpha Vantage 확인 |
| --- | --- |
| AMD | 2026-05-05 post-market Q1 EPS 1.37, estimated 1.29, surprise +0.08, +6.2016% |
| NOK | 2026-04-23 pre-market Q1 EPS 0.0586, estimated 0.0532, surprise +10.1504% |
| RGTI | 2026-05-11 pre-market Q1 EPS -0.0614, estimated -0.0356, surprise -72.4719% |
| QBTS | 2026-05-12 pre-market Q1 EPS -0.05, estimated -0.0631, surprise +20.7607% |
| IONQ news sentiment | 2026-05-11 IonQ 공식 기사: Q1 revenue $64.7M, +755% YoY, FY guidance $260M~$270M, ticker sentiment bullish |
| RGTI news sentiment | 2026-05-11~05-12: revenue $4.4M, operating loss $26.0M, cash $569M, mixed-to-bullish news; EPS surprise 자체는 부정적 |
| QBTS news sentiment | 2026-05-12~05-13: EPS beat, revenue -81% YoY, bookings +1,994%, analyst forecast cuts 포함, sentiment mixed/bearish |
| broad query | `IONQ,RGTI,QBTS,NOK` 2026-05-18~05-23 broad `NEWS_SENTIMENT`는 0건. 개별 조회 fallback 필요 |

## SEC EDGAR 확인

처음 `get_recent_filings`에 `symbol` 인자를 넣었을 때 필터링되지 않아 전체 최근 filing이 반환됐다. 도구 schema 확인 후 `identifier` 인자로 재조회했다.

| 티커 | SEC EDGAR 확인 |
| --- | --- |
| IONQ | 2026-05-06 8-K accepted 2026-05-06T20:05:20Z, 2026-05-07 10-Q accepted 2026-05-07T20:06:47Z, 2026-05-07 425, 2026-05-08 Form 4 accepted 2026-05-09T01:55:03Z |
| AMD | 2026-05-05 8-K accepted 2026-05-05T20:16:06Z, 2026-05-06 10-Q accepted 2026-05-05T22:06:27Z, 2026-05-15 8-K, 2026-05-15/19/22 Form 4 |
| RGTI | 2026-05-21 8-K accepted 2026-05-21T11:30:49Z, 2026-05-21/22 Form 144/Form 4 |
| QBTS | 2026-05-21 8-K accepted 2026-05-21T10:52:43Z, 2026-05-21/22 Form 144/Form 4 |
| NOK | 2026-05-13/18/20 Form 6-K, 2026-05-21 Form SD |

시간 누출 주의:

- IONQ 2026-05-08 Form 4는 filing date가 2026-05-08이지만 acceptance time이 2026-05-09T01:55:03Z라서 2026-05-08 정규장 종가 기준 추천에는 사용할 수 없다.
- RGTI/QBTS 2026-05-21 8-K는 미국 정규장 시작 전 acceptance라 2026-05-21 종가 기준 추천에는 사용할 수 있다.

## Firecrawl 공식 출처 확인

| 티커/주제 | Firecrawl 검색 결과 |
| --- | --- |
| AMD Q1 2026 | `https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results`; 설명: first quarter revenue $10.3B, gross margin 53%, operating income $1.5B, net income $1.4B |
| Rigetti Q1 2026 | `https://investors.rigetti.com/news-releases/news-release-details/rigetti-computing-reports-first-quarter-2026-financial-results`; 2026-05-11 5:00 PM ET conference call |
| D-Wave Q1 2026 | `https://ir.dwavesys.com/`; 설명에 2026-05-12 D-Wave Reports First Quarter 2026 Results |
| Nokia Q1 2026 | `https://www.nokia.com/newsroom/nokia-corporation-interim-report-for-q1-2026/`; Q1 comparable net sales grew 4% y-o-y constant currency/portfolio basis |
| Nokia AI networking lab | `https://www.nokia.com/newsroom/nokia-launches-ai-networking-lab-to-drive-co-innovation-with-partners-and-accelerate-next-era-of-ai-native-data-center-networking/`; 2026-05-21 AI-native data center networking lab |

검색 한계:

- `site:investor.rigetti.com` 제한 검색은 0건이었지만, broader query에서는 공식 `investors.rigetti.com` 결과가 반환됐다.
- 따라서 Firecrawl도 domain-restricted query가 0건이면 broader official-name query fallback을 사용한다.

## 데이터 공백

- FRED MCP는 tools/list 응답이 없어 프로세스를 중단했다. 금리, CPI, 유가, yield curve 등 macro regime은 이번 재감사에 반영하지 못했다.
- Alpha Vantage broad `NEWS_SENTIMENT`가 0건인 경우 실제 뉴스 부재로 해석하지 않는다. 개별 ticker 조회, Alpaca news, 공식 IR/SEC fallback이 필요하다.
- IEX 일봉/뉴스 기반이라 장중 뉴스 timestamp와 실제 bid/ask spread, limit fill 가능성은 확인하지 못했다.
