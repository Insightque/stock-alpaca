# 심플 명령 라우터

사용자는 아래처럼 짧게 지시합니다. Codex는 이 파일을 먼저 읽고, 해당되는 상세 워크플로우를 실행합니다.

## 기본값

- 사용자가 `주문`, `매수`, `매도`, `실행`, `submit`을 명시하지 않으면 주문을 제출하지 않습니다.
- 기본 분석 대상은 Alpaca watchlist입니다.
- 기본 데이터 소스는 Alpaca MCP와 현재 웹 리서치입니다.
- 기본 저장 위치는 `wiki/`입니다.
- 주문이 필요한 경우에도 paper trading, 미국 주식/ETF, whole-share, day limit order만 허용합니다.
- 주문 전에는 반드시 `scripts/check-risk-policy.py`를 통과해야 합니다.

## 사용자가 쓰는 명령

| 사용자 명령 | 내부 워크플로우 | 주문 여부 | 결과물 |
| --- | --- | --- | --- |
| `오늘 분석해줘` | `harness/workflows/daily.md` | 없음 | 일일 리포트, 종목 페이지, raw source, 주문 후보 |
| `관심종목 분석해줘` | `harness/workflows/research.md` | 없음 | watchlist 종목 리서치와 wiki 업데이트 |
| `AAPL 분석해줘` | `harness/workflows/research.md` | 없음 | 특정 종목 리서치와 wiki 업데이트 |
| `포트폴리오 점검해줘` | `harness/workflows/post-trade.md` | 없음 | 계좌, 포지션, 주문 상태 업데이트 |
| `리밸런싱 계획 짜줘` | `harness/workflows/rebalance.md` | 없음 | 리밸런싱 제안과 검증된 주문 계획 |
| `paper 주문까지 실행해줘` | `harness/workflows/rebalance.md` 또는 최신 주문 계획 | 조건부 제출 | risk gate 통과 시 Alpaca MCP paper 주문 |
| `거래 후 점검해줘` | `harness/workflows/post-trade.md` | 없음 | 체결, 미체결, 포지션, 현금 대조 |
| `거래 회고해줘` | `harness/workflows/trade-review.md` | 없음 | 거래 판단 회고, 종목별 리뷰, 추천 정책 개선 |
| `위키 정리해줘` | `harness/workflows/wiki-lint.md` | 없음 | wiki lint 리포트와 index/log 정리 |

## 명령 해석 규칙

### `오늘 분석해줘`

Alpaca watchlist를 기준으로 일일 시장 분석을 수행합니다. 종목별 일별/주별/월별 트렌드, 최신 뉴스, 웹 리서치, 후보 순위, 리스크를 정리합니다. 주문 후보는 만들 수 있지만 주문은 제출하지 않습니다.

### `관심종목 분석해줘`

Alpaca watchlist만 리서치합니다. 포트폴리오 배분이나 주문 실행보다 종목별 thesis와 출처 정리에 집중합니다.

### `AAPL 분석해줘`

문장 안의 티커를 추출해 해당 종목만 리서치합니다. 여러 종목이면 모두 비교합니다. 예: `AAPL MSFT NVDA 분석해줘`.

### `포트폴리오 점검해줘`

Alpaca MCP로 계좌, 현금, buying power, 포지션, 미체결 주문을 확인하고 `wiki/portfolio/current.md`를 업데이트합니다. 새 주문은 만들지 않습니다.

### `리밸런싱 계획 짜줘`

현재 포지션과 최신 종목 분석을 바탕으로 target allocation과 order-plan JSON을 만듭니다. `scripts/check-risk-policy.py`로 검증하지만 주문은 제출하지 않습니다.

### `paper 주문까지 실행해줘`

최신 리밸런싱 계획 또는 새 리밸런싱 결과를 사용합니다. paper mode, market open, fresh quote, risk gate를 모두 통과할 때만 Alpaca MCP로 주문을 제출합니다. 제출 직후 `거래 후 점검해줘` 흐름을 실행합니다.

### `거래 후 점검해줘`

최근 주문, 체결, 취소, 미체결 주문, 포지션, 현금, buying power를 대조하고 wiki를 업데이트합니다. 새 주문은 절대 제출하지 않습니다.

### `거래 회고해줘`

실제 체결된 paper 거래와 보유/청산 결과를 과거 분석 기록과 비교합니다. 당시 thesis, 점수, 주문 계획, 시장 맥락, raw source를 근거로 무엇을 잘 판단했고 무엇을 놓쳤는지 기록합니다. 결과는 `wiki/reviews/trades/`에 남기고, 반복적으로 확인된 교훈만 `wiki/policies/recommendation-policy.md`에 반영합니다. 새 주문은 절대 제출하지 않습니다.

### `위키 정리해줘`

오래된 주장, 누락된 출처, orphan page, index 누락, 모순된 판단을 점검합니다. 거래 관련 액션은 하지 않습니다.
