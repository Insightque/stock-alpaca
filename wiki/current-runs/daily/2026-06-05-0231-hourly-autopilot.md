# 2026-06-05-0231-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구는 scheduler workflow contract 기준으로 유지했고, scheduler-owned `0231` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup 기준 미체결 autopilot order는 없었고, scheduler Alpaca core preflight는 market/account/positions/open-orders/quotes hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider pass, `alpha-vantage`는 one-call-per-hour throttle에 따른 `provider_error` gap이었다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `QQQ`, `SPY`, `GOOGL`, `COP`, `WMT`는 같은 정규장 same-day filled buy라 duplicate discipline 때문에 제외했고, `NVDA`는 AI semiconductor_complex warning band와 기존 큰 보유 비중 때문에 add 우선순위에서 밀렸다. `NKE`와 `NEE`는 quote/spread는 통과했지만 2026-06-04 5D review 약세가 이어져 `MSFT`보다 replacement rank가 낮았다. `HOOD`는 research preflight coverage는 양호했지만 speculative broker candidate이고 reusable ticker thesis evidence가 얕아 `MSFT`보다 ranking이 낮았다. `MSFT`는 research preflight shortlist 포함, 신규 mega-cap quality diversifier, runtime quote `426.67/426.80`에서 spread `0.0305%`, same-day duplicate/open-order 충돌이 없어 1주 validation buy를 제출했고 Alpaca MCP `order_id=80ffa826-0a10-4945-b981-8ce7fd3cf535`는 `filled_avg_price=426.78`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | workflow authorization과 scheduler contract 유지, nested run에서도 paper-only path 사용 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T13:34:27.254343944-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup 기준 stale candidate/open order 없음, submit 전 runtime `get_orders(status=open)`도 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_orders/get_stock_latest_quote/get_asset` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha Vantage는 `provider_error` throttle gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | MSFT runtime quote `2026-06-04T17:34:55.022227753Z`, spread `0.0305%` |
| Risk plan | PASS | `MSFT` 1주 buy_notional `426.80`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `MSFT` 1주 regular day limit buy를 생성했고 즉시 `filled`로 확인됐다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| MSFT | submitted_filled | 0.0305% | 신규 mega-cap quality diversifier validation buy로 제출했고 즉시 체결됐다. |
| NKE | watch | 0.0231% | consumer diversifier지만 2026-06-04 5D review 약세와 lower replacement rank 때문에 MSFT보다 우선순위가 낮다. |
| NEE | watch | 0.0234% | quote/spread와 FRED macro gate는 통과했지만 5D review 약세가 이어져 MSFT보다 replacement rank가 낮다. |
| NVDA | watch | 0.0182% | 핵심 AI thesis는 유지되지만 cluster warning band와 기존 큰 보유 비중 때문에 이번 cycle 신규 add는 보수적으로 유지했다. |
| HOOD | watch | 0.0574% | research preflight coverage는 양호하지만 speculative broker candidate이고 ticker thesis evidence가 얕아 MSFT보다 ranking이 낮다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `MSFT` buy 1 @ `426.80` day limit
- Alpaca order id: `80ffa826-0a10-4945-b981-8ce7fd3cf535`
- Client order id: `hourly-20260605-0231-buy-msft`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, MSFT quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`, reconciliation 기준 `status=filled`, `filled_qty=1`, `filled_avg_price=426.78`
- Reconciliation: `get_order_by_client_id`, same-window `get_orders(symbol=MSFT)`, `get_account_activities(FILL)`, `get_account_info`가 모두 fill을 확인했다. runtime `get_orders(status=open)`와 `get_all_positions/get_open_position` direct refresh는 safety-layer `cancelled`로 남아 `gap_category=cancelled`를 기록했고, pre-submit open order 0건과 filled order/fill/account cross-check, prior position count 32에 신규 MSFT 1주 fill을 더한 추정으로 open orders 0건과 position count 33을 기록했다. runtime `get_account_info` 기준 cash `31222.79`, portfolio value `103362.01`, buying power `255996.07`, long market value `72139.22`였다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | MSFT 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0231-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0231-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 추가 provider call을 생략했고 `provider_error` gap으로 남았다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 제출되었거나 체결된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 weak-review consumer/utility 후보와 speculative HOOD보다 MSFT가 더 높은 learning-order 우선순위를 가졌다.
