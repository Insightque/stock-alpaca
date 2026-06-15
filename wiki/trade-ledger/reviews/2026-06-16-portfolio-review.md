---
id: 2026-06-16-portfolio-review
review_type: interim
reviewed_at: 2026-06-15T21:21:56Z
paper: true
decision_date:
  - 2026-06-12
  - 2026-06-14
  - 2026-06-15
---

# 2026-06-16 포트폴리오 리뷰

## 요약

- 이번 scheduled analyst review cycle은 `RGTI` 2026-06-12 ET trim 1D, `AVGO`/`MSFT` 2026-06-14 ET after-hours 1D closeout을 완료했다.
- 2026-06-15 ET 정규장 fill `18건`은 새 `1D` 대기열로 등록했다.
- 정책 변경 증거 임계치는 충족하지 못해 `wiki/policy-book/recommendation-policy.md`는 수정하지 않았다.

## Alpaca 정합성 점검

| 항목 | 값 |
| --- | --- |
| paper mode | `true` |
| market clock | `2026-06-15 17:22 ET`, closed |
| account status | `ACTIVE` |
| portfolio value | `102,566.01 USD` |
| cash | `29,836.36 USD` |
| buying power | `306,318.33 USD` |
| long market value | `72,729.65 USD` |
| open orders | `0` |
| positions | `33` |
| watchlists | `0` |
| fills scope | `after=2026-06-10T00:00:00Z` |
| new fills since prior cycle | `20건` |
| portfolio history | `cancelled` x3 |
| order mutations in this workflow | `submit 0 / replace 0 / cancel 0 / close 0` |

## Due horizon 스캔

| bucket | count | 메모 |
| --- | --- | --- |
| pending 1D | `18` | 2026-06-15 ET 신규 fill |
| pending 5D | `19` | 기존 16건 + 이번 1D closeout 3건 승격 |
| pending 20D | `1` | `NOK` add-block 검증 유지 |

- `blocked_add_symbols`: `NOK`
- `due_reviews_blocking_adds`: `NOK`

## 2026-06-14 ET after-hours 1D closeout

| symbol | action | fill | 2026-06-15 close | return | benchmark 비교 | 판단 |
| --- | --- | --- | --- | --- | --- | --- |
| `AVGO` | trim sell 1 | `391.92` | `393.97` | `+0.52%` | `SPY +1.76%`, `QQQ +3.12%` 대비 약세 | trim timing 약함 |
| `MSFT` | add buy 1 | `395.87` | `400.05` | `+1.06%` | 절대수익 양호, 지수 대비 열위 | `중립 양호` |

## 2026-06-12 ET RGTI trim 1D closeout

| symbol | action | fill | 2026-06-15 close | return | 판단 |
| --- | --- | --- | --- | --- | --- |
| `RGTI` | trim sell 12 | `21.010833` | `22.72` | `+8.14%` | 반등 구간을 너무 이르게 정리한 약한 trim timing |

## 2026-06-15 ET 신규 fill 등록

| symbol | action | fill | next due |
| --- | --- | --- | --- |
| `RGTI` | sell 9 | `23.366667` | 2026-06-16 ET close |
| `BAC` | buy 1 | `56.28` | 2026-06-16 ET close |
| `WMT` | buy 1 | `120.20` | 2026-06-16 ET close |
| `AVGO` | sell 1 | `392.14` | 2026-06-16 ET close |
| `NEE` | buy 1 | `85.78` | 2026-06-16 ET close |
| `JPM` | buy 1 | `321.53` | 2026-06-16 ET close |
| `FCX` | buy 1 | `69.49` | 2026-06-16 ET close |
| `SLB` | buy 1 | `54.03` | 2026-06-16 ET close |
| `XOM` | buy 1 | `141.76` | 2026-06-16 ET close |
| `NKE` | buy 1 | `45.36` | 2026-06-16 ET close |
| `COP` | buy 1 | `112.62` | 2026-06-16 ET close |
| `V` | buy 1 | `324.83` | 2026-06-16 ET close |
| `SO` | buy 1 | `94.37` | 2026-06-16 ET close |
| `MSFT` | buy 1 | `398.71` | 2026-06-16 ET close |
| `GOOGL` | buy 1 | `371.22` | 2026-06-16 ET close |
| `AMZN` | buy 1 | `246.19` | 2026-06-16 ET close |
| `AAPL` | buy 1 | `296.11` | 2026-06-16 ET close |
| `PFE` | sell 1 | `26.01` | 2026-06-16 ET close |

## 오픈 포지션 모니터

| symbol | qty | avg | 2026-06-15 close | unrealized | 메모 |
| --- | --- | --- | --- | --- | --- |
| `AAPL` | 6 | `301.965` | `296.53` | `-1.80%` | 2026-06-15 ET add는 1D 대기만 등록, 평균단가 낮추기 가설은 아직 검증 전 |
| `AVGO` | 2 | `423.3625` | `393.97` | `-6.94%` | staged de-risking 유지, 다만 연속 trim timing은 약함 |
| `NOK` | 402 | `15.044527` | `14.83` | `-1.43%` | 2026-06-18 ET 20D add-block review 전까지 신규 add 금지 유지 |
| `FCX` | 6 | `65.675` | `70.10` | `+6.74%` | missed-upside 사례지만 추격 완화 근거로는 아직 부족 |

## Skipped recommendation 재점검

| symbol | 현재 해석 | 결론 |
| --- | --- | --- |
| `FCX` | 구리 민감주 강세가 이어져 missed-upside 인상은 강화 | backlog 완화나 추격 허용 정책으로 일반화하지 않음 |
| `NEE` | 방어주 톤은 유지됐지만 close `86.115`로 prior close `85.94` 대비 `+0.20%`에 그침 | skip 판단을 뒤집을 정도의 명확한 기회비용은 아님 |

## MCP 커버리지와 데이터 갭

- `alpaca`: usable. account/orders/positions/activities/snapshots reconciliation 완료.
- `sec-edgar`: usable. `AAPL`, `AVGO`, `RGTI` recent filings 확인.
- `alpha-vantage`: usable. `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{}) -> TOOL_GET(EARNINGS) -> TOOL_CALL(EARNINGS,{symbol:AAPL})` 순서 준수.
- `yahoo-finance`: usable. `AAPL`, `NOK`, `FCX` 뉴스/추천 맥락 확인.
- `fred`: `gap_category=wrapper_error`. 등록된 callable tool surface 미노출.
- `firecrawl`: `gap_category=wrapper_error`. 등록된 callable tool surface 미노출.
- `alpaca portfolio_history`: `gap_category=cancelled`, `retry_count=2`. 동일 호출 3회 모두 취소.

## 정책 학습

- 이번 cycle의 closeout은 `RGTI`/`AVGO` trim timing 약세와 `MSFT` add 중립 양호 정도의 단발성 신호에 그쳤다.
- 누적 evidence threshold를 넘는 구조적 패턴은 추가되지 않았으므로 recommendation policy 변경은 보류한다.

## 다음 due 일정

- `2026-06-16 ET` close: 2026-06-15 ET 신규 fill `18건`의 `1D`
- `2026-06-17 ET` close: 2026-06-10 ET cohort `14건`의 `5D`
- `2026-06-18 ET` close: `NOK` `20D` add-block review
- `2026-06-19 ET` close: `PFE`, `AVGO` after-hours trim `5D`
- `2026-06-22 ET` close: `RGTI`, `AVGO`, `MSFT` 이번 closeout 건의 `5D`

## 참조

- [[2026-06-16-0621-analyst-review-cycle-sources]]
- `wiki/evidence-store/run-manifests/2026-06-16-0621-analyst-review-cycle.json`
