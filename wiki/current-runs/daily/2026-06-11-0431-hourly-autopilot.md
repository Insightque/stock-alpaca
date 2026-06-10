# 2026-06-11-0431-hourly-autopilot

## 요약

`0431` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. 이번 cycle은 required core row가 모두 fresh/pass라 추가 Alpaca read-only MCP 호출 없이 scheduler evidence로 regular market open, ACTIVE account, positions `33`, open orders `0`, same-day fills, fresh quote rows를 확정했고, strict universe/MCP/risk validator도 모두 통과했다.

sell-first 재평가에서는 `AVGO`가 ai_semiconductor warning-band trim rationale는 유지되지만 live spread `0.7981%`로 policy cap `0.50%`를 넘었고 same-day sell duplicate도 남았다. `RGTI`는 spread `0.1019%`로 정상이나 same-day sell duplicate가 추가 trim을 막았고, `SO`는 quote/spread `0.0952%`를 통과했지만 trim decision-grade metric gap이 지속됐다. buy fallback에서는 `FCX/WMT/AMZN/BAC/NEE` same-day buy duplicate, `GOOGL` weak review, `NVDA` same-cluster add block, `PLTR` low-confidence speculative profile, `INTC` prior weak exit-thesis history, `SPY/QQQ` validation floor per-order cap이 남아 `MSFT`가 가장 보수적인 floor-size learning order로 승격됐다. direct Alpaca MCP submit 결과 `client_order_id=hourly-20260611-0431-buy-msft`, `order_id=bbaadb29-91e7-4507-a59f-218c0cefc5ea`가 생성됐고 immediate reconciliation 기준 상태는 `new`, `filled_qty=0` open order다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler artifact와 workflow policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler Alpaca clock `2026-06-10T15:31:10.527821336-04:00`, regular market open |
| Stale order lifecycle | PASS | `0431` stale cleanup artifact와 submit 후 `get_orders(status=open)` 비교 기준 stale open order 없음 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass, account/positions/open-orders/recent-fills/quotes 모두 usable |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha throttle `provider_error` only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`라 신규 buy 슬롯은 `1`개, sell/trim은 비차단 |
| Quote/spread | PASS for MSFT | `398.32/398.38`, spread `0.0151%`, quote age 약 `0.06`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_spread_and_duplicate | 0.7981% | trim rationale는 유지되지만 spread hard gate fail과 same-day sell duplicate가 겹친다 |
| RGTI | blocked_duplicate_same_day | 0.1019% | speculative loss-control trigger는 유지되지만 same-day sell duplicate가 남는다 |
| SO | blocked_metric_gap | 0.0952% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| MSFT | selected_buy | 0.0151% | preflight-covered existing mega-cap quality holding, duplicate/open-order conflict 없음 |
| GOOGL | blocked_weak_review | 0.0140% | quote/spread는 양호하지만 recent weak review가 candidate floor를 막는다 |
| NVDA | blocked_same_cluster_add_block | 0.0100% | ai_semiconductor_complex warning-band add block 유지 |
| PLTR | blocked_low_confidence_speculative | 0.0230% | speculative growth 프로필과 낮은 reusable confidence가 MSFT보다 열위다 |
| INTC | blocked_prior_weak_exit_thesis | 0.0281% | recent weak exit-thesis history로 floor-size re-entry를 열지 않는다 |
| SPY | blocked_floor_cap | 0.0261% | 1주 ask가 validation floor per-order cap 약 `485.95 USD`를 초과 |
| QQQ | blocked_floor_cap | 0.0129% | 1주 ask가 validation floor per-order cap 약 `485.95 USD`를 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_within_policy | spread fail과 same-day sell duplicate가 함께 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T15:31:10.527821336-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-11-0431-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; MSFT quote freshness 약 `0.06`분; spread `0.0151%`; order shape `buy 1 share / limit 398.38 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0431` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/MSFT artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| MSFT | buy | 1 | 398.38 | `bbaadb29-91e7-4507-a59f-218c0cefc5ea` | `status=new`, `filled_qty=0` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle gap only |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 제출 후 정산

- `place_stock_order`는 정상 반환됐고 `client_order_id=hourly-20260611-0431-buy-msft`, `order_id=bbaadb29-91e7-4507-a59f-218c0cefc5ea`로 기록됐다.
- `get_order_by_client_id`와 `get_orders(status=all, symbols=MSFT, after=2026-06-10T19:30:00Z)` 기준 주문은 `status=new`, `filled_qty=0`, `filled_avg_price=null` open order다.
- `get_orders(status=open)` 기준 open orders는 `MSFT` 1건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `MSFT`는 아직 `1주`, `avg_entry_price=426.78`, `qty_available=1`로 unchanged다.
- `get_account_info` snapshot은 portfolio value `97,383.28 USD`, cash `31,263.75 USD`, buying power `294,660.65 USD`다.
- 새 fill은 아직 확인되지 않았고 이 주문은 다음 cycle stale cleanup/lifecycle check 대상으로 남긴다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0431-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0431-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0431-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0431-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0431-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-11-0431-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소된다.
- `spread_pct`: `(ask-bid)/ask*100` 기준 호가 스프레드다. regular-session hard gate는 `0.50%` 이하다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 fallback 매수는 막는다.
