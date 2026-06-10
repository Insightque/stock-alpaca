# 2026-06-11-0031-hourly-autopilot

## 요약

`0031` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/positions/same-day fills/quotes를 짧게 재확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었고, review backlog는 `pending_1d_count=9`라 신규 buy 슬롯만 `1`개로 축소됐지만 risk-reducing sell/trim 평가는 독립적으로 유지됐다.

sell-first 재평가에서는 `AVGO`와 `RGTI`가 모두 same-day filled trim duplicate에 막혔고 `SO`는 trim decision-grade metric gap이 지속됐다. buy fallback으로 이동한 뒤 `SPY/QQQ`는 validation floor per-order cap, `BAC/WMT/XOM`은 same-day buy duplicate가 남아 `JNJ` 1주 validation buy @ `239.35 USD`를 direct Alpaca MCP로 제출했다. immediate reconciliation 기준 이 주문은 `filled_avg_price=239.23 USD`로 즉시 전량 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` paper mode와 scheduler artifact 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-10T11:37:20.342891003-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha hourly throttle `provider_error` gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`로 buy 슬롯 `1`개로 축소, sell/trim은 비차단 |
| Quote/spread | PASS for JNJ | JNJ quote `239.29/239.35`, spread `0.0251%`, quote age 약 `4.6`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged-deployment warning only |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_duplicate_same_day | 0.1092% | same-day filled trim `hourly-20260610-2251-sell-avgo`가 있어 추가 sell 비허용 |
| RGTI | blocked_duplicate_same_day | 0.1004% | same-day filled trim `hourly-20260610-2311-sell-rgti`가 있어 추가 sell 비허용 |
| SO | blocked_metric_gap | 0.0319% | quote/spread는 정상이나 trim decision-grade expected-excess/replacement margin 공백 지속 |
| JNJ | selected_buy | 0.0251% | healthcare defensive diversifier, research preflight 포함, same-day duplicate/open-order conflict 없음 |
| SLB | backup_buy | 0.0178% | energy-services backup candidate지만 JNJ가 diversification 측면에서 우선 |
| COP | backup_buy | 0.0249% | energy/value backup candidate지만 JNJ가 non-energy diversification 측면에서 우선 |
| SPY | blocked_floor_cap | 0.0096% | 1주 ask가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0257% | 1주 ask가 validation floor per-order cap 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | ai_semiconductor warning band trim trigger는 active지만 same-day filled trim이 이미 있다 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative loss-control trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T11:37:20.342891003-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-11-0031-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; JNJ quote freshness 약 `4.6`분; spread `0.0251%`; order shape `buy 1 share / limit 239.35 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0031` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/JNJ artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| JNJ | buy | 1 | 239.35 | `c1075d80-4584-4f06-8e39-9182570e9f19` | `filled_avg_price=239.23 USD` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle gap only |
| `check-risk-policy.py --json` | PASS | JNJ floor-size validation buy risk gate 통과, staged-deployment warning only |

## 제출 후 정산

- `get_order_by_id`와 `get_order_by_client_id` 기준 `JNJ` 주문은 `filled`다.
- `get_orders(status=all, symbols=JNJ)` 기준 same-day `JNJ` buy order는 1건이며 `filled_qty=1`, `filled_avg_price=239.23 USD`다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `JNJ`는 `1주 -> 2주`, `avg_entry_price=238.385`, `qty_available=2`, `market_value=478.38 USD`로 증가했다.
- `get_account_info` snapshot은 portfolio value `97,745.31 USD`, cash `31,871.99 USD`, buying power `296,720.77 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-10)`는 새 `JNJ` fill 1건과 earlier same-day `XOM/PFE/BAC/WMT` buy fills, `RGTI/AVGO` sell fills, `AAPL` after-hours fills를 반환했다.
- 새 `JNJ` validation buy는 `1D/5D/20D` review bucket에 추가 추적 대상으로 남긴다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0031-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0031-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0031-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0031-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0031-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-11-0031-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `expected_excess_return_20d_pct`: 후보의 향후 20거래일 기대 초과수익 추정치다. 이번 JNJ floor-size validation buy는 정책학습 목적이라 `0.0`을 허용했다.
- `review_backlog_pending_1d_count`: 아직 1D review를 기다리는 validation buy 수다. `9`건이라 신규 buy 슬롯이 `1`개로 축소됐다.
- `spread_pct`: `(ask-bid)/ask*100` 기준 호가 스프레드다. regular-session hard gate는 `0.50%` 이하다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
