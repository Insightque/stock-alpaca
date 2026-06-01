---
id: 2026-06-02-portfolio-review
review_type: interim
reviewed_at: 2026-06-01T21:24:13Z
paper: true
decision_date: 2026-05-22/2026-05-29/2026-06-01
entry_date: multiple
exit_date:
---

# 2026-06-02 analyst review cycle

## 요약 판단

- 결론: 혼합이나 학습 신호는 명확하다. 2026-05-29 정규장 validation fill 10건의 1D 결과는 QQQ만 양호했고, AMZN/NKE/PFE/SO/V/GOOGL/NEE는 SPY와 QQQ를 모두 크게 밑돌았다. WMT/SLB는 절대 손실은 작았지만 벤치마크 대비 약했다.
- 2026-05-22 stock-only cohort의 5D 결과는 AI semiconductor/quantum/power 쪽이 강했다. AMD/AVGO/TSM/IONQ/NOK/NVDA는 5D 기준 SPY와 QQQ를 모두 이겼고, UNH/RGTI는 방어 또는 투기 분산 thesis가 충분하지 않았다.
- 2026-06-01 after-hours AVGO 1주 fill은 첫 정규장 close 기준 -0.25%로 판단 보류다. 같은 날 after-hours mark는 강했지만, 정책학습에는 official close를 우선한다.
- 정책 반영 여부: 보류. 기존 `defensive-diversification-price-confirmation`, `review_backlog_throttle`, `existing-position add price-confirmation` 가설을 강화하지만, portfolio history gap과 혼합 cohort 특성 때문에 `wiki/policy-book/recommendation-policy.md`는 변경하지 않는다.

## Reconciliation

| 항목 | 값 |
| --- | --- |
| Paper mode | `ALPACA_PAPER_TRADE=true` |
| Alpaca clock | 2026-06-01 17:21 ET closed, next open 2026-06-02 09:30 ET |
| Account status | ACTIVE |
| Portfolio value | 103,380.11 USD |
| Cash | 34,339.00 USD |
| Buying power | 131,106.21 USD |
| Long market value | 69,041.11 USD |
| Open US equity orders | 0 |
| Position count | 32 |
| Recent FILL scope | 2026-05-22 이후 queried page |
| Portfolio history | cancelled gap after initial + 2 retries |
| Orders submitted/replaced/cancelled/closed by this workflow | 0 / 0 / 0 / 0 |

## 2026-05-29 validation fills: 1D review

기준 가격은 Alpaca IEX daily bar의 2026-06-01 close다. 벤치마크는 SPY +0.28%, QQQ +0.59%다.

| Symbol | Fill | 2026-06-01 close | 1D return | SPY 대비 | QQQ 대비 | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| AMZN | 272.76 | 261.20 | -4.24% | -4.52%p | -4.83%p | 약함 |
| NKE | 46.59 | 45.92 | -1.44% | -1.72%p | -2.03%p | 약함 |
| PFE | 26.09 | 25.64 | -1.72% | -2.00%p | -2.32%p | 약함 |
| SO | 91.55 | 89.03 | -2.75% | -3.03%p | -3.35%p | 약함 |
| SLB | 54.79 | 54.77 | -0.04% | -0.31%p | -0.63%p | 중립 약함 |
| QQQ | 737.62 | 742.60 | +0.68% | +0.40%p | +0.08%p | 양호 |
| V | 331.00 | 322.73 | -2.50% | -2.78%p | -3.09%p | 약함 |
| GOOGL | 383.13 | 376.26 | -1.79% | -2.07%p | -2.39%p | 약함 |
| WMT | 115.00 | 114.57 | -0.37% | -0.65%p | -0.97%p | 중립 약함 |
| NEE | 86.46 | 83.65 | -3.25% | -3.53%p | -3.85%p | 약함 |

### 1D 해석

2026-05-29의 small validation buy는 너무 많은 서로 다른 thesis를 한 번에 검증했다. QQQ는 벤치마크형 validation으로 유효했지만, 개별 종목 다수는 2026-06-01의 AI/semiconductor 강세와 방어/소비/금리민감 약세의 갈림길에서 뒤처졌다.

AMZN/GOOGL은 mega-cap quality thesis였지만 1D 후속이 약했다. 이 둘은 같은 AI tape 안에서도 직접 반도체/AI infrastructure 수혜주보다 약해, mega-cap label만으로 buy quality를 높게 보지 않아야 한다. SO/NEE/PFE/WMT/V는 defensive 또는 quality diversification이었지만, risk-on tape에서 상대성과 방어가 되지 않았다. SLB는 절대 손실은 작았으나 mixed shelf headline과 에너지 macro headline 민감성이 남아 있다.

## 2026-05-22 stock-only cohort: 5D review

5D 기준은 2026-05-22 entry 또는 close 부근에서 2026-06-01 close까지다. 벤치마크는 2026-05-22 close 대비 SPY +1.71%, QQQ +3.50%다.

| Symbol | Avg entry | 2026-06-01 close | 5D return | SPY 대비 | QQQ 대비 | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| NVDA | 215.32 | 224.42 | +4.23% | +2.51%p | +0.73%p | 양호 |
| AMD | 462.73 | 510.05 | +10.23% | +8.52%p | +6.73%p | 강함 |
| AVGO | 410.73 | 460.09 | +12.02% | +10.30%p | +8.52%p | 강함 |
| LRCX | 307.91 | 317.27 | +3.04% | +1.33%p | -0.46%p | 중립 양호 |
| TSM | 405.20 | 436.03 | +7.61% | +5.89%p | +4.11%p | 강함 |
| NOK | 15.04 | 16.235 | +7.95% | +6.24%p | +4.45%p | 강함, 변동성 큼 |
| UNH | 386.56 | 379.85 | -1.74% | -3.45%p | -5.24%p | 약함 |
| ETN | 387.90 | 400.17 | +3.16% | +1.45%p | -0.34%p | 중립 양호 |
| IONQ | 63.48 | 69.285 | +9.14% | +7.43%p | +5.64%p | 강함 |
| RGTI | 25.569584 | 25.63 | +0.24% | -1.48%p | -3.26%p | 약함 |

### 5D 해석

5D 결과는 2026-05-22의 AI semiconductor 중심 stock-only 판단을 대체로 지지한다. AMD/AVGO/TSM/NVDA는 SPY/QQQ 대비 성과가 분명했고, IONQ도 높은 변동성을 감수한 소액 speculative sleeve로는 강했다. NOK는 2026-05-29까지 약했지만 2026-06-01 반등으로 5D 결과가 강해졌다. 단, 큰 단일 보유와 높은 intraday 변동성 때문에 추가매수 근거로 바로 승격하지 않는다.

UNH는 방어적 헬스케어 분산 thesis가 5D에도 작동하지 않았다. RGTI는 quantum sleeve 안에서도 IONQ 대비 품질이 낮았다. ETN/LRCX는 절대 성과와 SPY 대비는 양호하지만 QQQ 대비 edge는 약해, AI risk-on regime에서는 보조 후보로 보는 편이 맞다.

## 2026-06-01 AVGO after-hours validation

AVGO after-hours validation fill은 2026-06-01 00:38 UTC에 461.26 USD로 1주 체결됐다. 2026-06-01 regular close 460.09 USD 기준 수익률은 -0.25%로 판단 보류다. Yahoo Finance와 Alpaca news는 Broadcom earnings-preview 및 AI bottleneck 수혜 narrative를 보여줬지만, 이 이벤트성 맥락은 1D/5D 확인 전에는 add 근거가 아니다.

## Skipped recommendation review

| 대상 | 당시 이유 | 현재 회고 |
| --- | --- | --- |
| MRK 2026-05-30 00:31 계획 | open/new 이후 stale cleanup에서 취소, fill 없음 | 실제 포지션이 없으므로 trade review 대상은 아니다. 기회비용 판단도 현재 evidence로는 보류한다. |
| 2026-06-01 이후 repeated no-order hourly runs | due review backlog, buy entry window 종료, critical-source/portfolio-fit 제약 | 2026-05-29 cohort의 1D 결과가 약했으므로 추가 buy를 막은 lifecycle/review backlog 판단은 타당했다. |
| 2026-06-01 after-hours repeated no-order runs | after-hours session budget 2건 소진 | AVGO 첫 close가 보류이고 NVDA after-hours order는 fill 없이 취소됐으므로, budget cap은 과잉 validation을 막는 데 유효했다. |

## 잘한 점

- 2026-05-22 stock-only cohort는 AI semiconductor/power/quantum core thesis를 5D에서 대체로 잘 포착했다.
- 소액 validation size 덕분에 2026-05-29의 약한 1D cohort가 계좌 전체에 큰 손상을 주지 않았다.
- 2026-06-01 이후 hourly runs가 due review backlog와 lifecycle review를 신규 buy보다 우선한 것은 실제 1D 결과로도 정당화된다.

## 부족했던 점

- 2026-05-29 regular-session validation은 한 세션에 10개 fill을 쌓아 회고 품질과 신호 분리를 어렵게 만들었다.
- Defensive/quality diversification label만으로 PFE/SO/NEE/WMT/V를 검증한 것은 1D 기준 약했다. 금리/유틸리티/소비 방어 thesis는 FRED gap이 있을 때 특히 신규 buy 확신을 낮춰야 한다.
- AMZN/GOOGL은 AI tape 안에서도 직접 AI infrastructure 수혜주보다 약했다. mega-cap quality를 QQQ 대체재처럼 취급하면 상대성과가 희석될 수 있다.
- Portfolio history MCP가 계속 cancelled되어 계좌 단위 MFE/MAE와 drawdown path를 정책 증거로 쓰지 못했다.

## 정책학습 판단

- `defensive-diversification-price-confirmation` 가설은 강화한다. 2026-05-28 1D에 이어 2026-05-29 1D에서도 defensive/quality 후보 다수가 SPY/QQQ 대비 약했다.
- `AI semiconductor/core infrastructure follow-through` 가설도 강화한다. 2026-05-22 5D에서 AMD/AVGO/TSM/NVDA가 모두 benchmark를 이겼다.
- 단, 정책 변경은 보류한다. 현 evidence는 일부 반복성을 보이지만, 한 주의 같은 market regime에 집중되어 있고 portfolio history gap이 있어 active rule 승격 기준에는 부족하다.

## 다음 review due

- 2026-06-01 AVGO after-hours validation: 2026-06-02 regular close 이후 1D 확인.
- 2026-05-29 validation fills: 5D/20D 회고 대기.
- 2026-05-22 stock-only cohort: 20D 회고 대기.
- 2026-05-26, 2026-05-27, 2026-05-28 validation fills: 5D/20D 회고 대기.

## 연결 문서

- 원천 자료: [[2026-06-02-0624-analyst-review-cycle-sources]]
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-02-0624-analyst-review-cycle.json`
- 이전 회고: [[2026-06-01-portfolio-review]], [[2026-05-30-portfolio-review]], [[2026-05-27-portfolio-review]]
- 주문 계획: `wiki/trade-ledger/orders/2026-05-29-2231-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-2251-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-2351-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-30-0011-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-06-01-0931-after-hours-autopilot.json`
