from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "simulate-policy-improvement-candidates.py"

spec = importlib.util.spec_from_file_location("simulate_policy_improvement_candidates", SCRIPT_PATH)
assert spec and spec.loader
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)


def row(day: str, close: float) -> dict:
    return {"date": day, "open": close, "high": close * 1.01, "low": close * 0.99, "close": close, "volume": 1000}


class BacktestAlignmentTests(unittest.TestCase):
    def test_missing_symbol_date_does_not_fall_back_to_row_index(self) -> None:
        dates = [f"2026-01-{day:02d}" for day in range(1, 46)]
        rows = {
            "SPY": [row(day, 100 + idx) for idx, day in enumerate(dates)],
            "QQQ": [row(day, 100 + idx) for idx, day in enumerate(dates)],
            "ABC": [row(day, 50 + idx) for idx, day in enumerate(dates) if day != "2026-01-41"],
        }
        indices = sim.build_daily_indices(rows)
        result = sim.candidate_features("ABC", "2026-01-41", rows, indices, {})
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
