---
name: stock-alpaca-local-mcp-runtime
description: Debug and maintain stock-alpaca local MCP wrappers and provider runtimes. Use for scripts/mcp-*.sh, fred/firecrawl local servers, uvx/cache issues, wrapper timeouts, provider subprocess failures, or sandbox/network-related MCP runtime diagnosis.
---

# Stock Alpaca Local MCP Runtime

Use this skill when MCP wrappers or local provider servers are failing.

## Boundary

This skill owns local wrapper/server mechanics and subprocess/runtime diagnosis. Use `stock-alpaca-mcp-research-gate` to decide how a provider failure affects recommendation coverage.

## Scope

Relevant files include:

- `scripts/alpaca-mcp.sh`
- `scripts/mcp-alpha-vantage.sh`
- `scripts/mcp-fred.sh`
- `scripts/mcp-firecrawl.sh`
- `scripts/mcp-sec-edgar.sh`
- `scripts/mcp-yahoo-finance.sh`
- `scripts/fred-mcp-server.py`
- `scripts/firecrawl-mcp-server.py`
- `scripts/fetch-research-mcp-preflight.py`
- `scripts/fetch-alpaca-core-preflight.py`

## Diagnosis

1. Confirm whether failure is wrapper, provider, auth, network, timeout, or empty response.
2. Preserve provider-specific gap categories for manifests.
3. Avoid printing env values or command lines containing secrets.
4. Prefer deterministic tests around wrappers and parsers before changing scheduler behavior.
5. If a command fails due to sandbox network restrictions and is essential, request escalation rather than silently changing behavior.

## Verification

Run focused tests for changed wrappers, usually:

```bash
PATH=/usr/local/bin:$PATH python3 -m unittest tests.test_fetch_research_mcp_preflight tests.test_mcp_runtime_wrappers
```
