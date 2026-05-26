# 2026-05-27 01:31 KST hourly autopilot

## 요약

- 실행 모드: Alpaca paper submit 후보 검증.
- Paper mode: `.env`의 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: 2026-05-26 12:32:08 ET 기준 open, next close 16:00 ET.
- Alpaca core: pass. FCX asset 조회는 1회 cancelled 후 retry pass였고 첫 Alpaca 차단 gate는 없다.
- Research MCP: SEC EDGAR pass, Yahoo Finance pass, FRED preflight pass, Alpha Vantage cancelled, Firecrawl wrapper_error.
- Universe gate: 62개 metadata universe와 `SPY`, `QQQ` 포함, strict 검증 대상.
- 주문 후보: `FCX` 1주 paper validation buy.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 근거 | 차단/주의 |
| ---: | --- | --- | --- | --- |
| 1 | FCX | paper validation buy | fresh quote, pre-submit 0.031% spread, SEC/Yahoo/FRED 3개 research confirmation, unheld materials/mining diversification | commodity-cyclical risk 때문에 1주 검증 주문으로 제한 |
| 2 | NOK | recheck | fresh quote, spread pass, most-active volume, Alpaca news momentum | 이미 400주 보유, 추가매수보다 exposure 관찰 우선 |
| 3 | SMH | recheck | fresh quote, spread pass, semiconductor ETF momentum | 기존 AMD/AVGO/LRCX/NVDA/TSM 보유로 반도체 cluster 집중 |
| 4 | MU | recheck | 강한 당일/월간 모멘텀과 관련 뉴스 | 과열 위험과 반도체 concentration |
| 5 | AAPL | recheck | fresh quote, broad liquidity, benchmark 대비 안정 | FCX보다 current catalyst와 diversification 점수 낮음 |

## 주문 계획

| 티커 | Side | Qty | Type | Limit | Reference | Spread | Rationale |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| FCX | buy | 1 | limit/day | 63.97 | 63.96 | 0.031% | FCX는 fresh quote와 tight spread를 통과했고, SEC 최근 8-K/10-Q, Yahoo의 FCX-specific copper/mining 및 analyst context, FRED macro preflight가 모두 확인됐다. 현재 보유가 없는 materials/mining 노출이라 반도체 집중 포트폴리오를 소액으로 분산한다. |

## 제출/스킵

- 제출 조건: universe strict, MCP strict, risk policy, fresh quote, spread, active tradable asset, market open 모두 통과해야 한다.
- 스킵: NOK는 이미 400주 보유, SMH/MU/AMD/NVDA/AVGO는 반도체 cluster 집중 또는 기존 보유, LLY는 이번 quote spread fail, 보유 종목 sell/trim은 thesis-break/risk-limit/stale-thesis/sizing breach가 없어 제출하지 않는다.

## 제출 결과

- Validator 결과: universe strict PASS, MCP strict PASS, risk policy PASS.
- 제출 전 fresh quote 재확인: 2026-05-26T16:40:36Z FCX bid 63.95 / ask 63.97, spread 0.031%.

| 티커 | Side | Qty | Limit | 상태 | 체결가 | Alpaca order id |
| --- | --- | ---: | ---: | --- | ---: | --- |
| FCX | buy | 1 | 63.97 | filled | 63.94 | 6c6a31ab-2a07-4da1-9e2e-c1dfb57ccee1 |

- `place_stock_order`는 Alpaca MCP로 제출됐고 initial status는 `pending_new`였다.
- `get_orders(status=all, symbols=FCX)` 재조회에서 `2026-05-26T16:41:44.795047598Z` filled를 확인했다.
- `get_all_positions` 재조회에서 FCX 1주, 평균 단가 63.94 포지션을 확인했다.
- `get_order_by_client_id`, `get_order_by_id`, 첫 `get_orders`, 첫 `get_all_positions`, `get_account_activities` 일부 reconciliation 호출은 MCP wrapper cancelled/safety cancellation이 있었고, 같은 주문 id 기준의 `get_orders` retry와 positions retry로 체결을 확인했다.
- 신규 FCX fill은 1D/5D/20D 회고 대기 대상이다.

## MCP Coverage

| MCP | Outcome | Used | Gap category | Note |
| --- | --- | --- | --- | --- |
| alpaca | pass | yes | not_applicable | clock/account/orders/positions/activities/watchlists/quotes/assets/news |
| sec-edgar | pass | yes | not_applicable | local CIK cache 후 FCX company/recent filings 확인 |
| alpha-vantage | failed | no | cancelled | `TOOL_CALL("PING", {})` cancelled, non-PING retry 없음 |
| fred | pass | yes | not_applicable | scheduler preflight `get_macro_snapshot` pass |
| firecrawl | failed | no | wrapper_error | registered Codex MCP tool 미노출 |
| yahoo-finance | pass | yes | not_applicable | FCX news 확인, recommendations call은 cancelled |

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`. Risk policy의 submit 상한은 0.50%다.
- `quote_age_minutes`: 주문 제출 후보는 quote/snapshot 기준 20분 이내여야 한다.
- `confidence_score`: 가격 추세, source confidence, MCP confirmation, thesis-break 부재를 합친 내부 판단 점수다.
- `expected_excess_return_20d_pct`: 20거래일 기준 SPY 대비 기대 초과수익 가정치이며, 실제 성과 보장이 아니다.
- `expected_adverse_move_20d_pct`: 정책 시뮬레이션과 종목 변동성을 반영한 20거래일 불리한 이동 가정치다.

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-0131-hourly-autopilot-sources.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0131-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0131-hourly-autopilot.json`
