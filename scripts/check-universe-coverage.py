#!/usr/bin/env python3
"""Validate broad-universe coverage for recommendation run manifests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_MIN_SYMBOLS = 50
REQUIRED_BENCHMARKS = {"SPY", "QQQ"}
RECO_MODES = {"dry_run", "submit", "research"}


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"{path}: manifest must be a JSON object")
    return payload


def has_order_entries(manifest: dict[str, Any]) -> bool:
    risk = manifest.get("risk_check_result", {})
    if isinstance(risk, dict):
        summary = risk.get("summary", {})
        if isinstance(summary, dict) and int(summary.get("order_count", 0) or 0) > 0:
            return True
        if int(risk.get("order_count", 0) or 0) > 0:
            return True
    order_plan = manifest.get("order_plan", {})
    return isinstance(order_plan, dict) and bool(order_plan.get("orders"))


def actionable_recommendation(manifest: dict[str, Any]) -> bool:
    if manifest.get("mode") == "submit":
        return True
    if has_order_entries(manifest):
        return True
    decision = str(manifest.get("recommendation_actionability", "")).lower()
    return decision in {"actionable", "order_candidate", "submit_candidate"}


def as_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def as_symbol_set(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item).strip().upper() for item in value if str(item).strip()}


def validate(manifest: dict[str, Any], *, strict: bool = False) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    mode = str(manifest.get("mode", ""))
    actionable = actionable_recommendation(manifest)
    strict_required = strict or actionable or mode == "submit"

    coverage = manifest.get("universe_coverage")
    if mode in RECO_MODES and not isinstance(coverage, dict):
        errors.append("universe_coverage is required for recommendation/research manifests")
        return errors, warnings, {
            "strict_required": strict_required,
            "actionable": actionable,
            "minimum_required_symbols": DEFAULT_MIN_SYMBOLS,
            "symbols_loaded": 0,
        }

    if not isinstance(coverage, dict):
        return errors, warnings, {
            "strict_required": strict_required,
            "actionable": actionable,
            "minimum_required_symbols": DEFAULT_MIN_SYMBOLS,
            "symbols_loaded": 0,
        }

    scope_limited = bool(coverage.get("scope_limited_by_user", False))
    minimum = as_int(coverage.get("minimum_required_symbols"), DEFAULT_MIN_SYMBOLS) or DEFAULT_MIN_SYMBOLS
    considered = as_int(coverage.get("symbols_considered"))
    loaded = as_int(coverage.get("symbols_loaded"))
    benchmarks = as_symbol_set(coverage.get("benchmarks"))
    pre_mcp = as_symbol_set(coverage.get("pre_mcp_shortlist"))
    final = as_symbol_set(coverage.get("final_candidates"))
    passed = bool(coverage.get("passed"))
    gap_reason = str(coverage.get("gap_reason", "")).strip()
    screening_method = str(coverage.get("screening_method", "")).strip()
    universe_source = str(coverage.get("universe_source", "")).strip()

    if not universe_source:
        errors.append("universe_coverage.universe_source is required")
    if not screening_method:
        errors.append("universe_coverage.screening_method is required")
    if considered < loaded:
        errors.append("universe_coverage.symbols_considered must be >= symbols_loaded")
    if not REQUIRED_BENCHMARKS.issubset(benchmarks):
        missing = ", ".join(sorted(REQUIRED_BENCHMARKS - benchmarks))
        errors.append(f"universe_coverage.benchmarks missing required benchmarks: {missing}")
    if pre_mcp and final and not final.issubset(pre_mcp):
        errors.append("universe_coverage.final_candidates must be a subset of pre_mcp_shortlist")
    if len(pre_mcp) > 10:
        errors.append("universe_coverage.pre_mcp_shortlist must not exceed 10 symbols")
    if strict_required and not scope_limited and loaded < minimum:
        errors.append(
            f"strict recommendation universe requires at least {minimum} loaded symbols unless user limited scope"
        )
    if strict_required and len(pre_mcp) < 5:
        errors.append("strict recommendation universe requires at least 5 pre-MCP shortlist symbols")
    if strict_required and len(final) < 3:
        errors.append("strict recommendation universe requires at least 3 final candidates")
    if strict_required and not passed:
        errors.append("strict recommendation universe requires universe_coverage.passed=true")
    if not passed and not gap_reason:
        errors.append("universe_coverage.gap_reason is required when passed=false")

    if mode in RECO_MODES and coverage and not strict_required and not passed:
        warnings.append("non-actionable recommendation has universe coverage gap; do not create order entries")

    return errors, warnings, {
        "strict_required": strict_required,
        "actionable": actionable,
        "minimum_required_symbols": minimum,
        "symbols_considered": considered,
        "symbols_loaded": loaded,
        "benchmarks": sorted(benchmarks),
        "pre_mcp_shortlist_count": len(pre_mcp),
        "final_candidate_count": len(final),
        "scope_limited_by_user": scope_limited,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate recommendation universe coverage in a run manifest.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--strict", action="store_true", help="Require broad-universe coverage to pass.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable validation output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    errors, warnings, summary = validate(manifest, strict=args.strict)
    payload = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "summary": summary,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload["status"])
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
