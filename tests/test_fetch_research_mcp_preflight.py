from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
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

    def test_build_mcp_coverage_hint_defaults_missing_gap_category(self) -> None:
        providers = [
            {
                "server": "firecrawl",
                "queried": True,
                "outcome": "failed",
                "checked_at": "2026-05-27T01:00:00+00:00",
                "gap_category": "",
                "gap_reason": "wrapper returned no structured error classification",
                "retry_count": 0,
            },
        ]

        rows = research_preflight.build_mcp_coverage_hint(providers, "wiki/evidence-store/sources/test.json")

        self.assertFalse(rows[0]["used_in_score"])
        self.assertEqual("unknown", rows[0]["gap_category"])

    def test_provider_cache_round_trip_marks_cache_hit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cache_dir = Path(directory)
            cache_key = research_preflight.provider_cache_key("fred", [])
            row = research_preflight.provider_row(
                server="fred",
                queried=True,
                outcome="pass",
                checked_at="2026-05-27T01:00:00+00:00",
                gap_category="not_applicable",
                gap_reason="",
                retry_count=0,
                payload={"series": ["DGS10"]},
            )

            research_preflight.save_cached_provider(cache_dir, "fred", cache_key, row, ttl_seconds=600)
            cached = research_preflight.load_cached_provider(cache_dir, "fred", cache_key, ttl_seconds=600)

        self.assertIsNotNone(cached)
        assert cached is not None
        self.assertEqual("fred", cached["server"])
        self.assertEqual("pass", cached["outcome"])
        self.assertTrue(cached["cache_hit"])
        self.assertEqual(600, cached["cache_ttl_seconds"])

    def test_provider_cache_ignores_expired_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cache_dir = Path(directory)
            cache_key = research_preflight.provider_cache_key("fred", [])
            path = research_preflight.provider_cache_path(cache_dir, "fred", cache_key)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(
                    {
                        "stored_at": (datetime.now(timezone.utc) - timedelta(seconds=120)).isoformat(),
                        "provider": {"server": "fred", "outcome": "pass"},
                    }
                ),
                encoding="utf-8",
            )

            cached = research_preflight.load_cached_provider(cache_dir, "fred", cache_key, ttl_seconds=60)

        self.assertIsNone(cached)


class ResearchMcpPreflightAsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_sec_edgar_uses_local_cik_cache_and_lightweight_tools(self) -> None:
        calls: list[tuple[str, dict]] = []

        async def fake_call_sequence_with_retries(**kwargs):
            calls.extend(kwargs["calls"])
            self.assertEqual("jsonl", kwargs["protocol"])
            return {"outcome": "pass", "payloads": [{"company": "ok"}, {"filings": []}], "retry_count": 0}

        with patch.object(research_preflight, "call_sequence_with_retries", new=fake_call_sequence_with_retries):
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
        calls: list[tuple[str, dict]] = []

        async def fake_call_sequence_with_retries(**kwargs):
            calls.extend(kwargs["calls"])
            self.assertEqual("jsonl", kwargs["protocol"])
            return {
                "outcome": "failed",
                "gap_category": "timeout",
                "gap_reason": "MCP stdio call sequence timed out after 75s",
                "retry_count": 1,
            }

        with patch.object(research_preflight, "call_sequence_with_retries", new=fake_call_sequence_with_retries):
            row = await research_preflight.capture_sec_edgar(
                {"SEC_EDGAR_USER_AGENT": "present"},
                ["AMZN", "INTC"],
                {"AMZN": "0001018724", "INTC": "0000050863"},
            )

        self.assertEqual("failed", row["outcome"])
        self.assertEqual("timeout", row["gap_category"])
        self.assertEqual(
            [
                ("get_company_info", {"identifier": "0001018724"}),
                ("get_recent_filings", {"identifier": "0001018724", "days": 30, "limit": 5}),
                ("get_company_info", {"identifier": "0000050863"}),
                ("get_recent_filings", {"identifier": "0000050863", "days": 30, "limit": 5}),
            ],
            calls,
        )
        self.assertIn("INTC", row["per_symbol"])
        self.assertEqual("timeout", row["per_symbol"]["AMZN"]["recent_filings"]["gap_category"])

    async def test_yahoo_finance_fails_fast_on_systemic_timeout(self) -> None:
        calls: list[tuple[str, dict]] = []

        async def fake_call_sequence_with_retries(**kwargs):
            calls.extend(kwargs["calls"])
            self.assertEqual("jsonl", kwargs["protocol"])
            return {
                "outcome": "failed",
                "gap_category": "timeout",
                "gap_reason": "MCP stdio call sequence timed out after 75s",
                "retry_count": 1,
            }

        with patch.object(research_preflight, "call_sequence_with_retries", new=fake_call_sequence_with_retries):
            row = await research_preflight.capture_yahoo_finance({"ALPHA_VANTAGE_API_KEY": "irrelevant"}, ["AMZN", "INTC"])

        self.assertEqual("failed", row["outcome"])
        self.assertEqual("timeout", row["gap_category"])
        self.assertEqual(
            [
                (
                    "get_recommendations",
                    {"ticker": "AMZN", "recommendation_type": "recommendations", "months_back": 12},
                ),
                ("get_yahoo_finance_news", {"ticker": "AMZN"}),
                (
                    "get_recommendations",
                    {"ticker": "INTC", "recommendation_type": "recommendations", "months_back": 12},
                ),
                ("get_yahoo_finance_news", {"ticker": "INTC"}),
            ],
            calls,
        )
        self.assertIn("INTC", row["per_symbol"])
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

    async def test_cached_or_capture_provider_uses_cache_before_capture(self) -> None:
        async def capture_should_not_run():
            raise AssertionError("cache hit should avoid provider capture")

        with tempfile.TemporaryDirectory() as directory:
            cache_dir = Path(directory)
            cache_key = research_preflight.provider_cache_key("fred", [])
            row = research_preflight.provider_row(
                server="fred",
                queried=True,
                outcome="pass",
                checked_at="2026-05-27T01:00:00+00:00",
                gap_category="not_applicable",
                gap_reason="",
                retry_count=0,
            )
            research_preflight.save_cached_provider(cache_dir, "fred", cache_key, row, ttl_seconds=600)

            cached = await research_preflight.cached_or_capture_provider(
                server="fred",
                symbols=[],
                cache_dir=cache_dir,
                cache_ttl_override=None,
                no_cache=False,
                circuit_state={},
                circuit_seconds=600,
                capture=capture_should_not_run,
            )

        self.assertTrue(cached["cache_hit"])
        self.assertEqual("pass", cached["outcome"])

    async def test_cached_or_capture_provider_returns_circuit_row(self) -> None:
        async def capture_should_not_run():
            raise AssertionError("open circuit should avoid provider capture")

        state = {
            "sec-edgar": {
                "opened_until": (datetime.now(timezone.utc) + timedelta(seconds=60)).isoformat(),
                "gap_category": "timeout",
                "gap_reason": "recent timeout",
            }
        }
        with tempfile.TemporaryDirectory() as directory:
            row = await research_preflight.cached_or_capture_provider(
                server="sec-edgar",
                symbols=["AMZN"],
                cache_dir=Path(directory),
                cache_ttl_override=0,
                no_cache=False,
                circuit_state=state,
                circuit_seconds=600,
                capture=capture_should_not_run,
            )

        self.assertEqual("failed", row["outcome"])
        self.assertEqual("timeout", row["gap_category"])
        self.assertTrue(row["payload"]["circuit_breaker_open"])


if __name__ == "__main__":
    unittest.main()
