import plistlib
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class McpRuntimeWrapperTests(unittest.TestCase):
    def test_uvx_wrappers_use_workspace_local_runtime_dirs(self):
        for relative_path in (
            "scripts/alpaca-mcp.sh",
            "scripts/cancel-stale-autopilot-orders.py",
            "scripts/fetch-alpaca-core-preflight.py",
            "scripts/fetch-research-mcp-preflight.py",
            "scripts/mcp-alpha-vantage.sh",
            "scripts/mcp-sec-edgar.sh",
            "scripts/mcp-yahoo-finance.sh",
        ):
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                if relative_path.endswith(".py"):
                    if relative_path in {
                        "scripts/cancel-stale-autopilot-orders.py",
                        "scripts/fetch-alpaca-core-preflight.py",
                    }:
                        self.assertIn("session.call_tool", text)
                    else:
                        self.assertIn("Content-Length", text)
                        self.assertIn("tools/call", text)
                    self.assertIn("MCP_TIMEOUT_SECONDS", text)
                    continue
                self.assertIn("XDG_CACHE_HOME", text)
                self.assertIn("XDG_DATA_HOME", text)
                self.assertIn("UV_CACHE_DIR", text)
                self.assertIn("UV_TOOL_DIR", text)
                self.assertIn("UV_PYTHON_DOWNLOADS", text)
                self.assertIn("UV_LINK_MODE", text)
                self.assertIn("mkdir -p", text)

    def test_uvx_wrappers_prefer_installed_commands(self):
        expected_commands = {
            "scripts/alpaca-mcp.sh": "alpaca-mcp-server",
            "scripts/mcp-alpha-vantage.sh": "marketdata-mcp",
            "scripts/mcp-sec-edgar.sh": "sec-edgar-mcp",
            "scripts/mcp-yahoo-finance.sh": "yahoo-finance-mcp",
        }
        for relative_path, command in expected_commands.items():
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIn(f"command -v {command}", text)
                self.assertIn(f"exec {command}", text)

    def test_workspace_cache_is_not_tracked(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".cache/", gitignore.splitlines())

    def test_alpha_vantage_key_is_not_passed_as_process_argument(self):
        text = (ROOT / "scripts/mcp-alpha-vantage.sh").read_text(encoding="utf-8")

        self.assertIn("export ALPHA_VANTAGE_API_KEY", text)
        self.assertNotIn('marketdata-mcp "$ALPHA_VANTAGE_API_KEY"', text)

    def test_scheduled_codex_runs_preapprove_required_mcp_tools(self):
        expectations = {
            "scripts/run-hourly-autopilot-codex.sh": [
                "check-alpaca-market-open-mcp.py",
                "cancel-stale-autopilot-orders.py",
                "STALE_ORDER_CLEANUP_PATH",
                "fetch-alpaca-core-preflight.py",
                "ALPACA_PREFLIGHT_PATH",
                "Alpaca market is closed; scheduled autopilot exits before research/Codex run",
                'sandbox_permissions=["network-full-access"]',
                "mcp_servers.alpaca.command=",
                "mcp_servers.sec-edgar.command=",
                "mcp_servers.alpha-vantage.command=",
                "mcp_servers.fred.command=",
                "mcp_servers.firecrawl.command=",
                "mcp_servers.yahoo-finance.command=",
                'mcp_servers.alpaca.tools.get_clock.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_account_info.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_orders.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_all_positions.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_account_activities.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_watchlists.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_asset.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_stock_latest_quote.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_stock_snapshot.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_most_active_stocks.approval_mode="approve"',
                'mcp_servers.alpaca.tools.cancel_order_by_id.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_order_by_id.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_order_by_client_id.approval_mode="approve"',
                'mcp_servers.alpaca.tools.place_stock_order.approval_mode="approve"',
                'mcp_servers.sec-edgar.tools.get_recent_filings.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_LIST.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_GET.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_CALL.approval_mode="approve"',
                'mcp_servers.fred.tools.get_macro_snapshot.approval_mode="approve"',
                'mcp_servers.firecrawl.tools.firecrawl_scrape.approval_mode="approve"',
                'mcp_servers.yahoo-finance.tools.get_stock_info.approval_mode="approve"',
                "fetch-research-mcp-preflight.py",
                "RESEARCH_PREFLIGHT_PATH",
                "Do not run ad hoc local network helper scripts",
                "pre-submit gate summary",
                "client_order_id",
                "build-agent-dashboard.py",
                'CODEX_AUTOPILOT_TIMEOUT_SECONDS", "900"',
            ],
            "scripts/run-analyst-review-codex.sh": [
                'sandbox_permissions=["network-full-access"]',
                "mcp_servers.alpaca.command=",
                "mcp_servers.sec-edgar.command=",
                "mcp_servers.alpha-vantage.command=",
                "mcp_servers.fred.command=",
                "mcp_servers.firecrawl.command=",
                "mcp_servers.yahoo-finance.command=",
                'mcp_servers.alpaca.tools.get_clock.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_account_info.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_orders.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_all_positions.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_account_activities.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_watchlists.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_stock_latest_quote.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_stock_snapshot.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_most_active_stocks.approval_mode="approve"',
                'mcp_servers.sec-edgar.tools.get_recent_filings.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_LIST.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_GET.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_CALL.approval_mode="approve"',
                'mcp_servers.fred.tools.get_macro_snapshot.approval_mode="approve"',
                'mcp_servers.firecrawl.tools.firecrawl_scrape.approval_mode="approve"',
                'mcp_servers.yahoo-finance.tools.get_stock_info.approval_mode="approve"',
                "Do not run ad hoc local network helper scripts",
                "build-agent-dashboard.py",
            ],
        }
        for relative_path, snippets in expectations.items():
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIn("CODEX_HOME", text)
                self.assertIn("CODEX_SCHEDULED_CODEX_HOME", text)
                self.assertIn("--ephemeral", text)
                self.assertIn("--ignore-user-config", text)
                self.assertIn("workspace-write", text)
                self.assertIn("source .env", text)
                self.assertNotIn('approval_mode="auto"', text)
                self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", text)
                for snippet in snippets:
                    self.assertIn(snippet, text)

    def test_scheduled_autopush_tracks_dashboard_artifacts(self):
        text = (ROOT / "scripts/git-autopush-artifacts.sh").read_text(encoding="utf-8")

        self.assertIn("ui/agent-dashboard.html", text)
        self.assertIn("ui/backtests", text)

    def test_hourly_autopilot_launchd_runs_every_20_minutes(self):
        plist = plistlib.loads(
            (ROOT / "scheduler" / "com.insightque.stock-alpaca.hourly-autopilot.plist.example").read_bytes()
        )

        intervals = plist["StartCalendarInterval"]
        self.assertIsInstance(intervals, list)
        pairs = {(item["Hour"], item["Minute"]) for item in intervals}
        self.assertIn((22, 31), pairs)
        self.assertIn((22, 51), pairs)
        for hour in [23, 0, 1, 2, 3, 4, 5]:
            for minute in [11, 31, 51]:
                self.assertIn((hour, minute), pairs)
        self.assertNotIn((6, 11), pairs)


if __name__ == "__main__":
    unittest.main()
