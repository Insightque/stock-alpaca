---
id: 2026-05-22-alpaca-account-clock
source_type: alpaca
captured_at: 2026-05-22T13:39:00Z
source_url: ""
tool: "mcp__alpaca__.get_account_info; mcp__alpaca__.get_clock; mcp__alpaca__.get_all_positions; mcp__alpaca__.get_orders; mcp__alpaca__.get_watchlists"
tickers: []
immutable: true
---

# Alpaca Account, Clock, Positions, Orders, Watchlists

## Summary

- Paper flag in `.env` was confirmed as `ALPACA_PAPER_TRADE=true`.
- Alpaca account status was `ACTIVE`; trading was not blocked.
- Portfolio value was 100000 USD, cash was 100000 USD, buying power was 200000 USD.
- Long market value and short market value were both 0.
- Current positions, open US equity orders, and watchlists were empty.
- Alpaca market clock showed US equities open at `2026-05-22T09:36:27-04:00`; next close was `2026-05-22T16:00:00-04:00`.

## Key Evidence

- `portfolio_value`: 100000
- `cash`: 100000
- `buying_power`: 200000
- `long_market_value`: 0
- `short_market_value`: 0
- `positions`: []
- `open_orders`: []
- `watchlists`: []

## Tickers Mentioned

- None.

## Notes For Wiki Integration

- This is a fresh/no-position paper portfolio state.
- Because no user command included order execution language, the run remains no-submit.
