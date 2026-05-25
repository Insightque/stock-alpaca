import importlib.util
import json
import sys
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "fred-mcp-server.py"

spec = importlib.util.spec_from_file_location("fred_mcp_server", MODULE_PATH)
fred_mcp_server = importlib.util.module_from_spec(spec)
sys.modules["fred_mcp_server"] = fred_mcp_server
assert spec.loader is not None
spec.loader.exec_module(fred_mcp_server)


class FredMcpServerTest(unittest.TestCase):
    def test_tools_list_exposes_macro_tools(self):
        response = fred_mcp_server.handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})

        self.assertEqual(response["result"]["tools"][0]["name"], "get_series_observations")
        tool_names = {tool["name"] for tool in response["result"]["tools"]}
        self.assertIn("get_macro_snapshot", tool_names)
        self.assertIn("search_series", tool_names)

    def test_message_framing_round_trip(self):
        stream = BytesIO()
        payload = {"jsonrpc": "2.0", "id": 7, "result": {"ok": True}}

        fred_mcp_server.write_message(stream, payload)
        stream.seek(0)

        self.assertEqual(fred_mcp_server.read_message(stream), payload)

    def test_series_observations_uses_clean_params(self):
        def fake_fred_get(endpoint, params):
            self.assertEqual(endpoint, "series/observations")
            self.assertEqual(params["series_id"], "DGS10")
            self.assertEqual(params["limit"], 1)
            self.assertEqual(params["sort_order"], "desc")
            self.assertEqual(params["observation_end"], "2026-05-21")
            return {"observations": [{"date": "2026-05-21", "value": "4.53"}]}

        with patch.object(fred_mcp_server, "fred_get", side_effect=fake_fred_get):
            result = fred_mcp_server.get_series_observations(
                {"series_id": "dgs10", "limit": 1, "observation_end": "2026-05-21"}
            )

        self.assertEqual(result["series_id"], "DGS10")
        self.assertEqual(result["observations"][0]["value"], "4.53")

    def test_tool_call_returns_mcp_content(self):
        original_handler = fred_mcp_server.TOOLS["get_series_info"]["handler"]
        fred_mcp_server.TOOLS["get_series_info"]["handler"] = lambda arguments: {
            "series_id": "DGS10",
            "seriess": [{"id": "DGS10"}],
        }
        try:
            response = fred_mcp_server.handle_request(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {"name": "get_series_info", "arguments": {"series_id": "DGS10"}},
                }
            )
        finally:
            fred_mcp_server.TOOLS["get_series_info"]["handler"] = original_handler

        self.assertFalse(response["result"]["isError"])
        text = response["result"]["content"][0]["text"]
        self.assertEqual(json.loads(text)["series_id"], "DGS10")


if __name__ == "__main__":
    unittest.main()
