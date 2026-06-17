---
id: 2026-06-18-portfolio-review
review_type: interim
reviewed_at: 2026-06-17T21:21:45Z
paper: true
decision_date:
  - 2026-06-10
  - 2026-06-17
entry_date: multiple
exit_date: partial
---

# 2026-06-18 포트폴리오 리뷰

## 요약 판단

- 결론: 혼합. `2026-06-10 ET` fill cohort `14건`의 `5D` closeout을 완료했고, 결과는 `BAC/FCX`의 양호한 후속과 `COP/SLB/MSFT`의 약한 후속, `AVGO` trim timing의 되돌림이 함께 섞였다.
- 핵심 이유:
  - `BAC`는 `+3.23%`, `FCX`는 `+0.92%` absolute return이었고 둘 다 `SPY`, `QQQ`를 앞섰다.
  - `COP -8.15%`, `SLB -10.84%`, `MSFT -4.85%`, `AMZN -3.19%`는 5D에도 회복이 부족했다.
  - trim 계열에서는 `RGTI`와 `PFE`가 거의 flat 또는 소폭 유리했지만, `AVGO`는 trim 후 `+5.27%` 반등해 exact timing edge가 약했다.
- 정책 반영 여부: 보류. Alpaca `FILL` activity와 `portfolio_history`, SEC EDGAR가 모두 cancelled gap으로 남아 계좌 단위 증거와 filing-grounded 보강이 불완전하다.

## Alpaca 정합성 점검

| 항목 | 값 |
| --- | --- |
| paper mode | `true` |
| market clock | `2026-06-17 17:21 ET`, closed |
| account status | `ACTIVE` |
| portfolio value | `100,569.73 USD` |
| cash | `28,003.45 USD` |
| buying power | `299,508.51 USD` |
| long market value | `72,566.28 USD` |
| open orders | `0` |
| positions | `34` |
| watchlists | previous cycle source-of-record `0`, current run direct watchlist 호출 생략 |
| fills scope | `after=2026-06-11T00:00:00Z` order ledger 기준 |
| new fills since prior cycle | `17건` |
| Alpaca `FILL` activity | `cancelled` x3 |
| Alpaca `portfolio_history` | `cancelled` x3 |
| order mutations in this workflow | `submit 0 / replace 0 / cancel 0 / close 0` |

## Due horizon 스캔

| bucket | count | 메모 |
| --- | --- | --- |
| pending 1D | `17` | `2026-06-17 ET` overnight/regular fill cohort 신규 등록 |
| pending 5D | `23` | 기존 `37건` 중 오늘 due `14건` closeout 완료 |
| pending 20D | `15` | 기존 `1건(NOK)` + 오늘 `5D` closeout `14건` 승격 |

- `blocked_add_symbols`: `NOK`
- `due_reviews_blocking_adds`: `NOK`
- `NOK` `20D` add-block review는 여전히 `2026-06-18 ET` regular close 이후다.

## 2026-06-10 ET fill cohort 5D closeout

기준 benchmark는 Alpaca close-to-close 기준 `SPY 750.58 -> 741.02`로 `-1.27%`, `QQQ 729.87 -> 722.48`로 `-1.01%`다.

| Symbol | Action | Fill | 2026-06-17 close | 5D return | vs SPY | vs QQQ | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| WMT | buy | 118.49 | 118.185 | `-0.26%` | `+1.02%p` | `+0.76%p` | 중립 양호 |
| AVGO | sell trim 2주 | 373.25 | 392.91 | `+5.27%` | n/a | n/a | 약함 |
| RGTI | sell trim 17주 | 20.38 | 20.25 | `-0.64%` | n/a | n/a | 중립 양호 |
| BAC | buy | 54.77 | 56.54 | `+3.23%` | `+4.51%p` | `+4.24%p` | 강함 |
| PFE | sell trim 1주 | 25.94 | 25.93 | `-0.04%` | n/a | n/a | 중립 |
| XOM | buy | 141.54 | 140.79 | `-0.53%` | `+0.74%p` | `+0.48%p` | 중립 양호 |
| JNJ | buy | 237.54 | 233.92 | `-1.52%` | `-0.25%p` | `-0.51%p` | 중립 약함 |
| COP | buy | 121.05 | 111.19 | `-8.15%` | `-6.87%p` | `-7.13%p` | 강한 약함 |
| SLB | buy | 56.45 | 50.33 | `-10.84%` | `-9.57%p` | `-9.83%p` | 강한 약함 |
| AMZN | buy | 245.40 | 237.57 | `-3.19%` | `-1.92%p` | `-2.18%p` | 약함 |
| FCX | buy | 68.40 | 69.03 | `+0.92%` | `+2.19%p` | `+1.93%p` | 양호 |
| NEE | buy | 85.22 | 85.74 | `+0.61%` | `+1.88%p` | `+1.62%p` | 중립 양호 |
| NKE | buy | 43.98 | 44.19 | `+0.48%` | `+1.75%p` | `+1.49%p` | 중립 양호 |
| MSFT | buy | 398.38 | 379.05 | `-4.85%` | `-3.58%p` | `-3.84%p` | 강한 약함 |

### 해석

- `BAC`는 financials diversifier 가설이 이번 5D에서도 가장 선명했다. absolute와 relative 모두 충분히 양호했다.
- `FCX`는 copper/materials rotation 가설을 다시 지지했지만, `+0.92%` 수준이라 공격적 chase 완화 근거로 과대해석하진 않는다.
- `WMT`, `XOM`, `NEE`, `NKE`는 절대수익이 크진 않았지만 하락한 benchmark 대비 방어적으로 닫혀 `hold-quality` 역할은 유지했다.
- `COP`, `SLB`, `MSFT`, `AMZN`은 5D follow-through가 부족했다. 특히 energy add 두 건(`COP`, `SLB`)은 같은 구간에서 약세가 겹쳐 sector-level timing 리스크를 드러냈다.
- trim 계열에서는 `RGTI`와 `PFE`가 소폭 유리했지만 `AVGO`는 trim 후 반등이 커 exact timing edge가 약했다. 최근 staged de-risking success 사례를 곧바로 일반 규칙으로 강화하긴 이르다.

## Open-position monitor

| symbol | qty | avg | 2026-06-17 close/current | unrealized | 메모 |
| --- | --- | --- | --- | --- | --- |
| `AAPL` | 7 | `301.458571` | `296.07` | `-1.79%` | same US-date add가 있었지만 `mega-cap averaging-down`을 다시 공격적으로 키울 만큼의 품질 개선 증거는 없다. |
| `AVGO` | 1 | `461.26` | `392.91` | `-14.82%` | trim 뒤 5D rebound가 있었어도 잔여 포지션의 recovery confirmation은 여전히 부족하다. staged de-risking 자체는 유지하되 timing rule 강화는 보류한다. |
| `NOK` | 402 | `15.044527` | `13.81` | `-8.21%` | Alpha `EARNINGS` 최신 분기 beat와 JP Morgan 상향이 있어도 tape는 약하다. `2026-06-18 ET` 20D add-block review 전 해제 근거는 없다. |
| `RGTI` | 27 | `25.569583` | `20.25` | `-20.80%` | residual speculative sleeve 변동성은 여전히 높다. 이번 5D trim timing은 소폭 유리했지만 residual risk는 크게 달라지지 않았다. |
| `FCX` | 7 | `66.492857` | `69.03` | `+3.82%` | materials/copper diversifier 가설은 유지된다. 다만 tariff headline 민감도는 계속 확인이 필요하다. |

## Skipped recommendation 재점검

| symbol | 현재 해석 | 결론 |
| --- | --- | --- |
| `SBUX` | `2026-06-17 16:01 ET` actual submit timestamp로 정규장 종료 뒤 제출되어 즉시 취소됐다. fill이나 포지션 증가는 없다. | lifecycle discipline은 맞았고 trade review 대상은 아니다. |
| `NOK` | 최신 close `13.81 USD`와 add-block 유지 상태를 보면, 최근 자동운영의 `NOK` 신규 add 차단은 계속 타당하다. | skip/add-block을 policy miss로 뒤집지 않는다. |
| `FCX` | 기존 backlog-throttle 국면의 missed-upside 사례는 남아 있지만, 이번 5D도 절대강세가 폭발적이진 않았다. | throttle 완화 근거로 단독 승격하지 않는다. |

## 신규 fill 대기 등록

- `2026-06-17 ET` overnight/regular fill cohort `17건`은 다음 `1D` review 대기열로 등록한다.
- 대상: `PFE`, `RGTI`, `BAC`, `WMT`, `FCX`, `NKE`, `NEE`, `AMZN`, `MSFT`, `XOM`, `AAPL`, `GOOGL`, `COP`, `SO`, `SLB`, `MRK`, `NVDA`
- due 시점: `2026-06-18 ET` regular-session close 이후

## MCP 커버리지와 데이터 갭

- `alpaca`: usable. `clock/account/orders/positions/snapshots`는 usable이었다.
- `alpaca FILL activity`: `gap_category=cancelled`, `retry_count=2`. initial + 2 retries 모두 cancelled라 fill cross-check는 order ledger와 snapshot으로 대체했다.
- `alpaca portfolio_history`: `gap_category=cancelled`, `retry_count=2`. account-level curve/MFE/MAE는 이번 run에서 확인하지 못했다.
- `sec-edgar`: `gap_category=cancelled`. `analyze_form4_transactions(AVGO)`와 `get_financials(NOK)` 모두 cancelled였다.
- `alpha-vantage`: usable. required `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})` health check 통과 후 `TOOL_GET(EARNINGS)` / `TOOL_CALL(EARNINGS,{symbol:"NOK"})`도 성공했다.
- `yahoo-finance`: usable. `NOK` recommendation summary, `WMT`와 `FCX` current-news context를 보강했다.
- `fred`: `gap_category=wrapper_error`. registered callable tool surface 미노출.
- `firecrawl`: `gap_category=wrapper_error`. registered callable tool surface 미노출.

## 정책 학습

- `BAC`와 `FCX`의 5D follow-through는 기존 financials/materials diversification 가설을 지지하지만 표본 수가 여전히 작다.
- `COP`와 `SLB`의 동반 약세는 energy add timing을 더 보수적으로 보라는 신호지만, 같은 구간 macro headline 영향이 커 단일 cycle로 active rule을 만들진 않는다.
- `AVGO` trim의 5D rebound는 최근 staged de-risking success 사례에 대한 반례 하나로 기록한다. 즉시 규칙 완화/강화 모두 보류한다.
- 따라서 `wiki/policy-book/recommendation-policy.md`는 수정하지 않는다.

## 다음 due 일정

- `2026-06-18 ET` close: `NOK` `20D` add-block review, `2026-06-17 ET` overnight/regular fill cohort `17건`의 `1D`
- `2026-06-19 ET` close: `PFE`, `AVGO` after-hours trim `5D`
- `2026-06-22 ET` close: `2026-06-15 ET` fill cohort `18건`의 `5D`
- `2026-06-25 ET` close: 오늘 `5D` closeout한 `2026-06-10 ET` fill cohort `14건`의 `20D`

## 참조

- [[2026-06-18-0621-analyst-review-cycle-sources]]
- `wiki/evidence-store/run-manifests/2026-06-18-0621-analyst-review-cycle.json`
