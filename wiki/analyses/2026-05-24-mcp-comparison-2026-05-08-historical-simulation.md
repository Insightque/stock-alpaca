---
id: 2026-05-24-mcp-comparison-2026-05-08-historical-simulation
reviewed_simulation: 2026-04-23-to-2026-05-08-historical-decision-batch-v2
sample_asof: 2026-05-08
mode: mcp_comparison_review
paper: true
---

# MCP 보강 비교 검토 - 2026-05-08 과거 추천 표본

## 결론

이전 시뮬레이션의 `2026-05-08` 추천 세트인 `NVDA, IONQ, UNH`는 MCP 보강 후에도 크게 바뀌지 않는다. 다만 추천 이유의 질은 달라졌다. 기존 문서는 가격/뉴스 중심으로 "NVDA AI 촉매, IONQ 추세, UNH 방어적 상대강도"라고 적었지만, MCP 보강 후에는 SEC filing, 실적 surprise, 공식 IR/보도자료, 과열 후보 배제 근거까지 분리할 수 있었다.

가장 큰 차이는 `AMD`다. MCP 보강 전에는 "AMD/TSLA 단기 과열 감점" 정도였지만, MCP 보강 후에는 AMD가 실적 beat와 압도적인 뉴스 흐름에도 불구하고 2026-05-08 기준 직전 5거래일 +26.22%, 직전 1거래일 +11.48%였고 이후 5거래일 -6.83%였다는 점이 뚜렷해졌다. 즉 데이터 부족 때문에 AMD를 놓친 것이 아니라, 결과적으로는 과열 배제가 맞았다.

## 표본 선정

- 선택한 이력: [[2026-04-23-to-2026-05-08-historical-decision-batch-v2]]
- 선택 기준일: `2026-05-08`
- 원래 추천: `NVDA, IONQ, UNH`
- 비교 후보: `AMD, TSLA`
- 새 원천: [[2026-05-24-mcp-comparison-2026-05-08-sources]]

이 표본을 고른 이유는 기존 문서가 추가 데이터 필요성을 전제로 만든 v2 진단용 시뮬레이션이고, 추천 후보 3개가 AI 대형주, 고변동 양자컴퓨팅, 방어적 헬스케어로 성격이 달라 MCP 보강 효과를 비교하기 좋기 때문이다.

## 기존 판단과 MCP 보강 후 차이

| 티커 | 기존 2026-05-08 판단 | MCP 보강 후 확인 | 판단 변화 |
| --- | --- | --- | --- |
| NVDA | AI 촉매, 가격 회복 | 2026-05-08 8-K, Corning/IREN AI infrastructure 뉴스, 공식 NVIDIA-Corning 뉴스 확인 | 추천 근거 강화 |
| IONQ | 추세 회복, 고변동 1자리 | 2026-05-06 실적 surprise +503.9%, 2026-05-07 10-Q, revenue +755% IR, 동시에 profitability/cash burn 리스크 | 추천 유지, 단 소액 사이징 근거 강화 |
| UNH | 방어적 상대강도 | 2026-04-21 실적 surprise +9.5%, 2026-05-05 10-Q, 공식 Q1 revenue 111.7B USD 확인 | 방어주 편입 근거 강화 |
| AMD | 단기 과열로 제외 | 실적 beat와 bullish news는 강했지만 직전 5D +26.22%, 이후 5D -6.83% | 제외 판단 강화 |
| TSLA | 단기 과열/혼재로 제외 | EPS beat는 있었지만 리콜, China sales, 기술적 저항 뉴스가 혼재. 이후 5D -1.41% | 제외 판단 대체로 유지 |

## 성과와 과열 비교

Alpaca MCP 일봉 기준이다.

| 티커 | 05-01→05-08 | 05-08→05-15 | 해석 |
| --- | ---: | ---: | --- |
| NVDA | +8.48% | +4.69% | 촉매가 이어졌고 5D 추천 성과도 양호 |
| IONQ | +6.60% | +5.46% | 실적/10-Q 후 변동성은 컸지만 추천 성과 양호 |
| UNH | +2.99% | +3.62% | 방어적 후보로 SPY 대비 초과 성과 |
| AMD | +26.22% | -6.83% | 호재는 강했지만 신규 진입에는 과열 감점이 필요했음 |
| TSLA | +9.62% | -1.41% | 호재/악재 혼재 후 단기 추격매수 부적합 |
| SPY | +2.37% | +0.21% | 벤치마크 |

추천 3개는 모두 SPY를 5D로 이겼고, 제외한 AMD/TSLA는 5D로 SPY를 밑돌았다. 이 표본만 놓고 보면 추천 세트 자체보다 "왜 추천/제외했는지 설명하는 데이터 품질"이 더 큰 개선점이다.

## MCP별 실제 기여

| MCP | 기존 대비 추가 가치 | 한계 |
| --- | --- | --- |
| Alpaca MCP | 가격, 거래량, 뉴스, corporate action 없음 확인 | 뉴스는 많고 중복이 있어 핵심 이벤트 추출 규칙 필요 |
| SEC EDGAR MCP | NVDA 8-K, IONQ 10-Q, UNH 10-Q, TSLA 10-Q 확인 | 현재 기준 최근 filing 조회이므로 as-of cutoff 필터가 필수 |
| Alpha Vantage MCP | EPS surprise와 NEWS_SENTIMENT로 실적/뉴스 강도를 수치화 | 다중 티커 news query가 0건을 반환해 per-ticker fallback 필요 |
| Firecrawl MCP | 공식 IR/뉴스 URL을 찾아 원문 근거 확보 | 검색 결과만으로는 전문 해석 한계가 있어 필요 시 scrape/parse 단계 추가 필요 |
| Yahoo Finance MCP | 현재 valuation/analyst/news 보조 확인 가능 | 현재 기준 데이터라 strict historical decision에는 누출 위험 |
| FRED MCP | 사용 시 매크로 regime 보강 가능 | 이번 실행에서는 도구 목록 미반환으로 사용 불가 |

## 필요한 전략 보강

1. `post-earnings-overheat-gate`를 명시한다.
   - EPS surprise와 뉴스 sentiment가 강해도, 직전 5거래일 +20% 이상 또는 직전 1거래일 +8% 이상이면 신규 5D 추천 점수를 낮춘다.
   - AMD 2026-05-08 표본이 이 규칙의 대표 예시다.

2. `filing-aware-catalyst-check`를 추가한다.
   - 추천 직전 5거래일 내 10-Q/8-K/425가 있으면 filing을 확인하고, 추천 근거에 "가격 반응 전/후"를 분리한다.
   - IONQ는 2026-05-07 10-Q가 있었고, NVDA는 2026-05-08 8-K가 있었다.

3. `broad-query-fallback`을 둔다.
   - Alpha Vantage `NEWS_SENTIMENT`처럼 다중 티커 조회가 0건을 반환해도 데이터 없음으로 단정하지 않는다.
   - 1차 broad query 실패 시 추천 후보와 제외 후보 상위 5개는 per-ticker로 재조회한다.

4. `strict-asof-timestamp-filter`를 강화한다.
   - filing date만 보지 말고 `acceptance_datetime`을 기준으로 미국 정규장 close 이전/이후를 분리한다.
   - IONQ 2026-05-08 Form 4는 acceptance가 2026-05-09 01:55 UTC라 2026-05-08 정규장 close 추천에는 직접 사용하면 안 된다.

5. `official-ir-corroboration`을 추가한다.
   - 실적 surprise나 뉴스 sentiment가 핵심 근거일 때 Firecrawl로 공식 IR/press release URL을 최소 1개 캡처한다.
   - IONQ Q1 2026, UNH Q1 2026, NVIDIA-Corning partnership에서 유용했다.

## 최종 평가

- 추천 세트 차이: 없음. `NVDA, IONQ, UNH` 유지가 타당했다.
- 신뢰도 차이: 있음. IONQ/UNH는 MCP 보강 후 근거가 크게 강화됐고, AMD 제외는 과열 배제로 더 명확해졌다.
- 데이터 수집 차이: 큼. 기존 원천은 Alpaca 가격/뉴스 중심이었고, 이번 보강은 SEC filing, earnings, official IR까지 붙어 추천 이유와 리스크를 더 잘 분리했다.
- 정책 반영: 단일 표본이므로 living policy에는 즉시 승격하지 않고, 다음 배치 검증에서 위 5개 보강 규칙을 후보로 적용한다.

## 주문 제출 여부

- 이 검토는 과거 추천 비교이며 실제 주문, 취소, 포지션 변경은 없었다.
