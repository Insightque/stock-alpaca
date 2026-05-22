# Workflow: 종목 리서치 전용

사용자가 `관심종목 분석해줘`, `AAPL 분석해줘`라고 말하거나 종목 리서치만 요청할 때 사용한다.

## 목표

요청한 종목을 리서치하고 llm-wiki를 업데이트한다. 주문은 만들거나 제출하지 않는다.

## 필수 산출물

- `wiki/tickers/`의 종목 페이지 업데이트
- `wiki/raw/sources/`의 새 immutable raw source note
- 필요 시 `wiki/analyses/`의 교차 종목 분석
- `wiki/index.md` 업데이트
- `wiki/log.md` append-only 항목 추가

## 절차

1. `AGENTS.md`, `wiki/index.md`, 최근 `wiki/log.md`, `wiki/policies/recommendation-policy.md`를 읽는다.
2. 요청된 티커 목록을 파싱한다. 사용자가 티커를 지정하지 않았다면 Alpaca watchlist를 유니버스로 사용한다.
3. Alpaca MCP asset lookup으로 각 티커가 active/tradable 미국 주식 또는 ETF인지 확인한다.
4. Alpaca MCP stock bars, snapshots, quotes/trades, news로 시장 맥락을 수집한다.
5. `harness/mcp-source-map.md`를 읽고 보강 MCP를 사용한다.
   - `sec-edgar`: 10-K, 10-Q, 8-K, XBRL 재무제표, Form 4, insider activity.
   - `alpha-vantage`: 실적 캘린더와 earnings surprise. 키가 없으면 데이터 공백으로 기록.
   - `fred`: CPI, 금리, 실업률, 장단기 금리차 등 매크로 지표. 키가 없으면 데이터 공백으로 기록.
   - `firecrawl`: 회사 IR, 보도자료, earnings presentation 캡처. 키가 없으면 웹 출처로 대체.
   - `yahoo-finance`: Yahoo 뉴스, analyst recommendation, holders, insider, stock actions 보조 확인.
6. 현재 웹 출처에서 MCP로 부족한 기업 이벤트, 실적, 섹터 맥락, 관련 매크로 요인을 조사한다.
7. 유용한 출처는 immutable raw source note로 캡처한다.
8. 각 종목 페이지를 업데이트한다.
   - 현재 thesis.
   - 일간, 주간, 월간 추세.
   - 촉매와 리스크.
   - 출처 기반 신뢰도.
   - 포지션이 있으면 포트폴리오 관련성.
   - 추천 정책의 과거 회고 교훈이 적용된 부분.
9. 종목 비교가 필요하면 `wiki/analyses/` 아래 페이지를 만들거나 업데이트한다.
10. `wiki/index.md`와 `wiki/log.md`를 업데이트한다.

## 하드 룰

이 워크플로우에서는 주문 계획을 만들지 않고 주문도 제출하지 않는다.
