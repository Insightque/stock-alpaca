# 2026-06-17-2231-hourly-autopilot scheduled paper autopilot

## 요약

`2231` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-17T09:31:12.026866031-04:00`, account `ACTIVE`, positions `33`, open orders `0`, fresh IEX quote rows는 decision time 기준 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 충족했고, `Alpha Vantage`는 shortlisted symbols 뉴스 `0건`으로 `empty_response` gap, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

sell-first 평가에서는 `SO`가 trim decision-grade metric gap 때문에, `RGTI`와 `PFE`는 current quote spread가 각각 `2.0115%`, `10.2919%`로 policy cap `0.50%`를 넘어 executable trim으로 승격되지 못했다. buy fallback에서는 `SPY/QQQ`가 validation floor per-order cap 약 `507.02 USD`를 초과했고, `AMZN/GOOGL/COP`는 recent review 및 replacement rank 기준 `BAC`보다 후순위였다. 따라서 `BAC` 1주 validation buy를 `57.57 USD` day limit로 제출했다. immediate reconciliation 기준 order `bf01712f-be9d-4b0e-a7fb-0ec8b36e6eee`는 `status=new`, `filled_qty=0` open order이며 `BAC` position qty는 아직 `7주`로 unchanged다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T09:38:13.218016511-04:00`, regular market open |
| Stale order lifecycle | PASS | `2231` stale cleanup artifact 기준 stale candidates/open orders 모두 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, quote rows fresh |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha empty-response gap, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for BAC | live BAC quote `57.56/57.57`, spread `0.0174%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 BAC 1주 buy risk gate 통과 |
| Final submit path | PASS | BAC는 same-day duplicate/open-order conflict 없음, floor-size learning directive 충족 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.2877% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| RGTI | blocked_spread_fail_sell | 2.0115% | speculative trim trigger는 유지되지만 current spread가 policy cap 초과 |
| PFE | blocked_spread_fail_sell | 10.2919% | repeated weak-review trim rationale는 유지되지만 current spread가 policy cap 초과 |
| BAC | submitted_buy | 0.0174% | financials diversifier, 3-provider positive confirmation, same-day duplicate/open-order conflict 없음 |
| AMZN | lower_rank_backup | 0.0532% | current spread는 양호하지만 누적 weak-review history로 BAC보다 후순위 |
| GOOGL | lower_rank_backup | 0.1589% | mixed weak-review history와 mega-cap replacement rank 약화로 BAC보다 후순위 |
| COP | lower_rank_backup | 0.1982% | recent reversal evidence 때문에 BAC보다 후순위 |
| SPY | blocked_validation_floor_cap | 0.0972% | 1주 ask `751.16 USD`가 validation floor per-order cap을 초과 |
| QQQ | blocked_validation_floor_cap | 0.0259% | 1주 ask `734.01 USD`가 validation floor per-order cap을 초과 |
| NOK | blocked_validation_lifecycle_add_block | 0.0702% | review-due add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `spread_within_policy` | current spread `2.0115%`가 cap `0.50%` 초과 |
| PFE | watch | `spread_within_policy` | current spread `10.2919%`가 cap `0.50%` 초과 |

## 주문/체결

- Planned order: `BAC` buy `1` @ `57.57 USD` day limit
- `place_stock_order`: `BAC` buy 1주, `client_order_id=hourly-20260617-2231-buy-bac`, `order_id=bf01712f-be9d-4b0e-a7fb-0ec8b36e6eee`
- Immediate reconciliation: `get_order_by_client_id` 기준 상태는 `new`, `filled_qty=0`, `filled_avg_price=null`이다.
- Open orders after submit: `BAC` buy 1건 `status=new`
- Same US-date fills seen during reconciliation: `PFE` sell 1주 `26.03 USD`, `RGTI` sell 1주 `20.96 USD`
- Post-trade position check: `BAC qty=7`, `avg_entry_price=53.738571`, account cash `30,391.78 USD`, portfolio value `101,316.75 USD`, buying power `304,425.48 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gaps |
| `check-risk-policy.py --json` | PASS | BAC 1주 buy notional `57.34 USD`; staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-17-2231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-17-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-2231-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-17-2231-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-17-2231-hourly-autopilot-post-trade.json`

## 지표 설명

- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `507.02 USD`라 `SPY/QQQ` 1주가 초과했다.
- `sell_metric_gap`: sell_candidate_diagnostics는 남기되 trim submit에 필요한 decision-grade expected-excess/replacement margin이 비어 있으면 sell-first 경로로 승격하지 않는다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.
