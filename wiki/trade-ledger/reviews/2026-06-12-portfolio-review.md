---
id: 2026-06-12-portfolio-review
review_type: interim
reviewed_at: 2026-06-11T21:32:08Z
paper: true
decision_date: 2026-06-05/2026-06-10
entry_date: multiple
exit_date: partial
---

# 2026-06-12 analyst review cycle

## 요약 판단

- 결론: `2026-06-10 ET` fill cohort 14건의 1D closeout과 `2026-06-05 ET` fill cohort 13건의 5D closeout을 수행했다. 이번 cycle의 broad tape는 `SPY +1.72%`, `QQQ +3.27%` 반등이어서 상대성과 기준이 엄격했다.
- `FCX`와 `NKE`는 `2026-06-10 ET` 1D에서 각각 `+6.48%`, `+3.74%`로 가장 좋았다. `WMT/PFE/BAC`는 절대수익은 플러스였지만 broad rebound 대비로는 강하지 않았다.
- `AVGO/RGTI`의 `2026-06-10 ET` staged trim은 sell 뒤 주가가 각각 `+2.95%`, `+1.67%` 반등해 전일 cycle만큼 깔끔한 exact timing edge는 없었다. 다만 포지션 위험 축소 자체를 뒤집을 정도는 아니다.
- `2026-06-05 ET` 5D cohort는 `BAC`와 `FCX`만 의미 있게 유지됐고, `AAPL/AMZN/PLTR/NVDA/V/COP`는 여전히 약했다. `mega-cap quality averaging-down cadence`와 broad beta add는 계속 보수적으로 다뤄야 한다.
- 정책 반영 여부: 없음. mixed 1D/5D evidence라 반복 패턴 임계치를 넘지 못했다.

## Reconciliation

| 항목 | 값 |
| --- | --- |
| Paper mode | `ALPACA_PAPER_TRADE=true` |
| Alpaca clock | `2026-06-11 17:11 ET` closed, next open `2026-06-12 09:30 ET` |
| Account status | ACTIVE |
| Portfolio value | `99,643.36 USD` |
| Cash | `31,285.06 USD` |
| Buying power | `300,548.92 USD` |
| Long market value | `68,358.30 USD` |
| Open US equity orders | 0 |
| Position count | 33 |
| Recent fill scope | `2026-06-05T00:00:00Z` 이후 direct `FILL` ledger usable |
| Orders submitted/replaced/cancelled/closed by this workflow | 0 / 0 / 0 / 0 |

## 2026-06-10 ET fill cohort 1D closeout

기준 benchmark는 Alpaca close-to-close 기준 `SPY +1.72%`, `QQQ +3.27%`다.

| Symbol | Action | Fill | 2026-06-11 close/current | 1D return | vs SPY | vs QQQ | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| WMT | buy | 118.49 | 120.3782 | `+1.59%` | `-0.13%p` | `-1.68%p` | 중립 양호 |
| AVGO | sell trim 2주 | 373.25 | 384.25 | `+2.95%` | n/a | n/a | 중립 |
| RGTI | sell trim 17주 | 20.38 | 20.72 | `+1.67%` | n/a | n/a | 중립 |
| BAC | buy | 54.77 | 55.20 | `+0.79%` | `-0.93%p` | `-2.49%p` | 중립 |
| PFE | buy | 25.70 | 26.13 | `+1.67%` | `-0.05%p` | `-1.60%p` | 중립 양호 |
| XOM | buy | 151.41 | 146.81 | `-3.04%` | `-4.76%p` | `-6.31%p` | 약함 |
| JNJ | buy | 239.23 | 236.5421 | `-1.12%` | `-2.84%p` | `-4.40%p` | 약함 |
| COP | buy | 121.05 | 115.7518 | `-4.38%` | `-6.10%p` | `-7.65%p` | 강한 약함 |
| SLB | buy | 56.45 | 56.03 | `-0.74%` | `-2.46%p` | `-4.02%p` | 약함 |
| AMZN | buy | 239.33 | 241.49 | `+0.90%` | `-0.82%p` | `-2.37%p` | 중립 약함 |
| FCX | buy | 62.21 | 66.24 | `+6.48%` | `+4.76%p` | `+3.21%p` | 강한 양호 |
| NEE | buy | 85.22 | 84.97 | `-0.29%` | `-2.01%p` | `-3.57%p` | 약함 |
| NKE | buy | 43.98 | 45.625 | `+3.74%` | `+2.02%p` | `+0.47%p` | 양호 |
| MSFT | buy | 398.38 | 391.10 | `-1.83%` | `-3.55%p` | `-5.10%p` | 약함 |

### 해석

- `FCX`는 이번 cohort에서 가장 선명한 승자였다. commodity/materials diversifier가 적어도 이번 하루 반등에서는 broad beta를 넘어섰다.
- `NKE`도 소비재 rebound 표본으로는 양호했다. 다만 과거 `약함` 표본이 이미 누적돼 있어 단일 1D 반등만으로 승격할 수는 없다.
- `WMT/PFE/BAC`는 손실을 피하거나 소폭 수익을 냈지만 `QQQ` 급반등을 따라가지 못했다. defensive validation buy의 품질은 유지되지만 alpha는 제한적이다.
- `XOM/COP/JNJ/SLB/NEE/MSFT`는 broad rebound를 제대로 타지 못했다. 특히 `COP`는 전일 강한 1D 이후 바로 reverse가 나와 energy sleeve add cadence를 더 보수적으로 봐야 한다.
- `AVGO/RGTI` trim은 sell 이후 주가가 되돌림을 보였다. exact timing은 약했지만 포지션 크기 축소 자체를 잘못으로 보긴 어렵다.

## 2026-06-05 ET fill cohort 5D closeout

기준 benchmark는 `SPY 737.45 -> 737.90`로 `+0.06%`, `QQQ 705.375 -> 716.39`로 `+1.56%`다.

| Symbol | Action | Fill | 2026-06-11 close/current | 5D return | vs SPY | vs QQQ | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| JPM | buy | 311.81 | 313.50 | `+0.54%` | `+0.48%p` | `-1.02%p` | 중립 양호 |
| SO | buy | 93.32 | 93.40 | `+0.09%` | `+0.02%p` | `-1.48%p` | 중립 |
| PFE | buy | 26.09 | 26.13 | `+0.15%` | `+0.09%p` | `-1.41%p` | 중립 |
| AMZN | buy | 253.17 | 241.49 | `-4.61%` | `-4.67%p` | `-6.18%p` | 약함 |
| COP | buy | 117.42 | 115.7518 | `-1.42%` | `-1.48%p` | `-2.98%p` | 중립 약함 |
| SLB | buy | 55.67 | 56.03 | `+0.65%` | `+0.59%p` | `-0.91%p` | 중립 양호 |
| NVDA | buy | 208.73 | 205.13 | `-1.72%` | `-1.79%p` | `-3.29%p` | 약함 |
| V | buy | 321.90 | 319.69 | `-0.69%` | `-0.75%p` | `-2.25%p` | 중립 약함 |
| AAPL | buy | 313.27 | 295.50 | `-5.67%` | `-5.73%p` | `-7.23%p` | 강한 약함 |
| PLTR | buy | 138.53 | 131.6007 | `-5.00%` | `-5.06%p` | `-6.56%p` | 강한 약함 |
| FCX | buy | 65.15 | 66.24 | `+1.67%` | `+1.61%p` | `+0.11%p` | 양호 |
| WMT | buy | 119.78 | 120.3782 | `+0.50%` | `+0.44%p` | `-1.06%p` | 중립 양호 |
| BAC | buy | 53.83 | 55.20 | `+2.55%` | `+2.48%p` | `+0.98%p` | 양호 |

### 해석

- `BAC`는 financials diversifier 표본 중 가장 안정적이다. 1D와 5D를 합쳐도 손상보다 회복 쪽 데이터가 더 많다.
- `FCX`는 1D 약세 뒤 5D에서 회복해 `commodity diversifier` 가설을 다시 중립 이상으로 끌어올렸다.
- `JPM/SLB/WMT`는 크게 뛰어나진 않지만 보유 유지 논리와 validation hold 논리는 지켰다.
- `AAPL/AMZN/PLTR/NVDA/V`는 5D에서도 약했다. 특히 `AAPL`과 `AMZN`은 mega-cap quality label만으로 dip-buy cadence를 높이지 말아야 한다는 가설을 계속 지지한다.

## Open-position monitor

| Symbol | 현재 상태 | 해석 |
| --- | --- | --- |
| AAPL | `5주`, avg entry `303.136 USD`, current `295.5 USD`, 미실현 약 `-2.52%` | basis는 낮아졌지만 `2026-06-05 ET` add 5D가 여전히 약하다. quality averaging-down cadence는 계속 가설 단계다. |
| NOK | `402주`, avg entry `15.044527 USD`, current `14.205 USD`, 미실현 약 `-5.58%` | Yahoo narrative는 남지만 tape recovery가 불충분하다. `existing-position-breakout-add-penalty` add-block 유지가 타당하다. |
| RGTI | `49주`, avg entry `25.569583 USD`, current `20.72 USD`, 미실현 약 `-18.97%` | staged trim 이후에도 residual speculative sleeve 해석을 유지한다. add 또는 re-risk 근거는 없다. |
| AVGO | `5주`, avg entry `419.151667 USD`, current `384.25 USD`, 미실현 약 `-8.33%` | earnings beat와 analyst support는 남지만 price damage가 회복되지 않았다. staged de-risking 유지다. |

## Skipped recommendation review

| 대상 | 당시 이유 | 현재 회고 |
| --- | --- | --- |
| `2026-06-12-0431/0451` `WMT` | `review_backlog_throttle` | blocked quote가 약 `120.93/120.94`였고 현재 `120.3782`라 미집행이 기회손실로 남지 않았다. |
| `2026-06-12-0431/0451` `NEE` | `review_backlog_throttle` | blocked quote가 약 `85.27/85.29`였고 현재 `84.97`라 backlog discipline이 맞았다. |
| `2026-06-12-0611` after-hours `ADBE/PLTR/QQQ/SPY/RGTI/AVGO/SO` | stale quote, notional cap, spread, same-day sell discipline | 장외에서 신선도와 가격보호 규율을 깨지 않은 판단이 타당했다. missed setup보다 discipline 유지 가치가 크다. |

## Provider coverage와 data gaps

- Alpaca core는 current run에서 fill ledger와 latest quote 재확인에 usable이었다.
- SEC EDGAR는 `get_company_info(AVGO)`가 성공해 filing-grounded identity 확인에는 usable이었다. 다만 `get_insider_summary(AVGO,30d)`는 cancelled라 insider overlay는 불완전하다.
- Alpha Vantage는 required `TOOL_LIST -> TOOL_GET(PING)`까지는 가능했지만, 필수 경로인 `TOOL_CALL` entrypoint가 runtime에 노출되지 않았다. 이번 run은 `gap_category=wrapper_error`로 기록한다.
- `fred`와 `firecrawl`도 registered namespace가 노출되지 않아 둘 다 `gap_category=wrapper_error`다. shell/curl probe는 수행하지 않았다.
- Yahoo Finance는 `AVGO/AAPL/NOK` news와 analyst recommendation summary 보강에 usable이었다.

## 정책학습 판단

- `review_backlog_throttle`는 이번 cycle에서도 유효했다. `WMT/NEE`를 억지로 밀어넣지 않은 것이 hindsight 기준으로도 손해가 아니었다.
- `mega-cap quality averaging-down`은 `AAPL/AMZN` 5D 약세 때문에 계속 보수적으로 유지한다.
- `speculative sleeve staged de-risking`과 `post-earnings staged de-risking` 가설은 유지하지만, 이번 `AVGO/RGTI` 1D 반등 때문에 active rule 승격 임계치는 아직 아니다.

## 다음 review due

- `2026-06-11 ET` fill cohort 1D: `AVGO` trim 1주가 다음 cycle 핵심이다.
- `2026-06-10 ET` fill cohort 5D: `WMT/AVGO/RGTI/BAC/PFE/XOM/JNJ/COP/SLB/AMZN/FCX/NEE/NKE/MSFT`는 `2026-06-17 ET` regular close 이후.
- `2026-06-05 ET` fill cohort 20D와 `NOK` 20D add-block review는 계속 대기다.

## 연결 문서

- 원천 자료: [[2026-06-12-0632-analyst-review-cycle-sources]]
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-12-0632-analyst-review-cycle.json`
- 이전 회고: [[2026-06-11-portfolio-review]], [[2026-06-10-portfolio-review]], [[2026-06-09-portfolio-review]]
