---
id: 2026-05-27-autopilot-close-gate-analysis
created_at: 2026-05-27T10:08:00+09:00
source_type: autopilot-gate-analysis
paper: true
orders_submitted: 0
---

# 2026-05-27 장마감 전 자동운영 게이트 분석

## 결론

사용자가 지목한 `2026-05-27 02:06 KST` 로그는 run id `2026-05-27-0159-hourly-autopilot`의 기록이다. 이 run 자체는 주문이 없었다. 이유는 가격 후보가 없어서가 아니라 Alpaca 계좌, 포지션, 미체결 주문, asset 확인 같은 core submit gate가 cancelled되어 `alpaca_account`에서 멈췄기 때문이다.

다만 02:06 이후 장마감까지 전체를 보면 추천이나 매입이 전혀 없었던 것은 아니다. 자동운영은 이후에도 추천 shortlist를 만들었고, `NOK`, `NVDA`, `AAPL`은 1주 paper validation buy로 체결됐다. `AMZN`은 주문 제출까지 갔지만 장마감에 미체결 만료됐고, `INTC`는 주문 제출 MCP wrapper가 두 번 cancelled되어 실제 주문이 생성되지 않았다. 매도/trim은 thesis-break, 리스크 한도 위반, stale-thesis underperformance가 확인되지 않아 발생하지 않았다.

쉽게 말하면, 이 시간대의 핵심 문제는 "종목을 못 찾음"이 아니라 "자동주문 안전문이 여러 번 닫힘"이었다.

## 시간대별 요약

| KST 로그 | run id | 결과 | 가장 큰 이유 |
| --- | --- | --- | --- |
| 02:06 | `2026-05-27-0159-hourly-autopilot` | 주문 없음 | Alpaca account/order/position/asset core gate cancelled. 첫 차단 gate `alpaca_account` |
| 02:24 | `2026-05-27-0211-hourly-autopilot` | `NOK` 1주 buy 체결 | Alpaca/universe/MCP/risk 통과 |
| 02:35 | `2026-05-27-0226-hourly-autopilot` | `NVDA` 1주 buy 체결 | Alpaca/universe/MCP/risk 통과 |
| 03:00 | `2026-05-27-0251-hourly-autopilot` | `AAPL` 1주 buy 제출, 이후 체결 확인 | 최초 submit cancelled 후 같은 client id로 재시도. 사후 포지션 스냅샷에서 체결 확인 |
| 03:14 | `2026-05-27-0311-hourly-autopilot` | 주문 없음 | research MCP usable/pass가 FRED/Yahoo 2개뿐이라 submit 기준 3개 미달. AAPL open order도 존재 |
| 03:35 | `2026-05-27-0331-hourly-autopilot` | 주문 없음 | nested Codex shell에서 `ALPACA_PAPER_TRADE=true` 미확인, research MCP 2개뿐, AAPL open order age 30분 초과 |
| 04:20 | `2026-05-27-0411-hourly-autopilot` | `AMZN` 1주 buy 제출, 미체결 | Alpaca/universe/MCP/risk 통과했지만 limit order가 fill되지 않고 open `new`로 남음 |
| 04:39 | `2026-05-27-0431-hourly-autopilot` | `INTC` 계획은 PASS, 실제 주문 없음 | `place_stock_order` call과 retry가 모두 wrapper cancelled. reconcile에서 주문/체결/포지션 없음 확인 |
| 04:54 | `2026-05-27-0451-hourly-autopilot` | 주문 없음 | 기존 AMZN open order가 34.4분째 남아 lifecycle limit 30분 초과. 첫 차단 gate `risk_open_order_lifecycle` |

## 원인 묶음

1. `02:06` run의 직접 원인: Alpaca core gate 실패

`NOK`, `SMH`, `FCX`, `NVDA`, `AAPL`, `INTC`는 quote/spread가 통과했지만, 계좌 잔고, 현재 포지션, 미체결 주문, asset tradability를 확정하지 못했다. 자동주문은 중복 주문과 리스크 한도를 확인할 수 없으면 주문하지 않도록 설계되어 있어 전체 buy/sell 후보가 skip됐다.

2. `03:14` 이후 일부 run의 원인: research MCP 확인 수 부족

Submit 후보는 Alpaca 외 research MCP 중 최소 3개 usable/pass가 필요하다. `03:14`에는 FRED와 Yahoo Finance만 usable/pass라 2개에 그쳤고, SEC EDGAR와 Alpha Vantage는 cancelled, Firecrawl은 wrapper_error였다. 그래서 AMZN/INTC가 후보였어도 actionable buy로 승격되지 않았다.

3. `03:35` run의 원인: paper mode env 오탐

Scheduler preflight는 Alpaca core를 통과했지만 nested Codex shell에서 `ALPACA_PAPER_TRADE=true`가 보이지 않았다. paper-only 원칙상 이 값이 불확실하면 주문 제출은 즉시 중단된다. 이 문제는 이후 `2026-05-27 07:57 KST` maintenance에서 wrapper가 `.env`를 export하도록 보강됐다.

4. 장 후반 원인: open order lifecycle

`AMZN` 주문이 `04:20 KST`에 제출됐지만 체결되지 않고 open `new`로 남았다. `04:54 KST` run에서는 이 미체결 주문이 34.4분째 남아 risk policy의 30분 한도를 넘었다. 그래서 새 INTC validation buy 후보도 막혔다. 장마감 후 analyst review에서는 AMZN 주문이 `expired`, filled_qty 0으로 확인됐다.

5. INTC 미체결이 아니라 "미생성"

`04:39 KST` INTC는 universe/MCP/risk-check가 모두 PASS였지만 주문 제출 MCP call이 두 번 cancelled됐다. 이후 `get_orders`, FILL activity, positions 재확인에서 INTC 주문과 체결이 모두 없었다. 따라서 INTC는 미체결 주문이 아니라 실제 주문 생성 실패다.

## 매도/trim이 없었던 이유

해당 시간대 보고서들은 active trim trigger를 확인했지만, 개별 ticker 15% cap, speculative 12% cap, cash 20% floor, invested 80% cap 위반이 없다고 기록했다. thesis-break나 stale-thesis underperformance만으로 즉시 매도할 보유 종목도 없었다. 따라서 sell/trim은 안전 규칙상 제출되지 않았다.

## 추가 원인 설명

### Alpaca core `cancelled`의 원인과 예방

`02:06 KST` run의 Alpaca core failure는 계좌 데이터가 실제로 없었다기보다 scheduled nested Codex의 MCP 호출이 비대화식 실행에서 승인/래퍼 문제로 `user cancelled MCP tool call` 또는 `MCP safety cancellation`처럼 반환된 호출 이슈에 가깝다. 같은 시간대에 일부 Alpaca 도구는 pass했고, 이후 run에서 같은 Alpaca 계좌/주문/포지션 조회가 pass했기 때문이다.

이미 적용된 예방책은 다음과 같다.

- `scripts/run-hourly-autopilot-codex.sh`가 `.env`를 `source`/export한 뒤 nested Codex를 실행한다.
- scheduler-owned `fetch-alpaca-core-preflight.py`가 Alpaca core evidence를 먼저 read-only MCP로 캡처한다.
- nested Codex MCP 설정에 Alpaca read/order 도구별 `approval_mode="approve"`가 들어가 비대화식 `-a never` 실행의 false cancellation을 줄인다.
- Alpaca preflight가 pass이면 nested workflow는 그 JSON을 source_ref로 사용하고, 빠진 row만 registered MCP로 1회 재시도한다.

남는 리스크는 MCP wrapper 자체가 실제로 멈추거나 submit 도구가 cancelled되는 경우다. 이때는 안전상 fail-closed가 맞으며, 직접 REST 우회는 금지된다.

### Research MCP 공백은 데이터 없음인가 호출 이슈인가

`03:14 KST` run의 AMZN/INTC research MCP 실패는 대부분 데이터 없음이 아니라 호출/도구 노출 이슈였다.

- FRED는 pass했다.
- Yahoo Finance는 AMZN recommendations row가 usable했다. 뉴스 호출 일부는 cancelled였지만 provider 전체가 데이터 없음은 아니었다.
- SEC EDGAR는 AMZN/INTC CIK fallback이 성공했지만, 당시 SEC MCP `get_financials` 호출이 cancelled됐다. 즉 AMZN/INTC에 filing 데이터가 없어서가 아니라 호출이 무거웠거나 wrapper가 cancelled된 경우다.
- Alpha Vantage는 PING은 pass했지만 첫 `NEWS_SENTIMENT` candidate call이 cancelled됐다. 이것도 데이터 0건 반환이 아니라 호출 취소다.
- Firecrawl은 registered tool이 nested Codex tool catalog에 노출되지 않아 `wrapper_error`였다.

진짜 데이터 공백 가능성은 ETF나 ADR/비표준 종목에서 더 크다. 예를 들어 `SMH`는 ETF라 SEC ticker-CIK cache에 없을 수 있고, 그런 경우는 provider failure가 아니라 lookup/data coverage gap으로 분리해야 한다.

예방책은 SEC에서 heavy financials보다 `get_company_info`/`get_recent_filings` 같은 lightweight evidence를 먼저 쓰는 것, Firecrawl/FRED를 scheduled MCP override에 확실히 등록하는 것, 가능하면 research preflight를 FRED뿐 아니라 SEC/Yahoo/Alpha/Firecrawl까지 확장하는 것이다.

### AMZN 미체결 원인

`AMZN`은 `04:20 KST` run에서 제출됐지만 실제 제출 시각은 `2026-05-26 15:19:07 ET`로 장마감 약 41분 전이었다. 단순히 너무 늦어서만은 아니다. 다만 limit buy 가격 `263.10`은 약 7.4분 전 quote의 ask였고, 제출 시점에 시장이 그 가격 위로 움직였거나 주문 체결 우선순위가 밀리면 fill되지 않을 수 있다. 이후 주문은 `new`, filled_qty 0으로 남았고 day order라 `16:00 ET` 장마감에 `expired`됐다.

예방책은 submit 직전 quote를 더 강하게 refresh하고, validation buy는 정책 한도 0.5% 안에서 ask보다 아주 작은 여유 tick/buffer를 주거나, 장마감 전 N분 이내에는 신규 validation order를 내지 않는 것이다. 미체결 stale order는 이미 cleanup helper로 다음 run 전에 정리하도록 보강됐다.

### INTC submit cancelled

`INTC`는 후보, universe, MCP, risk check가 모두 pass였지만 `place_stock_order` 호출과 동일 client id retry가 모두 `user cancelled MCP tool call`을 반환했다. 이후 `get_orders`, FILL activity, positions 재확인에서 INTC 주문/체결/포지션이 없었으므로 실제 주문은 생성되지 않았다.

이것도 데이터 없음이나 판단 로직 문제가 아니라 submit MCP 호출 경로 문제다. 현재 wrapper는 `place_stock_order.approval_mode="approve"`를 명시해 예방했지만, submit tool이 계속 cancelled되면 안전상 주문하지 않는 것이 맞다.

### 매도가 없었던 것은 로직 오류인가

현재 정책상 자동 매도는 새 매수 후보가 더 좋아 보인다는 이유만으로 실행되지 않는다. 허용된 자동 trim 사유는 thesis break, risk limit, stale thesis, position sizing, speculative cap, cluster/theme/factor cap, overheat profit protection, underperformance control 등이다. 또 fresh quote, spread, open-order check, risk check가 필요하다.

해당 시간대에는 보유 포지션이 주요 cap을 넘지 않았고, 손실도 `speculative_loss_pct=-8%` 또는 20D SPY 대비 `-5%` 같은 stale thesis trigger에 걸렸다는 근거가 없었다. 따라서 매도 없음은 보수적 정책 설계에 따른 결과이지, 확인된 로직 오류는 아니다. 다만 더 적극적인 회전매매를 원한다면 별도 검증을 거쳐 `rotation_trim` 같은 새 정책 사유를 추가해야 한다.

## 재발 방지 조치

2번 문제의 근본 조치는 research MCP 확인을 nested Codex 안에서 매번 새로 시도하지 않고, scheduler wrapper가 먼저 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance를 로컬 MCP stdio로 수집해 JSON evidence로 넘기는 방식이다. 이렇게 하면 비대화식 Codex의 tool catalog/approval cancellation이 추천 gate를 흔드는 일을 줄일 수 있다.

구현 방향은 다음과 같다.

- `scripts/fetch-research-mcp-preflight.py`를 FRED 전용 preflight에서 5개 research MCP preflight로 확장한다.
- Alpaca core preflight의 fresh quote/spread 정보를 이용해 유동성 좋은 후보를 골라 research preflight 대상 symbol로 삼는다.
- SEC EDGAR는 local CIK cache와 lightweight `get_company_info`/`get_recent_filings`를 먼저 사용해 heavy financials cancellation을 피한다.
- Alpha Vantage는 `PING` health check 뒤 `NEWS_SENTIMENT` 한 번만 시도하고, candidate call cancellation은 명확히 `gap_category=cancelled`로 분류한다.
- 각 provider row에서 `mcp_coverage_hint`를 생성해 nested workflow가 그대로 manifest에 반영할 수 있게 한다.
- 실패 provider는 `auth`, `cancelled`, `dns`, `empty_response`, `provider_error`, `wrapper_error` 등으로 분리해 "데이터 없음"과 "호출 문제"가 섞이지 않게 한다.

이 변경은 주문을 강제로 늘리는 수정이 아니라, 원래 있어야 할 research evidence가 MCP 호출 취소 때문에 빠지는 false negative를 줄이는 안전장치다. 그래도 실제 provider가 auth/network/data gap이면 기존처럼 fail-closed로 기록하고, buy gate 3개 미만이면 주문하지 않는다.

## 참고 문서

- [[2026-05-27-0159-hourly-autopilot]]
- [[2026-05-27-0211-hourly-autopilot]]
- [[2026-05-27-0226-hourly-autopilot]]
- [[2026-05-27-0251-hourly-autopilot]]
- [[2026-05-27-0311-hourly-autopilot]]
- [[2026-05-27-0331-hourly-autopilot]]
- [[2026-05-27-0411-hourly-autopilot]]
- [[2026-05-27-0431-hourly-autopilot]]
- [[2026-05-27-0451-hourly-autopilot]]
- [[portfolio-current]]
