from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


class StrategyConfigSchemaTests(unittest.TestCase):
    def test_strategy_configs_validate(self) -> None:
        schema = json.loads((ROOT / "harness" / "strategy-config.schema.json").read_text())
        validator = Draft202012Validator(schema)
        for path in (ROOT / "harness" / "strategies").glob("*.yaml"):
            config = yaml.safe_load(path.read_text(encoding="utf-8"))
            errors = sorted(validator.iter_errors(config), key=lambda error: list(error.absolute_path))
            self.assertEqual([], [error.message for error in errors], path.name)

    def test_recommendation_policy_yaml_validates(self) -> None:
        schema = json.loads((ROOT / "harness" / "recommendation-policy.schema.json").read_text())
        policy = yaml.safe_load((ROOT / "harness" / "recommendation-policy.yaml").read_text(encoding="utf-8"))
        errors = sorted(Draft202012Validator(schema).iter_errors(policy), key=lambda error: list(error.absolute_path))
        self.assertEqual([], [error.message for error in errors])

    def test_recommendation_policy_active_paper_validation_settings(self) -> None:
        policy = yaml.safe_load((ROOT / "harness" / "recommendation-policy.yaml").read_text(encoding="utf-8"))

        long_term = policy["strategy_status"]["long_term_quality_momentum_v1"]
        self.assertEqual("auto_eligible_paper", long_term["status"])
        self.assertTrue(long_term["auto_orders_allowed"])

        cadence = policy["cadence_policy"]
        self.assertEqual(20, cadence["scheduled_interval_minutes"])
        self.assertTrue(cadence["market_hours_only"])
        self.assertTrue(cadence["alpaca_clock_preflight_required"])
        self.assertEqual([11, 31, 51], cadence["launchd_minutes"])
        self.assertEqual([22, 23, 0, 1, 2, 3, 4, 5], cadence["launchd_hour_window_kst"])
        self.assertEqual("exit_before_research_preflight_or_codex", cadence["off_market_behavior"])

        sizing = policy["paper_validation_execution"]["validation_order_sizing"]
        self.assertEqual(3, sizing["max_new_buy_orders_per_run"])
        self.assertEqual(0.06, sizing["max_validation_notional_pct_per_day"])
        self.assertTrue(sizing["allow_multiple_candidates_per_run"])


if __name__ == "__main__":
    unittest.main()
