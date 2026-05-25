import importlib.util
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
MODULE_PATH = SCRIPT_DIR / "simulate-one-year-daily-policy.py"
sys.path.insert(0, str(SCRIPT_DIR))

spec = importlib.util.spec_from_file_location("simulate_one_year_daily_policy", MODULE_PATH)
simulate_one_year = importlib.util.module_from_spec(spec)
sys.modules["simulate_one_year_daily_policy"] = simulate_one_year
assert spec.loader is not None
spec.loader.exec_module(simulate_one_year)


def rows_for(symbol: str, start_close: float, step: float) -> list[dict[str, float | str]]:
    start = date(2026, 1, 1)
    rows = []
    for offset in range(70):
        close = start_close + step * offset
        rows.append(
            {
                "date": (start + timedelta(days=offset)).isoformat(),
                "open": close - 0.2,
                "high": close + 0.5,
                "low": close - 0.5,
                "close": close,
                "volume": 1_000_000,
            }
        )
    return rows


class OneYearEventFeaturesTest(unittest.TestCase):
    def test_event_feature_join_uses_latest_point_in_time_record(self):
        rows = {
            "SPY": rows_for("SPY", 100.0, 0.05),
            "QQQ": rows_for("QQQ", 100.0, 0.05),
            "AAA": rows_for("AAA", 100.0, 1.0),
        }
        indices = simulate_one_year.build_indices(rows)
        metadata = {
            "defaults": {
                "theme": "test",
                "factor": "test",
                "volatility_bucket": "medium",
                "speculative_flag": False,
                "liquidity_bucket": "large",
                "source_confidence": "medium",
                "correlated_cluster": "test",
            },
            "symbols": {},
        }
        event_features = simulate_one_year.normalize_event_features(
            {
                "features": {
                    "AAA": {
                        "2026-02-10": {
                            "available_at": "2026-02-10T20:00:00Z",
                            "mcp_servers_used": ["sec-edgar", "alpha-vantage"],
                            "source_refs": ["wiki/evidence-store/sources/test.md"],
                            "score_adjustment": 2.5,
                            "source_confidence_delta": 0.1,
                        },
                        "2026-04-01": {
                            "available_at": "2026-04-01T20:00:00Z",
                            "mcp_servers_used": ["fred"],
                            "score_adjustment": -99.0,
                        },
                    }
                }
            }
        )

        features = simulate_one_year.candidate_features(
            "AAA",
            "2026-03-06",
            rows,
            indices,
            metadata,
            event_features,
        )

        assert features is not None
        self.assertTrue(features["event_feature_present"])
        self.assertEqual(features["event_available_date"], "2026-02-10")
        self.assertEqual(features["event_score_adjustment"], 2.5)
        self.assertEqual(features["mcp_servers_used"], ["sec-edgar", "alpha-vantage"])
        self.assertAlmostEqual(features["source_confidence_score"], 0.75)

    def test_event_exclude_blocks_candidate(self):
        row = {
            "event_exclude": True,
            "spy_excess20": 10.0,
            "qqq_excess20": 10.0,
            "ret40": 10.0,
            "vol20": 1.0,
            "drawdown60": -2.0,
            "ret20": 10.0,
            "ret5": 2.0,
            "source_confidence_score": 0.8,
            "avg_daily_dollar_volume": 100_000_000,
            "mcp_gap_count": 0,
        }
        self.assertFalse(simulate_one_year.passes_filters(row, {"filters": {}}))


if __name__ == "__main__":
    unittest.main()
