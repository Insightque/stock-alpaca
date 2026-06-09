# 2026-06-10-0311-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0311` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 blocking open order `0`건으로 종료됐고 core preflight hard gate도 `pass`였다. 이번 cycle은 required core/research row가 모두 fresh/pass라 preflight evidence를 source-of-record로 유지하면서 registered Alpaca MCP live submit-boundary check를 추가했다.

sell-first 진단에서는 `AVGO`가 post-earnings de-risk trim rationale를 유지하지만 `2026-06-09T17:00:40Z` same-day sell fill 때문에 duplicate symbol/side gate에 막혔고, `RGTI`도 speculative loss-control trim trigger는 남아 있지만 same-day sell fill 22주 때문에 추가 trim이 불가했다. `SO`는 quote/spread는 통과했지만 trim decision-grade metric gap이 이어졌다. buy fallback에서는 `COP`, `SLB`, `WMT`, `PFE`, `BAC`가 모두 same-day buy duplicate로 제외됐고, `SPY/QQQ`는 validation floor per-order cap 초과였다. `AAPL`, `AMZN`, `GOOGL`, `NKE`는 recent review 약세로 `NVDA`보다 후순위였다. 남은 research-covered fallback 중 `NVDA`가 2026-06-09 analyst review 기준 `2026-06-05 ET` fill 1D `-0.03%`, `SPY` 대비 `-0.28%p`의 `중립 양호` 판정을 유지했고, live IEX quote `205.37/205.40` spread `0.0146%`, same-day duplicate/open-order conflict 부재, active/tradable NASDAQ stock 조건을 충족해 floor-size validation buy로 선택됐다. direct Alpaca MCP `place_stock_order` 제출 후 immediate reconciliation 기준 주문은 `status=new` open order다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | live Alpaca clock `2026-06-09T14:15:36.189974147-04:00`, regular market open |
| Stale order cleanup | PASS | `0311` cleanup artifact 기준 stale/open autopilot order 모두 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, live `get_clock/get_account_info/get_orders/get_all_positions/get_account_activities/get_stock_latest_quote/get_asset` 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage throttled `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | `NVDA` live IEX quote `205.37/205.40`, spread `0.0146%`, freshness submit boundary `~0.00`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | PASS | registered Alpaca MCP `place_stock_order` accepted, same client id reconciliation 기준 `status=new` open order |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| NVDA | open_order_new | 0.0146% | research preflight 포함, 2026-06-09 review `중립 양호`, same-day duplicate/open-order conflict 없음, ai_semiconductor_complex warning band 아래에서 1주 floor-size add |
| AVGO | watch | duplicate | trim rationale는 유지되지만 17:00Z same-day sell fill 2주 때문에 duplicate sell gate |
| RGTI | watch | duplicate | speculative trim trigger는 유지되나 same-day earlier sell fill 때문에 duplicate sell gate |
| SO | watch | 0.0325% | quote/spread는 통과하지만 trim decision-grade metric gap |
| AAPL | watch | 0.0104% | mega-cap quality thesis는 유지되지만 2026-06-09 portfolio review 1D가 `약함`이라 NVDA보다 후순위 |
| AMZN | watch | 0.0245% | AI/cloud label 대비 recent validation follow-through가 약해 NVDA보다 후순위 |
| GOOGL | watch | 0.0247% | quote/spread는 양호하지만 recent review와 replacement rank가 NVDA보다 약함 |
| NKE | watch | 0.0223% | consumer turnaround review 약세가 남아 floor-size 우선순위가 낮다 |
| SPY | watch | 0.0123% | benchmark fallback이지만 1주 ask `732.66 USD`가 validation floor per-order cap 약 `491.32 USD` 초과 |
| QQQ | watch | 0.0171% | benchmark fallback이지만 1주 ask `700.75 USD`가 validation floor per-order cap 약 `491.32 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | 17:00Z trim fill 2주가 있어 추가 same-session trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | same-day sell fill 22주 때문에 추가 trim 불가 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 |

## 주문 제출과 reconciliation

- Pre-submit gate summary: paper mode `true`, market clock `2026-06-09T14:15:36.189974147-04:00`, order plan `wiki/trade-ledger/orders/2026-06-10-0311-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, `NVDA` quote freshness `~0.00m`, spread `0.0146%`, order shape `buy 1 / limit 205.40 / day / stock`, duplicate/open-order check `PASS`
- Submitted order: `NVDA` buy `1` @ `205.40 USD` day limit, `client_order_id=hourly-20260610-0311-buy-nvda`
- Alpaca response: `order_id=56d0bb25-b51d-40e5-8ba9-f76ab79d67ae`, initial status `pending_new`
- Immediate reconciliation: `get_order_by_id`와 `get_orders(status=open, symbols=NVDA)` / `get_orders(status=all, after=2026-06-09T18:15:00Z, symbols=NVDA)` 기준 주문은 `status=new`, `filled_qty=0` open order다. `get_account_activities(activity_types=FILL, after=2026-06-09T18:18:00Z)`에는 신규 fill이 아직 없다.
- Positions/account after submit: `get_all_positions` 기준 positions는 `32` 유지, `NVDA`는 아직 `38주`, `avg_entry_price=215.031579`, `qty_available=38`로 unchanged다. `get_account_info`는 portfolio value `98,401.87 USD`, cash `32,646.58 USD`, buying power `299,061.16 USD`, long market value `65,755.29 USD`를 보여줬다.
- Same-session fills tracked before this submit: `COP` buy 1 @ `116.05`, `SLB` buy 1 @ `55.11`, `WMT` buy 1 @ `118.70`, `AVGO` sell 2 @ `375.47`, `PFE` buy 1 @ `25.82`, `BAC` buy 1 @ `54.07`, `RGTI` sell 22 @ `22.30`.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | positive research confirmations 4개 유지 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0311-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0311-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0311-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `duplicate_symbol_side_same_day`: 같은 미국 세션에 이미 같은 symbol/side fill이 있어 추가 제출을 막는 규칙이다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 fallback buy를 막는 규칙이다.
- `review_backlog_throttle`: pending review 개수에 따라 신규 validation buy 슬롯을 줄이거나 막는 정책인데, 이번 cycle은 `pending_1d_count=0`이라 stop 조건에 닿지 않았다.
- `provider_error`: Alpha Vantage는 이번 cycle에 one-call-per-hour throttle이 열리지 않아 `provider_error` gap으로만 기록됐고, 나머지 4개 positive research confirmation 덕분에 strict MCP gate는 유지됐다.
