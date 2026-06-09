# 2026-06-10-0231-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0231` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 blocking open order `0`건으로 종료됐고 core preflight hard gate도 `pass`였다. 이번 cycle은 preflight core/research evidence를 유지한 상태에서 registered Alpaca MCP live submit-boundary check를 다시 수행했다.

sell-first 진단에서는 `AVGO`가 post-earnings de-risk trim rationale를 유지하지만 `2026-06-09T17:00:40Z` same-day sell fill 때문에 duplicate symbol/side gate에 막혔고, `RGTI`도 speculative loss-control trim trigger는 남아 있지만 same-day sell fill 22주 때문에 추가 trim이 불가했다. `SO`는 live quote/spread는 통과했지만 trim decision-grade metric gap이 이어졌다. buy fallback에서는 `WMT`, `PFE`, `BAC`가 same-day buy duplicate로 제외됐고, preflight 기준 유력했던 `GOOGL`은 live submit-boundary quote `352.00/363.23`로 spread hard gate를 통과하지 못했다. `SPY/QQQ`는 validation floor per-order cap 초과, `NOK`는 validation_lifecycle add-block이 남았다. 남은 executable fallback 중 `SLB`가 2026-06-09 analyst review 기준 `2026-06-05 ET` fill 1D `+1.58%`, energy-services diversifier 역할, Yahoo/SEC/FRED/Firecrawl positive confirmation, live quote `55.10/55.11` spread `0.0181%`를 모두 충족해 floor-size validation buy로 선택됐고 direct Alpaca MCP `place_stock_order` 제출 후 immediate reconciliation 기준 `status=new` open order로 남아 있다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | live Alpaca clock `2026-06-09T13:35:39.783355115-04:00`, regular market open |
| Stale order cleanup | PASS | `0231` cleanup artifact 기준 stale/open autopilot order 모두 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, live `get_clock/get_account_info/get_orders/get_all_positions/get_account_activities/get_stock_latest_quote` 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage throttled `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | `SLB` live quote `55.10/55.11`, spread `0.0181%`, freshness submit boundary `~0.00`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | PASS | registered Alpaca MCP `place_stock_order` accepted, immediate reconciliation 기준 `status=new` open order |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SLB | open order | 0.0181% | same-day duplicate/open-order conflict 없음, 2026-06-09 analyst review 1D `양호`, energy-services diversifier 역할, per-order cap 이내 |
| AVGO | watch | 0.1654% | trim rationale는 유지되지만 17:00Z same-day sell fill 2주 때문에 duplicate sell gate |
| RGTI | watch | 0.0519% | speculative trim trigger는 유지되나 same-day earlier sell fill 때문에 duplicate sell gate |
| SO | watch | 0.0216% | quote/spread는 통과하지만 trim decision-grade metric gap |
| WMT | watch | duplicate | 17:19Z same-day buy fill 1주 |
| PFE | watch | duplicate | 17:00Z same-day buy fill 1주 |
| BAC | watch | duplicate | 14:45Z same-day buy fill 1주 |
| GOOGL | watch | 3.1903% | live submit-boundary spread hard gate fail |
| SPY | watch | 0.0397% | 1주 ask `731.37 USD`가 validation floor per-order cap 약 `490.35 USD` 초과 |
| QQQ | watch | 0.0071% | 1주 ask `699.81 USD`가 validation floor per-order cap 약 `490.35 USD` 초과 |
| NOK | watch | 0.0733% | `review-due-index` add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | 17:00Z trim fill 2주가 있어 추가 same-session trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | same-day sell fill 22주 때문에 추가 trim 불가 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 |

## 주문 제출과 reconciliation

- Pre-submit gate summary: paper mode `true`, market clock `2026-06-09T13:35:39.783355115-04:00`, order plan `wiki/trade-ledger/orders/2026-06-10-0231-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, `SLB` quote freshness `~0.00m`, spread `0.0181%`, order shape `buy 1 / limit 55.11 / day / stock`, duplicate/open-order check `PASS`
- Submitted order: `SLB` buy `1` @ `55.11 USD` day limit, `client_order_id=hourly-20260610-0231-buy-slb`
- Alpaca response: `order_id=d225a67d-6bc2-4488-99f3-d45a48bf6f4e`, initial status `pending_new`
- Immediate reconciliation: `get_order_by_client_id`와 `get_orders(status=all, after=2026-06-09T17:35:00Z, symbols=SLB)` 기준 주문은 `status=new`, `filled_qty=0` open order다. `get_orders(status=open, symbols=SLB)`도 동일 1건을 보여줬고 `get_account_activities(activity_types=FILL, after=2026-06-09T17:35:00Z)`에는 신규 fill이 없었다.
- Positions/account after submit: `get_all_positions` 기준 positions는 `32` 유지, `SLB`는 아직 `4주`, `qty_available=4`로 unchanged다. `get_account_info`는 portfolio value `98,253.83 USD`, cash `32,817.74 USD`, buying power `298,988.03 USD`, long market value `65,436.09 USD`를 보여줬다.
- Same-session fills tracked before this submit: `WMT` buy 1 @ `118.70`, `AVGO` sell 2 @ `375.47`, `PFE` buy 1 @ `25.82`, `BAC` buy 1 @ `54.07`, `RGTI` sell 22 @ `22.298182`.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | positive research confirmations 4개 유지 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0231-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0231-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0231-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `duplicate_symbol_side_same_day`: 같은 미국 세션에 이미 같은 symbol/side fill이 있어 추가 제출을 막는 규칙이다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 fallback buy를 막는 규칙이다.
- `validation_lifecycle add-block`: due review가 남은 validation buy 종목의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에 적용됐다.
- `provider_error`: Alpha Vantage는 이번 cycle에 one-call-per-hour throttle이 열리지 않아 `provider_error` gap으로만 기록됐고, 나머지 4개 positive research confirmation 덕분에 strict MCP gate는 유지됐다.
