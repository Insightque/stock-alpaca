# Backtests

This directory stores policy tests, parameter checks, event studies, and historical performance reviews that intentionally include later outcome data.

Use this directory for:

- intraday policy simulations and validations
- long-term policy train/validation reviews
- event studies such as news-to-price lead/lag checks
- multi-month policy backtests with hit rate, P/L, drawdown, or benchmark excess return

Do not use this directory for point-in-time recommendation documents that must exclude future information. Those belong in `wiki/simulations/`.

Keep raw inputs and large calculation outputs in `wiki/raw/sources/`, and keep machine-readable run provenance in `wiki/runs/`.
