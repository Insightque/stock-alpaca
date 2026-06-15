# 2026-06-15-2351-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `2351` stale cleanup/core/research preflight를 우선 사용했다. core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했고 `get_account_activities`에는 same-session `WMT` buy 1주 체결(`2026-06-15T14:41:05Z`)과 `BAC` buy 1주 체결(`2026-06-15T14:19:50Z`)이 반영됐다. positions는 `33`건이며 account snapshot은 portfolio value `102,253.51 USD`, cash `31,980.21 USD`였다.

이번 cycle의 최종 blocker는 `risk_open_order_lifecycle`이다. stale cleanup report는 `2251` cycle `AVGO` sell 1주(`client_order_id=hourly-20260615-2251-sell-avgo`)를 stale candidate로 잡아 cancel attempt `pass`를 기록했지만, 같은 artifact의 `remaining_open_orders`에는 해당 주문이 age `48.73`분 `status=pending_cancel`로 남아 있었다. 반면 직후 scheduler-owned core preflight `get_orders_open` row는 open orders `[]`를 반환했다. workflow는 unresolved stale cleanup artifact를 우선 authoritative blocker로 취급하므로, sell-first 진단과 후보 ranking은 계속 수행했지만 신규 `place_stock_order`는 호출하지 않았다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler core preflight `get_clock` `2026-06-15T10:51:09.807705468-04:00`, regular market open |
| Stale order cleanup | FAIL | cleanup report에 `AVGO` stale sell이 cancel attempt 이후에도 `pending_cancel` remaining open order로 잔존 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, positions `33`, open-orders row `0`, same-session `WMT/BAC/RGTI` fills 반영 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage `empty_response` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for diagnostics | core preflight quotes hard gate pass; 이번 cycle은 lifecycle blocker 때문에 candidate-specific submit quote 단계까지 진행하지 않음 |
| Risk plan | FAIL | stale cleanup artifact 기준 unresolved `AVGO` pending_cancel이 `risk_open_order_lifecycle`를 발생 |
| Final submit path | FAIL | `place_stock_order` 호출 전 hard gate fail 확정 |

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| AVGO | block | stale cleanup artifact에 `pending_cancel` sell 1주가 남아 lifecycle hard gate를 직접 발생 |
| RGTI | watch | speculative trim trigger는 유지되나 `2026-06-15T13:41:43Z` same-session sell fill 9주로 duplicate sell gate |
| SO | watch | trim 재평가 대상이지만 decision-grade expected-excess/replacement margin 공백 지속 |
| WMT | watch | `2026-06-15T14:41:05Z` same-session fill이 이미 발생해 추가 buy는 duplicate 경로가 됨 |
| BAC | watch | `2026-06-15T14:19:50Z` same-session fill이 이미 발생해 추가 buy는 duplicate gate |
| SPY | watch | lifecycle block이 먼저 발생했고, fallback benchmark로도 새 submit은 허용되지 않음 |
| QQQ | watch | lifecycle block이 먼저 발생했고, fallback benchmark로도 새 submit은 허용되지 않음 |
| NOK | watch | `validation_lifecycle` add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | risk_open_order_lifecycle | stale cleanup artifact의 `pending_cancel` trim order가 먼저 해소돼야 추가 action 가능 |
| RGTI | watch | duplicate_symbol_side_same_day | earlier same-session trim fill이 있어 추가 sell 차단 |
| SO | watch | sell_metric_gap | trim 판단용 decision-grade metric 공백 지속 |

## 주문 제출과 reconciliation

- Orders: 없음. `place_stock_order`와 `cancel_order_by_id`는 호출하지 않았다.
- Immediate reconciliation: no-submit result. scheduler-owned core preflight 기준 open orders row는 `0`건이고 same-session fills는 `WMT` buy 1건, `BAC` buy 1건, `RGTI` sell 9건 cohort가 반영돼 있다.
- Lifecycle conflict note: workflow-required stale cleanup artifact는 같은 시점 `AVGO` stale sell 1건을 `pending_cancel` remaining open order로 유지해 source-of-record 충돌을 드러냈다. 이번 run은 이 충돌을 해소하지 못했으므로 신규 submit path를 열지 않았다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad-universe strict gate 통과 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpha empty-response gap 포함 tiered strict gate 통과 |
| `check-risk-policy.py --json` | FAIL | `AVGO` pending-cancel stale open order lifecycle block |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-15-2351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-15-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-15-2351-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-15-2351-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-15-2351-hourly-autopilot-post-trade.json`

## 지표 설명

- `risk_open_order_lifecycle`: stale cleanup 이후에도 autopilot open order가 남아 신규 주문을 막는 hard gate다.
- `pending_cancel`: cancel 요청은 접수됐지만 cleanup artifact 시점에는 주문 lifecycle이 아직 완전히 정리되지 않은 상태다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim/hold 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `duplicate_symbol_side_same_day`: 같은 symbol/side에서 같은 세션에 이미 체결된 주문이 있어 추가 제출을 막는 규칙이다.
- `sell_metric_gap`: trim 의사결정에 필요한 expected-excess 또는 replacement margin이 비어 있어 집행형 trim으로 승격하지 못한 상태다.
