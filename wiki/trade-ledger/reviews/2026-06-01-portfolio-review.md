---
id: 2026-06-01-portfolio-review
review_type: waiting
reviewed_at: 2026-05-31T21:23:00Z
paper: true
decision_date: 2026-05-29
entry_date: 2026-05-29
---

# 2026-06-01 analyst review 대기 회고

## 요약 판단

- 결론: 판단 보류. 이번 scheduled analyst review는 2026-06-01 06:23 KST, 즉 2026-05-31 17:23 ET에 실행되어 2026-06-01 미국 정규장 close 전이다. 따라서 2026-05-29 validation fills의 1D horizon과 2026-05-22 stock-only cohort의 5D horizon은 아직 완성되지 않았다.
- 핵심 이유: Alpaca MCP 기준 계좌, 포지션, 주문, fill 활동, 가격 bar는 조회 가능했고 open US equity order는 0건이었다. 그러나 portfolio history와 calendar reads는 각각 initial + 2 retries 후 cancelled gap으로 남아 계좌 단위 MFE/MAE와 정확한 calendar confirmation을 정책 증거로 쓰지 않는다.
- 정책 반영 여부: 보류. 완료된 새 1D/5D/20D 결과가 없고, Alpha/FRED/Firecrawl provider gap도 남아 있어 `wiki/policy-book/recommendation-policy.md`는 변경하지 않는다.

## Reconciliation

| 항목 | 값 |
| --- | --- |
| Paper mode | `ALPACA_PAPER_TRADE=true` |
| Account status | ACTIVE |
| Portfolio value | 101,975.35 USD |
| Cash | 34,800.26 USD |
| Buying power | 130,809.93 USD |
| Long market value | 67,175.09 USD |
| Open US equity orders | 0 |
| Position count | 32 |
| Recent FILL scope | 2026-05-22 이후 buy fills only |
| Portfolio history | cancelled gap after initial + 2 retries |
| Alpaca calendar | cancelled gap after initial + 2 retries |
| Orders submitted/replaced/cancelled/closed by this workflow | 0 / 0 / 0 / 0 |

## Review 후보

### 2026-05-29 validation fills

| Symbol | 2026-05-29 fill | Current/reference | Provisional return | 상태 |
| --- | ---: | ---: | ---: | --- |
| AMZN | 272.76 | 270.64 | -0.78% | 1D 대기 |
| NKE | 46.59 | 46.23 | -0.77% | 1D 대기 |
| PFE | 26.09 | 26.18 | +0.34% | 1D 대기 |
| SO | 91.55 | 92.05 | +0.55% | 1D 대기 |
| SLB | 54.79 | 54.55 | -0.44% | 1D 대기 |
| QQQ | 737.62 | 738.31 | +0.09% | 1D 대기 |
| V | 331.00 | 326.36 | -1.40% | 1D 대기 |
| GOOGL | 383.13 | 380.34 | -0.73% | 1D 대기 |
| WMT | 115.00 | 115.75 | +0.65% | 1D 대기 |
| NEE | 86.46 | 87.01 | +0.64% | 1D 대기 |

이 표는 주말 기준 mark-to-market이며 1D 판단이 아니다. 다음 미국 정규장 close 이후 SPY/QQQ 대비 1D 판단을 별도로 작성한다.

### 2026-05-22 stock-only cohort

2026-05-22 포트폴리오의 5D 회고는 2026-06-01 regular-session close 이후로 유지한다. 2026-05-29 최신 bar 기준으로는 AMD, IONQ, AVGO, LRCX, TSM, ETN이 양호했고 NVDA, NOK, UNH, RGTI는 약하거나 flat에 가까웠다. 그러나 계획된 5D horizon이 아직 완료되지 않았으므로 이번 문서에서는 사전 상태로만 남긴다.

## 당시 판단 복원

- 2026-05-29 22:31 KST run은 SPY/AMZN/NKE/PFE/BAC를 계획했지만 실제 fill은 AMZN/PFE만 있고 BAC/SPY는 취소, NKE는 이후 22:51 KST run에서 체결됐다.
- 2026-05-29 22:51 KST run은 NKE/SO/SLB 1주 validation buy를 체결했다.
- 2026-05-29 23:51 KST run은 QQQ/V 1주 validation buy를 체결했다.
- 2026-05-30 00:11 KST run은 GOOGL/WMT/NEE 1주 validation buy를 체결했다.
- 공통 근거는 paper-only, long-only, whole-share, day limit, active/tradable US equity or ETF, fresh quote/spread, open-order gate, 소액 validation sizing, research MCP minimum confirmation, 그리고 sell/trim 선평가에서 active risk-reducing trigger가 없다는 점이었다.

## 현재 결과와 해석

Alpaca news는 2026-05-29 이후 AI-led risk-on 장세가 이어졌음을 보여준다. AMZN/GOOGL/QQQ는 AI infrastructure와 hyperscaler 맥락이 있었고, WMT는 장후 목표가 상향 뉴스가 있었다. 반대로 SO는 hold와 목표가 하향, SLB는 mixed shelf filing headline이 있어 방어/에너지 분산 후보의 1D 후속을 더 엄격히 봐야 한다.

ADBE는 Yahoo Finance MCP에서 AI shopping/referral, Firefly/AI-agent 기대, stock-photo cannibalization 우려가 동시에 확인됐다. 이 맥락은 2026-05-29 ADBE after-hours validation buy의 강한 1D 결과를 설명하는 후보지만, 단일 사례라 정책 승격에는 쓰지 않는다.

## Skipped recommendation review

| 대상 | 당시 이유 | 현재 회고 |
| --- | --- | --- |
| MRK 2026-05-30 00:31 계획 | open `new` 이후 scheduler stale cleanup에서 취소, fill 없음 | 실제 포지션이 없으므로 trade review 대상은 아니다. 다음 healthcare/pharma 후보가 다시 뜨면 stale-open/order-lifecycle evidence를 먼저 확인한다. |
| 2026-05-30 이후 after-hours runs | quote freshness gate 실패와 후보별 thesis/concentration/notional/spread 제약 | 주말/장외 stale quote 문제라 opportunity miss로 보지 않는다. |
| AAPL/COP/NOK 추가 후보 | due validation lifecycle review 우선 | 추가 매수보다 회고를 우선한 판단은 현 policy와 일치한다. |

## 데이터 공백

- Alpaca portfolio history는 2회 retry 후에도 cancelled라 계좌 단위 MFE/MAE와 intraday drawdown을 계산하지 않았다.
- Alpaca calendar도 2회 retry 후 cancelled라 이번 run에서는 최신 완료 regular close를 Alpaca daily bars와 기존 review due schedule로만 판단했다.
- Alpha Vantage는 PING healthy였으나 첫 non-PING candidate call인 `MARKET_STATUS`가 cancelled되어 즉시 Alpha retries를 중단했다.
- FRED와 Firecrawl은 registered callable tool namespace가 노출되지 않아 `wrapper_error`로 기록했고 shell/curl probe는 하지 않았다.

## 정책학습 판단

- Review backlog throttle 가설은 유지한다. 2026-05-29 한 세션에서 10건의 validation buy가 쌓였고, 다음 정규장 close 이후 1D 회고 부담이 크다.
- `software/AI follow-through`, `defensive-diversification-price-confirmation`, `existing-position-breakout-add-penalty`는 계속 검증 중 가설이다.
- 이번 run은 새 완료 horizon이 없으므로 `wiki/policy-book/recommendation-policy.md`를 업데이트하지 않는다.

## 다음 review due

- 2026-05-29 정규장 validation fills 10건: 2026-06-01 regular-session close 이후 1D 회고 due.
- 2026-05-22 stock-only 포트폴리오: 2026-06-01 regular-session close 이후 5D 회고 due.
- 2026-05-26 validation fills LLY/FCX/NOK/NVDA/AAPL: 5D/20D 회고 대기.
- 2026-05-27 validation fills NKE/PFE/SO/WMT/NEE/AMZN/BAC/XOM/V: 5D/20D 회고 대기.
- 2026-05-28 validation fills와 2026-05-29 ADBE after-hours fill: 5D/20D 회고 대기.

## 연결 문서

- 주문 계획: `wiki/trade-ledger/orders/2026-05-29-2231-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-2251-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-2351-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-30-0011-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-30-0031-hourly-autopilot.json`
- 당시 리포트: [[2026-05-29-2231-hourly-autopilot]], [[2026-05-29-2251-hourly-autopilot]], [[2026-05-29-2351-hourly-autopilot]], [[2026-05-30-0011-hourly-autopilot]], [[2026-05-30-0031-hourly-autopilot]]
- 원천 자료: [[2026-06-01-0623-analyst-review-cycle-sources]]
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-01-0623-analyst-review-cycle.json`
- 포트폴리오: [[portfolio-current]]
