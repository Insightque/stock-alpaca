---
id: 2026-05-23-march-april-intraday-scalping-sources
created_at: 2026-05-23T16:10:00+09:00
source_type: alpaca-market-data-rest
paper: true
---

# 2026년 3월/4월 시간별 단타 시뮬레이션 원천

## 목적

사용자 요청에 따라 2026년 3월 특정일 3개를 선정해 시간별 단타 정책을 만들고, 2026년 4월 특정일에 대해 같은 정책이 작동하는지 검증하기 위한 원천 기록이다.

## 데이터 원천

- 가격: Alpaca Market Data API, IEX feed, `1Day` 및 `1Hour` bars.
- 뉴스: Alpaca News API, Benzinga source.
- 조회 시각: 2026-05-23 KST.
- 조회 기간:
  - 일봉: 2026-03-01~2026-05-01.
  - 1시간봉: 2026-03-01~2026-04-04.
  - 뉴스: 2026-03-09, 2026-03-30, 2026-03-31, 2026-04-02.
- 후보군: QQQ, SPY, SMH, NVDA, AMD, TSLA, PLTR, AVGO, TSM, LRCX.

주의: 이번 실행에서는 OpenClaw에 Alpaca MCP 도구가 직접 노출되지 않아 주문/계좌 endpoint가 아닌 Alpaca market data REST만 사용했다. API 키 값은 출력하지 않았다. 실제 주문 제출은 없었다.

## 날짜 선정 기준

3월 학습일은 QQQ의 2026년 3월 정규장 open-to-close 절대수익률 상위 3일로 선정했다.

| 선정 | 날짜 | QQQ open | QQQ close | open-to-close |
| --- | --- | ---: | ---: | ---: |
| 학습 1 | 2026-03-09 | 594.155 | 607.760 | +2.29% |
| 학습 2 | 2026-03-31 | 564.280 | 577.110 | +2.27% |
| 학습 3 | 2026-03-30 | 567.345 | 558.280 | -1.60% |

4월 검증일은 2026년 4월 QQQ 정규장 open-to-close 절대수익률 상위일로 선정했다.

| 선정 | 날짜 | QQQ open | QQQ close | open-to-close |
| --- | --- | ---: | ---: | ---: |
| 검증 | 2026-04-02 | 574.010 | 584.950 | +1.91% |

## 해당일 뉴스 요약

뉴스는 단타 정책의 직접 진입 조건에는 넣지 않고, 당일 가격 움직임의 배경을 이해하는 보조 정보로만 사용했다.

### 2026-03-09

- TSLA 관련 임원 이탈, robotaxi 신뢰도, valuation 우려 기사들이 다수 확인됐다.
- NVDA/TSM 관련 공급망과 지정학 리스크성 기사가 확인됐다.
- PLTR/TSM 관련 장기 투자 성과형 기사도 있었지만 장중 직접 촉매로 보기는 어렵다.
- 참고 URL:
  - https://www.benzinga.com/markets/prediction-markets/26/03/51146821/tesla-loses-director-behind-robotaxi-backend-what-do-prediction-markets-say
  - https://www.benzinga.com/markets/large-cap/26/03/51139696/tesla-20-crash-may-be-just-the-beginning-as-expert-slams-absurd-bull-valuations-bulls-believe-everything-elon-says
  - https://www.benzinga.com/trading-ideas/long-ideas/26/03/51138854/nvidias-4-trillion-empire-rests-on-a-country-98-dependent-on-the-strait-of-hormuz-see-the-problem

### 2026-03-30

- QQQ/SPY 관련 장중 반등 내러티브 기사가 있었지만, 1시간봉 기준 초기 시장 흐름은 약했다.
- TSLA는 SpaceX IPO 기대와 자율주행 경쟁 관련 뉴스가 혼재했다.
- NVDA와 기술주 옵션/정치 관련 보조 뉴스가 확인됐다.
- 참고 URL:
  - https://www.benzinga.com/Opinion/26/03/51549679/market-bounces-from-low-band-of-support-zone-deal-narrative-takes-hold-risk-mispriced
  - https://www.benzinga.com/trading-ideas/movers/26/03/51550224/spacex-ipo-etrade-reportedly-leads-retail-push-as-robinhood-sofi-compete-for-role
  - https://www.benzinga.com/markets/tech/26/03/51551675/nvidia-uber-waymo-av-stack-rebuilt-without-tesla

### 2026-03-31

- Iran 관련 긴장 완화 기대와 Nasdaq 100 반등 뉴스가 확인됐다.
- AMD, AVGO, NVDA, TSM 등 반도체/기술주 상승 맥락이 확인됐다.
- PLTR, TSLA, Apple 등이 지정학 리스크 기사에 같이 등장했다.
- 참고 URL:
  - https://www.benzinga.com/markets/equities/26/03/51579159/oil-tumbles-100-stocks-surge-iran-ready-end-war-markets-update-tuesday
  - https://www.benzinga.com/markets/tech/26/03/51580500/tech-stocks-rise-on-iran-de-escalation-hopes
  - https://www.benzinga.com/markets/equities/26/03/51577677/stocks-rebound-7-month-lows-yields-fall-trump-iran-exit-markets-tuesday

### 2026-04-02

- NVDA 상승 배경 기사와 Apple/NVDA가 방산주보다 강하다는 ETF/섹터형 기사가 확인됐다.
- TSLA는 Q1 판매, Ford 경쟁, SpaceX IPO 기대 뉴스가 혼재했다.
- AVGO CFO 교체 뉴스가 확인됐다.
- QQQ/SPY에 대해서는 시장 하락 가능성을 경고하는 의견 기사도 있었다.
- 참고 URL:
  - https://www.benzinga.com/trading-ideas/movers/26/04/51634868/nvidia-stock-is-climbing-today-whats-going-on
  - https://www.benzinga.com/etfs/sector-etfs/26/04/51637298/nvidia-apple-are-outgunning-defense-stocks-during-a-war-thats-weird
  - https://www.benzinga.com/news/26/04/51638642/broadcom-appoints-amie-thuener-as-cfo-effective-june-12-succeeding-kirsten-m-spears

## 데이터 공백과 한계

- 1시간봉은 IEX feed 기준이라 전체 SIP 거래량과 다를 수 있다.
- Alpaca `1Hour` bar timestamp는 정규장 초반 일부 구간을 시간 단위로 묶어 제공한다. 이번 분석에서는 09:00~10:00 ET 두 개 bar를 개장 후 초기 확인 구간으로 사용했다.
- 뉴스는 headline/summary 기준으로만 보조 분류했다. 유료 기사 전문은 사용하지 않았다.
- 이번 검증은 long-only 단타 정책이다. 하락장 short, inverse ETF, options, fractional 주문은 검토하지 않았다.
