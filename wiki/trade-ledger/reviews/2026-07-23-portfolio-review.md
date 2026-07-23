---
id: 2026-07-23-portfolio-review
review_type: interim
reviewed_at: 2026-07-23T21:23:54Z
paper: true
decision_date:
  - 2026-07-22
  - 2026-07-23
---

# 2026-07-23 포트폴리오 리뷰

## 요약 판단

- 이번 scheduled analyst review cycle은 `Thursday, July 23, 2026 ET` 정규장 종가 기준 `AVGO` residual after-hours trim `1D`와 `NOK` after-hours trim `1D` closeout을 완료했다.
- `AVGO` trim은 tail-risk 축소 의도 자체는 유지되지만 exact timing은 여전히 약했다. 반대로 `NOK` trim은 같은 날 실적 beat와 AI/클라우드 수요 headline에도 불구하고 주가가 더 밀려 방어적 timing이 유효했다.
- 오픈 포지션과 skipped recommendation 재점검 결과 `NOK` add-block, `IONQ` no-add, `GOOGL` immediate add 보류를 유지한다.
- 정책 반영 여부: 없음. `fred`/`firecrawl` wrapper gap이 계속됐고 `sec-edgar` 및 Alpaca 일부 surface cancellation이 남아 evidence threshold를 충족하지 못했다.

## Alpaca 정합성 점검

| 항목 | 값 |
| --- | --- |
| paper mode | `true` |
| market clock | `2026-07-23 17:22 ET`, closed |
| account status | `ACTIVE` |
| portfolio value | `97,620.71 USD` |
| cash | `29,027.15 USD` |
| buying power | `29,027.15 USD` |
| long market value | `68,593.56 USD` |
| open orders | `0` |
| positions | `31` |
| watchlists | `0` |
| recent fills scope | `after=2026-07-22T20:00:00Z` |
| portfolio history | `cancelled` x3 |
| order mutations in this workflow | `submit 0 / replace 0 / cancel 0 / close 0` |

## Due horizon 스캔

| bucket | count | 메모 |
| --- | --- | --- |
| pending 1D | `0` | `AVGO/NOK` 1D closeout 완료 |
| pending 5D | `2` | `AVGO`, `NOK` |
| pending 20D | `0` | 신규 due 없음 |

- `blocked_add_symbols`: `NOK`
- `due_reviews_blocking_adds`: `NOK`

## 2026-07-22 ET after-hours trim 1D closeout

| symbol | action | fill | 2026-07-23 close | return | benchmark 비교 | 판단 |
| --- | --- | --- | --- | --- | --- | --- |
| `AVGO` | trim sell `1` | `384.14` | `392.61` | `+2.20%` | `SPY -1.26%`, `QQQ -1.87%`, `SMH -1.12%` 대비 상대강도는 강하지만 trim 뒤 주가가 더 높게 마감 | trim timing 약함 |
| `NOK` | trim sell `2` | `10.95`, `10.78` | `9.72` | 평균 `-10.53%` | `SPY -1.26%`, `QQQ -1.87%` 대비 크게 약세 | trim timing 강한 양호 |

### 해석

- `AVGO`는 `2026-07-22 ET` same-day close `396.88 USD` 대비 `2026-07-23 ET` close `392.61 USD`로 rebound 일부가 식었지만, trim fill `384.14 USD`보다 여전히 높다. 따라서 이번 `1D`만 놓고 보면 tail-risk closeout 의도는 이해되더라도 exact top-tick 성격과는 거리가 있다.
- `NOK`는 Alpha Vantage `EARNINGS` 기준 `reportedDate=2026-07-23`, `reportedEPS=0.0799`, `estimatedEPS=0.07`, `surprisePercentage=14.1429`, `reportTime=pre-market`였다. Yahoo Finance 뉴스도 `2026-07-23` AI/data-center demand 기반 실적 beat를 확인했지만, 종가는 `9.72 USD`로 더 밀렸다. 결과적으로 trim은 price-first discipline 측면에서 타당했다.

## Open-position monitor

| symbol | qty | avg | 2026-07-23 close/current | unrealized | 메모 |
| --- | ---: | ---: | --- | --- | --- |
| `NOK` | 399 | `15.044539` | `9.72 / 9.78` | 약 `-35.39%` | 실적 beat와 JP Morgan `2026-06-12 Overweight / PT 21`에도 tape가 더 약해졌다. add-block 유지가 타당하다. |
| `IONQ` | 45 | `63.48` | `34.26 / 34.26` | 약 `-46.03%` | Yahoo recommendation summary `3개월` window 신규 row 공백과 깊은 drawdown이 함께 남아 있어 speculative no-add 유지다. |
| `GOOGL` | 5 | `376.204` | `318.80 / 318.80` | 약 `-15.26%` | quality label은 남지만 `2026-07-23 ET` 하루 낙폭이 커져 immediate add 근거가 약해졌다. |
| `AMD` | 14 | `462.73` | `547.9204 / 547.9204` | 약 `+18.41%` | winning concentration이 손실 sleeve를 상쇄 중이다. 개별 승자 사례만으로 losers averaging-down 완화를 정당화하지 않는다. |

## Skipped recommendation 재점검

| symbol | 현재 해석 | 결론 |
| --- | --- | --- |
| `NOK` | 실적 beat, AI/클라우드 수요 headline, 기존 JP Morgan 상향이 모두 남아도 주가는 `2026-07-23 ET`에 `-5.44%` 하락했다. | skip/add-block 유지 |
| `IONQ` | analyst summary 공백과 깊은 drawdown이 동시에 남아 있다. | no-add 유지 |
| `GOOGL` | quality/scale thesis는 유지되지만 최근 add cohort 손실과 `2026-07-23 ET` 급락을 감안하면 추가 확신이 부족하다. | immediate add 보류 |

## MCP 커버리지와 데이터 갭

- `alpaca`: usable. `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, `get_stock_snapshot`으로 account/order/fill/position/market-data reconciliation을 닫았다.
- `alpaca portfolio_history`: `gap_category=cancelled`, `retry_count=2`. `get_portfolio_history` 3회 호출 모두 cancelled였다.
- `alpaca get_order_by_client_id(ah-20260722-0911-sell-avgo-01)`: `gap_category=cancelled`, `retry_count=2`. direct order readback은 cancelled였지만 `[[2026-07-22-1051-after-hours-autopilot]]`와 기존 review artifact의 filled ledger로 AVGO fill을 교차 확인했다.
- `sec-edgar`: `gap_category=cancelled`, `retry_count=1`. `get_insider_summary(NOK, 60d)` 2회 모두 cancelled라 이번 run의 SEC 보강은 직전 artifact continuity에 의존했다.
- `alpha-vantage`: usable. required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check 통과 후 `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:"NOK"})` 성공.
- `yahoo-finance`: usable. `NOK`, `AVGO` recommendation summary와 news 보강을 반영했다.
- `fred`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `firecrawl`: `gap_category=wrapper_error`. registered callable tool surface 미노출.

## 정책 학습

- `NOK`는 좋은 headline과 EPS beat가 있어도 price confirmation이 없으면 add-block을 유지해야 한다는 기존 해석을 다시 지지했다. 다만 동일 포지션의 반복 표본이라 새 일반 규칙으로 승격하지는 않는다.
- `AVGO`는 trim 이후 relative performance가 지수와 섹터 ETF보다 강했음에도 fill 대비 다음 종가가 더 높았다. staged de-risking은 계속 risk-reduction 도구로 보되, exact timing 기대를 policy-book 규칙처럼 강화할 근거는 아직 부족하다.
- 이번 cycle만으로 `wiki/policy-book/recommendation-policy.md`를 수정하지 않는다.

## 다음 due 일정

- `2026-07-29 ET` close: `AVGO`, `NOK` `5D`
- `NOK`, `IONQ`, `GOOGL`: material drawdown open-position monitor 지속

## 참조

- [[2026-07-23-analyst-review-cycle-sources]]
- `wiki/evidence-store/run-manifests/2026-07-23-analyst-review-cycle.json`
