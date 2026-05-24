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


if __name__ == "__main__":
    unittest.main()
