import importlib.util
import json
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str, name: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AutopilotNotificationSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dashboard = load_module("scripts/build-agent-dashboard.py", "build_agent_dashboard")
        cls.notifier = load_module("scripts/send-openclaw-autopilot-update.py", "send_openclaw_autopilot_update")

    def test_dashboard_normalizes_string_risk_check_result(self):
        manifest = {
            "risk_check_result": "pass",
            "mcp_failures": [
                {
                    "server": "alpha-vantage",
                    "gap_category": "empty_response",
                    "gap_reason": "NEWS_SENTIMENT returned no candidate news items.",
                }
            ],
        }

        risk = self.dashboard.normalize_risk_check_result(manifest)
        self.assertEqual(risk["status"], "PASS")
        self.assertEqual(risk["warnings"], [])
        self.assertEqual(
            self.dashboard.mcp_failure_reasons(manifest),
            ["NEWS_SENTIMENT returned no candidate news items."],
        )

    def test_completed_message_handles_string_risk_check_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_id = "2026-05-29-0011-hourly-autopilot"
            (root / "wiki/current-runs/daily").mkdir(parents=True)
            (root / "wiki/trade-ledger/orders").mkdir(parents=True)
            (root / "wiki/evidence-store/run-manifests").mkdir(parents=True)
            (root / "wiki/evidence-store/sources").mkdir(parents=True)

            (root / "wiki/current-runs/daily" / f"{run_id}.md").write_text(
                "# run\n\nResult: SPY filled\n",
                encoding="utf-8",
            )
            (root / "wiki/trade-ledger/orders" / f"{run_id}.json").write_text(
                json.dumps(
                    {
                        "mode": "submit",
                        "review_bucket": "regular_validation",
                        "account": {"portfolio_value": 1000.0, "cash": 200.0, "buying_power": 200.0},
                        "orders": [
                            {
                                "symbol": "SPY",
                                "side": "buy",
                                "qty": 1,
                                "limit_price": 753.38,
                                "extended_hours": False,
                                "client_order_id": "hourly-20260529-0011-spy-buy-01",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (root / "wiki/evidence-store/sources" / f"{run_id}-alpaca-core-preflight.json").write_text(
                json.dumps(
                    {
                        "tool_results": {
                            "get_account_info": {
                                "payload": {
                                    "portfolio_value": "1000.0",
                                    "cash": "200.0",
                                    "buying_power": "200.0",
                                    "last_equity": "990.0",
                                }
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            (root / "wiki/evidence-store/run-manifests" / f"{run_id}.json").write_text(
                json.dumps(
                    {
                        "run_id": run_id,
                        "risk_check_result": "pass",
                        "mcp_failures": [
                            {
                                "server": "alpha-vantage",
                                "gap_category": "empty_response",
                                "gap_reason": "empty news response",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            message = self.notifier.build_completed_message(root, run_id, "regular")

        self.assertTrue(message.startswith("[STOCK-TRAIN] 2026-05-29 00:11 KST | regular 완료"))
        self.assertLessEqual(len(message.splitlines()), 20)
        self.assertIn("💰 Portfolio", message)
        self.assertIn("🟢 Buy (1)", message)
        self.assertIn("SPY | $753", message)
        self.assertIn("🔴 Sell (0)", message)
        self.assertIn("alpha-vantage:empty_response", message)
        self.assertIn("당일손익: $10 (+1.0%)", message)
        self.assertNotIn("당일손익 데이터 없음", message)


if __name__ == "__main__":
    unittest.main()
