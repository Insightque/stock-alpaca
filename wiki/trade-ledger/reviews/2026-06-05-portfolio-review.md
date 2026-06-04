---
id: 2026-06-05-portfolio-review
review_type: interim
reviewed_at: 2026-06-04T21:27:37Z
paper: true
decision_date: 2026-05-26/2026-05-27/2026-05-28/2026-06-04
entry_date: multiple
exit_date:
---

# 2026-06-05 analyst review cycle

## 요약 판단

- 결론: backlog closeout 기준으로는 혼합이다. 2026-05-26 validation 5D는 `LLY`/`FCX`/`NVDA`가 양호했고, 2026-05-27 validation 5D는 `BAC`/`XOM`만 의미 있게 회복했다. 2026-05-28 validation 5D는 `PLTR`/`QQQ`/`SLB`/`BAC`/`COP`/`NVDA`가 양호했지만 `INTC`/`NKE`/`GOOGL`/`SO`/`NEE`/`TSLA`/`AMZN`은 계속 약했다.
- 운영 해석: generic defensive/quality 라벨은 반복적으로 약했고, software/AI momentum과 selected energy/financials late-follow-through가 더 잘 작동했다. 다만 이 신호는 소표본 paper validation이라 바로 active rule로 승격하지 않는다.
- 예외 포지션: `AVGO`는 2026-06-04 미국 정규장 종가 417.99 USD, 당일 -12.78%로 earnings-event drawdown이 발생했다. 2026-06-01 after-hours validation 1주의 5D horizon은 아직 `2026-06-05` 미국 정규장 close 이후에만 닫을 수 있으므로 오늘은 catalyst alert만 기록한다.
- 정책 반영 여부: 보류. Alpaca `portfolio_history`와 `FILL` activity direct read가 cancelled gap이고, SEC/Alpha/FRED/Firecrawl 공백이 남아 있어 `wiki/policy-book/recommendation-policy.md`는 업데이트하지 않는다.

## Reconciliation

| 항목 | 값 |
| --- | --- |
| Paper mode | `ALPACA_PAPER_TRADE=true` |
| Alpaca clock | 2026-06-04 17:21 ET closed, next open 2026-06-05 09:30 ET |
| Account status | ACTIVE |
| Portfolio value | 102,944.26 USD |
| Cash | 30,487.94 USD |
| Buying power | 253,654.69 USD |
| Long market value | 72,456.32 USD |
| Open US equity orders | 0 |
| Position count | 33 |
| Recent FILL scope | `2026-05-22` 이후 order reconciliation cross-check 기준 reviewed |
| Direct FILL activity read | cancelled gap after initial + 2 retries |
| Portfolio history | cancelled gap after initial + 2 retries |
| Orders submitted/replaced/cancelled/closed by this workflow | 0 / 0 / 0 / 0 |

## 2026-05-26 validation fills: 5D review

기준 close는 Alpaca IEX daily bar의 `2026-06-04` 미국 정규장 종가다. 벤치마크는 SPY `+0.30%`, QQQ `+0.66%`, healthcare reference `XLV +2.37%`다.

| Symbol | Fill | 2026-06-04 close | 5D return | SPY 대비 | QQQ 대비 | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| LLY | 1079.38 | 1125.46 | +4.27% | +3.97%p | +3.61%p | 양호 |
| FCX | 63.94 | 69.85 | +9.24% | +8.94%p | +8.58%p | 강함 |
| NOK | 16.50 | 16.61 | +0.67% | +0.36%p | +0.01%p | 중립 |
| NVDA | 213.72 | 218.64 | +2.30% | +2.00%p | +1.64%p | 양호 |
| AAPL | 309.45 | 311.21 | +0.57% | +0.27%p | -0.09%p | 중립 양호 |

`LLY`는 healthcare growth thesis가 `XLV`와 벤치마크를 모두 앞섰고, `FCX`는 materials/copper cyclicality가 가장 강하게 이어졌다. `NVDA`는 5D 기준 우세를 유지했지만, 같은 구간 `SMH`보다 폭발적이지는 않았다. 반대로 `NOK` validation add는 1D 두 번의 약세 이후 5D에서는 본전 수준으로만 복구돼, 기존 대형 보유에 대한 추격 add timing이 여전히 불안정하다는 점을 남긴다.

## 2026-05-27 validation fills: 5D review

기준 close는 `2026-06-04` 미국 정규장 종가다. 벤치마크는 SPY `+0.08%`, QQQ `+0.31%`, sector references는 `XLF +1.22%`, `XLE +4.37%`, `XLU -1.06%`, `XLY -3.05%`다.

| Symbol | Fill | 2026-06-04 close | 5D return | SPY 대비 | QQQ 대비 | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| NKE | 46.15 | 43.60 | -5.53% | -5.61%p | -5.84%p | 약함 |
| PFE | 26.34 | 25.70 | -2.43% | -2.51%p | -2.74%p | 약함 |
| SO | 94.28 | 91.62 | -2.82% | -2.90%p | -3.13%p | 약함 |
| WMT | 118.31 | 117.75 | -0.47% | -0.56%p | -0.78%p | 중립 약함 |
| NEE | 87.34 | 85.66 | -1.92% | -2.01%p | -2.23%p | 약함 |
| AMZN | 270.05 | 253.855 | -6.00% | -6.08%p | -6.31%p | 약함 |
| BAC | 52.06 | 54.11 | +3.94% | +3.85%p | +3.63%p | 양호 |
| XOM | 147.07 | 152.09 | +3.41% | +3.33%p | +3.10%p | 양호 |
| V | 330.01 | 322.00 | -2.43% | -2.51%p | -2.74%p | 약함 |

이 cohort는 `defensive diversification` 가설에 가장 불리했다. `NKE/PFE/SO/WMT/NEE/V/AMZN`은 모두 5D에도 SPY와 QQQ를 못 이겼고, consumer/utilities/quality 라벨만으로는 edge가 없었다. 반면 `BAC`와 `XOM`은 1D 약세 또는 중립 이후 5D에 뒤집혔다. 즉, 금융/에너지 분산은 1D만 보면 오판하기 쉽고 5D 확인이 필요하다는 점은 강화되지만, utilities/defensive basket까지 일괄 정당화되지는 않는다.

## 2026-05-28 validation fills: 5D review

`ADBE` after-hours validation 1주는 `2026-05-28` ET after-hours 체결이라 5D horizon이 아직 완성되지 않았다. 오늘 closeout 대상은 같은 날 regular-session 및 earlier after-hours fills만 잡는다. 벤치마크는 SPY `-0.19%`, QQQ `-0.28%`, sector references는 `SMH +4.75%`, `XLE +2.58%`, `XLF +1.50%`, `XLU +2.01%`, `XLY -0.81%`다.

| Symbol | Fill | 2026-06-04 close | 5D return | SPY 대비 | QQQ 대비 | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| INTC | 116.79 | 111.78 | -4.29% | -4.10%p | -4.01%p | 약함 |
| NOK | 15.40 | 16.61 | +7.86% | +8.05%p | +8.14%p | 강함 |
| PLTR | 134.94 | 141.68 | +4.99% | +5.19%p | +5.28%p | 양호 |
| QQQ | 728.36 | 740.50 | +1.67% | +1.86%p | +1.95%p | 양호 |
| CVX | 184.03 | 188.34 | +2.34% | +2.54%p | +2.62%p | 양호 |
| NKE | 46.03 | 43.60 | -5.28% | -5.09%p | -5.00%p | 약함 |
| PFE | 26.16 | 25.70 | -1.76% | -1.56%p | -1.48%p | 약함 |
| WMT | 118.63 | 117.75 | -0.74% | -0.55%p | -0.46%p | 중립 약함 |
| GOOGL | 389.00 | 372.34 | -4.28% | -4.09%p | -4.00%p | 약함 |
| SO | 93.38 | 91.62 | -1.88% | -1.69%p | -1.60%p | 약함 |
| SLB | 55.48 | 58.02 | +4.58% | +4.77%p | +4.86%p | 양호 |
| SPY | 753.38 | 756.97 | +0.48% | +0.67%p | +0.76%p | 양호 |
| BAC | 51.14 | 54.11 | +5.81% | +6.00%p | +6.09%p | 강함 |
| NEE | 87.83 | 85.66 | -2.47% | -2.28%p | -2.19%p | 약함 |
| NVDA | 212.55 | 218.64 | +2.87% | +3.06%p | +3.15%p | 양호 |
| COP | 114.95 | 119.32 | +3.80% | +4.00%p | +4.08%p | 양호 |
| TSLA | 441.40 | 418.485 | -5.19% | -5.00%p | -4.91%p | 약함 |
| AMZN | 270.55 | 253.855 | -6.17% | -5.98%p | -5.89%p | 약함 |
| XOM | 148.37 | 152.09 | +2.51% | +2.70%p | +2.79%p | 양호 |

여기서도 패턴은 비슷하다. `PLTR`와 `QQQ`는 momentum bucket이 5D까지 유지됐고, energy/financials (`CVX/SLB/BAC/COP/XOM`)는 1D 약세였던 일부 이름까지 회복했다. 반면 `GOOGL/AMZN/TSLA/INTC`는 mega-cap or AI-adjacent라는 라벨만으로 상대우위가 보장되지 않았고, `SO/NEE/WMT/PFE/NKE` 같은 defensive mix는 반복적으로 약했다.

## Open-position catalyst review

| Symbol | 현재 상태 | 회고 |
| --- | --- | --- |
| AVGO | 417.99 USD, 당일 -12.78%, 평균단가 413.888125 USD 대비 아직 소폭 플러스 | earnings-event 이후 AI narrative는 유지되지만 기대치 과열이 크게 걷혔다. `2026-06-01` after-hours validation 1주 5D는 아직 미도래라 오늘은 policy evidence가 아니라 catalyst-risk alert로만 기록한다. |
| PLTR | 141.68 USD, 기존 1주 대비 5D 양호, 오늘 15:55 ET 추가 1주 fill | software/AI partnership news는 계속 나오지만 valuation noise도 크다. `2026-06-04` cohort 1D는 `2026-06-05` 미국 정규장 close 이후 별도로 본다. |
| SO | 보유 4주, 2026-05-27/28/29 validation add가 모두 weak-to-neutral | utilities defensive thesis는 rates/macro confirmation 없이는 신규 add를 정당화하지 못했다. sell trigger까지는 아니지만 add 보류는 유지가 맞다. |

## Skipped recommendation review

| 대상 | 당시 이유 | 현재 회고 |
| --- | --- | --- |
| HOOD `2026-05-28 23:31 KST` recheck-only | 일일 validation buy budget 소진, speculative_growth 노출 discipline | raw return만 보면 miss다. 당시 planned limit `77.26` 대비 `2026-06-04` close `88.315`로 약 `+14.31%`다. 다만 같은 세션에 speculative/software 표본이 이미 많았고 HOOD는 변동성이 매우 커서, 이번 건은 policy breach가 아니라 missed-opportunity hypothesis로 남긴다. |
| JNJ `2026-06-05 04:51 KST` canceled-after-close | actual submit timestamp가 `2026-06-04 16:02:59 ET`로 밀려 market clock hard gate 파손 | miss로 보지 않는다. `2026-06-04` close `228.27`은 planned limit `229.25`보다 낮아, close-race 취소는 규율 유지 측면에서 맞았다. |
| MRK stale-cleanup cancel | stale open-order lifecycle 정리 후 fill 없음 | 이후 performance alone으로 재평가할 근거가 부족하다. lifecycle discipline 유지 사례로만 남긴다. |

## 잘한 점

- today run은 order mutation 없이 backlog 5D review를 닫고, 미래 due와 catalyst alert를 분리했다.
- `BAC/XOM/CVX/SLB/COP`처럼 1D와 5D가 다른 이름을 남겨, 단기 약세와 thesis failure를 구분할 근거를 쌓았다.
- `PLTR/QQQ`와 `LLY/FCX`는 서로 다른 bucket에서 validation efficacy를 보여줬다.

## 부족했던 점

- review backlog가 실제로 밀려 `2026-05-26~2026-05-28` 5D가 한 번에 몰렸다. 신규 validation cadence 대비 analyst closeout capacity를 더 엄격히 맞춰야 한다.
- defensive/quality diversification은 여러 cohort에서 반복적으로 약했는데, macro/source confirmation gap 때문에 왜 약했는지까지는 아직 분해가 부족하다.
- Alpaca `portfolio_history`와 direct `FILL` activity path가 cancelled라 account-level drawdown path, MFE/MAE, fill-ledger audit이 불완전하다.

## 정책학습 판단

- `defensive-diversification-price-confirmation` 가설은 강화된다. `SO/NEE/WMT/PFE/NKE/V`가 여러 cohort에서 반복적으로 약했다.
- `existing-position-breakout-add-penalty`는 `NOK` add history 때문에 여전히 유효한 가설이지만, today 5D만 보면 absolute failure는 아니어서 active rule 승격은 보류한다.
- `energy-financials need 5D confirmation` 가설은 유용하다. `BAC/XOM/CVX/SLB/COP`은 1D보다 5D에서 더 진실한 판단을 제공했다.
- 그러나 정책 문서는 업데이트하지 않는다. provider gaps, small-N paper validations, missing account-path evidence 때문에 active rule threshold에 미달한다.

## 다음 review due

- `2026-06-04` 미국 정규장 fill cohort 1D: `QQQ`, `SPY`, `SLB`, `AAPL`, `XOM`, `WMT`, `FCX`, `COP`, `GOOGL`, `MSFT`, `NEE`, `V`, `NKE`, `SO`, `BAC`, `PLTR`는 `2026-06-05` 미국 정규장 close 이후에만 평가 가능하다.
- `AVGO` 2026-06-01 after-hours validation 1주 5D: `2026-06-05` 미국 정규장 close 이후 due.
- `2026-05-22` stock-only cohort 20D와 `2026-05-29` validation cohort 20D: 아직 미도래다.

## 연결 문서

- 원천 자료: [[2026-06-05-0627-analyst-review-cycle-sources]]
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-05-0627-analyst-review-cycle.json`
- 이전 회고: [[2026-06-04-portfolio-review]], [[2026-06-02-portfolio-review]], [[2026-05-30-portfolio-review]]
- 관련 주문: `wiki/trade-ledger/orders/2026-05-28-2231-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2251-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2311-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2331-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0011-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-06-05-0451-hourly-autopilot.json`
