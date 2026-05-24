---
id: 2026-05-24-current-recommendation-sources
source_type: alpaca|sec-edgar|alpha-vantage|yahoo-finance|web
captured_at: 2026-05-24T03:27:34Z
source_url: ""
tool: "Alpaca MCP, SEC EDGAR MCP, Alpha Vantage MCP, Yahoo Finance MCP, web.open"
tickers: [AMD, AVGO, ETN, IONQ, LRCX, NOK, NVDA, RGTI, TSM, UNH, PLTR, TSLA, QBTS, SMH, SPY, QQQ]
immutable: true
---

# 2026-05-24 현재 종목 추천 원천

## 요약

- 사용자 요청 `현재 기준으로 주식 종목 추천해줘`에 대해 no-submit 추천 run을 수행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`만 확인했고, 키 값은 기록하지 않았다.
- Alpaca MCP `get_clock` 기준 미국 주식시장은 닫혀 있었고, 다음 정규장 개장은 `2026-05-26T09:30:00-04:00`, 다음 정규장 마감은 `2026-05-26T16:00:00-04:00`였다.
- Alpaca calendar 기준 `2026-05-22` 다음 정규 거래일은 `2026-05-26`이었다.
- Alpaca watchlist는 비어 있어 현재 paper 포지션 10개와 기존 위키 후보/벤치마크를 후보군으로 사용했다.
- Alpaca account snapshot 기준 portfolio value `100418.67`, cash `44030.58`, buying power `138261.25`, long market value `56388.09`, open orders 없음.
- 보유 종목은 AMD, AVGO, ETN, IONQ, LRCX, NOK, NVDA, RGTI, TSM, UNH이며 모두 long 포지션이다.

## Alpaca 가격/시장 원천

- Alpaca MCP `get_most_active_stocks`: `2026-05-22T23:59:00Z` 기준 RGTI, NVDA, QBTS, NOK 등이 거래량 상위에 포함됐다. 저가/고변동 mover인 QTEX, BIYA, LFS 등은 정책상 신규 핵심 후보에서 제외했다.
- Alpaca MCP `get_market_movers`: `2026-05-22T23:59:00Z` 기준 고변동 저가주와 워런트가 상위 gainers/losers에 다수 포함되어, 이번 추천에서는 유동성/품질 필터를 우선 적용했다.
- Alpaca MCP `get_stock_snapshot` IEX: 2026-05-22 종가/스냅샷 기준 주요 종가:
  - AMD 467.64, LRCX 305.43, SMH 575.91, NOK 15.455, UNH 388.545, NVDA 215.34, TSM 404.33, AVGO 414.01, ETN 391.39.
  - IONQ 63.58, RGTI 26.41, QBTS 29.34는 매우 강했으나 5D/10D 급등과 valuation/short-interest 뉴스 때문에 watch-only로 분류했다.
- Alpaca MCP `get_stock_bars` IEX, adjustment all:
  - 20D 기준일: 2026-04-24 close.
  - 40D 기준일: 2026-03-26 close.
  - 60D 기준일: 2026-02-26 close.
  - 10D 기준일: 2026-05-08 close.
  - 5D 기준일: 2026-05-15 close.

## 계산 메모

벤치마크 20D 수익률:

| 심볼 | 20D 수익률 |
| --- | ---: |
| SPY | 4.44% |
| QQQ | 8.07% |
| SMH | 13.72% |

후보 주요 가격 모멘텀:

| 심볼 | 5D | 10D | 20D | SPY 대비 20D | 40D | 60D |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| AMD | 10.3% | 2.8% | 34.5% | 30.0%p | 129.5% | 129.6% |
| LRCX | 7.4% | 3.9% | 14.2% | 9.7%p | 44.3% | 27.8% |
| SMH | 3.4% | 1.7% | 13.7% | 9.3%p | 51.4% | 39.8% |
| NOK | 10.8% | 20.5% | 48.2% | 43.7%p | 87.0% | 106.8% |
| UNH | -1.3% | 2.3% | 9.5% | 5.0%p | 45.0% | 36.6% |
| IONQ | 22.4% | 29.1% | 49.1% | 44.6%p | 113.0% | 55.9% |
| RGTI | 48.0% | 39.5% | 59.0% | 54.6%p | 83.0% | 41.6% |
| QBTS | 44.2% | 30.1% | 58.8% | 54.3%p | 100.0% | 45.8% |
| NVDA | -4.4% | 0.1% | 3.4% | -1.0%p | 25.8% | 16.5% |
| TSM | 0.0% | -1.7% | 0.5% | -4.0%p | 24.0% | 7.5% |
| AVGO | -2.6% | -3.7% | -2.0% | -6.4%p | 33.7% | 29.0% |
| ETN | -2.1% | -2.5% | -7.5% | -11.9%p | 9.8% | 4.9% |

## 뉴스/리서치 원천

- Alpaca MCP `get_news`, `2026-05-20T00:00:00Z`~`2026-05-24T04:30:00Z`: NVDA/AMD/반도체, 양자컴퓨팅, SPY/QQQ macro 뉴스 다수 확인.
- Benzinga AMD 기사 URL: https://www.benzinga.com/markets/tech/26/05/52741867/what-is-going-on-with-amd-stock-on-friday-3
  - AMD는 2nm Venice CPU 생산 확대, 대만 AI 공급망 $10B+ 투자, CPU 시장 성장 기대가 긍정 촉매로 확인됐다.
  - 동시에 52주 고점 근처 가격이라는 과열 리스크가 확인됐다.
- Benzinga NVDA 기사 URL: https://www.benzinga.com/markets/tech/26/05/52750657/nvidia-crushes-earnings-but-ai-chip-supply-crunch-looms
  - NVDA는 실적/AI 수요/자사주매입이 강하지만, 메모리 공급과 높은 기대치가 단기 부담으로 확인됐다.
- Benzinga quantum 기사 URL: https://www.benzinga.com/markets/equities/26/05/52762946/quantum-computing-stocks-short-interest-jumps-amid-valuation-concerns
  - IONQ/RGTI/QBTS는 정부 quantum funding 기대와 가격 급등이 있지만, short interest와 valuation concern이 높아 신규 추격매수 신뢰도를 낮췄다.
- Benzinga macro 기사 URL: https://www.benzinga.com/markets/equities/26/05/52755165/sp-500-eighth-weekly-gain-hawkish-fed-consumer-sentiment
  - SPY는 8주 연속 상승 흐름이고, AI 제조/설비투자 모멘텀은 강하지만 Fed hawkish risk, 소비심리 악화, 인플레이션 기대 상승이 공존한다.
- Yahoo Finance MCP:
  - UNH: valuation check, AI adoption/turnaround narrative, UBS target increase, Medicare Advantage overpayment policy risk, Berkshire stake exit 관련 뉴스가 확인됐다.
  - LRCX: AI-era tools, capital return, Morgan Stanley upgrade, advanced packaging R&D, AI packaging 수혜 뉴스가 확인됐다.
  - AMD: Taiwan AI infrastructure investment, Venice CPU production, all-time high 근처 가격 뉴스가 확인됐다.
  - NVDA: $80B buyback, sell-the-news reaction, AI capex acceleration, valuation question 뉴스가 확인됐다.
- SEC EDGAR MCP:
  - AMD: 최근 30일 Form 4/144 다수, 2026-05-22 Form 4 acceptance `2026-05-22T21:43:20+00:00`.
  - NVDA: 2026-05-20 10-Q 및 8-K acceptance 확인.
  - UNH: 2026-05-05 10-Q, 2026-05-11 8-K, 2026-05-15 DEFA14A 확인.
  - LRCX: 2026-05-14 Form 144, 2026-05-04 Form 4 등 확인.
- Alpha Vantage MCP `NEWS_SENTIMENT`: `AMD,NVDA,UNH,LRCX,NOK,IONQ,RGTI,QBTS`, `20260520T0000`~`20260524T0430` 조회 결과 `items=0`. 이는 정보 부재가 아니라 provider/query coverage gap으로 기록한다.

## 추천 판단 반영

- 추천 1순위는 `UNH`: 20D가 SPY를 이기면서 5D 과열이 없고, 기술/AI 집중 포트폴리오의 변동성 완화 역할이 있다.
- 추천 2순위는 `LRCX`: 20D/40D 추세가 좋고 AI 반도체 장비/advanced packaging 촉매가 있다.
- 추천 3순위는 `AMD`: 모멘텀과 촉매는 가장 강하지만 20D +34.5%, 60D +129.6%라 staged entry만 적절하다.
- 추천 4순위는 `NVDA`: 실적/AI 수요는 강하지만 post-earnings sell-the-news와 공급/기대치 부담이 있어 소액 추가 또는 눌림 확인이 적절하다.
- 추천 5순위는 `TSM`: 단기 모멘텀은 약하지만 AMD/AI 공급망 촉매의 기반 포지션으로 소액 분산 후보가 된다.
- `NOK`, `IONQ`, `RGTI`, `QBTS`는 가격 모멘텀은 강하지만 5D/10D 급등과 테마 과열 리스크로 신규 추격보다 보유/관찰로 둔다.

## 데이터 공백

- Alpaca quote는 장 마감 후 stale 상태라 submit-mode quote freshness 조건을 만족하지 않는다.
- IEX feed 기준이므로 SIP 전체 시장 데이터와 일부 가격/거래량/호가가 다를 수 있다.
- Alpha Vantage news sentiment는 0건이었다. 개별 뉴스와 SEC/Alpaca/Yahoo 원천으로 보강했다.
- FRED MCP는 이번 run에서 callable tool이 노출되지 않아 별도 macro series 조회는 수행하지 않았다.

## 위키 반영 메모

- `wiki/reports/daily/2026-05-24.md`에 현재 추천과 risk-check 결과를 기록한다.
- `wiki/portfolio/order-plans/2026-05-24-current-recommendations.json`은 dry-run 후보이며 실제 주문은 없다.
- `wiki/portfolio/current.md`는 Alpaca account/positions 재조회 값으로 갱신한다.
