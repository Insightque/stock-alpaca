# Alpaca MCP Paper Trading Harness

This workspace is configured to run Alpaca's official MCP server in paper trading mode and to use Codex as a multi-agent trading harness.

The harness keeps all ticker research, trend analysis, allocation notes, order plans, and execution outcomes in an llm-wiki under `wiki/`.

## MCP Setup

1. Open `.env`.
2. Fill `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` with your Alpaca paper trading keys.
3. Restart VS Code or restart the `alpaca` MCP server from the MCP server list.

`ALPACA_PAPER_TRADE=true` is set in `.env` so this setup uses paper trading unless you deliberately change it.

## Codex Commands

Ask Codex one of these commands:

- `Run daily trading workflow`
- `Research AAPL MSFT NVDA only`
- `Rebalance paper portfolio`
- `Post-trade check`
- `Lint trading wiki`

Codex should follow `AGENTS.md` and the matching workflow in `harness/workflows/`.

에이전트에게 업무를 지시하는 예시는 `harness/agent-tasking-guide.md`를 참고하세요.

## Safety Model

- Paper trading only.
- US stocks/ETFs only.
- Long-only, whole-share, day limit orders only.
- Maximum 80% invested, minimum 20% cash reserve, maximum 20% per ticker.
- Maximum 10 new orders per run.
- Orders must pass `scripts/check-risk-policy.py`.
- Orders must be submitted through Alpaca MCP only, never custom REST trading code.

Validate an order plan:

```bash
python3 scripts/check-risk-policy.py harness/examples/order-plan.example.json
```

## Wiki Layout

- `wiki/raw/sources/` immutable captured sources.
- `wiki/tickers/` ticker thesis and trend pages.
- `wiki/portfolio/` account snapshots and order plans.
- `wiki/reports/daily/` daily trading workflow reports.
- `wiki/analyses/` cross-ticker and wiki-lint analyses.
- `wiki/index.md` content index.
- `wiki/log.md` append-only activity log.

## Optional Scheduler

Manual Codex execution is the default. Optional macOS launchd files live in `scheduler/`.
