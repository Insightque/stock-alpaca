# 2026-06-12-2351-hourly-autopilot

## 요약

`2351` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. 이번 cycle의 preflight clock `2026-06-12T10:51:11.313002467-04:00`, account `ACTIVE`, positions `33`, fresh IEX quote rows가 모두 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Firecrawl/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 충족했고, `Alpha Vantage`는 `NEWS_SENTIMENT` empty-response gap only로 유지했다.

sell-first 재평가에서는 global open-order lifecycle blocker가 없었다. scheduler-owned stale cleanup과 core preflight가 open orders `0`을 남겼고 same-day recent activities에는 `RGTI` sell 12주 `filled_at=2026-06-12T14:10:47.740608Z`, earlier `AVGO` sell 1주 `filled_at=2026-06-12T05:18:34.148553Z`, `PFE` sell 1주 `filled_at=2026-06-12T01:21:39.341022Z`가 남아 있었다. 다만 `RGTI`는 fresh IEX quote `20.45/21.03`, spread `2.7965%`로 policy cap `0.50%`를 크게 초과해 이번 cycle의 첫 hard blocker가 `spread_within_policy`로 바뀌었다. `AVGO`도 quote `376.90/382.00`, spread `1.3441%`로 계속 fail이고, `SO`는 quote `93.98/94.02`, spread `0.0426%`로 hard gate를 통과했지만 trim decision-grade metric gap이 그대로다.

buy fallback도 submit으로 이어지지 못했다. `WMT`와 `NEE`는 1주 floor-size buy가 가격/스프레드 기준으로는 executable이었지만 `review_backlog_pending_1d_count=14`가 YAML stop threshold `12`를 넘겨 review backlog throttle이 신규 buy를 차단했다. `SPY`와 `QQQ`는 1주 ask가 validation floor per-order cap 약 `501.01 USD`를 초과했고, `NOK`는 `review-due-index`의 validation lifecycle add-block이 그대로 남아 있다. 결과적으로 이번 cycle은 hard gate 전체 실패가 아니라, hard gate는 PASS했지만 exact spread/duplicate/metric/backlog gate 때문에 minimum learning order 1건을 만들지 못한 submit-mode no-op로 기록한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler-owned Alpaca clock `2026-06-12T10:51:11.313002467-04:00`, regular market open |
| Stale order lifecycle | PASS | stale cleanup status `pass`; initial/remaining open orders 모두 `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, quote row age 약 `0.04`분 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha는 `empty_response` gap only |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK ONLY | `pending_1d_count=14`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | PASS/MIXED | `SO/WMT/NEE/SPY/QQQ/NOK`는 spread cap 이내, `RGTI` `2.7965%`, `AVGO` `1.3441%`로 fail |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions/no open order 포함, `orders=[]` 허용 |
| Final submit path | NO SUBMIT | `RGTI` spread+same-day sell duplicate, `AVGO` spread+same-day duplicate, `SO` metric gap, buy backlog throttle가 minimum learning order를 모두 차단 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | blocked_spread_and_same_day_duplicate_sell | 2.7965% | `2231` sell 12주가 `2026-06-12T14:10:47.740608Z`에 filled 처리돼 residual speculative trim rationale에도 same-day duplicate sell discipline이 남아 있고, fresh spread가 policy cap을 크게 초과 |
| AVGO | blocked_spread_and_same_day_duplicate_sell | 1.3441% | ai_semiconductor warning-band trim rationale는 유지되지만 spread가 policy cap을 크게 초과하고 same-day sell fill 1주도 남음 |
| SO | blocked_metric_gap | 0.0426% | spread는 통과했지만 trim decision-grade metric gap이 지속 |
| WMT | blocked_review_backlog_only | 0.0501% | 1주 add는 executable quote지만 review backlog stop이 신규 buy를 막음 |
| NEE | blocked_review_backlog_only | 0.0234% | 1주 add는 executable quote지만 review backlog stop이 신규 buy를 막음 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0583% | 1주 ask `738.11 USD`가 validation floor per-order cap 약 `501.01 USD`를 초과 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0727% | 1주 ask `715.84 USD`가 validation floor per-order cap 약 `501.01 USD`를 초과 |
| NOK | blocked_validation_lifecycle_add_block | 0.0677% | due review 미완료로 add block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | `spread_within_policy` | same-day duplicate discipline도 남지만 이번 cycle의 첫 hard blocker는 spread `2.7965%` fail |
| AVGO | watch | `spread_within_policy` | same-day sell discipline도 남지만 이번 cycle의 첫 hard blocker는 spread `1.3441%` fail |
| SO | watch | `decision_grade_metric_gap` | quote/spread는 통과했지만 trim decision-grade metric 공백이 지속 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Same-day fills seen in source-of-record: `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`
- Post-trade reconciliation: 이번 cycle 신규 submit attempt는 없었다. scheduler-owned stale cleanup/core preflight가 open orders `0`, positions `33`, `RGTI qty_available=37`를 함께 재확인했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 8개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha empty-response gap only |
| `check-risk-policy.py --json` | PASS | current positions/no open orders 포함, `orders=[]` no-submit plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-12-2351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-12-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-12-2351-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-12-2351-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-12-2351-hourly-autopilot-post-trade.json`

## 지표 설명

- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `14`라 YAML stop threshold `12`를 넘어 신규 buy가 차단됐다.
- `same-day duplicate sell discipline`: 같은 미국 거래일에 이미 fill된 동일 symbol/side sell을 반복 제출하지 않는 규율이다. 이번 cycle에서는 `RGTI`와 earlier `AVGO` trim이 여기에 해당한다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle의 cap은 약 `501.01 USD`라 `SPY/QQQ` 1주가 초과했다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `provider gap`: 이번 run의 Alpha Vantage는 `NEWS_SENTIMENT` empty-response 때문에 `empty_response` gap으로 남았지만, 나머지 4개 research confirmations가 strict MCP gate를 통과시켰다.
