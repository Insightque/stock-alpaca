from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "check-universe-coverage.py"

spec = importlib.util.spec_from_file_location("check_universe_coverage", SCRIPT_PATH)
assert spec and spec.loader
check_universe_coverage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_universe_coverage)


def base_manifest() -> dict:
    return {
        "run_id": "test-current-recommendation",
        "mode": "dry_run",
        "paper": True,
        "created_at": "2026-05-26T06:00:00Z",
        "schema_version": "1.3",
        "recommendation_actionability": "actionable",
        "risk_check_result": {"status": "PASS", "summary": {"order_count": 1}},
        "universe_coverage": {
            "universe_source": "harness/symbol-metadata.yaml + Alpaca watchlists",
            "scope_limited_by_user": False,
            "symbols_considered": 62,
            "symbols_loaded": 62,
            "minimum_required_symbols": 50,
            "benchmarks": ["SPY", "QQQ"],
            "screening_method": "broad_universe_price_liquidity_screen_then_all_mcp_shortlist_validation",
            "pre_mcp_shortlist": ["AMD", "LRCX", "UNH", "SMH", "MU"],
            "final_candidates": ["LRCX", "UNH", "AMD"],
            "passed": True,
            "gap_reason": "",
        },
    }


class UniverseCoverageTests(unittest.TestCase):
    def test_strict_actionable_manifest_passes_with_broad_universe(self) -> None:
        errors, warnings, summary = check_universe_coverage.validate(base_manifest(), strict=True)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)
        self.assertTrue(summary["strict_required"])
        self.assertEqual(62, summary["symbols_loaded"])

    def test_actionable_manifest_fails_when_too_narrow(self) -> None:
        manifest = base_manifest()
        manifest["universe_coverage"]["symbols_loaded"] = 12
        errors, _, _ = check_universe_coverage.validate(manifest)
        self.assertTrue(any("at least 50 loaded symbols" in e for e in errors))

    def test_user_limited_scope_allows_small_universe(self) -> None:
        manifest = base_manifest()
        manifest["universe_coverage"]["scope_limited_by_user"] = True
        manifest["universe_coverage"]["symbols_considered"] = 3
        manifest["universe_coverage"]["symbols_loaded"] = 3
        errors, _, summary = check_universe_coverage.validate(manifest, strict=True)
        self.assertEqual([], errors)
        self.assertTrue(summary["scope_limited_by_user"])

    def test_missing_benchmark_fails(self) -> None:
        manifest = base_manifest()
        manifest["universe_coverage"]["benchmarks"] = ["SPY"]
        errors, _, _ = check_universe_coverage.validate(manifest)
        self.assertTrue(any("missing required benchmarks: QQQ" in e for e in errors))

    def test_cli_json_reports_fail(self) -> None:
        manifest = base_manifest()
        manifest.pop("universe_coverage")
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(manifest, handle)
            path = Path(handle.name)
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--json", str(path)],
                check=False,
                text=True,
                capture_output=True,
            )
        finally:
            path.unlink(missing_ok=True)
        self.assertNotEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("FAIL", payload["status"])
        self.assertTrue(any("universe_coverage is required" in e for e in payload["errors"]))


if __name__ == "__main__":
    unittest.main()
