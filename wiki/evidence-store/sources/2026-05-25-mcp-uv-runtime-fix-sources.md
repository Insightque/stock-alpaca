---
id: 2026-05-25-mcp-uv-runtime-fix-sources
created_at: 2026-05-25T18:34:00+09:00
source_type: mcp-runtime-fix-source
paper: true
orders_submitted: 0
---

# MCP `uvx` runtime 경로 조치 원천

## 이슈 설명

6개월 live MCP smoke run 실패는 두 층으로 나뉜다.

1. `uvx` runtime 경로 권한 문제.
   - 기존 `scripts/alpaca-mcp.sh`는 `uvx alpaca-mcp-server`를 바로 실행했다.
   - `uvx`는 기본적으로 `~/.cache/uv`와 `~/.local/share/uv/tools` 아래에 package cache와 tool environment를 만든다.
   - 현재 Codex sandbox는 레포와 일부 temp 경로만 쓰기 가능하므로 홈 디렉터리의 uv cache/tool 경로 접근이 거부됐다.

2. 첫 실행 dependency fetch 문제.
   - runtime 경로를 레포 내부로 옮긴 뒤에는 권한 에러가 사라졌다.
   - 하지만 현재 레포-local cache에 `alpaca-mcp-server`가 없어 `uvx`가 PyPI 조회를 시도했고, sandbox DNS 제한 때문에 실패했다.
   - unsandboxed 재시도는 정책상 승인되지 않았다.

따라서 코드상 문제였던 부분은 `uvx`가 sandbox 밖의 홈 캐시/도구 경로를 쓰던 점이다. 남은 제약은 새 MCP package를 처음 받아오는 네트워크 권한 문제다.

## 조치 내용

| 파일 | 조치 |
| --- | --- |
| `.gitignore` | 레포-local `.cache/`를 추적하지 않도록 추가. |
| `scripts/alpaca-mcp.sh` | `XDG_CACHE_HOME`, `XDG_DATA_HOME`, `UV_CACHE_DIR`, `UV_TOOL_DIR`를 레포 내부 `.cache`로 지정. `UV_LINK_MODE=copy`, `UV_PYTHON_DOWNLOADS=never` 기본값 추가. 로컬 설치된 `alpaca-mcp-server`가 있으면 `uvx` 없이 우선 실행. |
| `scripts/mcp-alpha-vantage.sh` | 같은 uv runtime 경로 고정과 `marketdata-mcp` 로컬 설치 fallback 추가. |
| `scripts/mcp-sec-edgar.sh` | 같은 uv runtime 경로 고정과 `sec-edgar-mcp` 로컬 설치 fallback 추가. |
| `scripts/mcp-yahoo-finance.sh` | 같은 uv runtime 경로 고정과 `yahoo-finance-mcp` 로컬 설치 fallback 추가. |
| `tests/test_mcp_runtime_wrappers.py` | uvx wrapper가 workspace-local runtime dirs와 installed-command fallback을 유지하는지 회귀 테스트 추가. |

## 재검증

성공:

- `bash -n scripts/alpaca-mcp.sh scripts/mcp-alpha-vantage.sh scripts/mcp-sec-edgar.sh scripts/mcp-yahoo-finance.sh scripts/mcp-fred.sh scripts/mcp-firecrawl.sh`
- `python3 -m unittest tests.test_mcp_runtime_wrappers`: 3개 통과.
- `python3 -m unittest discover -s tests`: 48개 통과.

제한 범위 6개월 smoke 재시도:

```bash
python3 scripts/simulate-six-month-3h-policy-review.py \
  --start 2026-05-01 \
  --end 2026-05-08 \
  --symbols AMD,MU,NOK,SPY,QQQ,SMH \
  --event-features-json wiki/evidence-store/sources/2026-05-25-mcp-verification-neutral-event-feature-cache.json \
  --output-json /private/tmp/verify-six-month-smoke-fixed.json \
  --output-md /private/tmp/verify-six-month-smoke-fixed.md \
  --source-md /private/tmp/verify-six-month-smoke-fixed-source.md \
  --run-manifest /private/tmp/verify-six-month-smoke-fixed-manifest.json
```

결과:

- 더 이상 `~/.cache/uv` 또는 `~/.local/share/uv/tools` 권한 에러는 발생하지 않았다.
- 새 실패 원인은 `https://pypi.org/simple/alpaca-mcp-server/` DNS 조회 실패였다.
- 로컬 Python 환경과 PATH에 `alpaca-mcp-server`는 설치되어 있지 않았다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## 운영상 남은 조건

이제 sandbox 안에서 wrapper 경로 문제는 해결됐다. 단, 레포-local cache가 비어 있는 새 환경에서는 `uvx`가 MCP package를 최초 1회 다운로드해야 한다. 네트워크가 허용된 환경에서 한 번 cache를 priming하거나, `alpaca-mcp-server` 실행 파일을 로컬 환경에 설치해두면 wrapper는 그 뒤 sandbox 경로 문제 없이 실행된다.
