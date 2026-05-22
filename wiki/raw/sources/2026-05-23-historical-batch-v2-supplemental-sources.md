---
id: 2026-05-23-historical-batch-v2-supplemental-sources
captured_at: 2026-05-23T07:12:00+09:00
source: alpaca-mcp-and-prior-review
paper: true
immutable: true
---

# 과거 추천 배치 v2 보강 원천

## 목적

- 이전 배치 회고([[2026-04-23-to-2026-05-08-historical-review-batch]])에서 어떤 데이터가 부족했는지 분석했다.
- 부족했던 데이터를 어떤 소스로 추가 수집해야 하는지 정리하고, 해당 데이터가 판단에 유리했는지 v2 재시뮬레이션에서 검증했다.
- 이 문서는 보강 원천과 데이터 공백을 기록한다. 추천 결과와 미래 성과는 별도 문서에 둔다.

## 추가 수집해야 할 데이터

| 데이터 | 수집 소스 | 판단에 쓰는 방식 | 이번 배치 반영 |
| --- | --- | --- | --- |
| 기준일 이전 뉴스/이벤트 | Alpaca MCP `get_news`, 필요 시 회사 IR/SEC 원문 | 실적, 파트너십, 규제, 대형 계약, 애널리스트 변경을 점수 보정에 사용 | 일부 반영 |
| 가격/거래량/변동성 | Alpaca MCP `get_stock_bars` daily IEX/SIP | 1D/5D/20D/60D 모멘텀, 거래량 급증, 최대낙폭, 변동성 패널티 계산 | 반영 |
| 섹터 벤치마크 | Alpaca MCP `get_stock_bars`의 SPY, QQQ, SMH | 후보가 시장/기술주/반도체 섹터를 이기는지 확인 | 반영 |
| 후보군 누락 점검 | 당시 위키 raw source, order plan, ticker page, Alpaca watchlist | strict mode에서 당시 기록된 후보만 쓰고, 누락 후보는 별도 공백으로 기록 | PLTR 가격 보강 |
| 실적/매크로 일정 | 회사 IR, SEC, 거래소/경제 캘린더 캡처 | 이벤트 전후 추천은 사이징을 낮추거나 관망 처리 | 미반영, 다음 개선 필요 |
| 유동성/스프레드 | Alpaca snapshot/latest quote | 주문 가능성과 리스크 정책 검증에 사용 | 일부 미반영, 다음 개선 필요 |

## 이번에 실제 보강한 원천

- Alpaca MCP `get_news`
  - 대상: NVDA, AMD, AVGO, LRCX, TSM, NOK, UNH, ETN, RGTI, IONQ, PLTR, TSLA, QBTS.
  - 범위: 2026-04-23부터 2026-05-09까지.
  - 확인된 주요 신호:
    - 2026-05-07~2026-05-08: Nvidia/AI 인프라 관련 긍정 뉴스와 애널리스트 기대가 반복 등장.
    - 2026-05-07~2026-05-08: AMD 관련 AI 인프라 파트너십/시장 관심 신호가 반복 등장.
    - 2026-05-08: TSLA 중국 판매 개선 보도.
    - 2026-05-08: NOK 방산/통신 파트너십 긍정 보도와 과열/실적 약점 신호가 동시에 존재.
    - 2026-05-08: AVGO/OpenAI 관련 대형 계약 기대와 자금 조달 공백 리스크가 동시에 존재.
- Alpaca MCP `get_stock_bars`
  - 대상: NVDA, AMD, AVGO, LRCX, TSM, NOK, UNH, ETN, RGTI, IONQ, PLTR, TSLA, QBTS, SPY, QQQ, SMH.
  - 범위: 2026-04-15부터 2026-05-23까지.
  - timeframe: `1Day`, feed: `iex`, adjustment: `raw`.
  - 지난 배치에서 빠졌던 PLTR daily bar를 별도로 재조회해 후보군 누락 공백을 줄였다.

## 데이터가 판단에 준 개선 방향

- 기존 v1은 품질 후보인 TSM/AVGO/NVDA를 단기 모멘텀 후보와 충분히 분리하지 못했다.
- v2는 다음 규칙을 추가했다.
  - 5D 상대강도가 강해도 직전 1D 급락, 거래량 급증 후 반락, 부정 뉴스가 있으면 감점한다.
  - 품질 우량주는 장기 보유 후보로 남기되 5D 추천에서는 단기 촉매가 없으면 후순위로 둔다.
  - NOK처럼 거래량과 가격 돌파가 동시에 발생한 후보는 단기 이벤트 후보로 승격하되, 과열 신호가 나오면 즉시 감점한다.
  - TSLA/NVDA/AMD처럼 뉴스 촉매와 가격 추세가 함께 확인된 후보는 5D 추천 가중치를 높인다.
  - PLTR은 가격 데이터 공백은 해소됐지만, 해당 기간 5D 상대성과가 약해 v2 추천 승격에는 쓰지 않았다.

## 한계

- v2 규칙은 이전 회고를 본 뒤 만든 진단용 재시뮬레이션이다. 따라서 성과 개선이 곧바로 실전 정책 승격을 의미하지 않는다.
- 뉴스 응답은 일부가 도구 출력에서 잘렸고, 전체 원문 기사 전문을 저장하지 않았다.
- 회사 IR/SEC, 실적 캘린더, quote spread, 정밀 유동성 데이터는 아직 자동 수집하지 못했다.
- 주말 보정 표본은 같은 거래일을 반복하므로 hit rate 계산에서 독립 표본으로 과대해석하면 안 된다.

## 연결 문서

- v1 추천: [[2026-04-23-to-2026-05-08-historical-decision-batch]]
- v1 회고: [[2026-04-23-to-2026-05-08-historical-review-batch]]
- v2 추천: [[2026-04-23-to-2026-05-08-historical-decision-batch-v2]]
- v2 회고: [[2026-04-23-to-2026-05-08-historical-review-batch-v2]]
