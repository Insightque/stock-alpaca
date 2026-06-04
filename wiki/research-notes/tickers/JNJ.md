---
id: JNJ
updated_at: 2026-06-04T19:58:13Z
symbol: JNJ
asset_type: stock
---

# JNJ

## 현재 Thesis

JNJ는 healthcare/pharma 성격의 대형 방어주로, 이번 regular-session validation에서는 AI/반도체와 성장주 편중 포트폴리오에 대한 분산 후보로 본다. 2026-06-04 15:56 ET runtime Alpaca quote는 `228.32/229.25`였고 spread는 약 `0.41%`로 정책 한도 이내다. scheduler-owned research preflight에서는 Yahoo Finance analyst summary가 `strongBuy 5 / buy 10 / hold 8 / strongSell 1`로 집계됐고, 관련 Yahoo 뉴스도 확인됐다.

## 추세

- 일간: 방어주 성격의 완만한 흐름으로 본다.
- 주간: 공격적 성장주 대비 저변동 분산 후보로 적합하다.
- 월간: 포트폴리오 defensive healthcare 슬롯 보강 후보다.

## 촉매

- AI/반도체 집중 포지션 대비 sector diversification.
- Yahoo Finance analyst summary 기준 중립 이상 수급 기대 유지.

## 리스크

- 개별 초과수익 기대치는 제한적일 수 있다.
- healthcare 대형주라 floor-size validation 이상 공격적 확대 근거는 아직 약하다.
- scheduler research preflight의 SEC lightweight row는 pass로 기록됐지만 payload 요약은 제한적이라 filing-positive thesis로 과장하지 않는다.

## 포트폴리오 맥락

- 현재 노출: 0%.
- 제안 역할: defensive healthcare diversifier.
- 현재 조치: regular-session floor-size validation buy 후보.

## 점수

- 점수: 62/100
- 신뢰도: 중간

## 출처

- `wiki/evidence-store/sources/2026-06-05-0451-hourly-autopilot-research-mcp-preflight.json`
- `wiki/evidence-store/sources/2026-06-05-0451-hourly-autopilot-alpaca-core-preflight.json`
- `harness/symbol-metadata.yaml`

## 2026-06-05 05:05 KST hourly autopilot

2026-06-05 04:51 KST hourly autopilot에서 JNJ 1주 regular-session day limit validation buy를 계획하고 `place_stock_order`까지 호출했지만, 실제 Alpaca submit timestamp가 `2026-06-04T20:02:59Z` (`16:02:59 ET`)로 regular close 이후에 기록됐다. runtime clock 재확인에서 `is_open=false`가 확인되어 해당 주문은 즉시 취소됐고, 신규 fill이나 포지션 증가는 남기지 않았다.

출처: [[2026-06-05-0451-hourly-autopilot]], `wiki/trade-ledger/orders/2026-06-05-0451-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-06-05-0451-hourly-autopilot-post-trade.json`
