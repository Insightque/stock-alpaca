# 2026-06-04-2351-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler stale cleanup은 남은 stale/open autopilot order 없이 `pass`였다. Alpaca core preflight의 clock/account/positions/open orders/recent activities/quotes는 모두 통과했고, runtime `get_clock`는 `2026-06-04T10:54:19.154271536-04:00` 기준 regular market open이었다.

이번 run은 `submit` mode였고, workflow 요구대로 sell/trim을 먼저 평가한 뒤 floor-size learning order를 만들었다. `QQQ`와 `SPY`는 각각 `2026-06-04T14:20:05Z`, `2026-06-04T14:40:11.754058Z` same-day filled buy가 있어 duplicate symbol/side discipline 때문에 재사용하지 않았다. 따라서 duplicate-free existing financials diversifier holding인 `BAC` 1주 regular-session day limit buy를 제출했고, Alpaca MCP는 `order_id=7d85f1b6-7d11-4992-9f96-8705ad4dfd73` / `client_order_id=hourly-20260604-2351-buy-bac`를 생성했다. post-trade reconciliation 시점에는 주문 상태가 `new` open order로 남아 있고 BAC 보유수량은 아직 2주 그대로다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T10:54:19.154271536-04:00`, regular market open |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-04-2351-hourly-autopilot-stale-order-cleanup.json`에서 stale/open autopilot order 없음 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime open orders 0건/BAC quote spot-check 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha는 `empty_response` gap 기록 |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | BAC spread `0.0373%`, quote timestamp `2026-06-04T14:54:54.559101438Z` |
| Risk plan | PASS | `BAC` 1주 buy_notional `53.60`, cash/exposure/ticker caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `BAC` 1주 regular day limit buy를 생성했고 reconciliation 기준 `status=new` open order로 확인됐다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| BAC | submitted_open | 0.0373% | financials diversifier holding으로 same-day duplicate/open-order 충돌이 없고, BAC-specific research rows와 macro confirmation이 유지돼 floor-size learning buy로 승격했다. 현재 status `new` open order다. |
| QQQ | watch | 0.0068% | `2026-06-04T14:20:05Z` same-day filled buy가 있어 duplicate discipline 때문에 제외했다. |
| SPY | watch | 0.0040% | `2026-06-04T14:40:11.754058Z` same-day filled buy가 있어 benchmark fallback 재사용을 피했다. |
| AMZN | watch | 0.1615% | add blocker는 없지만 이번 cycle에서는 financials diversifier BAC가 portfolio-fit 측면에서 더 우선이었다. |
| AAPL | watch | 0.0194% | mega-cap tech add보다 분산 보강이 우선이었다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 당일 급락으로 trim 재점검 대상이지만 decision-grade 20D metric 공백이 남아 즉시 trim order로 올리지 않았다. |
| SO | watch | decision_grade_metric_gap | FRED macro confirmation은 pass지만 per-symbol expected-excess 공백 때문에 trim justification이 부족했다. |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 trim fraction을 whole-share로 맞추기 어렵고 decision-grade metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `BAC` buy 1 @ `53.60` day limit
- Alpaca order id: `7d85f1b6-7d11-4992-9f96-8705ad4dfd73`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, BAC quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`, reconciliation 기준 `status=new`, `filled_qty=0`
- Reconciliation: `get_order_by_client_id`와 same-day `get_orders` 모두 동일 BAC order 1건을 `status=new`로 반환했다. `get_all_positions` 기준 BAC 보유수량은 2주로 아직 증가하지 않았고, supplementary runtime `get_account_info`는 tool layer에서 `cancelled`였다. 따라서 계좌 수치는 scheduler-owned preflight snapshot을 last confirmed state로 유지했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개 |
| `check-risk-policy.py --json` | PASS | BAC 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-04-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-04-2351-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-04-2351-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-04-2351-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-04-2351-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-04-2351-hourly-autopilot-research-mcp-preflight.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: 이번 run에서는 `0`이라 buy slot throttle을 유발하지 않았고, pending `20D=2`는 lifecycle 추적 용도로만 기록한다.
- `empty_response`: 이번 run의 Alpha Vantage는 shortlisted symbols 기준 candidate news sentiment가 비어 있어 `empty_response` gap으로 기록됐다. 나머지 research confirmations는 유지되어 strict MCP gate는 통과했다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 filled된 동일 symbol/side buy는 open order가 없더라도 새 validation buy로 재사용하지 않는 규칙이다.
