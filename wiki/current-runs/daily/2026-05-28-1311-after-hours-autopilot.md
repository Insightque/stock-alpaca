# 2026-05-28 13:11 KST after-hours autopilot

- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인

## Gate Summary

- Alpaca regular market: closed (`is_open=false`, clock `2026-05-28T00:15:18.805127399-04:00`). 정규장 open 상태가 아니므로 after-hours workflow 진행 가능.
- Scheduler Alpaca core preflight: account/positions/open orders/assets/quotes rows pass. `first_blocking_gate=market_closed`는 after-hours expected non-blocking으로 처리.
- Research MCP preflight: SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass. Alpha Vantage는 `empty_response` gap이며 minimum research confirmations 3개 이상 충족.
- Universe gate: 62 symbols loaded, SPY/QQQ 포함, final candidates QQQ/NOK/INTC.
- Quote/spread gate: INTC overnight quote bid 116.86, ask 117.15, spread 0.247853%, quote age 0.116분.
- Separate budget: `risk_inputs.after_hours_new_orders_submitted_today=0`; regular validation count 미사용.

## Planned Order

- INTC 1주 buy limit 117.15, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, client_order_id `ah-20260528-1311-intc-buy-01`.
- Submit은 strict universe/MCP/risk validation 통과 후에만 진행한다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-1311-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-28-1311-after-hours-autopilot.json`
- Core preflight: `wiki/evidence-store/sources/2026-05-28-1311-after-hours-autopilot-alpaca-core-preflight.json`
- Research preflight: `wiki/evidence-store/sources/2026-05-28-1311-after-hours-autopilot-research-mcp-preflight.json`

## Pre-Submit Refresh

- Refreshed INTC overnight quote at `2026-05-28T04:18:08.461875758Z`: bid 116.57, ask 116.80, spread 0.197112%, quote age 0.159분 at `2026-05-28T04:18:18Z`.
- Open orders: 0. Regular market remains closed by Alpaca clock at `2026-05-28T00:18:04.472106849-04:00`.

## Submit And Reconcile

- Pre-submit validators: universe strict PASS, MCP strict PASS, risk policy PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json`).
- Submitted through Alpaca MCP `place_stock_order` only. Direct Alpaca REST was not used.
- Reconciled by `client_order_id=ah-20260528-1311-intc-buy-01`.
- Result: filled. Order id `843838bd-6083-481d-b013-5ec7b0bf47fd`, filled_qty 1, filled_avg_price 116.79, filled_at `2026-05-28T04:19:01.732105386Z`.
- Post-trade account check: portfolio value 100344.46 USD, cash 41059.19 USD, buying power 135284.39 USD.
- Position check: INTC 1주, avg_entry_price 116.79, current_price 116.77.
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-05-28-1311-after-hours-autopilot-post-trade.json`
