# 2026-06-09-2251-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `2251` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 open order 0건으로 종료됐고 core preflight hard gate도 `pass`였다. 이후 registered Codex Alpaca MCP로 clock/account/open-orders/fills/quotes를 보강해 regular market open, open orders 0건, same-day fills는 earlier `RGTI` sell 22주 2건, `AVGO` live quote `403.00/403.66`를 재확인했다.

이번 cycle은 sell/trim을 먼저 평가했다. `RGTI`는 여전히 speculative loss-control trim trigger를 충족했지만 2026-06-09 ET same-day `RGTI` sell fill이 이미 있어 duplicate symbol/side conflict를 피해야 했다. 반면 `AVGO`는 직전 2231 cycle에서 trim을 막았던 live spread hard gate가 해소됐고, post-earnings staged de-risk watch와 ai_semiconductor warning-band 점검 대상으로 남아 있었다. 따라서 sell-first directive에 따라 `AVGO` 2주 regular-session day limit trim sell을 제출했다. immediate reconciliation 시점에는 `order_id=bf1247db-2054-4304-a16b-58ada7b39af7`, `status=new` open order로 남아 있었고 fills는 아직 없다. `SO`는 live spread는 통과했지만 decision-grade metric gap이 남아 있었고, `BAC/SPY/QQQ` buy fallback은 eligible risk-reducing sell이 먼저 열려 사용하지 않았다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-09T09:54:10.546861459-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-09-2251-hourly-autopilot-stale-order-cleanup.json`에서 stale/open autopilot order 없음 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime open orders 0건 / same-day fills 확인 / live quote refresh |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage one-call throttle `provider_error` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | `AVGO` live spread `0.1636%`, quote timestamp `2026-06-09T13:54:12.038089368Z` |
| Risk plan | PASS | `AVGO` 2주 trim sell notional `806.00 USD`, cash/exposure/ticker/cluster caps 통과 |
| Final submit path | PASS | registered Alpaca MCP가 `AVGO` 2주 sell을 제출했고 immediate reconciliation 기준 `status=new` open order로 남음 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | submitted_open | 0.1636% | post-earnings de-risk watch와 ai_semiconductor warning band가 유지되는 가운데 spread hard gate가 해소돼 duplicate-free trim 후보가 됐고, 2주 trim order를 제출했다. |
| RGTI | watch | 0.0904% | speculative loss-control trigger는 유지되지만 same-day earlier sell fill 때문에 duplicate symbol/side conflict |
| SO | watch | 0.0438% | spread는 정상이나 trim justification용 decision-grade expected-excess/replacement margin 공백 지속 |
| BAC | watch | 0.0184% | duplicate-free financials diversifier buy fallback이지만 sell-first directive 때문에 미사용 |
| SPY | watch | 0.0040% | benchmark fallback은 유효했지만 eligible sell path가 먼저 열려 미사용 |
| QQQ | watch | 0.0773% | benchmark fallback은 유효했지만 eligible sell path가 먼저 열려 미사용 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | duplicate_symbol_side_same_day | earlier `RGTI` sell fill 22주가 이미 있어 이번 cycle 추가 same-day sell 제출은 차단 |
| SO | watch | decision_grade_metric_gap | live quote `91.28/91.32`는 정상 범위지만 trim justification용 replacement margin 공백 지속 |
| BAC | hold_watch | sell_trigger_none | active trim trigger가 없어 no-trigger monitor로만 유지 |

## 주문 제출과 reconciliation

- Submitted order: `AVGO` sell 2 @ `403.00` day limit
- Alpaca order id: `bf1247db-2054-4304-a16b-58ada7b39af7`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, `AVGO` quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`
- Reconciliation: `get_orders(status=all, symbols=AVGO)` 기준 주문은 `status=new`, `filled_qty=0`, `filled_avg_price=null`로 open 상태다. `get_account_activities(activity_types=FILL, after=2026-06-09T13:50:00Z)`에는 신규 `AVGO` fill이 없었고, `get_all_positions` 기준 `AVGO` 보유수량은 `10주` 유지지만 `qty_available`가 `8주`로 감소해 open sell 2주가 예약된 상태임을 확인했다. account snapshot은 portfolio value `100656.56 USD`, cash `32265.39 USD`, buying power `304528.07 USD`, long market value `68391.17 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 4개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | `AVGO` 2주 regular-session trim sell 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-09-2251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-09-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-09-2251-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-09-2251-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-09-2251-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-09-2251-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-09-2251-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-09-2251-hourly-autopilot-runtime-gate-evaluation.json`, `wiki/evidence-store/sources/2026-06-09-2251-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `duplicate_symbol_side_same_day`: 같은 regular session 날짜에 이미 같은 symbol/side fill이 있으면 이번 cycle의 추가 submit 후보에서 제외하는 gate다.
- `review_backlog_pending_1d_count`: 이번 run에서는 `0`이라 신규 buy throttle을 유발하지 않았고, pending `5D=13`, `20D=1`은 lifecycle 추적용으로만 남겼다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler-owned one-call-per-hour throttle 때문에 provider_error gap으로만 기록됐고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
