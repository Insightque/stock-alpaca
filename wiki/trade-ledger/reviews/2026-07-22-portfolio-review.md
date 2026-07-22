---
id: 2026-07-22-portfolio-review
review_type: interim
reviewed_at: 2026-07-22T21:30:00Z
paper: true
decision_date:
  - 2026-06-17
  - 2026-07-22
entry_date: multiple
exit_date: partial
---

# 2026-07-22 포트폴리오 리뷰

## 요약 판단

- 결론: 혼합. `2026-06-17 ET` buy cohort의 overdue closeout은 `AAPL/BAC/COP/MRK/XOM` 쪽이 유의미하게 살아남았지만 `FCX/GOOGL/NKE/SLB/WMT`는 benchmark 대비 뒤처졌다.
- `RGTI/PFE`의 6월 trim들은 사후 성과가 대체로 양호했다. 반면 `2026-07-22 ET` after-hours `AVGO` trim은 same-day close 대비 약 `+3.32%` rebound가 먼저 나와 exact timing은 약했다.
- `NOK`는 Alpha quarterly beat, JP Morgan 상향, 최근 `6-K` 흐름에도 불구하고 `2026-07-22 ET` close `10.30 USD`가 평균단가 `15.044527 USD`를 크게 밑돌아 add-block 유지가 타당하다.
- 정책 반영 여부: 없음. Alpaca core reconciliation은 usable했지만 `portfolio_history` surface 부재와 `fred`/`firecrawl` wrapper gap 때문에 policy-book 증거 임계치를 충족하지 못했다.

## Alpaca 정합성 점검

| 항목 | 값 |
| --- | --- |
| paper mode | `true` |
| market clock | `2026-07-22 17:21 ET`, closed |
| account status | `ACTIVE` |
| portfolio value | `98,526.58 USD` |
| cash | `29,005.42 USD` |
| buying power | `298,711.89 USD` |
| long market value | `69,521.16 USD` |
| open orders | `0` |
| positions | `31` |
| recent fills scope | `after=2026-06-17T00:00:00Z` |
| new order mutations in this workflow | `submit 0 / replace 0 / cancel 0 / close 0` |

## Due horizon 스캔

| bucket | count | 메모 |
| --- | --- | --- |
| pending 1D | `2` | `2026-07-22 ET` after-hours `AVGO/NOK` fill |
| pending 5D | `2` | 동일 `AVGO/NOK` fill의 후속 horizon |
| pending 20D | `0` | 이번 run에서 stale backlog closeout 완료 |

- `blocked_add_symbols`: `NOK`
- `due_reviews_blocking_adds`: `NOK`

## 2026-06-17 ET buy cohort overdue closeout

기준 benchmark는 Alpaca close-to-close 기준 `SPY +0.87%`, `QQQ -2.39%`다. 아래 평가는 `2026-06-17 ET` fill 대비 `2026-07-22 ET` close 기준이다.

| Symbol | Fill | 2026-07-22 close | Return | vs SPY | vs QQQ | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `AAPL` | 298.42 | 325.88 | `+9.20%` | `+8.32%p` | `+11.59%p` | 강함 |
| `AMZN` | 240.44 | 244.82 | `+1.82%` | `+0.95%p` | `+4.21%p` | 양호 |
| `BAC` | 57.57 | 61.65 | `+7.09%` | `+6.22%p` | `+9.48%p` | 강함 |
| `COP` | 110.83 | 118.83 | `+7.22%` | `+6.35%p` | `+9.61%p` | 강함 |
| `FCX` | 71.40 | 64.99 | `-8.98%` | `-9.85%p` | `-6.59%p` | 강한 약함 |
| `GOOGL` | 365.24 | 342.06 | `-6.35%` | `-7.23%p` | `-3.96%p` | 약함 |
| `MRK` | 115.19 | 127.51 | `+10.70%` | `+9.82%p` | `+13.09%p` | 강함 |
| `MSFT` | 385.40 | 390.24 | `+1.26%` | `+0.39%p` | `+3.65%p` | 중립 양호 |
| `NEE` | 86.38 | 89.43 | `+3.53%` | `+2.66%p` | `+5.92%p` | 양호 |
| `NKE` | 45.30 | 42.21 | `-6.82%` | `-7.69%p` | `-4.43%p` | 약함 |
| `NVDA` | 206.23 | 212.07 | `+2.83%` | `+1.96%p` | `+5.22%p` | 양호 |
| `SLB` | 51.32 | 47.66 | `-7.13%` | `-8.00%p` | `-4.74%p` | 약함 |
| `SO` | 93.24 | 95.79 | `+2.74%` | `+1.87%p` | `+5.13%p` | 양호 |
| `WMT` | 119.83 | 109.34 | `-8.75%` | `-9.63%p` | `-6.36%p` | 강한 약함 |
| `XOM` | 141.54 | 154.49 | `+9.15%` | `+8.28%p` | `+11.54%p` | 강함 |

### 해석

- 6월 중순 broad diversification cohort는 결과가 뚜렷하게 갈렸다. 대형 quality와 integrated energy 일부는 살아남았지만 cyclicals와 retail/consumer turnarounds는 성과가 나빴다.
- `GOOGL`은 최근 Yahoo recommendation summary가 우호적이어도 결과적으로 6월 17일 add 표본은 아직 손실 구간이다. mega-cap quality 라벨만으로 자동 정당화하지 않는다.
- `FCX`, `SLB`, `WMT`는 개별 실행 오차라기보다 sector/cluster selection 약점으로 보는 편이 맞다.

## 기존 trim/exit closeout

| Symbol | Fill | 2026-07-22 close | Post-exit move | 판단 |
| --- | ---: | ---: | ---: | --- |
| `PFE` after-hours trim | 26.03 | 24.83 | `-4.61%` | 양호 |
| `PFE` regular trim | 25.28 | 24.83 | `-1.78%` | 양호 |
| `RGTI` after-hours trim | 20.96 | 15.24 | `-27.29%` | 강한 양호 |
| `RGTI` after-hours trim 2 | 20.75 | 15.24 | `-26.55%` | 강한 양호 |
| `RGTI` regular trim | 20.56 | 15.24 | `-25.88%` | 강한 양호 |
| `AVGO` after-hours trim | 384.14 | 396.88 | `+3.32%` | timing 약함, staged de-risking은 유지 |
| `NOK` after-hours trim | 10.33 | 10.30 | `-0.29%` | neutral, `1D` 대기 |

## 2026-07-22 ET 신규 fill review 상태

- `AVGO` 1주 after-hours trim은 fill 후 same-day close가 더 높아 exact timing은 불리했다. 다만 잔여 포지션이 이미 정리된 상태라 이번 표본은 `post-earnings staged de-risking`의 마지막 tail risk 축소로 해석한다.
- `NOK` 1주 after-hours trim은 fill과 same-day close 차이가 거의 없었다. `1D` horizon은 `2026-07-23 ET` close 이후 판단한다.

## Open-position monitor

| symbol | qty | avg | 2026-07-22 close/current | unrealized | 메모 |
| --- | ---: | ---: | --- | --- | --- |
| `NOK` | 401 | `15.044527` | `10.30 / 10.66` | 약 `-29.14%` | add-block 유지. analyst 우호 신호보다 tape 약세가 우선이다. |
| `IONQ` | 45 | `63.48` | `34.685 / 34.78` | 약 `-45.21%` | speculative sleeve no-add discipline 유지. |
| `GOOGL` | 5 | `376.204` | `342.06 / 326.67` | 약 `-13.17%` | recent street support에도 후속 약세. size 확대 근거 없음. |
| `SLB` | 8 | `55.0625` | `47.66 / 47.78` | 약 `-13.23%` | energy sleeve 선택 약점 점검 필요. |
| `AMD` | 14 | `462.73` | `552.37 / 552.76` | 약 `+19.46%` | winning concentration이 일부 손실 sleeve를 상쇄 중이다. |

## Skipped recommendation 재점검

| symbol | 현재 해석 | 결론 |
| --- | --- | --- |
| `NOK` | Alpha latest quarter beat, JP Morgan 상향, recent `6-K` 연속성에도 price confirmation이 없다. | skip/add-block 유지 |
| `IONQ` | Yahoo recommendation summary `3개월` window에 의미 있는 새 analyst row가 없고 drawdown이 깊다. | no-add 유지 |
| `GOOGL` | quality label은 유지되지만 최근 add 표본이 손실이라 추가 확신 근거가 부족하다. | immediate add 보류 |

## MCP 커버리지와 데이터 갭

- `alpaca`: usable. account, orders, fills, positions, bars, snapshots, news reconciliation 수행.
- `sec-edgar`: usable. `NOK`, `AVGO` recent filings continuity 확인.
- `alpha-vantage`: usable. required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check 통과 후 `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:"NOK"})` 성공.
- `yahoo-finance`: usable. `NOK/AVGO/GOOGL/IONQ` recommendation summary 확인.
- `fred`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `firecrawl`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `alpaca portfolio_history`: current tool surface 미노출로 account curve 기반 후행 attribution은 보강하지 못했다.

## 정책 학습

- `NOK` add-block 유지 사례는 또 한 번 맞았지만 단일 장기 패자 포지션 사례라 일반 규칙 강화까지는 부족하다.
- `RGTI/PFE` trim 성과는 좋았고 `AVGO` trim timing은 약했다. 결국 trim 정책은 "빠른 exact top pick"보다 "포지션 위험 축소" 성격으로 보는 편이 더 정확하다.
- 이번 run만으로 `wiki/policy-book/recommendation-policy.md`를 수정하지 않는다.

## 다음 due 일정

- `2026-07-23 ET` close: `AVGO`, `NOK` `1D`
- `2026-07-29 ET` close: `AVGO`, `NOK` `5D`
- `NOK`, `IONQ`, `GOOGL`: material drawdown open-position monitor 지속

## 참조

- [[2026-07-22-analyst-review-cycle-sources]]
- `wiki/evidence-store/run-manifests/2026-07-22-analyst-review-cycle.json`
