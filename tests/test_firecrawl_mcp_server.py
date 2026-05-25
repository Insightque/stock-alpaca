import importlib.util
import json
import sys
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "firecrawl-mcp-server.py"

spec = importlib.util.spec_from_file_location("firecrawl_mcp_server", MODULE_PATH)
firecrawl_mcp_server = importlib.util.module_from_spec(spec)
sys.modules["firecrawl_mcp_server"] = firecrawl_mcp_server
assert spec.loader is not None
spec.loader.exec_module(firecrawl_mcp_server)


class FirecrawlMcpServerTest(unittest.TestCase):
    def test_tools_list_exposes_firecrawl_tools(self):
        response = firecrawl_mcp_server.handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})

        tool_names = {tool["name"] for tool in response["result"]["tools"]}
        self.assertIn("firecrawl_scrape", tool_names)
        self.assertIn("firecrawl_map", tool_names)

    def test_message_framing_round_trip(self):
        stream = BytesIO()
        payload = {"jsonrpc": "2.0", "id": 7, "result": {"ok": True}}

        firecrawl_mcp_server.write_message(stream, payload)
        stream.seek(0)

        self.assertEqual(firecrawl_mcp_server.read_message(stream), payload)

    def test_scrape_uses_clean_payload(self):
        def fake_firecrawl_post(endpoint, body):
            self.assertEqual(endpoint, "scrape")
            self.assertEqual(body["url"], "https://example.com")
            self.assertEqual(body["formats"], ["markdown"])
            self.assertTrue(body["onlyMainContent"])
            self.assertEqual(body["maxAge"], 3600000)
            return {"success": True, "data": {"markdown": "Example Domain"}}

        with patch.object(firecrawl_mcp_server, "firecrawl_post", side_effect=fake_firecrawl_post):
            result = firecrawl_mcp_server.firecrawl_scrape(
                {
                    "url": "https://example.com",
                    "formats": ["markdown"],
                    "onlyMainContent": True,
                    "maxAge": 3600000,
                }
            )

        self.assertTrue(result["success"])

    def test_tool_call_returns_mcp_content(self):
        original_handler = firecrawl_mcp_server.TOOLS["firecrawl_scrape"]["handler"]
        firecrawl_mcp_server.TOOLS["firecrawl_scrape"]["handler"] = lambda arguments: {
            "success": True,
            "data": {"markdown": "Example Domain"},
        }
        try:
            response = firecrawl_mcp_server.handle_request(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {"name": "firecrawl_scrape", "arguments": {"url": "https://example.com"}},
                }
            )
        finally:
            firecrawl_mcp_server.TOOLS["firecrawl_scrape"]["handler"] = original_handler

        self.assertFalse(response["result"]["isError"])
        text = response["result"]["content"][0]["text"]
        self.assertTrue(json.loads(text)["success"])


if __name__ == "__main__":
    unittest.main()
