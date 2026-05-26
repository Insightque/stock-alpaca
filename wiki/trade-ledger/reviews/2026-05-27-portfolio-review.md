---
id: 2026-05-27-portfolio-review
review_type: interim
reviewed_at: 2026-05-26T21:24:00Z
paper: true
decision_date: 2026-05-22
entry_date: 2026-05-22
exit_date:
---

# 2026-05-22 stock-only 포트폴리오 1D 회고

## 요약 판단

- 결론: 혼합, 그러나 1D 기준으로는 포트폴리오 구성 판단이 대체로 합리적이었다.
- 핵심 이유: 2026-05-22 체결 10개 중 AMD, NOK, LRCX, ETN, AVGO, TSM은 다음 정규 거래일인 2026-05-26 기준 양호했고, 반도체/AI 인프라 thesis는 시장과 SMH 강세에 맞았다. 반면 RGTI, UNH, IONQ, NVDA는 각각 이벤트 반납, 헬스케어 리스크, 양자 섹터 변동성, 대형 AI 기대 선반영 부담이 드러났다.
- 정책 반영 여부: 보류. 단일 1D 회고이며 5D/20D가 남아 있어 `policy-book`은 변경하지 않는다.

## 거래 개요

| 항목 | 값 |
| --- | --- |
| 관련 주문 계획 | [[2026-05-22-stock-only-proposal]] |
| 당시 리포트 | [[2026-05-22]], [[2026-05-22-stock-only-trade-proposal]] |
| 체결 대상 | AMD, AVGO, LRCX, TSM, NOK, UNH, ETN, RGTI, IONQ, NVDA |
| 1D 평가 기준 | 2026-05-26 미국 정규장 종가 및 Alpaca current position |
| 계좌 현재 상태 | portfolio_value 101779.63 USD, cash 42347.59 USD, open orders 0 |
| 포트폴리오 히스토리 | Alpaca `get_portfolio_history` 3회 cancelled, 데이터 공백 |

## 당시 판단 복원

2026-05-22 stock-only 계획은 ETF를 제외하고 NVDA, AMD, AVGO, LRCX, NOK, TSM, ETN, UNH, RGTI, IONQ를 매수 후보로 삼았다. 근거는 AI/반도체/인프라 모멘텀, 일부 헬스케어/전력 인프라 분산, 양자컴퓨팅 이벤트성 촉매였다.

당시 명시된 리스크는 기술/AI 집중, 반도체 cluster 동조화, RGTI/IONQ의 이벤트성 변동성, 일부 IEX quote/spread 품질, 그리고 whole-share 주문에 따른 비중 조절 한계였다. Risk check는 PASS였고, 총 계획 매수 명목은 약 56.1%로 cash reserve를 유지했다.

## 실제 결과

2026-05-22 close 대비 2026-05-26 close benchmark는 SPY +0.64%, QQQ +1.76%, SMH +4.55%였다.

| 티커 | 2026-05-22 체결가 | 현재/평가가 | 실제 P/L | 실제 수익률 | 2026-05-26 close 기준 코멘트 |
| --- | ---: | ---: | ---: | ---: | --- |
| AMD | 462.73 | 504.60 | +586.18 | +9.05% | AI 반도체 thesis가 가장 잘 작동. SPY/QQQ/SMH를 모두 상회. |
| NOK | 15.04 | 16.75 | +684.25 전체 포지션 기준 | +11.34% 전체 포지션 기준 | AI 네트워킹/인프라 재평가가 강하게 지속. |
| LRCX | 307.91 | 322.62 | +294.20 | +4.78% | SMH와 비슷한 방향. 반도체 장비 체인 편입 판단은 타당. |
| ETN | 387.90 | 403.02 | +226.80 | +3.90% | 전력/인프라 분산이 기술주 강세와 같이 작동. |
| AVGO | 410.73 | 422.50 | +176.55 | +2.87% | AI 인프라 thesis는 유효하나 AMD/LRCX보다 약함. |
| TSM | 405.20 | 411.8986 | +100.479 | +1.65% | SPY는 상회, QQQ와 유사. 보조 supply-chain 노출로 무난. |
| NVDA | 215.32/213.72 | 214.51 | -27.56 전체 포지션 기준 | -0.36% 전체 포지션 기준 | 핵심 thesis는 유지되나 1D follow-through는 약했다. |
| IONQ | 63.48 | 62.99 | -22.05 | -0.77% | 양자 섹터 강세가 유지되지 못했고 변동성 리스크가 남았다. |
| UNH | 386.56 | 376.8175 | -146.1375 | -2.52% | 방어주 분산 의도와 달리 healthcare headline/policy risk가 부담. |
| RGTI | 25.569584 | 24.84 | -87.54996 | -2.85% | 이벤트성 양자 촉매 추격 리스크가 바로 나타남. |

## Skipped recommendation review

| 티커 | 당시 판단 | 2026-05-22 close | 2026-05-26 close | 1D 결과 | 회고 |
| --- | --- | ---: | ---: | ---: | --- |
| PLTR | 계약 분쟁/매크로 우려와 당일 약세로 제외 | 136.84 | 136.57 | -0.20% | 제외 판단은 1D 기준 타당. |
| QBTS | RGTI/IONQ와 중복, 낮은 신뢰도라 제외 | 29.34 | 27.82 | -5.18% | 양자 basket 중 고변동 중복 회피가 유효했다. |
| TSLA | SpaceX/합병 기대에 치우친 thesis라 제외 | 425.95 | 433.53 | +1.78% | 제외는 큰 opportunity miss는 아니지만 QQQ와 비슷한 상승은 놓쳤다. |

## 잘한 점

- 10개 주문 모두 long-only, whole-share, day limit 형태였고, 전체 노출은 초기 계좌의 약 56%라 risk policy의 cash reserve를 지켰다.
- AMD/NOK/LRCX/ETN처럼 thesis와 가격 follow-through가 함께 확인된 종목이 포트폴리오 손익을 견인했다.
- RGTI/IONQ는 낮은 신뢰도로 작게 편입했고, QBTS/PLTR/TSLA를 제외해 고변동 중복과 약한 thesis를 제한했다.
- NVDA 주문이 당초 일부 미체결이었다가 장중 체결됐지만 최종 보유 비중은 7%대라 ticker cap 안에 머물렀다.

## 부족했던 점

- 반도체/AI cluster 노출이 여전히 크다. 1D 성과는 좋았지만 SMH가 +4.55%인 날에는 cluster beta가 판단 품질을 실제보다 좋아 보이게 만들 수 있다.
- UNH의 분산 역할은 1D에 작동하지 않았다. 헬스케어 방어주도 Medicare Advantage, 정치/규제, sentiment 리스크를 별도 확인해야 한다.
- RGTI/IONQ의 이벤트성 촉매는 실제로 빠르게 반납됐다. 소액 편입은 적절했지만, event-aftershock risk를 더 강하게 표시할 필요가 있다.
- Alpaca portfolio history가 cancelled되어 계좌 단위 MFE/MAE와 intraday drawdown은 이번 회고에서 완전히 복원하지 못했다.

## 운 또는 당시 알기 어려웠던 점

- 2026-05-26 반도체/AI 관련 뉴스 플로우와 MU/AI memory 중심의 ETF 강세는 2026-05-22 결정 당시 일부만 알 수 있었다.
- RGTI의 2026-05-22 장마감 후 및 2026-05-26 Form 4/Form 144 흐름은 추천 시점 이후 정보이므로 추천 판단에는 사용할 수 없고 회고 참고로만 쓴다.
- NOK의 AI 인프라 재평가가 다음 거래일에 크게 확대된 것은 방향은 thesis와 맞았지만 강도는 사전 확정하기 어려웠다.

## 다음 추천 정책에 줄 교훈

- 1D 성과만으로 정책을 바꾸지 않는다. 이 회고는 `lt-dual-benchmark`, `theme cap`, `event risk`, `low-confidence sizing` 기존 원칙을 재확인하는 표본으로만 둔다.
- 다음 5D/20D 회고에서 AMD/NOK/LRCX의 초과수익이 유지되는지, RGTI/IONQ/UNH 손실이 회복되는지 확인해야 한다.
- 포트폴리오 리뷰에서는 체결 종목뿐 아니라 제외한 고순위 후보도 계속 비교한다. 이번 1D에서는 QBTS/PLTR 제외가 좋았고 TSLA 제외는 중립에 가까웠다.

## 정책 업데이트 제안

- 상태: 보류.
- 제안: 없음. 기존 정책의 `한 거래만으로 과도한 규칙을 만들지 않는다`, `theme cap`, `event risk`, `low-confidence sizing` 원칙을 유지한다.
- 근거: 1D horizon만 완료됐고 5D/20D 결과가 아직 없다. 또한 포트폴리오 히스토리 MCP가 cancelled되어 계좌 단위 drawdown 증거가 부족하다.

## 다음 review due

- 2026-05-22 체결분: 5D/20D 회고 대기.
- 2026-05-26 체결분 LLY/FCX/NOK/NVDA/AAPL: 1D/5D/20D 회고 대기.
- AMZN expired order: 체결 없음. 주문 품질은 lifecycle/risk gate 관찰로만 남기고 trade review 대상은 아니다.

## 연결 문서

- 주문 계획: [[2026-05-22-stock-only-proposal]]
- 당시 리포트: [[2026-05-22]], [[2026-05-22-stock-only-trade-proposal]]
- 원천 자료: [[2026-05-27-0624-analyst-review-cycle-sources]], [[2026-05-22-paper-order-submission]]
- 포트폴리오: [[portfolio-current]]
