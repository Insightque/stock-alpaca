# 2026-06-05-0411-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 유지했고, scheduler-owned `0411` stale cleanup/core/research preflight를 우선 사용했다. scheduler Alpaca core preflight의 `get_clock`는 `2026-06-04T15:11:10.677833688-04:00`에 미국 정규장이 열려 있음을 보여줬고, 연구 preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였다. `alpha-vantage`는 one-call-per-hour throttle 때문에 `provider_error` nonblocking gap으로 남았지만 tiered MCP submit gate는 유지됐다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. runtime quote 재확인에서는 `CVX`가 `189.08/190.25`로 spread 약 `0.615%`를 보여 정책 상한 `0.50%`를 넘겨 하드 게이트에서 제외됐다. `NVDA`는 ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위를 낮췄고, `TSLA`는 speculative growth와 약한 review 때문에 `BAC`보다 ranking이 낮았다. `QQQ`와 `SPY`는 같은 ET regular session same-day filled buy 이력 때문에 duplicate discipline을 유지했다. `BAC`는 기존 2주 보유의 low-notional financials diversifier이고, runtime quote `54.01/54.02`에서 spread `0.0185%`, scheduler asset check active/tradable, runtime open-order check 0건, same-symbol live duplicate conflict 없음, review backlog throttle 통과, strict universe/MCP/risk gate 유지 조건을 모두 충족해 1주 validation buy를 제출했고 same-minute fill로 정리됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler core preflight `2026-06-04T15:11:10.677833688-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, runtime `get_orders(status=open)` 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_stock_latest_quote/get_orders/get_order_by_client_id/get_order_by_id/get_all_positions/get_account_info` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage는 `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | BAC runtime quote `2026-06-04T19:16:16.058436303Z`, spread `0.0185%` |
| Risk plan | PASS | BAC 1주 buy notional `54.02`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `BAC` 1주 regular day limit buy를 생성했고 reconciliation 기준 `filled_avg_price=54.02`다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| BAC | submitted_filled | 0.0185% | existing financials diversifier로 runtime quote/spread와 duplicate/open-order 재확인을 통과해 1주 validation buy를 제출했고 same-minute filled 상태다. |
| CVX | blocked | 0.6150% | runtime quote에서 spread가 정책 상한 `0.50%`를 넘어 hard gate 실패다. |
| NVDA | watch | 0.0091% | 핵심 AI thesis는 유지되지만 ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 add 우선순위를 낮췄다. |
| TSLA | watch | 0.0238% | speculative growth와 약한 review 때문에 floor-size learning order 우선순위에서는 밀렸다. |
| MRK | blocked | n/a | research shortlist에는 있었지만 이번 run 시점 위키 thesis/risk page가 없어 제출 후보로 승격하지 않았다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `BAC` buy 1 @ `54.02` day limit
- Alpaca order id: `8c0016bd-c60a-45c1-a631-3568c5bc0098`
- Client order id: `hourly-20260605-0411-buy-bac`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, BAC quote freshness/spread `PASS`, same-symbol live duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`, repeated reconciliation 기준 `status=filled`, `filled_avg_price=54.02`
- Reconciliation: `get_order_by_client_id`, `get_order_by_id`, `get_orders(symbol=BAC)`, `get_all_positions`, `get_account_info`가 모두 BAC fill과 보유수량 증가를 확인했다. `get_account_activities_by_type(FILL)`는 tool-layer `cancelled`였지만 나머지 교차확인으로 fill을 확정했다. post-submit account snapshot은 cash `30,629.38`, portfolio value `103,442.99`, buying power `254,922.96`, long market value `72,813.61`, open orders `0`이다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | BAC 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0411-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0411-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0411-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0411-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 one-call-per-hour throttle 때문에 재호출하지 않고 nonblocking gap으로 남겼다.
- `same-day duplicate discipline`: 같은 ET regular session에서 이미 체결된 동일 symbol/side buy 또는 live duplicate conflict를 피하는 규칙이다. 이번 run에서는 BAC의 earlier canceled order는 live conflict가 아니었고, QQQ/SPY 같은 same-day filled buys는 계속 제외했다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 CVX spread hard gate 실패 이후 BAC를 financials diversifier floor-size learning order로 선택했다.
