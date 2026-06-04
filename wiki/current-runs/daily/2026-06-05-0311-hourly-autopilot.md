# 2026-06-05-0311-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0311` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup 시점에는 직전 `NEE` buy open order 1건이 있었지만 stale candidate는 아니었고, runtime Alpaca 재확인에서는 해당 주문이 `2026-06-04T18:11:17.997405Z`에 `filled`로 전환되어 decision 시점 open orders는 0건이었다. scheduler Alpaca core preflight는 market/account/positions/open-orders/quotes hard gate를 모두 `pass`로 기록했고, research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider pass, `alpha-vantage`는 `empty_response` nonblocking gap이었다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `QQQ`, `SPY`, `AAPL`, `COP`, `WMT`, `GOOGL`, `MSFT`, `NEE`는 같은 ET regular session same-day filled buy라 duplicate discipline 때문에 제외했고, `BAC`는 같은 세션 same-side submit/cancel 이력으로 재사용하지 않았다. `INTC`는 AI semiconductor_complex warning band와 기존 보유 비중 때문에 제외했고, `NKE`와 `SO`는 2026-06-04 5D review 약세가 이어졌다. `PLTR`은 speculative growth 성격상 같은 1주 learning order라면 `V`보다 보수적 우선순위였다. `V`는 research preflight shortlist 포함, runtime quote `319.71/319.83`에서 spread `0.0375%`, asset active/tradable, same-day duplicate/open-order 충돌 없음, review backlog throttle 통과, tiered MCP strict gate 유지 조건을 모두 충족해 1주 validation buy를 제출했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T14:14:03.579040549-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup는 stale candidate 0건, runtime 재확인에서는 prior `NEE` order filled로 decision 시점 open order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_orders/get_order_by_id/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot/get_asset` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage는 `empty_response` gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | V runtime quote `2026-06-04T18:15:18.402301625Z`, spread `0.0375%` |
| Risk plan | PASS | V 1주 buy notional `319.83`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `V` 1주 regular day limit buy를 생성했고 reconciliation 기준 `status=new` open order다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| V | submitted_open | 0.0375% | payments diversifier existing holding으로 runtime quote/asset check와 duplicate/open-order 재확인을 통과해 1주 validation buy를 제출했고 현재 open/new 상태다. |
| PLTR | watch | 0.0425% | speculative growth 성격과 최근 하락 노이즈 때문에 동일 1주 observation이라면 V보다 보수적 우선순위다. |
| NKE | watch | 0.0232% | consumer diversifier지만 2026-06-04 5D review 약세가 이어져 V보다 replacement rank가 낮다. |
| SO | watch | 0.0330% | utilities diversifier지만 5D review 약세와 rate-sensitive 부담이 남아 V보다 ranking이 낮다. |
| INTC | watch | 0.1509% | AI semiconductor_complex warning band와 기존 보유 비중 때문에 이번 cycle 신규 add 우선순위에서 밀렸다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `V` buy 1 @ `319.83` day limit
- Alpaca order id: `767f5f8e-d77a-48e8-bcc2-614f7b5d15e7`
- Client order id: `hourly-20260605-0311-buy-v`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, V quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`, repeated reconciliation 기준 `status=new`, `filled_qty=0`
- Reconciliation: `get_order_by_client_id`와 `get_orders(symbol=V)`가 모두 동일 order를 `status=new`로 반환했다. `get_orders(status=open)`와 `get_account_info` post-submit refresh는 tool safety layer에서 `cancelled`됐지만, `get_all_positions` 기준 V 보유수량은 여전히 2주라 fill 없이 open order만 생성됐음을 확인했다. 계좌 수치는 마지막 confirmed pre-submit runtime snapshot인 cash `31137.44`, portfolio value `103780.45`, buying power `256593.90`, long market value `72643.01`를 유지했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | V 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0311-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0311-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `empty_response`: 이번 cycle의 Alpha Vantage는 shortlisted symbols 기준 usable news payload를 만들지 못해 nonblocking gap으로 남았다.
- `same-day duplicate discipline`: 같은 ET regular session에서 이미 제출되었거나 체결된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 speculative PLTR보다 payments diversifier V를 floor-size learning order 우선순위로 선택했다.
