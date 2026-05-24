from __future__ import annotations

import unittest

from scripts.policy_simulation_lib import conservative_stop_take_exit


class IntradayStopTakeOrderingTests(unittest.TestCase):
    def test_same_bar_stop_and_take_uses_conservative_stop(self) -> None:
        exit_price, reason = conservative_stop_take_exit(entry=100, high=103, low=98, close=101, stop=99, take=102)
        self.assertEqual(99, exit_price)
        self.assertEqual("stop_before_take_conservative", reason)


if __name__ == "__main__":
    unittest.main()
