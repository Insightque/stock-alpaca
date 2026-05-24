# Trading Harness

This directory contains the reusable runbooks, templates, schemas, and examples that let Codex operate the Alpaca paper-trading harness consistently.

Start with these workflows:

- `simple-commands.md` for the user-facing Korean command router.
- `workflows/daily.md` for the full daily research, allocation, risk, and paper-order run.
- `workflows/research.md` for ticker research without orders.
- `workflows/rebalance.md` for portfolio-only allocation and paper-order planning.
- `workflows/intraday-paper-dry-run.md` for order-free real-time v0/v1 intraday signal logging.
- `workflows/post-trade.md` for order/fill reconciliation.
- `workflows/trade-review.md` for reviewing traded stocks and improving recommendation policy.
- `workflows/historical-decision-sim.md` for strict as-of-date recommendation simulations with dry-run orders only.
- `workflows/historical-decision-review.md` for 1D/5D/20D outcome reviews and policy-learning signals.
- `workflows/wiki-lint.md` for wiki maintenance.

Safety lives in two places:

- `AGENTS.md` is the operating contract that Codex should follow.
- `harness/risk-policy.yaml` is the machine-readable source of truth for numeric limits.
- `harness/order-plan.schema.json` defines required order-plan provenance fields.
- `scripts/check-risk-policy.py` validates proposed order-plan JSON before any paper order is submitted through Alpaca MCP.

Provenance and leakage controls:

- `harness/templates/run-manifest.json` and `harness/run-manifest.schema.json` define run manifests for `wiki/evidence-store/run-manifests/`.
- `scripts/check-leakage.py` scans historical simulation artifacts for obvious future-data leakage.
