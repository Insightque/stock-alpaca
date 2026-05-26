import importlib.util
from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "cancel-stale-autopilot-orders.py"
spec = importlib.util.spec_from_file_location("cancel_stale_autopilot_orders", MODULE_PATH)
cancel_stale_autopilot_orders = importlib.util.module_from_spec(spec)
sys.modules["cancel_stale_autopilot_orders"] = cancel_stale_autopilot_orders
assert spec.loader is not None
spec.loader.exec_module(cancel_stale_autopilot_orders)


class CancelStaleAutopilotOrdersTests(unittest.TestCase):
    def test_selects_only_old_unfilled_autopilot_day_limit_orders(self):
        now = datetime(2026, 5, 26, 20, 0, tzinfo=timezone.utc)
        orders = [
            {
                "id": "old-auto",
                "client_order_id": "hourly-20260527-0411-amzn-buy-1",
                "symbol": "AMZN",
                "asset_class": "us_equity",
                "type": "limit",
                "time_in_force": "day",
                "filled_qty": "0",
                "status": "new",
                "submitted_at": "2026-05-26T19:19:00Z",
            },
            {
                "id": "fresh-auto",
                "client_order_id": "hourly-20260527-0451-intc-buy-1",
                "symbol": "INTC",
                "asset_class": "us_equity",
                "type": "limit",
                "time_in_force": "day",
                "filled_qty": "0",
                "status": "new",
                "submitted_at": "2026-05-26T19:45:00Z",
            },
            {
                "id": "manual-old",
                "client_order_id": "manual-order",
                "symbol": "AAPL",
                "asset_class": "us_equity",
                "type": "limit",
                "time_in_force": "day",
                "filled_qty": "0",
                "status": "new",
                "submitted_at": "2026-05-26T19:00:00Z",
            },
            {
                "id": "partial-old",
                "client_order_id": "hourly-20260527-0411-msft-buy-1",
                "symbol": "MSFT",
                "asset_class": "us_equity",
                "type": "limit",
                "time_in_force": "day",
                "filled_qty": "0.5",
                "status": "partially_filled",
                "submitted_at": "2026-05-26T19:00:00Z",
            },
        ]

        stale = cancel_stale_autopilot_orders.stale_autopilot_orders(
            orders,
            now=now,
            max_age_minutes=30,
        )

        self.assertEqual([row["id"] for row in stale], ["old-auto"])
        self.assertEqual(stale[0]["symbol"], "AMZN")


if __name__ == "__main__":
    unittest.main()
