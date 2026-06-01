# 2026-06-02-0431-hourly-autopilot scheduled paper autopilot

## 요약

- 워크플로우: `harness/workflows/hourly-autopilot.md` 정규장 scheduled paper autopilot.
- Paper mode: `.env`에서 `ALPACA_PAPER_TRADE=true` 확인.
- 시장 상태: Alpaca scheduler preflight 기준 2026-06-01T15:31:14.102484492-04:00 정규장 열림, next_close 2026-06-01T16:00:00-04:00.
- 계좌 상태: portfolio value $103,269.87, cash $34,339.00, invested ratio 66.75%, 보유 포지션 32개.
- 주문 결과: 신규 주문 없음. `place_stock_order` 호출 없음.
- 첫 차단 게이트: `buy_entry_window_closed_no_eligible_sell_trim`.

## 게이트

| 게이트 | 결과 | 근거 |
| --- | --- | --- |
| stale order cleanup | PASS | scheduler cleanup 결과 stale/open autopilot order 없음 |
| Alpaca core | PASS | scheduler preflight가 clock/account/positions/open orders/recent activities/quotes 모두 pass; quote row 2026-06-01T19:31:35Z 기준 사용 |
| Open orders | PASS | scheduler Alpaca MCP `get_orders` 결과 open order 없음 |
| Positions | PASS | scheduler Alpaca MCP `get_all_positions`가 32개 보유 종목을 확인; order plan에 현재 포지션 포함 |
| Universe | PASS | metadata/preflight universe 62개, 보유 종목, SPY/QQQ 포함 |
| Research MCP | PASS | SEC EDGAR, Firecrawl, Yahoo usable/pass 3개 확인; Alpha provider_error와 FRED provider_error 429는 gap으로 기록 |
| Risk validator | PASS | 주문 없음 경고만 발생 |

Validators: `check-universe-coverage.py --strict --json` PASS, `check-mcp-coverage.py --strict --json` PASS, `check-risk-policy.py --json` PASS (`orders is empty` 경고만 발생).

## Sell/Trim 진단

| Symbol | 판단 | 차단 게이트 | 메모 |
| --- | --- | --- | --- |
| TSLA | watch | held_qty_minimum_for_trim | 1주 보유라 1주 trim 후 최소 잔여 1주 조건을 동시에 만족 불가 |
| SO | hold/watch | decision_grade_metric_and_macro_gap | 약세지만 FRED 429와 5D/20D decision metric 공백으로 trim 미확정 |
| NEE | hold/watch | decision_grade_metric_and_macro_gap | 3주 보유라 수량은 가능하지만 rate-sensitive macro/decision metric 공백 |

## 신규 Buy 후보

- 22:31-23:31 KST regular validation buy entry window가 닫혀 신규 buy 노출은 만들지 않았다.
- BAC: rate-sensitive thesis가 FRED macro/rates 확인 공백 때문에 watch로 강등.
- NKE/GOOGL/AMZN/WMT: validation lifecycle pending review와 portfolio-fit 조건 때문에 add 보류.
- NVDA: SEC/Firecrawl/Yahoo 근거는 usable/pass지만 AI semiconductor cluster target-band 제약 때문에 신규 same-cluster 노출 보류.
- validation backlog는 신규 buy 슬롯만 1개로 축소했으며, sell/trim 진단은 독립적으로 평가했다.

## 제출 전 판단

pre-submit gate summary는 주문 후보가 없어 작성 대상이 아니었다. Paper mode, market clock, universe/MCP/risk validator는 통과했지만 order plan의 `orders`가 비어 있어 `place_stock_order`를 호출하지 않았다.

## 지표 설명

- `first_blocking_gate`: 주문 제출 전에 가장 먼저 주문을 막은 정책 또는 데이터 게이트.
- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 검토가 필요한 상위 후보와 metric gap 사유.
- `review_backlog_pending_1d_count`: validation buy 후 1D 회고가 아직 완료되지 않은 항목 수. 이 값은 신규 buy 슬롯만 줄이며 sell/trim 진단은 독립적으로 유지한다.
- `gap_category`: MCP 공백 분류. 이번 run에서는 Alpha `provider_error`, FRED `provider_error`로 기록했다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-02-0431-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-02-0431-hourly-autopilot.json`
- Position snapshot: `wiki/trade-ledger/positions/2026-06-02-0431-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-02-0431-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-02-0431-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-02-0431-hourly-autopilot-research-mcp-preflight.json`
