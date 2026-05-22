# Medium Risk Policy

This policy is intentionally simple and conservative enough for automated paper trading while still allowing meaningful allocation experiments.

## Portfolio Limits

- Keep at least 20% of portfolio value in cash after new buy orders.
- Keep total invested exposure at or below 80% of portfolio value after new orders.
- Keep target exposure per ticker at or below 20% of portfolio value.
- Submit at most 10 new orders per run.

## Asset And Order Limits

- Allowed: active tradable US stocks and ETFs.
- Disallowed: live trading, options, crypto, shorts, margin-specific strategies, bracket orders, trailing stops, and fractional shares.
- Allowed order type: day limit orders only.
- Limit prices must be within 0.5% of the recorded reference price.
- Submit-mode quote data must be no older than 20 minutes.

## Failure Policy

If a proposed order plan violates any rule, do not submit orders. Update the relevant report with:

- The skipped ticker/order.
- The failing rule.
- The data source used for the decision.
- The next question or data gap to resolve.

