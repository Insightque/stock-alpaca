from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-policy-source-of-truth.py"


class PolicySourceOfTruthTests(unittest.TestCase):
    def test_active_docs_do_not_duplicate_policy_numbers(self) -> None:
        result = subprocess.run(
            ["python3", str(SCRIPT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_detects_hardcoded_active_policy_cap(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", dir=ROOT, delete=True) as handle:
            handle.write("Submit at most 10 new orders per run.\n")
            handle.flush()
            result = subprocess.run(
                ["python3", str(SCRIPT), Path(handle.name).relative_to(ROOT).as_posix()],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("hardcoded policy-like numeric value", result.stdout)


if __name__ == "__main__":
    unittest.main()
