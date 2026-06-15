# 2026-06-16-0031-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0031` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. account snapshot은 portfolio value `102,507.05 USD`, cash `32,372.35 USD`, positions `33`건이었다.

이번 cycle은 sell-first 경로를 먼저 재평가했지만 `AVGO`와 `RGTI`는 same-day duplicate sell discipline에, `SO`는 trim decision-grade metric gap에 막혔다. buy fallback에서는 `SPY/QQQ`가 validation floor per-order cap을 넘고 `BAC`는 same-day duplicate buy가 남았다. `NEE`는 research preflight shortlist 포함, FRED macro confirmation으로 rate-sensitive critical source rule을 통과하며, fresh quote `85.80/85.81`, spread `0.0117%`, same-day duplicate/open-order conflict 없음, held utilities diversifier라는 조건을 충족해 floor-size learning buy 1주 후보로 승격됐다. direct Alpaca MCP `place_stock_order`는 `2026-06-15T15:37:52Z`에 `client_order_id=hourly-20260616-0031-buy-nee`를 제출했고, immediate reconciliation 기준 `2026-06-15T15:37:52.982253179Z` `filled_avg_price=85.78 USD`로 즉시 체결됐다. post-trade readback 기준 open orders `0`, cash `32,286.57 USD`, `NEE qty=5 -> 6`, `avg_entry_price=86.33 USD`다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler core preflight `2026-06-15T11:31:09.44830553-04:00`, regular market open |
| Stale order cleanup | PASS | scheduler cleanup `status=pass`, stale candidate `0`, remaining open order `0` |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate `pass`, positions `33`, open orders row `0` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage `provider_error` gap only |
| Universe strict | PASS | metadata universe `62`개, `SPY/QQQ` 포함 |
| Quote/spread | PASS | `NEE` quote `85.80/85.81`, spread `0.0117%`, freshness `0.08`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `place_stock_order` executed and immediate fill confirmed |

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| NEE | selected_validation_buy | utilities diversifier, FRED macro confirmation, same-day duplicate/open-order 0, spread pass |
| AVGO | watch | `2026-06-15 11:18 ET` same-session trim fill이 이미 있고 current spread `0.6510%`도 hard cap 초과 |
| RGTI | watch | `2026-06-15 09:41 ET` same-session trim fill 9주 때문에 duplicate sell gate |
| SO | watch | trim decision-grade expected-excess/replacement margin 공백 지속 |
| AAPL | watch | mega-cap quality add는 가능하지만 이번 cycle은 utilities diversifier observation value가 더 컸다 |
| AMZN | watch | quote/spread는 양호하지만 diversification 기여가 `NEE`보다 약하다 |
| GOOGL | watch | quote/spread는 양호하지만 mega-cap replacement rank가 `NEE`보다 낮다 |
| NKE | watch | consumer turnaround review 약세가 남아 `NEE`보다 후순위 |
| SPY | watch | 1주 ask `755.21 USD`가 validation floor per-order cap 약 `512.54 USD` 초과 |
| QQQ | watch | 1주 ask `743.19 USD`가 validation floor per-order cap 약 `512.54 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | `duplicate_symbol_side_same_day` | same-session trim fill이 이미 있고 current spread `0.6510%`도 hard cap 초과 |
| RGTI | watch | `duplicate_symbol_side_same_day` | same-session filled trim 9주가 있어 추가 sell 차단 |
| SO | watch | `sell_metric_gap` | spread는 pass지만 trim decision-grade metric gap 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-15T11:31:09.44830553-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-0031-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; NEE quote freshness `0.08`분; spread `0.0117%`; order shape `buy 1 share / limit 85.81 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0031` stale cleanup/core/research preflight, `review-due-index`, `2026-06-15-portfolio-review`, `[[NEE]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| NEE | buy | 1 | 85.81 | filled | 85.78 | `fcf11144-3fe4-427e-84ec-418a59774883` |

- `place_stock_order` actual submit: `2026-06-15T15:37:52.039512771Z`
- `get_order_by_client_id` immediate reconciliation: `status=filled`, `filled_qty=1`, `filled_avg_price=85.78 USD`
- `get_orders(status=open)` immediate reconciliation: `0`건
- `get_all_positions` immediate reconciliation: `NEE qty=6`, `avg_entry_price=86.33`, positions 총 `33`건
- `get_account_info` immediate reconciliation: cash `32,286.57 USD`, portfolio value `102,518.43 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha provider-error gap only |
| `check-risk-policy.py --json` | PASS | NEE floor-size buy order plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-0031-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-0031-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-0031-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-0031-hourly-autopilot-runtime-gate-evaluation.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-16-0031-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-0031-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass_tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `duplicate_symbol_side_same_day`: 같은 세션에 이미 체결된 동일 symbol/side order가 있어 추가 학습 주문을 막는 규칙이다.
- `sell_metric_gap`: trim 판단에 필요한 expected-excess 또는 replacement margin이 비어 있어 집행형 trim으로 승격하지 못한 상태다.
- `validation floor per-order cap`: `portfolio_value * 0.5%` 상한이다. 이번 cycle의 cap은 약 `512.54 USD`라 `SPY/QQQ` 1주가 초과했다.
