# 2026-06-10-2351-hourly-autopilot

## 요약

`2351` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/positions/same-day fills/quotes를 짧게 재확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었고, review backlog는 `pending_1d_count=9`라 신규 buy 슬롯만 `1`개로 축소됐지만 risk-reducing sell/trim은 독립적으로 유지됐다.

sell-first 재평가에서는 `RGTI`와 `AVGO`가 모두 same-day filled trim duplicate에 막혔고 `SO`는 spread 정상화 후에도 decision-grade metric gap이 남았다. buy fallback으로 이동한 뒤 `BAC`와 `WMT`는 same-day buy duplicate, `SPY/QQQ`는 validation floor per-order cap 초과로 제외됐고, `PFE` 1주 validation buy @ `25.72 USD`를 direct Alpaca MCP로 제출했다. immediate reconciliation 기준 이 주문은 `filled_avg_price=25.70 USD`로 즉시 전량 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` paper mode와 scheduler artifact 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-10T10:53:16.865053926-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `empty_response` gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`로 buy 슬롯 `1`개로 축소, sell/trim은 비차단 |
| Quote/spread | PASS for PFE | PFE live quote `25.71/25.72`, spread `0.0389%`, quote age 약 `0.00`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS 예정 구조, 이후 validator 실측 PASS로 확인 |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | blocked_duplicate_same_day | 0.0976% | speculative loss-control trim trigger는 active지만 2311 cycle same-day filled trim이 있어 추가 sell 비허용 |
| AVGO | blocked_duplicate_same_day | 1.3158% | 2251 cycle same-day filled trim이 있고 live spread도 widened 상태 |
| SO | blocked_metric_gap | 0.0320% | quote/spread는 정상이나 trim decision-grade expected-excess/replacement margin 공백 지속 |
| BAC | blocked_duplicate_same_day | 0.0183% | 2331 cycle same-day buy fill `hourly-20260610-2331-buy-bac` 이미 존재 |
| PFE | selected_buy | 0.0389% | existing healthcare diversifier, research confirmation 유지, same-day duplicate/open-order conflict 없음 |
| WMT | blocked_duplicate_same_day | 0.0336% | same-day buy fill `hourly-20260610-2231-buy-wmt` 이미 존재 |
| SPY | blocked_floor_cap | 0.0054% | 1주 ask `734.85 USD`가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0892% | 1주 ask `706.57 USD`가 validation floor per-order cap 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | duplicate_symbol_side_same_day | 2311 cycle trim 직후라 추가 staged trim은 same-day duplicate discipline에 막힘 |
| AVGO | watch | duplicate_symbol_side_same_day | 2251 cycle trim 체결이 same-day conflict를 만들고 live spread도 widened |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남음 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T10:53:16.865053926-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-10-2351-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; PFE quote freshness 약 `0.00`분; spread `0.0389%`; order shape `buy 1 share / limit 25.72 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `2351` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/PFE artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| PFE | buy | 1 | 25.72 | `e010464f-f482-491e-bc31-76dcffb1730c` | `filled_avg_price=25.70 USD` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha empty-response gap only |
| `check-risk-policy.py --json` | PASS | PFE floor-size validation buy risk gate 통과 |

## 제출 후 정산

- `get_order_by_id`와 `get_orders(status=all, symbols=PFE)` 기준 `PFE` 주문은 `filled`다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `PFE`는 `5주 -> 6주`, `avg_entry_price=26.033333`, `qty_available=6`으로 증가했다.
- `get_account_info` snapshot은 portfolio value `98,606.28 USD`, cash `32,262.63 USD`, buying power `299,380.66 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-10)`는 새 `PFE` fill 1건과 earlier same-day `BAC` buy 1 fill, `RGTI` sell 2 fills, `AVGO` sell 2 fills, `WMT` buy 1 fill, `AAPL` buy 2 fills를 반환했다.
- 새 `PFE` validation buy는 `1D/5D/20D` review bucket에 추가 추적 대상으로 남긴다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-2351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-2351-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-2351-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-2351-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-10-2351-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소되지만 sell/trim 진단은 독립적으로 유지된다.
- `duplicate_symbol_side_same_day`: 같은 정규장 날짜에 동일 symbol/side filled order가 이미 있으면 추가 submit을 막는 규칙이다.
- `validation_floor_per_order_cap`: floor-size 학습 주문도 `max_validation_notional_pct_per_order` cap을 넘을 수 없다는 규칙이다.
- `empty_response`: 이번 run의 Alpha Vantage는 shortlisted symbols에 대해 usable candidate news item을 반환하지 않았고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
