---
id: recommendation-policy
updated_at: 2026-05-23T08:45:00+09:00
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

## 회고에서 나온 정책 변경

| 날짜 | 변경 | 근거 회고 | 상태 |
| --- | --- | --- | --- |
| 2026-05-22 | 거래 회고 체계를 신설하고, 체결 거래는 이후 결과와 당시 판단을 비교하도록 함 | 사용자 요청 및 하네스 구성 변경 | 적용 |
| 2026-05-23 | 과거 시점 추천 시뮬레이션과 1D/5D/20D 회고를 정책학습 입력으로 사용하도록 함 | `harness/workflows/historical-decision-sim.md`, `harness/workflows/historical-decision-review.md` | 적용 |
| 2026-05-23 | 회고 후 재시뮬레이션은 과최적화 위험을 명시하고 독립 기간 검증 전 정책 승격을 금지함 | [[2026-04-23-to-2026-05-08-historical-review-batch-v2]] | 적용 후보 |
| 2026-05-23 | 뉴스 촉매+상대강도 규칙은 별도 검증셋에서 60.0% hit rate에 그쳐 후보 발굴 신호로만 사용함 | [[2026-05-11-to-2026-05-15-historical-validation-review]] | 검증 중 |
| 2026-05-23 | 실적 beat 후 과열 필터와 MCP 확인 공백 감점을 적용하면 별도 검증셋이 80.0%로 개선됨 | [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-review]] | 검증 중 |
| 2026-05-23 | 최근 7일 1D 검증에서 뉴스 촉매+가격 돌파가 강하게 작동했지만 이벤트 집중 표본이라 정책 승격은 보류함 | [[2026-05-18-to-2026-05-22-recent-7d-historical-review]] | 검증 중 |

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
| 1d-event-catalyst-confirmation | 당일 뉴스 촉매와 가격 돌파가 동시에 확인된 후보는 1D 초과수익이 강할 수 있다 | 12 | 100.0% | +5.63%p | 2026-05-21 양자컴퓨팅 이벤트에 성과가 집중되어 추격매수 위험 큼 | 검증 중 | [[2026-05-18-to-2026-05-22-recent-7d-historical-review]] |

## 폐기하거나 완화한 규칙

| 날짜 | 규칙 | 이유 |
| --- | --- | --- |
