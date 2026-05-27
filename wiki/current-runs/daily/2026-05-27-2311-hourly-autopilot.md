---
id: 2026-05-27-2311-hourly-autopilot
created_at: 2026-05-27T14:15:30Z
workflow: hourly-autopilot
paper: true
---

# 2026-05-27 23:11 KST Hourly Autopilot

## 실행 요약

- Paper mode: `.env`/환경에서 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: Alpaca scheduler preflight 기준 `2026-05-27T10:11:13.225633645-04:00`, 정규장 open, next close `2026-05-27T16:00:00-04:00`.
- Stale order cleanup: 통과. stale autopilot order 0건, remaining open order 0건.
- Alpaca core MCP: clock/account/positions/open orders/recent fills/assets/quotes/snapshots/trades pass.
- Research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 후보 뉴스 0건으로 `empty_response` gap. Buy actionability에 필요한 usable/pass 3개 이상은 충족.
- Universe: `harness/symbol-metadata.yaml`와 현재 포지션, Alpaca preflight universe, SPY/QQQ 포함 62개 loaded.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 핵심 이유 | 제한 |
| ---: | --- | --- | --- | --- |
| 1 | GOOGL | 1주 validation buy | +0.33% intraday, 0.0282% spread, mega-cap quality growth 노출 보강 | mega_cap_tech cluster는 아직 정책 한도 미만 |
| 2 | WMT | 1주 validation buy | defensive quality/consumer defensive 분산, 0.0338% spread | 당일 약보합이라 validation size로만 제한 |
| 3 | NEE | 1주 validation buy | utilities_power/defensive yield 분산, 0.0229% spread | 당일 약보합이라 validation size로만 제한 |
| - | AAPL/BAC/QQQ/SPY/FCX/NOK/IONQ | recheck | 일부는 이미 보유 또는 momentum/cluster/portfolio fit이 약해 이번 3개 슬롯 밖 | 신규 주문 없음 |
| - | NKE/PFE/SO | skip duplicate | 22:46 run에서 같은 날 buy 체결됨 | same-day duplicate symbol/side 회피 |

## 주문 계획

| 티커 | 방향 | 수량 | 지정가 | 기준 quote | Spread | 주문 근거 |
| --- | --- | ---: | ---: | --- | ---: | --- |
| GOOGL | buy | 1 | 390.57 | `2026-05-27T14:11:33.48205341Z` | 0.0282% | quality growth validation, tight spread, no open duplicate |
| WMT | buy | 1 | 118.38 | `2026-05-27T14:11:33.078366576Z` | 0.0338% | defensive consumer diversification, tight spread, validation size |
| NEE | buy | 1 | 87.34 | `2026-05-27T14:11:33.704861043Z` | 0.0229% | utility/defensive-yield diversification, tight spread, validation size |

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | source_refs |
| --- | --- | --- | --- | --- | --- |
| alpaca | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2311-hourly-autopilot-alpaca-core-preflight.json` |
| sec-edgar | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2311-hourly-autopilot-research-mcp-preflight.json` |
| alpha-vantage | true | false | gap | empty_response | `wiki/evidence-store/sources/2026-05-27-2311-hourly-autopilot-research-mcp-preflight.json` |
| fred | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2311-hourly-autopilot-research-mcp-preflight.json` |
| firecrawl | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2311-hourly-autopilot-research-mcp-preflight.json` |
| yahoo-finance | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2311-hourly-autopilot-research-mcp-preflight.json` |

## 제출 전 Gate 상태

- Universe strict: PASS.
- MCP strict: PASS.
- Risk policy: PASS. `buy_notional=596.29`, `post_cash=41584.53`, `post_invested=59573.37`.
- Quote freshness: 약 4분, 20분 정책 이내.
- Spread: 0.0229%~0.0338%, 0.50% 한도 이내.
- Order shape: whole-share long-only stock day limit orders.
- Duplicate/open-order check: open orders 0건, same-day NKE/PFE/SO 중복 buy는 제외.

## 지표 설명

- `quote_age_minutes`: 주문 판단 시점과 Alpaca quote timestamp 사이의 시간이다. Submit mode에서는 20분 이내여야 한다.
- `spread_pct`: ask와 bid 차이를 중간값으로 나눈 비율이다. 낮을수록 지정가 체결 비용과 미체결 위험이 작다.
- `confidence_score`: trend, MCP 원천, 리스크, 포트폴리오 fit을 합친 내부 점수다. 0.50 이상이면 medium source confidence validation 후보가 될 수 있다.
- `expected_excess_return_20d_pct`: SPY 대비 20거래일 기대 초과수익 추정치다. 실제 수익 보장이 아니라 후보 간 우선순위 입력값이다.
- `expected_adverse_move_20d_pct`: 20거래일 안에 불리하게 움직일 수 있는 손실폭 추정치다.
- `review_horizons`: paper validation 주문을 1D/5D/20D 뒤에 회고해 정책 개선 자료로 쓰는 기간이다.

## 제출 및 사후 점검

| 티커 | client_order_id | 결과 | 체결 | 비고 |
| --- | --- | --- | --- | --- |
| GOOGL | `hourly-20260527-2311-googl-buy-1` | submitted, open `new` | 0/1 | day limit 390.57, client-order reconciliation pass |
| WMT | `hourly-20260527-2311-wmt-buy-1` | submitted, `filled` | 1/1 @ 118.31 | fill activity 확인 |
| NEE | `hourly-20260527-2311-nee-buy-1` | submitted, open `new` | 0/1 | day limit 87.34, client-order reconciliation pass |

Post-trade account snapshot: portfolio value 101221.29 USD, cash 42062.51 USD, buying power 136411.95 USD, long market value 59158.78 USD.

Post-trade gap: `get_orders(status=open)` list reconciliation returned `cancelled` once. Submitted order state is still reconciled through `get_order_by_client_id` for all three client IDs; open lifecycle follow-up is required for GOOGL and NEE if they remain unfilled near the stale-order threshold.

Post-trade source: `wiki/evidence-store/sources/2026-05-27-2311-hourly-autopilot-post-trade.json`.
