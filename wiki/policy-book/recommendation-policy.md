---
id: recommendation-policy
updated_at: 2026-05-25T02:06:00+09:00
---

# 추천 정책

이 문서는 거래 회고와 과거 시점 추천 시뮬레이션 회고에서 반복적으로 확인된 교훈을 모아 향후 종목 추천과 리밸런싱 판단에 반영하기 위한 living policy다. 아직 누적 회고가 적으므로, 현재는 하네스의 기본 리스크 정책과 초기 분석에서 나온 원칙을 담는다.

## 현재 원칙

- 출처가 부족한 급등주는 자동 매수 후보에서 제외한다.
- 1달러 미만 또는 비정상적으로 스프레드가 넓은 종목은 기본적으로 회피한다.
- 레버리지/인버스 ETF는 핵심 롱 포트폴리오 후보가 아니라 단기 전술 후보로만 다룬다.
- 점수가 높아도 신뢰도가 낮으면 비중을 낮추거나 watchlist로만 둔다.
- 수익률 결과와 판단 품질을 분리해서 회고한다.
- 과거 thesis를 사후에 덮어쓰지 않고, 별도 회고 문서나 날짜가 있는 회고 섹션으로 남긴다.
- 뉴스가 긍정적이어도 뉴스 전 3D/5D 가격이 이미 크게 올랐으면 선반영 가능성으로 감점한다.
- 테마/정책 뉴스는 당일 급등 추격보다 다음 거래일 유지 여부를 더 중요하게 본다.
- 장타 신규 매수 후보는 기본적으로 theme cap을 적용하고, 20D +45% 초과 또는 5D +25% 초과 구간은 과열 후보로 감점한다.
- 장타 우선순위는 20D 수익률이 SPY와 QQQ를 모두 초과하는지 확인하고, 초과하지 못하면 보조 후보나 관찰 후보로 낮춘다.
- 과열 가능성이 있는 장타 후보는 한 번에 목표 비중을 채우지 않고 `5D -7%~+12%`, `20D +2%~+35%` 범위에서 staged entry 후보로만 둔다.
- 확장 universe를 쓸 때는 단순 후보 수 확대를 개선으로 보지 않는다. theme cap, overheat guard, SPY/QQQ 상대강도 확인을 같이 적용한다.
- 백테스트는 종목별 row index가 아니라 `asof_date` key로 정렬해야 한다. 기준일, forward horizon, benchmark는 모두 날짜 기준으로 매칭하고, 특정 종목의 해당 날짜가 없으면 표본에서 제외한다.
- 주문 계획은 종목별 한도뿐 아니라 `theme`, `factor`, `volatility_bucket`, `speculative_flag`를 포함한 포트폴리오 노출 한도를 통과해야 한다.
- 추천 리포트에는 가능하면 `Expected excess return`, `Expected max adverse move`, `Confidence`, `Position size rationale`을 분리해 기록한다. 단일 점수는 설명용이고 주문 크기의 직접 근거가 아니다.
- 뉴스, SEC filing, valuation, macro, liquidity 정보는 narrative만 남기지 말고 raw source의 `구조화 시그널` 표에도 저장해 이후 정책학습에 재사용한다.
- MCP provider에서 뉴스/filing/매크로가 0건이어도 정보 부재로 단정하지 않고, 개별 ticker 조회와 SEC/공식 IR fallback으로 재확인한다.
- SEC filing은 filing date보다 acceptance time 기준으로 as-of 사용 가능 여부를 판단한다.
- 단타는 11:00 ET 신호만으로 자동 주문하지 않고, 11:05~11:15 후속 유지와 실제 bid/ask/fill 가능성을 확인하기 전까지 관찰 전용으로 둔다.
- 분석 결과 문서에 계산 지표나 정책학습 지표가 포함되면, 문서 하단에 `지표 설명` 섹션을 추가해 각 지표의 의미와 해석 방법을 쉬운 한국어로 설명한다.
- 운영 정책의 machine-readable source는 `harness/recommendation-policy.yaml`로 둔다. 이 Markdown 문서는 사람이 읽는 설명과 회고 로그이며, 전략 상태와 승격 기준은 YAML과 schema로 검증한다.
- 장기 `long-term-quality-momentum-v1`은 `active_dry_run_candidate`로 승격하되 자동 주문은 아직 금지한다. 핵심 필터는 SPY/QQQ dual benchmark, drawdown/volatility guard, theme/factor cap, overheat guard, source confidence, liquidity check다.
- 단타 `intraday-afternoon-followthrough-v1`과 기존 intraday variants는 모두 `observation_only`다. 결과는 수익률 후보가 아니라 `signal_log`, `skip_reason`, `spread_fill_observation`을 쌓는 체결 품질 학습 자료로만 사용한다.
- 알파 점수와 주문 결정을 분리한다. 가격/상대강도/이벤트 품질은 후보 점수이고, 실제 주문 크기는 보유 비중, cash reserve, theme/factor/speculative/cluster cap, spread/liquidity, expected adverse move, open orders, staged entry를 통과한 뒤 별도로 결정한다.
- `confidence_score < 0.50`, `source_confidence=low`, provider gap, stale quote, missing spread, missing metadata가 있으면 신규 order plan entry를 만들지 않는다.
- 확장 universe는 theme cap, factor cap, active/tradable 확인, 최소 가격, 유동성, spread, source confidence, SPY/QQQ 상대강도를 모두 통과할 때만 사용한다.
- 정책 변경은 `wiki/policy-book/proposals/TEMPLATE-policy-change.md` 구조를 통과해야 하며, 단일 백테스트 평균만으로 `auto_eligible_paper`로 승격하지 않는다.

## 회고에서 나온 정책 변경

| 날짜 | 변경 | 근거 회고 | 상태 |
| --- | --- | --- | --- |
| 2026-05-22 | 거래 회고 체계를 신설하고, 체결 거래는 이후 결과와 당시 판단을 비교하도록 함 | 사용자 요청 및 하네스 구성 변경 | 적용 |
| 2026-05-23 | 과거 시점 추천 시뮬레이션과 1D/5D/20D 회고를 정책학습 입력으로 사용하도록 함 | `harness/workflows/historical-decision-sim.md`, `harness/workflows/historical-decision-review.md` | 적용 |
| 2026-05-23 | 회고 후 재시뮬레이션은 과최적화 위험을 명시하고 독립 기간 검증 전 정책 승격을 금지함 | [[2026-04-23-to-2026-05-08-historical-review-batch-v2]] | 적용 후보 |
| 2026-05-23 | 뉴스 촉매+상대강도 규칙은 별도 검증셋에서 60.0% hit rate에 그쳐 후보 발굴 신호로만 사용함 | [[2026-05-11-to-2026-05-15-historical-validation-review]] | 검증 중 |
| 2026-05-23 | 실적 beat 후 과열 필터와 MCP 확인 공백 감점을 적용하면 별도 검증셋이 80.0%로 개선됨 | [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-review]] | 검증 중 |
| 2026-05-23 | 최근 7일 1D 검증에서 뉴스 촉매+가격 돌파가 강하게 작동했지만 이벤트 집중 표본이라 정책 승격은 보류함 | [[2026-05-18-to-2026-05-22-recent-7d-historical-review]] | 검증 중 |
| 2026-05-23 | 뉴스와 가격의 선후관계를 후보 점수화에 반영함. 실적, 정책/테마, 대형주, 애널리스트 뉴스 유형을 분리해 평가 | [[2026-05-23-news-price-lead-lag-simulation]] | 적용 후보 |
| 2026-05-23 | 시간별 단타 후보 정책 `intraday-rs-breakout-v0`를 추가함. QQQ 초기 risk-on, 종목 상대강도, 돌파 유지, +2% take/-1% stop을 묶어 paper 검증 후보로 둠 | [[2026-05-23-march-april-intraday-scalping-simulation]] | 검증 중 |
| 2026-05-23 | `intraday-rs-breakout-v0`를 다른 일정으로 재검증함. 플러스였지만 take profit 도달 없이 EOD 수익과 무거래 필터 기여가 컸음 | [[2026-05-23-march-april-intraday-scalping-alt-simulation]] | 검증 중 |
| 2026-05-23 | 2026년 2월~5월 임의 일자로 5회 추가 반복 검증함. 총손익은 플러스였지만 hit rate가 47.8%로 낮아지고 동시 stop 위험이 확인됨 | [[2026-05-23-random-intraday-scalping-5x-simulation]] | 자동 주문 부적합 |
| 2026-05-23 | 1시간봉 timestamp를 보정하고 1분봉으로 stop/take 순서를 검증함. v0는 플러스였지만 confirmation variants가 안정적으로 개선하지 못해 자동 주문 부적합 유지 | [[2026-05-23-intraday-scalping-minute-validation]] | paper-only manual candidate |
| 2026-05-23 | 단타 성과 개선용 추가 필터를 검증함. 시장 VWAP, SMH VWAP, 종목 VWAP, 반도체 breadth 4개 이상을 결합한 v1이 v0보다 평균 거래 손익과 hit rate를 개선함 | [[2026-05-23-intraday-scalping-feature-filter-simulation]] | paper-only manual candidate |
| 2026-05-23 | 기존 v0/v1에서 덜 다룬 VWAP 평균회귀·장중 반전·거래량 확인 모멘텀을 검증함. 장초반 눌림 후 VWAP 회복 후보는 플러스였지만 v1보다 약했고, 거래량 확인 모멘텀은 폐기 후보로 분류함 | [[2026-05-23-intraday-policy-candidates-simulation]] | paper-only secondary candidate |
| 2026-05-23 | 장타 투자 목적의 20D 보유 정책을 2026년 2~3월 13개 기준일로 학습하고 4~5월 10개 기준일로 검증함. `quality_top5`가 학습/검증 모두 플러스이고 단순 모멘텀보다 drawdown이 낮아 장타 후보 정책으로 기록함 | [[2026-05-23-long-term-feb-mar-apr-may-simulation]] | paper-only long-term candidate |
| 2026-05-24 | 현재 단타/장타 정책을 같은 구조로 재점검함. 단타 v1은 4~5월 검증 1 active day/3거래 모두 stop으로 자동 주문 부적합이 강화됐고, 장타 `quality_top5`는 검증 완료 30개 추천 평균 20D +25.62%, SPY 대비 +18.64%p로 후보 유지 | [[2026-05-24-short-long-policy-feb-mar-apr-may-review]] | 단타 관찰 전용 / 장타 검증 중 유지 |
| 2026-05-24 | 남은 정책 시뮬레이션 이력을 MCP로 재감사함. 기존 결론은 대부분 유지하되, broad query 0건 fallback, SEC acceptance time, filing-aware event risk, 실적/filing 확인 후 과열 감점을 명시함 | [[2026-05-24-mcp-policy-history-reaudit]] | 적용 후보 |
| 2026-05-24 | 최근 6개월을 3시간 구간으로 재집계해 독립 시뮬레이션함. 단타 3시간 variants는 전체 플러스지만 IEX 30분봉/체결 공백 때문에 관찰 전용으로 유지하고, 장타 `daily-3h-theme-capped-top5`는 320개 완료 추천 평균 20D SPY 초과 +7.82%p로 장타 후보 보강 근거로 추가함 | [[2026-05-24-six-month-3h-independent-policy-review]] | 단타 관찰 전용 / 장타 검증 중 유지 |
| 2026-05-24 | 정책 개선 후보 5개를 같은 6개월 데이터로 검증함. 장타는 과열 제한+theme cap, SPY/QQQ 동시 초과 확인, 변동성/drawdown 방어 필터, staged entry 필터를 채택/보조채택 후보로 추가했고 단타 `intraday-afternoon-followthrough-filter-v1`은 성과 개선에도 자동 주문 금지를 유지함 | [[2026-05-24-policy-improvement-candidates]] | 장타 정책 보강 / 단타 관찰 전용 |
| 2026-05-24 | 기존 관심 종목 외 빅테크/금융/헬스케어/소비재/산업재/에너지/소재/유틸리티/고변동 성장주까지 62개 심볼로 확장해 최근 6개월 3시간 시뮬레이션을 재수행함. 단타 top3와 VWAP reclaim은 악화됐고, 장타 `daily-3h-theme-capped-top5`는 평균 SPY 초과 +7.65%p로 기존 +7.82%p와 유사하게 유지됨 | [[2026-05-24-expanded-six-month-3h-policy-review]] | 확장 universe는 theme cap 적용 시에만 사용 |
| 2026-05-24 | 외부 리뷰 개선사항을 반영해 정책 개선 백테스트를 날짜 key 기반 정렬로 바꾸고, 주문 risk gate에 theme/factor/speculative exposure cap을 추가함. raw source에는 구조화 시그널 표를 추가해 뉴스/공시/밸류에이션/매크로 feature를 재사용 가능하게 기록하도록 함 | `scripts/simulate-policy-improvement-candidates.py`, `scripts/check-risk-policy.py`, `harness/risk-policy.yaml` | 적용 |
| 2026-05-24 | 리뷰 개선사항 반영 후 확장 universe로 재시뮬레이션함. 장타 `lt-dual-benchmark-confirm-v1`과 `lt-drawdown-volatility-guard-v1`은 이전 기준선보다 검증 SPY 초과수익과 평균 불리 이동이 개선됐고, 단타 `intraday-afternoon-followthrough-filter-v1`은 기존 최고 variant보다 낮아 자동 주문 금지를 유지함 | [[2026-05-24-review-hardening-comparison]] | 장타 우선 필터 보강 / 단타 관찰 전용 |
| 2026-05-25 | Request.md 개선사항을 반영해 recommendation-policy YAML/schema, strategy config, symbol metadata, risk-policy v1.1, order-plan schema v1.2, 유동성/스프레드/클러스터/중복 ID gate, 일별 독립 1년 시뮬레이션 워크플로우를 추가함 | `Request.md`, `harness/recommendation-policy.yaml`, `harness/strategies/long-term-quality-momentum-v1.yaml`, `scripts/simulate-one-year-daily-policy.py` | 적용 / 장타 dry-run 후보 유지 / 단타 observation_only |

## 검증 중인 가설

| 가설 | 관련 회고 | 다음 확인 조건 |
| --- | --- | --- |
| 고변동 저가 mover는 점수보다 신뢰도와 유동성 필터가 중요하다 | [[2026-05-22]] no-submit 분석 | 실제 paper 거래 또는 회피 후 결과 비교가 쌓일 때 |
| SMH/QQQ/SPY 같은 ETF 후보는 개별 급등주보다 초기 paper 계좌의 기준 포지션으로 더 적합할 수 있다 | [[2026-05-22]] no-submit 분석 | 실제 배분 후 벤치마크 대비 결과가 생길 때 |
| 과거 시점 추천은 미래 정보 누출을 엄격히 막아야 정책학습 신호로 쓸 수 있다 | `harness/workflows/historical-decision-sim.md` | 1D/5D/20D 회고가 3회 이상 쌓일 때 |
| 5D 상대강도가 강한 대형/중형 기술 후보는 단기 추천에서 유리할 수 있다 | [[2026-04-23-to-2026-05-08-historical-review-batch]] | 엄격한 as-of raw source가 있는 기간에서도 반복 확인될 때 |
| 품질 점수와 단기 모멘텀 점수는 분리해야 한다 | [[2026-04-23-to-2026-05-08-historical-review-batch]] | 품질 우량 후보가 1D/5D에서 반복 부진할 때 |
| 뉴스 촉매와 상대강도가 동시에 있는 후보는 단기 추천 품질을 높일 수 있다 | [[2026-04-23-to-2026-05-08-historical-review-batch-v2]] | v2 규칙을 보지 않은 독립 기간에서 반복 확인될 때 |
| 후보군 누락은 가격/뉴스 보강으로 먼저 해소하고, 보강 후에도 성과가 약하면 추천 승격하지 않는다 | [[2026-04-23-to-2026-05-08-historical-review-batch-v2]] | PLTR 외 다른 누락 후보에서도 반복 확인될 때 |
| 강한 촉매가 있어도 과열 직후에는 5D 신규 매수 성과가 약해질 수 있다 | [[2026-05-11-to-2026-05-15-historical-validation-review]] | 과열 필터를 수치화한 뒤 독립 기간에서 개선되는지 확인할 때 |
| 실적 서프라이즈는 매수 가산점이 아니라 과열 여부와 함께 해석해야 한다 | [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-review]] | Alpha/SEC/IR 원천을 포함한 독립 기간 3개 이상에서 반복될 때 |
| 당일 뉴스 촉매와 가격 돌파가 동시에 확인된 후보는 1D 성과가 강할 수 있다 | [[2026-05-18-to-2026-05-22-recent-7d-historical-review]] | 이벤트 당일 종가 추격의 5D 반납 여부와 손실 사례까지 확인할 때 |
| 뉴스가 가격을 움직이는지, 가격이 뉴스보다 먼저 움직이는지는 뉴스 유형별로 다를 수 있다 | [[2026-05-23-news-price-lead-lag-simulation]] | 3개 이상 독립 기간에서 뉴스 전/후 1D/5D 수익률을 반복 측정할 때 |
| SEC filing과 공식 IR가 붙어도 고변동 테마주는 event risk를 낮추지 않고, acceptance time과 실적 질을 함께 본다 | [[2026-05-24-mcp-policy-history-reaudit]] | RGTI/QBTS/IONQ/NOK 외 다른 테마 이벤트에서도 반복 확인될 때 |
| MCP broad query 0건은 정보 부재가 아니라 provider/query coverage gap일 수 있다 | [[2026-05-24-mcp-policy-history-reaudit]] | Alpha/Firecrawl/SEC/Alpaca 간 불일치 사례를 반복 수집할 때 |
| 개장 초반 QQQ risk-on과 종목 상대강도/돌파가 동시에 확인되면 long-only 단타 후보가 될 수 있다 | [[2026-05-23-march-april-intraday-scalping-simulation]] | 2026년 4월 전체 거래일에 같은 규칙을 고정 적용해 무거래일 포함 기대값이 플러스인지 확인할 때 |
| 단타 VWAP/breadth 필터만으로는 추격 손실을 막지 못할 수 있다 | [[2026-05-24-short-long-policy-feb-mar-apr-may-review]] | 11:05/11:15 후속 유지, bid/ask spread, 첫 5~15분 adverse move를 포함한 variant에서 개선되는지 확인할 때 |
| 장타 후보는 theme cap에 과열 제한을 같이 넣어야 성과와 집중 리스크의 균형이 좋아질 수 있다 | [[2026-05-24-policy-improvement-candidates]] | fresh quote, 실적/filing/valuation 확인을 붙인 다음 추천 run에서 반복 확인할 때 |
| 관심 종목 밖으로 universe를 넓히면 후보 발굴 폭은 커지지만 단타 잡음과 성과 집중도 같이 늘어난다 | [[2026-05-24-expanded-six-month-3h-policy-review]] | 업종별 broad universe를 반복 검증하고 top symbols 집중도를 낮추는 제약을 추가할 때 |

## 시간별 단타 정책 후보

`intraday-rs-breakout-v0`는 자동 주문 원칙이 아니라 paper 검증 후보로만 사용한다. 2026-05-23 분봉 검증 후 상태는 `paper-only manual candidate`다. 즉, 자동 주문에는 부적합하지만 주문 없는 실시간 paper dry-run으로 추적할 가치는 있다.

- QQQ의 초기 hour bar 기반 수익률이 +0.20% 이상일 때만 long 진입을 검토한다. Alpaca `1Hour` timestamp는 시작 시각이므로, `10:00` hour bar close를 쓴 신호는 11:00 ET 이후에만 실행 가능하다.
- 후보 종목은 초기 구간 +0.90% 이상, QQQ 대비 +0.40%p 이상, 10:00 ET close가 직전 bar high 근처 이상일 때만 통과한다.
- 통과 종목 중 최대 3개, 종목당 계좌 가치 5~10% 이하로 제한한다.
- 청산은 +2.0% take, -1.0% stop, 또는 당일 15:00 ET close다.
- QQQ가 `neutral` 또는 `risk_off`면 단타 long 진입을 하지 않는다.
- 같은 날 2연속 stop이 발생하면 추가 진입을 중단한다.
- 2026-03-31처럼 장중 후반 반전이 있는 날은 이 정책의 대상이 아니다. 별도 `midday-reversal` 검증 없이는 후반 추격 규칙을 섞지 않는다.
- 12:00 ET confirmation 버전은 손실일 일부를 줄였지만 총 기대값을 개선하지 못했다. 현 상태에서는 11:00 ET 이후 v0 신호를 주문 없이 기록하는 dry-run이 다음 단계다.

`intraday-rs-breadth-vwap-v1`은 v0에 시장/섹터 확인을 추가한 후보 정책이다.

- v0 신호를 먼저 만족해야 한다.
- 11:00 ET 진입 시점에 QQQ가 당일 VWAP 위에 있어야 한다.
- SMH가 당일 VWAP 위에 있어야 한다.
- 후보 종목이 당일 VWAP 위에 있어야 한다.
- 반도체 breadth가 4개 이상이어야 한다. 대상은 SMH, NVDA, AMD, AVGO, TSM, LRCX이며, 11:00 ET 진입가가 당일 open보다 높은지로 계산한다.
- 수익 극대화형은 top3, 안정성 우선형은 top2로 추적한다.
- 자동 주문은 금지하고 실시간 paper dry-run에서 v0와 병렬 비교한다.

2026-05-24 검증에서는 4~5월 10개 표본 중 v1이 2026-04-01 하루만 active였고, 3개 거래가 모두 stop이었다. 따라서 v1은 자동 주문 후보가 아니라 관찰 전용이며, 최소한 11:05~11:15 후속 유지와 실제 spread/fill 확인이 붙기 전까지 주문 계획에 넣지 않는다.

`intraday-pullback-vwap-reclaim-v0`은 v1 신호가 없을 때 관찰할 보조 후보 정책이다.

- 09:30~10:59 ET에 후보 종목이 당일 open 대비 최소 -1.0% 이상 눌려야 한다.
- 11:00 ET 이론 진입가가 오전 저점 대비 최소 +0.8% 회복해야 한다.
- 11:00 ET 이론 진입가가 종목 VWAP 위에 있어야 한다.
- QQQ와 SMH가 11:00 ET 기준 VWAP 위에 있어야 한다.
- 11:00 ET 이론 진입가가 당일 open 대비 +1.0%를 넘으면 추격으로 보고 제외한다.
- 후보는 회복률 기준 상위 2개만 추적한다.
- +1.5% take, -0.8% stop, EOD 청산을 사용한다.
- 2026-03-02~2026-05-22 59거래일 보조 스캔에서 플러스였지만 v1보다 약하므로 자동 주문은 금지한다.

`volume-confirmed-momentum`은 현재 폐기 후보로 둔다. 2026-03-02~2026-05-22 스캔에서 6거래 모두 수익 실패, 5 stop, P/L -$425.87이었다.

## 장타 정책 후보

`long-term-quality-momentum-v0`는 20거래일 이상 보유를 전제로 한 장타 후보 선별 정책이다.

- 후보별 20D, 40D, 60D 수익률을 계산한다.
- 20D 수익률에서 SPY/QQQ 20D 수익률을 뺀 상대강도를 계산한다.
- 최근 60D 최대낙폭이 -30%보다 깊으면 제외한다.
- 최근 20D 일간 변동성이 7.0% 이상이면 제외한다.
- 60D 수익률이 -10%보다 낮으면 제외한다.
- 20D 수익률이 과도하게 높은 후보는 추격 위험으로 추가 감점한다.
- 점수 상위 5개를 같은 비중 또는 종목당 최대 15% 상한으로 분산한다.
- 2026년 2~3월 학습에서는 65개 추천, 평균 20D +7.18%, 평균 SPY 대비 +6.77%p였다.
- 2026년 4~5월 검증에서는 50개 추천 중 20D 완료 30개, 평균 20D +25.62%, 평균 SPY 대비 +18.64%p였다.
- 5월 기준일 일부는 20D가 아직 미완료이므로 자동 주문 정책으로 승격하지 않는다.
- 다음 검증은 실적, 밸류에이션, SEC filing, 뉴스 촉매, 포트폴리오 상관 노출을 추가한 보강 버전으로 수행한다.
- 2026-05-24 재점검에서도 4~5월 검증 완료 30개 추천은 평균 20D +25.62%, 평균 SPY 초과 +18.64%p였다. 다만 AMD/NOK 성과 집중과 5월 20D 미완료가 남아 있어 자동 주문 정책으로 승격하지 않는다.
- 2026-05-24 6개월 3시간 재집계에서는 `daily-3h-quality-top5`가 320개 완료 추천 평균 20D +9.73%, SPY 초과 +7.70%p였고, `daily-3h-theme-capped-top5`가 평균 20D +9.86%, SPY 초과 +7.82%p였다. theme cap이 성과를 크게 해치지 않아 자동 주문 전 분산 제약 후보로 유지한다.
- 2026-05-24 정책 개선 검증에서는 `lt-overheat-guard-theme-cap-v1`이 257개 완료 추천 평균 20D +10.32%, SPY 초과 +8.89%p, 검증 구간 SPY 초과 +14.54%p였다. 장타 기본 후보에 20D +45% 초과/5D +25% 초과 과열 제한을 추가한다.
- `lt-dual-benchmark-confirm-v1`은 233개 완료 추천 평균 SPY 초과 +9.48%p, 검증 구간 +16.44%p였다. SPY와 QQQ를 모두 이기는 20D 상대강도는 장타 우선순위 보조 조건으로 쓴다.
- `lt-drawdown-volatility-guard-v1`은 220개 완료 추천 평균 SPY 초과 +9.44%p, 평균 불리 이동 -7.12%였다. 시장이 불안하거나 계좌 방어가 필요할 때 20D 변동성 5.5% 이하, 40D drawdown -22% 이내 필터를 적용한다.
- `lt-anti-chase-staged-entry-v1`은 평균 SPY 초과 +6.65%p로 성과는 낮아지지만 추격 구간을 줄인다. 과열 후보는 한 번에 채우지 않고 staged entry로만 다룬다.
- 2026-05-24 확장 universe 검증에서는 `daily-3h-theme-capped-top5`가 320개 완료 추천 평균 20D +9.68%, 평균 SPY 초과 +7.65%p, 검증 구간 SPY 초과 +11.84%p였다. 기존 관심 종목 중심 결과와 유사해 theme cap은 확장 universe에서도 유지한다.
- 같은 확장 검증에서 `daily-3h-quality-top5`는 평균 SPY 초과 +6.73%p로 기존 +7.70%p보다 낮았고, `daily-3h-momentum-top3`는 평균 SPY 초과 +8.30%p지만 평균 불리 이동 -10.41%였다. 따라서 넓은 universe에서는 단순 quality 또는 단순 momentum보다 theme cap과 과열 제한을 우선한다.
- 리뷰 개선사항 반영 후 확장 universe 재시뮬레이션에서는 `lt-dual-benchmark-confirm-v1`이 평균 SPY 초과 +8.03%p, 검증 +13.15%p, 평균 불리 이동 -7.86%였고, `lt-drawdown-volatility-guard-v1`이 평균 SPY 초과 +7.91%p, 검증 +13.25%p, 평균 불리 이동 -7.75%였다. 이전 `daily-3h-theme-capped-top5`의 평균 SPY 초과 +7.65%p, 검증 +11.84%p, 평균 불리 이동 -9.07%보다 방어적 품질이 좋아졌으므로 다음 장타 후보 선별의 우선 필터로 둔다.

`momentum_top3`식 단순 20D 모멘텀 정책은 보조 비교군으로만 둔다. 검증 성과는 좋았지만 2~3월 학습에서 평균 20D +1.19%, 평균 20D 불리 이동 -11.20%로 장타 목적에 부적합했다.

### 실시간 paper dry-run 운영 원칙

다음 단계는 `harness/workflows/intraday-paper-dry-run.md`를 사용해 11:00 ET 신호를 기록하는 것이다. 이 운영은 주문 계획이 아니라 관찰 로그이며, `orders_submitted=0`을 명시해야 한다.

- 10:00-10:59 ET 데이터가 완성된 뒤 11:00 ET 이후 첫 1분봉 open을 이론적 entry reference로 기록한다.
- v0 top3/top2와 v1 top3/top2를 같은 후보군에서 병렬 기록한다.
- v1은 QQQ VWAP, SMH VWAP, 후보 VWAP, 반도체 breadth 4개 이상을 모두 통과해야 한다.
- 11:00 ET 근처 bid/ask, spread, quote freshness, fill 가능성을 반드시 별도 필드로 남긴다. bid/ask가 없으면 fill 가능성은 `unknown`이다.
- 12:00 ET 확인은 상태 기록용으로만 쓰고 새 진입 신호를 만들지 않는다.
- 15:59 ET 또는 장 마감 후 1분봉으로 stop/take/EOD 이론 결과를 기록한다.
- 반복 관찰에서 slippage, spread, 동시 stop, VWAP 이탈 문제가 확인되기 전까지 자동 주문 승격을 금지한다.
- `intraday-afternoon-followthrough-filter-v1`은 첫 3시간 QQQ risk-on, 첫 두 3시간 구간의 QQQ 대비 상대강도, window VWAP 확인, speculative theme 과열 제외를 결합한 관찰 후보로 추가한다. 2025-11-24~2026-05-22 백테스트에서 78거래, hit rate 58.97%, 가상 P/L +$1,386.98였지만, IEX 30분봉과 실제 bid/ask/fill 공백 때문에 자동 주문은 계속 금지한다.
- 확장 universe 검증에서는 `3h-momentum-top3`가 기존 $+981.43에서 $-150.28로 악화됐고 `3h-vwap-reclaim-top2`도 $+734.04에서 $-580.17로 악화됐다. 단타에 broad universe를 그대로 쓰지 말고 top2 제한, 후속 유지 확인, fresh quote/spread/fill 확인을 통과한 paper-only 관찰에만 사용한다.

## 뉴스-가격 선후관계 적용 규칙

후보 점수화 전에 각 뉴스 이벤트를 아래 네 유형으로 분류한다.

| 유형 | 가격 반응 경향 | 점수 반영 |
| --- | --- | --- |
| 실적 surprise | 다음 거래일 1D 반응이 빠를 수 있음 | 실적 직후 1D 반응은 인정하되, 3~5D 누적 급등 후 신규 매수는 감점 |
| 정책/테마 뉴스 | 뉴스 당일 가격 돌파와 다음날 후속 흐름이 같이 나타날 수 있음 | 당일 급등만으로 추격하지 않고, 다음 거래일 유지 확인 전까지 소액/관망 |
| 대형 인기주 긍정 뉴스 | 뉴스 전 기대 선반영이나 발표 후 차익실현 가능 | 뉴스 전 3D/5D 상승률, 고점 대비 위치, 거래량 과열을 먼저 확인 |
| 애널리스트 목표가/의견 | thesis 확인용 보조 신호 | 단독 매수 신호로 쓰지 않고 다른 촉매·가격 신호와 결합 |

각 후보는 아래 항목을 기록한다.

- `news_type`: earnings, theme_policy, mega_cap_expectation, analyst, macro, unknown.
- `pre_news_3d_return`, `pre_news_5d_return`: 뉴스 전 가격 선반영 여부.
- `event_day_return`: 뉴스 당일 가격 반응.
- `post_news_1d_return`, `post_news_5d_return`: 뉴스 후 후속 반응. 미래 정보가 필요한 값은 회고 문서에만 기록한다.
- `lead_lag_label`: news-led, price-led, same-day, sell-the-news, inconclusive.

## 정책학습 지표

과거 추천 회고에서 반복적으로 등장하는 교훈은 아래 지표로 관리한다. 단일 사례는 가설로만 기록하고, 최소 3회 이상 반복되거나 손익 영향이 큰 경우에만 현재 원칙으로 승격한다.

| policy_signal_id | 교훈 | evidence_count | hit_rate | avg_excess_return | max_drawdown_note | status | 근거 |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
| leakage-control | 추천 단계와 회고 단계의 미래 정보 분리 | 0 |  |  |  | 적용 원칙 | `harness/workflows/historical-decision-sim.md` |
| low-confidence-sizing | 신뢰도 낮은 고변동 종목은 소액 또는 관망 처리 | 0 |  |  |  | 검증 중 | [[2026-05-22]] |
| short-term-relative-strength | 5D 상대강도가 강한 대형/중형 기술 후보는 단기 회고에서 유리했다 | 48 | 54.2% | 계산 필요 | 주말 중복과 fallback universe 때문에 신뢰도 중간 이하 | 검증 중 | [[2026-04-23-to-2026-05-08-historical-review-batch]] |
| weekend-duplicate-samples | 주말 보정 기준일은 독립 표본으로 과대평가하지 않는다 | 4 |  |  | 동일 as-of 반복 | 적용 원칙 후보 | [[2026-04-23-to-2026-05-08-historical-review-batch]] |
| catalyst-plus-relative-strength | 뉴스 촉매와 5D 상대강도가 동시에 있는 후보가 단기 추천에 유리했다 | 48 | 97.9% | +9.63%p | v1 회고 후 설계되어 과최적화 위험 높음 | 검증 중 | [[2026-04-23-to-2026-05-08-historical-review-batch-v2]] |
| candidate-gap-check | 누락 후보는 가격/뉴스를 보강하되, 보강 후 성과가 약하면 승격하지 않는다 | 1 |  |  | PLTR 가격 공백 해소 후 추천 미승격 | 검증 중 | [[2026-04-23-to-2026-05-08-historical-review-batch-v2]] |
| overfit-warning | 회고 후 만든 v2 규칙은 독립 기간 검증 전 강한 정책으로 승격하지 않는다 | 1 |  |  | 사후 규칙 조정 | 적용 원칙 후보 | [[2026-04-23-to-2026-05-08-historical-review-batch-v2]] |
| catalyst-plus-relative-strength-oos | 뉴스 촉매+상대강도 규칙을 별도 검증셋에 적용하면 성과가 크게 낮아졌다 | 15 | 60.0% | +0.73%p | 성과가 2026-05-15에 집중, 과열 구간 취약 | 검증 중 | [[2026-05-11-to-2026-05-15-historical-validation-review]] |
| overextension-filter-needed | 촉매 후보라도 최근 급등, 과매수, 차익실현 뉴스가 있으면 신규 매수 점수를 낮춰야 한다 | 15 |  |  | AMD/IONQ/NVDA가 2026-05-11~05-14에 되돌림 | 검증 중 | [[2026-05-11-to-2026-05-15-historical-validation-review]] |
| earnings-beat-overextension-filter | 실적 beat가 확인돼도 발표 후 3~5거래일 누적 상승률이 과도하면 신규 매수 점수를 낮춘다 | 15 | 80.0% | +3.35%p | AMD 2026-05-05 실적 beat 후 2026-05-11~05-12 추격매수 회피가 개선에 기여 | 검증 중 | [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-review]] |
| mcp-confirmation-gap-penalty | 보강 MCP가 뉴스/filing/macro를 확인하지 못하면 긍정 신호를 추가하지 않고 공백으로 남긴다 | 15 | 80.0% | +3.35%p | Alpha NEWS_SENTIMENT 0건, SEC/FRED 공백을 긍정 신호로 오해하지 않음 | 검증 중 | [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-review]] |
| mcp-cross-source-fallback | 한 provider의 broad query가 0건이면 개별 ticker, Alpaca news, SEC EDGAR, 공식 IR 순서로 재확인한다 | 5 source groups |  |  | Alpha broad 0건과 개별 ticker 결과 불일치, Firecrawl domain 제한 0건 후 broader query 성공 | 적용 후보 | [[2026-05-24-mcp-policy-history-reaudit]] |
| 1d-event-catalyst-confirmation | 당일 뉴스 촉매와 가격 돌파가 동시에 확인된 후보는 1D 초과수익이 강할 수 있다 | 12 | 100.0% | +5.63%p | 2026-05-21 양자컴퓨팅 이벤트에 성과가 집중되어 추격매수 위험 큼 | 검증 중 | [[2026-05-18-to-2026-05-22-recent-7d-historical-review]] |
| filing-aware-event-risk | 8-K/10-Q/6-K/Form 4/144는 filing date가 아니라 acceptance time 기준으로 as-of 사용 가능 여부를 판단하고, 이벤트 리스크 태그로 분리한다 | 5 tickers |  |  | IONQ 2026-05-08 Form 4는 종가 이후 acceptance, RGTI/QBTS 2026-05-21 8-K는 장전 acceptance | 적용 후보 | [[2026-05-24-mcp-policy-history-reaudit]] |
| news-price-lead-lag | 뉴스 전/후 가격 반응을 분리해 뉴스 주도, 가격 선행, 당일 동행, sell-the-news를 구분한다 | 10 |  |  | 대표 이벤트 중심 수동 분류. 장중 선후관계는 일봉만으로 한계 있음 | 적용 후보 | [[2026-05-23-news-price-lead-lag-simulation]] |
| sell-the-news-risk | 좋은 뉴스에도 당일 또는 다음날 하락하면 기대 선반영과 차익실현 위험으로 감점한다 | 1 |  |  | NVDA 2026-05-21~05-22 사례 | 검증 중 | [[2026-05-23-news-price-lead-lag-simulation]] |
| theme-news-follow-through | 정책/테마 뉴스는 당일 급등보다 다음 거래일 유지 여부를 더 높게 평가한다 | 4 |  |  | RGTI/QBTS/IONQ/NOK 2026-05-21~05-22 사례 | 검증 중 | [[2026-05-23-news-price-lead-lag-simulation]] |
| earnings-fast-reaction | 실적 surprise는 발표 직후 1D 반응과 3~5D 과열 구간을 분리 평가한다 | 1 |  |  | AMD 2026-05-05~05-06 사례 | 검증 중 | [[2026-05-23-news-price-lead-lag-simulation]] |
| intraday-rs-breakout-v0 | 개장 초반 QQQ risk-on과 종목 상대강도/돌파가 동시에 확인된 후보만 long 단타로 진입한다. 1시간봉 timestamp 보정 후 11:00 ET 이후 진입으로 해석한다 | 28 trading days / 34 trades | 55.9% trade hit | +$1,410.00 on $10k per trade simulation | 1분봉 검증상 플러스지만 confirmation variants가 개선 실패. IEX feed/슬리피지/fill 불확실성 남음 | paper-only manual candidate | [[2026-05-23-march-april-intraday-scalping-simulation]], [[2026-05-23-march-april-intraday-scalping-alt-simulation]], [[2026-05-23-random-intraday-scalping-5x-simulation]], [[2026-05-23-intraday-scalping-minute-validation]] |
| intraday-rs-breadth-vwap-v1 | v0에 QQQ/SMH/종목 VWAP 확인과 반도체 breadth 4개 이상 조건을 추가한다 | 28 trading days / 27 trades | 59.3% trade hit | +$1,547.25 on $10k per trade simulation | 거래 수 감소. IEX VWAP, slippage, fill 가능성 미반영. 독립 실시간 검증 필요 | paper-only manual candidate | [[2026-05-23-intraday-scalping-feature-filter-simulation]] |
| intraday-rs-breadth-vwap-v1-top2 | v1 조건을 만족한 후보 중 상위 2개만 진입한다 | 28 trading days / 18 trades | 66.7% trade hit | +$1,395.55 on $10k per trade simulation | 총손익은 v1 top3보다 낮지만 평균 거래 손익은 높음 | paper-only manual candidate | [[2026-05-23-intraday-scalping-feature-filter-simulation]] |
| intraday-followthrough-filter-needed | 11:00 ET 돌파/VWAP/breadth 조건만으로는 4~5월 검증 손실을 막지 못했다. 11:05~11:15 후속 유지와 실제 spread/fill 확인을 추가한다 | validation 10 days / v1 3 trades | 0.0% trade hit | -$300.00 on $10k per trade simulation | 2026-04-01 TSLA/AMD/LRCX 모두 stop. v0도 9거래 중 7 stop | 적용 후보 | [[2026-05-24-short-long-policy-feb-mar-apr-may-review]] |
| intraday-pullback-vwap-reclaim-v0 | 장초반 -1% 이상 눌린 종목이 11:00 ET에 VWAP 위로 회복하고 QQQ/SMH도 VWAP 위일 때만 long 진입 후보로 본다 | train 5 days / 6 trades; validation 5 days / 10 trades; 59-day scan / 38 trades | validation 60.0%; 59-day scan 55.3% | validation +$222.57; 59-day scan +$822.98 on $10k per trade simulation | v1보다 평균 거래 손익이 낮고 2026-04-01처럼 동시 stop 가능. 실제 spread/fill 미반영 | paper-only secondary candidate | [[2026-05-23-intraday-policy-candidates-simulation]] |
| three-hour-intraday-momentum | 첫 3시간 QQQ risk-on과 종목 상대강도가 동시에 나타난 후보를 다음 3시간 구간 open에 진입하는 독립 variant | 124 trading days / 127 trades | 48.0% trade hit | +$981.43 on $10k per trade simulation | 앞구간은 -$658.86, 뒤구간은 +$1,640.29로 regime 의존. IEX 30분봉, spread/fill 미반영 | paper-only research candidate | [[2026-05-24-six-month-3h-independent-policy-review]] |
| three-hour-vwap-reclaim | 첫 3시간 하락 후 window VWAP 위로 회복한 후보를 다음 구간에 진입하는 독립 variant | 124 trading days / 35 trades | 48.6% trade hit | +$734.04 on $10k per trade simulation | 검증 hit 38.9%, stop 17건. 단독 주문 신호로 약함 | paper-only secondary candidate | [[2026-05-24-six-month-3h-independent-policy-review]] |
| three-hour-afternoon-continuation | 첫 두 3시간 구간에서 QQQ 대비 강한 상대강도를 보인 후보를 15:30 ET 근처에 짧게 추적하는 variant | 124 trading days / 90 trades | 61.1% trade hit | +$1,530.61 on $10k per trade simulation | 장마감 직전 짧은 보유라 체결/스프레드 민감. 실제 quote 없는 자동 주문 금지 | paper-only research candidate | [[2026-05-24-six-month-3h-independent-policy-review]] |
| volume-confirmed-momentum | 10시대 상승이 거래량 증가와 같이 나타날 때 추격한다 | 59-day scan / 6 trades | 0.0% | -$425.87 on $10k per trade simulation | 가격+거래량 추격이 모두 실패. stop 5건, EOD 손실 1건 | rejected | [[2026-05-23-intraday-policy-candidates-simulation]] |
| long-term-quality-momentum-v0 | 20D/40D/60D 추세, SPY/QQQ 상대강도, 60D drawdown, 20D 변동성, 거래량 변화를 함께 점수화해 top5로 분산한다 | train 13 as-of days / 65 recommendations; validation 10 as-of days / 50 recommendations | train 20D SPY hit 42/65; validation completed 20D SPY hit 24/30 | train avg 20D excess +6.77%p; validation completed avg 20D excess +18.64%p | 5월 기준일 일부 20D 미완료. 가격 기반만 사용해 실적/밸류에이션/filing 미반영 | paper-only long-term candidate | [[2026-05-23-long-term-feb-mar-apr-may-simulation]] |
| daily-3h-theme-capped-quality | 20D/40D 추세, SPY/QQQ 상대강도, drawdown, 변동성, 최근 첫 3시간 양봉 빈도에 테마별 최대 2종목 제한을 더한 장타 variant | 84 as-of days / 420 recommendations / 320 completed | 214/320 SPY hit | +7.82%p avg 20D SPY excess | 평균 20D 불리 이동 -8.34%, NOK/AMD 성과 집중. 실적/filing/valuation 미반영 | paper-only long-term candidate | [[2026-05-24-six-month-3h-independent-policy-review]] |
| daily-3h-momentum-top3 | 첫 3시간 양봉 빈도와 20D 상대강도를 요구하는 집중형 장타 비교군 | 83 as-of days / 234 recommendations / 174 completed | 110/174 SPY hit | +10.62%p avg 20D SPY excess | 평균 20D 불리 이동 -9.47%, AMD/NOK/IONQ 집중. 기본 정책보다 비교군으로 유지 | comparison only | [[2026-05-24-six-month-3h-independent-policy-review]] |
| lt-overheat-guard-theme-cap-v1 | 장타 quality+theme cap에 20D +45% 초과, 5D +25% 초과 과열 제한을 추가한다 | 84 as-of days / 357 recommendations / 257 completed | 174/257 SPY hit | +8.89%p avg 20D SPY excess | 평균 불리 이동 -7.16%, 검증 구간 SPY 초과 +14.54%p. NOK/AMD 성과 집중은 남음 | long-term candidate filter | [[2026-05-24-policy-improvement-candidates]] |
| lt-dual-benchmark-confirm-v1 | 20D 수익률이 SPY와 QQQ를 모두 초과하고 40D 추세가 양수인 후보만 우선순위에 둔다 | 84 as-of days / 331 recommendations / 233 completed | 155/233 SPY hit | +9.48%p avg 20D SPY excess | 평균 불리 이동 -7.11%, 검증 구간 SPY 초과 +16.44%p. 후보 수 감소 | long-term priority filter | [[2026-05-24-policy-improvement-candidates]] |
| lt-drawdown-volatility-guard-v1 | 방어형 상황에서 20D 변동성 5.5% 이하, 40D drawdown -22% 이내 후보만 사용한다 | 82 as-of days / 320 recommendations / 220 completed | 143/220 SPY hit | +9.44%p avg 20D SPY excess | 평균 불리 이동 -7.12%, 검증 구간 SPY 초과 +17.10%p. 성과는 NOK/AMD 집중에 민감 | defensive long-term filter | [[2026-05-24-policy-improvement-candidates]] |
| lt-anti-chase-staged-entry-v1 | 5D -7%~+12%, 20D +2%~+35% 범위에서만 staged entry 후보로 둔다 | 82 as-of days / 282 recommendations / 188 completed | 117/188 SPY hit | +6.65%p avg 20D SPY excess | 평균 불리 이동 -7.26%, 검증 구간 SPY 초과 +11.38%p. 추격 제한용으로 사용 | staged-entry filter | [[2026-05-24-policy-improvement-candidates]] |
| intraday-afternoon-followthrough-filter-v1 | 첫 3시간 QQQ risk-on, 첫 두 3시간 상대강도 유지, VWAP 위 가격, speculative 과열 제외를 결합한다 | 124 trading days / 78 trades | 59.0% trade hit | +$1,386.98 on $10k per trade simulation | 검증 구간 +$1,053.78. IEX 30분봉, spread/fill 미반영으로 자동 주문 금지 | paper-only research candidate | [[2026-05-24-policy-improvement-candidates]] |
| expanded-universe-theme-capped-quality | 관심 종목 외 다양한 업종을 포함한 broad universe에서 장타 theme cap top5를 유지한다 | 84 as-of days / 420 recommendations / 320 completed | 186/320 SPY hit | +7.65%p avg 20D SPY excess | 검증 구간 +11.84%p. INTC/NOK/AMD 성과 집중이 있어 실적/filing/valuation 확인 필요 | long-term universe rule | [[2026-05-24-expanded-six-month-3h-policy-review]] |

## 폐기하거나 완화한 규칙

| 날짜 | 규칙 | 이유 |
| --- | --- | --- |
