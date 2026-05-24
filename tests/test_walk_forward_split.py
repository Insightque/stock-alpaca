from __future__ import annotations

import unittest

from scripts.policy_simulation_lib import walk_forward_splits


class WalkForwardSplitTests(unittest.TestCase):
    def test_three_month_train_one_month_validation_rolls_monthly(self) -> None:
        dates = [
            "2025-01-31",
            "2025-02-28",
            "2025-03-31",
            "2025-04-30",
            "2025-05-30",
        ]
        windows = walk_forward_splits(dates, train_months=3, validation_months=1)
        self.assertEqual("2025-01-31", windows[0]["train_start"])
        self.assertEqual("2025-03-31", windows[0]["train_end"])
        self.assertEqual("2025-04-30", windows[0]["validation_start"])
        self.assertEqual("2025-04-30", windows[0]["validation_end"])
        self.assertEqual("2025-05-30", windows[1]["validation_start"])


if __name__ == "__main__":
    unittest.main()
