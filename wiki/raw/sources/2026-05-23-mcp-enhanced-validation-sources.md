---
id: 2026-05-23-mcp-enhanced-validation-sources
captured_at: 2026-05-23T08:45:00+09:00
source: alpaca-mcp-alpha-vantage-mcp
paper: true
immutable: true
---

# MCP 보강 검증 원천 - 2026-05-11~2026-05-15

## 목적

- 사용자가 `.env`에 보강 MCP 키를 추가한 뒤, 과거 검증셋에 실적/뉴스/매크로 보강 데이터가 정책 수립에 도움이 되는지 확인했다.
- 검증 구간은 이전 out-of-sample 구간과 동일한 2026-05-11~2026-05-15다.
- 이 문서는 원천과 데이터 공백을 기록한다.

## 사용한 MCP

| MCP | 사용 여부 | 결과 |
| --- | --- | --- |
| Alpaca MCP `get_stock_bars` | 사용 | 2026-05-04~2026-05-23 가격/거래량 재조회 |
| Alpha Vantage MCP `EARNINGS` | 사용 | AMD 2026-05-05 실적: EPS 1.37, 추정 1.29, surprise +6.20%, post-market |
| Alpha Vantage MCP `NEWS_SENTIMENT` | 사용 | 2026-05-09~2026-05-16 AMD/NVDA/IONQ/NOK/TSLA 조회 결과 0건 |
| Alpha Vantage MCP `TREASURY_YIELD` | 시도 | 무료 키 rate-limit 안내가 반환되어 이번 검증에서는 미사용 |
| SEC EDGAR MCP | 시도 전 설정 확인 | `SEC_EDGAR_USER_AGENT`가 없어 실행 불가. 설정 공백으로 기록 |
| FRED MCP | 시도 | 현재 래퍼가 유효한 JSON-RPC 응답을 반환하지 않아 미사용 |
| Firecrawl MCP | 미사용 | 이번 검증은 회사 IR 페이지 캡처 없이 Alpha/Alpaca 이벤트만 사용 |

## 보강 데이터 해석

- AMD는 2026-05-05 장마감 후 EPS +6.20% surprise가 확인됐다.
- 2026-05-11 기준 AMD는 실적 발표 이후 이미 크게 오른 상태였으므로, 실적 호재 자체는 긍정이지만 신규 매수에는 과열 감점이 필요했다.
- Alpha Vantage `NEWS_SENTIMENT`가 같은 검증 기간에 0건을 반환했으므로, Alpaca 뉴스와 Alpha 뉴스가 일치하지 않는 경우 보강 데이터 부재를 곧바로 긍정 신호로 해석하면 안 된다.
- 매크로 MCP는 이번 실행에서 유효한 수치를 제공하지 못했으므로, 2026-05-12 CPI/Nasdaq 약세 맥락은 기존 Alpaca 뉴스 원천에 의존했다.

## 데이터 공백

- SEC EDGAR MCP 사용을 위해 `.env`에 `SEC_EDGAR_USER_AGENT`가 추가로 필요하다.
- Alpha Vantage 무료 키는 rate limit이 있으므로 대량 티커/지표 반복 검증에는 캐시 또는 호출 절약이 필요하다.
- FRED MCP 래퍼는 별도 점검이 필요하다.
- Firecrawl은 IR/보도자료 URL 캡처가 필요한 개별 종목 분석에서 우선 사용한다.

## 연결 문서

- 보강 검증 추천: [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-decision]]
- 보강 검증 회고: [[2026-05-11-to-2026-05-15-mcp-enhanced-validation-review]]
- 기존 검증 회고: [[2026-05-11-to-2026-05-15-historical-validation-review]]
