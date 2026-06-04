# 2026-06-05-0331-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0331` stale cleanup/core/research preflight를 우선 사용했다. `2026-06-04T14:33:45.452066764-04:00` runtime Alpaca clock 기준 미국 정규장은 열려 있었고, scheduler core preflight와 runtime reconciliation 기준 open-order lifecycle도 유지됐다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였고, `alpha-vantage`는 one-call-per-hour throttle 때문에 `provider_error` nonblocking gap으로 남았다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `QQQ`, `SPY`, `SLB`, `AAPL`, `XOM`, `WMT`, `FCX`, `COP`, `GOOGL`, `MSFT`, `NEE`, `V`는 같은 ET regular session same-day filled buy라 duplicate discipline 때문에 제외했고, `BAC`는 같은 세션 earlier submit/cancel 이력으로 재사용하지 않았다. `NVDA`는 AI semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위에서 밀렸다. `SO`는 2026-06-04 5D review 약세와 rate-sensitive 부담 때문에 `NKE`보다 ranking이 낮았다. `NKE`는 research preflight shortlist 포함, runtime quote `43.25/43.26`에서 spread `0.0231%`, scheduler core asset check active/tradable, same-day duplicate/open-order 충돌 없음, review backlog throttle 통과, strict universe/MCP/risk gate 유지 조건을 모두 충족해 1주 validation buy를 제출했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T14:33:45.452066764-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, core preflight `get_orders_open` 0건, prior `V` order는 filled로 정리 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_order_by_client_id/get_account_activities/get_account_info/get_stock_latest_quote` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage는 `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | NKE runtime quote `2026-06-04T18:34:30.054058234Z`, spread `0.0231%` |
| Risk plan | PASS | NKE 1주 buy notional `43.26`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `NKE` 1주 regular day limit buy를 생성했고 reconciliation 기준 `status=new` open order다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| NKE | submitted_open | 0.0231% | consumer diversifier existing holding으로 runtime quote/asset check와 duplicate/open-order 재확인을 통과해 1주 validation buy를 제출했고 현재 open/new 상태다. |
| SO | watch | 0.0220% | utilities diversifier지만 2026-06-04 5D review 약세와 rate-sensitive 부담 때문에 NKE보다 replacement rank가 낮다. |
| NVDA | watch | 0.0091% | 핵심 AI thesis는 유지되지만 ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 add 우선순위를 낮췄다. |
| BAC | watch | 0.0185% | financials diversifier지만 같은 세션 earlier submit/cancel 이력 때문에 duplicate-risk discipline을 우선 적용했다. |
| TSLA | watch | 0.4067% | spread 한도 안이지만 weak review와 1주 보유 상태가 겹쳐 이번 floor-size learning order 우선순위에서는 밀렸다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `NKE` buy 1 @ `43.26` day limit
- Alpaca order id: `b80fab3c-72bd-4735-9230-4ea12623a096`
- Client order id: `hourly-20260605-0331-buy-nke`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, NKE quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`, repeated reconciliation 기준 `status=new`, `filled_qty=0`
- Reconciliation: `get_order_by_client_id`가 동일 NKE order를 `status=new`로 반환했고, post-submit `get_account_activities(FILL)`는 빈 결과였다. `get_all_positions`와 `get_order_by_id`는 cancelled였지만 post-submit `get_account_info` 기준 cash는 `30817.61`로 유지되어 신규 fill 없이 open order만 생성됐다고 기록한다. 계좌 수치는 runtime post-submit snapshot인 portfolio value `103630.87`, buying power `255572.55`, long market value `72813.26`를 사용했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | NKE 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0331-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0331-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 one-call-per-hour throttle 때문에 재호출하지 않고 nonblocking gap으로 남겼다.
- `same-day duplicate discipline`: 같은 ET regular session에서 이미 제출되었거나 체결된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 cluster warning이 있는 NVDA나 weak-rate-sensitive SO보다 NKE를 floor-size learning order 우선순위로 선택했다.
