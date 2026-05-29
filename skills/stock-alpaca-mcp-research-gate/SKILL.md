---
name: stock-alpaca-mcp-research-gate
description: Manage stock-alpaca MCP preflight, research coverage, provider gaps, cache/backoff, and strict coverage validation. Use for Alpha Vantage, FRED, Firecrawl, SEC EDGAR, Yahoo Finance, Alpaca core, mcp_coverage, gap_category, retry_count, or provider-gap alert work.
---

# Stock Alpaca MCP Research Gate

Use this skill when current-market recommendations, autopilot, or alerts depend on MCP coverage.

## Boundary

This skill owns coverage policy, gap classification, and validator expectations. Use `stock-alpaca-local-mcp-runtime` for wrapper/server mechanics and `stock-alpaca-secret-hygiene` for sanitizing provider payloads or caches.

## Sources

1. Read `harness/mcp-source-map.md`.
2. Read `harness/recommendation-policy.yaml` for gate policy.
3. Use Alpaca MCP first for account/order/position/watchlist/market data.
4. Use research MCPs for SEC, Alpha Vantage, FRED, Firecrawl, Yahoo Finance context when configured.

## Coverage Contract

- Every meaningful recommendation run must record `mcp_coverage`.
- Scheduled runs must classify failures with `gap_category` and `retry_count`.
- Alpaca core failures must identify the first failed hard gate.
- Actionable recommendations and submit-mode runs must pass:

```bash
python3 scripts/check-mcp-coverage.py --strict <run-manifest>
```

## Provider Gaps

- Use the defined categories: `timeout`, `cancelled`, `dns`, `auth`, `empty_response`, `provider_error`, `wrapper_error`, `not_applicable`, `unknown`.
- Do not fabricate missing provider context.
- Record provider gaps in raw source notes and continue only when the policy allows it.
- Keep provider cache/backoff scoped safely and avoid leaking keys.

## Alpha/FRED Notes

- Alpha Vantage scheduler preflight should make at most one actual provider call per hour.
- Alpha rate-limit payloads are provider errors, not empty responses.
- FRED timeouts should be reported as provider gaps and should not stall nested shutdown.
