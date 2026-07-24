---
id: 2026-07-24-portfolio-review
review_type: interim
reviewed_at: 2026-07-24T21:25:08Z
paper: true
decision_date:
  - 2026-07-23
  - 2026-07-24
---

# 2026-07-24 포트폴리오 리뷰

## 요약 판단

- 이번 scheduled analyst review cycle은 `Friday, July 24, 2026 ET` 정규장 종가 기준으로 `NOK` after-hours trim fill `1D 대기`를 등록하고, `NOK/IONQ/GOOGL` 중심 open-position monitor와 skipped recommendation 재점검을 수행했다.
- `NOK`의 새 trim `1주 @ 9.67 USD`는 same-day close `9.07 USD` 기준으로는 방어적으로 맞았지만, 이는 `1D` closeout이 아니라 같은 거래일 후행 mark다. 최종 평가는 `Monday, July 27, 2026 ET` 정규장 종가 이후로 넘긴다.
- `NOK` add-block, `IONQ` no-add, `GOOGL` immediate add 보류를 유지한다.
- 정책 반영 여부: 없음. Alpaca `portfolio_history`가 3회 연속 cancelled였고, `sec-edgar`는 두 번 모두 cancelled, `yahoo-finance`는 `NOK/IONQ/GOOGL` 조회가 timeout이라 evidence threshold를 충족하지 못했다.

## Alpaca 정합성 점검

| 항목 | 값 |
| --- | --- |
| paper mode | `true` |
| market clock | `2026-07-24 17:21 ET`, closed |
| account status | `ACTIVE` |
| portfolio value | `96,255.96 USD` |
| cash | `29,036.78 USD` |
| buying power | `294,264.37 USD` |
| long market value | `67,219.18 USD` |
| open orders | `0` |
| positions | `31` |
| watchlists | `0` |
| recent fills scope | `after=2026-07-23T20:00:00Z` |
| portfolio history | `cancelled` x3 |
| order mutations in this workflow | `submit 0 / replace 0 / cancel 0 / close 0` |

## Due horizon 스캔

| bucket | count | 메모 |
| --- | --- | --- |
| pending 1D | `1` | `NOK` `2026-07-24 ET` fill `1주 @ 9.67` |
| pending 5D | `3` | `AVGO`, `NOK` `2026-07-22 ET` trim cohort + `NOK` `2026-07-24 ET` trim |
| pending 20D | `1` | `NOK` `2026-07-24 ET` trim |

- `blocked_add_symbols`: `NOK`
- `due_reviews_blocking_adds`: `NOK`

## 2026-07-24 ET 신규 fill lifecycle 등록

| symbol | action | fill | same-day close | same-day move | review status |
| --- | --- | --- | --- | --- | --- |
| `NOK` | trim sell `1` | `9.67` | `9.07` | `-6.20%` | `1D 대기` |

### 해석

- 이 fill은 `client_order_id=ah-20260723-2151-sell-nok-01`로 `2026-07-24T13:17:49.876154Z`에 체결됐다.
- `2026-07-24 ET` close `9.07 USD`는 fill 대비 더 낮아 same-day 방어 결과는 양호했다.
- 다만 workflow 기준 `1D/5D/20D` 평가는 다음 정규장 close 단위로 닫아야 하므로, 이 결과를 최종 `1D` 판단으로 승격하지 않는다.

## Open-position monitor

| symbol | qty | avg | 2026-07-24 close/current | unrealized | 메모 |
| --- | ---: | ---: | --- | --- | --- |
| `NOK` | 398 | `15.044561` | `9.07 / 9.06` | 약 `-39.78%` | `2026-07-23` quarterly miss 이후 tape 약세가 더 깊어졌다. add-block 유지가 타당하다. |
| `IONQ` | 45 | `63.48` | `33.16 / 33.16` | 약 `-47.76%` | speculative sleeve no-add 유지. 새 analyst/recommendation 보강은 이번 run에서 Yahoo timeout으로 미확인이다. |
| `GOOGL` | 5 | `376.204` | `319.66 / 319.66` | 약 `-15.03%` | quality label은 유지되지만 recent add cohort 손실이 지속돼 immediate add 근거가 약하다. |
| `AMD` | 14 | `462.73` | `522.35 / 522.35` | 약 `+12.88%` | winning concentration은 유지되지만 losers averaging-down 완화를 정당화하지 않는다. |

## Skipped recommendation 재점검

| symbol | 현재 해석 | 결론 |
| --- | --- | --- |
| `NOK` | Alpha Vantage `2026-07-23` quarterly row는 `reportedEPS=0.05`, `estimatedEPS=0.07`, `surprisePercentage=-28.5714`, `reportTime=pre-market`였다. earnings miss와 약한 tape가 같이 남아 있다. | skip/add-block 유지 |
| `IONQ` | deep drawdown은 지속되는데 이번 run의 Yahoo recommendation query가 timeout이라 새 외부 확인을 보강하지 못했다. | no-add 유지 |
| `GOOGL` | current loss와 최근 add cohort 약세가 지속된다. 이번 run의 Yahoo recommendation query도 timeout이라 street support refresh를 확인하지 못했다. | immediate add 보류 |

## Benchmark 및 계좌 맥락

- `SPY`: `2026-07-23 ET` close `738.06` -> `2026-07-24 ET` close `738.90`, `+0.11%`
- `QQQ`: `2026-07-23 ET` close `691.98` -> `2026-07-24 ET` close `684.33`, `-1.11%`
- 계좌 equity는 `last_equity 97,419.55 USD`에서 `96,255.96 USD`로 `-1,163.59 USD`, 약 `-1.19%` 감소했다.
- 다만 `get_portfolio_history`가 3회 연속 cancelled라 계좌 단위 MFE/MAE나 curve attribution은 이번 run에서 보강하지 못했다.

## MCP 커버리지와 데이터 갭

- `alpaca`: usable. `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, `get_stock_snapshot`으로 account/order/fill/position/market-data reconciliation을 닫았다.
- `alpaca portfolio_history`: `gap_category=cancelled`, `retry_count=2`. initial call과 2회 retry가 모두 cancelled였다.
- `sec-edgar`: `gap_category=cancelled`, `retry_count=1`. callable surface 재시도까지 모두 cancelled라 이번 run의 filing-grounded 보강은 prior ticker notes continuity에 의존했다.
- `alpha-vantage`: usable. required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check 통과 후 `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:"NOK"})` 성공.
- `fred`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `firecrawl`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `yahoo-finance`: `gap_category=timeout`. `NOK` news, `NOK/IONQ/GOOGL` recommendation queries가 모두 `curl (28)` timeout으로 종료됐다.

## 정책 학습

- `NOK`는 좋은 headline이 아니라도, 혹은 반대로 기존 우호 narrative가 남아 있더라도, quarterly miss와 약한 tape가 겹치면 add-block을 유지해야 한다는 기존 원칙을 다시 지지했다.
- 하지만 이번 run의 신규 fill은 아직 same-day mark뿐이고, `portfolio_history`와 Yahoo 보강도 불완전하므로 `wiki/policy-book/recommendation-policy.md`를 수정할 근거는 아니다.

## 다음 due 일정

- `Monday, July 27, 2026 ET` close: `NOK` `1D`
- `Tuesday, July 29, 2026 ET` close: `AVGO`, `NOK` `5D` (`2026-07-22 ET` trim cohort)
- `Thursday, July 31, 2026 ET` close: `NOK` `5D` (`2026-07-24 ET` trim)
- `Friday, August 21, 2026 ET` close: `NOK` `20D` (`2026-07-24 ET` trim)

## 참조

- [[2026-07-24-analyst-review-cycle-sources]]
- `wiki/evidence-store/run-manifests/2026-07-24-analyst-review-cycle.json`
