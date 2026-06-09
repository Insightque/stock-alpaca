# 2026-06-09-2231-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `2231` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 open order 0건으로 종료됐고 core preflight hard gate도 `pass`였다. 이후 registered Codex Alpaca MCP로 clock/account/open-orders/fills/quotes를 보강해 regular market open, same-day fills 0건, open orders 0건, `RGTI` live quote `22.07/22.09`를 재확인했다.

이번 cycle은 sell/trim을 먼저 평가했다. 새 trading day로 넘어오면서 어제 `RGTI` trim의 same-day duplicate blocker가 해소됐고, 남은 `90주`는 avg entry `25.569583 USD` 대비 약 `-12.94%` 손실로 speculative loss-control trigger를 계속 충족했다. live spread는 `0.0906%`로 policy cap 안이었고, held quantity와 risk validator도 통과했다. 반면 `AVGO`는 live quote `392.00/408.00`으로 spread `3.9990%`가 hard gate를 넘었고, `SO`는 spread는 정상이지만 decision-grade metric gap이 남았다. 따라서 buy fallback(`BAC/SPY/QQQ`)은 사용하지 않고 `RGTI` 22주 regular-session day limit trim sell을 제출했다. nested shell submit helper는 Alpaca stdio DNS failure로 실패했지만, registered Codex Alpaca MCP direct fallback이 `order_id=cb22952f-69a1-4b37-a8a8-09740c4225ac`를 생성했고 same-day reconciliation 기준 `filled_avg_price=22.298182 USD`로 체결을 확인했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-09T09:34:34.31554732-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-09-2231-hourly-autopilot-stale-order-cleanup.json`에서 stale/open autopilot order 없음 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime open orders 0건 / same-day fills 0건 / live quote refresh |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage `empty_response` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | `RGTI` live spread `0.0906%`, quote timestamp `2026-06-09T13:35:51.813270850Z` |
| Risk plan | PASS | `RGTI` 22주 trim sell_notional `485.54 USD`, cash/exposure/ticker/speculative caps 통과 |
| Final submit path | PASS | registered Alpaca MCP가 `RGTI` 22주 sell을 제출했고 reconciliation 기준 `filled`로 종료 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | submitted_filled | 0.0906% | speculative loss-control trim trigger active, new trading day로 duplicate blocker 해소, held qty/risk gate 통과. `22주` trim이 `22.298182 USD` 평균가로 체결됐다. |
| AVGO | watch | 3.9990% | post-earnings de-risk watch는 유지되지만 live IEX spread가 policy cap `0.50%`를 크게 초과해 trim hard gate 실패 |
| SO | watch | 0.1424% | spread는 통과했지만 repeated weak review를 trim order로 승격할 decision-grade expected-excess/replacement margin이 여전히 비어 있음 |
| BAC | watch | 0.0738% | duplicate-free financials diversifier buy fallback은 유지됐지만 workflow의 sell-first directive 때문에 이번 cycle에서는 사용하지 않음 |
| SPY | watch | 0.0054% | benchmark fallback은 유효했지만 eligible risk-reducing sell이 먼저 열려 있어 미사용 |
| QQQ | watch | 별도 live refresh 없음 | benchmark fallback 필요성이 sell path 성립으로 사라져 재주문 후보에서 후순위 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_within_policy | live quote `392.00/408.00`으로 spread `3.9990%`가 policy cap `0.50%`를 초과 |
| SO | watch | decision_grade_metric_gap | live quote `91.22/91.35`는 정상 범위지만 trim justification용 replacement margin 공백 지속 |
| PFE | hold_watch | sell_trigger_none | weak review는 남아도 active trim trigger가 없어 no-trigger monitor로만 유지 |

## 주문 제출과 reconciliation

- Submitted order: `RGTI` sell 22 @ `22.07` day limit
- Alpaca order id: `cb22952f-69a1-4b37-a8a8-09740c4225ac`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, `RGTI` quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`
- Reconciliation: same-day `get_orders(status=all, symbols=RGTI)` 기준 주문은 `filled_qty=22`, `filled_avg_price=22.298182`, `filled_at=2026-06-09T13:40:55.433789Z`로 닫혔다. `get_account_activities(activity_types=FILL)`는 partial-fill `2주 @ 22.28` 후 fill `20주 @ 22.30`로 총 `22주` 체결을 보여줬다. `get_all_positions` 기준 `RGTI` 보유수량은 `90주 -> 68주`, account snapshot은 portfolio value `100629.16 USD`, cash `32265.39 USD`, buying power `304479.71 USD`, long market value `68363.77 USD`다.
- Submit helper note: `scripts/submit-validated-order-plan-mcp.py`는 nested shell의 Alpaca stdio DNS failure로 `status=failed`였지만, registered Codex Alpaca MCP direct fallback으로 실제 주문 제출과 reconciliation을 완료했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 4개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | `RGTI` 22주 regular-session trim sell 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-09-2231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-09-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-09-2231-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-09-2231-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-09-2231-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-09-2231-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-09-2231-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-09-2231-hourly-autopilot-runtime-gate-evaluation.json`, `wiki/evidence-store/sources/2026-06-09-2231-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `speculative_loss_control`: speculative sleeve 손실이 정책 임계값을 넘을 때 buy-side throttle과 독립적으로 trim/exit를 우선 평가하는 trigger다.
- `review_backlog_pending_1d_count`: 이번 run에서는 `0`이라 신규 buy throttle을 유발하지 않았고, pending `5D=13`, `20D=1`은 lifecycle 추적용으로만 남겼다.
- `empty_response`: 이번 run의 Alpha Vantage는 shortlisted symbols 기준 candidate sentiment/news row가 비어 있어 `empty_response` gap으로만 기록됐다. 나머지 research confirmations가 유지돼 strict MCP gate는 통과했다.
