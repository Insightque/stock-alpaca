---
name: stock-alpaca-simulation-lab
description: Run stock-alpaca historical decision simulations, historical reviews, intraday dry-runs, and policy candidate simulations. Use for YYYY-MM-DD 기준 추천 시뮬레이션, YYYY-MM-DD 추천 회고, leakage control, dry-run order plans, or strategy simulation scripts.
---

# Stock Alpaca Simulation Lab

Use this skill for non-live simulations and policy experiments.

## Boundary

This skill owns dry-run historical and strategy experiments. It never mutates Alpaca state. Use `stock-alpaca-review-policy-learning` for actual paper-trade reviews and promotion of lessons into the living policy book.

## Historical Decisions

1. Treat date-based recommendations as historical simulations, not live trading.
2. Use only information available at or before the as-of point.
3. If only a date is given, use that US regular trading day close unless it was a holiday; then use the closest prior regular trading day and record the adjustment.
4. Create dry-run order plans only.
5. Never submit, replace, cancel, or close orders.
6. Run `scripts/check-leakage.py` when practical.

## Historical Reviews

- Put later-outcome evaluations under `wiki/backtest-runs/results/`.
- Do not edit the original decision under `wiki/backtest-runs/decisions/` with future data.
- Use 1D/5D/20D horizons by default.

## Strategy Simulations

For intraday or long-term policy simulations, read the matching workflow and strategy YAML first. Keep results separate from live/autopilot artifacts and record assumptions in the wiki log.
