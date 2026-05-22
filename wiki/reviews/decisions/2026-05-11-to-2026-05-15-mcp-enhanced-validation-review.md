---
id: 2026-05-11-to-2026-05-15-mcp-enhanced-validation-review
decision_id: 2026-05-11-to-2026-05-15-mcp-enhanced-validation-decision
reviewed_at: 2026-05-23T08:45:00+09:00
review_horizons: [5D]
paper: true
---

# MCP 보강 검증 회고 - 2026-05-11~2026-05-15

## 요약

- Alpha Vantage MCP의 AMD 실적 이력과 MCP 데이터 공백 정보를 기존 검증셋에 반영했다.
- 5개 기준일, 15개 매수 추천을 평가했다.
- 5D 기준 hit rate는 12/15 = 80.0%다.
- 평균 5D SPY 대비 초과수익은 +3.35%p다.
- 기존 검증셋의 60.0%, +0.73%p보다 개선됐지만, 표본이 작으므로 정책 승격이 아니라 조건부 가설로 둔다.

## 기존 검증 대비

| 항목 | 기존 검증 | MCP 보강 검증 |
| --- | ---: | ---: |
| 기간 | 2026-05-11~2026-05-15 | 2026-05-11~2026-05-15 |
| 추천 수 | 15 | 15 |
| 5D hit rate | 9/15 = 60.0% | 12/15 = 80.0% |
| 평균 5D SPY 대비 초과수익 | +0.73%p | +3.35%p |
| 핵심 차이 | 촉매+상대강도 중심 | 실적 beat 후 과열 감점, 데이터 공백 감점 |

## 날짜별 5D 회고

| 기준일 | 5D 평가일 | 추천 후보 | 5D hit | 5D 성과 요약 |
| --- | --- | --- | ---: | --- |
| 2026-05-11 | 2026-05-18 | NVDA, UNH, NOK | 2/3 | NVDA +1.32%(SPY대비 +1.43%p), UNH +1.71%(+1.82%p), NOK -1.51%(-1.40%p) |
| 2026-05-12 | 2026-05-19 | NVDA, NOK, UNH | 2/3 | NVDA -0.11%(+0.49%p), NOK +3.57%(+4.16%p), UNH -1.77%(-1.17%p) |
| 2026-05-13 | 2026-05-20 | AMD, AVGO, TSM | 3/3 | AMD +0.48%(+0.62%p), AVGO +0.18%(+0.32%p), TSM +0.47%(+0.61%p) |
| 2026-05-14 | 2026-05-21 | AMD, IONQ, NOK | 2/3 | AMD -0.06%(+0.66%p), IONQ +2.40%(+3.12%p), NOK -1.94%(-1.22%p) |
| 2026-05-15 | 2026-05-22 | AMD, IONQ, NOK | 3/3 | AMD +10.30%(+9.41%p), IONQ +22.43%(+21.55%p), NOK +10.79%(+9.90%p) |

## 판단

- Alpha Vantage 실적 데이터는 AMD를 무조건 매수 후보로 강화하기보다, 실적 발표 후 과열 여부를 판단하는 데 더 유용했다.
- 2026-05-11~05-12에 AMD와 IONQ 추격매수를 줄인 것이 성과 개선의 핵심이었다.
- 보강 MCP에서 뉴스가 0건이 나온 경우에는 “긍정 뉴스 없음”이 아니라 “해당 provider에서 추가 확인 실패”로 다루는 것이 맞다.
- SEC filings와 FRED macro가 비어 있으면 정책 신뢰도를 높이지 않는다.

## 정책 수립

- `earnings-beat-overextension-filter`: 실적 beat가 확인돼도 발표 후 3~5거래일 누적 상승률이 과도하면 신규 매수 점수를 낮춘다.
- `mcp-confirmation-gap-penalty`: 보강 MCP가 뉴스/filing/macro를 확인하지 못하면 긍정 신호를 추가하지 않고 데이터 공백으로 남긴다.
- `post-catalyst-reentry`: 강한 촉매 뒤 첫 급등은 추격하지 않고, 1~3거래일 조정 또는 벤치마크 대비 상대강도 유지가 확인될 때 재진입한다.
- 현재 상태는 모두 `검증 중`이다. 같은 규칙이 최소 3개 독립 구간에서 반복되기 전에는 현재 원칙으로 승격하지 않는다.

## 다음 과제

- `SEC_EDGAR_USER_AGENT`를 `.env`에 추가해 SEC filings MCP를 활성화한다.
- Alpha Vantage rate limit을 고려해 MCP 결과 캐시 raw source를 남긴다.
- FRED MCP 래퍼를 점검하거나 Alpha Vantage macro endpoints로 대체한다.
- 동일 규칙을 2026-04-23~2026-05-08 학습 구간이 아닌 다른 독립 기간에 walk-forward 검증한다.

## 연결 문서

- 보강 추천: [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-decision]]
- 원천 자료: [[2026-05-23-mcp-enhanced-validation-sources]]
- 기존 검증: [[2026-05-11-to-2026-05-15-historical-validation-review]]
