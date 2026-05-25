---
id: 2026-05-25-mcp-simulation-integration-fix-sources
created_at: 2026-05-25T18:16:00+09:00
source_type: mcp-simulation-integration-fix-source
paper: true
orders_submitted: 0
---

# MCP-only 시뮬레이션 경로와 event feature 결합 조치 원천

## 목적

사용자 요청에 따라 이전 감사에서 확인된 두 공백을 조치했다.

- `scripts/simulate-intraday-policy-candidates.py`, `scripts/simulate-short-long-policy-review.py`의 Alpaca market data REST 직접 `curl` 경로 제거.
- 1년/6개월 가격 기반 시뮬레이션에 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 등 research MCP 산출물을 event-level feature cache로 결합할 수 있는 경로 추가.

## 안전 확인

- `ALPACA_PAPER_TRADE=true` 조건을 유지했다.
- 실제 주문, 취소, 교체, 포지션 청산 도구는 호출하지 않았다.
- 새 검증 실행은 기존 Alpaca MCP 캡처 파일과 테스트 fixture를 사용했다.
- `orders_submitted=0`.

## 코드 변경 요약

| 파일 | 변경 |
| --- | --- |
| `scripts/alpaca_mcp_bars.py` | Alpaca `get_stock_bars`를 stdio MCP로 호출하는 공용 read-only helper 추가. |
| `scripts/simulate-intraday-policy-candidates.py` | `curl`/`APCA-API-*`/`data.alpaca.markets` 직접 호출 제거, `fetch_stock_bars_mcp` 사용. |
| `scripts/simulate-short-long-policy-review.py` | intraday bar 수집을 Alpaca MCP helper로 이전. |
| `scripts/simulate-one-year-daily-policy.py` | `--event-features-json` 추가. `available_at`/`asof_date` 기준 point-in-time feature join, `score_adjustment`, `source_confidence_delta`, `exclude`, `mcp_gaps`, `source_refs` 반영. |
| `scripts/simulate-long-term-policy.py` | wrapper에서도 `--event-features-json`을 전달하도록 확장. |
| `scripts/simulate-six-month-3h-policy-review.py` | `--event-features-json` 추가. 단타/장타 row에 event feature를 결합하고, daily score와 intraday ranking에 `event_score_adjustment`를 반영. |
| `harness/templates/event-feature-cache.json` | research MCP feature cache 형식 추가. |
| `harness/workflows/one-year-daily-simulation.md` | event feature cache 작성과 시뮬레이터 전달 단계를 workflow에 추가. |
| `tests/test_mcp_only_market_data.py` | 두 intraday 시뮬레이터에 Alpaca REST 직접 호출이 남지 않았는지 회귀 테스트. |
| `tests/test_one_year_event_features.py` | point-in-time event feature join과 `exclude` gate 테스트. |
| `tests/fixtures/event-feature-cache.sample.json` | 5개 research MCP 서버가 포함된 샘플 cache. |

## 확인 결과

직접 REST 경로 확인:

- `scripts/simulate-intraday-policy-candidates.py`
- `scripts/simulate-short-long-policy-review.py`

위 두 파일에서 아래 문자열이 사라졌음을 확인했다.

- `APCA-API-KEY-ID`
- `APCA-API-SECRET-KEY`
- `data.alpaca.markets`
- `urllib.parse`

1년 시뮬레이션 event feature smoke:

```bash
python3 scripts/simulate-one-year-daily-policy.py \
  --input-json wiki/evidence-store/sources/2026-05-25-one-year-daily-bars.json \
  --strategy-config harness/strategies/long-term-quality-momentum-v1.yaml \
  --metadata-yaml harness/symbol-metadata.yaml \
  --event-features-json tests/fixtures/event-feature-cache.sample.json \
  --output-json /private/tmp/event-sim.json \
  --output-md /private/tmp/event-sim.md \
  --scorecard-json /private/tmp/event-scorecard.json
```

결과:

- `event_feature_cache_used=true`
- `event_feature_matches=1`
- `mcp_event_servers_used=alpha-vantage,firecrawl,fred,sec-edgar,yahoo-finance`
- `orders_submitted=0`
- `recommendations=953`
- `completed=853`

## 검증 명령

- `python3 -m py_compile scripts/alpaca_mcp_bars.py scripts/simulate-intraday-policy-candidates.py scripts/simulate-short-long-policy-review.py scripts/simulate-one-year-daily-policy.py scripts/simulate-long-term-policy.py scripts/simulate-six-month-3h-policy-review.py`: PASS.
- `python3 -m unittest discover -s tests`: 45개 통과.

## 남은 운영 과제

- 실제 대규모 1년/6개월 재시뮬레이션에서 의미 있는 event feature coverage를 얻으려면 as-of cache를 날짜/종목별로 채워야 한다.
- FRED 공식 API health check는 앞선 감사에서 현재 sandbox 정책 때문에 이번 세션에서 재확인하지 못했다. 로컬 MCP wrapper와 도구 노출은 정상이다.
