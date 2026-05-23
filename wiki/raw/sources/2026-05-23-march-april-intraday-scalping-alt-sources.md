---
id: 2026-05-23-march-april-intraday-scalping-alt-sources
created_at: 2026-05-23T17:15:00+09:00
source_type: alpaca-market-data-rest
paper: true
---

# 2026년 3월/4월 시간별 단타 재검증 원천

## 목적

앞선 `intraday-rs-breakout-v0` 시간별 단타 시뮬레이션과 다른 일정으로 같은 정책을 다시 검증하기 위한 원천 기록이다.

## 데이터 원천

- 가격: Alpaca Market Data API, IEX feed, `1Day` 및 `1Hour` bars.
- 뉴스: Alpaca News API, Benzinga source.
- 조회 시각: 2026-05-23 KST.
- 후보군: QQQ, SPY, SMH, NVDA, AMD, TSLA, PLTR, AVGO, TSM, LRCX.

주의: 이번 실행에서도 market data만 조회했고, 주문 제출은 하지 않았다. API 키 값은 출력하지 않았다.

## 날짜 선정 기준

앞선 표본에서 사용한 2026-03-09, 2026-03-31, 2026-03-30, 2026-04-02를 제외했다.

3월 학습일은 제외 후 QQQ 3월 정규장 open-to-close 절대수익률 상위 3일로 선정했다.

| 선정 | 날짜 | QQQ open | QQQ close | open-to-close |
| --- | --- | ---: | ---: | ---: |
| 학습 1 | 2026-03-26 | 582.605 | 573.680 | -1.53% |
| 학습 2 | 2026-03-02 | 598.900 | 608.030 | +1.52% |
| 학습 3 | 2026-03-20 | 591.070 | 582.085 | -1.52% |

4월 검증일은 2026-04-02 제외 후 4월 QQQ 정규장 open-to-close 절대수익률 상위일로 선정했다.

| 선정 | 날짜 | QQQ open | QQQ close | open-to-close |
| --- | --- | ---: | ---: | ---: |
| 검증 | 2026-04-14 | 620.360 | 628.580 | +1.33% |

## 해당일 뉴스 요약

### 2026-03-26

- Fed Cook 발언과 불확실성 관련 매크로 뉴스가 확인됐다.
- Microsoft/Nvidia nuclear push 관련 ETF 기사와 TSLA/BYD 경쟁 뉴스가 있었다.
- QQQ 초기 흐름은 neutral이었고 반도체 후보 대부분이 약했다.

참고 URL:

- https://www.benzinga.com/news/26/03/51497707/feds-cook-says-uncertainty-is-elevated-balance-of-risks-are-largely-on-net-in-balance-see-inflation
- https://www.benzinga.com/etfs/sector-etfs/26/03/51497336/microsoft-nvidia-nuclear-push-sparks-etf-opportunity-beyond-semiconductors
- https://www.benzinga.com/trading-ideas/long-ideas/26/03/51498896/tesla-beware-byd-just-played-the-james-bond-card-in-europe

### 2026-03-02

- NVDA H200 중국 고객 판매 제한 검토 관련 Bloomberg 인용 뉴스가 확인됐다.
- PLTR AI scenario 관련 기사, TSLA 유럽 판매 회복과 prediction market 약세 기사가 확인됐다.
- QQQ 초기 흐름은 risk-on이었고 PLTR/NVDA/TSLA가 상대강도 조건을 통과했다.

참고 URL:

- https://www.benzinga.com/news/26/03/50985508/us-mulls-capping-nvidia-h200-sales-at-75-000-per-chinese-customer-bloomberg
- https://www.benzinga.com/markets/prediction-markets/26/03/50984975/why-palantir-is-the-model-if-the-viral-ai-doom-scenario-plays-out
- https://www.benzinga.com/markets/prediction-markets/26/03/50982099/tesla-sales-rebound-in-key-european-markets-but-why-are-prediction-markets-still-bearish

### 2026-03-20

- 중동 군사 노력 종료 가능성 관련 매크로 뉴스, TSLA/Musk 관련 부정적 법률 뉴스가 확인됐다.
- QQQ 초기 흐름은 risk-off였고 long 진입은 없었다.

참고 URL:

- https://www.benzinga.com/news/26/03/51392762/president-trump-says-we-are-getting-very-close-to-meeting-our-objectives-as-we-consider-winding-down
- https://www.benzinga.com/news/26/03/51393136/elon-musk-misled-twitter-investors-before-2022-buyout-jury-says-bloomberg

### 2026-04-14

- AVGO/META 다년 AI chip partnership 뉴스가 확인됐다.
- NVDA 관련 AI/기술주 의견 기사와 원유 재고 매크로 뉴스가 있었다.
- QQQ 초기 흐름은 risk-on이었다. AVGO는 강했지만 정책상 breakout 조건을 통과하지 못해 제외됐다.

참고 URL:

- https://www.benzinga.com/news/26/04/51820348/broadcom-and-meta-announce-a-multi-year-multi-generation-strategic-partnership-to-support-metas-rapi
- https://www.benzinga.com/trading-ideas/movers/26/04/51820856/meta-broadcom-extend-multi-year-ai-chip-partnership-stocks-climb
- https://www.benzinga.com/markets/tech/26/04/51819978/chamath-palihipitiya-says-a-digital-super-god-is-coming-for-tech-stocks-and-could-expose-a-debt-bomb

## 데이터 공백과 한계

- IEX feed 1시간봉 기준이므로 전체 시장 체결량과 다를 수 있다.
- 정책은 동일하게 고정 적용했다. 날짜별 결과에 맞춰 파라미터를 조정하지 않았다.
- 뉴스는 headline/summary 맥락 확인용이며, 직접 진입 조건으로 쓰지 않았다.
