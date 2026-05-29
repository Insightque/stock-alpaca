---
id: 2026-05-30-portfolio-review
review_type: interim
reviewed_at: 2026-05-29T21:25:00Z
paper: true
decision_date: 2026-05-28
entry_date: 2026-05-28
exit_date:
---

# 2026-05-28 validation fills 1D 회고

## 요약 판단

- 결론: 혼합. PLTR와 ADBE는 1D 기준으로 매우 강했고, QQQ/BAC/NKE/SPY는 소액 검증 판단이 양호했다. 반면 NOK/WMT/GOOGL/SO/SLB/TSLA/XOM은 SPY/QQQ 대비 약해 분산 또는 방어 라벨만으로는 충분하지 않았다.
- 핵심 이유: 2026-05-29 close/current Alpaca position 기준 SPY는 +0.20%, QQQ는 +0.33% 수준의 완만한 상승이었다. 같은 기간 PLTR +15.72%, ADBE +7.07%는 소프트웨어/AI 재평가 흐름과 맞았지만, 유틸리티/에너지/소비 방어 일부는 벤치마크보다 크게 뒤졌다.
- 정책 반영 여부: 보류. 한 거래일 1D 표본이고, Alpaca portfolio history가 initial + 2 retries 모두 cancelled되어 계좌 단위 MFE/MAE가 불완전하다.

## Reconciliation

| 항목 | 결과 |
| --- | --- |
| Paper mode | `ALPACA_PAPER_TRADE=true` |
| Alpaca clock | 2026-05-29 17:21 ET closed, next open 2026-06-01 09:30 ET |
| Account | ACTIVE |
| Portfolio value | 102,008.32 USD |
| Cash | 34,800.26 USD |
| Buying power | 130,798.68 USD |
| Open US equity orders | 0 |
| Position count | 32 |
| Portfolio history | cancelled after 2 retries, data gap |

## 거래 개요

벤치마크 비교는 Alpaca position의 `lastday_price` 대비 current price로 산출한 SPY +0.20%, QQQ +0.33%를 기준으로 삼았다. 개별 수익률은 각 validation fill price 대비 현재가다.

| 티커 | 진입 일시 UTC | 평균 진입가 | 현재가 | 1D/현 수익률 | SPY 대비 | QQQ 대비 | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| INTC | 2026-05-28 04:19 | 116.79 | 115.91 | -0.75% | -0.95%p | -1.08%p | 약함 |
| NOK | 2026-05-28 04:58 | 15.40 | 14.9686 | -2.80% | -3.00%p | -3.13%p | 약함 |
| PLTR | 2026-05-28 13:37 | 134.94 | 156.15 | +15.72% | +15.52%p | +15.39%p | 강함 |
| QQQ | 2026-05-28 13:38 | 728.36 | 737.99 | +1.32% | +1.13%p | +1.00%p | 양호 |
| CVX | 2026-05-28 13:57 | 184.03 | 182.3155 | -0.93% | -1.13%p | -1.26%p | 약함 |
| NKE | 2026-05-28 13:59 | 46.03 | 46.28 | +0.54% | +0.35%p | +0.22%p | 양호 |
| PFE | 2026-05-28 14:20 | 26.16 | 26.16 | +0.00% | -0.20%p | -0.33%p | 중립 |
| WMT | 2026-05-28 14:30 | 118.63 | 115.79 | -2.39% | -2.59%p | -2.72%p | 약함 |
| GOOGL | 2026-05-28 14:49 | 389.00 | 380.80 | -2.11% | -2.30%p | -2.43%p | 약함 |
| SO | 2026-05-28 14:40 | 93.38 | 91.90 | -1.58% | -1.78%p | -1.91%p | 약함 |
| SLB | 2026-05-28 15:00 | 55.48 | 54.55 | -1.68% | -1.87%p | -2.00%p | 약함 |
| SPY | 2026-05-28 15:18 | 753.38 | 756.09 | +0.36% | +0.16%p | +0.03%p | 양호 |
| BAC | 2026-05-28 15:18 | 51.14 | 51.55 | +0.80% | +0.60%p | +0.48%p | 양호 |
| NEE | 2026-05-28 15:25 | 87.83 | 87.28 | -0.63% | -0.82%p | -0.95%p | 중립 약함 |
| NVDA | 2026-05-28 15:38 | 212.55 | 212.55 | +0.00% | -0.20%p | -0.33%p | 중립 |
| COP | 2026-05-28 15:38 | 114.95 | 114.36 | -0.51% | -0.71%p | -0.84%p | 중립 약함 |
| TSLA | 2026-05-28 15:45 | 441.40 | 435.04 | -1.44% | -1.64%p | -1.77%p | 약함 |
| AMZN | 2026-05-28 15:58 | 270.55 | 270.62 | +0.03% | -0.17%p | -0.30%p | 중립 |
| XOM | 2026-05-28 16:17 | 148.37 | 145.38 | -2.02% | -2.21%p | -2.34%p | 약함 |
| ADBE | 2026-05-29 00:16 | 242.36 | 259.50 | +7.07% | +6.88%p | +6.75%p | 강함 |

## 당시 판단 복원

2026-05-28 정규장/장외 validation fills는 모두 paper, long-only, whole-share, day limit 형태였다. 각 run은 universe strict, MCP strict, risk policy를 통과한 뒤 Alpaca MCP를 통해서만 제출했다. Alpha Vantage는 대체로 `empty_response` gap이었지만 SEC EDGAR, FRED, Firecrawl, Yahoo Finance가 pass로 기록되어 minimum research confirmation은 충족했다.

- INTC/NOK/ADBE는 after-hours validation bucket의 별도 표본이었다. INTC와 NOK는 기존 보유/테마 노출이 있어 1주로 제한했고, ADBE는 software/growth_quality 신규 표본이었다.
- PLTR/QQQ/BAC는 regular-session 첫 validation group이었다. PLTR는 speculative growth지만 1주 floor로 제한했고, QQQ는 broad benchmark 노출, BAC는 financials 분산 후보였다.
- CVX/NKE/PFE/WMT/SO/SLB/SPY/NEE/COP/XOM은 에너지, 소비, 헬스케어, 유틸리티, 벤치마크 분산 표본이었다.
- GOOGL/NVDA/TSLA/AMZN은 mega-cap 또는 AI/growth quality 검증 표본이었지만, 기존 AI/tech 노출 때문에 1주 단위로만 제한됐다.

## 실제 결과

PLTR와 ADBE는 software/AI 관련 뉴스와 시장 선호가 1D 성과로 이어졌다. Alpaca/Yahoo 뉴스는 Dell, Snowflake, AI spending, software confidence 회복을 반복적으로 보여줬고, PLTR는 Dell AI Factory partnership과 defense-tech momentum 관련 뉴스가 동반됐다. ADBE는 Firefly/AI agent 기대와 AI가 기존 stock-photo economics를 잠식할 수 있다는 우려가 같이 있었지만, 이번 1D 가격 결과는 긍정 쪽이 압도했다.

반대로 INTC는 AI/semiconductor headline 수혜가 간접적이었고, SEC/Yahoo 확인에서도 직접 촉매가 약했다. NOK는 기존 보유가 큰 상태에서 추가 1주가 또 약했고, 2026-05-26 add의 1D 부진과 같은 방향이다. WMT/GOOGL/SO/SLB/XOM은 분산 후보였지만 2026-05-29의 risk-on/AI-led 장세에서는 상대성과가 약했다.

## Skipped recommendation review

| 구간 | 스킵/대기 대상 | 당시 이유 | 회고 |
| --- | --- | --- | --- |
| 2026-05-28 23:31 | HOOD | submit/runtime cancelled 후 실제 주문 없음 | PLTR가 같은 speculative/software bucket에서 강했으므로 HOOD missed opportunity 가능성은 있지만 체결 evidence가 없어 trade review 대상은 아니다. 다음 cycle에서 skipped high-ranked 후보로 별도 추적한다. |
| 2026-05-28 23:51 | AAPL/SPY 계획 일부 | AAPL open 이후 stale cleanup, SPY submit/retry/reconcile 불완전 | AAPL은 체결 없음. SPY는 이후 2026-05-29 00:11 run에서 체결되어 이번 표에는 실제 fill만 포함했다. |
| 2026-05-29 00:51 | INTC regular-session plan | runtime cancelled 및 reconciliation 404 | INTC는 after-hours 1주가 이미 존재했고 1D 부진했다. regular-session 미체결은 현재 기준 opportunity miss가 아니다. |
| 2026-05-30 이후 no-submit runs | AAPL/COP/NOK 추가 후보 등 | due validation lifecycle review 우선 | due review를 작성하기 전 추가 매수를 막은 것은 타당했다. |

## 잘한 점

- 모든 실제 주문은 tiny validation size로 제한되어, 약한 후보가 많았음에도 계좌 손상은 작았다.
- PLTR/ADBE처럼 기존 반도체 집중과 다른 software/AI 표본을 추가한 점은 유용했다.
- QQQ/SPY benchmark ETF validation은 개별 종목 성과를 해석할 기준점을 만들었다.
- 이후 hourly runs가 due review를 추가 매수보다 우선한 것은 validation lifecycle 정책과 맞다.

## 부족했던 점

- 같은 날 너무 많은 1주 validation fills가 쌓여 회고 대기열이 커졌다. 1D 판단은 가능하지만 각 종목의 원인 분석은 얕아질 위험이 있다.
- Defensive/diversification 후보라는 라벨은 1D edge를 보장하지 않았다. WMT/SO/NEE/PFE/CVX/XOM은 대체로 AI-led risk-on 시장을 이기지 못했다.
- NOK는 2026-05-26 add와 2026-05-28 after-hours add 모두 1D 부진이다. 기존 보유가 큰 고모멘텀 종목에 대한 추가 validation은 더 엄격한 price confirmation이 필요하다는 가설을 강화한다.
- Portfolio-history MCP가 계속 cancelled되어 계좌 단위 MFE/MAE, cashflow-adjusted P/L, intraday drawdown은 아직 복원하지 못했다.

## 운 또는 당시 알기 어려웠던 점

- 2026-05-29 Dell/Snowflake/AI spending 흐름이 PLTR/ADBE와 QQQ에 얼마나 강하게 반영될지는 2026-05-28 주문 시점에 확정하기 어려웠다.
- 에너지 후보는 Iran/Hormuz headlines와 oil-risk premium 변화에 민감했다. CVX/SLB/XOM의 약세는 단순 회사 thesis보다 macro/news regime 영향이 크다.
- ADBE는 AI가 제품 가치를 높인다는 narrative와 기존 stock-photo economics를 잠식한다는 narrative가 공존했다. 1D 급등만으로 장기 thesis 우위를 확정할 수 없다.

## 다음 추천 정책에 줄 교훈

- `software/AI infrastructure follow-through`는 이번 1D cohort에서 강했지만, PLTR/ADBE 2건만으로 active rule을 만들지는 않는다.
- `defensive diversification` 후보는 시장 regime이 AI-led risk-on일 때 벤치마크를 이기지 못할 수 있다. 5D에서도 반복되면 defensive 후보에는 가격 확인 또는 regime 확인을 강화하는 정책 후보로 올린다.
- `existing-position breakout add penalty` 가설은 NOK 사례가 2회 연속 약해져 강화됐다. 하지만 아직 1D 중심이라 5D/20D 확인 전 active rule로 승격하지 않는다.

## 정책 업데이트 제안

- 상태: 보류.
- 제안: 정책 변경 없음. `software/AI follow-through`, `defensive-diversification-price-confirmation`, `existing-position-breakout-add-penalty`를 검증 중 가설로 유지한다.
- 근거: 단일 1D cohort이고 portfolio-history gap이 남아 있다. 정책 업데이트 threshold인 반복 증거와 계좌 단위 drawdown/효과 확인을 충족하지 못했다.

## 다음 review due

- 2026-05-22 stock-only 포트폴리오: 5D 회고는 2026-06-01 close 이후 due, 20D 대기.
- 2026-05-26 validation fills LLY/FCX/NOK/NVDA/AAPL: 5D/20D 회고 대기.
- 2026-05-27 validation fills NKE/PFE/SO/WMT/NEE/AMZN/BAC/XOM/V: 5D/20D 회고 대기.
- 2026-05-28 validation fills와 2026-05-29 ADBE after-hours fill: 5D/20D 회고 대기.
- 2026-05-29 regular-session fills QQQ/V/GOOGL/WMT/NEE: 다음 trading day close 이후 1D 회고 대기.

## 연결 문서

- 주문 계획: `wiki/trade-ledger/orders/2026-05-28-1311-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1351-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2231-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2251-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2311-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2331-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2351-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0011-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0031-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0051-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0111-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0911-after-hours-autopilot.json`
- 당시 리포트: [[2026-05-28-1311-after-hours-autopilot]], [[2026-05-28-1351-after-hours-autopilot]], [[2026-05-28-2231-hourly-autopilot]], [[2026-05-28-2251-hourly-autopilot]], [[2026-05-28-2311-hourly-autopilot]], [[2026-05-28-2331-hourly-autopilot]], [[2026-05-28-2351-hourly-autopilot]], [[2026-05-29-0011-hourly-autopilot]], [[2026-05-29-0031-hourly-autopilot]], [[2026-05-29-0051-hourly-autopilot]], [[2026-05-29-0111-hourly-autopilot]], [[2026-05-29-0911-after-hours-autopilot]]
- 원천 자료: [[2026-05-30-0625-analyst-review-cycle-sources]]
- Run manifest: `wiki/evidence-store/run-manifests/2026-05-30-0625-analyst-review-cycle.json`
- 포트폴리오: [[portfolio-current]]
