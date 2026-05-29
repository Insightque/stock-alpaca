from __future__ import annotations

import argparse
import importlib.util
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "evaluate-intraday-dry-run.py"
SPEC = importlib.util.spec_from_file_location("evaluate_intraday_dry_run", MODULE_PATH)
assert SPEC and SPEC.loader
intraday = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = intraday
SPEC.loader.exec_module(intraday)


class EvaluateIntradayDryRunTests(unittest.TestCase):
    def bar(self, minute: str, open_price: float, high: float, low: float, close: float):
        return intraday.Bar(
            ts=datetime.fromisoformat(f"2026-05-28T{minute}:00-04:00"),
            open=open_price,
            high=high,
            low=low,
            close=close,
            volume=1000,
        )

    def test_time_stop_exits_before_late_eod_gain(self) -> None:
        entry = self.bar("11:00", 100.0, 100.2, 99.8, 100.1)
        bars = [
            entry,
            self.bar("12:20", 100.5, 100.6, 100.2, 100.5),
            self.bar("15:59", 110.0, 110.0, 109.8, 110.0),
        ]

        outcome, pl_pct, exit_price = intraday.theoretical_outcome(
            bars,
            entry,
            time_stop_minutes=80,
        )

        self.assertEqual("time_stop_gain", outcome)
        self.assertAlmostEqual(0.5, pl_pct)
        self.assertEqual(100.5, exit_price)

    def test_stop_takes_precedence_before_time_stop(self) -> None:
        entry = self.bar("11:00", 100.0, 100.2, 99.8, 100.1)
        bars = [
            entry,
            self.bar("11:10", 100.0, 100.1, 98.9, 99.0),
            self.bar("12:20", 101.0, 101.0, 100.8, 101.0),
        ]

        outcome, pl_pct, exit_price = intraday.theoretical_outcome(
            bars,
            entry,
            time_stop_minutes=80,
        )

        self.assertEqual("stop", outcome)
        self.assertEqual(-1.0, pl_pct)
        self.assertEqual(99.0, exit_price)

    def test_strategy_config_exit_rules_override_defaults(self) -> None:
        args = argparse.Namespace(
            strategy_config=None,
            take_profit_pct=2.0,
            stop_loss_pct=1.0,
            time_stop_minutes=None,
            fallback_exit_time_et="15:59",
        )
        with tempfile.NamedTemporaryFile("w", suffix=".yaml") as handle:
            handle.write(
                "exit_rules:\n"
                "  take_profit_pct: 1.5\n"
                "  stop_loss_pct: 0.8\n"
                "  time_stop_minutes: 80\n"
                "  fallback_exit_time_et: \"15:55\"\n"
            )
            handle.flush()
            args.strategy_config = handle.name
            intraday.apply_strategy_exit_rules(args)

        self.assertEqual(1.5, args.take_profit_pct)
        self.assertEqual(0.8, args.stop_loss_pct)
        self.assertEqual(80, args.time_stop_minutes)
        self.assertEqual("15:55", args.fallback_exit_time_et)


if __name__ == "__main__":
    unittest.main()
