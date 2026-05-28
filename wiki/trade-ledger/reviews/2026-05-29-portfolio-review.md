---
id: 2026-05-29-portfolio-review
review_type: interim
reviewed_at: 2026-05-28T21:25:00Z
paper: true
decision_date: 2026-05-27
entry_date: 2026-05-27
exit_date:
---

# 2026-05-27 validation fills 1D 회고

## 요약 판단

- 결론: 혼합. AMZN/NKE는 1D 기준으로 벤치마크 대비 양호했고, WMT/NEE/XOM은 검증 주문으로는 중립에 가깝다. BAC/V/SO/PFE는 1D follow-through가 약해 방어/분산 thesis가 즉시 작동하지 않았다.
- 핵심 이유: 2026-05-28 정규장 close 기준 SPY는 전일 대비 +0.54%, QQQ는 +0.84%였다. 같은 구간에서 AMZN +1.45%, NKE +2.62%만 두 벤치마크를 명확히 앞섰고, BAC -2.38%, SO -1.88%, V -1.54%는 상대적으로 부진했다.
- 정책 반영 여부: 보류. 1D 표본이고 Alpaca portfolio history가 3회 cancelled되어 계좌 단위 drawdown/MFE/MAE가 불완전하다.

## 거래 개요

| 티커 | 진입 일시 UTC | 수량 | 평균 진입가 | 2026-05-28 close | 1D 수익률 | SPY 대비 | QQQ 대비 | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| NKE | 2026-05-27 13:55:58 | 1 | 46.15 | 47.36 | +2.62% | +2.08%p | +1.78%p | 양호 |
| PFE | 2026-05-27 13:57:28 | 1 | 26.34 | 26.15 | -0.72% | -1.27%p | -1.56%p | 약함 |
| SO | 2026-05-27 13:57:42 | 1 | 94.28 | 92.505 | -1.88% | -2.43%p | -2.73%p | 약함 |
| WMT | 2026-05-27 14:17:41 | 1 | 118.31 | 118.895 | +0.49% | -0.05%p | -0.35%p | 중립 |
| NEE | 2026-05-27 14:19:56 | 1 | 87.34 | 87.26 | -0.09% | -0.64%p | -0.94%p | 중립 |
| AMZN | 2026-05-27 14:38:30 | 1 | 270.05 | 273.98 | +1.45% | +0.91%p | +0.61%p | 양호 |
| BAC | 2026-05-27 14:38:42 | 1 | 52.06 | 50.82 | -2.38% | -2.93%p | -3.23%p | 약함 |
| XOM | 2026-05-27 14:38:53 | 1 | 147.07 | 146.99 | -0.05% | -0.60%p | -0.90%p | 중립 |
| V | 2026-05-27 15:11:26 | 1 | 330.01 | 324.93 | -1.54% | -2.08%p | -2.38%p | 약함 |

## 당시 판단 복원

2026-05-27 후반 validation fills는 tiny 1-share paper order로, daily/hourly autopilot의 MCP, universe, quote/spread, risk gate가 통과한 뒤 제출됐다. 주문들은 신규 장기 포지션을 크게 늘리기보다 여러 업종의 후보를 소액으로 검증하는 목적이었다.

- NKE/WMT/PFE/SO/NEE/V는 defensive consumer, healthcare, utility, payments 분산 후보였다.
- AMZN은 mega-cap AI/cloud quality 후보였고, 이후 Alpaca/Yahoo news에서 AWS와 AI data infrastructure 관련 긍정 흐름이 확인됐다.
- BAC/XOM은 financials/energy 분산 및 macro/commodity hedge 후보였다.
- BAC, SO, V의 1D 부진은 "분산 후보가 약한 시장에서는 방어가 된다"는 단순 가정을 바로 지지하지 않았다.

## 실제 결과

| 티커 | 1D high | 1D low | 대략 MFE | 대략 MAE | 회고 |
| --- | ---: | ---: | ---: | ---: | --- |
| NKE | 47.64 | 45.58 | +3.23% | -1.24% | 소매/소비재 validation 중 가장 좋았다. Yahoo consensus는 hold 비중이 높아 conviction은 중립으로 유지한다. |
| PFE | 26.28 | 26.02 | -0.23% | -1.21% | 손실은 작지만 방어적 healthcare thesis가 1D에는 작동하지 않았다. |
| SO | 94.205 | 92.415 | -0.08% | -1.98% | utility 방어 분산 후보였지만 1D 상대성과가 약했다. |
| WMT | 119.12 | 117.365 | +0.68% | -0.80% | 안정적이지만 SPY/QQQ 초과 근거는 부족하다. Costco earnings preview 뉴스는 비교 소매 맥락으로만 사용한다. |
| NEE | 88.45 | 87.035 | +1.27% | -0.35% | 장중 MFE는 있었지만 종가 기준 우위는 없다. |
| AMZN | 274.36 | 267.465 | +1.60% | -0.96% | AWS/AI 데이터 인프라 뉴스 흐름과 가격 follow-through가 맞았다. |
| BAC | 51.495 | 50.64 | -1.09% | -2.73% | financials 분산 후보였지만 1D 약세. SEC 424B2 다수는 구조화채 발행 맥락이며 단기 매수 촉매로 보기 어렵다. |
| XOM | 150.17 | 146.885 | +2.11% | -0.13% | 장중에는 우호적이었지만 종가 추세는 중립. Iran ceasefire/nuclear-talk news가 에너지 리스크 프리미엄을 낮춘 점은 회고 참고 사항이다. |
| V | 326.71 | 320.93 | -1.00% | -2.75% | payments quality thesis가 단기에는 약했고, Alpaca news의 의회 매도/crypto card volume 이슈는 혼재 신호였다. |

## Skipped recommendation review

| 구간 | 스킵/대기 대상 | 당시 이유 | 회고 |
| --- | --- | --- | --- |
| 2026-05-29 01:31 이후 정규장 empty plans | NVDA, QQQ, AAPL, NEE, WMT, SLB, BAC, XOM 등 | same ET-session `risk_daily_new_orders_budget` 20/20 | 제출 없음. 후보들은 `recheck_only`였고 1D 결과가 아직 완성되지 않아 opportunity review는 다음 cycle로 미룬다. |
| 2026-05-29 06:11 after-hours | QQQ, NOK, SPY, SMH/NVDA/ADBE/LIN/XOM | after-hours quote freshness 실패 | 제출 없음. fresh quote gate가 차단했으므로 skip 판단은 현재까지 정책 위반이 아니다. |
| 2026-05-28 신규 fills | INTC, NOK, PLTR, QQQ, CVX, NKE, PFE, WMT, GOOGL, SO, SLB, SPY, BAC, NEE, NVDA, COP, TSLA, AMZN, XOM | 신규 또는 same-day fill | 회고 대기. 1D horizon은 2026-05-29 정규장 이후 평가한다. |

## 잘한 점

- 모든 2026-05-27 reviewed fills는 paper, long-only, whole-share, day limit validation size였다.
- AMZN/NKE처럼 서로 다른 thesis의 소액 검증이 1D 초과수익으로 이어진 사례가 있다.
- BAC/SO/V 손실은 validation size라 계좌 손상은 작았고, 분산 후보의 실제 follow-through를 측정할 수 있었다.
- 2026-05-29 no-submit runs는 주문 cap/fresh quote gate를 강제로 우회하지 않았다.

## 부족했던 점

- Defensive/quality 분산 후보라는 라벨만으로는 1D edge가 충분하지 않았다. BAC/SO/V는 SPY/QQQ 대비 의미 있게 부진했다.
- Energy/financials 후보는 macro headline에 민감했다. XOM은 장중 MFE가 있었지만 종가 기준 neutral이고, BAC는 금리/credit/risk-on 흐름과 따로 확인해야 한다.
- 신규 fills가 너무 많이 쌓여 1D/5D/20D 회고 대기열이 빠르게 늘었다. 검증 주문 수가 많아지면 회고 품질이 얕아질 수 있다.
- Alpaca portfolio history가 cancelled되어 계좌 단위 MFE/MAE와 cashflow-adjusted P/L은 이번 회고에서 완전히 복원하지 못했다.

## 운 또는 당시 알기 어려웠던 점

- 2026-05-28 AI software와 AWS/Snowflake 뉴스가 AMZN/PLTR/QQQ 쪽으로 리스크 선호를 강화한 강도는 2026-05-27 진입 시점에 확정하기 어려웠다.
- US-Iran ceasefire 및 nuclear-talk 관련 헤드라인은 XOM/CVX 같은 에너지 후보의 단기 리스크 프리미엄을 흔들 수 있었고, 당시 주문 직후의 결과로만 판단하기 어렵다.
- BAC의 다수 424B2 filing은 매수 thesis의 직접 촉매라기보다 대형은행 발행 활동으로, 단기 가격 방향을 설명하는 근거로 약하다.

## 다음 추천 정책에 줄 교훈

- 한 거래만으로 정책을 바꾸지 않는다. 다만 `defensive diversification` 후보도 SPY/QQQ 대비 단기 follow-through를 별도로 검증해야 한다는 가설을 남긴다.
- Validation order 수가 많아질수록 review backlog가 늘어난다. 주문 cap은 손실 통제뿐 아니라 회고 가능성을 보존하는 운영 장치로도 유효하다.
- BAC/SO/V 같은 약한 1D 사례가 5D에서도 반복되면 defensive/quality 라벨에 대한 price-confirmation 요건을 강화할 수 있다.

## 정책 업데이트 제안

- 상태: 보류.
- 제안: `defensive-diversification-price-confirmation` 가설을 관찰한다.
- 근거: 1D 표본 9개이고, portfolio-history MCP gap이 있어 정책학습 지표 업데이트 threshold를 충족하지 못했다.

## 다음 review due

- 2026-05-22 stock-only 포트폴리오: 5D/20D 회고 대기.
- 2026-05-26 validation fills LLY/FCX/NOK/NVDA/AAPL: 5D/20D 회고 대기.
- 2026-05-27 validation fills NKE/PFE/SO/WMT/NEE/AMZN/BAC/XOM/V: 5D/20D 회고 대기.
- 2026-05-28 fills: 1D/5D/20D 회고 대기.

## 연결 문서

- 주문 계획: `wiki/trade-ledger/orders/2026-05-27-2246-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-27-2311-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-27-2331-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-27-2351-hourly-autopilot.json`
- 당시 리포트: [[2026-05-27-2246-hourly-autopilot]], [[2026-05-27-2311-hourly-autopilot]], [[2026-05-27-2331-hourly-autopilot]], [[2026-05-27-2351-hourly-autopilot]]
- 원천 자료: [[2026-05-29-0625-analyst-review-cycle-sources]]
- 포트폴리오: [[portfolio-current]]
