---
id: 2026-05-25-mcp-connection-simulation-audit-sources
created_at: 2026-05-25T17:58:00+09:00
source_type: mcp-connection-simulation-audit-source
paper: true
orders_submitted: 0
---

# MCP 연결 재점검과 시뮬레이션 스모크 원천

## 안전 확인

- `.env`에서 필요한 변수 이름의 존재만 확인했다. 키 값은 출력하지 않았다.
- 확인된 변수: `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `ALPACA_PAPER_TRADE`, `SEC_EDGAR_USER_AGENT`, `ALPHA_VANTAGE_API_KEY`, `FRED_API_KEY`, `FIRECRAWL_API_KEY`.
- `ALPACA_PAPER_TRADE=true` 확인.
- 실제 주문, 취소, 교체, 포지션 청산 도구는 호출하지 않았다.

## 현재 Codex 세션 MCP 확인

| MCP | 확인 도구 | 결과 |
| --- | --- | --- |
| Alpaca | `get_calendar`, `get_account_info`, `get_all_positions`, `get_watchlists`, `get_stock_bars`, `get_news` | 정상. 2026-05-22와 2026-05-26 정규장 캘린더 확인, account 상태 ACTIVE, 보유 long position 10개, watchlist 0개, SPY/QQQ 2026-05-20~2026-05-22 IEX adjusted 일봉 각각 3개, AMD 뉴스 3건 확인. |
| Alpha Vantage | `TOOL_LIST`, `TOOL_GET(PING)`, `TOOL_CALL(PING)`, `TOOL_GET(EARNINGS_CALENDAR)`, `TOOL_CALL(EARNINGS_CALENDAR)` | 정상. `PING`은 `pong`. AMD earnings calendar는 2026-08-04, fiscal date 2026-06-30, estimate 1.61 USD 행을 반환. |
| SEC EDGAR | `get_company_info`, `get_recent_filings` | 정상. AMD company info는 CIK 2488, 최근 30일 filing 3건 반환. 최신 행은 2026-05-22 Form 4. |
| Yahoo Finance | `get_stock_info`, `get_recommendations` | 정상. AMD stock info와 analyst recommendation summary 반환. 현재 period recommendation은 strongBuy 5, buy 36, hold 10, sell 0, strongSell 0. |
| FRED | 로컬 wrapper `scripts/mcp-fred.sh` `initialize`, `tools/list` | 부분 확인. 로컬 MCP 서버는 `stock-alpaca-fred`로 시작했고 `get_series_observations`, `get_series_info`, `search_series`, `get_macro_snapshot`을 노출했다. 공식 FRED API health check는 sandbox DNS 제한으로 실패했고, credential network escalation은 자동 승인 정책에서 거부됐다. |
| Firecrawl | 로컬 wrapper `scripts/mcp-firecrawl.sh` `initialize`, `tools/list`, `--health-check` | 정상. 로컬 MCP 서버는 `stock-alpaca-firecrawl`로 시작했고 `firecrawl_scrape`, `firecrawl_map`을 노출했다. 공식 API health check는 `firecrawl_api: ok`, `markdown_chars: 167`. |

## 시뮬레이션 스모크

기존 Alpaca MCP 캡처 파일을 입력으로 장기 일별 독립 정책 시뮬레이션을 `/private/tmp`에 재실행했다.

```bash
python3 scripts/simulate-one-year-daily-policy.py \
  --input-json wiki/evidence-store/sources/2026-05-25-one-year-daily-bars.json \
  --strategy-config harness/strategies/long-term-quality-momentum-v1.yaml \
  --metadata-yaml harness/symbol-metadata.yaml \
  --output-json /private/tmp/mcp-smoke-one-year-sim.json \
  --output-md /private/tmp/mcp-smoke-one-year-sim.md \
  --scorecard-json /private/tmp/mcp-smoke-scorecard.json
```

결과:

- `orders_submitted=0`
- `source_feed=alpaca_iex`, `bar_interval=1Day`
- `daily_independent_runs=191`
- `recommendations=953`
- `completed=853`
- `hit_rate_after_cost_pct=58.73388`
- `avg_excess_after_cost_pct=3.749958`
- `policy_status=active_dry_run_candidate`

`wiki/evidence-store/run-manifests/2026-05-25-one-year-daily-policy-simulation.json`도 `mcp_servers_used=["alpaca"]`, `symbols_loaded=62`, `mcp_failures=[]`로 확인됐다.

## 실행 제한과 데이터 공백

- `scripts/fetch-alpaca-bars-mcp.py`를 새로 실행해 `/private/tmp/mcp-smoke-bars.json`을 만들려 했으나, sandbox가 `/Users/insightque/.cache/uv/sdists-v9/.git` 접근을 막아 실패했다. 같은 명령의 escalated rerun도 credential network 사용 때문에 자동 승인 정책에서 거부됐다.
- 따라서 이번 세션에서 “새 파일 생성까지 포함한 로컬 Alpaca helper end-to-end”는 확인하지 못했다. 대신 현재 Codex 세션의 Alpaca MCP `get_stock_bars` 직접 호출은 정상 응답했다.
- FRED는 로컬 wrapper와 도구 노출까지 확인했지만, 공식 FRED API까지 이어지는 런타임 호출은 이번 세션에서 확인하지 못했다.
- 가격 기반 대규모 시뮬레이션은 의도적으로 Alpaca 일봉만 사용한다. SEC, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 결과는 아직 일별 event/fundamental/macro feature로 결합되어 있지 않다.
- `scripts/simulate-intraday-policy-candidates.py`와 `scripts/simulate-short-long-policy-review.py`에는 Alpaca market data REST를 직접 `curl`로 읽는 경로가 남아 있다. 현재 하네스 원칙인 “시장 데이터도 Alpaca MCP 사용”과 맞지 않아 MCP helper 경유로 이전해야 한다.

## 검증 명령

- `python3 -m unittest tests.test_fred_mcp_server tests.test_firecrawl_mcp_server`: 8개 통과.
- `python3 -m unittest discover -s tests`: 41개 통과.
