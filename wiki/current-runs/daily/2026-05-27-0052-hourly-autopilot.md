# 2026-05-27 00:52 KST hourly autopilot

## 요약

- 실행 모드: Alpaca paper submit 후보 검증.
- Paper mode: `.env`의 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: 2026-05-26 11:52:30 ET 기준 open, next close 16:00 ET.
- Alpaca core: pass. Positions 조회는 1회 cancelled 후 retry pass였고 첫 Alpaca 차단 gate는 없다.
- Research MCP: SEC EDGAR pass, Yahoo Finance pass, FRED preflight pass, Alpha Vantage cancelled, Firecrawl wrapper_error.
- Universe gate: 62개 metadata universe와 `SPY`, `QQQ` 포함, strict pass.
- 주문 후보: `LLY` 1주 paper validation buy.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 근거 | 차단/주의 |
| ---: | --- | --- | --- | --- |
| 1 | LLY | paper validation buy | fresh quote, 0.105% spread, SEC/Yahoo/FRED 3개 research confirmation, Alpaca catalyst news, 미보유 | 단일 1주 검증 주문으로 제한 |
| 2 | FCX | recheck | fresh quote, spread pass, commodity rebound | LLY보다 회사 이벤트/분석 confirmation 약함 |
| 3 | NOK | recheck | fresh quote, spread pass, Alpaca news momentum | 이미 400주 보유, 추가매수보다 관찰 우선 |
| 4 | MU | recheck | 강한 당일/월간 모멘텀 | 과열 위험과 포트폴리오 반도체 클러스터 집중 |
| 5 | AMD | skip | 보유 중, 모멘텀 양호 | snapshot spread fail |

## 주문 계획

| 티커 | Side | Qty | Type | Limit | Reference | Spread | Rationale |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| LLY | buy | 1 | limit/day | 1079.78 | 1079.34 | 0.082% | GLP-1/대사질환 및 gene-therapy 촉매가 Alpaca news에 있고, SEC 최근 filing과 Yahoo analyst/news, FRED macro preflight가 모두 확인됐다. 기존 LLY 보유가 없고 1주 검증 주문은 현금/티커/theme/risk 한도 안에 있다. |

## 제출/스킵

- 제출 조건: universe strict, MCP strict, risk policy, fresh quote, spread, active tradable asset, market open 모두 통과해야 한다.
- 스킵: AMD/LRCX는 spread fail. NOK는 이미 보유 중이고 신규 추가보다 LLY 미보유 validation이 우선. 보유 종목 sell/trim은 thesis-break, risk-limit, stale-thesis, sizing breach가 없어 제출하지 않았다.

## 제출 결과

| 티커 | Side | Qty | Limit | 상태 | 체결가 | Alpaca order id |
| --- | --- | ---: | ---: | --- | ---: | --- |
| LLY | buy | 1 | 1079.78 | filled | 1079.38 | f2626164-9d01-4134-97ab-5e73748fc790 |

- 첫 `place_stock_order` 시도는 MCP safety wrapper에서 cancelled 되었고, 동일 idempotent client order id로 1회 retry했다.
- retry는 Alpaca MCP로 성공했고, `get_orders` 재조회에서 2026-05-26T16:02:35.719698Z에 filled를 확인했다.
- `get_all_positions`에서 LLY 1주, 평균 단가 1079.38 포지션을 확인했다.
- 신규 fill이 있으므로 LLY는 1D/5D/20D 회고 대기 대상이다.

## MCP Coverage

| MCP | Outcome | Used | Gap category | Note |
| --- | --- | --- | --- | --- |
| alpaca | pass | yes | not_applicable | clock/account/orders/positions/activities/watchlists/quotes/assets/news |
| sec-edgar | pass | yes | not_applicable | local CIK cache 후 LLY company/recent filings 확인 |
| alpha-vantage | failed | no | cancelled | `TOOL_CALL("PING", {})` cancelled |
| fred | pass | yes | not_applicable | scheduler preflight `get_macro_snapshot` pass |
| firecrawl | failed | no | wrapper_error | registered Codex MCP tool 미노출 |
| yahoo-finance | pass | yes | not_applicable | LLY news/recommendations 확인 |

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`. Risk policy의 submit 상한은 0.50%다.
- `quote_age_minutes`: 주문 제출 후보는 quote/snapshot 기준 20분 이내여야 한다.
- `confidence_score`: 가격 추세, source confidence, MCP confirmation, thesis-break 부재를 합친 내부 판단 점수다.
- `expected_excess_return_20d_pct`: 20거래일 기준 SPY 대비 기대 초과수익 가정치이며, 실제 성과 보장이 아니다.
- `expected_adverse_move_20d_pct`: 정책 시뮬레이션과 종목 변동성을 반영한 20거래일 불리한 이동 가정치다.

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-0052-hourly-autopilot-sources.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0052-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0052-hourly-autopilot.json`
