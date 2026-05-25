import importlib.util
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
MODULE_PATH = SCRIPT_DIR / "simulate-one-year-hourly-buy-sell.py"
sys.path.insert(0, str(SCRIPT_DIR))

spec = importlib.util.spec_from_file_location("simulate_one_year_hourly_buy_sell", MODULE_PATH)
simulate_hourly = importlib.util.module_from_spec(spec)
sys.modules["simulate_one_year_hourly_buy_sell"] = simulate_hourly
assert spec.loader is not None
spec.loader.exec_module(simulate_hourly)


def hourly_rows(start_close: float, step: float, days: int = 90) -> list[dict]:
    start = date(2026, 1, 1)
    rows = []
    for offset in range(days):
        day = start + timedelta(days=offset)
        base = start_close + step * offset
        first_open = base - 0.2
        first_close = base
        second_close = base + step * 0.25
        rows.extend(
            [
                {
                    "timestamp": f"{day.isoformat()}T14:30:00Z",
                    "open": first_open,
                    "high": first_close + 0.4,
                    "low": first_open - 0.4,
                    "close": first_close,
                    "volume": 1_000_000,
                    "vwap": first_close,
                },
                {
                    "timestamp": f"{day.isoformat()}T15:30:00Z",
                    "open": first_close,
                    "high": second_close + 0.4,
                    "low": min(first_close, second_close) - 0.4,
                    "close": second_close,
                    "volume": 1_000_000,
                    "vwap": second_close,
                },
            ]
        )
    return rows


class OneYearHourlyBuySellTest(unittest.TestCase):
    def test_simulation_records_buy_sell_independent_runs_and_horizons(self):
        raw = {
            "SPY": hourly_rows(100.0, 0.1),
            "QQQ": hourly_rows(100.0, 0.1),
            "AAA": hourly_rows(80.0, 1.0),
            "BBB": hourly_rows(120.0, -0.3),
        }
        hourly_by_day = simulate_hourly.build_hourly_by_day(raw)
        daily = simulate_hourly.aggregate_daily(hourly_by_day)
        config = {
            "benchmarks": ["SPY", "QQQ"],
            "cost_model": {"slippage_bps": 10, "spread_bps": 5, "fee_bps": 0},
            "filters": {
                "min_avg_daily_dollar_volume": 50_000_000,
                "max_vol20": 20,
                "min_source_confidence_score": 0.5,
            },
            "selection": {"top_n": 1, "theme_cap": 1},
        }
        metadata = {
            "defaults": {
                "theme": "test",
                "factor": "test",
                "volatility_bucket": "medium",
                "speculative_flag": False,
                "liquidity_bucket": "large",
                "source_confidence": "high",
                "correlated_cluster": "test",
            },
            "symbols": {},
        }

        result = simulate_hourly.simulate(hourly_by_day, daily, config, metadata)
        recommendations = result["recommendations"]

        self.assertTrue(any(row["action"] == "virtual_buy" for row in recommendations))
        self.assertTrue(any(row["action"] == "virtual_sell" for row in recommendations))
        self.assertTrue(all(row["orders_submitted"] == 0 for row in recommendations))
        self.assertTrue(all(row["independent_run_id"] for row in recommendations))
        self.assertIn("20D", recommendations[0]["horizon_results"])
        self.assertEqual(
            recommendations[0]["position_effect"] in {"open_virtual_long", "sell_or_avoid_existing_long_only_no_short"},
            True,
        )


if __name__ == "__main__":
    unittest.main()
