from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "check-leakage.py"

spec = importlib.util.spec_from_file_location("check_leakage", SCRIPT_PATH)
assert spec and spec.loader
check_leakage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_leakage)


class LeakageCheckerTests(unittest.TestCase):
    def test_future_date_in_simulation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "2026-05-08-historical-decision.md"
            path.write_text(
                "historical_asof: 2026-05-08T20:00:00Z\n"
                "추천 근거는 2026-05-08 기준이다.\n"
                "미래 뉴스 2026-05-11 이 섞이면 안 된다.\n",
                encoding="utf-8",
            )
            errors, asof = check_leakage.check_file(path, None)
        self.assertIsNotNone(asof)
        self.assertTrue(any("after as-of" in error for error in errors))

    def test_review_horizon_dates_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "2026-05-08-historical-decision.md"
            path.write_text(
                "historical_asof: 2026-05-08T20:00:00Z\n"
                "review_horizons: 1D 2026-05-11, 5D 2026-05-15\n",
                encoding="utf-8",
            )
            errors, _ = check_leakage.check_file(path, None)
        self.assertEqual([], errors)

    def test_review_only_phrase_in_simulation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "2026-05-08-historical-decision.md"
            path.write_text(
                "historical_asof: 2026-05-08T20:00:00Z\n"
                "actual_return: +3.0%\n",
                encoding="utf-8",
            )
            errors, _ = check_leakage.check_file(path, None)
        self.assertTrue(any("review-only" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
