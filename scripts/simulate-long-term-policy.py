#!/usr/bin/env python3
"""Simulate long-horizon equity policies from captured Alpaca MCP data.

Use ``scripts/fetch-alpaca-bars-mcp.py`` to capture daily bars first. This
script never calls Alpaca REST endpoints directly and never submits, replaces,
cancels, or closes orders.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
ONE_YEAR_SCRIPT = ROOT_DIR / "scripts" / "simulate-one-year-daily-policy.py"


def load_one_year_module() -> Any:
    spec = importlib.util.spec_from_file_location("simulate_one_year_daily_policy", ONE_YEAR_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {ONE_YEAR_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", type=Path, required=True, help="Captured Alpaca MCP daily bars JSON.")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path)
    parser.add_argument("--cache-json", type=Path, help="Optional compact bar cache output for compatibility.")
    parser.add_argument(
        "--strategy-config",
        type=Path,
        default=ROOT_DIR / "harness" / "strategies" / "long-term-quality-momentum-v1.yaml",
    )
    parser.add_argument("--metadata-yaml", type=Path, default=ROOT_DIR / "harness" / "symbol-metadata.yaml")
    parser.add_argument("--scorecard-json", type=Path)
    return parser.parse_args()


def write_cache(source: dict[str, Any], cache_path: Path) -> None:
    rows = source.get("extracted", {}).get("daily_bars", {})
    compact = {
        symbol: [
            {
                "t": row["date"],
                "o": row.get("open"),
                "h": row.get("high"),
                "l": row.get("low"),
                "c": row.get("close"),
                "v": row.get("volume"),
            }
            for row in symbol_rows
        ]
        for symbol, symbol_rows in rows.items()
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(compact, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    args = parse_args()
    source = json.loads(args.input_json.read_text(encoding="utf-8"))
    module = load_one_year_module()
    config = module.load_yaml(args.strategy_config)
    metadata = module.load_yaml(args.metadata_yaml)
    rows = source.get("extracted", {}).get("daily_bars")
    if not isinstance(rows, dict):
        raise SystemExit("input JSON must contain extracted.daily_bars")

    simulation = module.simulate(rows, config, metadata)
    data_manifest = {
        **source.get("data_manifest", {}),
        "dataset_hash": module.file_sha256(args.input_json),
        "raw_input_file": str(args.input_json),
    }
    output = {
        "run_id": "long-term-policy-simulation",
        "created_at": module.datetime.now().astimezone().isoformat(timespec="seconds"),
        "paper": True,
        "orders_submitted": 0,
        "strategy_config": str(args.strategy_config),
        "metadata_yaml": str(args.metadata_yaml),
        "data_manifest": data_manifest,
        "data_gaps": source.get("data_gaps", [])
        + [
            "This long-term simulator uses captured Alpaca MCP data only.",
            "Event/source confidence, valuation, earnings, and filing features are represented by metadata buckets unless joined from raw sources.",
        ],
        "simulation": simulation,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md = args.output_md or args.output_json.with_suffix(".md")
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(module.render_markdown(output), encoding="utf-8")
    if args.scorecard_json:
        scorecard = {
            "created_at": output["created_at"],
            "strategy_id": config["strategy_id"],
            "policy_status": config["policy_status"],
            "summary": simulation["summary"],
            "promotion_decision": "active_dry_run_candidate",
            "promotion_reason": "rolling validation and cost metrics recorded; quote/source/valuation blockers remain",
        }
        args.scorecard_json.parent.mkdir(parents=True, exist_ok=True)
        args.scorecard_json.write_text(json.dumps(scorecard, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.cache_json:
        write_cache(source, args.cache_json)


if __name__ == "__main__":
    main()
