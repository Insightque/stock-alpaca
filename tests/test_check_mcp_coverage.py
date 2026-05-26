from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "check-mcp-coverage.py"

spec = importlib.util.spec_from_file_location("check_mcp_coverage", SCRIPT_PATH)
assert spec and spec.loader
check_mcp_coverage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_mcp_coverage)


def coverage_row(server: str, *, queried: bool = True, used: bool = True, outcome: str = "pass") -> dict:
    return {
        "server": server,
        "required": True,
        "queried": queried,
        "used_in_score": used,
        "outcome": outcome,
        "checked_at": "2026-05-26T06:00:00Z",
        "source_refs": [f"wiki/evidence-store/sources/test-{server}.md"] if queried else [],
        "gap_reason": "" if queried and outcome == "pass" else "test gap",
        "gap_category": "not_applicable" if outcome == "pass" else "unknown",
        "retry_count": 0,
    }


def base_manifest() -> dict:
    return {
        "run_id": "test-current-recommendation",
        "mode": "dry_run",
        "paper": True,
        "created_at": "2026-05-26T06:00:00Z",
        "schema_version": "1.2",
        "mcp_servers_used": list(check_mcp_coverage.REQUIRED_DECISION_MCPS),
        "mcp_failures": [],
        "mcp_coverage": [coverage_row(server) for server in check_mcp_coverage.REQUIRED_DECISION_MCPS],
        "recommendation_actionability": "actionable",
        "risk_check_result": {"status": "PASS", "summary": {"order_count": 1}},
    }


class McpCoverageTests(unittest.TestCase):
    def test_strict_actionable_manifest_passes_with_all_mcps(self) -> None:
        errors, warnings, summary = check_mcp_coverage.validate(base_manifest(), strict=True)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)
        self.assertTrue(summary["strict_required"])

    def test_actionable_manifest_fails_when_mcp_not_queried(self) -> None:
        manifest = base_manifest()
        for row in manifest["mcp_coverage"]:
            if row["server"] == "firecrawl":
                row.update(
                    {
                        "queried": False,
                        "used_in_score": False,
                        "outcome": "gap",
                        "source_refs": [],
                        "gap_reason": "firecrawl unavailable",
                    }
                )
        errors, _, _ = check_mcp_coverage.validate(manifest)
        self.assertTrue(any("firecrawl: research MCP gate requires queried=true" in e for e in errors))

    def test_actionable_manifest_allows_research_gap_when_minimum_confirmations_pass(self) -> None:
        manifest = base_manifest()
        for row in manifest["mcp_coverage"]:
            if row["server"] in {"fred", "firecrawl"}:
                row.update(
                    {
                        "queried": True,
                        "used_in_score": False,
                        "outcome": "failed",
                        "source_refs": [],
                        "gap_reason": "transient provider failure after retry",
                    }
                )
        errors, warnings, summary = check_mcp_coverage.validate(manifest, strict=True)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)
        self.assertEqual(3, summary["min_research_confirmations"])
        self.assertEqual(["alpha-vantage", "sec-edgar", "yahoo-finance"], summary["positive_research_confirmations"])

    def test_actionable_manifest_fails_when_research_confirmations_too_low(self) -> None:
        manifest = base_manifest()
        for row in manifest["mcp_coverage"]:
            if row["server"] in check_mcp_coverage.RESEARCH_DECISION_MCPS[:3]:
                row.update(
                    {
                        "queried": True,
                        "used_in_score": False,
                        "outcome": "failed",
                        "source_refs": [],
                        "gap_reason": "provider failure",
                    }
                )
        errors, _, _ = check_mcp_coverage.validate(manifest, strict=True)
        self.assertTrue(any("research MCP gate requires at least 3" in e for e in errors))

    def test_strict_gap_requires_gap_category(self) -> None:
        manifest = base_manifest()
        for row in manifest["mcp_coverage"]:
            if row["server"] == "sec-edgar":
                row.update(
                    {
                        "queried": True,
                        "used_in_score": False,
                        "outcome": "failed",
                        "source_refs": [],
                        "gap_reason": "tool call cancelled after retry",
                        "gap_category": "",
                    }
                )
        errors, _, _ = check_mcp_coverage.validate(manifest, strict=True)
        self.assertTrue(any("sec-edgar: strict failed/gap outcome requires gap_category" in e for e in errors))

    def test_non_actionable_research_allows_gap_with_warning(self) -> None:
        manifest = base_manifest()
        manifest["recommendation_actionability"] = "non_actionable_research"
        manifest["risk_check_result"]["summary"]["order_count"] = 0
        for row in manifest["mcp_coverage"]:
            if row["server"] == "sec-edgar":
                row.update(
                    {
                        "queried": False,
                        "used_in_score": False,
                        "outcome": "gap",
                        "source_refs": [],
                        "gap_reason": "not available in isolated research mode",
                    }
                )
        errors, warnings, summary = check_mcp_coverage.validate(manifest)
        self.assertEqual([], errors)
        self.assertTrue(warnings)
        self.assertFalse(summary["strict_required"])

    def test_used_in_score_requires_query_and_positive_outcome(self) -> None:
        manifest = base_manifest()
        for row in manifest["mcp_coverage"]:
            if row["server"] == "alpha-vantage":
                row.update(
                    {
                        "queried": False,
                        "used_in_score": True,
                        "outcome": "gap",
                        "source_refs": [],
                        "gap_reason": "not queried",
                    }
                )
        errors, _, _ = check_mcp_coverage.validate(manifest)
        self.assertTrue(any("used_in_score cannot be true" in e for e in errors))
        self.assertTrue(any("used_in_score requires a positive outcome" in e for e in errors))

    def test_cli_json_reports_fail(self) -> None:
        manifest = base_manifest()
        manifest["mcp_coverage"] = manifest["mcp_coverage"][:-1]
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
        self.assertTrue(any("yahoo-finance: missing" in e for e in payload["errors"]))


if __name__ == "__main__":
    unittest.main()
