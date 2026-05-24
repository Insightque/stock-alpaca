---
id: 2026-05-24-mcp-comparison-2026-05-08-sources
captured_at: 2026-05-24T11:11:00+09:00
source: alpaca-mcp-sec-edgar-mcp-alpha-vantage-mcp-firecrawl-mcp-yahoo-finance-mcp
paper: true
immutable: true
---

# 2026-05-08 과거 추천 시뮬레이션 MCP 보강 비교 원천

## 목적

- 이전 시뮬레이션 [[2026-04-23-to-2026-05-08-historical-decision-batch-v2]] 중 `2026-05-08` 기준 추천을 표본으로 골라, MCP 보강 수집 전후 판단 차이를 확인했다.
- 원래 추천은 `NVDA, IONQ, UNH`였다.
- 비교 후보로 원래 추천에서 빠진 `AMD, TSLA`를 함께 확인했다.
- 이 문서는 새로 수집한 원천과 데이터 공백만 기록한다. 원래 추천 문서는 수정하지 않는다.

## 사용한 MCP

| MCP | 도구 | 조회 범위 | 결과 |
| --- | --- | --- | --- |
| Alpaca MCP | `get_stock_bars` | NVDA, IONQ, UNH, AMD, TSLA, SPY, QQQ, SMH / 2026-04-24~2026-05-16 / `1Day`, IEX, raw | 기준일 전 모멘텀, 기준일 후 5D 성과, 거래량 배율 계산 가능 |
| Alpaca MCP | `get_news` | NVDA, IONQ, UNH, AMD, TSLA / 2026-05-06~2026-05-09 | NVDA AI 인프라, IONQ 실적/목표가, AMD 실적/애널리스트/차익실현, TSLA 리콜/중국 판매 뉴스 확인 |
| Alpaca MCP | `get_corporate_action_announcements` | NVDA, IONQ, UNH / 2026-05-01~2026-05-09 | 배당, 분할, 합병, spinoff 공시 없음 |
| SEC EDGAR MCP | `get_recent_filings` | NVDA, IONQ, UNH, AMD, TSLA / 최근 60~90일 | NVDA 2026-05-08 8-K, IONQ 2026-05-07 10-Q 및 2026-05-08 Form 4, UNH 2026-05-05 10-Q, TSLA 2026-04-23 10-Q 확인 |
| Alpha Vantage MCP | `EARNINGS` | NVDA, IONQ, UNH, AMD, TSLA | IONQ 2026-05-06 EPS surprise +503.9%, AMD 2026-05-05 EPS surprise +6.2%, UNH 2026-04-21 EPS surprise +9.5%, TSLA 2026-04-22 EPS surprise +17.1% |
| Alpha Vantage MCP | `NEWS_SENTIMENT` | IONQ, AMD 개별 및 5종목 묶음 / 2026-05-06~2026-05-09 | IONQ 개별 조회 6건, AMD 개별 조회 50건. 5종목 묶음 조회는 0건으로 반환되어 broad query 공백 확인 |
| Firecrawl MCP | `firecrawl_search` | 공식 IR/뉴스 사이트 검색 | IONQ Q1 2026 IR, NVIDIA-Corning 공식 뉴스, UNH Q1 2026 결과 페이지/PDF 확인 |
| Yahoo Finance MCP | `get_stock_info`, `get_yahoo_finance_news` | NVDA, IONQ, UNH | 현재 기준 보조 정보만 사용. strict 2026-05-08 판단 근거로는 사용하지 않음 |
| FRED MCP | wrapper JSON-RPC 점검 | `scripts/mcp-fred.sh` | 도구 목록이 반환되지 않아 이번 비교에서는 매크로 MCP 공백으로 기록 |

## 가격 및 거래량 요약

Alpaca MCP `get_stock_bars` 기준이다. 수익률은 2026-05-01 종가 대비 2026-05-08 종가, 그리고 2026-05-08 종가 대비 2026-05-15 종가로 계산했다.

| 티커 | 2026-05-08 종가 | 05-01→05-08 | 05-08→05-15 | SPY 대비 5D 초과 | 05-08 거래량/직전 5일 평균 |
| --- | ---: | ---: | ---: | ---: | ---: |
| NVDA | 215.21 | +8.48% | +4.69% | +4.48%p | 0.95x |
| IONQ | 49.24 | +6.60% | +5.46% | +5.25%p | 0.84x |
| UNH | 379.79 | +2.99% | +3.62% | +3.40%p | 1.41x |
| AMD | 455.07 | +26.22% | -6.83% | -7.05%p | 1.22x |
| TSLA | 428.31 | +9.62% | -1.41% | -1.62%p | 1.55x |
| SPY | 737.54 | +2.37% | +0.21% |  |  |

## 종목별 보강 신호

### NVDA

- Alpaca News:
  - 2026-05-07: Musk가 Nvidia GB300을 "best AI computer"로 언급하고 SpaceX/Anthropic deal 맥락이 보도됨.
  - 2026-05-07: NVIDIA와 IREN의 최대 5GW AI infrastructure partnership 및 NVIDIA의 최대 2.1B USD 투자 옵션 보도.
  - 2026-05-08: NVIDIA-Corning long-term partnership 관련 보도.
- SEC EDGAR MCP:
  - 2026-05-08 `8-K` accession `0001045810-26-000028`.
  - 2026-04-27 `8-K` accession `0001045810-26-000026`.
- Firecrawl MCP:
  - NVIDIA 공식 뉴스 검색 결과: `NVIDIA and Corning Announce Long-Term Partnership to Strengthen US Manufacturing for AI Infrastructure`.
- Alpha Vantage MCP:
  - 다음 실적 발표는 2026-05-20이므로 2026-05-08 결정 시점에서는 아직 미래 정보다.

### IONQ

- Alpaca News:
  - 2026-05-07: Q1 revenue jump와 함께 "one big catch"로 adjusted EBITDA/profitability 리스크가 보도됨.
  - 2026-05-07: Wedbush가 Outperform 유지, price target을 75 USD로 상향.
  - 2026-05-07: JP Morgan은 Neutral 유지, price target 50 USD로 상향.
- SEC EDGAR MCP:
  - 2026-05-07 `10-Q` accession `0001193125-26-211876`, acceptance `2026-05-07T20:06:47Z`.
  - 2026-05-07 `425` accession `0000950142-26-001324`.
  - 2026-05-08 `Form 4` accession `0001193125-26-215307`, acceptance `2026-05-09T01:55:03Z`. 미국 정규장 close 기준으로는 사후 정보에 가깝다.
- Alpha Vantage MCP:
  - 2026-05-06 pre-market Q1 EPS `2.07`, estimate `-0.5125`, surprise `+503.9024%`.
  - `NEWS_SENTIMENT` IONQ 개별 조회: 6건. Stock Titan/Business Wire/TradingView는 bullish, Reuters/Investing.com은 neutral.
- Firecrawl MCP:
  - IonQ IR 검색 결과: `IonQ Announces First Quarter 2026 Financial Results`.
  - 설명: revenue 64.7M USD, guidance midpoint 30% 상회, 전년 대비 755% 성장.

### UNH

- Alpaca News:
  - 2026-05-06: CNBC final trades 맥락에서 UNH 언급.
  - 2026-05-01: healthcare sector breakout 후보 맥락에서 UNH 언급.
- SEC EDGAR MCP:
  - 2026-05-05 `10-Q` accession `0000731766-26-000127`.
  - 2026-04-21 `8-K` accession `0000731766-26-000121`.
- Alpha Vantage MCP:
  - 2026-04-21 pre-market Q1 EPS `7.23`, estimate `6.60`, surprise `+9.5455%`.
- Firecrawl MCP:
  - UnitedHealth Group 공식 Q1 2026 results 검색 결과.
  - 설명: Q1 2026 revenue 111.7B USD, EPS 6.90, adjusted EPS 7.23.

### AMD

- 원래 2026-05-08 추천에서는 제외된 비교 후보다.
- Alpaca News:
  - 2026-05-06~05-08 기간에 AMD 실적, AI server CPU, analyst target 상향, OpenAI/Microsoft/AMD/Intel/Nvidia/Broadcom networking protocol 관련 호재 다수.
  - 동시에 Cathie Wood/ARK가 AMD 강세 구간에서 매도했다는 차익실현성 뉴스가 반복 등장.
- Alpha Vantage MCP:
  - 2026-05-05 post-market Q1 EPS `1.37`, estimate `1.29`, surprise `+6.2016%`.
  - `NEWS_SENTIMENT` AMD 개별 조회는 50건으로 많았고, 주요 기사 다수는 bullish 또는 somewhat bullish였다.
- 가격:
  - 2026-05-01→2026-05-08 +26.22%, 2026-05-08 하루 전 대비 +11.48%.
  - 2026-05-08→2026-05-15 -6.83%.

### TSLA

- 원래 2026-05-08 추천에서는 제외된 비교 후보다.
- Alpaca News:
  - 2026-05-06: rearview camera recall 관련 부정 뉴스.
  - 2026-05-07: China-made vehicle sales 보도.
  - 2026-05-07: 기술적 저항선 테스트 및 robotaxi/self-driving 관련 혼재 뉴스.
- SEC EDGAR MCP:
  - 2026-04-23 `10-Q` accession `0001628280-26-026673`.
  - 2026-04-30 `10-K/A` accession `0001104659-26-053166`.
- Alpha Vantage MCP:
  - 2026-04-22 post-market Q1 EPS `0.41`, estimate `0.35`, surprise `+17.1429%`.
- 가격:
  - 2026-05-01→2026-05-08 +9.62%, 2026-05-08 하루 전 대비 +4.00%.
  - 2026-05-08→2026-05-15 -1.41%.

## 데이터 공백 및 주의

- FRED MCP는 `.env`의 API key와 별개로 현재 JSON-RPC 도구 목록을 반환하지 않아 매크로 regime 보강에 실패했다.
- Yahoo Finance MCP 정보는 조회일 현재 기준 데이터가 섞여 있어 2026-05-08 strict decision에는 직접 사용하지 않았다.
- SEC EDGAR `get_recent_filings`는 현재 기준 최근 filing 목록을 반환하므로, 2026-05-08 decision close 이전에 실제 사용 가능했는지 acceptance time을 별도 필터링해야 한다.
- Alpha Vantage `NEWS_SENTIMENT`는 다중 티커 broad query에서 0건을 반환했지만, 개별 티커 조회에서는 IONQ/AMD 뉴스가 반환됐다. 대량 검증에서는 broad query 실패 시 per-ticker fallback이 필요하다.

## 주문 제출 여부

- 실제 주문, 취소, 포지션 변경은 없었다.
