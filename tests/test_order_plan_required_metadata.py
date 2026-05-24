from __future__ import annotations

import copy
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


class OrderPlanRequiredMetadataTests(unittest.TestCase):
    def test_missing_order_exposure_metadata_fails_schema(self) -> None:
        plan = test_helpers.base_plan()
        del plan["orders"][0]["theme"]
        errors, _, _ = check_risk_policy.validate(plan)
        self.assertTrue(any("'theme' is a required property" in error for error in errors))

    def test_missing_liquidity_object_fails_schema(self) -> None:
        plan = test_helpers.base_plan()
        del plan["orders"][0]["liquidity"]
        errors, _, _ = check_risk_policy.validate(plan)
        self.assertTrue(any("'liquidity' is a required property" in error for error in errors))

    def test_duplicate_decision_id_fails(self) -> None:
        plan = test_helpers.base_plan()
        second = copy.deepcopy(plan["orders"][0])
        second["symbol"] = "QQQ"
        second["client_order_id"] = "test-run-qqq-buy"
        plan["orders"].append(second)
        errors, _, _ = check_risk_policy.validate(plan)
        self.assertTrue(any("duplicate decision_id" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
