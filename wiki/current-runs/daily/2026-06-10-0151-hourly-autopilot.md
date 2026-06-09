# 2026-06-10-0151-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0151` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup report는 stale `PFE` buy candidate를 잡아 cancel attempt `pass`를 기록했고, live Alpaca order history에서는 해당 `0111` cycle `PFE` buy가 `2026-06-09T16:51:10Z`에 실제 취소된 것을 재확인했다. 현재 open order lifecycle에는 fresh `AVGO` sell 1건만 남아 있어 `risk_open_order_lifecycle` hard gate는 통과했지만, 같은 `AVGO` sell 재제출은 duplicate gate에 걸린다.

sell/trim 재평가에서는 `AVGO`가 live quote `370.08/371.30`, spread `0.3291%`로 trim hard gate 자체는 통과했지만 이미 `0131` cycle `AVGO` sell 2주 open order가 있어 same-symbol/same-side duplicate로 신규 trim을 만들 수 없었다. `RGTI`는 same-day sell fill 22주 때문에 duplicate sell gate, `SO`는 trim decision-grade metric gap으로 계속 blocked였다. buy fallback 후보를 다시 비교한 결과 `BAC`는 same-day buy fill duplicate, `GOOGL`은 spread `1.9589%` fail, `SPY/QQQ`는 validation floor per-order cap 초과, `NOK`는 add-block 유지로 제외됐고, `PFE`가 floor-size existing healthcare holding fallback으로 남았다. direct registered Alpaca MCP `place_stock_order`로 `PFE` 1주 @ `25.85 USD` day limit를 제출했고, immediate reconciliation 기준 주문은 `filled_avg_price=25.82 USD`로 바로 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-09T12:53:21.581649315-04:00`, regular market open |
| Stale order cleanup | PASS | cleanup report가 stale `PFE` buy cancel attempt `pass`, live order history도 canceled 재확인 |
| Open-order lifecycle | PASS | remaining open order는 fresh `AVGO` sell 1건뿐이며 age가 lifecycle limit `30`분 이내 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + submit-boundary live account/order/quote check |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo pass, Alpha Vantage `provider_error` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS | `PFE` quote `25.84/25.85`, spread `0.0387%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | direct registered Alpaca MCP `place_stock_order` success, immediate fill 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| PFE | filled | 0.0387% | stale prior buy가 cleanup으로 해소됐고 healthcare fallback buy hard gate 통과 후 1주 체결 |
| AVGO | watch | 0.3291% | trim gate는 통과하지만 existing open sell 2주 때문에 same-symbol/same-side duplicate |
| RGTI | watch | 0.0538% | speculative trim trigger는 유지되나 same-day earlier sell fill로 duplicate sell gate |
| SO | watch | 0.0429% | trim decision-grade metric gap 지속 |
| BAC | watch | 0.0186% | same-day buy fill duplicate |
| GOOGL | watch | 1.9589% | spread hard gate fail |
| SPY | watch | 0.0318% | 1주 ask `724.26 USD`가 validation floor per-order cap 약 `482.84 USD` 초과 |
| QQQ | watch | 0.0102% | 1주 ask `688.24 USD`가 validation floor per-order cap 약 `482.84 USD` 초과 |
| NOK | watch | 0.0755% | `review-due-index` add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | open_sell_duplicate_same_symbol | existing `hourly-20260610-0131-sell-avgo` open order가 있어 추가 trim 재제출 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | earlier `RGTI` sell fill `22주` 때문에 추가 same-day sell 차단 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 지속 |

## 주문 제출과 reconciliation

- Submitted order: `PFE` buy `1` @ `25.85 USD` day limit, `client_order_id=hourly-20260610-0151-buy-pfe`
- Alpaca response: `order_id=3f342972-201b-4599-9209-ba6ec56f89eb`, initial `pending_new`, immediate reconciliation 후 `status=filled`
- Filled: `PFE` buy `1` @ `25.82 USD`
- Open/new: 기존 `AVGO` sell 2주 @ `375.32 USD` (`status=new`) 1건만 유지
- Cancelled: 이번 submit attempt에서는 없음
- Position count observed by Alpaca MCP: `32` positions 유지. `PFE`는 `4주 -> 5주`로 증가했고 `AVGO`는 `10주`, `qty_available=8`로 기존 open sell 2주 예약 상태가 유지된다.
- Account snapshot after submit attempt: portfolio value `97,153.73 USD`, cash `32,185.50 USD`, buying power `295,519.35 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe strict gate 통과 |
| `check-mcp-coverage.py --strict --json` | PASS | 4개 positive research confirmations 유지 |
| `check-risk-policy.py --json` | PASS | PFE validation buy risk gate 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0151-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0151-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0151-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0151-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0151-hourly-autopilot-post-trade.json`

## 지표 설명

- `risk_open_order_lifecycle`: stale cleanup 이후에도 autopilot open order가 남아 신규 주문을 막는 hard gate다. 이번 cycle은 fresh `AVGO` open sell 1건만 남아 있었고 age가 limit 이내라 different-symbol buy는 허용됐다.
- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `open_sell_duplicate_same_symbol`: 이미 open 상태인 같은 symbol/side autopilot 주문이 있어 추가 중복 제출을 막는 규칙이다.
- `decision_grade_metric_gap`: trim은 열려 있어도 expected-excess/replacement margin 같은 결정급 지표가 비어 있어 승격하지 못한 상태다.
- `validation_lifecycle add-block`: 기존 validation buy의 due review가 남아 해당 symbol의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에 적용됐다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler preflight에서 `provider_error`로 기록됐지만, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
