# 2026-05-27 03:11 KST hourly autopilot

## 요약

- 실행 모드: scheduled Alpaca paper autopilot, submit gate 검증.
- Paper mode: `.env`의 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: scheduler-owned Alpaca preflight `2026-05-26T14:11:10.836217373-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Alpaca core: pass. Preflight의 clock/account/open orders/positions/fills/watchlist/asset/quote/snapshot/latest trade가 usable했다.
- First blocking gate: `research_mcp_minimum_confirmations`.
- Research MCP: FRED preflight pass, Yahoo Finance usable, SEC EDGAR cancelled, Alpha Vantage cancelled, Firecrawl wrapper_error. Research usable count는 2개로 submit 기준 3개에 미달한다.
- Universe gate: 62개 metadata universe와 `SPY`, `QQQ` 포함.
- 주문 계획/실행: 주문 없음. 기존 AAPL open buy order가 있고, research MCP strict gate가 실패했으므로 `place_stock_order`는 호출하지 않았다.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 근거 | 차단/주의 |
| ---: | --- | --- | --- | --- |
| 1 | AMZN | actionable_if_provider_recovered | mega-cap quality 분산 후보, Alpaca quote spread 0.0152%, Yahoo recommendation usable | SEC/Alpha cancelled로 research confirmation 2개에 그침 |
| 2 | INTC | actionable_if_provider_recovered | 반도체 laggard/AI capex 재평가 후보, spread 0.0408% | high-volatility, SEC/Alpha cancelled |
| 3 | SMH | recheck | 반도체 ETF momentum, spread 0.0467% | ETF라 SEC CIK lookup 공백, AI semiconductor cluster 집중 주의 |
| 4 | AAPL | skip | spread 0.0097%로 quote gate는 양호 | 직전 run의 AAPL buy order `new`가 열려 있어 duplicate/open-order gate 차단 |
| 5 | MU | recheck | 강한 momentum | spread 0.4796%로 0.50% 상한에 근접 |

## 주문 계획

| 티커 | Side | Qty | Type | Limit | Rationale |
| --- | --- | ---: | --- | ---: | --- |
| 없음 | - | 0 | - | - | Research MCP usable/pass가 FRED와 Yahoo 2개뿐이라 buy submit 기준 3개를 충족하지 못했다. 기존 AAPL open order도 duplicate/open-order gate로 신규 AAPL 주문을 막는다. |

## 제출/스킵

- Validator: universe strict PASS, MCP strict FAIL, empty-order risk policy PASS.
- MCP strict failure: research MCP gate requires at least 3 usable/pass research providers; got 2 (`fred`, `yahoo-finance`).
- Submit: 없음. `place_stock_order` 호출 없음.
- Same-day fills: `LLY`, `FCX`, `NOK`, `NVDA` buy fills가 preflight에 있다. 같은 종목 추가 buy는 duplicate/review cadence상 skip했다.
- Open order: `AAPL` 1주 limit buy status `new`; 신규 AAPL 주문은 skip했다.
- Active trim triggers: 개별 ticker 15% cap, speculative 12% cap, cash 20% floor, invested 80% cap은 현재 위반하지 않는다. thesis-break나 stale-thesis underperformance만으로 즉시 trim할 보유 종목은 없다.

## MCP Coverage

| MCP | Outcome | Used | Gap category | Note |
| --- | --- | --- | --- | --- |
| alpaca | pass | yes | not_applicable | scheduler preflight hard gate pass, quote rows <20분 |
| sec-edgar | failed | no | cancelled | local CIK fallback 후 SEC MCP calls cancelled |
| alpha-vantage | failed | no | cancelled | health pass 후 first non-PING candidate call cancelled |
| fred | pass | yes | not_applicable | scheduler preflight `get_macro_snapshot` pass |
| firecrawl | failed | no | wrapper_error | Codex tool catalog에 registered Firecrawl MCP tool 미노출 |
| yahoo-finance | usable | yes | not_applicable | AMZN recommendations pass, news call cancelled |

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`. Risk policy의 submit 상한은 0.50%다.
- `quote_age_minutes`: 주문 제출 후보는 quote/snapshot 기준 20분 이내여야 한다.
- `first_blocking_gate`: 주문 제출을 중단시킨 첫 hard gate다. 이번 run은 research MCP usable/pass 3개 미달이다.
- `research MCP confirmation`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass인 provider 수다. 이번 run은 FRED/Yahoo 2개다.
- `validation floor`: paper 검증 목적의 1주 소액 주문은 모든 hard gate가 통과할 때만 허용된다.

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-0311-hourly-autopilot-sources.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0311-hourly-autopilot.json`

## 회고 대기

- 이번 run 신규 fill 없음.
- AAPL order는 open `new` 상태라 체결 회고는 아직 생성하지 않는다.
- LLY/FCX/NOK/NVDA 및 2026-05-22 체결분은 계속 `회고 대기`다.
