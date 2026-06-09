# 2026-06-10-0111-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0111` stale cleanup/core/research preflight를 우선 사용했다. cleanup report는 stale autopilot open order를 남기지 않았고 runtime Alpaca MCP `get_orders(status=open)`도 `[]`를 반환해 open-order lifecycle hard gate가 해소된 상태로 시작했다. core preflight와 submit-boundary live check 모두 market open, ACTIVE account, positions, fresh quotes를 확인했고 research tiered gate도 SEC EDGAR/FRED/Firecrawl/Yahoo pass와 Alpha Vantage `empty_response` gap으로 strict threshold를 유지했다.

sell/trim 재평가에서는 `AVGO`가 live quote `372.00/395.12` 기준 spread `6.0276%`로 정책 상한 `0.50%`를 크게 넘겨 trim hard gate fail, `RGTI`는 same-day sell fill `22주` 때문에 duplicate symbol/side sell gate, `SO`는 trim decision-grade metric gap으로 승격되지 못했다. buy fallback에서는 `BAC`가 same-day buy fill, `SPY/QQQ`가 validation floor per-order cap 초과, `NOK`가 validation_lifecycle add-block으로 막혔다. 따라서 hard gate를 모두 통과한 floor-size healthcare diversifier fallback으로 `PFE` 1주 buy @ `25.70 USD` day limit를 direct registered Alpaca MCP로 제출했다. immediate reconciliation 기준 주문은 `status=new`, `filled_qty=0` open order이며 same-session 신규 fill은 아직 없다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-09T12:13:30.435000137-04:00`, regular market open |
| Stale order cleanup | PASS | cleanup report `remaining_open_orders=[]`, runtime open orders `[]` |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + submit-boundary live account/order/quote check |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage `empty_response` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS | `PFE` quote `25.69/25.70`, spread `0.0389%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | PASS | direct registered Alpaca MCP `place_stock_order` success |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | watch | 6.0276% | ai_semiconductor de-risk watch는 유지되지만 spread가 정책 상한 초과 |
| RGTI | watch | 0.0523% | speculative trim trigger는 유지되나 same-day earlier sell fill로 duplicate sell gate |
| SO | watch | 0.0323% | trim decision-grade metric gap 지속 |
| BAC | watch | 0.0371% | same-day buy fill이 이미 있어 duplicate buy gate |
| SPY | watch | 0.0041% | 1주 ask `728.79 USD`가 validation floor per-order cap 약 `487.12 USD` 초과 |
| QQQ | watch | 0.0776% | 1주 ask `696.42 USD`가 validation floor per-order cap 약 `487.12 USD` 초과 |
| NOK | watch | 0.0743% | `review-due-index` add-block 유지 |
| PFE | submitted | 0.0389% | healthcare diversifier fallback, same-day duplicate/open-order conflict 없음 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_out_of_policy | live spread `6.0276%`가 policy cap `0.50%` 초과 |
| RGTI | watch | duplicate_symbol_side_same_day | earlier `RGTI` sell fill `22주` 때문에 추가 same-day sell 차단 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 지속 |

## 주문 제출과 reconciliation

- Submitted order: `PFE` buy `1` @ `25.70 USD` day limit, `client_order_id=hourly-20260610-0111-buy-pfe`
- Alpaca response: `order_id=df1b6130-1929-4189-9003-ad7f47add552`, initial `pending_new`, reconciliation 후 `status=new`
- Open/new: `PFE` buy 1주 @ `25.70 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `PFE`는 아직 `4주` 그대로이며 `qty_available=4`; 신규 open order는 `PFE` 1건이다.
- Account snapshot after submit attempt: portfolio value `96,778.03 USD`, cash `32,211.32 USD`, buying power `294,630.25 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe strict gate 통과 |
| `check-mcp-coverage.py --strict --json` | PASS | 4개 positive research confirmations 유지 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0111-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0111-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0111-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0111-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0111-hourly-autopilot-post-trade.json`

## 지표 설명

- `risk_open_order_lifecycle`: stale cleanup 이후에도 autopilot open order가 남아 신규 주문을 막는 hard gate다. 이번 cycle은 cleanup PASS로 해소됐다.
- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `decision_grade_metric_gap`: trim은 열려 있어도 expected-excess/replacement margin 같은 결정급 지표가 비어 있어 승격하지 못한 상태다.
- `validation_lifecycle add-block`: 기존 validation buy의 due review가 남아 해당 symbol의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에 적용됐다.
- `empty_response`: 이번 run의 Alpha Vantage는 shortlisted symbols에 대한 `NEWS_SENTIMENT` 결과가 0건이어서 `empty_response` gap으로 기록됐고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
