---
id: 2026-08-10-portfolio-review
review_type: interim
reviewed_at: 2026-08-10T23:24:00Z
paper: true
decision_date:
  - 2026-07-22
  - 2026-07-24
  - 2026-08-10
---

# 2026-08-10 포트폴리오 리뷰

## 요약 판단

- 이번 scheduled analyst review cycle은 `Monday, August 10, 2026 ET` 정규장 종가 기준으로 `AVGO` `2026-07-22 ET` trim cohort `5D`, `NOK` `2026-07-22 ET` trim cohort `5D`, `NOK` `2026-07-24 ET` trim `1D/5D` closeout을 완료했다.
- `NOK` trim들은 `1D/5D` 모두 방어적으로 맞았고, 기존 add-block 유지 판단을 다시 지지했다. `AVGO` residual trim은 `1D`에서는 timing이 약했지만 `5D`에는 fill 이후 주가가 더 낮아져 `tail-risk 축소` 관점에서는 `중립 양호`로 정리한다.
- 오픈 포지션 재점검에서는 `NOK` add-block, `IONQ` no-add, `GOOGL` immediate add 보류를 유지한다. `WMT/MCD`의 2026-07-24 after-hours skip은 이후 수익이 아주 크지 않아 policy miss로 승격하지 않는다.
- 정책 반영 여부: 없음. 오늘 run은 Alpaca 코어와 기존 위키 증거로는 충분히 truthfully closeout할 수 있었지만, `sec-edgar`, `alpha-vantage`, `fred`, `firecrawl`, `yahoo-finance` registered Codex MCP tool surface가 현재 세션에 노출되지 않아 독립 cross-provider evidence threshold를 충족하지 못했다.

## Alpaca 정합성 점검

| 항목 | 값 |
| --- | --- |
| paper mode | `true` |
| market clock | `2026-08-10 19:21 ET`, closed |
| next open | `2026-08-11 09:30 ET` |
| account status | `ACTIVE` |
| portfolio value | `98,640.81 USD` |
| cash | `29,036.76 USD` |
| buying power | `300,863.91 USD` |
| long market value | `69,604.05 USD` |
| open orders | `0` |
| positions | `31` |
| watchlists | `0` |
| recent fills scope | `after=2026-07-22T00:00:00Z` |
| portfolio history | `cancelled` x3 |
| order mutations in this workflow | `submit 0 / replace 0 / cancel 0 / close 0` |

## Due horizon 스캔

| bucket | count | 메모 |
| --- | ---: | --- |
| pending 1D | `0` | due closeout 없음 |
| pending 5D | `0` | due closeout 없음 |
| pending 20D | `1` | `NOK` `2026-07-24 ET` trim |

- `blocked_add_symbols`: `NOK`
- `due_reviews_blocking_adds`: `NOK`

## Due horizon closeout

| symbol | cohort | action | fill | closeout close | return | benchmark 비교 | 판단 |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `AVGO` | `2026-07-22 ET` `5D` | trim sell `1` | `384.14` | `370.33` (`2026-07-29 ET`) | `-3.59%` | `SPY -2.40%`, `QQQ -6.18%`, `SMH -14.17%` | 중립 양호 |
| `NOK` | `2026-07-22 ET` `5D` | trim sell `2` | `10.95`, `10.78` | `8.40` (`2026-07-29 ET`) | 평균 `-22.69%` | `SPY -2.40%`, `QQQ -6.18%` 대비 큰 약세 | 양호 |
| `NOK` | `2026-07-24 ET` `1D` | trim sell `1` | `9.67` | `9.27` (`2026-07-27 ET`) | `-4.14%` | `SPY -0.01%`, `QQQ -0.32%` 대비 약세 | 양호 |
| `NOK` | `2026-07-24 ET` `5D` | trim sell `1` | `9.67` | `9.10` (`2026-07-31 ET`) | `-5.89%` | `SPY +1.07%`, `QQQ +0.52%` 대비 큰 약세 | 양호 |

### 해석

- `AVGO`는 `1D` review에서 exact timing이 약했지만, `5D` close `370.33 USD`는 fill `384.14 USD`보다 낮다. 결과적으로 residual 1주 tail-risk를 줄인 판단은 `완전히 이른 매도`라기보다 `늦지 않은 de-risking`에 가까웠다.
- 다만 `AVGO`의 `5D` 하락폭은 `SMH`보다 훨씬 작았다. 즉, 종목 자체의 상대강도는 남아 있었고 이번 한 건만으로 aggressive trim 규칙을 강화할 근거는 아니다.
- `NOK`는 `2026-07-22 ET` trim cohort와 `2026-07-24 ET` trim 모두 후행 `1D/5D`에서 더 낮은 가격이 확인됐다. earnings headline이나 prior bullish narrative보다 price-first discipline이 우선해야 한다는 해석을 다시 지지한다.

## Open-position monitor

| symbol | qty | avg | 2026-08-10 close/current | unrealized | 메모 |
| --- | ---: | ---: | --- | --- | --- |
| `NOK` | 398 | `15.044573` | `9.12 / 9.12` | 약 `-39.38%` | 7월 trim 판단은 맞았지만 잔여 포지션은 아직 깊은 손실 구간이다. add-block 유지가 타당하다. |
| `IONQ` | 45 | `63.48` | `42.51 / 42.54` | 약 `-33.03%` | 8월 실적 beat와 가이던스 상향으로 반등했지만 basis recovery가 멀다. speculative no-add 유지다. |
| `GOOGL` | 5 | `376.204` | `357.545 / 357.03` | 약 `-4.96%` | 7월 저점 대비 회복은 컸지만 recent add cohort의 손실을 완전히 해소하진 못했다. immediate add 보류를 유지한다. |
| `AMD` | 14 | `462.73` | `469.67 / 469.67` | 약 `+1.50%` | winner가 남아 있어도 losers averaging-down 완화 근거로 일반화하지 않는다. |

## Skipped recommendation 재점검

| symbol | 현재 해석 | 결론 |
| --- | --- | --- |
| `NOK` | 7월 trim closeout이 모두 양호했고 현재가도 `9.12 USD`로 낮다. | skip/add-block 유지 |
| `IONQ` | 8월 실적 beat와 DARPA headline 이후 `42.51 USD`까지 회복했지만 여전히 평균단가를 크게 밑돈다. | no-add 유지 |
| `GOOGL` | AI leadership exit headline 이후 흔들렸지만 8월 초 강하게 회복했다. 다만 quality thesis refresh를 외부 MCP로 검증하지 못해 immediate add는 보류한다. | immediate add 보류 |
| `WMT` | `2026-07-24 ET` close `109.46`에서 `2026-08-10 ET` close `112.67`로 `+2.93%`였다. | gate-correct skip, policy miss 아님 |
| `MCD` | `2026-07-24 ET` close `264.715`에서 `2026-08-10 ET` close `273.675`로 `+3.39%`였다. | gate-correct skip, policy miss 아님 |

## Benchmark 및 계좌 맥락

- `SPY`: `2026-07-24 ET` close `738.90` -> `2026-08-10 ET` close `773.02`, `+4.62%`
- `QQQ`: `2026-07-24 ET` close `684.33` -> `2026-08-10 ET` close `720.805`, `+5.33%`
- `SMH`: `2026-07-24 ET` close `561.22` -> `2026-08-10 ET` close `569.46`, `+1.47%`
- account equity는 Alpaca `last_equity 99,181.77 USD` 대비 `98,640.81 USD`로 `-540.96 USD`, 약 `-0.55%`다.
- 다만 `get_portfolio_history`가 initial call과 2회 retry 모두 cancelled여서 curve attribution과 account-level MFE/MAE는 이번 run에서도 보강하지 못했다.

## MCP 커버리지와 데이터 갭

- `alpaca`: usable. `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_all_positions`, `get_watchlists`, `get_stock_bars`, `get_stock_snapshot`, `get_news`로 account/order/fill/position/benchmark/news reconciliation을 닫았다.
- `alpaca portfolio_history`: `gap_category=cancelled`, `retry_count=2`. initial call과 2회 retry가 모두 cancelled였다.
- `sec-edgar`: `gap_category=wrapper_error`. registered Codex MCP tool surface를 discovery했지만 callable namespace가 현재 세션에 노출되지 않았다.
- `alpha-vantage`: `gap_category=wrapper_error`. required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check를 수행해야 하지만 해당 surface가 현재 세션에 노출되지 않아 실행할 수 없었다.
- `fred`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `firecrawl`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `yahoo-finance`: `gap_category=wrapper_error`. registered callable tool surface 미노출.

## 정책 학습

- `NOK`는 7월 말 trim 표본이 독립적으로 3개 더 쌓였고 모두 후행 가격이 더 낮았다. 다만 모두 같은 대형 잔여 포지션에서 나온 반복 표본이라 새 일반 규칙으로 승격하지 않는다.
- `AVGO` residual trim은 `1D`와 `5D` 해석이 달랐다. staged de-risking은 유지하되 exact timing 기대를 강한 규칙으로 바꾸지 않는 현재 정책이 여전히 맞다.
- `WMT/MCD` skip은 이후 소폭 상승이 있었지만 source-of-record quote discipline을 뒤집을 정도는 아니었다.
- 이번 cycle만으로 `wiki/policy-book/recommendation-policy.md`를 수정하지 않는다.

## 다음 due 일정

- `Friday, August 21, 2026 ET` close: `NOK` `20D` (`2026-07-24 ET` trim)
- `NOK`, `IONQ`, `GOOGL`: open-position monitor 지속

## 참조

- [[2026-08-10-analyst-review-cycle-sources]]
- `wiki/evidence-store/run-manifests/2026-08-10-analyst-review-cycle.json`
