---
id: 2026-06-04-portfolio-review
review_type: interim
reviewed_at: 2026-06-03T21:24:26Z
paper: true
decision_date: 2026-05-29/2026-06-01
entry_date: multiple
exit_date:
---

# 2026-06-04 analyst review cycle

## 요약 판단

- 결론: 혼합이다. 2026-05-29 validation fill 10건의 5D 결과는 SLB/QQQ/WMT만 의미 있게 버텼고, AMZN/NKE/PFE/SO/V/GOOGL/NEE는 여전히 SPY와 QQQ를 모두 밑돌았다.
- 2026-06-01 after-hours AVGO validation 1주는 2026-06-03 close 기준 +3.76%로 SPY/QQQ를 웃돌았지만, 같은 날 Yahoo post-market은 earnings 이후 약 -11.25%를 보여 event risk가 남았다.
- 정책 반영 여부: 보류. defensive diversification 약세와 AI infrastructure follow-through 가설은 강화되지만, portfolio history gap과 SEC/Alpha/FRED/Firecrawl 공백 때문에 `wiki/policy-book/recommendation-policy.md`는 업데이트하지 않는다.

## Reconciliation

| 항목 | 값 |
| --- | --- |
| Paper mode | `ALPACA_PAPER_TRADE=true` |
| Alpaca clock | 2026-06-03 17:21 ET closed, next open 2026-06-04 09:30 ET |
| Account status | ACTIVE |
| Portfolio value | 102,969.30 USD |
| Cash | 34,339.00 USD |
| Buying power | 130,747.66 USD |
| Long market value | 68,630.30 USD |
| Open US equity orders | 0 |
| Position count | 32 |
| Recent FILL scope | 2026-05-22 이후 queried page, reviewed scope에서 sell fill 없음 |
| Portfolio history | cancelled gap after initial + 2 retries |
| Orders submitted/replaced/cancelled/closed by this workflow | 0 / 0 / 0 / 0 |

## 2026-06-01 AVGO after-hours validation: 1D review closeout

AVGO after-hours validation 1주는 461.26 USD에 체결됐고, 2026-06-03 close 478.62 USD 기준 수익률은 +3.76%다. 같은 기간 benchmark는 SPY -0.56%, QQQ +0.22%라서 초과수익은 각각 +4.33%p, +3.55%p다.

이 결과만 보면 first-close validation은 `양호`다. 다만 Alpaca news와 Yahoo Finance는 2026-06-03 ET 장마감 후 Broadcom 실적이 mixed reaction을 받으며 post-market 425.30 USD까지 밀렸음을 보여준다. 즉, AI infrastructure thesis는 유효하지만 earnings-event gap risk가 여전히 커서 즉시 add rule로 승격할 근거는 아니다.

## 2026-05-29 validation fills: 5D review

기준 가격은 Alpaca IEX daily bar의 2026-06-03 close다. 벤치마크는 SPY -0.29%, QQQ +0.81%다.

| Symbol | Fill | 2026-06-03 close | 5D return | SPY 대비 | QQQ 대비 | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| AMZN | 272.76 | 249.99 | -8.35% | -8.06%p | -9.16%p | 약함 |
| NKE | 46.59 | 43.81 | -5.97% | -5.68%p | -6.78%p | 약함 |
| PFE | 26.09 | 25.36 | -2.80% | -2.51%p | -3.61%p | 약함 |
| SO | 91.55 | 90.52 | -1.13% | -0.84%p | -1.94%p | 중립 약함 |
| SLB | 54.79 | 56.86 | +3.78% | +4.06%p | +2.97%p | 양호 |
| QQQ | 737.62 | 744.205 | +0.89% | +1.18%p | +0.08%p | 양호 |
| V | 331.00 | 313.635 | -5.25% | -4.96%p | -6.06%p | 약함 |
| GOOGL | 383.13 | 359.37 | -6.20% | -5.92%p | -7.01%p | 약함 |
| WMT | 115.00 | 116.93 | +1.68% | +1.96%p | +0.87%p | 중립 양호 |
| NEE | 86.46 | 84.615 | -2.13% | -1.85%p | -2.95%p | 약함 |

### 5D 해석

2026-05-29 cohort는 1D에서 보였던 약세가 5D에서도 대부분 해소되지 않았다. AMZN/GOOGL은 mega-cap quality 또는 AI adjacency만으로 직접 AI infrastructure 수혜주를 대체하기 어렵다는 점을 다시 보여줬다. NKE/PFE/SO/NEE/V는 defensive 또는 quality diversification label이 risk-on 및 rates/noise tape에서 edge를 주지 못했다.

예외는 SLB, QQQ, WMT였다. SLB는 oil/energy headline과 commodity tape 덕분에 5D에서 회복했고, QQQ는 benchmark validation 역할을 충실히 했다. WMT는 1D에는 약했지만 5D에서는 소폭 양호로 돌아섰다. 다만 WMT도 QQQ 대비 초과폭은 제한적이라 defensive retail을 적극 승격할 근거는 아니다.

## Skipped recommendation review

| 대상 | 당시 이유 | 현재 회고 |
| --- | --- | --- |
| MRK 2026-05-30 00:31 계획 | stale cleanup에서 취소, fill 없음 | 5D cohort 자체가 약했으므로 no-fill을 opportunity miss로 보지 않는다. 아직 trade review 대상도 아니다. |
| 2026-06-02~2026-06-04 repeated no-order hourly runs | due review backlog, buy window 종료, portfolio-fit/replacement-rank 부족 | 오늘 5D 결과를 보면 신규 buy를 늦춘 판단은 보수적이지만 타당했다. 특히 defensive/quality add를 강행하지 않은 점이 맞았다. |
| AVGO/NOK add 보류 | due validation review 우선 | AVGO 1D는 양호, NOK 5D는 기존 강함 판단 유지로 보이지만 add 전 lifecycle review를 먼저 닫은 절차는 합리적이었다. |

## 잘한 점

- benchmark ETF(QQQ) validation은 5D에도 안정적으로 동작했다.
- SLB처럼 1D 약세가 5D에서 회복된 사례를 남겨 단기 약세와 thesis failure를 구분할 수 있게 했다.
- AVGO after-hours validation은 small size로 event alpha를 확인하면서도 계좌 리스크를 크게 늘리지 않았다.

## 부족했던 점

- 2026-05-29 cohort는 한 세션에 너무 많은 서로 다른 thesis를 동시에 검증해 신호 분리가 어렵다.
- defensive diversification 후보군은 1D에 이어 5D에서도 반복적으로 약했다. label보다 tape/regime 적합도와 price confirmation을 더 강하게 봐야 한다.
- mega-cap quality 보조 후보(AMZN/GOOGL)는 direct AI infrastructure leader 대비 상대성과가 약했다.

## 정책학습 판단

- `defensive-diversification-price-confirmation` 가설은 강화한다. NKE/PFE/SO/NEE/V가 1D에 이어 5D에서도 대부분 benchmark를 밑돌았다.
- `AI semiconductor/core infrastructure follow-through` 가설도 유지 강화한다. AVGO after-hours 1D와 기존 2026-05-22 stock-only 5D 증거는 여전히 우호적이다.
- 그러나 정책 변경은 보류한다. 이번 run은 반복 패턴을 보여도 한정된 시장 regime와 incomplete provider set 위에서 나온 결과라 active rule 승격 기준에는 미달한다.

## 다음 review due

- AVGO after-hours validation 1주: 5D review는 2026-06-05 미국 정규장 close, 즉 2026-06-06 KST 이후 확인한다.
- 2026-05-22 stock-only cohort: 20D review 대기.
- 2026-05-29 validation fills: 20D review 대기.
- 2026-05-28 validation fills와 ADBE after-hours fill: 5D/20D review 대기.

## 연결 문서

- 원천 자료: [[2026-06-04-0624-analyst-review-cycle-sources]]
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-04-0624-analyst-review-cycle.json`
- 이전 회고: [[2026-06-02-portfolio-review]], [[2026-06-01-portfolio-review]], [[2026-05-30-portfolio-review]]
- 주문 계획: `wiki/trade-ledger/orders/2026-05-29-2231-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-2251-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-2351-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-30-0011-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-06-01-0931-after-hours-autopilot.json`
