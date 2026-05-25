from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class McpOnlyMarketDataTest(unittest.TestCase):
    def test_intraday_simulators_do_not_call_alpaca_rest_directly(self):
        for relative in (
            "scripts/simulate-intraday-policy-candidates.py",
            "scripts/simulate-short-long-policy-review.py",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("APCA-API-KEY-ID", text)
            self.assertNotIn("APCA-API-SECRET-KEY", text)
            self.assertNotIn("data.alpaca.markets", text)
            self.assertNotIn("urllib.parse", text)

    def test_intraday_simulators_use_alpaca_mcp_helper(self):
        for relative in (
            "scripts/simulate-intraday-policy-candidates.py",
            "scripts/simulate-short-long-policy-review.py",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("fetch_stock_bars_mcp", text)
            self.assertIn("Alpaca MCP get_stock_bars", text)


if __name__ == "__main__":
    unittest.main()
