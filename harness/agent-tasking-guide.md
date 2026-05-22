# 에이전트 업무 지시 가이드

이 문서는 사용자가 Codex와 트레이딩 에이전트들에게 업무를 줄 때 쓰는 실전 가이드입니다. 운영 규칙의 원본은 `AGENTS.md`이고, 이 문서는 좋은 지시문을 작성하는 방법에 집중합니다.

파일명, 경로, 티커, 모드명(`research-only`, `dry-run`, `submit paper orders`)처럼 하네스가 해석해야 하는 고유 식별자는 원문 표기를 유지합니다.

## 기본 원칙

- 먼저 원하는 결과물을 말합니다: 리서치, 일일 리포트, 리밸런싱, 주문 실행, 사후 점검 중 무엇인지 명확히 씁니다.
- 종목 범위를 정합니다: 특정 티커, Alpaca watchlist, 섹터/테마, 현재 보유 종목 중 하나를 지정합니다.
- 실행 모드를 정합니다: `research-only`, `dry-run`, `submit paper orders` 중 하나를 명시합니다.
- 시간축을 정합니다: 일별, 주별, 월별 관점 중 무엇이 중요한지 말합니다.
- wiki 저장을 요구합니다: 모든 조사와 판단은 `wiki/`에 남기라고 말합니다.
- 주문 관련 업무는 항상 paper trading임을 적습니다.
- 자동 주문을 허용할 때도 리스크 검증과 시장 개장 여부 확인을 반드시 요구합니다.

## 바로 쓰는 명령

```text
일일 트레이딩 워크플로우를 dry-run 모드로 실행해줘.
분석 대상은 Alpaca watchlist를 기준으로 삼아줘.
Alpaca MCP 데이터와 현재 웹 리서치를 함께 사용해줘.
조사 결과와 판단은 llm-wiki에 생성하거나 업데이트해줘.
주문 계획은 scripts/check-risk-policy.py로 검증해줘.
dry-run 모드이므로 주문은 제출하지 말고, 제출 가능 여부와 사유만 리포트에 남겨줘.
```

```text
AAPL, MSFT, NVDA만 리서치해줘.
주문 계획을 만들거나 주문을 제출하지 마.
각 종목 페이지에 일별, 주별, 월별 트렌드, 촉매, 리스크, 출처 기반 신뢰도를 업데이트해줘.
원천 자료는 wiki/raw/sources/에 raw source note로 저장해줘.
```

```text
paper portfolio를 리밸런싱해줘.
현재 Alpaca 포지션과 계좌 가치를 기준으로 계산해줘.
중립 리스크 정책을 지켜줘: 최대 80% 투자, 최소 20% 현금 보유, 종목당 최대 20%.
JSON 주문 계획을 만들고 검증해줘.
모든 안전 조건을 통과할 때만 Alpaca MCP로 paper 주문을 제출해줘.
```

```text
사후 거래 점검을 실행해줘.
최근 Alpaca paper 주문, 체결, 포지션, 현금, 매수 가능 금액을 대조해줘.
wiki/portfolio/current.md, 영향을 받은 종목 페이지, 오늘 리포트, wiki/log.md를 업데이트해줘.
새 주문은 제출하지 마.
```

```text
트레이딩 wiki를 점검해줘.
오래된 주장, 누락된 source note, 고아 종목 페이지, index 링크 누락, 모순된 판단을 찾아줘.
점검 리포트는 wiki/analyses/에 작성해줘.
주문은 절대 하지 마.
```

## 지시문 템플릿

```text
[업무 유형]
일일 트레이딩 워크플로우 실행 / 특정 종목 리서치 / paper portfolio 리밸런싱 / 사후 거래 점검 / trading wiki 점검

[종목 범위]
Alpaca watchlist 사용 / 다음 티커만 사용: ... / 현재 보유 종목 사용 / 다음 테마 사용: ...

[실행 모드]
research-only / dry-run / submit paper orders

[분석 관점]
일별, 주별, 월별 트렌드를 모두 확인해줘.
특히 실적, 거시 리스크, 변동성, 유동성, 섹터 모멘텀을 주의 깊게 봐줘.

[저장 위치]
llm-wiki를 업데이트해줘: raw source note, 종목 페이지, 포트폴리오 페이지, 일일 리포트, index, log.

[안전 조건]
paper trading만 허용해줘. 미국 주식/ETF만 허용해줘. long-only, whole-share, day limit order만 허용해줘.
주문 제출 전 반드시 scripts/check-risk-policy.py로 주문 계획을 검증해줘.
```

## 에이전트별 업무 지시법

### 코디네이터 에이전트

좋은 지시:

```text
일일 실행을 시작해줘. 먼저 AGENTS.md, wiki/index.md, 최근 wiki/log.md 항목을 읽어줘. Alpaca paper mode, 계좌, 시장 시계, watchlist, 포지션, 미체결 주문을 확인해줘. 나머지 워크플로우를 진행하기 전에 blocker를 요약해줘.
```

언제 쓰나:

- 전체 워크플로우를 시작할 때
- 현재 계좌와 시장 상태를 확인할 때
- 다른 에이전트에게 줄 업무 범위를 정리할 때

### 유니버스 에이전트

좋은 지시:

```text
내 Alpaca watchlist와 현재 보유 종목을 기준으로 후보 종목 universe를 만들어줘. active이고 tradable인 미국 주식/ETF만 남겨줘. crypto, options, 비활성 자산, 거래 불가 자산, short, fractional share가 필요한 종목은 제외해줘.
```

언제 쓰나:

- 분석 대상 종목을 좁힐 때
- watchlist가 바뀐 뒤
- 특정 테마나 보유 종목 중심으로 재분석할 때

### 시장 데이터 에이전트

좋은 지시:

```text
선정된 universe에 대해 Alpaca bars, snapshot, 최신 quote/trade, Alpaca news를 수집해줘. Executor가 quote freshness를 확인할 수 있도록 캡처 시각을 보존해줘. 주문은 넣지 마.
```

언제 쓰나:

- 가격, 거래량, 뉴스 기반 분석 전
- 주문 계획 전 최신 quote를 검증할 때

### 웹 리서치 에이전트

좋은 지시:

```text
이 티커들에 대해 현재 기업 이벤트, 실적, 애널리스트 의견, 섹터 흐름, 거시 맥락을 리서치해줘. 유용한 출처는 모두 wiki/raw/sources/ 아래 immutable raw note로 저장하고, source URL, 캡처 시각, 관련 티커, 핵심 근거를 간결하게 남겨줘.
```

언제 쓰나:

- 최신 이벤트를 반영할 때
- Alpaca 데이터만으로 설명이 부족할 때
- 종목 thesis의 근거를 보강할 때

### 트렌드 에이전트

좋은 지시:

```text
각 후보 종목의 일별, 주별, 월별 트렌드를 계산해줘. 가격 방향, 거래량, 모멘텀, 변동성, drawdown, 상대강도를 사용해줘. 0-100 점수와 신뢰도를 부여하고, 사용한 데이터 출처를 함께 남겨줘.
```

언제 쓰나:

- 종목 순위를 산정할 때
- 매수, 보류, 회피 판단의 기술적 근거를 만들 때

### 종목 thesis 에이전트

좋은 지시:

```text
각 종목에 대해 wiki/tickers/SYMBOL.md를 업데이트해줘. 현재 thesis, 일별/주별/월별 트렌드, 촉매, 리스크, 포트폴리오 맥락, 오래된 주장, 모순된 근거, 신뢰도, source link를 포함해줘.
```

언제 쓰나:

- 개별 종목 페이지를 정리할 때
- 리서치 결과를 장기 지식으로 남길 때

### 포트폴리오/리스크 에이전트

좋은 지시:

```text
중립 리스크 정책을 사용해 target allocation과 order-plan JSON을 만들어줘. 최대 80% 투자, 최소 20% 현금, 종목당 최대 20%, 신규 주문 최대 10개, 미국 주식/ETF만 허용해줘. scripts/check-risk-policy.py를 실행하고, 제외된 주문은 모두 사유와 함께 보고해줘.
```

언제 쓰나:

- 투자 금액을 배분할 때
- 리밸런싱할 때
- 자동 paper 주문 직전에 검증할 때

### 실행 에이전트

좋은 지시:

```text
ALPACA_PAPER_TRADE=true이고, 미국 주식 시장이 열려 있고, quote가 fresh하고, risk checker가 통과했을 때만 paper 주문을 제출해줘. 주문은 Alpaca MCP로만 제출해줘. whole-share day limit order만 사용해줘. 제출 후 바로 post-trade check를 실행해줘.
```

언제 쓰나:

- 실제 paper order를 제출할 때
- 반드시 risk gate 이후에만 사용합니다.

### wiki 큐레이터 에이전트

좋은 지시:

```text
wiki/index.md를 업데이트하고 wiki/log.md에 항목을 추가해줘. 새 raw source, 종목 페이지, 일일 리포트, 분석 페이지, 주문 계획이 모두 찾을 수 있게 링크해줘. 모순된 내용은 숨기지 말고 표시해줘.
```

언제 쓰나:

- 워크플로우 마지막
- wiki 정리
- 출처와 링크 누락 점검

### 사후 거래 점검 에이전트

좋은 지시:

```text
Alpaca MCP로 제출된 paper 주문, 체결, 취소, 미체결 주문, 포지션, 현금, 매수 가능 금액을 확인해줘. wiki/portfolio/current.md와 오늘 일일 리포트를 업데이트해줘. 새 주문은 제출하지 마.
```

언제 쓰나:

- 주문 실행 후
- 장 마감 후 상태 확인
- 리밸런싱 결과 검증

## 좋은 지시문 패턴

좋은 지시:

```text
AAPL, MSFT, NVDA만 리서치해줘. Alpaca MCP 데이터와 현재 웹 출처를 사용해줘. 주문은 넣지 마. 종목 페이지와 raw source note를 업데이트해줘. 일별, 주별, 월별 트렌드를 비교한 뒤 세 종목의 순위, 신뢰도, 핵심 리스크를 정리해줘.
```

왜 좋은가:

- 종목 범위가 명확합니다.
- 데이터 소스가 명확합니다.
- 주문 금지가 명확합니다.
- 저장 위치가 명확합니다.
- 기대 산출물이 명확합니다.

부족한 지시:

```text
좋은 주식 찾아줘.
```

문제:

- universe가 불명확합니다.
- 주문 가능 여부가 불명확합니다.
- 시간축과 리스크 기준이 없습니다.
- wiki 업데이트 여부가 없습니다.

개선:

```text
일일 트레이딩 워크플로우를 실행해줘. 분석 대상은 Alpaca watchlist를 사용해줘. 일별/주별/월별 트렌드와 현재 뉴스를 중심으로 봐줘. 일일 리포트와 주문 계획을 만들어줘. 시장이 열려 있고 risk gate를 통과할 때만 paper 주문을 제출해줘.
```

## 실행 모드 선택

### research-only

분석과 wiki 업데이트만 합니다. 주문 계획도 만들지 않는 것이 기본입니다.

사용 예:

```text
TSLA만 research-only 모드로 리서치해줘. 종목 페이지와 raw source note를 업데이트해줘. 주문 계획을 만들거나 주문을 제출하지 마.
```

### dry-run

주문 계획까지 만들고 검증하지만 주문은 넣지 않습니다.

사용 예:

```text
일일 트레이딩 워크플로우를 dry-run 모드로 실행해줘. 주문 계획을 만들고 검증하되, 주문은 제출하지 마.
```

### submit paper orders

리스크 검증, 시장 개장, fresh quote, paper mode를 모두 통과하면 Alpaca MCP로 paper order를 넣습니다.

사용 예:

```text
paper portfolio를 submit 모드로 리밸런싱해줘. 모든 안전 점검을 통과할 때만 paper 주문을 제출해줘. day limit order만 사용해줘.
```

## 결과물을 확인하는 질문

워크플로우가 끝난 뒤 이렇게 물어보면 좋습니다:

```text
오늘 daily report 경로, 생성된 raw source note 목록, 업데이트된 ticker page, order plan 경로, risk checker 결과, 제출/제외된 주문을 요약해줘.
```

```text
이번 실행에서 신뢰도가 낮은 판단과 추가로 확인해야 할 source gap만 정리해줘.
```

```text
wiki/index.md 기준으로 최근 생성된 페이지들이 모두 링크되어 있는지 확인해줘.
```

## 하지 말아야 할 지시

- live trading으로 전환하라는 지시
- options, crypto, short, fractional share 주문 지시
- `.env`나 API key 값을 출력하라는 지시
- 리스크 검증 없이 주문하라는 지시
- Alpaca REST API를 직접 호출해 주문하라는 지시
- 출처 없이 최신 뉴스나 실적 내용을 단정하라는 지시

## 추천 운영 루틴

1. 장 시작 전 또는 관심 시점에 `일일 트레이딩 워크플로우를 dry-run 모드로 실행해줘`라고 지시합니다.
2. 리포트와 order plan을 확인합니다.
3. 괜찮으면 `paper portfolio를 submit 모드로 리밸런싱해줘`라고 지시합니다.
4. 주문 후 바로 `사후 거래 점검을 실행해줘`라고 지시합니다.
5. 주 1회 `트레이딩 wiki를 점검해줘`라고 지시합니다.

자동 paper 주문 실험을 계속할수록 wiki가 누적 지식 베이스가 됩니다. 에이전트에게 업무를 줄 때는 항상 범위, 모드, 산출물, 안전 조건을 같이 말하는 것이 가장 중요합니다.
