# 2026-06-02-0031-hourly-autopilot 정규장 hourly autopilot

## 요약

- 실행 기준: 2026-06-02 00:31 KST / 2026-06-01 11:31 ET 정규장.
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인.
- Alpaca core preflight: clock/account/positions/open orders/recent fills/quote/trade rows 통과. Stale cleanup도 통과했고 남은 open order는 없습니다.
- Research MCP: SEC EDGAR, Firecrawl, Yahoo Finance는 usable/pass. Alpha Vantage와 FRED는 `provider_error` gap으로 분류했습니다. 최소 3개 research confirmation은 충족했습니다.
- 주문 결과: 신규 주문 없음. `place_stock_order`는 호출하지 않았습니다.

## 게이트

| 게이트 | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에 `ALPACA_PAPER_TRADE=true` 존재 |
| Market clock | PASS | Alpaca preflight `is_open=true`, checked_at `2026-06-01T15:31:11Z` |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-06-02-0031-hourly-autopilot-stale-order-cleanup.json` 기준 remaining open orders 없음 |
| Alpaca core MCP | PASS | `wiki/evidence-store/sources/2026-06-02-0031-hourly-autopilot-alpaca-core-preflight.json` |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Research MCP strict | PASS | SEC/Firecrawl/Yahoo 3개 usable, Alpha/FRED gap 기록 |
| Risk validator | PASS | 빈 주문 계획 경고만 예상 |
| Submit eligibility | BLOCKED | 후보 정책 필터와 lifecycle/source/portfolio-fit 조건 미충족 |

## Sell/Trim 진단

| 종목 | 진단 | 차단 게이트 | 결론 |
| --- | --- | --- | --- |
| TSLA | 약한 validation review와 미실현 손실이 있어 recheck 대상 | held_qty_minimum_for_trim | watch |
| SO | rate-sensitive 보유가 약세이나 FRED macro gap과 낮은 비중으로 trim 조건 미달 | sell_trigger_metric_and_macro_gap | hold/watch |
| NEE | utility/rate-sensitive 보유가 약세이나 5D/20D decision metric과 FRED 확인 부족 | decision_grade_metric_and_macro_gap | hold/watch |

## 신규 Buy 후보

BAC, COP, SLB, SO, WMT를 재점검했지만 신규 매수로 승격하지 않았습니다. BAC/SO는 macro/rate-sensitive thesis에 FRED provider gap이 남아 watch로 강등했고, SLB/WMT는 validation lifecycle pending review 및 backlog throttle 제약이 남아 있습니다. COP는 이미 보유한 energy exposure 대비 portfolio contribution/replacement rank가 신규 노출을 정당화하지 못했습니다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-02-0031-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-02-0031-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-02-0031-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-02-0031-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-02-0031-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-02-0031-hourly-autopilot-research-mcp-preflight.json`

## 지표 설명

- `sell_candidate_diagnostics`: risk-trim 정책 기준으로 보유 종목 중 trim/exit 재점검이 필요한 상위 후보입니다. 주문이 없어도 metric 또는 metric gap reason을 기록합니다.
- `review_backlog_pending_1d_count`: validation buy의 1D 회고 대기 수입니다. 이번 run에서는 10개로 신규 buy slot이 1개까지 축소되며, sell/trim 진단에는 적용하지 않습니다.
- `gap_category=provider_error`: MCP wrapper는 호출됐지만 provider 응답/제한으로 usable evidence가 되지 않은 상태입니다.
