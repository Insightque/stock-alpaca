import json
import plistlib
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class McpRuntimeWrapperTests(unittest.TestCase):
    def test_uvx_wrappers_use_workspace_local_runtime_dirs(self):
        for relative_path in (
            "scripts/alpaca-mcp.sh",
            "scripts/cancel-stale-autopilot-orders.py",
            "scripts/fetch-alpaca-core-preflight.py",
            "scripts/fetch-research-mcp-preflight.py",
            "scripts/mcp-alpha-vantage.sh",
            "scripts/mcp-sec-edgar.sh",
            "scripts/mcp-yahoo-finance.sh",
        ):
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                if relative_path.endswith(".py"):
                    if relative_path in {
                        "scripts/cancel-stale-autopilot-orders.py",
                        "scripts/fetch-alpaca-core-preflight.py",
                    }:
                        self.assertIn("session.call_tool", text)
                    else:
                        self.assertIn("Content-Length", text)
                        self.assertIn("tools/call", text)
                    self.assertIn("MCP_TIMEOUT_SECONDS", text)
                    continue
                self.assertIn("XDG_CACHE_HOME", text)
                self.assertIn("XDG_DATA_HOME", text)
                self.assertIn("UV_CACHE_DIR", text)
                self.assertIn("UV_TOOL_DIR", text)
                self.assertIn("UV_PYTHON_DOWNLOADS", text)
                self.assertIn("UV_LINK_MODE", text)
                self.assertIn("mkdir -p", text)

    def test_uvx_wrappers_prefer_installed_commands(self):
        expected_commands = {
            "scripts/alpaca-mcp.sh": "alpaca-mcp-server",
            "scripts/mcp-alpha-vantage.sh": "marketdata-mcp",
            "scripts/mcp-sec-edgar.sh": "sec-edgar-mcp",
            "scripts/mcp-yahoo-finance.sh": "yahoo-finance-mcp",
        }
        for relative_path, command in expected_commands.items():
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIn(f"command -v {command}", text)
                self.assertIn(f"exec {command}", text)

    def test_workspace_cache_is_not_tracked(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".cache/", gitignore.splitlines())

    def test_alpha_vantage_key_is_not_passed_as_process_argument(self):
        text = (ROOT / "scripts/mcp-alpha-vantage.sh").read_text(encoding="utf-8")

        self.assertIn("export ALPHA_VANTAGE_API_KEY", text)
        self.assertNotIn('marketdata-mcp "$ALPHA_VANTAGE_API_KEY"', text)

    def test_scheduled_codex_runs_preapprove_required_mcp_tools(self):
        expectations = {
            "scripts/run-hourly-autopilot-codex.sh": [
                "check-alpaca-market-open-mcp.py",
                "cancel-stale-autopilot-orders.py",
                "STALE_ORDER_CLEANUP_PATH",
                "fetch-alpaca-core-preflight.py",
                "ALPACA_PREFLIGHT_PATH",
                "AFTER_HOURS_ORDER_PROBE_PATH",
                "CODEX_AUTOPILOT_RUN_LABEL",
                "CODEX_AUTOPILOT_AFTER_HOURS_ORDER_PROBE",
                "probe-alpaca-after-hours-order.py",
                "Alpaca market is closed; scheduled autopilot exits before research/Codex run",
                'sandbox_permissions=["network-full-access"]',
                "mcp_servers.alpaca.command=",
                "mcp_servers.sec-edgar.command=",
                "mcp_servers.alpha-vantage.command=",
                "mcp_servers.fred.command=",
                "mcp_servers.firecrawl.command=",
                "mcp_servers.yahoo-finance.command=",
                'mcp_servers.alpaca.tools.get_clock.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_account_info.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_orders.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_all_positions.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_account_activities.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_watchlists.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_asset.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_stock_latest_quote.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_stock_snapshot.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_most_active_stocks.approval_mode="approve"',
                'mcp_servers.alpaca.tools.cancel_order_by_id.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_order_by_id.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_order_by_client_id.approval_mode="approve"',
                'mcp_servers.alpaca.tools.place_stock_order.approval_mode="approve"',
                'mcp_servers.sec-edgar.tools.get_recent_filings.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_LIST.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_GET.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_CALL.approval_mode="approve"',
                'mcp_servers.fred.tools.get_macro_snapshot.approval_mode="approve"',
                'mcp_servers.firecrawl.tools.firecrawl_scrape.approval_mode="approve"',
                'mcp_servers.yahoo-finance.tools.get_stock_info.approval_mode="approve"',
                "fetch-research-mcp-preflight.py",
                "RESEARCH_PREFLIGHT_PATH",
                "--alpaca-preflight-json",
                "CODEX_AUTOPILOT_RESEARCH_SYMBOL_LIMIT",
                "CODEX_AUTOPILOT_RESEARCH_MCP_TIMEOUT_SECONDS",
                "CODEX_AUTOPILOT_RESEARCH_CACHE_DIR",
                "CODEX_AUTOPILOT_RESEARCH_CACHE_TTL_SECONDS",
                "CODEX_AUTOPILOT_RESEARCH_CIRCUIT_SECONDS",
                "CODEX_AUTOPILOT_REGISTER_RESEARCH_MCP",
                "cache_hit",
                "circuit_breaker_open",
                "has_authoritative_research_preflight",
                "authoritative scheduled evidence",
                "mcp_coverage_hint",
                "Do not run ad hoc local network helper scripts",
                "SSL_CERT_FILE",
                "REQUESTS_CA_BUNDLE",
                "LANG",
                "LC_ALL",
                "pre-submit gate summary",
                "client_order_id",
                "build-agent-dashboard.py",
                'CODEX_AUTOPILOT_TIMEOUT_SECONDS", "900"',
            ],
            "scripts/run-analyst-review-codex.sh": [
                'sandbox_permissions=["network-full-access"]',
                "mcp_servers.alpaca.command=",
                "mcp_servers.sec-edgar.command=",
                "mcp_servers.alpha-vantage.command=",
                "mcp_servers.fred.command=",
                "mcp_servers.firecrawl.command=",
                "mcp_servers.yahoo-finance.command=",
                'mcp_servers.alpaca.tools.get_clock.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_account_info.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_orders.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_all_positions.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_account_activities.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_watchlists.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_stock_latest_quote.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_stock_snapshot.approval_mode="approve"',
                'mcp_servers.alpaca.tools.get_most_active_stocks.approval_mode="approve"',
                'mcp_servers.sec-edgar.tools.get_recent_filings.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_LIST.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_GET.approval_mode="approve"',
                'mcp_servers.alpha-vantage.tools.TOOL_CALL.approval_mode="approve"',
                'mcp_servers.fred.tools.get_macro_snapshot.approval_mode="approve"',
                'mcp_servers.firecrawl.tools.firecrawl_scrape.approval_mode="approve"',
                'mcp_servers.yahoo-finance.tools.get_stock_info.approval_mode="approve"',
                "Do not run ad hoc local network helper scripts",
                "build-agent-dashboard.py",
            ],
        }
        for relative_path, snippets in expectations.items():
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIn("CODEX_HOME", text)
                self.assertIn("CODEX_SCHEDULED_CODEX_HOME", text)
                self.assertIn("--ephemeral", text)
                self.assertIn("--ignore-user-config", text)
                self.assertIn("workspace-write", text)
                self.assertIn("source .env", text)
                self.assertNotIn('approval_mode="auto"', text)
                self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", text)
                for snippet in snippets:
                    self.assertIn(snippet, text)

    def test_hourly_autopilot_shell_handles_empty_research_cache_ttl_args(self):
        script_path = ROOT / "scripts" / "run-hourly-autopilot-codex.sh"
        text = script_path.read_text(encoding="utf-8")

        subprocess.run(["bash", "-n", str(script_path)], check=True)
        self.assertIn('if [ "${#RESEARCH_CACHE_TTL_ARGS[@]}" -gt 0 ]; then', text)
        self.assertIn('RESEARCH_PREFLIGHT_COMMAND+=("${RESEARCH_CACHE_TTL_ARGS[@]}")', text)
        self.assertNotIn('"${RESEARCH_CACHE_TTL_ARGS[@]}"; then', text)

    def test_hourly_autopilot_runtime_smoke_handles_empty_research_cache_ttl_args(self):
        source_script = ROOT / "scripts" / "run-hourly-autopilot-codex.sh"

        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            scripts_dir = temp_root / "scripts"
            scripts_dir.mkdir()
            (temp_root / ".env").write_text("ALPACA_PAPER_TRADE=true\n", encoding="utf-8")
            (scripts_dir / source_script.name).write_text(source_script.read_text(encoding="utf-8"), encoding="utf-8")

            stubs = {
                "check-alpaca-market-open-mcp.py": "print('stub market open')\n",
                "cancel-stale-autopilot-orders.py": "import json, sys\njson.dump({'ok': True}, open(sys.argv[sys.argv.index('--output-json') + 1], 'w'))\n",
                "fetch-alpaca-core-preflight.py": "import json, sys\njson.dump({'hard_gate': 'pass'}, open(sys.argv[sys.argv.index('--output-json') + 1], 'w'))\n",
                "fetch-research-mcp-preflight.py": (
                    "import json, pathlib, sys\n"
                    "path = pathlib.Path(sys.argv[sys.argv.index('--output-json') + 1])\n"
                    "json.dump({'hard_gate': 'pass', 'argv': sys.argv}, path.open('w'))\n"
                ),
            }
            for name, body in stubs.items():
                (scripts_dir / name).write_text(body, encoding="utf-8")
            notify_stub = scripts_dir / "send-openclaw-autopilot-update.py"
            notify_stub.write_text(
                "import pathlib, sys\n"
                "status = sys.argv[sys.argv.index('--status') + 1]\n"
                "root = pathlib.Path(__file__).resolve().parents[1]\n"
                "(root / 'notify.log').open('a', encoding='utf-8').write(status + '\\n')\n",
                encoding="utf-8",
            )
            notify_stub.chmod(0o755)

            completed = subprocess.run(
                ["bash", str(scripts_dir / source_script.name)],
                cwd=temp_root,
                env={
                    "HOME": str(temp_root),
                    "PATH": "/usr/local/bin:/usr/bin:/bin",
                    "CODEX_AUTOPILOT_RUNTIME_SMOKE_TEST": "1",
                },
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
            self.assertIn("runtime smoke test reached research preflight", completed.stdout)
            self.assertNotIn("RESEARCH_CACHE_TTL_ARGS: unbound variable", completed.stderr + completed.stdout)
            self.assertEqual(["completed"], (temp_root / "notify.log").read_text(encoding="utf-8").splitlines())

    def test_hourly_autopilot_after_hours_probe_runs_before_closed_exit(self):
        source_script = ROOT / "scripts" / "run-hourly-autopilot-codex.sh"

        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            scripts_dir = temp_root / "scripts"
            scripts_dir.mkdir()
            (temp_root / ".env").write_text("ALPACA_PAPER_TRADE=true\n", encoding="utf-8")
            (scripts_dir / source_script.name).write_text(source_script.read_text(encoding="utf-8"), encoding="utf-8")
            (scripts_dir / "check-alpaca-market-open-mcp.py").write_text(
                "import sys\nprint('{\"is_open\": false}')\nsys.exit(75)\n",
                encoding="utf-8",
            )
            (scripts_dir / "probe-alpaca-after-hours-order.py").write_text(
                "import json, pathlib, sys\n"
                "path = pathlib.Path(sys.argv[sys.argv.index('--output-json') + 1])\n"
                "path.parent.mkdir(parents=True, exist_ok=True)\n"
                "json.dump({'status': 'pass', 'argv': sys.argv}, path.open('w'))\n"
                "print('after-hours probe stub')\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                ["bash", str(scripts_dir / source_script.name)],
                cwd=temp_root,
                env={
                    "HOME": str(temp_root),
                    "PATH": "/usr/local/bin:/usr/bin:/bin",
                    "CODEX_AUTOPILOT_AFTER_HOURS_ORDER_PROBE": "1",
                },
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
            self.assertIn("running explicit after-hours paper order probe", completed.stdout)
            self.assertIn("after-hours probe stub", completed.stdout)
            self.assertNotIn("scheduled autopilot exits before research/Codex run", completed.stdout)
            probe_files = list((temp_root / "wiki" / "evidence-store" / "sources").glob("*after-hours-order-probe.json"))
            self.assertEqual(1, len(probe_files))

    def test_after_hours_autopilot_wrapper_sets_independent_label_and_probe_flag(self):
        script_path = ROOT / "scripts" / "run-after-hours-autopilot-codex.sh"
        text = script_path.read_text(encoding="utf-8")

        subprocess.run(["bash", "-n", str(script_path)], check=True)
        self.assertIn('RUN_LABEL="after-hours-autopilot"', text)
        self.assertIn("send-openclaw-autopilot-update.py", text)
        self.assertIn("TERMINAL_NOTIFY_SENT", text)
        self.assertNotIn('notify_autopilot "started"', text)
        self.assertIn('notify_autopilot "completed"', text)
        self.assertIn('notify_autopilot "failed"', text)
        self.assertIn("harness/workflows/after-hours-autopilot.md", text)
        self.assertIn("market.session=after_hours", text)
        self.assertIn("extended_hours=true", text)
        self.assertIn("after_hours_new_orders_submitted_today", text)
        self.assertIn("CODEX_AFTER_HOURS_AUTOPILOT_RUNTIME_SMOKE_TEST", text)
        self.assertNotIn("CODEX_AUTOPILOT_AFTER_HOURS_ORDER_PROBE", text)

    def test_openclaw_autopilot_update_summarizes_after_hours_orders(self):
        script_path = ROOT / "scripts" / "send-openclaw-autopilot-update.py"
        subprocess.run(["python3", "-m", "py_compile", str(script_path)], check=True)

        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            (temp_root / "wiki" / "current-runs" / "daily").mkdir(parents=True)
            (temp_root / "wiki" / "trade-ledger" / "orders").mkdir(parents=True)
            (temp_root / "wiki" / "evidence-store" / "run-manifests").mkdir(parents=True)
            run_id = "2026-05-28-1311-after-hours-autopilot"
            (temp_root / "wiki" / "current-runs" / "daily" / f"{run_id}.md").write_text(
                "Result: filled. filled_qty 1, filled_avg_price 116.79\n",
                encoding="utf-8",
            )
            (temp_root / "wiki" / "trade-ledger" / "orders" / f"{run_id}.json").write_text(
                json.dumps(
                    {
                        "mode": "submit",
                        "orders": [
                            {
                                "symbol": "INTC",
                                "side": "buy",
                                "qty": 1,
                                "limit_price": 116.8,
                                "extended_hours": True,
                                "client_order_id": "ah-20260528-1311-intc-buy-01",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (temp_root / "wiki" / "evidence-store" / "run-manifests" / f"{run_id}.json").write_text(
                json.dumps(
                    {
                        "mode": "submit",
                        "review_bucket": "after_hours_validation",
                        "risk_check_result": {"status": "PASS"},
                    }
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    "python3",
                    str(script_path),
                    "--run-id",
                    run_id,
                    "--session",
                    "after_hours",
                    "--status",
                    "completed",
                    "--root",
                    str(temp_root),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
            self.assertIn("[STOCK-TRAIN] 2026-05-28 13:11 KST | after_hours 완료", completed.stdout)
            self.assertIn("💰 Portfolio", completed.stdout)
            self.assertIn("🟢 Buy (1)", completed.stdout)
            self.assertIn("INTC | $117", completed.stdout)
            self.assertIn("🔴 Sell (0)", completed.stdout)
            self.assertLessEqual(len(completed.stdout.strip().splitlines()), 20)
            self.assertIn("OpenClaw notify target is unset; skipping message send.", completed.stderr)

    def test_after_hours_autopilot_runtime_smoke_reaches_research_preflight(self):
        source_script = ROOT / "scripts" / "run-after-hours-autopilot-codex.sh"

        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            scripts_dir = temp_root / "scripts"
            scripts_dir.mkdir()
            (temp_root / ".env").write_text("ALPACA_PAPER_TRADE=true\n", encoding="utf-8")
            (scripts_dir / source_script.name).write_text(source_script.read_text(encoding="utf-8"), encoding="utf-8")
            stubs = {
                "check-alpaca-market-open-mcp.py": "import sys\nprint('{\"is_open\": false}')\nsys.exit(75)\n",
                "fetch-alpaca-core-preflight.py": "import json, sys\njson.dump({'hard_gate': 'pass'}, open(sys.argv[sys.argv.index('--output-json') + 1], 'w'))\n",
                "fetch-research-mcp-preflight.py": (
                    "import json, pathlib, sys\n"
                    "path = pathlib.Path(sys.argv[sys.argv.index('--output-json') + 1])\n"
                    "json.dump({'hard_gate': 'pass', 'argv': sys.argv}, path.open('w'))\n"
                ),
            }
            for name, body in stubs.items():
                (scripts_dir / name).write_text(body, encoding="utf-8")
            notify_stub = scripts_dir / "send-openclaw-autopilot-update.py"
            notify_stub.write_text(
                "import pathlib, sys\n"
                "status = sys.argv[sys.argv.index('--status') + 1]\n"
                "root = pathlib.Path(__file__).resolve().parents[1]\n"
                "(root / 'notify.log').open('a', encoding='utf-8').write(status + '\\n')\n",
                encoding="utf-8",
            )
            notify_stub.chmod(0o755)

            completed = subprocess.run(
                ["bash", str(scripts_dir / source_script.name)],
                cwd=temp_root,
                env={
                    "HOME": str(temp_root),
                    "PATH": "/usr/local/bin:/usr/bin:/bin",
                    "CODEX_AFTER_HOURS_AUTOPILOT_RUNTIME_SMOKE_TEST": "1",
                },
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
            self.assertIn("after-hours autopilot runtime smoke test reached research preflight", completed.stdout)
            self.assertEqual(["completed"], (temp_root / "notify.log").read_text(encoding="utf-8").splitlines())

    def test_after_hours_probe_uses_mcp_extended_hours_and_cancel(self):
        script_path = ROOT / "scripts" / "probe-alpaca-after-hours-order.py"
        text = script_path.read_text(encoding="utf-8")

        subprocess.run(["python3", "-m", "py_compile", str(script_path)], check=True)
        self.assertIn("session.call_tool", text)
        self.assertIn('"place_stock_order"', text)
        self.assertIn('"extended_hours": True', text)
        self.assertIn('"time_in_force": "day"', text)
        self.assertIn('"type": "limit"', text)
        self.assertIn('"get_order_by_client_id"', text)
        self.assertIn('"cancel_order_by_id"', text)
        self.assertIn("ALPACA_PAPER_TRADE", text)
        self.assertNotIn("requests.", text)

    def test_scheduled_autopush_tracks_dashboard_artifacts(self):
        text = (ROOT / "scripts/git-autopush-artifacts.sh").read_text(encoding="utf-8")

        self.assertIn("ui/agent-dashboard.html", text)
        self.assertIn("ui/backtests", text)

    def test_hourly_autopilot_launchd_runs_every_20_minutes(self):
        plist = plistlib.loads(
            (ROOT / "scheduler" / "com.insightque.stock-alpaca.hourly-autopilot.plist.example").read_bytes()
        )

        intervals = plist["StartCalendarInterval"]
        self.assertIsInstance(intervals, list)
        pairs = {(item["Hour"], item["Minute"]) for item in intervals}
        self.assertIn((22, 31), pairs)
        self.assertIn((22, 51), pairs)
        for hour in [23, 0, 1, 2, 3, 4, 5]:
            for minute in [11, 31, 51]:
                self.assertIn((hour, minute), pairs)
        self.assertNotIn((6, 11), pairs)
        env = plist["EnvironmentVariables"]
        self.assertEqual("/Users/insightque", env["HOME"])
        self.assertEqual("en_US.UTF-8", env["LANG"])
        self.assertEqual("en_US.UTF-8", env["LC_ALL"])
        self.assertIn("/usr/local/bin", env["PATH"])
        self.assertEqual("127.0.0.1,localhost", env["NO_PROXY"])
        self.assertEqual("600", env["CODEX_AUTOPILOT_RESEARCH_CIRCUIT_SECONDS"])
        self.assertEqual("auto", env["CODEX_AUTOPILOT_REGISTER_RESEARCH_MCP"])

    def test_after_hours_autopilot_launchd_runs_every_20_minutes_with_separate_wrapper(self):
        plist = plistlib.loads(
            (ROOT / "scheduler" / "com.insightque.stock-alpaca.after-hours-autopilot.plist.example").read_bytes()
        )

        self.assertEqual(
            ["/Users/insightque/stock-alpaca/scripts/run-after-hours-autopilot-codex.sh"],
            plist["ProgramArguments"],
        )
        intervals = plist["StartCalendarInterval"]
        self.assertIsInstance(intervals, list)
        pairs = {(item["Hour"], item["Minute"]) for item in intervals}
        for hour in range(6, 22):
            for minute in [11, 31, 51]:
                self.assertIn((hour, minute), pairs)
        for hour in [22, 23, 0, 1, 2, 3, 4, 5]:
            self.assertNotIn((hour, 11), pairs)
        env = plist["EnvironmentVariables"]
        self.assertEqual("/Users/insightque", env["HOME"])
        self.assertEqual("en_US.UTF-8", env["LANG"])
        self.assertEqual("en_US.UTF-8", env["LC_ALL"])
        self.assertIn("/usr/local/bin", env["PATH"])
        self.assertEqual("127.0.0.1,localhost", env["NO_PROXY"])
        self.assertEqual("telegram", env["OPENCLAW_AUTOPILOT_NOTIFY_CHANNEL"])
        self.assertEqual("REPLACE_WITH_TELEGRAM_CHAT_ID", env["OPENCLAW_AUTOPILOT_NOTIFY_TARGET"])


if __name__ == "__main__":
    unittest.main()
