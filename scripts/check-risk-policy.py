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
DEFAULT_RECOMMENDATION_POLICY_PATH = ROOT_DIR / "harness" / "recommendation-policy.yaml"
DEFAULT_SCHEMA_PATH = ROOT_DIR / "harness" / "order-plan.schema.json"
DEFAULT_METADATA_PATH = ROOT_DIR / "harness" / "symbol-metadata.yaml"


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


def load_recommendation_policy(path: Path = DEFAULT_RECOMMENDATION_POLICY_PATH) -> dict[str, Any]:
    return _load_yaml(path)


def load_symbol_metadata(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    metadata_ref = policy.get("exposure_limits", {}).get("metadata_path")
    metadata_path = ROOT_DIR / metadata_ref if metadata_ref else DEFAULT_METADATA_PATH
    data = _load_yaml(metadata_path)
    defaults = data.get("defaults", {})
    symbols = data.get("symbols", {})
    if not isinstance(defaults, dict) or not isinstance(symbols, dict):
        raise ValueError(f"{metadata_path} must contain defaults and symbols mappings")
    return {str(symbol).upper(): {**defaults, **meta} for symbol, meta in symbols.items() if isinstance(meta, dict)}


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


def normalize_label(value: Any) -> str:
    return str(value or "").strip().lower()


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
    recommendation_policy: dict[str, Any] | None = None,
    *,
    check_schema: bool = True,
) -> tuple[list[str], list[str], dict[str, float | str]]:
    errors: list[str] = []
    warnings: list[str] = []

    policy = policy or load_policy()
    recommendation_policy = recommendation_policy or load_recommendation_policy()
    after_hours_policy = recommendation_policy.get("after_hours_policy", {})
    if not isinstance(after_hours_policy, dict):
        after_hours_policy = {}
    portfolio_limits = policy.get("portfolio_limits", {})
    exposure_limits = policy.get("exposure_limits", {})
    liquidity_limits = policy.get("liquidity_limits", {})
    order_limits = policy.get("order_limits", {})
    daily_limits = policy.get("daily_limits", {})
    correlated_cluster_limits = policy.get("correlated_cluster_limits", {})
    order_lifecycle = policy.get("order_lifecycle", {})
    symbol_metadata = load_symbol_metadata(policy)

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
    max_theme_ratio = as_float(
        exposure_limits.get("max_theme_ratio"), "risk_policy.exposure_limits.max_theme_ratio", errors
    )
    max_factor_ratio = as_float(
        exposure_limits.get("max_factor_ratio"), "risk_policy.exposure_limits.max_factor_ratio", errors
    )
    max_speculative_ratio = as_float(
        exposure_limits.get("max_speculative_ratio"), "risk_policy.exposure_limits.max_speculative_ratio", errors
    )
    require_exposure_metadata = bool(exposure_limits.get("require_exposure_metadata", False))
    max_cluster_ratio = as_float(
        correlated_cluster_limits.get("max_cluster_ratio", 1.0),
        "risk_policy.correlated_cluster_limits.max_cluster_ratio",
        errors,
    )
    cluster_overrides = correlated_cluster_limits.get("clusters", {})
    if not isinstance(cluster_overrides, dict):
        cluster_overrides = {}
    min_price = as_float(liquidity_limits.get("min_price", 0.0), "risk_policy.liquidity_limits.min_price", errors)
    min_adv = as_float(
        liquidity_limits.get("min_avg_daily_dollar_volume", 0.0),
        "risk_policy.liquidity_limits.min_avg_daily_dollar_volume",
        errors,
    )
    max_spread_pct = as_float(
        liquidity_limits.get("max_spread_pct", 100.0), "risk_policy.liquidity_limits.max_spread_pct", errors
    )
    reject_if_spread_missing = bool(liquidity_limits.get("reject_if_spread_missing", False))
    allowed_liquidity_buckets = {normalize_label(item) for item in liquidity_limits.get("allowed_liquidity_buckets", [])}
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
    max_policy_turnover = as_float(
        daily_limits.get("max_policy_turnover_ratio", 1.0),
        "risk_policy.daily_limits.max_policy_turnover_ratio",
        errors,
    )
    max_weekly_turnover = as_float(
        daily_limits.get("max_weekly_turnover_ratio", 1.0),
        "risk_policy.daily_limits.max_weekly_turnover_ratio",
        errors,
    )
    max_daily_loss_ratio = as_float(
        daily_limits.get("max_daily_realized_loss_ratio", 1.0),
        "risk_policy.daily_limits.max_daily_realized_loss_ratio",
        errors,
    )
    max_stop_count = int(daily_limits.get("max_stop_triggered_orders_per_day", 999999))
    max_new_orders_per_day = int(daily_limits.get("max_new_orders_per_day", 999999))
    raw_daily_order_cap_sides = daily_limits.get(
        "max_new_orders_per_day_applies_to_sides", order_limits.get("allowed_sides", [])
    )
    if not isinstance(raw_daily_order_cap_sides, list):
        errors.append("risk_policy.daily_limits.max_new_orders_per_day_applies_to_sides must be an array")
        raw_daily_order_cap_sides = []
    daily_order_cap_sides = {normalize_label(item) for item in raw_daily_order_cap_sides if normalize_label(item)}
    invalid_daily_order_cap_sides = daily_order_cap_sides - allowed_sides
    if invalid_daily_order_cap_sides:
        errors.append(
            "risk_policy.daily_limits.max_new_orders_per_day_applies_to_sides contains invalid sides "
            f"{sorted(invalid_daily_order_cap_sides)}"
        )
    max_open_age = as_float(
        order_lifecycle.get("max_open_order_age_minutes", 999999),
        "risk_policy.order_lifecycle.max_open_order_age_minutes",
        errors,
    )
    reject_duplicate_symbol_side = bool(order_lifecycle.get("reject_duplicate_symbol_side_same_day", True))
    require_partial_fill_recompute = bool(
        order_lifecycle.get("partial_fill_policy", {}).get("require_recompute_risk_after_fill", True)
    )

    mode = plan.get("mode")
    if mode not in {"dry_run", "submit"}:
        errors.append("mode must be 'dry_run' or 'submit'")

    if plan.get("paper") is not True:
        errors.append("paper must be true")

    market = plan.get("market")
    if not isinstance(market, dict):
        errors.append("market must be an object")
        market = {}

    market_session = normalize_label(market.get("session") or "regular")
    if market_session not in {"regular", "after_hours"}:
        errors.append("market.session must be regular or after_hours")
        market_session = "regular"

    if mode == "submit" and market_session == "regular" and market.get("is_open") is not True:
        errors.append("submit mode requires market.is_open=true")
    if mode == "submit" and market_session == "after_hours" and market.get("is_open") is True:
        errors.append("after_hours submit mode requires market.is_open=false")
    if market_session == "after_hours" and after_hours_policy.get("enabled_for_explicit_autopilot_runs") is not True:
        errors.append("after-hours orders require after_hours_policy.enabled_for_explicit_autopilot_runs=true")

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
    daily_realized_loss = as_float(account.get("daily_realized_loss", 0.0), "account.daily_realized_loss", errors)
    if portfolio_value > 0 and daily_realized_loss > portfolio_value * max_daily_loss_ratio:
        errors.append(
            f"daily realized loss {daily_realized_loss:.2f} exceeds limit {portfolio_value * max_daily_loss_ratio:.2f}"
        )

    risk_inputs = plan.get("risk_inputs", {})
    if not isinstance(risk_inputs, dict):
        errors.append("risk_inputs must be an object when provided")
        risk_inputs = {}
    turnover = as_float(risk_inputs.get("policy_turnover_ratio", 0.0), "risk_inputs.policy_turnover_ratio", errors)
    weekly_turnover = as_float(risk_inputs.get("weekly_turnover_ratio", 0.0), "risk_inputs.weekly_turnover_ratio", errors)
    stop_count = int(risk_inputs.get("stop_triggered_orders_today", 0) or 0)
    raw_new_orders_today = risk_inputs.get("new_orders_submitted_today")
    raw_after_hours_new_orders_today = risk_inputs.get("after_hours_new_orders_submitted_today")
    new_orders_submitted_today = 0
    after_hours_new_orders_submitted_today = 0
    if raw_new_orders_today is not None:
        if isinstance(raw_new_orders_today, bool):
            errors.append("risk_inputs.new_orders_submitted_today must be an integer")
        else:
            try:
                new_orders_submitted_today = int(raw_new_orders_today)
            except (TypeError, ValueError):
                errors.append("risk_inputs.new_orders_submitted_today must be an integer")
                new_orders_submitted_today = 0
            if new_orders_submitted_today < 0:
                errors.append("risk_inputs.new_orders_submitted_today must be non-negative")
    if raw_after_hours_new_orders_today is not None:
        if isinstance(raw_after_hours_new_orders_today, bool):
            errors.append("risk_inputs.after_hours_new_orders_submitted_today must be an integer")
        else:
            try:
                after_hours_new_orders_submitted_today = int(raw_after_hours_new_orders_today)
            except (TypeError, ValueError):
                errors.append("risk_inputs.after_hours_new_orders_submitted_today must be an integer")
                after_hours_new_orders_submitted_today = 0
            if after_hours_new_orders_submitted_today < 0:
                errors.append("risk_inputs.after_hours_new_orders_submitted_today must be non-negative")
    if turnover > max_policy_turnover:
        errors.append(f"policy turnover {turnover:.2%} exceeds daily limit {max_policy_turnover:.2%}")
    if weekly_turnover > max_weekly_turnover:
        errors.append(f"weekly turnover {weekly_turnover:.2%} exceeds weekly limit {max_weekly_turnover:.2%}")
    if stop_count > max_stop_count:
        errors.append(f"stop-triggered orders today {stop_count} exceeds limit {max_stop_count}")

    raw_positions = plan.get("positions", [])
    if not isinstance(raw_positions, list):
        errors.append("positions must be an array")
        raw_positions = []

    estimated_invested_from_account = max(portfolio_value - cash, 0.0)
    position_reconciliation_tolerance = max(portfolio_value * 0.02, 500.0)
    if estimated_invested_from_account > position_reconciliation_tolerance and not raw_positions:
        errors.append(
            "positions cannot be empty when account portfolio_value minus cash implies "
            f"{estimated_invested_from_account:.2f} of invested exposure"
        )

    position_qty: dict[str, float] = {}
    ticker_values: dict[str, float] = {}
    theme_values: dict[str, float] = {}
    factor_values: dict[str, float] = {}
    cluster_values: dict[str, float] = {}
    speculative_value = 0.0
    current_invested = 0.0

    def metadata_for(symbol: str, record: dict[str, Any], prefix: str) -> dict[str, Any]:
        policy_meta = symbol_metadata.get(symbol, {})
        metadata = {
            "theme": record.get("theme", policy_meta.get("theme")),
            "factor": record.get("factor", policy_meta.get("factor")),
            "volatility_bucket": record.get("volatility_bucket", policy_meta.get("volatility_bucket")),
            "speculative_flag": record.get("speculative_flag", policy_meta.get("speculative_flag", False)),
            "liquidity_bucket": record.get("liquidity_bucket", policy_meta.get("liquidity_bucket")),
            "source_confidence": record.get("source_confidence", policy_meta.get("source_confidence")),
            "correlated_cluster": record.get("correlated_cluster", policy_meta.get("correlated_cluster")),
        }
        missing = [
            key
            for key in ("theme", "factor", "volatility_bucket", "liquidity_bucket", "source_confidence")
            if not metadata.get(key)
        ]
        if require_exposure_metadata and missing:
            errors.append(f"{prefix}: missing exposure metadata fields {', '.join(missing)}")
        if metadata["volatility_bucket"] and normalize_label(metadata["volatility_bucket"]) not in {"low", "medium", "high"}:
            errors.append(f"{prefix}: volatility_bucket must be low, medium, or high")
        if metadata["liquidity_bucket"] and normalize_label(metadata["liquidity_bucket"]) not in {
            "mega",
            "large",
            "medium",
            "small",
            "unknown",
        }:
            errors.append(f"{prefix}: liquidity_bucket must be mega, large, medium, small, or unknown")
        if allowed_liquidity_buckets and normalize_label(metadata["liquidity_bucket"]) not in allowed_liquidity_buckets:
            errors.append(f"{prefix}: liquidity_bucket {metadata['liquidity_bucket']} is not allowed by risk policy")
        if metadata["source_confidence"] and normalize_label(metadata["source_confidence"]) not in {"high", "medium", "low"}:
            errors.append(f"{prefix}: source_confidence must be high, medium, or low")
        if not isinstance(metadata["speculative_flag"], bool):
            errors.append(f"{prefix}: speculative_flag must be boolean")
            metadata["speculative_flag"] = False
        metadata["theme"] = normalize_label(metadata["theme"])
        metadata["factor"] = normalize_label(metadata["factor"])
        metadata["volatility_bucket"] = normalize_label(metadata["volatility_bucket"])
        metadata["liquidity_bucket"] = normalize_label(metadata["liquidity_bucket"])
        metadata["source_confidence"] = normalize_label(metadata["source_confidence"])
        metadata["correlated_cluster"] = normalize_label(metadata["correlated_cluster"])
        return metadata

    def apply_exposure(value: float, metadata: dict[str, Any]) -> None:
        nonlocal speculative_value
        if metadata.get("theme"):
            theme_values[metadata["theme"]] = theme_values.get(metadata["theme"], 0.0) + value
        if metadata.get("factor"):
            factor_values[metadata["factor"]] = factor_values.get(metadata["factor"], 0.0) + value
        if metadata.get("correlated_cluster"):
            cluster_values[metadata["correlated_cluster"]] = cluster_values.get(metadata["correlated_cluster"], 0.0) + value
        if metadata.get("speculative_flag") is True:
            speculative_value += value

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
        apply_exposure(max(market_value, 0.0), metadata_for(symbol, position, f"positions[{index}]"))
        current_invested += max(market_value, 0.0)

    if (
        estimated_invested_from_account > position_reconciliation_tolerance
        and abs(current_invested - estimated_invested_from_account) > position_reconciliation_tolerance
    ):
        errors.append(
            f"positions market_value total {current_invested:.2f} does not reconcile with "
            f"account-implied invested exposure {estimated_invested_from_account:.2f} "
            f"within tolerance {position_reconciliation_tolerance:.2f}"
        )

    orders = plan.get("orders", [])
    if not isinstance(orders, list):
        errors.append("orders must be an array")
        orders = []

    if len(orders) > max_orders:
        errors.append(f"orders has {len(orders)} entries; maximum is {max_orders}")
    if not orders:
        warnings.append("orders is empty")
    planned_daily_cap_orders = sum(
        1
        for order in orders
        if isinstance(order, dict) and normalize_label(order.get("side")) in daily_order_cap_sides
    )
    if mode == "submit" and planned_daily_cap_orders and raw_new_orders_today is None:
        errors.append("submit mode requires risk_inputs.new_orders_submitted_today for daily order cap validation")
    if mode == "submit" and market_session == "after_hours" and raw_after_hours_new_orders_today is None:
        errors.append(
            "after_hours submit mode requires risk_inputs.after_hours_new_orders_submitted_today "
            "for separate session order cap validation"
        )
    if new_orders_submitted_today + planned_daily_cap_orders > max_new_orders_per_day:
        errors.append(
            "daily capped new orders "
            f"{new_orders_submitted_today + planned_daily_cap_orders} exceeds limit {max_new_orders_per_day}"
        )
    if market_session == "after_hours":
        planned_after_hours_orders = sum(
            1
            for order in orders
            if isinstance(order, dict)
            and normalize_label(order.get("side"))
            in {normalize_label(item) for item in after_hours_policy.get("allowed_sides", [])}
        )
        max_after_hours_orders = int(after_hours_policy.get("max_new_orders_per_session", 0) or 0)
        if after_hours_new_orders_submitted_today + planned_after_hours_orders > max_after_hours_orders:
            errors.append(
                "after-hours new orders "
                f"{after_hours_new_orders_submitted_today + planned_after_hours_orders} exceeds session limit "
                f"{max_after_hours_orders}"
            )

    buy_notional = 0.0
    sell_notional = 0.0
    seen_order_keys: set[tuple[str, str, int, float]] = set()
    seen_symbol_side: set[tuple[str, str]] = set()
    seen_client_order_ids: set[str] = set()
    seen_decision_ids: set[str] = set()
    open_symbol_side: set[tuple[str, str]] = set()

    raw_open_orders = plan.get("open_orders", [])
    if not isinstance(raw_open_orders, list):
        errors.append("open_orders must be an array when provided")
        raw_open_orders = []
    has_partial_fill = False
    for index, open_order in enumerate(raw_open_orders):
        if not isinstance(open_order, dict):
            errors.append(f"open_orders[{index}] must be an object")
            continue
        symbol = normalize_symbol(open_order.get("symbol"))
        side = str(open_order.get("side", "")).strip().lower()
        age = as_float(open_order.get("age_minutes"), f"open_orders[{index}].age_minutes", errors)
        status = normalize_label(open_order.get("status"))
        if age > max_open_age:
            errors.append(f"{symbol}: open order age {age:.1f} minutes exceeds lifecycle limit {max_open_age:.1f}")
        if status == "partially_filled":
            has_partial_fill = True
        if symbol and side:
            open_symbol_side.add((symbol, side))
        client_order_id = str(open_order.get("client_order_id", "")).strip()
        if client_order_id:
            seen_client_order_ids.add(client_order_id)

    if has_partial_fill and require_partial_fill_recompute and risk_inputs.get("risk_recomputed_after_partial_fill") is not True:
        errors.append("partial fill detected; risk_inputs.risk_recomputed_after_partial_fill must be true")

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
        order_session = normalize_label(order.get("session") or market_session)
        extended_hours = order.get("extended_hours", False)
        qty_raw = order.get("qty")
        qty = as_float(qty_raw, f"{symbol}.qty", errors)
        limit_price = as_float(order.get("limit_price"), f"{symbol}.limit_price", errors)
        reference_price = as_float(order.get("reference_price"), f"{symbol}.reference_price", errors)
        quote_age = as_float(order.get("quote_age_minutes"), f"{symbol}.quote_age_minutes", errors)
        quote_captured_at = parse_datetime(order.get("quote_captured_at"), f"{symbol}.quote_captured_at", errors)
        parse_datetime(order.get("asset_checked_at"), f"{symbol}.asset_checked_at", errors)
        client_order_id = str(order.get("client_order_id", "")).strip()
        decision_id = str(order.get("decision_id", "")).strip()
        policy_status = normalize_label(order.get("policy_status"))
        confidence_score = as_float(order.get("confidence_score"), f"{symbol}.confidence_score", errors)
        source_confidence = normalize_label(order.get("source_confidence"))
        review_bucket = str(order.get("review_bucket", "")).strip()
        liquidity = order.get("liquidity", {})

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
        if order_session != market_session:
            errors.append(f"{symbol}: order session must match market.session={market_session}")
        if market_session == "regular" and extended_hours is True:
            errors.append(f"{symbol}: regular-session orders must not set extended_hours=true")
        if market_session == "after_hours":
            if extended_hours is not True:
                errors.append(f"{symbol}: after-hours orders require extended_hours=true")
            if order_session != "after_hours":
                errors.append(f"{symbol}: after-hours orders require session=after_hours")
            expected_review_bucket = str(after_hours_policy.get("review_bucket", "")).strip()
            if not review_bucket:
                errors.append(f"{symbol}: after-hours orders require review_bucket")
            elif expected_review_bucket and review_bucket != expected_review_bucket:
                errors.append(f"{symbol}: review_bucket must be {expected_review_bucket}")
            allowed_after_hours_sides = {
                str(item).lower() for item in after_hours_policy.get("allowed_sides", []) if str(item).strip()
            }
            if allowed_after_hours_sides and side not in allowed_after_hours_sides:
                errors.append(f"{symbol}: side must be one of {sorted(allowed_after_hours_sides)} in after-hours")
        if not isinstance(qty_raw, int) or isinstance(qty_raw, bool) or qty < 1:
            errors.append(f"{symbol}: qty must be a whole-share integer >= 1")
        elif side in allowed_sides:
            order_key = (symbol, side, qty_raw, round(limit_price, 6))
            if order_key in seen_order_keys:
                errors.append(f"{symbol}: duplicate same-run order for side/qty/limit")
            seen_order_keys.add(order_key)
            symbol_side = (symbol, side)
            if reject_duplicate_symbol_side and symbol_side in seen_symbol_side:
                errors.append(f"{symbol}: duplicate same-day {side} order for symbol")
            seen_symbol_side.add(symbol_side)
            if reject_duplicate_symbol_side and symbol_side in open_symbol_side:
                errors.append(f"{symbol}: open {side} order already exists for symbol")
        if mode == "submit" and not client_order_id:
            errors.append(f"{symbol}: submit mode requires client_order_id for idempotency")
        if client_order_id:
            if client_order_id in seen_client_order_ids:
                errors.append(f"{symbol}: duplicate client_order_id {client_order_id}")
            seen_client_order_ids.add(client_order_id)
        if decision_id:
            if decision_id in seen_decision_ids:
                errors.append(f"{symbol}: duplicate decision_id {decision_id}")
            seen_decision_ids.add(decision_id)
        else:
            errors.append(f"{symbol}: decision_id is required")
        if side == "buy":
            if policy_status in {"observation_only", "comparison_only", "rejected"}:
                errors.append(f"{symbol}: policy_status {policy_status} cannot create a buy order plan entry")
            if mode == "submit" and policy_status != "auto_eligible_paper":
                errors.append(f"{symbol}: submit mode buy requires policy_status=auto_eligible_paper")
            if confidence_score < 0.5:
                errors.append(f"{symbol}: confidence_score {confidence_score:.2f} is below 0.50 minimum for buy")
            if source_confidence == "low":
                errors.append(f"{symbol}: source_confidence=low blocks new buy order generation")
        elif side == "sell" and str(order.get("entry_style", "")).strip().lower() not in {"trim", "exit"}:
            errors.append(f"{symbol}: sell orders require entry_style=trim or exit")
        if limit_price <= 0:
            errors.append(f"{symbol}: limit_price must be greater than 0")
        if reference_price <= 0:
            errors.append(f"{symbol}: reference_price must be greater than 0")
        if reference_price > 0 and reference_price < min_price:
            errors.append(f"{symbol}: reference_price {reference_price:.2f} is below minimum price {min_price:.2f}")
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

        if not isinstance(liquidity, dict):
            errors.append(f"{symbol}: liquidity must be an object")
            liquidity = {}
        spread_pct = as_float(liquidity.get("spread_pct"), f"{symbol}.liquidity.spread_pct", errors)
        avg_dollar_volume = as_float(
            liquidity.get("avg_daily_dollar_volume"), f"{symbol}.liquidity.avg_daily_dollar_volume", errors
        )
        bid = liquidity.get("bid")
        ask = liquidity.get("ask")
        if reject_if_spread_missing and "spread_pct" not in liquidity:
            errors.append(f"{symbol}: spread_pct is required by risk policy")
        if bid is not None and ask is not None:
            bid_value = as_float(bid, f"{symbol}.liquidity.bid", errors)
            ask_value = as_float(ask, f"{symbol}.liquidity.ask", errors)
            if bid_value > 0 and ask_value > 0 and ask_value < bid_value:
                errors.append(f"{symbol}: liquidity.ask must be greater than or equal to bid")
        if spread_pct > max_spread_pct:
            errors.append(f"{symbol}: spread_pct {spread_pct:.2f}% exceeds maximum {max_spread_pct:.2f}%")
        if avg_dollar_volume < min_adv:
            errors.append(
                f"{symbol}: avg daily dollar volume {avg_dollar_volume:.2f} is below minimum {min_adv:.2f}"
            )

        if market_session == "after_hours":
            max_after_hours_quote_age = as_float(
                after_hours_policy.get("max_quote_age_minutes_submit", max_quote_age_minutes),
                "recommendation_policy.after_hours_policy.max_quote_age_minutes_submit",
                errors,
            )
            after_hours_limit_guardrail = as_float(
                after_hours_policy.get("limit_guardrail_ratio", limit_guardrail_ratio),
                "recommendation_policy.after_hours_policy.limit_guardrail_ratio",
                errors,
            )
            max_after_hours_spread = as_float(
                after_hours_policy.get("max_spread_pct", max_spread_pct),
                "recommendation_policy.after_hours_policy.max_spread_pct",
                errors,
            )
            max_after_hours_notional_pct = as_float(
                after_hours_policy.get("max_notional_pct_per_order", 0.0),
                "recommendation_policy.after_hours_policy.max_notional_pct_per_order",
                errors,
            )
            if mode == "submit" and quote_age > max_after_hours_quote_age:
                errors.append(
                    f"{symbol}: after-hours quote data is {quote_age:.1f} minutes old; "
                    f"maximum is {max_after_hours_quote_age:.1f}"
                )
            if limit_price > 0 and reference_price > 0:
                after_hours_deviation = abs(limit_price - reference_price) / reference_price
                if after_hours_deviation > after_hours_limit_guardrail:
                    errors.append(
                        f"{symbol}: after-hours limit price deviates {after_hours_deviation:.2%}; "
                        f"maximum is {after_hours_limit_guardrail:.2%}"
                    )
            if spread_pct > max_after_hours_spread:
                errors.append(
                    f"{symbol}: after-hours spread_pct {spread_pct:.2f}% exceeds maximum "
                    f"{max_after_hours_spread:.2f}%"
                )
            if portfolio_value > 0 and qty > 0 and limit_price > 0:
                after_hours_notional = qty * limit_price
                max_after_hours_notional = portfolio_value * max_after_hours_notional_pct
                if after_hours_notional > max_after_hours_notional:
                    errors.append(
                        f"{symbol}: after-hours notional {after_hours_notional:.2f} exceeds "
                        f"per-order limit {max_after_hours_notional:.2f}"
                    )

        notional = max(qty, 0.0) * max(limit_price, 0.0)
        if side == "buy":
            buy_notional += notional
            ticker_values[symbol] = ticker_values.get(symbol, 0.0) + notional
            apply_exposure(notional, metadata_for(symbol, order, prefix))
        elif side == "sell":
            held_qty = position_qty.get(symbol, 0.0)
            if qty > held_qty:
                errors.append(f"{symbol}: sell qty {qty:g} exceeds held qty {held_qty:g}")
            sell_notional += notional
            ticker_values[symbol] = max(0.0, ticker_values.get(symbol, 0.0) - notional)
            apply_exposure(-notional, metadata_for(symbol, order, prefix))

    post_cash = cash - buy_notional + sell_notional
    post_invested = current_invested + buy_notional - sell_notional

    min_cash = portfolio_value * min_cash_ratio
    max_invested = portfolio_value * max_invested_ratio
    max_ticker_value = portfolio_value * max_ticker_ratio
    max_theme_value = portfolio_value * max_theme_ratio
    max_factor_value = portfolio_value * max_factor_ratio
    max_speculative_value = portfolio_value * max_speculative_ratio
    max_cluster_value = portfolio_value * max_cluster_ratio

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

    for theme, value in sorted(theme_values.items()):
        if value > max_theme_value:
            errors.append(f"theme {theme}: post-order exposure {value:.2f} exceeds theme limit {max_theme_value:.2f}")

    for factor, value in sorted(factor_values.items()):
        if value > max_factor_value:
            errors.append(f"factor {factor}: post-order exposure {value:.2f} exceeds factor limit {max_factor_value:.2f}")

    if speculative_value > max_speculative_value:
        errors.append(
            f"speculative exposure {speculative_value:.2f} exceeds speculative limit {max_speculative_value:.2f}"
        )

    for cluster, value in sorted(cluster_values.items()):
        override = cluster_overrides.get(cluster, {})
        cluster_ratio = as_float(
            override.get("max_ratio", max_cluster_ratio),
            f"risk_policy.correlated_cluster_limits.clusters.{cluster}.max_ratio",
            errors,
        )
        cluster_limit = portfolio_value * cluster_ratio
        if value > cluster_limit:
            errors.append(f"cluster {cluster}: post-order exposure {value:.2f} exceeds cluster limit {cluster_limit:.2f}")

    summary = {
        "policy_version": policy_version,
        "buy_notional": buy_notional,
        "sell_notional": sell_notional,
        "post_cash": post_cash,
        "post_invested": post_invested,
        "min_cash": min_cash,
        "max_invested": max_invested,
        "max_ticker_value": max_ticker_value,
        "max_theme_value": max_theme_value,
        "max_factor_value": max_factor_value,
        "max_speculative_value": max_speculative_value,
        "max_cluster_value": max_cluster_value,
        "speculative_value": speculative_value,
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
    print(f"- Per-theme maximum: {summary['max_theme_value']:.2f}")
    print(f"- Per-factor maximum: {summary['max_factor_value']:.2f}")
    print(f"- Speculative exposure: {summary['speculative_value']:.2f} (maximum {summary['max_speculative_value']:.2f})")
    print(f"- Default correlated-cluster maximum: {summary['max_cluster_value']:.2f}")

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
