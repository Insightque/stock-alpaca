# 2026-06-10-0211-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0211` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 blocking open order `0`건으로 종료됐고 core preflight hard gate도 `pass`였다. 이번 cycle은 preflight quote가 decision time 기준 20분 이내라 Alpaca core coverage를 scheduler evidence로 확정한 뒤 sell/trim을 먼저 재평가했다.

sell-first 진단에서는 `AVGO`가 post-earnings de-risk trim rationale를 유지하지만 `2026-06-09T17:00:40Z` same-day sell fill 때문에 duplicate symbol/side gate에 막혔고, `RGTI`도 speculative loss-control trim trigger는 남아 있지만 same-day sell fill 22주 때문에 추가 trim이 불가했다. `SO`는 quote/spread는 통과했지만 trim decision-grade metric gap이 이어졌다. buy fallback에서는 `PFE`와 `BAC`가 same-day buy duplicate, `GOOGL`은 spread `0.9829%` fail, `SPY/QQQ`는 validation floor per-order cap 초과, `NOK`는 validation_lifecycle add-block으로 제외됐다. 남은 eligible fallback 중 `WMT`가 최근 1D review `중립 양호`, Yahoo recommendation breadth, consumer defensive diversifier 역할, quote `118.79/118.84` spread `0.0421%`, review backlog throttle 비차단을 모두 충족해 floor-size validation buy로 선택됐고 direct Alpaca MCP `place_stock_order` 제출 후 `118.70 USD`에 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler Alpaca clock `2026-06-09T13:11:11.215116244-04:00`, regular market open |
| Stale order cleanup | PASS | `0211` cleanup artifact 기준 stale/open autopilot order 모두 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, quotes/assets/orders/activities 포함 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage `empty_response` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | `WMT` quote `118.79/118.84`, spread `0.0421%`, freshness submit boundary 약 `0.03`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | PASS | registered Alpaca MCP `place_stock_order` 성공, same client id reconciliation 기준 즉시 fill |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| WMT | filled | 0.0421% | same-day duplicate/open-order conflict 없음, 1D review `중립 양호`, defensive diversifier 역할, per-order cap 이내 |
| AVGO | watch | 0.2591% | trim rationale는 유지되지만 17:00Z same-day sell fill 2주 때문에 duplicate sell gate |
| RGTI | watch | 0.0523% | speculative trim trigger는 유지되나 same-day earlier sell fill 때문에 duplicate sell gate |
| SO | watch | 0.0323% | quote/spread는 통과하지만 trim decision-grade metric gap, buy fallback final rank는 WMT보다 낮음 |
| PFE | watch | 0.0388% | 17:00Z same-day buy fill 때문에 duplicate buy gate |
| BAC | watch | 0.0186% | 14:45Z same-day buy fill 때문에 duplicate buy gate |
| GOOGL | watch | 0.9829% | spread hard gate fail |
| SPY | watch | 0.0261% | 1주 ask `727.95 USD`가 validation floor per-order cap 약 `487.32 USD` 초과 |
| QQQ | watch | 0.0144% | 1주 ask `695.20 USD`가 validation floor per-order cap 약 `487.32 USD` 초과 |
| NOK | watch | 0.0738% | `review-due-index` add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | 17:00Z trim fill 2주가 있어 추가 same-session trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | same-day sell fill 22주 때문에 추가 trim 불가 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 |

## 주문 제출과 reconciliation

- Pre-submit gate summary: paper mode `true`, market clock `2026-06-09T13:11:11.215116244-04:00`, order plan `wiki/trade-ledger/orders/2026-06-10-0211-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, WMT quote freshness `~0.03m`, spread `0.0421%`, order shape `buy 1 / limit 118.84 / day / stock`, duplicate/open-order check `PASS`
- Submitted order: `WMT` buy `1` @ `118.84 USD` day limit, `client_order_id=hourly-20260610-0211-buy-wmt`
- Alpaca response: `order_id=40066752-96cc-4225-aa77-0e6ba6c7ccb3`, initial status `pending_new`
- Immediate reconciliation: `get_order_by_client_id`와 `get_orders(status=all, after=2026-06-09T17:10:00Z, symbols=WMT)` 기준 주문은 `status=filled`, `filled_qty=1`, `filled_avg_price=118.70 USD`로 닫혔다. `get_orders(status=open, symbols=WMT)`는 0건이다.
- Positions/account after submit: `get_all_positions` 기준 `32` positions 유지, `WMT`는 `6주 -> 7주`, `avg_entry_price=118.165715`, `qty_available=7`로 증가했다. `get_account_info`는 portfolio value `97,900.12 USD`, cash `32,817.74 USD`, buying power `298,103.41 USD`, long market value `65,082.38 USD`를 보여줬다.
- Same-session fills now tracked: `WMT` buy 1 @ `118.70`, `AVGO` sell 2 @ `375.47`, `PFE` buy 1 @ `25.82`, `BAC` buy 1 @ `54.07`, `RGTI` sell 22 @ `22.298182`.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | positive research confirmations 4개 유지 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0211-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0211-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0211-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0211-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0211-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `duplicate_symbol_side_same_day`: 같은 미국 세션에 이미 같은 symbol/side fill이 있어 추가 제출을 막는 규칙이다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 fallback buy를 막는 규칙이다.
- `validation_lifecycle add-block`: due review가 남은 validation buy 종목의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에 적용됐다.
- `empty_response`: Alpha Vantage는 이번 cycle에 candidate news item을 찾지 못해 `empty_response` gap으로만 기록됐고, 나머지 4개 positive research confirmation 덕분에 strict MCP gate는 유지됐다.
