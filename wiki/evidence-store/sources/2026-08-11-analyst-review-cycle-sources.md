---
id: 2026-08-11-analyst-review-cycle-sources
created_at: 2026-08-11T22:35:06Z
workflow: analyst-review-cycle
paper: true
---

# 2026-08-11 analyst review cycle sources

## Runtime anchor

- evaluated market session: `Tuesday, August 11, 2026 ET`
- runtime timestamp: `2026-08-11T22:35:06Z`
- workflow checksum: `f2e0c827a703feff49efe3fa2abc70a65a80f55da47e28ce4a26699a174bc0c9`

## Paper mode

- `ALPACA_PAPER_TRADE=true`

## MCP discovery

- discovery method: Codex `tool_search`
- query: `alpaca MCP account orders positions activities market data tools; sec-edgar mcp; alpha-vantage mcp; fred mcp; firecrawl mcp; yahoo-finance mcp`
- result: `0 tools found`

## Consequence

- Alpaca MCP read-only reconciliation tools (`get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_all_positions`, `get_watchlists`, `get_stock_bars`, `get_stock_snapshot`, `get_news`)를 호출할 surface가 현재 세션에 없었다.
- `sec-edgar`, `alpha-vantage`, `fred`, `firecrawl`, `yahoo-finance`도 동일하게 callable namespace가 없었다.
- `alpha-vantage` mandatory health check `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})`는 surface 부재 때문에 시작하지 못했다.

## Carry-forward evidence used

- prior review: [[2026-08-10-portfolio-review]]
- prior source note: [[2026-08-10-analyst-review-cycle-sources]]
- prior manifest: `wiki/evidence-store/run-manifests/2026-08-10-analyst-review-cycle.json`
- current due index: `wiki/trade-ledger/reviews/review-due-index.json`

## Carry-forward due state

- `pending_1d_count=0`
- `pending_5d_count=0`
- `pending_20d_count=1`
- `blocked_add_symbols=["NOK"]`
- next due: `Friday, August 21, 2026 ET` `NOK` `20D`

## Provider coverage

| provider | outcome | gap_category | note |
| --- | --- | --- | --- |
| `alpaca` | gap | `wrapper_error` | callable Codex MCP surface 미노출 |
| `sec-edgar` | gap | `wrapper_error` | callable Codex MCP surface 미노출 |
| `alpha-vantage` | gap | `wrapper_error` | required PING health check surface 미노출 |
| `fred` | gap | `wrapper_error` | callable Codex MCP surface 미노출 |
| `firecrawl` | gap | `wrapper_error` | callable Codex MCP surface 미노출 |
| `yahoo-finance` | gap | `wrapper_error` | callable Codex MCP surface 미노출 |

## Data gaps

- `August 11, 2026 ET` post-close Alpaca reconciliation is missing entirely for this run.
- local wiki artifacts alone cannot prove whether account value, open orders, fills, positions, or catalyst context changed after `Monday, August 10, 2026 ET` close.
