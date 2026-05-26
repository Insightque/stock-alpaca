# MCP 원천 소스 맵

이 문서는 주식 분석 에이전트가 Alpaca MCP 외에 어떤 MCP를 어떤 목적으로 써야 하는지 정리한다. 모든 MCP 결과는 raw source note에 출처, 조회 시각, 기준 시점, 데이터 공백을 남긴다.

## 등록된 MCP 서버

`.vscode/mcp.json`에는 아래 래퍼들이 모두 등록되어 있다. Alpaca는 필수이고, 보강 MCP는 필요한 환경 변수가 없으면 실패를 데이터 공백으로 기록한 뒤 가능한 원천으로 계속 진행한다.

| MCP | 실행 래퍼 | 주요 목적 | 필요 환경 변수 | 사용 상태 |
| --- | --- | --- | --- | --- |
| `alpaca` | `scripts/alpaca-mcp.sh` | 계좌, 주문, 포지션, watchlist, 가격, 뉴스, corporate action, calendar | Alpaca paper 키 | 기본 사용 |
| `sec-edgar` | `scripts/mcp-sec-edgar.sh` | SEC filings, XBRL 재무제표, insider 거래, 10-K/10-Q/8-K | `SEC_EDGAR_USER_AGENT` | 보강 사용 |
| `yahoo-finance` | `scripts/mcp-yahoo-finance.sh` | Yahoo Finance 뉴스, 재무정보, analyst recommendation, holder/insider 보조 정보 | 없음 | 보강 사용 |
| `alpha-vantage` | `scripts/mcp-alpha-vantage.sh` | 실적 캘린더, earnings, 기술지표, fundamental data | `ALPHA_VANTAGE_API_KEY` | 키 필요 |
| `fred` | `scripts/mcp-fred.sh` -> `scripts/fred-mcp-server.py` | FRED 매크로 지표, 경제 release, 금리, CPI, 실업률 | `FRED_API_KEY` | 로컬 MCP 사용 |
| `firecrawl` | `scripts/mcp-firecrawl.sh` -> `scripts/firecrawl-mcp-server.py` | 회사 IR, 보도자료, earnings presentation, SEC/IR 웹페이지 캡처 | `FIRECRAWL_API_KEY` | 로컬 MCP 사용 |

## 에이전트별 사용 규칙

- Market Data Agent는 Alpaca MCP를 기본 가격/뉴스 원천으로 사용한다.
- Daily/current recommendation에서 빠른 판단을 위해 보강 MCP를 생략하지 않는다. 최종 후보 순위와 주문 후보를 만들기 전에 Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance coverage를 모두 기록한다.
- Web Research Agent는 아래 순서로 이벤트 보강을 수행한다.
  1. Alpaca `get_news`, `get_corporate_action_announcements`, `get_calendar`.
  2. `sec-edgar`로 최근 10-K, 10-Q, 8-K, Form 4, 주요 재무제표 확인.
  3. `alpha-vantage`로 실적 캘린더와 earnings surprise 확인. 키가 없으면 공백으로 기록.
  4. `yahoo-finance`로 Yahoo 뉴스, analyst recommendation, holder/insider 보조 정보 확인.
  5. `fred`로 CPI, 금리, 실업률, 장단기 금리차, 금융환경 등 매크로 지표 확인. 키가 없으면 공백으로 기록.
  6. `firecrawl`로 회사 IR/보도자료/earnings presentation 웹페이지를 캡처. 키가 없으면 웹 브라우징 또는 수동 raw URL로 대체.
- Historical Decision Agent는 기준 시점 이후 정보가 섞이지 않게 각 MCP 조회 기간을 기준 시점 이전으로 제한한다.
- Historical Review Agent는 미래 가격과 이벤트를 회고 문서에서만 사용한다. 원래 추천 문서는 수정하지 않는다.
- Portfolio/Risk Agent와 Executor Agent는 외부 리서치 MCP를 주문 제출 근거 보강에만 사용하고, 실제 주문은 Alpaca MCP와 risk gate만 통과한 뒤 수행한다.
- `wiki/evidence-store/run-manifests/`의 각 recommendation manifest는 `mcp_coverage`를 포함해야 한다. Actionable dry-run 또는 submit-mode에서는 `scripts/check-mcp-coverage.py --strict <manifest>`가 PASS하기 전까지 주문 후보를 만들거나 제출하지 않는다.
- MCP가 실패하거나 0건을 반환하면 긍정 근거로 사용하지 않는다. `gap_reason`을 남기고 관련 ticker의 source confidence를 낮추거나 recommendation을 `non_actionable_research`로 유지한다.

## 키 관리

- API 키와 provider 설정은 `.env`에만 둔다.
- 키 이름은 `ALPHA_VANTAGE_API_KEY`, `FRED_API_KEY`, `FIRECRAWL_API_KEY`를 사용한다.
- SEC EDGAR는 API 키 대신 `SEC_EDGAR_USER_AGENT`가 필요하다. 예: `stock-alpaca/0.1 contact@example.com`.
- 키 값을 로그, raw source, 커밋, 터미널 출력에 남기지 않는다.
- 키가 없으면 해당 MCP를 건너뛰고 `데이터 공백`에 명시한다.
- `ALPACA_PAPER_TRADE`가 없거나 `true`가 아니면 `scripts/alpaca-mcp.sh`는 실행을 중단한다.
- FRED는 외부 npm 패키지를 즉석 실행하지 않고 레포 내부 `scripts/fred-mcp-server.py`를 통해 공식 FRED API만 호출한다. API 키는 curl stdin config로 전달해 process list와 일반 로그에 남기지 않는다.
- Firecrawl도 외부 npm 패키지를 즉석 실행하지 않고 레포 내부 `scripts/firecrawl-mcp-server.py`를 통해 공식 Firecrawl API만 호출한다. API 키는 curl stdin config로 전달해 process list와 일반 로그에 남기지 않는다.
- `uvx` 기반 wrapper인 Alpaca, SEC EDGAR, Alpha Vantage, Yahoo Finance는 sandbox 홈 디렉터리 접근을 피하기 위해 `UV_CACHE_DIR`, `UV_TOOL_DIR`, `XDG_CACHE_HOME`, `XDG_DATA_HOME`을 레포 내부 `.cache/`로 지정한다. `.cache/`는 git에 추적하지 않는다.
- `uvx` package가 레포-local cache에 없고 실행 파일도 PATH에 없으면 최초 1회 PyPI/GitHub fetch가 필요하다. 네트워크가 제한된 실행 환경에서는 이를 MCP runtime 데이터 공백으로 기록한다.

## raw source 기록 형식

뉴스/이벤트 보강 원천은 가능한 한 아래 항목을 포함한다.

- 조회 MCP와 도구 이름.
- 조회 시각과 기준 시점.
- 티커와 기간.
- 원문 URL 또는 filing accession/source identifier.
- 에이전트 판단에 사용한 요약.
- 데이터 공백과 실패한 MCP 호출.

## Manifest coverage gate

각 recommendation run은 아래 MCP별 coverage row를 남긴다.

- `server`: `alpaca`, `sec-edgar`, `alpha-vantage`, `fred`, `firecrawl`, `yahoo-finance`.
- `queried`: 실제 호출 여부.
- `used_in_score`: 점수, confidence, risk, allocation 판단에 반영했는지.
- `outcome`: `pass`, `usable`, `ok`, `gap`, `failed`, `unavailable`, `not_applicable`.
- `source_refs`: raw source note 또는 캡처 파일.
- `gap_reason`: 호출 실패, provider 0건, key/runtime 공백, 기준시점 누수 위험 등.

Actionable 추천은 모든 required MCP가 `queried=true`, `outcome=pass|usable|ok`, source ref 1개 이상이어야 한다. Submit mode에서는 모든 required MCP가 `used_in_score=true`여야 한다.

## 우선순위

1. Alpaca MCP: 계좌, 주문, 가격, watchlist, 뉴스의 기본 원천.
2. SEC EDGAR MCP: filings와 insider/form 이벤트의 사실 확인.
3. Alpha Vantage MCP: 실적 캘린더와 earnings 정보.
4. FRED MCP: 매크로 regime 확인.
5. Firecrawl MCP: IR/보도자료 원문 캡처.
6. Yahoo Finance MCP: analyst/news 보조 확인.
