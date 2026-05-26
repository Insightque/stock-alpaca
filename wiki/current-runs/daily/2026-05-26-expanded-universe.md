---
date: 2026-05-26
run_id: 2026-05-26-1620-expanded-universe-recommendation
mode: dry_run
paper: true
status: completed_non_actionable
recommendation_actionability: non_actionable_research
---

# 확장 Universe 기반 종목 추천 - 2026-05-26

## 요약

추천 정책을 한 단계 강화해 watchlist 중심이 아니라 `harness/symbol-metadata.yaml`의 62개 확장 universe를 먼저 스크리닝했다. `SPY`, `QQQ`를 benchmark로 포함했고 universe gate는 strict PASS했다.

다만 최종 후보군에 대한 Firecrawl IR 원문 캡처가 일부 실패했으므로 이번 결과는 `non_actionable_research`다. 실제 주문, 취소, 포지션 변경은 없다.

## Universe Coverage

| 항목 | 값 |
| --- | --- |
| Universe source | `harness/symbol-metadata.yaml` + Alpaca watchlists + current holdings |
| Symbols considered | 62 |
| Symbols loaded | 62 |
| Minimum required | 50 |
| Benchmarks | `SPY`, `QQQ` |
| Screening method | broad universe price/liquidity screen -> all-MCP shortlist validation |
| Pre-MCP shortlist | `LLY`, `LRCX`, `AAPL`, `SMH`, `ASML` |
| Final candidates | `LRCX`, `LLY`, `ASML` |
| Gate result | PASS (`scripts/check-universe-coverage.py --strict`) |

## 1차 스크리닝 결과

| 티커 | 5D | 20D | 40D | 20D vs SPY | 20D vs QQQ | 판정 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| RGTI | +48.04% | +59.05% | +83.02% | +54.61%p | +50.98%p | speculative/overheat로 신규 추격 제외 |
| QBTS | +44.25% | +58.77% | +100.00% | +54.33%p | +50.70%p | speculative/overheat로 신규 추격 제외 |
| MU | +3.73% | +51.36% | +111.33% | +46.92%p | +43.29%p | 40D 과열로 관찰 |
| NOK | +10.79% | +48.18% | +87.04% | +43.74%p | +40.11%p | 과열/중간 source confidence로 추격 제외 |
| IONQ | +22.43% | +49.06% | +113.03% | +44.62%p | +40.99%p | speculative/overheat로 신규 추격 제외 |
| AMD | +10.30% | +34.46% | +129.53% | +30.02%p | +26.40%p | 기존 보유 유지, 신규 매수는 과열로 보류 |
| LLY | +6.06% | +20.75% | +18.96% | +16.31%p | +12.68%p | shortlist |
| LRCX | +7.41% | +14.17% | +44.26% | +9.73%p | +6.10%p | shortlist |
| AAPL | +2.87% | +14.04% | +22.23% | +9.60%p | +5.97%p | target upside 제한으로 관찰 |
| SMH | +3.42% | +13.72% | +51.35% | +9.28%p | +5.65%p | ETF/반도체 cluster 중복으로 관찰 |
| ASML | +8.76% | +12.29% | +23.03% | +7.85%p | +4.22%p | shortlist |

## 재추천

| 순위 | 티커 | 판단 | 근거 | 리스크 |
| --- | --- | --- | --- | --- |
| 1 | LRCX | 최우선 후보, 단 신규 주문은 보류 | 20D +14.17%, SPY 대비 +9.73%p, QQQ 대비 +6.10%p. 기존 all-MCP 자료에서 SEC/Alpha/FRED/Firecrawl/Yahoo 확인 완료. 반도체 장비 테마 중 AMD/MU/INTC보다 과열 부담이 작음. | forward PE 약 38.5, beta 1.82, AI 반도체 cluster 노출이 이미 큼. |
| 2 | LLY | 방어적 성장 후보 | 20D +20.75%, beta 0.48, Yahoo analyst `buy`, forward PE 약 24. 확장 universe에서 비투기/비과열 종목 중 가장 강한 상대강도. | Firecrawl IR 캡처 실패로 source confidence를 high로 올리지 않음. SEC 8-K/144 확인 필요. |
| 3 | ASML | 반도체 장비 대안 후보 | 20D +12.29%, Yahoo `strong_buy`, forward PE 약 34.3. LRCX와 같은 장비 테마지만 글로벌 EUV 핵심 노출. | SEC filing 조회 일부 실패, Firecrawl IR 캡처 실패, 고가/ADR 변동성. |

## 보유/제외 판단

- `AMD`: 보유 관찰. 20D +34.46%, 40D +129.53%라 신규 매수는 강화 정책상 과열로 보류.
- `UNH`: 이전 추천보다 우선순위 하향. 20D +9.48%로 양호하지만 확장 universe 기준에서는 `LLY`의 상대강도/리스크 조합이 더 낫다.
- `AAPL`: 20D +14.04%는 좋지만 Yahoo target mean이 현재가와 거의 같아 신규 추천에서는 제외.
- `RGTI`, `QBTS`, `IONQ`: 강한 모멘텀은 인정하지만 speculative/overheat 규칙으로 신규 추격 제외.
- `MU`, `NOK`, `INTC`: 20D 모멘텀은 매우 강하지만 40D 과열이 커서 신규 진입 보류.

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | source_refs | gap_reason |
| --- | --- | --- | --- | --- | --- |
| Alpaca | true | true | pass | `2026-05-26-expanded-universe-bars.json`, `2026-05-26-expanded-universe-screen.json`, `2026-05-26-current-alpaca-account-news.json` |  |
| SEC EDGAR | true | true | pass | `2026-05-26-expanded-shortlist-all-mcp.json` |  |
| Alpha Vantage | true | true | pass | `2026-05-26-expanded-shortlist-all-mcp.json` |  |
| FRED | true | true | pass | `2026-05-26-current-fred-macro.json` |  |
| Firecrawl | true | false | failed | `2026-05-26-expanded-shortlist-all-mcp.json`, `2026-05-26-current-firecrawl-ir.json` | expanded shortlist IR scrape failed; actionability blocked |
| Yahoo Finance | true | true | pass | `2026-05-26-expanded-shortlist-all-mcp.json` |  |

## 리스크 게이트

- Order plan: `wiki/trade-ledger/orders/2026-05-26-1620-expanded-universe-recommendation.json`.
- Orders: `[]`.
- Risk check: PASS, warning `orders is empty`.
- Universe coverage: PASS.
- MCP coverage non-strict: PASS with Firecrawl warning.
- MCP coverage strict: FAIL due Firecrawl, therefore this run remains non-actionable.

## 지표 설명

- `5D`, `20D`, `40D`: 최근 5/20/40거래일 종가 수익률이다.
- `20D vs SPY`, `20D vs QQQ`: 같은 기간 종목 수익률에서 benchmark 수익률을 뺀 값이다. 양수면 benchmark보다 강했다는 뜻이다.
- `shortlist`: 넓은 universe 1차 스크리닝 후 MCP 정밀 검증 대상으로 올린 후보군이다.
- `non_actionable_research`: 투자 판단 참고용 분석이며, 주문 후보나 실행 가능한 매수 신호로 승격하지 않았다는 뜻이다.
