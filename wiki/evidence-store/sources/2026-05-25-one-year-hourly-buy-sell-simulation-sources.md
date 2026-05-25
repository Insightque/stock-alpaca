---
id: 2026-05-25-one-year-hourly-buy-sell-simulation-sources
created_at: 2026-05-25T21:40:49+09:00
source_type: alpaca-mcp-hourly-backtest-source
paper: true
orders_submitted: 0
---

# 과거 1년 1시간봉 매입/매도 시뮬레이션 원천

## 조회 원천

- Alpaca MCP: `get_stock_bars`
- 캡처 스크립트: `scripts/fetch-alpaca-hourly-bars-mcp.py`
- 기간: 2025-05-23T00:00:00Z ~ 2026-05-22T23:59:59Z
- time frame: `1Hour`
- feed: `alpaca_iex`
- adjustment: `all`
- raw JSON: `wiki/evidence-store/sources/2026-05-25-one-year-hourly-bars.json`
- simulation JSON: `wiki/evidence-store/sources/2026-05-25-one-year-hourly-buy-sell-simulation-data.json`
- scorecard JSON: `wiki/evidence-store/sources/2026-05-25-one-year-hourly-buy-sell-scorecard.json`

## 데이터 품질

- symbols_requested: 62
- symbols_loaded: 62
- hourly bars loaded: 114060
- missing_symbols: []
- stale_quotes: 0
- corporate_actions_checked: true
- survivorship_bias_controlled: false
- dataset_hash: `sha256:20f49fc662e0153d8aaa357961b94a37867cddf60e76dd4cacff9eb9c079c7c1`

## 데이터 공백

- 1시간봉에는 quote-level bid/ask, queue priority, limit-fill probability가 없다.
- IEX feed는 SIP 통합 체결/거래량과 다를 수 있다.
- 현재 중앙 universe 기준이므로 survivorship bias 통제가 완전하지 않다.
- event feature cache가 없으면 SEC/실적/애널리스트/밸류에이션/매크로 맥락은 점수에 직접 반영되지 않는다.
