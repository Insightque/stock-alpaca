from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "check-risk-policy.py"
TEST_RISK = ROOT / "tests" / "test_check_risk_policy.py"

spec = importlib.util.spec_from_file_location("check_risk_policy", SCRIPT_PATH)
assert spec and spec.loader
check_risk_policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_risk_policy)

test_spec = importlib.util.spec_from_file_location("test_check_risk_policy_helpers", TEST_RISK)
assert test_spec and test_spec.loader
test_helpers = importlib.util.module_from_spec(test_spec)
test_spec.loader.exec_module(test_helpers)


class RiskPolicyLiquidityTests(unittest.TestCase):
    def test_wide_spread_fails(self) -> None:
        plan = test_helpers.base_plan()
        plan["orders"][0]["liquidity"]["spread_pct"] = 0.75
        errors, _, _ = check_risk_policy.validate(plan)
        self.assertTrue(any("spread_pct" in error and "exceeds maximum" in error for error in errors))

    def test_low_average_dollar_volume_fails(self) -> None:
        plan = test_helpers.base_plan()
        plan["orders"][0]["liquidity"]["avg_daily_dollar_volume"] = 1000000
        errors, _, _ = check_risk_policy.validate(plan)
        self.assertTrue(any("avg daily dollar volume" in error for error in errors))

    def test_low_source_confidence_fails(self) -> None:
        plan = test_helpers.base_plan()
        plan["orders"][0]["source_confidence"] = "low"
        plan["orders"][0]["confidence_score"] = 0.49
        errors, _, _ = check_risk_policy.validate(plan)
        self.assertTrue(any("source_confidence=low" in error for error in errors))
        self.assertTrue(any("confidence_score" in error for error in errors))

    def test_observation_only_policy_cannot_create_order(self) -> None:
        plan = test_helpers.base_plan()
        plan["orders"][0]["policy_status"] = "observation_only"
        errors, _, _ = check_risk_policy.validate(plan)
        self.assertTrue(any("observation_only cannot create" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
