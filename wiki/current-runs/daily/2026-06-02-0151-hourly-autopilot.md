# 2026-06-02-0151-hourly-autopilot scheduled paper autopilot

## 요약

- 워크플로우: `harness/workflows/hourly-autopilot.md` 정규장 scheduled paper autopilot.
- Paper mode: `.env`에서 `ALPACA_PAPER_TRADE=true` 확인.
- 시장 상태: Alpaca scheduler preflight 기준 2026-06-01T12:51:11.652119441-04:00 정규장 열림, next_close 2026-06-01T16:00:00-04:00.
- 계좌 상태: portfolio value $103,133.85, cash $34,339.00, invested ratio 66.70%, 보유 포지션 32개.
- 주문 결과: 신규 주문 없음. `place_stock_order` 호출 없음.
- 첫 차단 게이트: `candidate_policy_filters_no_order`.

## 게이트

| 게이트 | 결과 | 근거 |
| --- | --- | --- |
| stale order cleanup | PASS | scheduler cleanup 결과 stale/open autopilot order 없음 |
| Alpaca core | PASS | clock/account/positions/open orders/recent activities/quotes 모두 pass; 첫 blocking gate 없음 |
| Universe | PASS | metadata 62개, 보유 종목, SPY/QQQ 포함 |
| Research MCP | PASS | SEC EDGAR, Firecrawl, Yahoo usable/pass 3개 확인; Alpha empty_response와 FRED provider_error는 gap으로 기록 |
| Risk validator | PASS | 주문 없음 경고만 발생 |

Validators: `check-universe-coverage.py --strict --json` PASS, `check-mcp-coverage.py --strict --json` PASS, `check-risk-policy.py --json` PASS (`orders is empty` warning).

## Sell/Trim 진단

| Symbol | 판단 | 차단 게이트 | 메모 |
| --- | --- | --- | --- |
| TSLA | watch | held_qty_minimum_for_trim | 1주 보유라 1주 trim 후 최소 잔여 1주 조건을 동시에 만족 불가 |
| SO | hold/watch | decision_grade_metric_and_macro_gap | 약세지만 FRED 429와 5D/20D decision metric 공백으로 trim 미확정 |
| NEE | hold/watch | decision_grade_metric_and_macro_gap | 3주 보유라 수량은 가능하지만 rate-sensitive macro/decision metric 공백 |

## 신규 Buy 후보

- BAC: rate-sensitive thesis가 FRED macro/rates 확인 공백 때문에 watch로 강등.
- NKE: validation lifecycle pending review 때문에 신규 add를 보류.
- NVDA: SEC/Firecrawl/Yahoo 근거는 usable/pass지만 AI semiconductor cluster target-band 제약 때문에 신규 same-cluster 노출을 보류.
- GOOGL/WMT: validation lifecycle, review backlog throttle, replacement rank/portfolio contribution 조건이 신규 노출을 정당화하지 못함.
- validation backlog는 신규 buy 슬롯만 1개로 축소했으며, sell/trim 진단은 독립적으로 평가했다.

## 제출 전 판단

pre-submit gate summary는 주문 후보가 없어 작성 대상이 아니었다. Paper mode, market clock, universe/MCP/risk validator는 통과했지만 order plan의 `orders`가 비어 있어 `place_stock_order`를 호출하지 않았다.

## 지표 설명

- `first_blocking_gate`: 주문 제출 전에 가장 먼저 주문을 막은 정책 또는 데이터 게이트.
- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 검토가 필요한 상위 후보와 metric gap 사유.
- `review_backlog_pending_1d_count`: validation buy 후 1D 회고가 아직 완료되지 않은 항목 수. 이 값은 신규 buy 슬롯만 줄이며 sell/trim 진단은 독립적으로 유지한다.
- `gap_category`: MCP 공백 분류. 이번 run에서는 Alpha `empty_response`, FRED `provider_error`로 기록했다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-02-0151-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-02-0151-hourly-autopilot.json`
- Position snapshot: `wiki/trade-ledger/positions/2026-06-02-0151-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-02-0151-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-02-0151-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-02-0151-hourly-autopilot-research-mcp-preflight.json`
