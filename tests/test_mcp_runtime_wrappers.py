from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class McpRuntimeWrapperTests(unittest.TestCase):
    def test_uvx_wrappers_use_workspace_local_runtime_dirs(self):
        for relative_path in (
            "scripts/alpaca-mcp.sh",
            "scripts/mcp-alpha-vantage.sh",
            "scripts/mcp-sec-edgar.sh",
            "scripts/mcp-yahoo-finance.sh",
        ):
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
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


if __name__ == "__main__":
    unittest.main()
