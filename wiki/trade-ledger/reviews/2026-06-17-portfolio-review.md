---
id: 2026-06-17-portfolio-review
review_type: interim
reviewed_at: 2026-06-16T21:23:55Z
paper: true
decision_date:
  - 2026-06-15
  - 2026-06-16
---

# 2026-06-17 포트폴리오 리뷰

## 요약

- 이번 scheduled analyst review cycle은 `2026-06-15 ET` regular fill cohort `18건`의 `1D` closeout을 완료했다.
- `pending_1d_count`는 `18 -> 0`으로 내려 backlog stop을 해소했고, 이 cohort는 전부 `5D` 대기열로 승격해 `pending_5d_count`가 `19 -> 37`로 늘었다.
- `5D`와 `20D`는 오늘 새 closeout이 없었다. `2026-06-17 ET` close `14건`, `2026-06-18 ET` close `NOK 20D`, `2026-06-19 ET` close `2건`이 다음 due다.
- `portfolio_history`는 3회 연속 cancelled였고 `fred/firecrawl`은 wrapper gap, `alpha-vantage`는 health check 후 provider-rate-limit gap이었지만, 정책 변경 근거 임계치는 여전히 충족하지 못했다.

## Alpaca 정합성 점검

| 항목 | 값 |
| --- | --- |
| paper mode | `true` |
| market clock | `2026-06-16 17:22 ET`, closed |
| account status | `ACTIVE` |
| portfolio value | `100,693.70 USD` |
| cash | `30,344.81 USD` |
| buying power | `302,530.20 USD` |
| long market value | `70,348.89 USD` |
| open orders | `0` |
| positions | `33` |
| watchlists | `0` |
| fills scope | `after=2026-06-10T00:00:00Z` |
| new fills since prior cycle | `21건` |
| portfolio history | `cancelled` x3 |
| order mutations in this workflow | `submit 0 / replace 0 / cancel 0 / close 0` |

## Due horizon 스캔

| bucket | count | 메모 |
| --- | --- | --- |
| pending 1D | `0` | 오늘 due `18건` closeout 완료 |
| pending 5D | `37` | 기존 `19건` + 오늘 closeout `18건` 승격 |
| pending 20D | `1` | `NOK` add-block 검증 유지 |

- `blocked_add_symbols`: `NOK`
- `due_reviews_blocking_adds`: `NOK`
- 오늘 기준 새 `5D/20D` closeout은 없다. 단, due queue는 다음 regular close로 유지한다.

## 2026-06-15 ET fill cohort 1D closeout

| symbol | action | fill | 2026-06-16 close | return | benchmark 비교 | 판단 |
| --- | --- | --- | --- | --- | --- | --- |
| `RGTI` | trim sell 9 | `23.366667` | `20.63` | `-11.71%` | `SPY -0.55%`, `QQQ -1.87%`보다 더 크게 하락 | trim timing 양호 |
| `BAC` | buy 1 | `56.28` | `56.85` | `+1.01%` | 양 지수 대비 초과 | 양호 |
| `WMT` | buy 1 | `120.20` | `121.07` | `+0.72%` | 양 지수 대비 초과 | 양호 |
| `AVGO` | trim sell 1 | `392.14` | `376.53` | `-3.98%` | sell 뒤 추가 하락 | trim timing 양호 |
| `NEE` | buy 1 | `85.78` | `86.24` | `+0.54%` | 양 지수 대비 초과 | 중립 양호 |
| `JPM` | buy 1 | `321.53` | `331.14` | `+2.99%` | 양 지수 대비 강함 | 강함 |
| `FCX` | buy 1 | `69.49` | `70.155` | `+0.96%` | 양 지수 대비 초과 | 양호 |
| `SLB` | buy 1 | `54.03` | `53.085` | `-1.75%` | `QQQ`보단 양호, `SPY`보단 약함 | 중립 약함 |
| `XOM` | buy 1 | `141.76` | `141.875` | `+0.08%` | 양 지수 대비 방어 | 중립 양호 |
| `NKE` | buy 1 | `45.36` | `45.04` | `-0.71%` | `QQQ`보단 양호, `SPY`와 유사 | 중립 |
| `COP` | buy 1 | `112.62` | `111.33` | `-1.15%` | `QQQ`보단 양호, `SPY`보단 약함 | 중립 약함 |
| `V` | buy 1 | `324.83` | `333.21` | `+2.58%` | 양 지수 대비 강함 | 강함 |
| `SO` | buy 1 | `94.37` | `94.305` | `-0.07%` | 양 지수 대비 방어 | 중립 양호 |
| `MSFT` | buy 1 | `398.71` | `393.97` | `-1.19%` | `QQQ`보단 양호, `SPY`보단 약함 | 중립 약함 |
| `GOOGL` | buy 1 | `371.22` | `373.37` | `+0.58%` | 양 지수 대비 초과 | 양호 |
| `AMZN` | buy 1 | `246.19` | `246.15` | `-0.02%` | 양 지수 대비 방어 | 중립 양호 |
| `AAPL` | buy 1 | `296.11` | `299.26` | `+1.06%` | 양 지수 대비 초과 | 양호 |
| `PFE` | trim sell 1 | `26.01` | `26.05` | `+0.15%` | trim 뒤 소폭 반등 | trim timing 약함 |

## Open-position monitor

| symbol | qty | avg | 2026-06-16 close | unrealized | 메모 |
| --- | --- | --- | --- | --- | --- |
| `AAPL` | 6 | `301.965` | `299.26` | `-0.90%` | 최신 add 1D는 양호했지만 mega-cap averaging-down을 다시 공격적으로 확대할 증거는 아직 부족하다. |
| `AVGO` | 1 | `435.995` | `376.53` | `-13.64%` | staged de-risking은 계속 유효하다. 최근 trim timing은 개선됐지만 잔여 포지션 recovery confirmation은 아직 없다. |
| `NOK` | 402 | `15.044527` | `13.975` | `-7.11%` | JP Morgan `Overweight/PT 21`는 우호적이지만 가격 구조가 다시 약해져 `2026-06-18 ET` 20D add-block review 전 해제 근거가 없다. |
| `RGTI` | 28 | `25.569583` | `20.63` | `-19.32%` | 큰 하락폭 때문에 speculative sleeve trim은 hindsight상 유효했다. 다만 residual sleeve 변동성은 여전히 높다. |
| `FCX` | 6 | `65.675` | `70.155` | `+6.82%` | materials/copper diversifier 가설은 유지된다. backlog-throttle가 풀린 뒤에도 chase 완화 규율은 그대로 필요하다. |

## Skipped recommendation 재점검

| symbol | 현재 해석 | 결론 |
| --- | --- | --- |
| `FCX` | 구리/소재 강세는 여전히 유효하고 hindsight상 missed-upside 사례가 남아 있다. | backlog-throttle을 완화할 단독 근거로는 아직 부족하다. 다만 backlog 자체가 오늘 해소됐으므로 다음 buy review에서는 구조적으로 더 공정한 재평가가 가능하다. |
| `WMT` | consumer defensive tape는 완만하게 우상향했지만 과열 없이 움직였다. | 기존 skip을 policy miss로 일반화하지 않는다. |
| `NEE` | defensive utility 성격에 맞는 작은 우상향만 확인됐다. | backlog-throttle 우선순위를 뒤집을 정도의 missed-upside는 아니다. |

## MCP 커버리지와 데이터 갭

- `alpaca`: usable. account/orders/positions/activities/snapshots reconciliation 완료.
- `sec-edgar`: usable. `AVGO`, `AAPL`, `NOK` recent filings 확인.
- `alpha-vantage`: `gap_category=provider_error`. required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check는 통과했지만, 직후 `TOOL_GET(EARNINGS)` 및 `TOOL_CALL(EARNINGS,{symbol:AAPL})`는 daily-rate-limit payload로 종료됐다.
- `yahoo-finance`: usable. `FCX` 뉴스, `WMT` 뉴스, `NOK` upgrades/downgrades summary 확인.
- `fred`: `gap_category=wrapper_error`. 등록된 callable tool surface 미노출.
- `firecrawl`: `gap_category=wrapper_error`. 등록된 callable tool surface 미노출.
- `alpaca portfolio_history`: `gap_category=cancelled`, `retry_count=2`. 동일 호출 3회 모두 취소.

## 정책 학습

- 오늘 closeout은 `RGTI/AVGO` trim timing 개선, `JPM/V/BAC/AAPL/WMT` 1D 양호, `PFE` trim timing 약함 정도의 혼합 신호를 남겼다.
- 그러나 동일 패턴이 policy-book의 evidence threshold를 넘을 정도로 반복 축적되지는 않았다.
- 따라서 `wiki/policy-book/recommendation-policy.md`는 수정하지 않는다.

## 다음 due 일정

- `2026-06-17 ET` close: 기존 `5D` due `14건`
- `2026-06-18 ET` close: `NOK` `20D` add-block review
- `2026-06-19 ET` close: `PFE`, `AVGO` after-hours trim `5D`
- `2026-06-22 ET` close: 오늘 closeout한 `2026-06-15 ET` fill cohort `18건`의 `5D`와 기존 `RGTI/AVGO/MSFT` `5D`

## 참조

- [[2026-06-17-0623-analyst-review-cycle-sources]]
- `wiki/evidence-store/run-manifests/2026-06-17-0623-analyst-review-cycle.json`
