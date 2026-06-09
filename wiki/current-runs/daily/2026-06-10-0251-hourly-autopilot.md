# 2026-06-10-0251-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0251` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 blocking open order `0`건으로 종료됐고 core preflight hard gate도 `pass`였다. 이번 cycle은 preflight core/research evidence를 유지한 상태에서 registered Alpaca MCP live submit-boundary check를 다시 수행했다.

sell-first 진단에서는 `AVGO`가 post-earnings de-risk trim rationale를 유지하지만 `2026-06-09T17:00:40Z` same-day sell fill 때문에 duplicate symbol/side gate에 막혔고, `RGTI`도 speculative loss-control trim trigger는 남아 있지만 same-day sell fill 22주 때문에 추가 trim이 불가했다. `SO`는 live quote/spread는 통과했지만 trim decision-grade metric gap이 이어졌다. buy fallback에서는 `SLB`, `WMT`, `PFE`, `BAC`가 모두 same-day buy duplicate로 제외됐고, `SPY/QQQ`는 validation floor per-order cap 초과였다. `NOK`는 validation_lifecycle add-block이 계속 남았다. 남은 same-cycle research-covered fallback 중 `COP`가 2026-06-09 analyst review 기준 `2026-06-05 ET` fill 1D `+1.28%`, `SPY` 대비 `+1.04%p`, energy/value diversifier 역할, live IEX quote `116.09/116.14` spread `0.0431%`, same-day duplicate/open-order conflict 부재를 모두 충족해 floor-size validation buy로 선택됐고 direct Alpaca MCP `place_stock_order` 제출 후 immediate reconciliation 기준 `filled_avg_price=116.05 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | live Alpaca clock `2026-06-09T13:53:14.173164099-04:00`, regular market open |
| Stale order cleanup | PASS | `0251` cleanup artifact 기준 stale/open autopilot order 모두 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, live `get_clock/get_account_info/get_orders/get_all_positions/get_account_activities` 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage throttled `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | `COP` live IEX quote `116.09/116.14`, spread `0.0431%`, freshness submit boundary `~0.00`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | PASS | registered Alpaca MCP `place_stock_order` accepted, same client id reconciliation 기준 즉시 filled |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| COP | filled | 0.0431% | same-day duplicate/open-order conflict 없음, 2026-06-09 analyst review 1D `양호`, same-cycle research preflight coverage 유지, energy/value diversifier 역할 |
| AVGO | watch | duplicate | trim rationale는 유지되지만 17:00Z same-day sell fill 2주 때문에 duplicate sell gate |
| RGTI | watch | duplicate | speculative trim trigger는 유지되나 same-day earlier sell fill 때문에 duplicate sell gate |
| SO | watch | 0.0324% | quote/spread는 통과하지만 trim decision-grade metric gap |
| SLB | watch | duplicate | 17:45Z same-day buy fill 1주 |
| WMT | watch | duplicate | 17:19Z same-day buy fill 1주 |
| PFE | watch | duplicate | 17:00Z same-day buy fill 1주 |
| BAC | watch | duplicate | 14:45Z same-day buy fill 1주 |
| SPY | watch | 0.0628% | 1주 ask `732.62 USD`가 validation floor per-order cap 약 `490.43 USD` 초과 |
| QQQ | watch | 0.0228% | 1주 ask `700.30 USD`가 validation floor per-order cap 약 `490.43 USD` 초과 |
| NOK | watch | 0.0734% | `review-due-index` add-block 유지 |
| NEE | watch | 0.0118% | same-cycle research-covered 후보지만 최근 validation review가 약해 `COP`보다 후순위 |
| NKE | watch | 0.0223% | same-cycle research-covered 후보지만 rebound review가 약해 `COP`보다 후순위 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | 17:00Z trim fill 2주가 있어 추가 same-session trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | same-day sell fill 22주 때문에 추가 trim 불가 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 |

## 주문 제출과 reconciliation

- Pre-submit gate summary: paper mode `true`, market clock `2026-06-09T13:53:14.173164099-04:00`, order plan `wiki/trade-ledger/orders/2026-06-10-0251-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, `COP` quote freshness `~0.00m`, spread `0.0431%`, order shape `buy 1 / limit 116.14 / day / stock`, duplicate/open-order check `PASS`
- Submitted order: `COP` buy `1` @ `116.14 USD` day limit, `client_order_id=hourly-20260610-0251-buy-cop`
- Alpaca response: `order_id=34da84fa-1653-4852-a955-6a1e0efd3fa8`, initial status `pending_new`
- Immediate reconciliation: `get_order_by_client_id`와 `get_orders(status=all, after=2026-06-09T17:58:00Z, symbols=COP)` 기준 주문은 `status=filled`, `filled_qty=1`, `filled_avg_price=116.05 USD`로 닫혔다. `get_orders(status=open, symbols=COP)`는 0건이었고 `get_account_activities(activity_types=FILL, after=2026-06-09T18:00:00Z)`에는 같은 fill 1건만 추가로 잡혔다.
- Positions/account after submit: `get_all_positions` 기준 positions는 `32` 유지, `COP`는 `3주 -> 4주`, `avg_entry_price=116.8975`, `qty_available=4`로 증가했다. `get_account_info`는 portfolio value `98,245.27 USD`, cash `32,646.58 USD`, buying power `298,881.33 USD`, long market value `65,598.69 USD`를 보여줬다.
- Same-session fills tracked before this submit: `SLB` buy 1 @ `55.11`, `WMT` buy 1 @ `118.70`, `AVGO` sell 2 @ `375.47`, `PFE` buy 1 @ `25.82`, `BAC` buy 1 @ `54.07`, `RGTI` sell 22 @ `22.30`.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | positive research confirmations 4개 유지 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0251-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0251-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0251-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `duplicate_symbol_side_same_day`: 같은 미국 세션에 이미 같은 symbol/side fill이 있어 추가 제출을 막는 규칙이다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 fallback buy를 막는 규칙이다.
- `validation_lifecycle add-block`: due review가 남은 validation buy 종목의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에 적용됐다.
- `provider_error`: Alpha Vantage는 이번 cycle에 one-call-per-hour throttle이 열리지 않아 `provider_error` gap으로만 기록됐고, 나머지 4개 positive research confirmation 덕분에 strict MCP gate는 유지됐다.
