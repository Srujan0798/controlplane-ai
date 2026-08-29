"""T8.1 — make verify with number-drift guard (RED first).

Acceptance: one command runs preflight -> tests -> content laws -> eval -> bench,
then DIFFS every number printed against every number quoted in the PDF and deck.
Any drift fails the build. The guard must actually FAIL when a number changes.

We exercise scripts/verify.py in its lightweight `--drift-only` mode (rebuilds the
README PDF from the live eval/bench JSON and asserts the in-PDF figures match).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify.py"
EVAL_JSON = ROOT / "evals" / "last_run.json"


def _run_verify(args=None):
    cmd = [sys.executable, str(VERIFY)] + (args or [])
    return subprocess.run(cmd, capture_output=True, text=True)


def test_verify_script_exists():
    assert VERIFY.exists(), "scripts/verify.py must exist for `make verify`"


def test_verify_passes_on_consistent_tree():
    res = _run_verify(["--drift-only"])
    assert res.returncode == 0, f"verify drift-only failed:\n{res.stdout}\n{res.stderr}"


def test_verify_fails_on_eval_number_drift():
    """Tamper the eval JSON FNR; the guard must detect the drift and fail."""
    data = json.loads(EVAL_JSON.read_text())
    summary = data.setdefault("summary", {})
    saved = summary.get("overall_fnr_wilson")
    try:
        # Force a fabricated FNR that the rebuilt PDF cannot contain.
        summary["overall_fnr_wilson"] = [0.1234, 0.10, 0.15]
        EVAL_JSON.write_text(json.dumps(data, indent=2))
        res = _run_verify(["--drift-only"])
        assert res.returncode != 0, "verify must FAIL when eval FNR drifts from PDF"
    finally:
        if saved is not None:
            summary["overall_fnr_wilson"] = saved
        EVAL_JSON.write_text(json.dumps(data, indent=2))
