#!/usr/bin/env python3
"""Validate a proposed Alpaca paper-trading order plan.

This script never submits orders. It checks the local JSON plan against the
medium-risk policy documented in AGENTS.md and harness/risk-policy.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


MAX_INVESTED_RATIO = 0.80
MIN_CASH_RATIO = 0.20
MAX_TICKER_RATIO = 0.20
MAX_ORDERS = 10
MAX_QUOTE_AGE_MINUTES = 20.0
LIMIT_GUARDRAIL_RATIO = 0.005
ALLOWED_ASSET_TYPES = {"stock", "etf"}


def as_float(value: Any, name: str, errors: list[str]) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        errors.append(f"{name} must be a number")
        return 0.0
    if number != number:
        errors.append(f"{name} must not be NaN")
        return 0.0
    return number


def normalize_symbol(value: Any) -> str:
    return str(value or "").strip().upper()


def load_plan(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("order plan root must be a JSON object")
    return data


def validate(plan: dict[str, Any]) -> tuple[list[str], list[str], dict[str, float]]:
    errors: list[str] = []
    warnings: list[str] = []

    mode = plan.get("mode")
    if mode not in {"dry_run", "submit"}:
        errors.append("mode must be 'dry_run' or 'submit'")

    if plan.get("paper") is not True:
        errors.append("paper must be true")

    market = plan.get("market")
    if not isinstance(market, dict):
        errors.append("market must be an object")
        market = {}

    if mode == "submit" and market.get("is_open") is not True:
        errors.append("submit mode requires market.is_open=true")

    account = plan.get("account")
    if not isinstance(account, dict):
        errors.append("account must be an object")
        account = {}

    portfolio_value = as_float(account.get("portfolio_value"), "account.portfolio_value", errors)
    cash = as_float(account.get("cash"), "account.cash", errors)
    buying_power = as_float(account.get("buying_power"), "account.buying_power", errors)

    if portfolio_value <= 0:
        errors.append("account.portfolio_value must be greater than 0")
    if cash < 0:
        errors.append("account.cash must be non-negative")
    if buying_power < 0:
        errors.append("account.buying_power must be non-negative")

    raw_positions = plan.get("positions", [])
    if not isinstance(raw_positions, list):
        errors.append("positions must be an array")
        raw_positions = []

    position_qty: dict[str, float] = {}
    ticker_values: dict[str, float] = {}
    current_invested = 0.0

    for index, position in enumerate(raw_positions):
        if not isinstance(position, dict):
            errors.append(f"positions[{index}] must be an object")
            continue
        symbol = normalize_symbol(position.get("symbol"))
        if not symbol:
            errors.append(f"positions[{index}].symbol is required")
            continue
        qty = as_float(position.get("qty"), f"positions[{index}].qty", errors)
        market_value = as_float(position.get("market_value"), f"positions[{index}].market_value", errors)
        if qty < 0:
            errors.append(f"{symbol}: existing short positions are not allowed")
        if market_value < 0:
            errors.append(f"{symbol}: market_value must be non-negative")
        position_qty[symbol] = position_qty.get(symbol, 0.0) + qty
        ticker_values[symbol] = ticker_values.get(symbol, 0.0) + max(market_value, 0.0)
        current_invested += max(market_value, 0.0)

    orders = plan.get("orders", [])
    if not isinstance(orders, list):
        errors.append("orders must be an array")
        orders = []

    if len(orders) > MAX_ORDERS:
        errors.append(f"orders has {len(orders)} entries; maximum is {MAX_ORDERS}")
    if not orders:
        warnings.append("orders is empty")

    buy_notional = 0.0
    sell_notional = 0.0

    for index, order in enumerate(orders):
        prefix = f"orders[{index}]"
        if not isinstance(order, dict):
            errors.append(f"{prefix} must be an object")
            continue

        symbol = normalize_symbol(order.get("symbol"))
        if not symbol:
            errors.append(f"{prefix}.symbol is required")
            continue

        asset_type = str(order.get("asset_type", "")).strip().lower()
        side = str(order.get("side", "")).strip().lower()
        order_type = str(order.get("order_type", "")).strip().lower()
        time_in_force = str(order.get("time_in_force", "")).strip().lower()
        qty_raw = order.get("qty")
        qty = as_float(qty_raw, f"{symbol}.qty", errors)
        limit_price = as_float(order.get("limit_price"), f"{symbol}.limit_price", errors)
        reference_price = as_float(order.get("reference_price"), f"{symbol}.reference_price", errors)
        quote_age = as_float(order.get("quote_age_minutes"), f"{symbol}.quote_age_minutes", errors)

        if asset_type not in ALLOWED_ASSET_TYPES:
            errors.append(f"{symbol}: asset_type must be stock or etf")
        if side not in {"buy", "sell"}:
            errors.append(f"{symbol}: side must be buy or sell")
        if order_type != "limit":
            errors.append(f"{symbol}: order_type must be limit")
        if time_in_force != "day":
            errors.append(f"{symbol}: time_in_force must be day")
        if not isinstance(qty_raw, int) or qty < 1:
            errors.append(f"{symbol}: qty must be a whole-share integer >= 1")
        if limit_price <= 0:
            errors.append(f"{symbol}: limit_price must be greater than 0")
        if reference_price <= 0:
            errors.append(f"{symbol}: reference_price must be greater than 0")
        if quote_age < 0:
            errors.append(f"{symbol}: quote_age_minutes must be non-negative")
        if mode == "submit" and quote_age > MAX_QUOTE_AGE_MINUTES:
            errors.append(
                f"{symbol}: quote data is {quote_age:.1f} minutes old; maximum is {MAX_QUOTE_AGE_MINUTES:.1f}"
            )

        if limit_price > 0 and reference_price > 0:
            deviation = abs(limit_price - reference_price) / reference_price
            if deviation > LIMIT_GUARDRAIL_RATIO:
                errors.append(
                    f"{symbol}: limit price deviates {deviation:.2%}; maximum is {LIMIT_GUARDRAIL_RATIO:.2%}"
                )

        notional = max(qty, 0.0) * max(limit_price, 0.0)
        if side == "buy":
            buy_notional += notional
            ticker_values[symbol] = ticker_values.get(symbol, 0.0) + notional
        elif side == "sell":
            held_qty = position_qty.get(symbol, 0.0)
            if qty > held_qty:
                errors.append(f"{symbol}: sell qty {qty:g} exceeds held qty {held_qty:g}")
            sell_notional += notional
            ticker_values[symbol] = max(0.0, ticker_values.get(symbol, 0.0) - notional)

    post_cash = cash - buy_notional + sell_notional
    post_invested = current_invested + buy_notional - sell_notional

    min_cash = portfolio_value * MIN_CASH_RATIO
    max_invested = portfolio_value * MAX_INVESTED_RATIO
    max_ticker_value = portfolio_value * MAX_TICKER_RATIO

    if buy_notional > buying_power:
        errors.append(f"buy notional {buy_notional:.2f} exceeds buying power {buying_power:.2f}")
    if post_cash < min_cash:
        errors.append(f"post-order cash {post_cash:.2f} is below required reserve {min_cash:.2f}")
    if post_invested > max_invested:
        errors.append(f"post-order invested exposure {post_invested:.2f} exceeds limit {max_invested:.2f}")

    for symbol, value in sorted(ticker_values.items()):
        if value > max_ticker_value:
            errors.append(f"{symbol}: post-order exposure {value:.2f} exceeds per-ticker limit {max_ticker_value:.2f}")

    summary = {
        "buy_notional": buy_notional,
        "sell_notional": sell_notional,
        "post_cash": post_cash,
        "post_invested": post_invested,
        "min_cash": min_cash,
        "max_invested": max_invested,
        "max_ticker_value": max_ticker_value,
    }
    return errors, warnings, summary


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 scripts/check-risk-policy.py path/to/order-plan.json", file=sys.stderr)
        return 2

    path = Path(argv[1])
    try:
        plan = load_plan(path)
    except Exception as exc:  # noqa: BLE001 - CLI should show any load/parse error plainly.
        print(f"Risk policy check: FAIL\n- Could not load {path}: {exc}", file=sys.stderr)
        return 1

    errors, warnings, summary = validate(plan)

    status = "FAIL" if errors else "PASS"
    print(f"Risk policy check: {status}")
    print(f"- Buy notional: {summary['buy_notional']:.2f}")
    print(f"- Sell notional: {summary['sell_notional']:.2f}")
    print(f"- Post-order cash: {summary['post_cash']:.2f} (minimum {summary['min_cash']:.2f})")
    print(f"- Post-order invested: {summary['post_invested']:.2f} (maximum {summary['max_invested']:.2f})")
    print(f"- Per-ticker maximum: {summary['max_ticker_value']:.2f}")

    for warning in warnings:
        print(f"WARNING: {warning}")

    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

