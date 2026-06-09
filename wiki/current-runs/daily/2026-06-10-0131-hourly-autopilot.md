# 2026-06-10-0131-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0131` stale cleanup/core/research preflight를 우선 사용했다. cleanup report는 stale autopilot open order를 남기지 않았고 현재 open order는 fresh `PFE` buy 1건만 남아 있어 symbol/side가 다른 risk-reducing sell을 막지 않았다. core preflight와 submit-boundary live check 모두 market open, ACTIVE account, positions, fresh quotes를 확인했고 research tiered gate도 SEC EDGAR/FRED/Firecrawl/Yahoo pass와 Alpha Vantage `provider_error` gap으로 strict threshold를 유지했다.

sell/trim 재평가에서는 `AVGO`가 live quote `375.32/375.64`, spread `0.0852%`로 정책 상한 `0.50%` 안으로 정상화돼 25% trim hard gate를 통과했다. `RGTI`는 same-day sell fill `22주` 때문에 duplicate symbol/side sell gate, `SO`는 trim decision-grade metric gap으로 계속 blocked다. user의 learning_trade_directive는 hard gate가 모두 통과할 때 eligible risk-reducing sell/trim을 new buy보다 우선하도록 요구하므로, 이번 cycle은 `AVGO` 2주 trim @ `375.32 USD` day limit를 direct registered Alpaca MCP로 제출했다. immediate reconciliation 기준 주문은 `status=new`, `filled_qty=0` open order이며 same-session 신규 fill은 아직 없다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-09T12:33:37.896038687-04:00`, regular market open |
| Stale order cleanup | PASS | cleanup report status=`pass`, stale candidate 없음 |
| Open-order lifecycle | PASS | fresh `PFE` buy 1건만 존재, age 약 `13.5`분으로 lifecycle limit `30`분 이내 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + submit-boundary live account/order/quote check |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage `provider_error` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS | `AVGO` quote `375.32/375.64`, spread `0.0852%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | direct registered Alpaca MCP `place_stock_order` success |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | submitted_open | 0.0852% | ai_semiconductor warning-band / post-earnings de-risk watch, spread 정상화로 trim gate 통과 |
| RGTI | watch | 0.0528% | speculative trim trigger는 유지되나 same-day earlier sell fill로 duplicate sell gate |
| SO | watch | 0.0322% | trim decision-grade metric gap 지속 |
| PFE | watch | 0.0387% | fresh open buy 1건이 이미 있어 same-symbol buy duplicate |
| GOOGL | watch | 0.0221% | buy fallback으로는 가능하지만 eligible AVGO trim이 우선 |
| SPY | watch | 0.0220% | 1주 ask `728.15 USD`가 validation floor per-order cap 약 `486.02 USD` 초과 |
| QQQ | watch | 0.0749% | 1주 ask `694.33 USD`가 validation floor per-order cap 약 `486.02 USD` 초과 |
| NOK | watch | 0.0747% | `review-due-index` add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | duplicate_symbol_side_same_day | earlier `RGTI` sell fill `22주` 때문에 추가 same-day sell 차단 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 지속 |
| BAC | hold_watch | sell_trigger_none | sell trigger는 없고 eligible AVGO trim이 먼저 열려 buy fallback 필요 없음 |

## 주문 제출과 reconciliation

- Submitted order: `AVGO` sell `2` @ `375.32 USD` day limit, `client_order_id=hourly-20260610-0131-sell-avgo`
- Alpaca response: `order_id=d850cf67-3c44-4a63-9f44-ef53c5fe8897`, initial `pending_new`, reconciliation 후 `status=new`
- Open/new: `AVGO` sell 2주 @ `375.32 USD` (`status=new`), 기존 `PFE` buy 1주 @ `25.70 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: `32` positions 유지. `AVGO`는 아직 `10주` 그대로이며 `qty_available=8`로 open sell 2주가 예약됐다. `PFE`는 `4주` 유지다.
- Account snapshot after submit attempt: portfolio value `96,473.09 USD`, cash `32,211.32 USD`, buying power `293,877.73 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe strict gate 통과 |
| `check-mcp-coverage.py --strict --json` | PASS | 4개 positive research confirmations 유지 |
| `check-risk-policy.py --json` | PASS | AVGO trim order-plan risk gate 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0131-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0131-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0131-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0131-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0131-hourly-autopilot-post-trade.json`

## 지표 설명

- `risk_open_order_lifecycle`: stale cleanup 이후에도 autopilot open order가 남아 신규 주문을 막는 hard gate다. 이번 cycle은 fresh `PFE` open buy 1건만 남아 있었고 age가 limit 이내라 different-symbol trim은 허용됐다.
- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `decision_grade_metric_gap`: trim은 열려 있어도 expected-excess/replacement margin 같은 결정급 지표가 비어 있어 승격하지 못한 상태다.
- `validation_lifecycle add-block`: 기존 validation buy의 due review가 남아 해당 symbol의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에 적용됐다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 API call을 건너뛰었고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
