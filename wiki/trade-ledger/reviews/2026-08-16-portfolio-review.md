---
id: 2026-08-16-portfolio-review
review_type: interim
reviewed_at: 2026-08-16T23:49:49Z
paper: true
decision_date:
  - 2026-08-14
  - 2026-08-16
---

# 2026-08-16 포트폴리오 리뷰

## 요약 판단

- 이번 scheduled analyst review cycle은 `Sunday, August 16, 2026 ET`에 실행됐다. 미국 정규장은 휴장 중이어서 새 `1D/5D/20D` due closeout은 없고, 마지막 확정 종가인 `Friday, August 14, 2026 ET` 기준 carry-forward review로 기록한다.
- Alpaca MCP reconciliation은 truthfully 완료했다. `ALPACA_PAPER_TRADE=true`, account `ACTIVE`, portfolio value `100,806.67 USD`, cash `29,036.76 USD`, open orders `0`, positions `31`, recent review cohort fills `NOK 4건 / AVGO 1건`을 재확인했다.
- open-position monitor에서는 `NOK`의 반등이 있었지만 basis recovery와는 거리가 멀어 add-block을 유지한다. `IONQ`는 실적 이후 회복 연장이 보였지만 speculative no-add를 유지하고, `GOOGL`은 `August 10-14` 주간 상대약세로 immediate add 보류를 유지한다.
- skipped recommendation 재점검에서는 `WMT`와 `MCD`가 `Friday, July 24, 2026 ET` 대비 각각 약 `+5.31%`, `+3.06%`였지만 quote discipline을 뒤집을 정도의 missed upside는 아니어서 gate-correct skip으로 유지한다.
- 정책 반영 여부: 없음. `sec-edgar`, `alpha-vantage`, `fred`, `firecrawl`, `yahoo-finance` callable surface가 이번 세션에 없고, `get_portfolio_history`도 initial call과 2회 retry 모두 cancelled라 evidence threshold를 충족하지 못했다.

## Alpaca 정합성 점검

| 항목 | 값 |
| --- | --- |
| paper mode | `true` |
| market clock | `2026-08-16 19:48 ET`, closed |
| next open | `2026-08-17 09:30 ET` |
| next close | `2026-08-17 16:00 ET` |
| account status | `ACTIVE` |
| portfolio value | `100,806.67 USD` |
| cash | `29,036.76 USD` |
| buying power | `305,111.84 USD` |
| long market value | `71,769.91 USD` |
| open orders | `0` |
| positions | `31` |
| recent fills scope | `after=2026-07-20T00:00:00Z` |
| recent fill count | `5` |
| portfolio history | `cancelled` x3 |
| order mutations in this workflow | `submit 0 / replace 0 / cancel 0 / close 0` |

## Due horizon 스캔

| bucket | count | 메모 |
| --- | ---: | --- |
| pending 1D | `0` | 새 due closeout 없음 |
| pending 5D | `0` | 새 due closeout 없음 |
| pending 20D | `1` | `NOK` `2026-07-24 ET` trim |

- `blocked_add_symbols`: `NOK`
- `due_reviews_blocking_adds`: `NOK`
- next due closeout: `Friday, August 21, 2026 ET` regular-session close `NOK` `20D`

## Review status

- `AVGO` `2026-07-22 ET` trim `5D`, `NOK` `2026-07-22 ET` trim `5D`, `NOK` `2026-07-24 ET` trim `1D/5D`는 `Monday, August 10, 2026 ET` review에서 이미 닫혀 있다.
- `Sunday, August 16, 2026 ET` run은 비거래일 carry-forward cycle이므로 새 horizon closeout은 만들지 않고, open positions와 skipped recommendations의 decision quality만 재확인한다.

## Open-position monitor

| symbol | qty | avg | `2026-08-10 ET` close | `2026-08-14 ET` close/current | move vs `2026-08-10` | unrealized | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `NOK` | 398 | `15.044573` | `9.12` | `10.77 / 10.78` | `+18.09%` | 약 `-28.48%` | add-block 유지 |
| `IONQ` | 45 | `63.48` | `42.51` | `46.30 / 46.30` | `+8.92%` | 약 `-27.11%` | speculative no-add 유지 |
| `GOOGL` | 5 | `376.204` | `357.545` | `345.86 / 345.33` | `-3.27%` | 약 `-8.21%` | immediate add 보류 유지 |

### 해석

- `NOK`는 `2026-08-13` Alpaca news의 stronger-than-expected Q2 / AI-cloud order volume headline과 함께 주간 반등이 나왔다. 하지만 current `10.78 USD`도 평균단가 `15.044573 USD`를 크게 밑돌고, 기존 trim closeout들이 모두 방어적으로 맞았다는 점을 뒤집지 못한다.
- `IONQ`는 `Friday, August 14, 2026 ET` close `46.30 USD`로 `Monday, August 10, 2026 ET` close `42.51 USD` 대비 회복했다. 그럼에도 basis gap이 여전히 약 `27%`이고 speculative sleeve 특성이 강해 averaging-down 완화 근거로는 부족하다.
- `GOOGL`은 `August 10-14` 주간에 `SPY`, `QQQ`, `SMH` 모두를 하회했다. quality/scale thesis 자체는 남지만 이번 주 price action만 보면 immediate add를 재개할 정도의 tape confirmation은 아니다.

## Skipped recommendation 재점검

| symbol | 기준 구간 | 성과 | 결론 |
| --- | --- | ---: | --- |
| `WMT` | `2026-07-24 ET close 109.46` -> `2026-08-14 ET close 115.27` | `+5.31%` | gate-correct skip 유지 |
| `MCD` | `2026-07-24 ET close 264.715` -> `2026-08-14 ET close 272.825` | `+3.06%` | gate-correct skip 유지 |

### 해석

- `WMT`는 주간 바운스가 있었지만 source-of-record quote discipline을 뒤집을 정도의 급격한 missed upside는 아니다. 특히 이번 주 Alpaca news도 다음 주 earnings-volatility watch 성격이어서 hindsight로 add 정당성을 부여하긴 어렵다.
- `MCD`도 소폭 우상향했지만 절대 성과가 제한적이고, `Friday, July 24, 2026 ET` 이후 즉시 추격하지 않은 판단을 policy miss로 승격할 근거는 부족하다.

## Benchmark 및 계좌 맥락

- `SPY`: `2026-08-10 ET close 773.02` -> `2026-08-14 ET close 776.30`, `+0.42%`
- `QQQ`: `2026-08-10 ET close 720.805` -> `2026-08-14 ET close 731.045`, `+1.42%`
- `SMH`: `2026-08-10 ET close 569.46` -> `2026-08-14 ET close 587.78`, `+3.22%`
- `GOOGL`은 같은 구간 `-3.27%`로 세 벤치마크를 모두 하회했다.
- `NOK`와 `IONQ`의 주간 반등은 의미 있지만, 계좌 차원의 high-conviction add 재개 시그널로 일반화할 정도는 아니다.
- account `balance_asof`는 `2026-08-14`이며, `get_portfolio_history`가 initial call과 2회 retry 모두 cancelled여서 curve attribution과 account-level MFE/MAE는 이번 run에서도 보강하지 못했다.

## MCP 커버리지와 데이터 갭

- `alpaca`: usable. `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_all_positions`, `get_stock_bars`, `get_stock_snapshot`, `get_news`로 account/order/fill/position/market-data reconciliation을 닫았다.
- `alpaca portfolio_history`: `gap_category=cancelled`, `retry_count=2`. initial call과 2회 retry가 모두 `user cancelled MCP tool call`이었다.
- `sec-edgar`: `gap_category=wrapper_error`. registered server는 있지만 callable Codex tool surface가 현재 세션에 없다.
- `alpha-vantage`: `gap_category=wrapper_error`. required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check를 시작할 surface가 노출되지 않았다.
- `fred`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `firecrawl`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `yahoo-finance`: `gap_category=wrapper_error`. registered callable tool surface 미노출.

## 정책 학습

- `NOK`의 반등 자체는 `trim-after-weakness` 규칙을 반박하지 않는다. 기존 trim closeout들이 모두 fill 이후 추가 약세를 보여준 만큼, 현재 정책은 여전히 `price-first` 쪽이 맞다.
- `GOOGL`의 quality thesis는 남아 있어도 recent add cohort가 벤치마크 대비 즉시 강한 회복을 보여주지 못하면 추가 매수를 자동 완화하지 않는 현재 규율이 유효하다.
- `WMT/MCD` skipped recommendation은 hindsight로 보면 아쉬움이 있지만, 이번 표본만으로 quote/source discipline을 느슨하게 바꿀 정도의 operational lesson은 아니다.
- 따라서 `wiki/policy-book/recommendation-policy.md`는 변경하지 않는다.

## 다음 due 일정

- `Friday, August 21, 2026 ET` close: `NOK` `20D` (`2026-07-24 ET` trim)
- `NOK`, `IONQ`, `GOOGL`: open-position monitor 지속

## 참조

- [[2026-08-10-portfolio-review]]
- [[2026-08-16-analyst-review-cycle-sources]]
- `wiki/evidence-store/run-manifests/2026-08-16-analyst-review-cycle.json`
