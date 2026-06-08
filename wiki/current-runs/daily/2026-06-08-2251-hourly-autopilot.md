# 2026-06-08-2251-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고 scheduler stale cleanup은 `pass`였다. scheduler-owned Alpaca core/research preflight를 우선 사용했고, runtime Alpaca MCP로 watchlist 0건, open order 0건, same-day filled order 3건(`AVGO` 장외 trim 2건, `TSLA` regular exit 1건)을 대조한 뒤 `RGTI` risk-reducing trim을 제출했다.

이번 run은 review backlog throttle 때문에 신규 buy는 계속 차단됐지만 risk-reducing sell은 독립적으로 평가했다. `RGTI` 30주 trim은 speculative sleeve 손실 심화와 weak stock-only review를 근거로 했고, `client_order_id=hourly-20260608-2251-sell-rgti`가 `21.48 USD`에 전량 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime Alpaca clock `2026-06-08T09:55:06.443186071-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-08-2251-hourly-autopilot-stale-order-cleanup.json`, stale/open autopilot order 0건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + runtime watchlist/open-order/order-history reconciliation |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `provider_error` one-call-per-hour throttle nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK | `pending_1d_count=13`로 YAML `stop_new_buys_at_pending_1d=12` 초과. sell/trim에는 비적용 |
| Quote/spread | PASS for RGTI sell | preflight RGTI quote `21.48/21.49`, spread `0.0466%`, quote age 약 `3.59`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | sell trim | 0.0466% | speculative sleeve 손실 약 `-15.27%`, 2026-06-02 5D review `약함`, same-day duplicate/open-order conflict 없음 |
| AVGO | watch | 0.2937% | same-day after-hours sell 2건이 이미 있어 duplicate symbol/side discipline이 먼저 막는다 |
| SO | watch | 0.0651% | weak-to-neutral review는 누적됐지만 trim을 정당화할 decision-grade metric이 비어 있다 |
| SPY | watch | 0.0094% | benchmark add는 backlog throttle 아래에서 sell-first 우선순위를 넘지 못했다 |
| QQQ | watch | 0.0126% | benchmark add는 가능하지만 신규 buy throttle 때문에 submit 대상에서 제외했다 |
| NOK | blocked add | 0.0681% | 기존 20D add-block과 pending review discipline을 유지한다 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | trim | PASS | 2026-05-22 stock-only 5D review 약세와 현재 손실 약 `-15.27%`로 speculative sleeve trim trigger active |
| AVGO | watch | same-day duplicate fail | 장외 trim 2건 이후 same-day regular-session sell 재진입은 duplicate discipline에 막힌다 |
| SO | watch | metric gap fail | quote/spread는 정상이나 decision-grade replacement margin이 비어 있다 |

## 주문/체결

- Planned orders: 1
- Submitted orders: 1
- Filled orders: `RGTI` sell 30 @ `21.48 USD` (`client_order_id=hourly-20260608-2251-sell-rgti`, order id `6ce608f7-bbd1-45f8-a43f-9722f376a100`)
- Pre-submit gate summary: paper mode `true`, market clock `2026-06-08T09:55:06.443186071-04:00`, order plan path `wiki/trade-ledger/orders/2026-06-08-2251-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, RGTI quote freshness `3.59`분 및 spread `0.0466%`, order shape `sell 30 shares / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `2251` stale cleanup/core/research preflight와 runtime gate evaluation/review artifacts
- Post-trade reconciliation: runtime `get_orders(status=open)` 0건, `get_orders(status=all, after=2026-06-08T00:00:00Z)` 기준 RGTI fill 1건과 TSLA/AVGO same-day fills 3건을 확인했다. `get_all_positions` 기준 positions는 `32` 유지, `RGTI`는 `120 -> 90`으로 감소했고 account snapshot은 portfolio value `99,552.10 USD`, cash `31,774.85 USD`, buying power `300,430.68 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, shortlist 6, final candidates 3 |
| `check-mcp-coverage.py --strict --json` | PASS | positive research 4개(`sec-edgar/fred/firecrawl/yahoo-finance`) |
| `check-risk-policy.py --json` | PASS | sell notional `644.40`, review backlog 13 반영 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-08-2251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-08-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-08-2251-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-08-2251-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-08-2251-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-08-2251-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-08-2251-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-08-2251-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy review backlog count다. 이번 run에서는 `13`으로 YAML stop threshold `12`를 넘겨 신규 buy를 막았지만, risk-reducing sell에는 적용하지 않았다.
- `gap_category`: 이번 run의 research 공백은 Alpha `provider_error` one-call throttle뿐이었고 다른 4개 provider는 usable/pass였다.
- `portfolio_construction_policy`: 신규 buy가 기존 보유 대비 분산과 replacement-rank를 개선하는지 보는 계층이다. 이번 run은 sell-first candidate가 존재해 buy 비교 이전에 RGTI trim을 우선했다.
