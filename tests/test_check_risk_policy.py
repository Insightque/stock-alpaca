from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "check-risk-policy.py"

spec = importlib.util.spec_from_file_location("check_risk_policy", SCRIPT_PATH)
assert spec and spec.loader
check_risk_policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_risk_policy)


def base_plan() -> dict:
    return {
        "run_id": "test-run",
        "schema_version": "1.2",
        "risk_policy_version": "medium-risk-v1.1",
        "recommendation_policy_sha": "sha256:" + "0" * 64,
        "created_at": "2026-05-22T12:30:00Z",
        "mode": "dry_run",
        "paper": True,
        "market": {
            "is_open": False,
            "checked_at": "2026-05-22T12:30:00Z",
        },
        "account": {
            "portfolio_value": 100000.0,
            "cash": 100000.0,
            "buying_power": 100000.0,
            "currency": "USD",
        },
        "positions": [],
        "risk_inputs": {
            "policy_turnover_ratio": 0.05,
            "weekly_turnover_ratio": 0.10,
            "stop_triggered_orders_today": 0,
            "new_orders_submitted_today": 0,
            "risk_recomputed_after_partial_fill": True,
        },
        "orders": [
            {
                "symbol": "SPY",
                "asset_type": "etf",
                "asset_status": "active",
                "asset_tradable": True,
                "side": "buy",
                "order_type": "limit",
                "time_in_force": "day",
                "qty": 10,
                "limit_price": 500.0,
                "reference_price": 500.0,
                "quote_age_minutes": 5,
                "quote_captured_at": "2026-05-22T12:25:00Z",
                "asset_checked_at": "2026-05-22T12:24:30Z",
                "theme": "broad_market",
                "factor": "broad_index",
                "volatility_bucket": "low",
                "speculative_flag": False,
                "liquidity_bucket": "mega",
                "source_confidence": "high",
                "correlated_cluster": "broad_index",
                "strategy_id": "long-term-quality-momentum-v1",
                "strategy_version": "1.0",
                "policy_status": "active_dry_run_candidate",
                "expected_excess_return_20d_pct": 3.0,
                "expected_adverse_move_20d_pct": -4.0,
                "confidence_score": 0.75,
                "sizing_basis": "test sizing basis",
                "entry_style": "staged",
                "max_additional_entry_count": 2,
                "liquidity": {
                    "bid": 499.95,
                    "ask": 500.05,
                    "spread_pct": 0.02,
                    "avg_daily_dollar_volume": 20000000000,
                    "quote_source": "alpaca",
                    "measured_at": "2026-05-22T12:25:00Z",
                },
                "client_order_id": "test-run-spy-buy",
                "decision_id": "test-run-spy-decision",
                "source_refs": ["wiki/evidence-store/sources/test-market.md"],
                "rationale": "test order",
            }
        ],
        "source_refs": ["wiki/evidence-store/sources/test-clock.md"],
    }


def position(symbol: str, market_value: float, qty: int = 10) -> dict:
    metadata = check_risk_policy.load_symbol_metadata(check_risk_policy.load_policy())[symbol]
    return {
        "symbol": symbol,
        "asset_type": "etf" if symbol in {"SPY", "QQQ", "SMH"} else "stock",
        "qty": qty,
        "market_value": market_value,
        "theme": metadata["theme"],
        "factor": metadata["factor"],
        "volatility_bucket": metadata["volatility_bucket"],
        "speculative_flag": metadata["speculative_flag"],
        "liquidity_bucket": metadata["liquidity_bucket"],
        "source_confidence": metadata["source_confidence"],
        "correlated_cluster": metadata["correlated_cluster"],
    }


class RiskPolicyTests(unittest.TestCase):
    def validate(self, plan: dict) -> tuple[list[str], list[str], dict]:
        return check_risk_policy.validate(plan)

    def test_example_order_plan_passes(self) -> None:
        plan = json.loads((ROOT / "harness" / "examples" / "order-plan.example.json").read_text())
        errors, warnings, summary = self.validate(plan)
        self.assertEqual([], errors)
        self.assertEqual("medium-risk-v1.1", summary["policy_version"])
        self.assertEqual([], warnings)

    def test_sell_diagnostics_and_lifecycle_metadata_are_schema_allowed(self) -> None:
        plan = base_plan()
        plan["sell_candidate_diagnostics"] = [
            {
                "symbol": "SPY",
                "held_qty": 1,
                "current_weight_pct": 0.5,
                "trigger_status": "no_trigger",
                "primary_reason": "risk trim trigger not active",
                "skipped_gate": "",
                "expected_excess_return_20d_pct": 1.0,
                "relative_to_spy_20d_pct": 0.0,
                "replacement_symbol": "QQQ",
                "replacement_confidence_score": 0.6,
                "recommendation": "hold",
                "source_refs": ["wiki/evidence-store/sources/test-market.md"],
            }
        ]
        plan["validation_lifecycle"] = {
            "due_reviews": [
                {
                    "symbol": "SPY",
                    "horizon": "1D",
                    "decision_due": True,
                    "current_decision": "pending",
                    "source_refs": ["wiki/trade-ledger/orders/test-run.json"],
                }
            ],
            "blocked_add_symbols": ["SPY"],
        }
        errors, warnings, _ = self.validate(plan)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_invested_and_cash_boundary_passes(self) -> None:
        plan = base_plan()
        plan["account"]["cash"] = 35000.0
        plan["account"]["buying_power"] = 35000.0
        plan["positions"] = [
            position("AAPL", 13000.0),
            position("MSFT", 13000.0),
            position("NVDA", 13000.0),
            position("QQQ", 13000.0),
            position("UNH", 13000.0),
        ]
        plan["orders"][0]["qty"] = 30
        errors, _, summary = self.validate(plan)
        self.assertEqual([], errors)
        self.assertEqual(20000.0, summary["post_cash"])
        self.assertEqual(80000.0, summary["post_invested"])

    def test_account_implied_invested_exposure_requires_positions(self) -> None:
        plan = base_plan()
        plan["account"]["cash"] = 35000.0
        plan["account"]["buying_power"] = 35000.0
        plan["orders"] = []
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("positions cannot be empty" in error for error in errors))

    def test_positions_must_reconcile_with_account_implied_invested_exposure(self) -> None:
        plan = base_plan()
        plan["account"]["cash"] = 35000.0
        plan["account"]["buying_power"] = 35000.0
        plan["positions"] = [position("AAPL", 10000.0)]
        plan["orders"] = []
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("does not reconcile with account-implied invested exposure" in error for error in errors))

    def test_cash_reserve_violation_fails(self) -> None:
        plan = base_plan()
        plan["orders"][0]["qty"] = 161
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("below required reserve" in error for error in errors))

    def test_per_ticker_violation_fails(self) -> None:
        plan = base_plan()
        plan["orders"][0]["qty"] = 31
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("per-ticker limit" in error for error in errors))

    def test_theme_exposure_violation_fails(self) -> None:
        plan = base_plan()
        plan["account"]["cash"] = 70000.0
        plan["account"]["buying_power"] = 70000.0
        plan["positions"] = [
            position("NVDA", 10000.0),
            position("AMD", 10000.0),
            position("TSM", 10000.0),
        ]
        plan["orders"][0]["symbol"] = "NVDA"
        plan["orders"][0]["asset_type"] = "stock"
        plan["orders"][0]["theme"] = "ai_semiconductor"
        plan["orders"][0]["factor"] = "ai_semiconductor"
        plan["orders"][0]["volatility_bucket"] = "high"
        plan["orders"][0]["correlated_cluster"] = "ai_semiconductor_complex"
        plan["orders"][0]["qty"] = 6
        plan["orders"][0]["limit_price"] = 1000.0
        plan["orders"][0]["reference_price"] = 1000.0
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("theme ai_semiconductor" in error for error in errors))

    def test_speculative_exposure_violation_fails(self) -> None:
        plan = base_plan()
        plan["orders"][0]["symbol"] = "RGTI"
        plan["orders"][0]["asset_type"] = "stock"
        plan["orders"][0]["theme"] = "quantum_speculative"
        plan["orders"][0]["factor"] = "speculative_growth"
        plan["orders"][0]["volatility_bucket"] = "high"
        plan["orders"][0]["speculative_flag"] = True
        plan["orders"][0]["liquidity_bucket"] = "medium"
        plan["orders"][0]["source_confidence"] = "medium"
        plan["orders"][0]["correlated_cluster"] = "quantum_speculative"
        plan["orders"][0]["qty"] = 13
        plan["orders"][0]["limit_price"] = 1000.0
        plan["orders"][0]["reference_price"] = 1000.0
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("speculative exposure" in error for error in errors))

    def test_submit_mode_stale_quote_fails(self) -> None:
        plan = base_plan()
        plan["mode"] = "submit"
        plan["market"]["is_open"] = True
        plan["market"]["checked_at"] = "2026-05-22T13:00:00Z"
        plan["orders"][0]["client_order_id"] = "test-submit-spy"
        plan["orders"][0]["quote_captured_at"] = "2026-05-22T12:30:00Z"
        plan["orders"][0]["quote_age_minutes"] = 30
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("quote data is 30.0 minutes old" in error for error in errors))

    def test_submit_mode_requires_client_order_id(self) -> None:
        plan = base_plan()
        plan["mode"] = "submit"
        plan["market"]["is_open"] = True
        del plan["orders"][0]["client_order_id"]
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("requires client_order_id" in error for error in errors))

    def test_dry_run_stale_quote_warns(self) -> None:
        plan = base_plan()
        plan["market"]["checked_at"] = "2026-05-22T13:00:00Z"
        plan["orders"][0]["quote_captured_at"] = "2026-05-22T12:30:00Z"
        plan["orders"][0]["quote_age_minutes"] = 30
        errors, warnings, _ = self.validate(plan)
        self.assertEqual([], errors)
        self.assertTrue(any("dry-run plans may keep stale quotes" in warning for warning in warnings))

    def test_sell_more_than_held_fails(self) -> None:
        plan = base_plan()
        plan["orders"][0]["side"] = "sell"
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("exceeds held qty" in error for error in errors))

    def test_buy_cannot_rely_on_same_run_sell_proceeds(self) -> None:
        plan = base_plan()
        plan["account"]["cash"] = 0.0
        plan["account"]["buying_power"] = 100000.0
        plan["positions"] = [position("AAPL", 50000.0, qty=200)]
        plan["orders"] = [
            {
                **copy.deepcopy(plan["orders"][0]),
                "symbol": "AAPL",
                "asset_type": "stock",
                "side": "sell",
                "qty": 100,
                "limit_price": 250.0,
                "reference_price": 250.0,
            },
            {
                **copy.deepcopy(plan["orders"][0]),
                "qty": 50,
                "client_order_id": "test-run-spy-buy-2",
                "decision_id": "test-run-spy-decision-2",
            },
        ]
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("do not rely on same-run sell proceeds" in error for error in errors))

    def test_bool_qty_rejected(self) -> None:
        plan = base_plan()
        plan["orders"][0]["qty"] = True
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("whole-share integer" in error or "True is not of type" in error for error in errors))

    def test_infinite_numbers_rejected(self) -> None:
        plan = base_plan()
        plan["orders"][0]["limit_price"] = float("inf")
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("must be finite" in error for error in errors))

    def test_schema_rejects_extra_properties(self) -> None:
        plan = base_plan()
        plan["orders"][0]["unexpected"] = "field"
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors))

    def test_duplicate_same_run_order_fails(self) -> None:
        plan = base_plan()
        plan["orders"].append(copy.deepcopy(plan["orders"][0]))
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("duplicate same-run order" in error for error in errors))

    def test_daily_new_order_cap_fails(self) -> None:
        plan = base_plan()
        plan["risk_inputs"]["new_orders_submitted_today"] = 20
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("daily capped new orders 21 exceeds limit 20" in error for error in errors))

    def test_sell_not_blocked_by_daily_new_buy_order_cap(self) -> None:
        plan = base_plan()
        plan["risk_inputs"]["new_orders_submitted_today"] = 20
        plan["positions"] = [position("SPY", 5000.0, qty=10)]
        plan["orders"][0]["side"] = "sell"
        plan["orders"][0]["entry_style"] = "trim"
        errors, _, summary = self.validate(plan)
        self.assertEqual([], errors)
        self.assertEqual(0.0, summary["buy_notional"])
        self.assertEqual(5000.0, summary["sell_notional"])

    def test_sell_exit_not_blocked_by_buy_quality_gates(self) -> None:
        plan = base_plan()
        plan["mode"] = "submit"
        plan["market"]["is_open"] = True
        plan["positions"] = [position("SPY", 5000.0, qty=10)]
        plan["orders"][0]["side"] = "sell"
        plan["orders"][0]["entry_style"] = "exit"
        plan["orders"][0]["policy_status"] = "rejected"
        plan["orders"][0]["source_confidence"] = "low"
        plan["orders"][0]["confidence_score"] = 0.1
        errors, _, summary = self.validate(plan)
        self.assertEqual([], errors)
        self.assertEqual(0.0, summary["buy_notional"])
        self.assertEqual(5000.0, summary["sell_notional"])

    def test_sell_requires_trim_or_exit_entry_style(self) -> None:
        plan = base_plan()
        plan["positions"] = [position("SPY", 5000.0, qty=10)]
        plan["orders"][0]["side"] = "sell"
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("sell orders require entry_style=trim or exit" in error for error in errors))

    def test_submit_mode_requires_daily_order_count(self) -> None:
        plan = base_plan()
        plan["mode"] = "submit"
        plan["market"]["is_open"] = True
        del plan["risk_inputs"]["new_orders_submitted_today"]
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("new_orders_submitted_today" in error for error in errors))

    def test_after_hours_submit_requires_separate_profile_and_extended_hours(self) -> None:
        plan = base_plan()
        plan["mode"] = "submit"
        plan["market"]["is_open"] = False
        plan["market"]["session"] = "after_hours"
        plan["risk_inputs"]["after_hours_new_orders_submitted_today"] = 0
        plan["orders"][0]["qty"] = 1
        plan["orders"][0]["policy_status"] = "auto_eligible_paper"
        plan["orders"][0]["session"] = "after_hours"
        plan["orders"][0]["extended_hours"] = True
        plan["orders"][0]["review_bucket"] = "after_hours_validation"
        plan["orders"][0]["quote_age_minutes"] = 1
        plan["orders"][0]["quote_captured_at"] = "2026-05-22T12:29:00Z"
        errors, _, _ = self.validate(plan)
        self.assertEqual([], errors)

    def test_after_hours_submit_rejects_regular_review_bucket_mixing(self) -> None:
        plan = base_plan()
        plan["mode"] = "submit"
        plan["market"]["session"] = "after_hours"
        plan["risk_inputs"]["after_hours_new_orders_submitted_today"] = 0
        plan["orders"][0]["policy_status"] = "auto_eligible_paper"
        plan["orders"][0]["session"] = "regular"
        plan["orders"][0]["extended_hours"] = False
        plan["orders"][0]["review_bucket"] = "regular_validation"
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("order session must match market.session=after_hours" in error for error in errors))
        self.assertTrue(any("after-hours orders require extended_hours=true" in error for error in errors))
        self.assertTrue(any("review_bucket must be after_hours_validation" in error for error in errors))

    def test_after_hours_submit_uses_separate_session_order_cap(self) -> None:
        plan = base_plan()
        plan["mode"] = "submit"
        plan["market"]["session"] = "after_hours"
        plan["risk_inputs"]["after_hours_new_orders_submitted_today"] = 2
        plan["orders"][0]["policy_status"] = "auto_eligible_paper"
        plan["orders"][0]["session"] = "after_hours"
        plan["orders"][0]["extended_hours"] = True
        plan["orders"][0]["review_bucket"] = "after_hours_validation"
        errors, _, _ = self.validate(plan)
        self.assertTrue(any("after-hours new orders 3 exceeds session limit 2" in error for error in errors))

    def test_cli_json_output(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--json", str(ROOT / "harness" / "examples" / "order-plan.example.json")],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        payload = json.loads(completed.stdout)
        self.assertEqual("PASS", payload["status"])
        self.assertEqual([], payload["errors"])


if __name__ == "__main__":
    unittest.main()
