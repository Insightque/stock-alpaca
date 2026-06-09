# 2026-06-10-0331-hourly-autopilot

regular-session scheduled paper autopilot 실행. scheduler-owned `0331` stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP submit-boundary check를 더해 `AMZN` 1주 floor-size validation buy를 제출한 뒤 즉시 체결까지 reconciliation 했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | live Alpaca clock `2026-06-09T14:33:32.700896649-04:00`, regular market open |
| Stale order cleanup | PASS | `0331` cleanup artifact 기준 stale candidate 0건, 남은 open order는 fresh `NVDA` buy 1건뿐 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, live `get_clock/get_account_info/get_orders/get_all_positions/get_account_activities/get_stock_latest_quote/get_asset` 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage `empty_response` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | `AMZN` live IEX quote `245.43/245.48`, spread `0.0204%`, freshness submit boundary `~0.00`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | PASS | registered Alpaca MCP `place_stock_order` accepted, same client id reconciliation 기준 `filled_avg_price=245.40 USD` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AMZN | filled | 0.0204% | research preflight 포함, same-day duplicate 없음, fresh `NVDA` open buy와 다른 cluster, `SPY/QQQ` cap 초과와 `NEE` spread fail 이후 남은 exact hard-gate-passing mega-cap AI/cloud fallback |
| NVDA | watch | open_order | `0311` cycle open buy 1건이 아직 fresh 상태라 same cluster 추가 buy는 열지 않았다 |
| AVGO | watch | duplicate | trim rationale는 유지되지만 17:00Z same-day sell fill 2주 때문에 duplicate sell gate |
| RGTI | watch | duplicate | speculative trim trigger는 유지되나 same-day earlier sell fill 때문에 duplicate sell gate |
| SO | watch | 0.0216% | quote/spread는 통과하지만 trim decision-grade metric gap |
| AAPL | watch | 0.0137% | spread는 가장 좋지만 2026-06-09 review 1D `약함`이 `AMZN`보다 더 약했다 |
| GOOGL | watch | 0.3310% | research-covered mega-cap 후보지만 weak review와 quote inconsistency가 남아 `AMZN`보다 후순위 |
| NEE | watch | 4.8441% | live quote `84.38/88.57`로 spread hard gate fail |
| SPY | watch | 0.0313% | benchmark fallback이지만 1주 ask `735.73 USD`가 validation floor per-order cap 약 `493.61 USD` 초과 |
| QQQ | watch | 0.0284% | benchmark fallback이지만 1주 ask `705.35 USD`가 validation floor per-order cap 약 `493.61 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | 17:00Z trim fill 2주가 있어 추가 same-session trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | same-day sell fill 22주 때문에 추가 trim 불가 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 |

## 주문 제출과 reconciliation

- Pre-submit gate summary: paper mode `true`, market clock `2026-06-09T14:33:32.700896649-04:00`, order plan `wiki/trade-ledger/orders/2026-06-10-0331-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, `AMZN` quote freshness `~0.00m`, spread `0.0204%`, order shape `buy 1 / limit 245.48 / day / stock`, duplicate/open-order check `PASS`
- Submitted order: `AMZN` buy `1` @ `245.48 USD` day limit, `client_order_id=hourly-20260610-0331-buy-amzn`
- Alpaca response: `order_id=7a783061-253f-4c53-8c0e-377e194c469e`, initial status `pending_new`
- Immediate reconciliation: `get_order_by_client_id`, `get_order_by_id`, `get_orders(status=all, symbols=AMZN)`, `get_account_activities(activity_types=FILL)` 기준 주문은 `2026-06-09T18:38:03.133912338Z`에 `filled_avg_price=245.40 USD`로 즉시 체결됐다.
- Positions/account after submit: `get_all_positions` 기준 positions는 `32` 유지, `AMZN`은 `4주 -> 5주`, `avg_entry_price=262.386`, `qty_available=5`로 증가했다. `NVDA` open buy 1건은 계속 `status=new`다. `get_account_info`는 portfolio value `98,762.36 USD`, cash `32,401.18 USD`, buying power `299,705.49 USD`, long market value `66,361.18 USD`를 확인했다.
- Same-session fills tracked before this submit: `COP` buy 1 @ `116.05`, `SLB` buy 1 @ `55.11`, `WMT` buy 1 @ `118.70`, `AVGO` sell 2 @ `375.47`, `PFE` buy 1 @ `25.82`, `BAC` buy 1 @ `54.07`, `RGTI` sell 22 @ `22.30`.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | positive research confirmations 4개 유지 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0331-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-0331-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0331-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `duplicate_symbol_side_same_day`: 같은 미국 세션에 이미 같은 symbol/side fill이 있어 추가 제출을 막는 규칙이다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 fallback buy를 막는 규칙이다.
- `review_backlog_throttle`: pending review 개수에 따라 신규 validation buy 슬롯을 줄이거나 막는 정책인데, 이번 cycle은 `pending_1d_count=0`이라 stop 조건에 닿지 않았다.
- `empty_response`: Alpha Vantage는 이번 cycle에 shortlist 대상 NEWS_SENTIMENT 결과가 비어 `empty_response` gap으로만 기록됐고, 나머지 4개 positive research confirmation 덕분에 strict MCP gate는 유지됐다.
