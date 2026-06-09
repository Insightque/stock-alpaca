# 2026-06-10-0051-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0051` stale cleanup/core/research preflight를 우선 사용했다. cleanup report는 stale autopilot open buy 두 건(`SO`, `WMT`)을 검사했고 `SO`는 제거됐지만 `WMT` `hourly-20260609-2351-buy-wmt`는 cancel attempt 이후에도 `remaining_open_orders`에 남았다. core preflight는 `market_open/account/positions/quotes` hard gate를 모두 PASS로 기록했고 quotes는 `2026-06-09T15:51:33Z` 전후라 submit freshness 20분 한도 안이었다.

sell/trim 재평가에서는 `AVGO`가 scheduler-owned quote `380.50/398.95` 기준 spread `4.7347%`로 정책 상한 `0.50%`를 크게 넘겨 trim hard gate fail, `RGTI`는 same-day sell fill 22주 때문에 duplicate symbol/side sell gate, `SO`는 cleanup으로 open buy는 해소됐지만 trim decision-grade metric gap이 남아 승격되지 못했다. buy fallback에서는 `BAC`가 same-day buy duplicate, `SPY/QQQ`가 validation floor per-order cap 초과, `NOK`가 validation_lifecycle add-block으로 막혔다. `PFE` 1주 healthcare fallback buy는 quote/spread/research/cap 기준으로는 passable이었지만, workflow가 요구한 stale cleanup artifact에서 `WMT` stale open buy가 여전히 남아 있어 final first blocking gate=`risk_open_order_lifecycle`로 확정됐고 신규 submit은 수행하지 않았다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler core preflight `get_clock` `2026-06-09T11:51:12.997718451-04:00`, regular market open |
| Stale order cleanup | FAIL | cleanup report에 `WMT` open buy가 cancel attempt 이후에도 `remaining_open_orders`로 잔존 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, quote rows `15:51:33Z` 전후 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage one-call throttle `provider_error` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for blocked buy candidate | `PFE` quote `25.57/25.58`, spread `0.0391%`, freshness pass |
| Risk plan | FAIL | stale cleanup artifact 기준 `WMT` remaining stale open order가 `risk_open_order_lifecycle`를 발생 |
| Final submit path | FAIL | `place_stock_order` 호출 전 hard gate fail 확정 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | watch | 4.7347% | ai_semiconductor de-risk watch는 유지되지만 spread가 정책 상한 초과 |
| RGTI | watch | 0.0509% | speculative trim trigger는 유지되나 same-day earlier sell fill로 duplicate sell gate |
| SO | watch | 0.0865% | cleanup로 open buy는 해소됐지만 trim decision-grade metric gap 지속 |
| WMT | block | 0.0752% | stale cleanup report에 remaining open buy가 남아 lifecycle hard gate 발생 |
| BAC | watch | 0.0372% | same-day buy fill이 이미 있어 duplicate buy gate |
| SPY | watch | 0.0055% | 1주 ask `731.63 USD`가 validation floor per-order cap 약 `491.65 USD` 초과 |
| QQQ | watch | 0.0655% | 1주 ask `702.79 USD`가 validation floor per-order cap 약 `491.65 USD` 초과 |
| NOK | watch | 0.0727% | `review-due-index` add-block 유지 |
| PFE | watch | 0.0391% | healthcare diversifier fallback 자체는 passable이었지만 `risk_open_order_lifecycle`가 최종 blocker |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_out_of_policy | live spread `4.7347%`가 policy cap `0.50%` 초과 |
| RGTI | watch | duplicate_symbol_side_same_day | earlier `RGTI` sell fill `22주` 때문에 추가 same-day sell 차단 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 지속 |

## 주문 제출과 reconciliation

- Planned order before final lifecycle gate: `PFE` buy `1` @ `25.58 USD` day limit
- Pre-submit status: workflow-required stale cleanup artifact에 `WMT` stale open buy가 남아 있어 `place_stock_order` 호출 단계까지 가지 않음
- Orders: 없음. `place_stock_order`와 `cancel_order_by_id`는 호출하지 않았다.
- Immediate reconciliation: scheduler-owned cleanup source-of-record 기준 remaining open order는 `WMT` buy 1건뿐이다. same-day fills는 `BAC` buy 1건과 `RGTI` sell 22건이며 이번 cycle 신규 fill은 없다. account snapshot은 portfolio value `98,330.54 USD`, cash `32,211.32 USD`, buying power `298,502.11 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | actionable strict gate 통과 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpha throttle gap 포함 tiered strict gate 통과 |
| `check-risk-policy.py --json` | FAIL | `WMT` stale open order lifecycle block |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0051-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0051-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0051-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0051-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0051-hourly-autopilot-post-trade.json`

## 지표 설명

- `risk_open_order_lifecycle`: stale cleanup 이후에도 autopilot open order가 남아 신규 주문을 막는 hard gate다.
- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `decision_grade_metric_gap`: trim은 열려 있어도 expected-excess/replacement margin 같은 결정급 지표가 비어 있어 승격하지 못한 상태다.
- `validation_lifecycle add-block`: 기존 validation buy의 due review가 남아 해당 symbol의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에 적용됐다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler-owned one-call-per-hour throttle 때문에 `provider_error` gap으로만 기록됐고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
