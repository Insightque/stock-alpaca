from __future__ import annotations

import unittest

from scripts.policy_simulation_lib import apply_round_trip_cost


class CostModelTests(unittest.TestCase):
    def test_round_trip_cost_subtracts_bps(self) -> None:
        result = apply_round_trip_cost(5.0, {"slippage_bps": 10, "spread_bps": 5, "fee_bps": 0})
        self.assertAlmostEqual(4.75, result)


if __name__ == "__main__":
    unittest.main()
