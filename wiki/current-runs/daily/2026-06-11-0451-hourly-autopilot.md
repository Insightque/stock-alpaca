# 2026-06-11-0451-hourly-autopilot

## 요약

`0451` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, stale cleanup/open-order rows 모두 `0`건으로 유지됐다. `0431` cycle에서 open/new였던 `MSFT` buy 1주는 이번 preflight recent fills 기준 `2026-06-10T19:47:34.876997Z`, `398.38 USD`에 체결되어 보유 수량이 `1주 -> 2주`, `avg_entry_price=412.58`로 갱신됐다.

sell-first 재평가에서는 `AVGO`가 ai_semiconductor warning-band trim rationale를 유지했지만 live spread `0.6118%`로 policy cap `0.50%`를 넘었고 same-day sell duplicate도 남았다. `RGTI`는 spread `0.1013%`로 정상이나 same-day sell duplicate가 추가 trim을 막았고, `SO`는 quote/spread `0.0319%`를 통과했지만 trim decision-grade metric gap이 지속됐다. buy fallback에서는 `GOOGL` weak review, `NVDA` same-cluster add block, `PLTR` low-confidence speculative profile, `MSFT` same-day buy duplicate, `SPY/QQQ` validation floor per-order cap이 남아 `UNH`가 가장 보수적인 floor-size learning order 후보로 올라왔다. 다만 실제 `place_stock_order` 직전 live Alpaca clock이 `2026-06-10T16:00:30.547773652-04:00`로 regular close를 넘겨 final hard gate `market_open`이 닫혔고, 이번 cycle은 `orders: []` no-submit으로 종료한다.

연구 MCP는 tiered pass를 유지했다. `SEC EDGAR/FRED/Firecrawl/Yahoo Finance`는 pass였고, `Alpha Vantage`는 `NEWS_SENTIMENT` empty-response gap만 남았지만 최소 confirmation 수는 충족했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler artifact와 workflow policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock preflight | PASS | scheduler Alpaca clock `2026-06-10T15:51:10.349148231-04:00`, regular market open |
| Stale order lifecycle | PASS | `0451` stale cleanup artifact와 core preflight open-orders row 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass, account/positions/open-orders/recent-fills/quotes 모두 usable |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `empty_response` gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`라 신규 buy 슬롯은 `1`개로 축소되지만 stop threshold `12` 미만 |
| Quote/spread | PASS for UNH | `406.81/406.90`, spread `0.0221%`, quote age 약 `0.09`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Submit boundary market clock | BLOCK | live Alpaca clock `2026-06-10T16:00:30.547773652-04:00`로 regular market closed |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_spread_and_duplicate | 0.6118% | trim rationale는 유지되지만 spread hard gate fail과 same-day sell duplicate가 겹친다 |
| RGTI | blocked_duplicate_same_day | 0.1013% | speculative loss-control trigger는 active지만 same-day sell duplicate가 남는다 |
| SO | blocked_metric_gap | 0.0319% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| UNH | blocked_market_closed_submit_boundary | 0.0221% | universe/MCP/risk/duplicate/asset/quote gate를 모두 통과했지만 live market clock이 close로 전환됐다 |
| GOOGL | blocked_weak_review | 0.0197% | quote/spread는 양호하지만 recent weak review가 candidate floor를 막는다 |
| NVDA | blocked_same_cluster_add_block | 0.0149% | ai_semiconductor_complex warning-band add block 유지 |
| PLTR | blocked_low_confidence_speculative | 0.0153% | speculative growth 프로필과 낮은 reusable confidence가 UNH보다 열위다 |
| MSFT | blocked_same_day_duplicate | 0.1131% | 이번 cycle 초반에 `398.38 USD` 체결이 확정되어 same-day buy duplicate가 된다 |
| SPY | blocked_floor_cap | 0.0165% | 1주 ask `727.28 USD`가 validation floor per-order cap 약 `487.04 USD`를 초과 |
| QQQ | blocked_floor_cap | 0.0201% | 1주 ask `696.21 USD`가 validation floor per-order cap 약 `487.04 USD`를 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_within_policy | spread fail과 same-day sell duplicate가 함께 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

### 제출 직전 게이트 요약

paper mode `true`; market clock `2026-06-10T16:00:30.547773652-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-11-0451-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; UNH quote freshness 약 `0.09`분; spread `0.0221%`; order shape `buy 1 share / limit 406.90 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0451` stale cleanup/core/research preflight, runtime gate snapshot, review index, `UNH/MSFT` ticker artifacts다. final blocker는 `market_open`이다.

- Planned orders before boundary check: `UNH` buy 1주 @ `406.90 USD` day limit
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Immediate reconciliation: no-submit result. live Alpaca MCP 기준 account `ACTIVE`, positions `33`, open orders `0`, cash `30,865.37 USD`, portfolio value `97,098.83 USD`, long market value `66,233.46 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha empty-response gap only |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0451-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0451-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0451-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0451-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0451-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소된다.
- `submit boundary market clock`: scheduler preflight가 열려 있어도 실제 `place_stock_order` 직전 live Alpaca clock이 close로 넘어가면 submit을 중단해야 한다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 benchmark fallback 매수는 막는다.
