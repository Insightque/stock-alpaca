# 2026-06-08-2231-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고 scheduler stale cleanup은 `pass`였다. scheduler-owned Alpaca core/research preflight를 우선 사용했고, runtime Alpaca MCP로 watchlist 0건, open order 0건, same-day filled order 2건(`AVGO` 장외 trim)만 추가 대조한 뒤 `TSLA` risk-reducing exit를 제출했다.

이번 run은 review backlog throttle 때문에 신규 buy는 차단됐지만 risk-reducing sell은 독립적으로 평가했다. `TSLA` 1주 exit은 speculative loss control과 spread/quote/risk gate를 모두 통과했고, `client_order_id=hourly-20260608-2231-sell-tsla`가 `398.59 USD`에 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime Alpaca clock `2026-06-08T09:36:13.51028951-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-08-2231-hourly-autopilot-stale-order-cleanup.json`, stale/open autopilot order 0건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + runtime watchlist/open-order/order-history reconciliation |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `empty_response` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK | `pending_1d_count=13`로 YAML `stop_new_buys_at_pending_1d=12` 초과. sell/trim에는 비적용 |
| Quote/spread | PASS for TSLA sell | runtime TSLA quote `396.52/396.77`, spread `0.0630%`, quote age 약 `1.78`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| TSLA | sell exit | 0.0630% | speculative loss control(-10.19%)과 weak validation review가 겹쳤고 duplicate/open-order conflict가 없다. |
| AVGO | watch | 1.7937% | same-day after-hours sell 2건이 이미 있고 runtime spread가 hard cap을 초과한다. |
| SO | watch | 5.7066% | weak-to-neutral review는 누적됐지만 runtime quote quality와 decision-grade metric이 부족하다. |
| SPY | watch | 0.0040% | benchmark add는 backlog throttle 아래에서 sell-first 우선순위를 넘지 못했다. |
| QQQ | watch | 0.0783% | benchmark add는 가능하지만 신규 buy throttle 때문에 submit 대상에서 제외했다. |
| NOK | blocked add | 0.0689% | 기존 20D add-block과 pending review discipline을 유지한다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| TSLA | close | PASS | 2026-05-30 1D review 약세 + 현재 손실 -10.19%로 speculative loss trigger active |
| AVGO | watch | spread/same-day duplicate fail | 장외 trim 2건 이후 regular-session 재진입 sell은 비효율이고 spread도 cap 초과 |
| SO | watch | spread/metric gap fail | quote quality와 decision-grade replacement margin이 모두 부족 |

## 주문/체결

- Planned orders: 1
- Submitted orders: 1
- Filled orders: `TSLA` sell 1 @ `398.59 USD` (`client_order_id=hourly-20260608-2231-sell-tsla`, order id `20c75f1e-91b1-44a3-ba80-7e9247a86114`)
- Pre-submit gate summary: paper mode `true`, market clock `2026-06-08T09:36:13.51028951-04:00`, order plan path `wiki/trade-ledger/orders/2026-06-08-2231-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, TSLA quote freshness `1.78`분 및 spread `0.0630%`, order shape `sell 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `2231` stale cleanup/core/research preflight와 runtime gate evaluation/review artifacts
- Post-trade reconciliation: runtime `get_orders(status=open)` 0건, `get_orders(status=all, after=2026-06-08T00:00:00Z)` 기준 TSLA fill 1건과 AVGO after-hours fills 2건 확인, `get_all_positions` 기준 positions `33 -> 32`, `TSLA` 포지션 제거, account snapshot은 portfolio value `99,862.11 USD`, cash `31,130.45 USD`, buying power `300,491.66 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, shortlist 6, final candidates 3 |
| `check-mcp-coverage.py --strict --json` | PASS | positive research 4개(`sec-edgar/fred/firecrawl/yahoo-finance`) |
| `check-risk-policy.py --json` | PASS | sell notional `396.52`, review backlog 13 반영 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-08-2231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-08-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-08-2231-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-08-2231-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-08-2231-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-08-2231-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-08-2231-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-08-2231-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy review backlog count다. 이번 run에서는 `13`으로 YAML stop threshold `12`를 넘겨 신규 buy를 막았지만, risk-reducing sell에는 적용하지 않았다.
- `gap_category`: 이번 run의 research 공백은 Alpha `empty_response`로만 남았고 다른 4개 provider는 usable/pass였다.
- `portfolio_construction_policy`: 신규 buy가 기존 보유 대비 분산과 replacement-rank를 개선하는지 보는 계층이다. 이번 run은 sell-first candidate가 존재해 buy 비교 이전에 TSLA exit를 우선했다.
