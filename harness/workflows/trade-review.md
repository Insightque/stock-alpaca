# Workflow: 거래 회고 및 추천 정책 개선

사용자가 `거래 회고해줘`라고 말하거나, post-trade/rebalance 과정에서 회고가 필요하다고 판단될 때 사용한다.

## 목표

체결된 paper 거래가 좋은 판단이었는지 회고하고, 당시 기록과 실제 결과를 비교해 추천 정책이 조금씩 개선되도록 위키에 남긴다. 이 워크플로우는 절대 주문을 제출하지 않는다.

## 회고 대상

- 청산된 paper 포지션.
- 아직 보유 중이지만 의미 있는 손익, thesis 훼손, 촉매 발생, 리스크 현실화, 또는 보유 기간 경과가 있는 포지션.
- 최근 주문이 체결됐지만 아직 판단하기 이른 경우에는 `회고 대기`로만 표시한다.

## 필수 입력

- Alpaca MCP 계좌, 포지션, 주문, 체결 활동, 포트폴리오 히스토리.
- 당시 생성된 주문 계획 JSON.
- 당시 일일 리포트와 종목 페이지.
- 관련 raw source notes.
- 현재 종목 페이지, 현재 시장 데이터, 현재 뉴스.
- `wiki/policy-book/recommendation-policy.md`.

## 필수 산출물

- `wiki/trade-ledger/reviews/YYYY-MM-DD-SYMBOL-review.md` 또는 `wiki/trade-ledger/reviews/YYYY-MM-DD-portfolio-review.md`
- 관련 `wiki/research-notes/tickers/SYMBOL.md`의 `회고 기록` 섹션 업데이트
- 필요 시 `wiki/policy-book/recommendation-policy.md` 업데이트
- `wiki/index.md` 업데이트
- `wiki/log.md` append-only 항목 추가

## 절차

1. `AGENTS.md`, `wiki/index.md`, `wiki/log.md`, `wiki/policy-book/recommendation-policy.md`를 읽는다.
2. Alpaca MCP로 계좌, 포지션, 최근 주문, 최근 체결 활동, 포트폴리오 히스토리를 확인한다.
3. 회고 대상 거래를 식별한다.
   - 신규 체결 직후라 판단 근거가 부족하면 `회고 대기`로 기록한다.
   - 청산 거래는 최종 회고 대상으로 본다.
   - 보유 중인 거래는 중간 회고 대상으로 본다.
4. 각 거래의 의사결정 당시 기록을 복원한다.
   - 주문 계획의 생성 시각, side, qty, limit/reference price, 의도.
   - 당시 ticker thesis, 점수, 신뢰도, 촉매, 리스크.
   - 당시 daily report의 시장 판단과 후보 순위.
   - 당시 raw source와 Alpaca market data.
5. 실제 결과를 계산한다.
   - 진입가, 현재가 또는 청산가.
   - 실현/미실현 손익과 수익률.
   - 보유 기간.
   - 최대 유리/불리 이동이 확인 가능하면 기록한다.
   - 벤치마크 비교가 가능하면 SPY/QQQ/관련 ETF와 비교한다.
6. 판단 품질을 분해한다.
   - 잘한 점: thesis, 추세, 촉매, 리스크 관리, 사이징, 주문 가격, 회피 판단 중 맞았던 것.
   - 부족한 점: 놓친 리스크, 과신, 늦은 진입/청산, 유동성, 이벤트 해석, macro 무시, 출처 부족.
   - 운/불확실성: 당시 합리적으로 알기 어려웠던 것.
7. 추천 정책 개선안을 제안한다.
   - 한 거래만으로 과도한 규칙을 만들지 않는다.
   - 반복되거나 명확한 교훈만 정책에 반영한다.
   - 정책 변경은 `추가`, `완화`, `강화`, `보류` 중 하나로 표시한다.
8. 회고 파일을 `harness/templates/trade-review.md` 형식으로 작성한다.
9. 관련 ticker page에 `## 회고 기록` 섹션을 추가하거나 갱신한다.
10. `wiki/policy-book/recommendation-policy.md`를 업데이트할 경우 변경 근거와 링크를 남긴다.
11. `wiki/index.md`와 `wiki/log.md`를 업데이트한다.

## 판단 기준

- 수익이 났다고 항상 좋은 판단은 아니다.
- 손실이 났다고 항상 나쁜 판단은 아니다.
- 좋은 판단은 당시 정보로 합리적이고, 리스크가 명시됐으며, 사이징과 주문 형태가 정책에 맞고, 사후 결과가 thesis와 비교 가능하게 기록된 판단이다.
- 나쁜 판단은 출처 부족, 촉매 오해, 리스크 누락, 과도한 확신, 유동성 무시, 정책 위반, 또는 사후 검증 불가능한 판단이다.

## 금지 사항

- 이 워크플로우에서 새 주문을 제출하지 않는다.
- 과거 기록을 지워서 당시 판단을 미화하지 않는다.
- API key 또는 민감 정보를 출력하지 않는다.
- 단일 사례만으로 자동 매수/매도 정책을 크게 바꾸지 않는다.
