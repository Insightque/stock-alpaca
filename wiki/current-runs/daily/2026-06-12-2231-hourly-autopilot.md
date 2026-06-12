# 2026-06-12-2231-hourly-autopilot

## 요약

`2231` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. 이번 cycle은 preflight clock `2026-06-12T09:31:10.482418382-04:00`, account `ACTIVE`, positions `33`, open orders `0`, fresh IEX quote rows가 모두 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Firecrawl/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 충족했고, `Alpha Vantage`는 `empty_response` gap only로 유지했다.

sell-first 재평가에서는 `RGTI`가 가장 먼저 열렸다. current avg entry `25.569583 USD` 대비 current price `20.9899 USD`로 약 `-17.91%` 손실, scheduler-owned fresh IEX quote `21.01/21.04` spread `0.1427%`, open orders `0`, same trade-date duplicate sell 부재, held qty `49주`가 모두 trim hard gate를 통과했다. `risk_trim_policy.active_trim_triggers.default_trim_fraction_pct=25`를 적용하면 whole-share trim qty는 `12주`이고 잔여 `37주`가 남아 minimum remaining qty도 충족한다. strict universe/MCP/risk validator 세 개를 모두 통과했기 때문에 user directive와 policy를 함께 만족하는 이번 cycle minimum learning order로 `RGTI 12주 trim`을 제출했다.

submit 직후 Alpaca readback 기준 주문은 `client_order_id=hourly-20260612-2231-sell-rgti`, `order_id=1f49ece2-83b5-4136-bf38-e3794c1184fb`, `status=new`로 접수됐다. same client id 조회와 same-symbol order ledger 모두 `cancelled`/`failed` 없이 동일한 open order를 반환했다. nested Codex에는 positions/account read-only Alpaca tool이 노출되지 않아 post-submit 포지션 refresh는 다음 scheduler core preflight 또는 후속 reconciliation cycle에서 확정한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`와 workflow policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler-owned Alpaca clock `2026-06-12T09:31:10.482418382-04:00`, regular market open |
| Stale order lifecycle | PASS | stale cleanup artifact와 core preflight open order row 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, quote row age 약 `0.02`분 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha는 `empty_response` gap only |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK ONLY | `pending_1d_count=14`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | MIXED PASS | `RGTI/WMT/NEE/SPY/QQQ`는 spread cap 이내, `AVGO/SO/PFE`는 FAIL |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions 포함, `RGTI` sell 12주 허용 |
| Final submit path | PASS | `RGTI` sell은 core/MCP/universe/risk/fresh quote/spread/order-shape/duplicate/open-order gate를 모두 통과 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | selected_trim | 0.1427% | speculative-loss control과 residual staged de-risking rationale가 유지되고 duplicate/open-order gate가 비어 있다 |
| AVGO | blocked_spread | 7.5143% | market-open pulse ask가 크게 벌어져 trim hard gate 실패 |
| SO | blocked_spread_and_metric_gap | 4.2847% | spread hard gate 실패와 decision-grade metric gap 동시 지속 |
| WMT | blocked_review_backlog_only | 0.0582% | 1주 add는 executable quote지만 review backlog stop이 신규 buy를 막는다 |
| NEE | blocked_review_backlog_only | 0.1174% | 1주 add는 executable quote지만 review backlog stop이 신규 buy를 막는다 |
| SPY | blocked_floor_cap_and_review_backlog | 0.1056% | 1주 ask `739.20 USD`가 validation floor per-order cap 약 `499.22 USD`를 초과 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.1971% | 1주 ask `716.07 USD`가 validation floor per-order cap 약 `499.22 USD`를 초과 |
| NOK | blocked_validation_lifecycle_add_block | 0.0694% | review-due-index가 due review 미완료로 add block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | trim | pass | spread, duplicate, open-order, held-qty, risk gate를 모두 통과한 이번 cycle 우선 trim |
| AVGO | watch | spread_within_policy | quote `375.66/404.99`가 너무 넓어 trim hard gate를 닫는다 |
| SO | watch | spread_within_policy | quote `93.41/97.50` spread fail과 decision-grade metric gap이 함께 남는다 |

## 주문/체결

- Planned orders: 1
- Submitted orders: 1
- `place_stock_order` 호출: `RGTI` sell 12주 `limit 21.01`, `client_order_id=hourly-20260612-2231-sell-rgti`
- Pre-submit gate summary: paper mode `PASS`, market clock `2026-06-12T09:31:10.482418382-04:00`, order plan `wiki/trade-ledger/orders/2026-06-12-2231-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk validator `PASS`, quote freshness `PASS`, `RGTI` spread `0.1427%` `PASS`, order shape `whole-share/day-limit/stock`, duplicate/open-order check `PASS`, source refs는 scheduler-owned `2231` stale/core/research preflight와 `[[RGTI]]`, `[[2026-06-12-portfolio-review]]`다.
- Post-trade reconciliation: same `client_order_id` readback과 `get_orders(status=all, symbols=RGTI, after=2026-06-12T13:30:00Z)` 모두 주문을 `status=new` open order로 반환했다. `filled_qty=0`, `filled_avg_price=null`, `submitted_at=2026-06-12T13:41:09.3025829Z`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 8개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | `RGTI` sell 12주 trim plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-12-2231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-12-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-12-2231-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-12-2231-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-12-2231-hourly-autopilot-post-trade.json`

## 지표 설명

- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `14`라 YAML stop threshold `12`를 넘어 신규 buy가 차단됐다.
- `speculative_loss_pct`: `risk_trim_policy.active_trim_triggers.speculative_loss_pct=-8` 조건이다. `RGTI`는 current avg entry 대비 약 `-17.91%`라 trim trigger가 계속 active다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `provider gap`: 이번 run의 Alpha Vantage는 `NEWS_SENTIMENT returned no candidate news items for the shortlisted symbols.`로 `empty_response` gap만 남았고, 나머지 4개 research confirmations가 strict MCP gate를 통과시켰다.
