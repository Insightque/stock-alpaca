#!/usr/bin/env python3
"""Validate MCP coverage for recommendation run manifests.

This checker is intentionally stricter than a JSON schema. The schema can
verify shape, but this script verifies the recommendation contract: every
connected decision MCP must either be queried and tied to evidence, or the run
must clearly block actionable recommendations.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_DECISION_MCPS = (
    "alpaca",
    "sec-edgar",
    "alpha-vantage",
    "fred",
    "firecrawl",
    "yahoo-finance",
)
CORE_DECISION_MCPS = ("alpaca",)
RESEARCH_DECISION_MCPS = tuple(server for server in REQUIRED_DECISION_MCPS if server not in CORE_DECISION_MCPS)
DEFAULT_MIN_RESEARCH_CONFIRMATIONS = 3

RECO_MODES = {"dry_run", "submit", "research"}
POSITIVE_OUTCOMES = {"pass", "usable", "ok"}
GAP_OUTCOMES = {"gap", "failed", "unavailable", "not_applicable"}


def as_bool(value: Any) -> bool:
    return bool(value) if isinstance(value, bool) else False


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


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


def normalize_coverage(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = manifest.get("mcp_coverage")
    if not isinstance(rows, list):
        return {}
    normalized: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        server = str(row.get("server", "")).strip()
        if server:
            normalized[server] = row
    return normalized


def validate(manifest: dict[str, Any], *, strict: bool = False) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    mode = str(manifest.get("mode", ""))
    coverage = normalize_coverage(manifest)
    actionable = actionable_recommendation(manifest)
    strict_required = strict or actionable or mode == "submit"
    gate_policy = manifest.get("mcp_gate_policy", {})
    if not isinstance(gate_policy, dict):
        gate_policy = {}
    try:
        min_research_confirmations = int(
            gate_policy.get("min_research_confirmations", DEFAULT_MIN_RESEARCH_CONFIRMATIONS)
        )
    except (TypeError, ValueError):
        min_research_confirmations = DEFAULT_MIN_RESEARCH_CONFIRMATIONS
    min_research_confirmations = max(0, min(min_research_confirmations, len(RESEARCH_DECISION_MCPS)))
    positive_research: list[str] = []
    used_positive_research: list[str] = []

    if mode in RECO_MODES and not coverage:
        errors.append("mcp_coverage is required for recommendation/research manifests")
        return errors, warnings, {
            "required_servers": list(REQUIRED_DECISION_MCPS),
            "covered_servers": [],
            "strict_required": strict_required,
            "actionable": actionable,
        }

    for server in REQUIRED_DECISION_MCPS:
        row = coverage.get(server)
        if not row:
            errors.append(f"{server}: missing mcp_coverage row")
            continue

        queried = as_bool(row.get("queried"))
        used = as_bool(row.get("used_in_score"))
        outcome = str(row.get("outcome", "")).lower()
        gap_reason = str(row.get("gap_reason", "")).strip()
        source_refs = [str(item) for item in as_list(row.get("source_refs")) if str(item).strip()]

        if outcome not in POSITIVE_OUTCOMES | GAP_OUTCOMES:
            errors.append(f"{server}: outcome must be one of {sorted(POSITIVE_OUTCOMES | GAP_OUTCOMES)}")

        if queried and outcome in POSITIVE_OUTCOMES and not source_refs:
            errors.append(f"{server}: queried MCP must include at least one source_ref")

        if used and not queried:
            errors.append(f"{server}: used_in_score cannot be true when queried is false")

        if used and outcome not in POSITIVE_OUTCOMES:
            errors.append(f"{server}: used_in_score requires a positive outcome")

        if not queried and not gap_reason:
            errors.append(f"{server}: not queried requires gap_reason")

        if outcome in GAP_OUTCOMES and not gap_reason:
            errors.append(f"{server}: gap/failed outcome requires gap_reason")

        if server in RESEARCH_DECISION_MCPS and queried and outcome in POSITIVE_OUTCOMES:
            positive_research.append(server)
            if used:
                used_positive_research.append(server)

        if strict_required and server in CORE_DECISION_MCPS and not queried:
            errors.append(f"{server}: core MCP gate requires queried=true")

        if strict_required and server in CORE_DECISION_MCPS and outcome not in POSITIVE_OUTCOMES:
            errors.append(f"{server}: core MCP gate requires usable/pass outcome")

        if strict_required and server in RESEARCH_DECISION_MCPS and not queried:
            errors.append(f"{server}: research MCP gate requires queried=true or an attempted failure row")

    if strict_required and len(positive_research) < min_research_confirmations:
        errors.append(
            "research MCP gate requires at least "
            f"{min_research_confirmations} usable/pass research providers; got {len(positive_research)} "
            f"({', '.join(sorted(positive_research)) or 'none'})"
        )

    if mode == "submit":
        unused_core = [
            server
            for server, row in coverage.items()
            if server in CORE_DECISION_MCPS and not as_bool(row.get("used_in_score"))
        ]
        if unused_core:
            errors.append(f"submit mode requires core MCPs to be used_in_score: {', '.join(sorted(unused_core))}")
        if len(used_positive_research) < min_research_confirmations:
            errors.append(
                "submit mode requires at least "
                f"{min_research_confirmations} positive research MCPs to be used_in_score: "
                f"{', '.join(sorted(used_positive_research)) or 'none'}"
            )

    if mode in RECO_MODES and coverage and not strict_required:
        gaps = [
            server
            for server, row in coverage.items()
            if server in REQUIRED_DECISION_MCPS and str(row.get("outcome", "")).lower() in GAP_OUTCOMES
        ]
        if gaps:
            warnings.append(
                "non-actionable recommendation has MCP gaps; do not create order entries before resolving: "
                + ", ".join(sorted(gaps))
            )

    return errors, warnings, {
        "required_servers": list(REQUIRED_DECISION_MCPS),
        "core_servers": list(CORE_DECISION_MCPS),
        "research_servers": list(RESEARCH_DECISION_MCPS),
        "covered_servers": sorted(coverage),
        "strict_required": strict_required,
        "actionable": actionable,
        "min_research_confirmations": min_research_confirmations,
        "positive_research_confirmations": sorted(positive_research),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate MCP decision-source coverage in a run manifest.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--strict", action="store_true", help="Require all decision MCPs to be queried and usable.")
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
