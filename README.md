# Alpaca MCP Paper Trading Harness

This workspace is configured to run Alpaca's official MCP server in paper trading mode and to use Codex as a multi-agent trading harness.

The harness keeps all ticker research, trend analysis, allocation notes, order plans, and execution outcomes in an llm-wiki under `wiki/`.

## MCP Setup

1. Open `.env`.
2. Fill `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` with your Alpaca paper trading keys.
3. Restart VS Code or restart the `alpaca` MCP server from the MCP server list.

`ALPACA_PAPER_TRADE=true` is set in `.env` so this setup uses paper trading unless you deliberately change it.

## 간단한 Codex 명령

Codex에게 아래처럼 짧게 말하면 됩니다:

- `오늘 분석해줘`
- `관심종목 분석해줘`
- `AAPL 분석해줘`
- `포트폴리오 점검해줘`
- `리밸런싱 계획 짜줘`
- `paper 주문까지 실행해줘`
- `거래 후 점검해줘`
- `위키 정리해줘`

Codex는 `AGENTS.md`를 따르고, `harness/simple-commands.md`에서 명령을 해석한 뒤, `harness/workflows/`의 맞는 워크플로우를 실행합니다.

에이전트에게 업무를 지시하는 예시는 `harness/agent-tasking-guide.md`를 참고하세요.

## 안전 모델

- Paper trading only.
- US stocks/ETFs only.
- Long-only, whole-share, day limit orders only.
- Maximum 80% invested, minimum 20% cash reserve, maximum 20% per ticker.
- Maximum 10 new orders per run.
- Orders must pass `scripts/check-risk-policy.py`.
- Orders must be submitted through Alpaca MCP only, never custom REST trading code.

주문 계획 검증:

```bash
python3 scripts/check-risk-policy.py harness/examples/order-plan.example.json
```

## Wiki 구조

- `wiki/raw/sources/` immutable captured sources.
- `wiki/tickers/` ticker thesis and trend pages.
- `wiki/portfolio/` account snapshots and order plans.
- `wiki/reports/daily/` daily trading workflow reports.
- `wiki/analyses/` cross-ticker and wiki-lint analyses.
- `wiki/index.md` content index.
- `wiki/log.md` append-only activity log.

## 선택형 스케줄러

기본은 Codex 수동 실행입니다. 선택형 macOS launchd 파일은 `scheduler/`에 있습니다.
