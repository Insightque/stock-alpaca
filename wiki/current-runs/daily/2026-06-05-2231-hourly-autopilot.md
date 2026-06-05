# 2026-06-05-2231-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `2231` stale cleanup/core/research preflight를 우선 사용했다. runtime Alpaca clock `2026-06-05T09:34:21.060631313-04:00` 기준 미국 정규장은 열려 있었고, research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였으며 `alpha-vantage`는 `empty_response` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. 반면 `BAC`는 scheduler shortlist 포함, live quote `53.90/53.92`, spread `0.0371%`, same-day duplicate/open-order 없음, review backlog throttle 통과, 2026-06-05 portfolio review 기준 5D validation 성과 양호라는 조건을 동시에 만족해 floor-size learning buy 1주 후보로 승격했다. strict universe/MCP/risk validator를 모두 통과하면 BAC 1주 day limit buy를 제출한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` `2026-06-05T09:34:21.060631313-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, runtime open orders 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_clock/get_account_info/get_orders/get_asset(BAC)/get_stock_latest_quote(BAC)` 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage는 `empty_response` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | BAC runtime quote `2026-06-05T13:35:19.525543916Z`, spread `0.0371%` |
| Risk plan | PASS | BAC 1주 buy notional `53.92`, cash/ticker/theme/factor/cluster caps 통과 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| BAC | submitted_filled | 0.0371% | existing financials diversifier이고 5D review가 가장 강하며 hard gate 전체를 통과해 제출됐고 `53.83 USD`에 체결됐다. |
| SLB | watch | preflight usable | 5D follow-through는 양호하지만 BAC보다 diversification과 review signal이 덜 명확했다. |
| AAPL | watch | preflight usable | mega-cap quality add는 가능하지만 현재 포트폴리오의 mega-cap 노출 대비 BAC의 분산 기여가 더 컸다. |
| WMT | watch | preflight usable | defensive-diversification bucket의 최근 5D 성과가 중립 약함이라 BAC보다 우선순위가 낮았다. |
| SPY | watch | preflight usable | benchmark floor buy는 fallback으로 유지했지만 BAC가 더 나은 학습 표본으로 남았다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Planned order: `BAC` buy 1 @ `53.92` day limit
- Alpaca order id: `ecd6232b-91ac-4e8a-a0f1-2a338bcf01db`
- Client order id: `hourly-20260605-2231-buy-bac`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, BAC quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: Alpaca accepted the order at `2026-06-05T13:39:10.344124456Z` and `get_order_by_client_id` confirmed `filled_at=2026-06-05T13:39:42.716508022Z`, `filled_avg_price=53.83`
- Reconciliation: `get_orders(status=open)` returned `0` open orders after fill. direct post-fill `get_all_positions/get_account_info` refresh는 runtime safety monitor가 취소해, post-trade snapshot은 fresh 2231 core preflight 포지션과 confirmed fill을 결합해 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | BAC 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-2231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-2231-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-2231-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `empty_response`: 이번 cycle의 Alpha Vantage는 candidate shortlist에 대한 `NEWS_SENTIMENT` 항목이 0건이어서 nonblocking gap으로 남겼다.
- `review_backlog_throttle`: pending review 개수에 따라 신규 validation buy 슬롯을 줄이거나 막는 정책인데, 이번 run은 `pending_1d_count=0`이라 buy stop 조건에 닿지 않았다.
- `portfolio_construction_policy`: 신규 buy를 기존 보유와 비교해 분산 기여와 replacement rank를 함께 평가하는 규칙이다.
