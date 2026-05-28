---
id: 2026-05-28-portfolio-review
review_type: interim
reviewed_at: 2026-05-27T21:22:00Z
paper: true
decision_date: 2026-05-26
entry_date: 2026-05-26
exit_date:
---

# 2026-05-26 validation fills 1D 회고

## 요약 판단

- 결론: 혼합. LLY와 AAPL은 1D 기준 소액 validation buy 판단이 합리적이었고, FCX와 NVDA는 손실이 작아 검증 주문으로는 허용 가능한 품질이었다. NOK 추가 1주는 breakout 직후 추격 리스크가 바로 드러나 판단 품질이 약했다.
- 핵심 이유: SPY가 거의 보합(+0.02%)이고 QQQ가 소폭 하락(-0.09%)한 1D 환경에서 LLY/AAPL은 벤치마크를 앞섰다. 반면 NOK는 2026-05-26 52-week-high/AI networking 촉매 직후 추가 진입이었고 다음 정규장에서 -4.97%로 되돌림이 컸다.
- 정책 반영 여부: 보류. 1D 표본 5개뿐이고, 5D/20D 결과와 portfolio-history 기반 drawdown 증거가 아직 없다.

## 거래 개요

| 티커 | 진입 일시 UTC | 수량 | 평균 진입가 | 2026-05-27 close | 1D 수익률 | SPY 대비 | QQQ 대비 | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LLY | 2026-05-26 16:02:35 | 1 | 1079.38 | 1084.23 | +0.45% | +0.43%p | +0.54%p | 양호 |
| FCX | 2026-05-26 16:41:44 | 1 | 63.94 | 63.625 | -0.49% | -0.51%p | -0.41%p | 보류 |
| NOK | 2026-05-26 17:21:49 | 1 | 16.50 | 15.68 | -4.97% | -4.99%p | -4.88%p | 약함 |
| NVDA | 2026-05-26 17:34:00 | 1 | 213.72 | 212.575 | -0.54% | -0.55%p | -0.45%p | 보류 |
| AAPL | 2026-05-26 18:43:10 | 1 | 309.45 | 310.93 | +0.48% | +0.46%p | +0.56%p | 양호 |

## 당시 판단 복원

- LLY: GLP-1/대사질환과 infectious disease/vaccine pipeline M&A 촉매, SEC/Yahoo/FRED 확인, 기존 LLY 미보유, 1주 validation size.
- FCX: materials/mining 분산, copper/mining 맥락, SEC/Yahoo/FRED 확인, commodity-cyclical 리스크 때문에 1주 제한.
- NOK: AI networking catalyst, 52-week high, SEC/Alpha/FRED 확인. 이미 400주 보유였고 ADR/high-volatility/source confidence medium이라 1주 validation floor만 허용했다.
- NVDA: SEC 10-Q/8-K, Yahoo/FRED 확인, AI semiconductor quality thesis. 기존 35주 보유와 AI semiconductor cluster 집중 때문에 1주만 추가했다.
- AAPL: mega-cap quality/agentic AI optionality, SEC/Yahoo/FRED 확인, AI semiconductor가 아닌 mega-cap tech 분산 목적으로 1주 validation buy.

## 실제 결과

| 티커 | 1D high | 1D low | 대략 MFE | 대략 MAE | 회고 |
| --- | ---: | ---: | ---: | ---: | --- |
| LLY | 1092.81 | 1071.44 | +1.24% | -0.74% | 촉매와 방어적 healthcare growth thesis가 1D에는 작동했다. |
| FCX | 64.38 | 62.88 | +0.69% | -1.66% | 손실은 작지만 commodity-cyclical 분산 진입은 즉시 우위가 확인되지 않았다. |
| NOK | 16.04 | 15.545 | -2.79% | -5.79% | 전일 breakout/52-week-high 추격 위험이 가장 크게 현실화됐다. |
| NVDA | 214.15 | 208.79 | +0.20% | -2.31% | AI thesis는 유지되나 1D follow-through는 약했고 장중 불리 이동이 있었다. |
| AAPL | 313.22 | 308.38 | +1.22% | -0.35% | cluster 분산 목적과 agentic AI quality thesis가 1D에는 양호했다. |

## Skipped recommendation review

| 구간 | 스킵/대기 대상 | 당시 이유 | 회고 |
| --- | --- | --- | --- |
| 2026-05-26 validation runs | SMH, MU, INTC, AMZN 등 | cluster concentration, spread fail, confidence/risk 우선순위 | 신규 주문 대신 LLY/FCX/NOK/NVDA/AAPL 1주 검증에 머문 것은 전체 위험 관리 측면에서 타당했다. |
| 2026-05-27 later runs | GOOGL, SLB, COP, PLTR, QQQ, SPY 등 | same-session validation history와 `risk_daily_new_orders_budget` | 정정: 당시 회고의 10개 validation budget 판단은 legacy 문서 중복에서 온 오판이었다. Active policy 기준은 `harness/risk-policy.yaml`과 `harness/recommendation-policy.yaml`을 따라야 하며, 해당 run들의 no-submit 판단은 별도 재평가 대상이다. |
| 2026-05-27 GOOGL | fresh open order 후 stale cleanup cancel | 미체결 stale order lifecycle | filled_qty 0이라 trade review 대상은 아니며, order lifecycle 관찰로만 남긴다. |

## 잘한 점

- 모든 체결은 paper, whole-share, long-only, day limit validation size로 제한됐다.
- LLY/AAPL처럼 기존 cluster 밖 또는 낮은 추가 위험의 후보는 1D에서 벤치마크를 앞섰다.
- FCX/NVDA는 손실이 났지만 1주로 제한되어 thesis 검증 비용이 작았다.
- 정정: 2026-05-27 후속 run의 daily validation order budget 차단 판단은 legacy 10건 기준에 오염됐다. 같은 세션 주문 누적 위험 자체는 관리해야 하지만, 차단 기준은 active YAML 정책으로만 판단해야 한다.

## 부족했던 점

- NOK는 이미 400주 보유한 상태에서 52-week high 직후 1주를 추가했다. 크기는 작았지만, "기존 보유 + 급등 직후 + source confidence medium" 조합은 신규 evidence 수집보다 되돌림 위험이 컸다.
- NVDA는 1주 추가 자체는 작았으나 AI semiconductor cluster가 이미 큰 상황에서 1D follow-through 근거가 약했다.
- Alpaca portfolio history가 계속 cancelled되어 계좌 단위 intraday drawdown, portfolio-level MFE/MAE, cashflow-adjusted P/L은 복원하지 못했다.

## 다음 추천 정책에 줄 교훈

- 1주 validation이라도 기존 보유가 큰 종목을 52-week high 직후 추가할 때는 `same-symbol existing exposure + breakout chase`를 별도 감점으로 기록하는 편이 낫다.
- Cluster 분산 목적의 소액 검증은 1D 손익보다 리스크 budget을 얼마나 아꼈는지가 더 중요하다.
- 과매매 방지 장치는 필요하지만, daily validation order budget의 실제 기준은 active YAML 정책으로만 판단해야 한다. 2026-05-27 후속 run들은 legacy 10건 기준 오염 때문에 별도 재평가가 필요하다.

## 정책 업데이트 제안

- 상태: 보류.
- 제안: `existing_position_breakout_add_penalty` 가설을 검증 중 항목으로만 유지한다.
- 근거: NOK 1건의 1D 부진만으로 active rule을 만들기에는 증거가 부족하다. 5D/20D와 다른 existing-position add 사례가 필요하다.

## 다음 review due

- 2026-05-26 validation fills LLY/FCX/NOK/NVDA/AAPL: 5D/20D 회고 대기.
- 2026-05-27 validation fills NKE/PFE/SO/WMT/NEE/AMZN/BAC/XOM/V: 1D/5D/20D 회고 대기.
- 2026-05-22 stock-only 포트폴리오: 5D/20D 회고 대기.
- Portfolio-history MCP gap이 해소되면 계좌 단위 drawdown과 open-position MFE/MAE를 보강한다.

## 연결 문서

- 주문 계획: `wiki/trade-ledger/orders/2026-05-27-0052-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-27-0131-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-27-0211-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-27-0226-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-27-0251-hourly-autopilot.json`
- 당시 리포트: [[2026-05-27-0052-hourly-autopilot]], [[2026-05-27-0131-hourly-autopilot]], [[2026-05-27-0211-hourly-autopilot]], [[2026-05-27-0226-hourly-autopilot]], [[2026-05-27-0251-hourly-autopilot]]
- 원천 자료: [[2026-05-28-0622-analyst-review-cycle-sources]]
