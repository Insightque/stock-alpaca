---
id: 2026-06-19-portfolio-review
review_type: interim
reviewed_at: 2026-06-18T21:30:00Z
paper: true
decision_date:
  - 2026-05-22
  - 2026-06-17
  - 2026-06-18
entry_date: multiple
exit_date: partial
---

# 2026-06-19 포트폴리오 리뷰

## 요약 판단

- 결론: 혼합. `2026-06-17 ET` fill cohort `17건`의 `1D` closeout과 `NOK` `20D` add-block review를 마쳤고, 결과는 `NVDA/AMZN/GOOGL`의 양호한 후속과 `SLB/FCX/BAC/COP/WMT`의 약한 후속이 함께 나왔다.
- 핵심 이유:
  - `NVDA`는 `206.23 -> 210.38`로 `+2.01%` 올라 절대수익이 양호했고, `QQQ +2.40%`에는 소폭 못 미쳤지만 AI core holding add의 품질은 유지됐다.
  - `MRK -1.12%`, `SO -0.13%`, `AAPL -0.19%`는 방어형 또는 mega-cap validation add가 당장 강한 후속을 만들지 못했다.
  - `NOK`는 `2026-06-18 ET` close `13.49 USD`로 평균단가 `15.044527 USD`를 계속 하회해, JP Morgan 상향과 Alpha quarterly beat에도 `existing-position-breakout-add-penalty`를 해제할 근거가 없었다.
- 정책 반영 여부: 보류. direct Alpaca account/order는 정상 재확인했지만 `get_account_activities_by_type(FILL)`와 `get_portfolio_history`가 다시 cancelled였고, recent scheduler source-of-record `positions=32`와 이번 direct `get_all_positions=34` 사이의 정합성 차이도 남아 있다.

## Alpaca 정합성 점검

| 항목 | 값 |
| --- | --- |
| paper mode | `true` |
| market clock | `2026-06-18 17:21 ET`, closed |
| account status | `ACTIVE` |
| portfolio value | `101,755.32 USD` |
| cash | `28,610.97 USD` |
| buying power | `303,996.18 USD` |
| long market value | `73,144.35 USD` |
| open orders | `0` |
| positions | direct `34`, recent source-of-record `32` |
| watchlists | `0` |
| fills scope | `after=2026-06-12T00:00:00Z` activity ledger 기준 |
| Alpaca `FILL` activity by type | `cancelled` x1 |
| Alpaca `portfolio_history` | `cancelled` x1 |
| order mutations in this workflow | `submit 0 / replace 0 / cancel 0 / close 0` |

## Due horizon 스캔

| bucket | count | 메모 |
| --- | --- | --- |
| pending 1D | `17` | `2026-06-18 ET` trim/exit fill cohort `17건` 신규 등록 |
| pending 5D | `40` | 기존 `23건` + 오늘 closeout한 `2026-06-17 ET` fill cohort `17건` 승격 |
| pending 20D | `14` | `NOK` `20D` closeout 완료로 `15 -> 14` |

- `blocked_add_symbols`: `NOK`
- `due_reviews_blocking_adds`: 없음. 다만 `NOK` add-block 자체는 유지한다.

## 2026-06-17 ET fill cohort 1D closeout

기준 benchmark는 Alpaca close-to-close 기준 `SPY 741.02 -> 746.75`로 `+0.77%`, `QQQ 722.48 -> 739.82`로 `+2.40%`다.

| Symbol | Action | Fill | 2026-06-18 close | 1D return | vs SPY | vs QQQ | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| PFE | sell trim 1주 | 25.97 | 25.22 | `-2.89%` | n/a | n/a | 양호 |
| RGTI | sell trim 1주 | 20.75 | 21.34 | `+2.84%` | n/a | n/a | 약함 |
| BAC | buy | 57.57 | 56.15 | `-2.47%` | `-3.24%p` | `-4.87%p` | 약함 |
| WMT | buy | 119.83 | 117.19 | `-2.20%` | `-2.97%p` | `-4.60%p` | 약함 |
| FCX | buy | 71.40 | 68.66 | `-3.84%` | `-4.61%p` | `-6.24%p` | 강한 약함 |
| NKE | buy | 45.30 | 45.195 | `-0.23%` | `-1.00%p` | `-2.63%p` | 중립 약함 |
| NEE | buy | 86.38 | 86.735 | `+0.41%` | `-0.36%p` | `-1.99%p` | 중립 |
| AMZN | buy | 240.44 | 244.61 | `+1.73%` | `+0.96%p` | `-0.67%p` | 양호 |
| MSFT | buy | 385.40 | 379.08 | `-1.64%` | `-2.41%p` | `-4.04%p` | 약함 |
| XOM | buy | 141.54 | 137.81 | `-2.64%` | `-3.41%p` | `-5.04%p` | 약함 |
| AAPL | buy | 298.42 | 297.86 | `-0.19%` | `-0.96%p` | `-2.59%p` | 중립 약함 |
| GOOGL | buy | 365.24 | 367.93 | `+0.74%` | `-0.03%p` | `-1.66%p` | 중립 양호 |
| COP | buy | 110.83 | 107.735 | `-2.79%` | `-3.56%p` | `-5.19%p` | 약함 |
| SO | buy | 93.24 | 93.12 | `-0.13%` | `-0.90%p` | `-2.53%p` | 중립 약함 |
| SLB | buy | 51.32 | 48.095 | `-6.28%` | `-7.05%p` | `-8.68%p` | 강한 약함 |
| MRK | buy | 115.19 | 113.895 | `-1.12%` | `-1.89%p` | `-3.52%p` | 중립 약함 |
| NVDA | buy | 206.23 | 210.38 | `+2.01%` | `+1.24%p` | `-0.39%p` | 양호 |

### 해석

- 이번 1D는 broad risk-on tape였지만, cohort 내부 확산은 고르지 않았다. `NVDA`와 `AMZN`은 절대수익이 양호했고 `GOOGL`도 benchmark 근처에서 버텼다.
- 반대로 `FCX`, `SLB`, `COP`, `XOM`은 energy/materials sleeve가 같은 날 동반 약세를 보이며 sector timing 리스크를 다시 드러냈다.
- `MRK`, `SO`, `AAPL`은 손실 폭이 크진 않았지만, 새 validation add가 즉시 follow-through를 만든 것도 아니다. 방어형 분산 자체는 유지하되, 단일 1D 결과만으로 defensive sleeve 확대를 정당화하진 않는다.
- trim timing은 엇갈렸다. `PFE` residual exit는 다음 close가 더 낮아 유리했지만, `RGTI` residual trim은 다음 close가 더 높아 exact timing edge가 약했다.

## NOK 20D add-block review

- 기준 판단: `add-block 유지`
- 핵심 수치:
  - 평균단가 `15.044527 USD`
  - `2026-06-18 ET` close `13.49 USD`
  - close 기준 미실현 약 `-10.34%`
- 보강 근거:
  - Alpha Vantage `EARNINGS` 최신 분기 row는 `2026-03-31` 분기 `reportedEPS=0.06`, `estimatedEPS=0.05`, `surprisePercentage=20`로 beat였다.
  - Yahoo Finance recommendation summary에서는 `2026-06-12` JP Morgan `Overweight`, PT `14 -> 21`이 유지됐다.
  - SEC EDGAR recent filings는 `2026-06-09/06-05/06-01/05-26` `6-K` 흐름으로 공시 연속성은 확인됐다.
- 결론:
  - fundamental/news tone은 예전보다 낫지만, price confirmation은 없다.
  - 따라서 `existing-position-breakout-add-penalty`를 유지하고, `NOK` 신규 add 차단은 계속 타당하다고 본다.

## Open-position monitor

| symbol | qty | avg | 2026-06-18 close/current | unrealized | 메모 |
| --- | --- | --- | --- | --- | --- |
| `NOK` | 402 | `15.044527` | `13.49 / 13.55` | 약 `-9.93% ~ -10.34%` | 20D review를 닫았지만 add-block 유지가 맞다. |
| `NVDA` | 39 | `214.805897` | `210.38 / 210.50` | 약 `-2.00%` | 1D 신규 add는 양호했다. core holding으로는 유지 가능하다. |
| `MRK` | 1 | `115.19` | `113.895 / 114.03` | 약 `-1.01% ~ -1.12%` | defensive probe는 유지 가능하지만 추가 확대 근거는 부족하다. |
| `AVGO` | 1 | `461.26` | `411.07 / 412.00` | 약 `-10.68% ~ -10.89%` | 잔여 1주라 trim 후속 정책 해석은 계속 제한적이다. |
| `RGTI` | 0 | n/a | `21.34` | closed | residual speculative sleeve는 정규장 trim 연속 집행으로 모두 정리됐다. |

## Skipped recommendation 재점검

| symbol | 현재 해석 | 결론 |
| --- | --- | --- |
| `NOK` | latest close/current 모두 평균단가 아래에 머물러 add-block 해제 근거가 없다. | skip/add-block 유지 |
| `SBUX` | 직전 cycle의 regular-close-after submission cancellation은 여전히 lifecycle discipline 쪽 판단이 맞다. | trade review 대상 아님 |
| `SO` | current holding은 유지되지만 `2026-06-17 ET` add 1D가 benchmark를 못 따라 trim/scale 논리를 바로 강화하기 어렵다. | metric 보강 전 관망 |

## MCP 커버리지와 데이터 갭

- `alpaca`: usable. direct `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_watchlists/get_account_activities/get_stock_snapshot/get_asset`는 usable이었다.
- `alpaca FILL activity by type`: `gap_category=cancelled`, `retry_count=0`. 이번 run 단일 재시도도 cancelled라 fill-by-type cross-check는 general activity ledger로 대체했다.
- `alpaca portfolio_history`: `gap_category=cancelled`, `retry_count=0`. account curve/MFE/MAE는 이번 run에서 보강하지 못했다.
- `sec-edgar`: usable. `NOK/NVDA/MRK` company info와 recent filings는 usable이었지만 일부 deeper calls는 cancelled였다.
- `alpha-vantage`: usable. required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check를 통과했고 `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:"NOK"})`도 성공했다.
- `yahoo-finance`: usable. `NOK/NVDA/MRK/SO` recommendation summary와 `NOK/MRK/NVDA` news는 usable이었지만 일부 per-symbol calls는 timeout이 있었다.
- `fred`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `firecrawl`: `gap_category=wrapper_error`. registered callable tool surface 미노출.

## 정책 학습

- `NOK`의 20D add-block 유지 판단은 증거가 한 번 더 쌓였지만, 단일 종목 사례라 policy-book 규칙 강화까지는 가지 않는다.
- `NVDA` 1D는 양호했지만 `QQQ` 강세장과 거의 같은 방향이어서 `AI core holding add`를 더 공격적으로 일반화할 정도의 새 정보는 아니다.
- `MRK/SO/AAPL`의 방어형 add는 즉시 성과가 약했고, `FCX/SLB/COP/XOM`의 commodity-energy sleeve는 동반 약세였다. 다만 하루치 결과만으로 sector ban 또는 mandatory trim 규칙을 만들진 않는다.
- 따라서 `wiki/policy-book/recommendation-policy.md`는 수정하지 않는다.

## 다음 due 일정

- `2026-06-19 ET` close: `PFE`, `AVGO` after-hours trim `5D`, `2026-06-18 ET` trim/exit fill cohort `17건`의 `1D`
- `2026-06-22 ET` close: `2026-06-15 ET` fill cohort `18건`의 `5D`
- `2026-06-24 ET` close: `2026-06-17 ET` fill cohort `17건`의 `5D`

## 참조

- [[2026-06-19-0630-analyst-review-cycle-sources]]
- `wiki/evidence-store/run-manifests/2026-06-19-0630-analyst-review-cycle.json`
