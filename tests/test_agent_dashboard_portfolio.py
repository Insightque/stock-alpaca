import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_dashboard_module():
    path = ROOT / "scripts" / "build-agent-dashboard.py"
    spec = importlib.util.spec_from_file_location("build_agent_dashboard", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AgentDashboardPortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_dashboard_module()

    def test_portfolio_snapshot_reads_current_positions(self):
        portfolio = self.module.portfolio_snapshot()
        self.assertEqual(portfolio["positions_count"], 10)
        self.assertIn("USD", portfolio["portfolio_value"])
        self.assertGreater(portfolio["exposure_ratio"], 50.0)
        self.assertGreater(portfolio["cash_ratio"], 40.0)
        self.assertEqual(portfolio["positions"][0]["symbol"], "NVDA")

    def test_dashboard_run_metrics_fall_back_to_portfolio_snapshot(self):
        data = self.module.build_dashboard_data()
        self.assertIn("portfolio", data)
        self.assertGreater(data["run"]["invested_ratio"], 50.0)
        self.assertGreater(data["run"]["cash_ratio"], 40.0)


if __name__ == "__main__":
    unittest.main()
