---
id: 2026-07-25-portfolio-review
review_type: interim
reviewed_at: 2026-07-25T21:24:00Z
paper: true
decision_date:
  - 2026-07-24
  - 2026-07-25
---

# 2026-07-25 포트폴리오 리뷰

## 요약 판단

- 이번 scheduled analyst review cycle은 `Saturday, July 25, 2026` 런타임에서 `Friday, July 24, 2026 ET` 정규장 종가와 그 이후 after-hours no-submit 연속 사이클을 검토했다.
- Alpaca 기준 신규 체결, 취소, 미체결 드리프트는 없었다. `NOK` trim `1주 @ 9.67 USD`만 최근 fill로 유지되고 `1D` 평가는 여전히 `Monday, July 27, 2026 ET` 정규장 종가 이후에 닫는다.
- `NOK` add-block, `IONQ` no-add, `GOOGL` immediate add 보류를 유지한다. `WMT/MCD` after-hours skipped buy도 policy miss가 아니라 source-of-record quote quality gate가 맞게 작동한 사례로 본다.
- 정책 반영 여부: 없음. `portfolio_history`가 3회 연속 cancelled였고 `sec-edgar` 재호출도 cancelled라 신규 일반화 근거가 부족하다.

## Alpaca 정합성 점검

| 항목 | 값 |
| --- | --- |
| paper mode | `true` |
| market clock | `2026-07-25 17:22 ET`, closed |
| next open | `2026-07-27 09:30 ET` |
| account status | `ACTIVE` |
| portfolio value | `96,284.29 USD` |
| cash | `29,036.76 USD` |
| buying power | `294,299.08 USD` |
| long market value | `67,247.53 USD` |
| open orders | `0` |
| positions | `31` |
| watchlists | `0` |
| recent fills scope | `after=2026-07-24T20:00:00Z` |
| portfolio history | `cancelled` x3 |
| order mutations in this workflow | `submit 0 / replace 0 / cancel 0 / close 0` |

## Due horizon 스캔

| bucket | count | 메모 |
| --- | ---: | --- |
| pending 1D | `1` | `NOK` `2026-07-24 ET` trim `1주 @ 9.67` |
| pending 5D | `3` | `AVGO`, `NOK` `2026-07-22 ET` trim cohort + `NOK` `2026-07-24 ET` trim |
| pending 20D | `1` | `NOK` `2026-07-24 ET` trim |

- `blocked_add_symbols`: `NOK`
- `due_reviews_blocking_adds`: `NOK`
- 이번 run에서 즉시 닫을 `1D/5D/20D` horizon은 새로 열리지 않았다.

## 최근 fill continuity

| symbol | action | fill timestamp | fill | status | review status |
| --- | --- | --- | ---: | --- | --- |
| `NOK` | trim sell `1` | `2026-07-24T13:17:49.876154Z` | `9.67` | 유지 | `1D 대기` |

### 해석

- `Saturday, July 25, 2026` Alpaca continuity에서도 `client_order_id=ah-20260723-2151-sell-nok-01`는 계속 `filled` 상태였다.
- `2026-07-24 ET` close `9.07 USD`, latest trade `9.09 USD`, latest quote `9.05 / 9.10` 기준으로 same-day 방어 효과는 유지되지만, workflow상 정식 `1D` 평가는 다음 미국 정규장 close 이후로 미룬다.

## Open-position monitor

| symbol | qty | avg | close/current | unrealized | 메모 |
| --- | ---: | ---: | --- | --- | --- |
| `NOK` | 398 | `15.044573` | `9.07 / 9.10` | 약 `-39.51%` | Alpha Vantage quarter beat와 Yahoo AI-networking 기사에도 tape가 계속 약하다. add-block 유지. |
| `IONQ` | 45 | `63.48` | `32.83 / 32.84` | 약 `-48.27%` | Yahoo 추천 집계는 여전히 bullish지만 deep drawdown이 계속돼 speculative no-add 유지. |
| `GOOGL` | 5 | `376.204` | `319.725 / 319.74` | 약 `-15.01%` | Yahoo 추천 집계는 강하지만 recent add cohort 손실이 지속돼 immediate add 보류. |
| `AMD` | 14 | `462.73` | `522.03 / 521.95` | 약 `+12.80%` | winner가 남아도 losers averaging-down 완화 근거로 일반화하지 않는다. |

## Skipped recommendation 재점검

| symbol | 현재 해석 | 결론 |
| --- | --- | --- |
| `NOK` | Alpha Vantage `EARNINGS` latest row는 `reportedDate=2026-07-23`, `reportedEPS=0.08`, `estimatedEPS=0.07`, `surprisePercentage=14.2857`, `reportTime=pre-market`였다. 하지만 Yahoo 기사와 Alpaca tape를 합치면 실적 이후에도 가격 약세가 이어진다. | skip/add-block 유지 |
| `IONQ` | Yahoo 추천 집계는 `0m` 기준 `strongBuy=1`, `buy=9`, `hold=2`로 우호적이지만 `2026-07-24 ET` close/current가 `32.83/32.84 USD`까지 내려가 deep drawdown이 계속된다. | no-add 유지 |
| `GOOGL` | Yahoo 추천 집계는 `0m` 기준 `strongBuy=14`, `buy=44`, `hold=6`로 강하지만 recent add cohort 손실과 약한 tape가 겹친다. | immediate add 보류 |
| `WMT` | `2026-07-25` after-hours source-of-record에서는 quote가 반복적으로 one-sided였다. live continuity가 더 좋아 보여도 submit boundary로 승격하지 않았다. | gate-correct skip |
| `MCD` | `2026-07-25` after-hours source-of-record 기준 quote age와 spread가 반복적으로 fail했고 대표 row는 spread 약 `2.27%`였다. | gate-correct skip |

## Friday, July 24, 2026 ET after-hours no-submit 해석

- `2026-07-25-0611`부터 `2026-07-25-2151` KST까지의 after-hours scheduled runs는 모두 신규 주문 없이 종료했다.
- 핵심 차단은 policy miss가 아니라 source-of-record `fresh_quote` 실패였다.
- `NOK`는 가장 근접한 sell 후보였지만 source-of-record quote `9.05/9.10`, spread 약 `0.55%`가 after-hours 허용 범위를 계속 넘었다.
- `WMT`는 one-sided quote, `MCD`는 stale + wide spread, `QQQ/SPY`는 per-order cap 또는 stale quote 문제라 신규 buy를 열 수 없었다.

## Benchmark 및 계좌 맥락

- `SPY`: `2026-07-23 ET` close `738.06` -> `2026-07-24 ET` close `738.90`, `+0.11%`
- `QQQ`: `2026-07-23 ET` close `691.98` -> `2026-07-24 ET` close `684.33`, `-1.11%`
- `WMT`: `108.39 -> 109.46`, `+0.99%`
- `MCD`: `262.83 -> 264.715`, `+0.72%`
- account equity는 직전 analyst review의 `96,255.96 USD`에서 `96,284.29 USD`로 `+28.33 USD`, 약 `+0.03%`다.
- 다만 `get_portfolio_history`가 3회 연속 cancelled라 curve attribution이나 benchmark-relative drawdown path는 이번 run에서 보강하지 못했다.

## MCP 커버리지와 데이터 갭

- `alpaca`: usable. `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, `get_stock_snapshot`으로 account/order/fill/position/market-data reconciliation을 닫았다.
- `alpaca portfolio_history`: `gap_category=cancelled`, `retry_count=2`. initial call과 2회 retry가 모두 cancelled였다.
- `sec-edgar`: `gap_category=cancelled`, `retry_count=1`. `get_insider_summary(IONQ, 90d)` initial call과 retry가 모두 cancelled였다.
- `alpha-vantage`: usable. required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check 통과 후 `TOOL_GET(EARNINGS)` 직후 `TOOL_CALL(EARNINGS,{symbol:"NOK"})` 성공.
- `fred`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `firecrawl`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `yahoo-finance`: usable. `NOK` news, `NOK/IONQ/GOOGL` recommendation summary를 이번 run에서 확보했다.

## 정책 학습

- 이번 run은 `WMT/MCD`의 “좋아 보였지만 못 산 후보”를 policy miss로 보지 않고, source-of-record quote discipline이 과잉 실행을 막은 사례로 정리한다.
- `NOK`는 earnings beat headline과 analyst support가 있어도 price confirmation이 무너지면 add-block을 유지해야 한다는 기존 해석을 다시 지지한다.
- 그러나 새 일반 규칙으로 승격할 만큼 독립 표본이 늘지 않았고 `portfolio_history`/`sec-edgar` 보강도 불완전해 `wiki/policy-book/recommendation-policy.md`는 수정하지 않는다.

## 다음 due 일정

- `Monday, July 27, 2026 ET` close: `NOK` `1D`
- `Tuesday, July 29, 2026 ET` close: `AVGO`, `NOK` `5D` (`2026-07-22 ET` trim cohort)
- `Friday, July 31, 2026 ET` close: `NOK` `5D` (`2026-07-24 ET` trim)
- `Friday, August 21, 2026 ET` close: `NOK` `20D` (`2026-07-24 ET` trim)

## 참조

- [[2026-07-25-analyst-review-cycle-sources]]
- `wiki/evidence-store/run-manifests/2026-07-25-analyst-review-cycle.json`
