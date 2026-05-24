---
id: 2026-05-25-one-year-daily-simulation-sources
created_at: 2026-05-25T02:25:00+09:00
source_type: alpaca-mcp-backtest-source
paper: true
orders_submitted: 0
---

# 2026-05-25 과거 1년 일별 독립 시뮬레이션 원천

## 조회 원천

- Alpaca MCP: `get_stock_bars`
- 캡처 스크립트: `scripts/fetch-alpaca-bars-mcp.py`
- 기간: 2025-05-23T00:00:00Z ~ 2026-05-22T23:59:59Z
- time frame: `1Day`
- feed: `iex`
- adjustment: `all`
- universe: `harness/symbol-metadata.yaml`의 62개 심볼
- raw JSON: `wiki/raw/sources/2026-05-25-one-year-daily-bars.json`
- simulation JSON: `wiki/raw/sources/2026-05-25-one-year-daily-policy-simulation-data.json`
- scorecard JSON: `wiki/raw/sources/2026-05-25-one-year-policy-scorecard.json`

## 데이터 품질

- symbols_requested: 62
- symbols_loaded: 62
- 각 심볼 loaded bars: 251
- missing_symbol_dates: 0
- stale_quotes: 0
- corporate_actions_checked: true, adjusted bars 사용
- survivorship_bias_controlled: false. 현재 중앙 universe를 기준으로 조회했으므로, 완전한 과거 시점 구성 종목 survivorship control은 아니다.
- dataset_hash: `sha256:dd4652f26a5fee046692bf29e5b28f0dd91bedf738d0ff0dac36d252196db5ce`

## 데이터 공백

- 일봉에는 quote-level bid/ask, queue priority, limit-fill probability가 없다.
- source confidence는 이벤트별 raw source join이 아니라 `harness/symbol-metadata.yaml`의 bucket을 사용했다.
- 실적, SEC filing, analyst, valuation, macro feature는 정책상 필수 확인 대상이지만 이번 수치 시뮬레이션에는 별도 feature로 결합하지 않았다.
- 따라서 결과가 장기 dry-run 후보를 보강하더라도 `auto_eligible_paper` 승격 근거로 단독 사용하지 않는다.
