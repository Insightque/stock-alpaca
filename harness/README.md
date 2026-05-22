# Trading Harness

This directory contains the reusable runbooks, templates, schemas, and examples that let Codex operate the Alpaca paper-trading harness consistently.

Start with these workflows:

- `workflows/daily.md` for the full daily research, allocation, risk, and paper-order run.
- `workflows/research.md` for ticker research without orders.
- `workflows/rebalance.md` for portfolio-only allocation and paper-order planning.
- `workflows/post-trade.md` for order/fill reconciliation.
- `workflows/wiki-lint.md` for wiki maintenance.

Safety lives in two places:

- `AGENTS.md` is the operating contract that Codex should follow.
- `scripts/check-risk-policy.py` validates proposed order-plan JSON before any paper order is submitted through Alpaca MCP.

