#!/usr/bin/env python3
"""Validate a proposed Alpaca paper-trading order plan.

This script never submits orders. It checks the local JSON plan against the
machine-readable medium-risk policy in ``harness/risk-policy.yaml`` and the
order-plan JSON Schema in ``harness/order-plan.schema.json``.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_POLICY_PATH = ROOT_DIR / "harness" / "risk-policy.yaml"
DEFAULT_SCHEMA_PATH = ROOT_DIR / "harness" / "order-plan.schema.json"


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ModuleNotFoundError as exc:  # pragma: no cover - exercised only on minimal Python installs.
        raise RuntimeError("PyYAML is required to load harness/risk-policy.yaml") from exc

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def load_policy(path: Path = DEFAULT_POLICY_PATH) -> dict[str, Any]:
    return _load_yaml(path)


def policy_value(policy: dict[str, Any], section: str, key: str) -> Any:
    try:
        return policy[section][key]
    except KeyError as exc:
        raise ValueError(f"risk policy missing {section}.{key}") from exc


def as_float(value: Any, name: str, errors: list[str]) -> float:
    if isinstance(value, bool):
        errors.append(f"{name} must be a number")
        return 0.0

    try:
        number = float(value)
    except (TypeError, ValueError):
        errors.append(f"{name} must be a number")
        return 0.0
    if not math.isfinite(number):
        errors.append(f"{name} must be finite")
        return 0.0
    return number


def parse_datetime(value: Any, name: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{name} must be an ISO datetime string")
        return None
    raw = value.strip()
    normalized = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        errors.append(f"{name} must be an ISO datetime string")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{name} must include timezone information")
        return None
    return parsed.astimezone(timezone.utc)


def normalize_symbol(value: Any) -> str:
    return str(value or "").strip().upper()


def load_plan(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("order plan root must be a JSON object")
    return data


def format_schema_path(error: Any) -> str:
    parts = [str(part) for part in error.absolute_path]
    return ".".join(parts) if parts else "<root>"


def validate_schema(plan: dict[str, Any], schema_path: Path = DEFAULT_SCHEMA_PATH) -> list[str]:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ModuleNotFoundError as exc:  # pragma: no cover - exercised only on minimal Python installs.
        return [f"jsonschema is required to validate {schema_path}: {exc}"]

    with schema_path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors = sorted(validator.iter_errors(plan), key=lambda item: list(item.absolute_path))
    return [f"schema {format_schema_path(error)}: {error.message}" for error in schema_errors]


def validate(
    plan: dict[str, Any],
    policy: dict[str, Any] | None = None,
    *,
    check_schema: bool = True,
) -> tuple[list[str], list[str], dict[str, float | str]]:
    errors: list[str] = []
    warnings: list[str] = []

    policy = policy or load_policy()
    portfolio_limits = policy.get("portfolio_limits", {})
    order_limits = policy.get("order_limits", {})

    if check_schema:
        errors.extend(validate_schema(plan))

    policy_version = str(policy.get("version", "")).strip()
    if not policy_version:
        errors.append("risk policy version is required")
    elif plan.get("risk_policy_version") != policy_version:
        errors.append(f"risk_policy_version must be {policy_version}")

    max_invested_ratio = as_float(
        portfolio_limits.get("max_invested_ratio"), "risk_policy.portfolio_limits.max_invested_ratio", errors
    )
    min_cash_ratio = as_float(
        portfolio_limits.get("min_cash_ratio"), "risk_policy.portfolio_limits.min_cash_ratio", errors
    )
    max_ticker_ratio = as_float(
        portfolio_limits.get("max_ticker_ratio"), "risk_policy.portfolio_limits.max_ticker_ratio", errors
    )
    max_orders = int(policy_value(policy, "order_limits", "max_orders_per_run"))
    max_quote_age_minutes = as_float(
        order_limits.get("max_quote_age_minutes_submit"), "risk_policy.order_limits.max_quote_age_minutes_submit", errors
    )
    quote_age_tolerance_minutes = as_float(
        order_limits.get("quote_age_tolerance_minutes"), "risk_policy.order_limits.quote_age_tolerance_minutes", errors
    )
    limit_guardrail_ratio = as_float(
        order_limits.get("limit_guardrail_ratio"), "risk_policy.order_limits.limit_guardrail_ratio", errors
    )
    allowed_asset_types = {str(item).lower() for item in order_limits.get("allowed_asset_types", [])}
    allowed_sides = {str(item).lower() for item in order_limits.get("allowed_sides", [])}
    required_order_type = str(order_limits.get("required_order_type", "")).lower()
    required_time_in_force = str(order_limits.get("required_time_in_force", "")).lower()
    disallow_buy_reliance = bool(order_limits.get("disallow_buy_reliance_on_same_run_sell_proceeds", True))

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

    market_checked_at = parse_datetime(market.get("checked_at"), "market.checked_at", errors)

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

    if len(orders) > max_orders:
        errors.append(f"orders has {len(orders)} entries; maximum is {max_orders}")
    if not orders:
        warnings.append("orders is empty")

    buy_notional = 0.0
    sell_notional = 0.0
    seen_order_keys: set[tuple[str, str, int, float]] = set()

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
        quote_captured_at = parse_datetime(order.get("quote_captured_at"), f"{symbol}.quote_captured_at", errors)
        parse_datetime(order.get("asset_checked_at"), f"{symbol}.asset_checked_at", errors)
        client_order_id = str(order.get("client_order_id", "")).strip()

        asset_status = str(order.get("asset_status", "")).strip().lower()
        if asset_status and asset_status != "active":
            errors.append(f"{symbol}: asset_status must be active")
        if "asset_tradable" in order and order.get("asset_tradable") is not True:
            errors.append(f"{symbol}: asset_tradable must be true when provided")

        if asset_type not in allowed_asset_types:
            errors.append(f"{symbol}: asset_type must be one of {sorted(allowed_asset_types)}")
        if side not in allowed_sides:
            errors.append(f"{symbol}: side must be one of {sorted(allowed_sides)}")
        if order_type != required_order_type:
            errors.append(f"{symbol}: order_type must be {required_order_type}")
        if time_in_force != required_time_in_force:
            errors.append(f"{symbol}: time_in_force must be {required_time_in_force}")
        if not isinstance(qty_raw, int) or isinstance(qty_raw, bool) or qty < 1:
            errors.append(f"{symbol}: qty must be a whole-share integer >= 1")
        elif side in allowed_sides:
            order_key = (symbol, side, qty_raw, round(limit_price, 6))
            if order_key in seen_order_keys:
                errors.append(f"{symbol}: duplicate same-run order for side/qty/limit")
            seen_order_keys.add(order_key)
        if mode == "submit" and not client_order_id:
            errors.append(f"{symbol}: submit mode requires client_order_id for idempotency")
        if limit_price <= 0:
            errors.append(f"{symbol}: limit_price must be greater than 0")
        if reference_price <= 0:
            errors.append(f"{symbol}: reference_price must be greater than 0")
        if quote_age < 0:
            errors.append(f"{symbol}: quote_age_minutes must be non-negative")
        if mode == "submit" and quote_age > max_quote_age_minutes:
            errors.append(
                f"{symbol}: quote data is {quote_age:.1f} minutes old; maximum is {max_quote_age_minutes:.1f}"
            )
        elif mode == "dry_run" and quote_age > max_quote_age_minutes:
            warnings.append(
                f"{symbol}: quote data is {quote_age:.1f} minutes old; dry-run plans may keep stale quotes as evidence"
            )

        if market_checked_at and quote_captured_at:
            computed_age = (market_checked_at - quote_captured_at).total_seconds() / 60.0
            if computed_age < -quote_age_tolerance_minutes:
                errors.append(f"{symbol}: quote_captured_at is after market.checked_at")
            elif abs(computed_age - quote_age) > quote_age_tolerance_minutes:
                errors.append(
                    f"{symbol}: quote_age_minutes {quote_age:.1f} does not match timestamp age {computed_age:.1f}"
                )

        if limit_price > 0 and reference_price > 0:
            deviation = abs(limit_price - reference_price) / reference_price
            if deviation > limit_guardrail_ratio:
                errors.append(
                    f"{symbol}: limit price deviates {deviation:.2%}; maximum is {limit_guardrail_ratio:.2%}"
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

    min_cash = portfolio_value * min_cash_ratio
    max_invested = portfolio_value * max_invested_ratio
    max_ticker_value = portfolio_value * max_ticker_ratio

    if buy_notional > buying_power:
        errors.append(f"buy notional {buy_notional:.2f} exceeds buying power {buying_power:.2f}")
    if disallow_buy_reliance and buy_notional > cash:
        errors.append(
            f"buy notional {buy_notional:.2f} exceeds current cash {cash:.2f}; do not rely on same-run sell proceeds"
        )
    if post_cash < min_cash:
        errors.append(f"post-order cash {post_cash:.2f} is below required reserve {min_cash:.2f}")
    if post_invested > max_invested:
        errors.append(f"post-order invested exposure {post_invested:.2f} exceeds limit {max_invested:.2f}")

    for symbol, value in sorted(ticker_values.items()):
        if value > max_ticker_value:
            errors.append(f"{symbol}: post-order exposure {value:.2f} exceeds per-ticker limit {max_ticker_value:.2f}")

    summary = {
        "policy_version": policy_version,
        "buy_notional": buy_notional,
        "sell_notional": sell_notional,
        "post_cash": post_cash,
        "post_invested": post_invested,
        "min_cash": min_cash,
        "max_invested": max_invested,
        "max_ticker_value": max_ticker_value,
    }
    return errors, warnings, summary


def build_result(path: Path, errors: list[str], warnings: list[str], summary: dict[str, float | str]) -> dict[str, Any]:
    return {
        "status": "FAIL" if errors else "PASS",
        "path": str(path),
        "errors": errors,
        "warnings": warnings,
        "summary": summary,
    }


def print_human(result: dict[str, Any]) -> None:
    summary = result["summary"]
    print(f"Risk policy check: {result['status']}")
    print(f"- Policy version: {summary['policy_version']}")
    print(f"- Buy notional: {summary['buy_notional']:.2f}")
    print(f"- Sell notional: {summary['sell_notional']:.2f}")
    print(f"- Post-order cash: {summary['post_cash']:.2f} (minimum {summary['min_cash']:.2f})")
    print(f"- Post-order invested: {summary['post_invested']:.2f} (maximum {summary['max_invested']:.2f})")
    print(f"- Per-ticker maximum: {summary['max_ticker_value']:.2f}")

    for warning in result["warnings"]:
        print(f"WARNING: {warning}")

    if result["errors"]:
        print("Errors:")
        for error in result["errors"]:
            print(f"- {error}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate an Alpaca paper-trading order plan.")
    parser.add_argument("--json", action="store_true", help="print a machine-readable validation result")
    parser.add_argument("path", help="path to an order-plan JSON file")
    args = parser.parse_args(argv[1:])

    path = Path(args.path)
    try:
        policy = load_policy()
        plan = load_plan(path)
        errors, warnings, summary = validate(plan, policy)
    except Exception as exc:  # noqa: BLE001 - CLI should show any load/parse error plainly.
        result = build_result(path, [f"Could not validate {path}: {exc}"], [], {"policy_version": "unknown"})
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(f"Risk policy check: FAIL\n- Could not validate {path}: {exc}", file=sys.stderr)
        return 2

    result = build_result(path, errors, warnings, summary)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
