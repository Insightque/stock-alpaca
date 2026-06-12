# 2026-06-12-2251-hourly-autopilot

## 요약

`2251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. 이번 cycle도 preflight clock `2026-06-12T09:51:07.544358301-04:00`, account `ACTIVE`, positions `33`, fresh IEX quote rows가 모두 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Firecrawl/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 충족했고, `Alpha Vantage`는 one-call-per-hour throttle에 따른 `provider_error` gap only로 유지했다.

sell-first 재평가에서는 직전 `2231` cycle의 `RGTI` trim open order가 이번 cycle의 최우선 blocker가 됐다. `RGTI`는 current avg entry `25.569583 USD` 대비 current price `20.63 USD`로 약 `-19.32%` 손실이고 scheduler-owned fresh IEX quote `20.60/20.61` spread `0.0485%`도 정상 범위지만, stale cleanup과 core preflight가 모두 `client_order_id=hourly-20260612-2231-sell-rgti`, `status=new`, `qty=12`, `qty_available=37` open sell을 재확인해 same symbol/side duplicate gate가 추가 trim을 막았다. `AVGO`는 quote `379.86/380.39`, spread `0.1394%`로 정상화됐지만 `2026-06-12T05:18:34Z` same-day sell fill 1주가 recent activities에 남아 duplicate sell discipline이 유지됐다. `SO`는 quote `93.99/94.15`, spread `0.1701%`까지 회복됐지만 trim decision-grade metric gap이 해소되지 않았다.

buy fallback도 submit으로 이어지지 못했다. `WMT`와 `NEE`는 1주 floor-size buy가 가격/스프레드 기준으로는 executable이었지만 `review_backlog_pending_1d_count=14`가 YAML stop threshold `12`를 넘겨 review backlog throttle이 신규 buy를 차단했다. `SPY`와 `QQQ`는 1주 ask가 validation floor per-order cap 약 `499.72 USD`를 초과했고, `NOK`는 `review-due-index`의 validation lifecycle add-block이 그대로 남아 있다. 결과적으로 이번 cycle은 hard gate 전체 실패가 아니라, hard gate는 PASS했지만 exact duplicate/metric/backlog gate 때문에 minimum learning order 1건을 만들지 못한 submit-mode no-op로 기록한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler-owned Alpaca clock `2026-06-12T09:51:07.544358301-04:00`, regular market open |
| Stale order lifecycle | PASS | stale cleanup status `pass`; open order 1건은 fresh `RGTI` sell이라 lifecycle failure는 아님 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, quote row age 약 `0.01`분 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha는 throttle `provider_error` gap only |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK ONLY | `pending_1d_count=14`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | PASS/MIXED | `RGTI/AVGO/SO/WMT/NEE/SPY/QQQ/NOK` 모두 spread cap 이내 |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions/open order 포함, `orders=[]` 허용 |
| Final submit path | NO SUBMIT | `RGTI` open-order duplicate, `AVGO` same-day duplicate sell, `SO` metric gap, buy backlog throttle가 minimum learning order를 모두 차단 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | blocked_open_order_duplicate | 0.0485% | residual speculative trim rationale는 유지되지만 `2231` open sell 12주가 same symbol/side open-order gate를 유지 |
| AVGO | blocked_same_day_duplicate_sell | 0.1394% | warning-band trim rationale와 정상 spread에도 same-day sell fill 1주가 duplicate discipline 유지 |
| SO | blocked_metric_gap | 0.1701% | spread는 통과했지만 trim decision-grade metric gap이 그대로 |
| WMT | blocked_review_backlog_only | 0.0579% | 1주 add는 executable quote지만 review backlog stop이 신규 buy를 막음 |
| NEE | blocked_review_backlog_only | 0.0352% | 1주 add는 executable quote지만 review backlog stop이 신규 buy를 막음 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0612% | 1주 ask `735.92 USD`가 validation floor per-order cap 약 `499.72 USD`를 초과 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0112% | 1주 ask `713.02 USD`가 validation floor per-order cap 약 `499.72 USD`를 초과 |
| NOK | blocked_validation_lifecycle_add_block | 0.0679% | due review 미완료로 add block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | open_order_check | spread와 held qty는 정상이나 `hourly-20260612-2231-sell-rgti` open order가 추가 trim을 차단 |
| AVGO | watch | duplicate_symbol_side_same_day | spread 정상화에도 `2026-06-12T05:18:34Z` same-day sell fill 1주가 남음 |
| SO | watch | decision_grade_metric_gap | spread 정상화에도 trim decision-grade metric 공백이 지속 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Existing open order carried forward: `RGTI` sell 12주 `limit 21.01`, `client_order_id=hourly-20260612-2231-sell-rgti`, `status=new`
- Post-trade reconciliation: 이번 cycle 신규 submit attempt는 없었다. scheduler-owned stale cleanup과 core preflight가 같은 `RGTI` open order와 `qty_available=37` 예약 상태를 다시 확인했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 8개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | current positions/open order 포함, `orders=[]` no-submit plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-12-2251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-12-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-12-2251-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-12-2251-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-12-2251-hourly-autopilot-post-trade.json`

## 지표 설명

- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `14`라 YAML stop threshold `12`를 넘어 신규 buy가 차단됐다.
- `speculative_loss_pct`: `risk_trim_policy.active_trim_triggers.speculative_loss_pct=-8` 조건이다. `RGTI`는 current avg entry 대비 약 `-19.32%`라 trim trigger 자체는 계속 active다.
- `same-day duplicate discipline`: 같은 미국 거래일에 이미 fill되었거나 아직 살아 있는 동일 symbol/side 주문을 반복 제출하지 않는 규율이다. 이번 cycle에서는 `AVGO` same-day sell fill과 `RGTI` open sell이 여기에 해당한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `provider gap`: 이번 run의 Alpha Vantage는 provider throttle 때문에 `provider_error` gap으로 남았지만, 나머지 4개 research confirmations가 strict MCP gate를 통과시켰다.
