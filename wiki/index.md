# 트레이딩 위키 인덱스

이 파일은 Alpaca paper-trading llm-wiki의 탐색 인덱스다. 모든 워크플로우에서 먼저 읽고, 페이지가 새로 만들어지거나 의미 있게 변경될 때마다 업데이트한다.

## 핵심 페이지

- [[portfolio-current]] - 현재 paper 계좌, 포지션, buying power, 미체결 주문. 2026-05-23 KST 체결현황 재조회 후 갱신.
- [[log]] - append-only 형식의 시간순 활동 로그.

## 종목

- [[NVDA]] - AI 반도체 핵심 주식 후보, 2026-05-22 업데이트.
- [[AMD]] - AI 반도체 보조 핵심 후보, 2026-05-22 업데이트.
- [[AVGO]] - AI 반도체 인프라 후보, 2026-05-22 업데이트.
- [[LRCX]] - 반도체 장비 후보, 2026-05-22 업데이트.
- [[TSM]] - 글로벌 반도체 제조 후보, 2026-05-22 업데이트.
- [[NOK]] - AI 인프라/네트워크 보조 후보, 2026-05-22 업데이트.
- [[UNH]] - 헬스케어 방어적 분산 후보, 2026-05-22 업데이트.
- [[ETN]] - 전력/인프라 분산 후보, 2026-05-22 업데이트.
- [[IONQ]] - 양자컴퓨팅 소액 분산 후보, 2026-05-22 업데이트.
- [[QBTS]] - 양자컴퓨팅 watchlist 후보, 2026-05-22 업데이트.
- [[PLTR]] - AI 소프트웨어 watchlist 후보, 이번 주문 제외, 2026-05-22 업데이트.
- [[TSLA]] - EV/AI 이벤트성 watchlist 후보, 이번 주문 제외, 2026-05-22 업데이트.
- [[SPY]] - 광범위 시장 ETF 벤치마크, 2026-05-22 업데이트.
- [[QQQ]] - 성장/기술주 ETF 벤치마크, 2026-05-22 업데이트.
- [[SMH]] - 반도체 ETF 후보, 2026-05-22 업데이트.
- [[RGTI]] - 투기적 양자컴퓨팅 촉매 종목, 2026-05-22 업데이트.
- [[SOXS]] - 레버리지 인버스 반도체 ETF, 핵심 롱 후보로 회피, 2026-05-22 업데이트.
- [[FUTU]] - 갭다운 ADR 브로커 관찰 종목, 2026-05-22 업데이트.
- [[TIGR]] - 갭다운 ADR 브로커 관찰 종목, 2026-05-22 업데이트.
- [[LFS]] - 투기적 고모멘텀 mover, 2026-05-22 업데이트.
- [[QTEX]] - 투기적 1달러 미만 mover, 2026-05-22 업데이트.
- [[BIYA]] - 투기적 저가 mover, 2026-05-22 업데이트.

## 일일 리포트

- [[2026-05-22]] - 현재 시장 분석과 이후 주식 중심 paper 매수 실행 업데이트.

## 분석

- [[2026-05-22-stock-only-trade-proposal]] - ETF 제외, 주식 중심 금일 거래 제안과 paper 주문 실행 결과.

## 과거 시점 시뮬레이션

- `wiki/simulations/` - 과거 특정 시점 기준 추천 시뮬레이션 저장소. 추천 문서는 미래 가격 정보를 포함하지 않는다.
- [[2026-04-23-to-2026-05-08-historical-decision-batch]] - 2026-04-23부터 2026-05-08까지 1일 단위 과거 추천 시뮬레이션 배치.
- [[2026-04-23-to-2026-05-08-historical-decision-batch-v2]] - 추가 데이터 필요성을 반영한 2026-04-23~2026-05-08 진단용 재시뮬레이션.
- [[2026-05-11-to-2026-05-15-historical-validation-decision]] - v2 규칙을 학습에 쓰지 않은 날짜에 적용한 out-of-sample 검증 추천.
- [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-decision]] - Alpha Vantage 실적 데이터와 MCP 공백 감점을 반영한 보강 검증 추천.
- [[2026-05-18-to-2026-05-22-recent-7d-historical-decision]] - 최근 7일 이내 과거 추천 시뮬레이션. 2026-05-22 추천은 회고 대기.

## 거래 회고

2026-05-22 paper 주문 체결분은 다음 회고 대상이다. 회고는 `wiki/reviews/trades/`에 저장한다.

## 과거 추천 회고

- `wiki/reviews/decisions/` - 과거 추천 시뮬레이션을 1D/5D/20D 이후 실제 가격으로 평가하는 회고 저장소.
- [[2026-04-23-to-2026-05-08-historical-review-batch]] - 2026-04-23부터 2026-05-08까지 추천 배치의 1D/5D/20D 회고.
- [[2026-04-23-to-2026-05-08-historical-review-batch-v2]] - 보강 데이터와 v2 규칙 적용 후 5D 성과 재회고. 과최적화 위험 포함.
- [[2026-05-11-to-2026-05-15-historical-validation-review]] - v2 규칙의 별도 검증셋 회고. 5D hit rate 60.0%, 평균 초과수익 +0.73%p.
- [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-review]] - MCP 보강 검증 회고. 5D hit rate 80.0%, 평균 초과수익 +3.35%p.
- [[2026-05-18-to-2026-05-22-recent-7d-historical-review]] - 최근 7일 1D 회고. 검증 가능 추천 12/12 hit, 평균 SPY 대비 +5.63%p. 이벤트 집중으로 정책 승격 보류.

## 추천 정책

- [[recommendation-policy]] - 거래 회고에서 나온 교훈을 반영하는 living policy.

## 원천 자료

- [[2026-05-22-alpaca-account-clock]] - 계좌, 시장 시계, 포지션, 주문, watchlist.
- [[2026-05-22-alpaca-market-data]] - most-active, movers, 스냅샷, 봉 데이터, asset 확인.
- [[2026-05-22-alpaca-news]] - Alpaca/Benzinga 뉴스 스냅샷.
- [[2026-05-22-web-market-context]] - 매크로/뉴스 내러티브용 웹 맥락 캡처.
- [[2026-05-22-stock-only-alpaca-snapshot]] - ETF 제외 주식 중심 후보군 스냅샷과 뉴스/자산 확인.
- [[2026-05-22-expanded-stock-review-alpaca]] - 추가 요청 종목 LRCX, TSM, UNH, ETN, AVGO, PLTR, TSLA 포함 확장 검토.
- [[2026-05-22-paper-order-submission]] - 2026-05-22 주식 중심 paper 주문 제출과 사후 상태.
- [[2026-05-23-alpaca-fill-status]] - 2026-05-23 KST 오늘 주식 체결현황 Alpaca MCP 재조회.
- [[2026-05-23-next-session-research]] - 2026-05-26 다음 미국 정규 거래일 후보 분석용 휴장일, 가격, 뉴스 원천 캡처.
- [[2026-05-23-historical-batch-2026-04-23-to-2026-05-08-alpaca]] - 2026-04-23~2026-05-08 과거 추천 배치용 Alpaca MCP 가격 원천과 데이터 공백 기록.
- [[2026-05-23-historical-batch-v2-supplemental-sources]] - 이전 회고 기반 추가 수집 데이터, 소스, v2 반영 범위와 한계.
- [[2026-05-23-historical-validation-2026-05-11-to-2026-05-15-sources]] - v2 과적합 점검을 위한 별도 검증셋 Alpaca MCP 가격/뉴스 원천.
- [[2026-05-23-mcp-enhanced-validation-sources]] - Alpha Vantage/Alpaca MCP 기반 실적·뉴스·데이터 공백 보강 원천.
- [[2026-05-23-recent-7d-historical-validation-sources]] - 최근 7일 과거 추천 검증용 Alpaca MCP 가격/뉴스 원천.
