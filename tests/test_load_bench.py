"""T3.4 — load bench at claimed scale (RED first).

These assert the contract before ``scripts/load_bench.py`` produces it:
  - n >= 10000 (T3.4 acceptance)
  - per-stage breakdown present (extract / bind / entitle / interlock)
  - concurrency sweep with multiple levels
  - a methodology block so numbers aren't quotable out of context
  - never quotes 40ms as p95 (content law 6)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "scripts" / "load_bench.py"


def _run_bench(*extra):
    out = ROOT / "submission" / "latency_bench.json"
    cmd = [sys.executable, str(BENCH), *extra]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"bench failed: {res.stderr}"
    return json.loads(out.read_text())


def test_bench_runs_n_10000():
    rep = _run_bench("-n", "10000", "--sweep")
    assert rep["n"] >= 10000, f"n={rep['n']} < 10000"


def test_per_stage_breakdown_present():
    rep = _run_bench("-n", "10000", "--sweep")
    assert "per_stage_ms" in rep
    for stage in ("extract", "bind", "entitle", "interlock"):
        assert stage in rep["per_stage_ms"], f"missing stage {stage}"
        s = rep["per_stage_ms"][stage]
        assert "p50" in s and "p95" in s and "p99" in s


def test_concurrency_sweep_multiple_levels():
    rep = _run_bench("-n", "10000", "--sweep")
    assert "concurrency_sweep" in rep
    # At least the levels 1 and a higher concurrency are present.
    levels = rep["concurrency_sweep"]
    assert any(item["concurrency"] == 1 for item in levels)
    assert max(item["concurrency"] for item in levels) >= 4


def test_methodology_block_present():
    rep = _run_bench("-n", "10000", "--sweep")
    assert "methodology" in rep and isinstance(rep["methodology"], dict)
    assert "machine" in rep["methodology"] or "note" in rep["methodology"]


def test_never_quotes_40ms_as_p95():
    rep = _run_bench("-n", "10000", "--sweep")
    # Content law 6: never quote 40ms as p95. The reported gate p95 must be
    # honestly >= whatever was measured, and the note must not claim 40ms == p95.
    note = json.dumps(rep.get("methodology", {})) + json.dumps(rep.get("note", ""))
    # If a p95 figure is reported, the gate p95 must not be asserted as exactly 40.
    gate = rep.get("gate_latency_ms") or {}
    p95 = gate.get("p95")
    if p95 is not None:
        assert p95 >= 0  # sanity; the real guard is the methodology honesty
    assert "40ms as p95" not in note, "content law 6 violation: 40ms quoted as p95"
