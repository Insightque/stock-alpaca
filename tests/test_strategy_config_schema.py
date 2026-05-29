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

    def test_intraday_exit_rules_are_explicit(self) -> None:
        for name in ("intraday-rs-breakout-v0.yaml", "intraday-rs-breadth-vwap-v1.yaml"):
            config = yaml.safe_load((ROOT / "harness" / "strategies" / name).read_text(encoding="utf-8"))
            self.assertEqual(2.0, config["exit_rules"]["take_profit_pct"])
            self.assertEqual(1.0, config["exit_rules"]["stop_loss_pct"])
            self.assertEqual("eod", config["exit_rules"]["fallback_exit"])
            self.assertEqual("15:59", config["exit_rules"]["fallback_exit_time_et"])
            self.assertNotIn("time_stop_minutes", config["exit_rules"])

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
        self.assertEqual("staged_confidence_notional", sizing["allocation_mode"])
        self.assertEqual(5, sizing["max_new_buy_orders_per_run"])
        self.assertEqual(0.10, sizing["max_validation_notional_pct_per_day"])
        self.assertTrue(sizing["allow_multiple_candidates_per_run"])
        self.assertEqual(0.25, sizing["cash_ratio_floor_for_additional_orders"])
        self.assertEqual(0.80, sizing["target_exposure_path"]["max_policy_target_ratio"])
        self.assertEqual(0.75, sizing["target_exposure_path"]["prefer_rebalance_over_new_buy_above_ratio"])
        self.assertTrue(sizing["open_order_policy"]["allow_different_cluster_new_buy_when_open_orders_are_fresh"])
        self.assertEqual(6, sizing["confidence_tiers"][-1]["max_qty"])

        risk_trim = policy["risk_trim_policy"]
        self.assertEqual("before_new_buys", risk_trim["evaluation_order"])
        self.assertTrue(risk_trim["decouple_from_buy_entry_window"])
        self.assertTrue(risk_trim["decouple_from_buy_budget"])
        self.assertTrue(risk_trim["sell_candidate_diagnostics"]["enabled"])
        self.assertEqual(3, risk_trim["sell_candidate_diagnostics"]["top_n"])
        self.assertTrue(risk_trim["validation_lifecycle"]["enabled"])
        self.assertEqual(["hold", "add", "trim", "close"], risk_trim["validation_lifecycle"]["required_decisions"])
        self.assertTrue(risk_trim["rotation_trim"]["enabled"])
        self.assertEqual("relative_opportunity_cost", risk_trim["rotation_trim"]["reason"])
        ai_theme = risk_trim["portfolio_target_bands"]["themes"]["ai_semiconductor"]
        self.assertEqual(0.25, ai_theme["target_ratio"])
        self.assertEqual(0.30, ai_theme["warning_ratio"])

        after_hours = policy["after_hours_policy"]
        self.assertTrue(after_hours["enabled_for_explicit_autopilot_runs"])
        self.assertFalse(after_hours["enabled_for_regular_hourly_autopilot"])
        self.assertEqual("after_hours", after_hours["session_name"])
        self.assertEqual("after_hours_validation", after_hours["review_bucket"])
        self.assertEqual(20, after_hours["cadence"]["scheduled_interval_minutes"])
        self.assertEqual([11, 31, 51], after_hours["cadence"]["launchd_minutes"])
        self.assertEqual(list(range(6, 22)), after_hours["cadence"]["launchd_hour_window_kst"])
        self.assertEqual("separate_lock_skip", after_hours["cadence"]["overlap_behavior"])
        self.assertTrue(after_hours["separate_from_regular_validation"])
        self.assertTrue(after_hours["require_extended_hours_flag"])
        self.assertTrue(after_hours["require_separate_order_budget"])

    def test_order_caps_match_strategic_allocation_policy(self) -> None:
        risk_policy = yaml.safe_load((ROOT / "harness" / "risk-policy.yaml").read_text(encoding="utf-8"))
        order_plan_schema = json.loads((ROOT / "harness" / "order-plan.schema.json").read_text())

        self.assertEqual(20, risk_policy["order_limits"]["max_orders_per_run"])
        self.assertEqual(20, risk_policy["daily_limits"]["max_new_orders_per_day"])
        self.assertEqual(20, order_plan_schema["properties"]["orders"]["maxItems"])


if __name__ == "__main__":
    unittest.main()
