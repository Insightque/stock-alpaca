---
id: 2026-05-24-mcp-policy-history-reaudit
created_at: 2026-05-24T11:25:00+09:00
source_type: mcp-policy-history-reaudit
paper: true
---

# 남은 시뮬레이션 이력 MCP 보강 재검토

## 목적

2026-05-08 표본 비교에서 MCP 보강 정보가 추천 세트 자체보다 판단 근거와 제외 사유를 더 정밀하게 만든다는 점이 확인됐다. 이번 문서는 나머지 시뮬레이션/정책 분석 이력도 같은 방식으로 다시 훑어, 기존 정책 결론이 바뀌는지 확인한다.

실제 주문은 제출하지 않았다. 이 검토는 정책학습과 데이터 공백 식별용이다.

## 범위와 방법

전체 분봉/일봉 시뮬레이션을 모두 재계산하지는 않았다. 이미 계산된 가격 성과는 보존하고, 추가 MCP 정보가 아래 질문에 답을 바꾸는지 확인했다.

- 당시 추천 후보를 더 강하게 뒷받침하는 공식 실적/filing/IR 근거가 있었는가?
- 추천 제외 후보가 새 정보로 추천 후보가 되어야 했는가?
- 기존 정책학습 결론이 데이터 공백이나 provider query 실패 때문에 왜곡됐는가?
- 단타/장타 정책에 새로 필요한 데이터 항목이 추가되는가?

사용 원천은 [[2026-05-24-mcp-policy-history-reaudit-sources]]에 기록했다.

## 결론 요약

| 이력 묶음 | MCP 보강 후 판단 |
| --- | --- |
| 2026-04-23~05-08 v1/v2 추천/회고 | 2026-05-08 표본에서 확인한 결론을 뒤집을 정보는 없었다. v2의 촉매+상대강도 규칙은 유용하지만 과최적화 경고를 유지한다. |
| 2026-05-11~05-15 검증 및 MCP 보강 검증 | SEC/IR가 붙으면서 MCP 보강 검증의 신뢰도가 올라갔다. 기존 `earnings-beat-overextension-filter`와 `mcp-confirmation-gap-penalty`는 유지한다. |
| 2026-05-18~05-22 최근 7일 추천/회고 | RGTI/QBTS/NOK 이벤트가 SEC/IR로 확인되면서 1D 이벤트 성과의 출처는 선명해졌다. 하지만 성과 집중도도 더 커졌으므로 정책 승격 보류가 맞다. |
| 뉴스-가격 선후관계 분석 | AMD, IONQ, RGTI/QBTS, NOK 모두 공식/SEC 근거가 붙어 lead/lag 분류의 신뢰도는 올라갔다. broad query 0건 fallback 규칙이 필요하다. |
| 단타 정책 분석들 | MCP 보강은 과거 분봉 손익을 바꾸지 않는다. 다만 이벤트일/filing일/실적일 태그, 뉴스 timestamp, spread/fill 확인 필요성이 더 강해졌다. |
| 장타 정책 분석들 | `quality_top5` 유지 결론은 바뀌지 않는다. 다만 AMD/NOK 성과 집중과 양자 종목의 mixed fundamentals 때문에 실적/filing/테마상한 보강 없이는 자동 주문으로 올리지 않는다. |

## 과거 추천 이력 재검토

### 2026-04-23~2026-05-08

선행 문서 [[2026-05-24-mcp-comparison-2026-05-08-historical-simulation]]에서 2026-05-08 표본을 깊게 확인했다.

- 원래 추천 `NVDA, IONQ, UNH`는 유지됐다.
- AMD는 실적 beat와 긍정 뉴스가 있었지만 2026-05-01→05-08 +26.22% 급등 후 2026-05-08→05-15 -6.83%로 되돌림이 컸다.
- TSLA는 뉴스가 혼재했고 2026-05-08→05-15 -1.41%라 추천 제외 판단이 유지됐다.

이번 추가 재감사에서 2026-05-11 이후 AMD 10-Q/8-K, IONQ 8-K/10-Q, 공식 IR 자료가 더 붙었지만, 이것은 `2026-05-08 기준 추천`을 소급 변경하는 근거가 아니라 `왜 그 판단이 타당했는지`를 설명하는 사후 회고 자료다.

정책 판단:

- v2의 `catalyst-plus-relative-strength`는 후보 발굴 신호로 유지한다.
- `overfit-warning`은 유지한다.
- AMD 사례는 `earnings-beat-overextension-filter`의 보조 근거로 추가한다.

### 2026-05-11~2026-05-15

기존 MCP 보강 검증은 Alpha Vantage 실적 데이터와 MCP 공백 감점을 반영해 5D hit rate 80.0%, 평균 SPY 대비 +3.35%p를 기록했다. 이번 SEC/Firecrawl 보강은 그 결론을 강화한다.

확인한 보강 근거:

- AMD: 2026-05-05 8-K, 2026-05-06 10-Q, Alpha EPS surprise +6.2016%, AMD 공식 IR Q1 revenue $10.3B.
- IONQ: 2026-05-06 8-K, 2026-05-07 10-Q, Alpha/IonQ 공식 Q1 revenue $64.7M, +755% YoY.
- NOK: 2026-04-23 Q1 EPS surprise +10.1504%, Nokia 공식 Q1 comparable net sales 성장, 2026-05-13/18/20 6-K.
- RGTI/QBTS: 실적/filing은 존재하지만 RGTI EPS surprise는 부정적이고 QBTS는 EPS beat와 revenue decline이 섞였다.

정책 판단:

- `mcp-enhanced-validation`의 개선은 단순히 더 많은 뉴스를 붙인 결과가 아니라, 실적 beat 뒤 과열 후보를 감점하고 provider 0건을 긍정 신호로 오해하지 않은 결과로 보는 것이 맞다.
- Alpha broad query 0건은 정보 부재가 아니므로, 앞으로는 개별 ticker Alpha 조회와 SEC/IR fallback을 함께 쓴다.
- FRED 공백은 여전히 남아 있어 macro regime 점수는 강화하지 않는다.

## 최근 7일 이벤트 구간 재검토

2026-05-18~05-22 리뷰는 12/12 hit, 평균 1D SPY 대비 +5.63%p였지만 2026-05-21 양자컴퓨팅 이벤트에 성과가 집중되어 정책 승격을 보류했다.

이번 MCP 보강은 이 보류 판단을 더 강하게 만든다.

| 티커 | 보강 확인 | 정책 의미 |
| --- | --- | --- |
| RGTI | 2026-05-21 8-K, 2026-05-21/22 Form 144/Form 4, Q1 revenue/roadmap 뉴스와 EPS miss 혼재 | 이벤트 추격보다 filing-aware risk tag 필요 |
| QBTS | 2026-05-21 8-K, 2026-05-21/22 Form 144/Form 4, EPS beat와 revenue -81%/bookings +1,994% 혼재 | 가격 follow-through는 강했지만 fundamental 품질은 혼합 |
| IONQ | 앞선 8-K/10-Q와 공식 revenue beat가 이미 확인됨 | 양자 테마 중 상대적으로 근거가 강하나 고변동 소액 제한 유지 |
| NOK | 6-K와 공식 Q1/AI networking lab source 확인 | 이벤트성 강세는 설명되지만 이미 4~5월 성과 집중도가 높음 |

정책 판단:

- `1d-event-catalyst-confirmation`은 유지하되 자동 주문 승격은 금지한다.
- 2026-05-21 같은 날은 `theme-news-follow-through`와 함께 `filing-aware-event-risk`를 붙인다.
- 고변동 테마주는 1D 수익이 좋아도 5D/20D 반납 확인 전까지 소액 또는 관망 라벨을 유지한다.

## 단타 정책 이력 재검토

MCP 보강 정보는 단타의 과거 가격 결과를 직접 바꾸지 않는다. 1분봉 stop/take, VWAP, breadth 조건의 손익은 이미 계산된 가격 데이터가 기준이다.

다만 새 정보는 단타 정책을 자동 주문으로 올릴 수 없다는 결론을 강화한다.

- 2026-04-01과 2026-05-13 같은 손실 구간은 가격/브레드스 필터만으로 gap-and-fade를 막지 못했다.
- TSLA, AMD, RGTI/QBTS 같은 이벤트 민감 종목은 뉴스 timestamp와 filing acceptance time이 없으면 11:00 ET 신호의 해석이 불완전하다.
- Alpha/FRED/Firecrawl/SEC provider별 응답 공백이 존재하므로 실시간 단타 판단에는 `source_confidence`가 필요하다.

추가 데이터 요구:

- 09:30~11:15 ET 뉴스 timestamp와 filing acceptance time.
- 10:59~11:15 ET bid/ask spread, mid-price, limit fill 가능성.
- 이벤트일 태그: earnings, SEC filing, analyst, policy/theme, macro.
- 장중 첫 5분/15분 adverse move.
- provider query failure와 true no-news를 구분하는 상태값.

정책 판단:

- `intraday-rs-breakout-v0`, `intraday-rs-breadth-vwap-v1`, `intraday-pullback-vwap-reclaim-v0`는 모두 paper-only 관찰 후보로 유지한다.
- 자동 주문 후보로 승격하지 않는다.

## 장타 정책 이력 재검토

`long-term-quality-momentum-v0`는 2~3월 학습과 4~5월 검증 모두 플러스였고, 이번 MCP 보강 후에도 유지할 가치가 있다.

다만 MCP 자료는 장타 정책의 취약점도 분명히 했다.

- AMD는 공식 실적/10-Q/8-K가 강하지만 5월 초 급등 후 과열 감점이 필요하다.
- NOK는 Q1 beat와 공식 Q1/AI networking lab 자료가 있어 장타 후보 근거가 보강된다.
- RGTI/QBTS는 가격 follow-through가 강해도 실적 질이 혼합적이라 장타 top5에는 테마 상한과 fundamental gate가 필요하다.
- NVDA 같은 대형 인기주는 좋은 뉴스에도 2026-05-18~05-22 하락해 sell-the-news/expectation risk를 계속 봐야 한다.

정책 판단:

- `quality_top5`는 장타 후보 선별의 기본 정책으로 유지한다.
- 자동 주문 전에는 `quality_top5 + earnings/filing confirmation + theme exposure cap + staged entry` 보강 버전을 만들어 같은 검증셋에 재적용한다.
- 같은 theme exposure가 40%를 넘으면 다음 후보로 대체하는 variant를 우선 테스트한다.

## 추가 전략/데이터 제안

| 항목 | 제안 |
| --- | --- |
| MCP fallback | Alpha broad query 0건이면 개별 ticker query, Alpaca news, SEC EDGAR, Firecrawl 공식 IR 순으로 fallback한다. |
| filing-aware event tag | 8-K/10-Q/6-K/Form 4/144를 event source로 분리하고 acceptance time 기준으로 as-of 사용 가능 여부를 판단한다. |
| earnings-overextension gate | EPS/revenue surprise가 있어도 발표 후 3D/5D 누적 수익률과 거래량 과열을 먼저 감점한다. |
| theme exposure cap | 장타 top5에서 AI semiconductor, quantum/speculative, networking, healthcare, power infrastructure theme 비중을 기록하고 40% 초과 시 대체 후보를 찾는다. |
| staged entry | 장타 후보가 20D 급등 상태면 즉시 진입 대신 3D pullback 또는 10D moving-average 유지 확인을 테스트한다. |
| intraday source confidence | 단타 dry-run 결과에 `news_timestamp_status`, `filing_status`, `spread_status`, `fill_confidence` 필드를 추가한다. |
| macro gap | FRED MCP 래퍼를 계속 점검하고, 실패 시 Alpha/FRED direct source를 raw note로 대체하는 fallback을 설계한다. |

## 정책 반영

이번 재감사는 기존 정책을 크게 뒤집기보다, 아래 원칙을 강화한다.

- MCP 데이터가 추천 종목을 바꾸는 경우보다, 추천/제외 사유의 신뢰도를 조정하는 경우가 많다.
- provider 0건은 정보 부재가 아니라 provider coverage/query 실패일 수 있다.
- 실적/filing/IR 공식 근거가 붙어도 가격이 이미 과열이면 신규 매수 점수를 낮춘다.
- 테마 이벤트의 1D 성과는 5D/20D 검증 전 자동 주문 근거가 아니다.

## 연결 문서

- 원천: [[2026-05-24-mcp-policy-history-reaudit-sources]]
- 선행 표본 비교: [[2026-05-24-mcp-comparison-2026-05-08-historical-simulation]]
- 정책: [[recommendation-policy]]
