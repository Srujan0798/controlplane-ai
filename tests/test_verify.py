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
    """Tamper the eval JSON FNR/FPR; the guard must detect the drift and fail."""
    data = json.loads(EVAL_JSON.read_text())
    summary = data.setdefault("summary", {})
    saved_fnr = summary.get("ungrounded_fnr_wilson")
    saved_fpr = summary.get("passable_fpr_wilson")
    try:
        # Force fabricated headline metrics the rebuilt PDF cannot contain.
        summary["ungrounded_fnr_wilson"] = [0.1234, 0.10, 0.15]
        summary["passable_fpr_wilson"] = [0.5678, 0.50, 0.60]
        EVAL_JSON.write_text(json.dumps(data, indent=2))
        res = _run_verify(["--drift-only"])
        assert res.returncode != 0, "verify must FAIL when eval FNR/FPR drifts from PDF"
    finally:
        if saved_fnr is not None:
            summary["ungrounded_fnr_wilson"] = saved_fnr
        if saved_fpr is not None:
            summary["passable_fpr_wilson"] = saved_fpr
        EVAL_JSON.write_text(json.dumps(data, indent=2))
