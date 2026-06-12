---
id: 2026-06-13-portfolio-review
review_type: interim
reviewed_at: 2026-06-12T21:22:12Z
paper: true
decision_date: 2026-06-11/2026-06-05/2026-06-12
entry_date: multiple
exit_date: partial
---

# 2026-06-13 analyst review cycle

## 요약 판단

- 결론: `2026-06-11 ET` after-hours trim 2건(`PFE`, `AVGO`)의 1D closeout과 `2026-06-05 ET` fill cohort 13건의 5D closeout을 수행했다.
- `AVGO`의 `2026-06-11 ET` after-hours trim 1주는 `387.06 USD -> 381.95 USD`로 다음 정규장 close 기준 `-1.32%`가 나와 staged de-risking 판단을 다시 지지했다. `PFE` trim 1주는 `26.13 USD -> 26.21 USD`로 `+0.31%`라 exact timing edge는 작았다.
- `2026-06-05 ET` 5D cohort에서는 `BAC`, `FCX`, `JPM`이 가장 견조했고 `AAPL`, `PLTR`, `AMZN`은 계속 약했다. `mega-cap quality averaging-down cadence`는 여전히 active rule로 승격할 근거가 부족하다.
- open-position monitor에서는 `AAPL`, `NOK`, `RGTI`, `AVGO`를 계속 핵심으로 본다. `RGTI`는 `2026-06-12 ET` regular-session trim 12주가 새로 체결돼 첫 1D horizon이 `2026-06-15` 미국 정규장 close로 넘어간다.
- 정책 반영 여부: 없음. `portfolio_history`가 initial + 2 retries 모두 cancelled였고, `sec-edgar`도 insider summary가 cancelled로 남아 policy-book 증거 임계치를 충족하지 못했다.

## Reconciliation

| 항목 | 값 |
| --- | --- |
| Paper mode | `ALPACA_PAPER_TRADE=true` |
| Alpaca clock | `2026-06-12 17:22 ET` closed, next open `2026-06-15 09:30 ET` |
| Account status | ACTIVE |
| Portfolio value | `100,506.96 USD` |
| Cash | `31,950.36 USD` |
| Buying power | `303,033.51 USD` |
| Long market value | `68,556.60 USD` |
| Open US equity orders | 0 |
| Position count | 33 |
| Recent fill scope | `2026-06-06T00:00:00Z` 이후 direct `FILL` ledger usable |
| Portfolio history | initial + 2 retries 모두 `cancelled` |
| Orders submitted/replaced/cancelled/closed by this workflow | 0 / 0 / 0 / 0 |

## 2026-06-11 ET after-hours trim cohort 1D closeout

기준 benchmark는 Alpaca close-to-close 기준 `SPY +0.54%`, `QQQ +0.65%`다.

| Symbol | Action | Fill | 2026-06-12 close/current | 1D return | vs SPY | vs QQQ | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| PFE | sell trim 1주 | 26.13 | 26.21 | `+0.31%` | n/a | n/a | 중립 |
| AVGO | sell trim 1주 | 387.06 | 381.95 | `-1.32%` | n/a | n/a | 양호 |

### 해석

- `AVGO`는 sell 뒤 다음 정규장 close가 더 낮아져 `2026-06-11 ET` after-hours trim도 staged de-risking 맥락에서 타당했다. Alpha Vantage `EARNINGS` 기준 `2026-06-03` post-market 분기 EPS는 `2.44`, estimate `2.39`, surprise `+2.09%`였지만, 가격은 그 이후에도 recovery를 확정하지 못했다.
- `PFE`는 trim 뒤 `+0.31%` 반등이 나와 exact timing edge는 작았다. 다만 upside 규모가 작고 기존 반복 약세 review를 감안하면 trim 자체를 잘못으로 볼 수준은 아니다.

## 2026-06-05 ET fill cohort 5D closeout

기준 benchmark는 `SPY 737.45 -> 741.67`로 `+0.57%`, `QQQ 705.375 -> 721.31`로 `+2.26%`다.

| Symbol | Action | Fill | 2026-06-12 close/current | 5D return | vs SPY | vs QQQ | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| JPM | buy | 311.81 | 320.71 | `+2.85%` | `+2.28%p` | `+0.59%p` | 양호 |
| SO | buy | 93.32 | 94.015 | `+0.74%` | `+0.17%p` | `-1.52%p` | 중립 양호 |
| PFE | buy | 26.09 | 26.21 | `+0.46%` | `-0.11%p` | `-1.80%p` | 중립 |
| AMZN | buy | 253.17 | 238.56 | `-5.77%` | `-6.34%p` | `-8.03%p` | 강한 약함 |
| COP | buy | 117.42 | 116.965 | `-0.39%` | `-0.96%p` | `-2.65%p` | 중립 약함 |
| SLB | buy | 55.67 | 56.17 | `+0.90%` | `+0.33%p` | `-1.36%p` | 중립 양호 |
| NVDA | buy | 208.73 | 205.17 | `-1.71%` | `-2.28%p` | `-3.97%p` | 약함 |
| V | buy | 321.90 | 322.39 | `+0.15%` | `-0.42%p` | `-2.11%p` | 중립 |
| AAPL | buy | 313.27 | 291.085 | `-7.08%` | `-7.65%p` | `-9.34%p` | 강한 약함 |
| PLTR | buy | 138.53 | 127.98 | `-7.62%` | `-8.19%p` | `-9.87%p` | 강한 약함 |
| FCX | buy | 65.15 | 68.40 | `+4.99%` | `+4.42%p` | `+2.73%p` | 강한 양호 |
| WMT | buy | 119.78 | 121.05 | `+1.06%` | `+0.49%p` | `-1.20%p` | 중립 양호 |
| BAC | buy | 53.83 | 55.99 | `+4.01%` | `+3.44%p` | `+1.75%p` | 양호 |

### 해석

- `BAC`, `FCX`, `JPM`은 이번 cohort에서 가장 유의미한 5D follow-through를 보였다. 특히 `FCX`는 `2026-06-10 ET` 1D 강세에 이어 기존 `2026-06-05 ET` fill 5D도 강하게 닫아 materials/copper diversifier 가설을 다시 살렸다.
- `AAPL`, `PLTR`, `AMZN`은 5D에서도 계속 약했다. `AAPL`과 `AMZN`은 mega-cap quality 또는 cloud/consumer label만으로 dip-buy cadence를 높이면 안 된다는 기존 가설을 다시 지지한다.
- `SO`, `SLB`, `WMT`는 절대수익은 플러스지만 `QQQ` 반등을 이기지는 못했다. 방어/분산 후보군은 `hold-quality`와 `alpha-quality`를 계속 분리해서 봐야 한다.

## Open-position monitor

| Symbol | 현재 상태 | 해석 |
| --- | --- | --- |
| AAPL | `5주`, avg entry `303.136 USD`, current `291.37 USD`, 미실현 약 `-3.88%` | Yahoo Finance 기사에는 AI 부품비용과 pricing dilemma, WWDC 이후 제품/서비스 집중 narrative가 병존한다. 5D 약세가 더 쌓였기 때문에 `quality averaging-down cadence`는 계속 가설 단계다. |
| NOK | `402주`, avg entry `15.044527 USD`, current `14.86 USD`, 미실현 약 `-1.23%` | Yahoo Finance와 analyst action에서는 AI networking과 `2026-06-12 JP Morgan Overweight / PT 21`이 확인됐지만, current add-block은 유지한다. 다음 lifecycle review는 `2026-06-18` 미국 정규장 close다. |
| RGTI | `37주`, avg entry `25.569583 USD`, current `21.01 USD`, 미실현 약 `-17.83%` | `2026-06-12 ET` regular-session trim 12주가 `21.010833 USD`로 체결됐다. residual speculative sleeve 해석은 유지하고, 첫 1D horizon은 주말을 건너 `2026-06-15` 미국 정규장 close에 닫힌다. |
| AVGO | `4주`, avg entry `420.836 USD`, current `381.80 USD`, 미실현 약 `-9.28%` | Alpha earnings beat와 Yahoo analyst target raise 다수는 남아 있지만, price damage가 recovery를 확정하지 못했다. `core thesis 전면 폐기 아님 + staged de-risking 지속`을 유지한다. |

## Skipped recommendation review

| 대상 | 당시 이유 | 현재 회고 |
| --- | --- | --- |
| `2026-06-13-0611` after-hours `QQQ` | freshest quote `722.00/722.21`도 stale quote cap 초과 | `2026-06-12 ET` close `721.31 USD`가 stale ask 아래라 no-submit이 기회손실로 남지 않았다. |
| `2026-06-13-0611` after-hours `MSFT` | runtime quote age 약 31분 stale | `2026-06-12 ET` close/current `390.31 USD`가 stale after-hours reference `398.38 USD`보다 낮아 freshness discipline이 맞았다. |
| `2026-06-13-0451` regular-session `FCX/NEE` 신규 buy | `review_backlog_pending_1d_count=14`로 backlog throttle 활성 | hindsight상 `FCX`는 강했지만 이번 cycle에서 실제 due review를 닫아 backlog를 줄인 뒤 재평가하는 절차가 여전히 더 중요했다. `NEE`는 current `85.84 USD`로 급한 missed upside가 아니었다. |

## Provider coverage와 data gaps

- Alpaca core는 `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_account_activities`, `get_stock_bars`가 모두 usable이었다.
- Alpaca `get_portfolio_history`는 initial + 2 retries 모두 `cancelled`였다. account-level equity path와 exact portfolio MFE/MAE는 current-run gap으로 남긴다.
- Alpha Vantage는 user-required health check `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})`를 통과했고, 직후 `TOOL_GET(EARNINGS)` 다음 `TOOL_CALL(EARNINGS,{symbol:"AVGO"})`도 성공했다.
- SEC EDGAR `get_insider_summary(AVGO, 30d)`는 cancelled였다. insider overlay는 partial gap으로 남긴다.
- `fred`와 `firecrawl`은 registered callable namespace가 노출되지 않아 둘 다 `gap_category=wrapper_error`로 기록한다. shell/curl probe는 수행하지 않았다.
- Yahoo Finance는 `AVGO/AAPL/NOK/PFE` news와 `AVGO/AAPL/NOK` analyst recommendation summary 보강에 usable이었다.

## 정책학습 판단

- `staged de-risking after post-earnings price damage`는 `AVGO`에서 다시 유효했다. 하지만 단일 name 중심 반복이라 active rule 승격 근거로는 아직 부족하다.
- `mega-cap quality averaging-down`은 `AAPL`과 `AMZN`의 누적 5D 약세 때문에 계속 보수적으로 유지한다.
- `review_backlog_throttle`는 이번 cycle에서도 운영상 유효했다. 다만 `FCX`처럼 hindsight 강세 표본이 남았으므로 throttle이 selection alpha를 잃는 비용도 계속 추적해야 한다.

## 다음 review due

- `2026-06-12 ET` `RGTI` trim 12주 1D: `2026-06-15` 미국 정규장 close 이후.
- `2026-06-10 ET` fill cohort 5D: `WMT/AVGO/RGTI/BAC/PFE/XOM/JNJ/COP/SLB/AMZN/FCX/NEE/NKE/MSFT`는 `2026-06-17` 미국 정규장 close 이후.
- `2026-06-11 ET` after-hours trim cohort 5D: `PFE/AVGO`는 `2026-06-19` 미국 정규장 close 이후.
- `NOK` 20D add-block review: `2026-06-18` 미국 정규장 close 이후.

## 연결 문서

- 원천 자료: [[2026-06-13-0622-analyst-review-cycle-sources]]
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-13-0622-analyst-review-cycle.json`
- 이전 회고: [[2026-06-12-portfolio-review]], [[2026-06-11-portfolio-review]], [[2026-06-10-portfolio-review]]
