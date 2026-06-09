# 2026-06-09-2351-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `2351` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup과 core preflight 모두 open order `0`건으로 lifecycle block이 해소된 상태를 보여줬다. 이번 cycle은 sell/trim을 먼저 재평가했지만 `AVGO`는 spread `3.5054%`로 hard gate fail, `RGTI`는 2026-06-09 ET same-day sell fill 때문에 duplicate symbol/side conflict, `SO`는 decision-grade replacement margin 공백으로 trim 승격에 실패했다. `BAC`는 2331 cycle buy 1주가 14:45Z same-day fill로 확인돼 buy-side duplicate gate에 걸렸다. 따라서 learning_trade_directive에 따라 `WMT` 1주 regular-session day limit buy를 floor-size validation fallback으로 제출했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler core preflight `2026-06-09T10:51:11.454264746-04:00`, regular market open |
| Stale order cleanup | PASS | stale candidate/open order 모두 `0`건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, quotes/assets/orders 모두 포함 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage는 `empty_response` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | `WMT` quote `118.94/118.99`, spread `0.0420%`, freshness 약 `0.10`분 |
| Risk plan | PASS | strict risk validator 통과, 경고는 staged deployment 유지 안내만 존재 |
| Final submit path | PASS | registered Alpaca MCP `place_stock_order` 성공, immediate reconciliation까지 수행 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | watch | 3.5054% | trim thesis는 유지되지만 live spread가 정책 상한 초과 |
| RGTI | watch | 0.0974% | speculative loss-control trim trigger 유지, 다만 same-day earlier sell fill로 duplicate conflict |
| SO | watch | 0.0326% | spread는 정상이나 decision-grade replacement margin 공백 지속 |
| BAC | watch | 0.0186% | 2331 cycle buy 1주가 same-day fill로 확인돼 이번 cycle buy duplicate gate |
| WMT | submitted open | 0.0420% | 1D review `중립 양호`, defensive diversifier, duplicate/open-order conflict 없음, per-order cap 이내 |
| SPY | watch | 0.0082% | benchmark fallback이지만 1주 ask가 validation_floor per-order cap 초과 |
| QQQ | watch | 0.0282% | benchmark fallback이지만 1주 ask가 validation_floor per-order cap 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_out_of_policy | open-order lifecycle은 해소됐지만 live spread가 0.50% 상한 초과 |
| RGTI | watch | duplicate_symbol_side_same_day | earlier `RGTI` sell fill 22주가 있어 추가 same-day sell 제출 차단 |
| SO | watch | decision_grade_metric_gap | live spread는 정상이나 trim justification용 replacement margin 공백 지속 |

## 주문 제출과 reconciliation

- Submitted order: `WMT` buy 1 @ `118.99` day limit
- Alpaca order: `order_id=487039ff-24cb-4094-9301-add50be8886c`, `client_order_id=hourly-20260609-2351-buy-wmt`
- Immediate status: `new`, `filled_qty=0`, `filled_avg_price=null`, `expires_at=2026-06-09T20:00:00Z`
- Reconciliation: `get_order_by_client_id`와 `get_orders(status=open, symbols=WMT)` 모두 동일 open order 1건을 확인했다. `get_account_activities(activity_types=FILL, after=2026-06-09T14:40:00Z)`에는 `BAC` buy 1 fill만 있고 `WMT` fill은 아직 없다. `get_all_positions`는 `32` positions 유지, `WMT`는 아직 `6주` 그대로이며 `get_account_info`는 portfolio value `99,280.96 USD`, cash `32,211.32 USD`, buying power `300,869.80 USD`를 확인했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | positive research confirmations 4개 유지 |
| `check-risk-policy.py --json` | PASS | staged deployment 경고만 존재 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-09-2351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-09-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-09-2351-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-09-2351-hourly-autopilot-post-trade.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-09-2351-hourly-autopilot-runtime-gate-evaluation.json`
- Deterministic submit note: `wiki/evidence-store/sources/2026-06-09-2351-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `spread_out_of_policy`: trim signal이 있어도 live spread가 `harness/risk-policy.yaml` 상한을 넘으면 submit을 막는 hard gate다.
- `learning_trade_directive`: hard gate가 모두 통과하고 executable sell이 없을 때 benchmark/diversifier/existing holding의 floor-size buy를 강제하는 validation policy다.
- `empty_response`: 이번 run의 Alpha Vantage는 candidate news item이 0건이라 `empty_response` gap으로만 기록됐고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과한다.
