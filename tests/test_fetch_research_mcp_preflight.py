from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "fetch-research-mcp-preflight.py"

spec = importlib.util.spec_from_file_location("fetch_research_mcp_preflight", SCRIPT_PATH)
assert spec and spec.loader
research_preflight = importlib.util.module_from_spec(spec)
sys.modules["fetch_research_mcp_preflight"] = research_preflight
spec.loader.exec_module(research_preflight)


class ResearchMcpPreflightTests(unittest.TestCase):
    def test_parse_symbols_deduplicates_and_normalizes(self) -> None:
        self.assertEqual(["AMZN", "INTC"], research_preflight.parse_symbols(" amzn,INTC,amzn ,, "))

    def test_read_env_supports_export_syntax(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".env").write_text('export FRED_API_KEY="present"\nALPACA_PAPER_TRADE=true\n', encoding="utf-8")

            env = research_preflight.read_env(root)

        self.assertEqual("present", env["FRED_API_KEY"])
        self.assertEqual("true", env["ALPACA_PAPER_TRADE"])

    def test_extract_symbols_from_alpaca_preflight_prefers_tight_spreads(self) -> None:
        payload = {
            "tool_results": {
                "get_stock_latest_quote": {
                    "batches": [
                        {
                            "payload": {
                                "quotes": {
                                    "WIDE": {"bp": 100, "ap": 110},
                                    "TIGHT": {"bp": 10, "ap": 10.01},
                                    "MID": {"bp": 20, "ap": 20.10},
                                }
                            }
                        }
                    ]
                }
            }
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(payload, handle)
            path = Path(handle.name)
        try:
            symbols = research_preflight.extract_symbols_from_alpaca_preflight(path, max_symbols=2)
        finally:
            path.unlink(missing_ok=True)

        self.assertEqual(["TIGHT", "MID"], symbols)

    def test_build_mcp_coverage_hint_preserves_gap_classification(self) -> None:
        providers = [
            {
                "server": "sec-edgar",
                "queried": True,
                "outcome": "pass",
                "checked_at": "2026-05-27T01:00:00+00:00",
                "gap_category": "not_applicable",
                "gap_reason": "",
                "retry_count": 0,
            },
            {
                "server": "firecrawl",
                "queried": True,
                "outcome": "unavailable",
                "checked_at": "2026-05-27T01:00:00+00:00",
                "gap_category": "auth",
                "gap_reason": "FIRECRAWL_API_KEY is not present in the scheduler environment.",
                "retry_count": 0,
            },
        ]

        rows = research_preflight.build_mcp_coverage_hint(providers, "wiki/evidence-store/sources/test.json")

        self.assertTrue(rows[0]["used_in_score"])
        self.assertEqual(["wiki/evidence-store/sources/test.json"], rows[0]["source_refs"])
        self.assertFalse(rows[1]["used_in_score"])
        self.assertTrue(rows[1]["queried"])
        self.assertEqual("auth", rows[1]["gap_category"])


class ResearchMcpPreflightAsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_sec_edgar_uses_local_cik_cache_and_lightweight_tools(self) -> None:
        calls: list[tuple[str, dict]] = []

        async def fake_call_with_retries(**kwargs):
            calls.append((kwargs["tool_name"], kwargs["arguments"]))
            self.assertEqual("jsonl", kwargs["protocol"])
            return {"outcome": "pass", "payload": {"ok": True}, "retry_count": 0}

        with patch.object(research_preflight, "call_with_retries", new=fake_call_with_retries):
            row = await research_preflight.capture_sec_edgar(
                {"SEC_EDGAR_USER_AGENT": "present"},
                ["AMZN", "SMH"],
                {"AMZN": "0001018724"},
            )

        self.assertEqual("pass", row["outcome"])
        self.assertEqual(
            [
                ("get_company_info", {"identifier": "0001018724"}),
                ("get_recent_filings", {"identifier": "0001018724", "days": 30, "limit": 5}),
            ],
            calls,
        )
        self.assertEqual("empty_response", row["per_symbol"]["SMH"]["gap_category"])

    async def test_sec_edgar_fails_fast_on_systemic_timeout(self) -> None:
        calls: list[str] = []

        async def fake_call_with_retries(**kwargs):
            calls.append(kwargs["tool_name"])
            self.assertEqual("jsonl", kwargs["protocol"])
            return {
                "outcome": "failed",
                "gap_category": "timeout",
                "gap_reason": "MCP stdio call sequence timed out after 75s",
                "retry_count": 1,
            }

        with patch.object(research_preflight, "call_with_retries", new=fake_call_with_retries):
            row = await research_preflight.capture_sec_edgar(
                {"SEC_EDGAR_USER_AGENT": "present"},
                ["AMZN", "INTC"],
                {"AMZN": "0001018724", "INTC": "0000050863"},
            )

        self.assertEqual("failed", row["outcome"])
        self.assertEqual("timeout", row["gap_category"])
        self.assertEqual(["get_company_info"], calls)
        self.assertNotIn("INTC", row["per_symbol"])
        self.assertEqual("timeout", row["per_symbol"]["AMZN"]["recent_filings"]["gap_category"])

    async def test_yahoo_finance_fails_fast_on_systemic_timeout(self) -> None:
        calls: list[str] = []

        async def fake_call_with_retries(**kwargs):
            calls.append(kwargs["tool_name"])
            self.assertEqual("jsonl", kwargs["protocol"])
            return {
                "outcome": "failed",
                "gap_category": "timeout",
                "gap_reason": "MCP stdio call sequence timed out after 75s",
                "retry_count": 1,
            }

        with patch.object(research_preflight, "call_with_retries", new=fake_call_with_retries):
            row = await research_preflight.capture_yahoo_finance({"ALPHA_VANTAGE_API_KEY": "irrelevant"}, ["AMZN", "INTC"])

        self.assertEqual("failed", row["outcome"])
        self.assertEqual("timeout", row["gap_category"])
        self.assertEqual(["get_recommendations"], calls)
        self.assertNotIn("INTC", row["per_symbol"])
        self.assertEqual("timeout", row["per_symbol"]["AMZN"]["news"]["gap_category"])

    async def test_alpha_vantage_sequence_counts_candidate_news(self) -> None:
        captured_calls: list[tuple[str, dict]] = []

        async def fake_sequence(**kwargs):
            self.assertEqual("jsonl", kwargs["protocol"])
            captured_calls.extend(kwargs["calls"])
            return [
                {"tools": ["PING", "NEWS_SENTIMENT"]},
                {"name": "PING"},
                {"text": "pong"},
                {"name": "NEWS_SENTIMENT"},
                {"feed": [{"title": "AMZN news"}]},
            ]

        with patch.object(research_preflight, "call_stdio_tool_sequence", new=fake_sequence):
            row = await research_preflight.capture_alpha_vantage({"ALPHA_VANTAGE_API_KEY": "present"}, ["AMZN"])

        self.assertEqual("pass", row["outcome"])
        self.assertEqual(1, row["payload"]["item_count"])
        self.assertEqual(
            ["TOOL_LIST", "TOOL_GET", "TOOL_CALL", "TOOL_GET", "TOOL_CALL"],
            [name for name, _ in captured_calls],
        )
        self.assertEqual("NEWS_SENTIMENT", captured_calls[-1][1]["tool_name"])

    async def test_alpha_vantage_empty_candidate_payload_is_gap_not_cancelled(self) -> None:
        async def fake_sequence(**kwargs):
            self.assertEqual("jsonl", kwargs["protocol"])
            return [
                {"tools": ["PING", "NEWS_SENTIMENT"]},
                {"name": "PING"},
                {"text": "pong"},
                {"name": "NEWS_SENTIMENT"},
                {"feed": []},
            ]

        with patch.object(research_preflight, "call_stdio_tool_sequence", new=fake_sequence):
            row = await research_preflight.capture_alpha_vantage({"ALPHA_VANTAGE_API_KEY": "present"}, ["INTC"])

        self.assertEqual("gap", row["outcome"])
        self.assertEqual("empty_response", row["gap_category"])


if __name__ == "__main__":
    unittest.main()
