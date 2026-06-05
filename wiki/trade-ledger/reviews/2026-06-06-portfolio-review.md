---
id: 2026-06-06-portfolio-review
review_type: interim
reviewed_at: 2026-06-05T21:26:55Z
paper: true
decision_date: 2026-06-04/2026-06-05/2026-06-01
entry_date: multiple
exit_date:
---

# 2026-06-06 analyst review cycle

## 요약 판단

- 결론: 혼합이다. `2026-06-04 ET` validation buy cohort의 1D 결과는 Nasdaq 급락 하루에서 `AAPL/WMT/NEE/V/SO/BAC`가 방어적으로 버틴 반면 `QQQ/SLB/FCX/PLTR`는 약했다. 단일 day-shock만으로 defensive/financial 규칙을 승격하기는 이르다.
- 핵심 이벤트: `AVGO`의 `2026-06-01` after-hours validation 1주는 `2026-06-05` close 기준 `-16.37%`로 5D가 약했고, 정규장 trim 4주가 `389.25 USD`에 체결되며 risk-reducing 대응이 실행됐다. `INTC`는 `99.93 USD` exit fill이 확인돼 validation buy 전체 판단은 `약함`, exit discipline은 `양호`로 정리한다.
- 정책 반영 여부: 보류. Alpaca `portfolio_history`가 3회 연속 cancelled였고, `alpha-vantage`는 PING 이후 첫 non-PING call이 cancelled, `fred/firecrawl`은 namespace 미노출 `wrapper_error`라 active rule 승격 근거가 부족하다.

## Reconciliation

| 항목 | 값 |
| --- | --- |
| Paper mode | `ALPACA_PAPER_TRADE=true` |
| Alpaca clock | `2026-06-05 17:21 ET` closed, next open `2026-06-08 09:30 ET` |
| Account status | ACTIVE |
| Portfolio value | `97,974.00 USD` |
| Cash | `29,947.81 USD` |
| Buying power | `293,831.53 USD` |
| Long market value | `68,026.19 USD` |
| Open US equity orders | 0 |
| Position count | 33 |
| Recent FILL scope | `2026-06-04T00:00:00Z` 이후 direct `FILL` ledger 확인 성공 |
| Portfolio history | cancelled gap after initial + 2 retries |
| Orders submitted/replaced/cancelled/closed by this workflow | 0 / 0 / 0 / 0 |

## 2026-06-04 ET validation fills: 1D review

기준 close는 Alpaca snapshot daily bar의 `2026-06-05` 미국 정규장 종가다. 벤치마크는 `SPY -2.16%`, `QQQ -4.06%`다. sector/theme ETF는 `XLF +0.18%`, `XLE -1.87%`, `XLU +0.93%`, `XLY -2.04%`, `XLK -6.66%`, `SMH -9.34%`를 참고했다.

| Symbol | Fill | 2026-06-05 close | 1D return | SPY 대비 | QQQ 대비 | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| QQQ | 735.23 | 705.375 | -4.06% | -1.90%p | +0.00%p | 기준 약세 |
| SPY | 753.75 | 737.45 | -2.16% | +0.00%p | +1.90%p | 기준 약세 |
| SLB | 57.65 | 54.875 | -4.81% | -2.65%p | -0.75%p | 약함 |
| AAPL | 310.07 | 307.59 | -0.80% | +1.36%p | +3.26%p | 양호 |
| XOM | 153.26 | 150.03 | -2.11% | +0.05%p | +1.95%p | 중립 |
| WMT | 118.36 | 118.90 | +0.46% | +2.62%p | +4.52%p | 양호 |
| FCX | 69.51 | 63.37 | -8.83% | -6.67%p | -4.77%p | 약함 |
| COP | 119.17 | 117.115 | -1.72% | +0.44%p | +2.34%p | 중립 양호 |
| GOOGL | 372.43 | 368.98 | -0.93% | +1.24%p | +3.13%p | 양호 |
| MSFT | 426.78 | 416.635 | -2.38% | -0.21%p | +1.68%p | 중립 |
| NEE | 85.35 | 85.825 | +0.56% | +2.72%p | +4.62%p | 양호 |
| V | 319.83 | 323.66 | +1.20% | +3.36%p | +5.26%p | 강함 |
| NKE | 43.26 | 42.98 | -0.65% | +1.52%p | +3.41%p | 중립 양호 |
| SO | 90.95 | 92.64 | +1.86% | +4.02%p | +5.92%p | 강함 |
| BAC | 54.02 | 53.82 | -0.37% | +1.79%p | +3.69%p | 양호 |
| PLTR | 141.44 | 135.60 | -4.13% | -1.97%p | -0.07%p | 중립 약함 |

### 1D 해석

`2026-06-05`는 rate-hike fear와 AI de-risking이 겹친 tape였다. 이런 날에는 직전 5D 회고에서 약하던 `SO/NEE/WMT/NKE`가 절대수익 또는 benchmark-relative 기준으로 오히려 버텼고, `QQQ/SLB/FCX/PLTR`는 더 취약했다. 따라서 최근 몇 차례 5D review가 보여준 `defensive diversification 전반 약세`를 곧바로 active rule로 강화하면 과적합 위험이 크다. 이번 1D는 regime shock 대응력 자료로만 남기고, 5D와 20D에서 다시 확인해야 한다.

반면 `AAPL/GOOGL/BAC/V`는 절대수익이 크지 않아도 SPY와 QQQ를 모두 이겼다. 특히 `V`와 `SO`는 market-wide drawdown 대비 명확한 완충 역할을 했다. 이 역시 단기 tape 적합성의 증거일 뿐, 즉시 add rule 승격 근거는 아니다.

## AVGO after-hours validation 5D review

`AVGO` after-hours validation 1주는 `2026-06-01` 평균 `461.26 USD`에 체결됐고, `2026-06-05` close `385.73 USD` 기준 수익률은 `-16.37%`다. `2026-06-04` earnings 이후 기대 대비 덜 인상적인 AI guidance, semiconductor-wide de-risking, megacap AI 밸류에이션 리셋이 한꺼번에 반영됐다.

이번 5D closeout의 핵심은 결과 자체보다 대응 방식이다. scheduled hourly autopilot은 `2026-06-06 03:37 KST` 정규장 run에서 same-day duplicate/open-order conflict 없이 quote `389.00/389.72`, spread `0.1847%`, held qty `16` 조건을 확인하고 risk-reducing trim 4주를 `389.25 USD`에 체결했다. 즉, validation add 자체는 `약함`이지만 core position 전체를 감정적으로 청산하지 않고 size를 줄인 대응은 합리적이었다.

## Closed-position review: INTC

`INTC`의 validation buy는 `116.79 USD` 진입 후 `2026-06-05` 정규장에서 `99.93 USD` full-exit가 체결돼 총 수익률 `-14.44%`로 닫혔다. `2026-05-30` 1D review와 `2026-06-05` 5D review가 모두 `약함`이었고, direct catalyst depth보다 sector sympathy와 옵션/AI headline에 더 기대던 포지션이었다.

여기서 loss 자체보다 중요한 점은 lifecycle exit timing이다. exit order는 `2026-06-05` close `98.97 USD`보다 높은 `99.93 USD`에 체결됐고, latest trade도 `97.50 USD`까지 내려가 있었다. 즉, 초기 진입 판단은 약했지만 5D weakness 이후의 후속 exit discipline은 손실 통제 측면에서 맞았다.

## Open-position catalyst review

| Symbol | 현재 상태 | 회고 |
| --- | --- | --- |
| AVGO | 보유 12주, current price `387.33 USD`, avg entry `413.888125 USD` | earnings-event shock 이후 validation add는 실패했다. 다만 trim으로 size를 줄였고 AI infrastructure core thesis까지 즉시 폐기할 단계는 아니다. |
| JPM | 보유 1주, avg entry `311.81 USD`, current price `311.40 USD` | 당일 financials rotation idea는 first close `312.38 USD`까지는 유지됐다. 아직 1D horizon 전이므로 `회고 대기`로만 둔다. |
| SO | 보유 5주, current price `92.00 USD`, avg entry `92.696 USD` | 5D weak narrative와 달리 2026-06-05 shock day에는 상대적으로 버텼다. trim/watch 근거는 유지하되 immediate negative rule 승격은 과도하다. |

## Skipped recommendation review

| 대상 | 당시 이유 | 현재 회고 |
| --- | --- | --- |
| JNJ `2026-06-05 04:51 KST` close-race cancel | actual submit timestamp가 `2026-06-04 16:02:59 ET`로 밀려 market-close hard gate 복구 | `2026-06-05` close `232.71 USD`는 planned limit `229.25 USD` 대비 `+1.51%`라 결과만 보면 miss다. 그래도 close-after-submit를 허용했다면 규율 파손이 더 큰 문제였으므로 policy miss로 보지 않는다. |
| NKE `2026-06-06 04:51 KST` close-race cancel | regular close 이후 submit되어 즉시 cancel | `2026-06-05` close `42.98 USD`는 canceled limit `43.20 USD`보다 `-0.51%`라 miss가 아니다. 복구 cancel이 맞았다. |
| CVX `2026-06-06 02:51 KST` same-session cancel | stale/open-order lifecycle 정리 후 no fill | `2026-06-05` close `187.31 USD`는 planned limit `187.68 USD`보다 `-0.20%`라 강한 missed opportunity는 아니다. |
| NEE `2026-06-06 02:31 KST` same-session cancel | stale/open-order lifecycle 정리 후 no fill | `2026-06-05` close `85.825 USD`는 planned limit `85.47 USD`보다 `+0.42%`지만 spread/lifecycle cleanup 직후 재진입 회피 규율까지 감안하면 policy breach로 보기 어렵다. |

## 잘한 점

- 이번 run은 read-only reconciliation만으로 `JPM` 신규 fill, `AVGO` trim fill, `INTC` exit fill, `NKE/CVX/NEE/JNJ` cancel을 모두 cross-check했다.
- `AVGO`는 validation add failure와 core thesis를 분리해 기록했고, `INTC`는 손실 원인과 exit discipline을 나눠 평가했다.
- `2026-06-05` shock day 1D 결과가 5D narrative와 다를 수 있음을 남겨 policy overfit을 막았다.

## 부족했던 점

- Alpaca `portfolio_history`가 끝내 복구되지 않아 account-level drawdown path와 realized/unrealized curve 검증이 비어 있다.
- `alpha-vantage`는 PING 뒤 첫 non-PING candidate call이 cancelled되어 earnings detail cross-check를 못 했다.
- `fred`와 `firecrawl`은 등록 요구와 달리 callable namespace가 노출되지 않아 macro/IR 보강을 runtime에서 직접 확인하지 못했다.

## 정책학습 판단

- `event-validation-adds must stay small` 가설은 강화된다. `AVGO`처럼 first-close가 양호해도 5D event shock가 크면 add 승격은 매우 위험하다.
- `lifecycle-exit-after-5D-weakness` 가설은 `INTC` 사례에서 유용해 보인다. 다만 단일 사례라 active rule 승격은 보류한다.
- `defensive names can outperform on shock days` 관찰은 남긴다. 하지만 5D/20D data와 충돌하므로 가설 단계에 머문다.

## 다음 review due

- `2026-06-05 ET` fill cohort 1D: `JPM`, `SO`, `PFE`, `AMZN`, `COP`, `SLB`, `NVDA`, `V`, `AAPL`, `PLTR`, `FCX`, `WMT`, `BAC`는 `2026-06-08` 미국 정규장 close 이후 평가 가능하다.
- `2026-06-04 ET` fill cohort 5D: `QQQ`, `SPY`, `SLB`, `AAPL`, `XOM`, `WMT`, `FCX`, `COP`, `GOOGL`, `MSFT`, `NEE`, `V`, `NKE`, `SO`, `BAC`, `PLTR`는 `2026-06-11` 미국 정규장 close 이후 5D review 대상이다.
- `NOK` 20D는 기존 일정대로 유지한다.

## 연결 문서

- 원천 자료: [[2026-06-06-0626-analyst-review-cycle-sources]]
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-06-0626-analyst-review-cycle.json`
- 개별 회고: [[2026-06-06-INTC-review]]
- 이전 회고: [[2026-06-05-portfolio-review]], [[2026-06-04-portfolio-review]], [[2026-06-02-portfolio-review]]
