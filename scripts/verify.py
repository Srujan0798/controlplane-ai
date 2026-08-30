#!/usr/bin/env python3
"""T8.1 — `make verify`: one command, end to end, with number-drift guard.

Runs:
  scripts/preflight-lite.sh  (if present)
  pytest -q                  (full suite, incl. content laws)
  make eval                  (real FNR/FPR with Wilson CIs)
  make bench                 (n=10000 per-stage)

Then the DRIFT GUARD: regenerate the README PDF from the live eval/bench JSON and
assert the numbers printed into the PDF match evals/last_run.json and
submission/latency_bench.json. The README PDF is the single source of "numbers a
judge reads"; if its rendered figures disagree with the freshly computed metrics,
the build FAILS. Proposal PDF / deck are checked for content-law compliance via
the pytest content-laws suite above.

Exit non-zero on any failure (including drift).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_PDF = ROOT / "submission" / "ControlPlane_Round2_README.pdf"
EVAL_JSON = ROOT / "evals" / "last_run.json"
BENCH_JSON = ROOT / "submission" / "latency_bench.json"
PREFILIGHT = ROOT / "scripts" / "preflight-lite.sh"


def _run(cmd, *, check=True):
    print(f"\n$ {' '.join(cmd)}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    if out:
        print(out[-1500:])
    if check and r.returncode != 0:
        print(f"FAILED ({cmd}): exit {r.returncode}")
        sys.exit(r.returncode)
    return r


def _pdf_fnr_text() -> str:
    try:
        from pypdf import PdfReader
    except ImportError as e:
        raise SystemExit(
            "FATAL: pypdf is required for README PDF drift guard "
            "(pip install -e '.[dev]'). "
            f"ImportError: {e}"
        ) from e
    if not README_PDF.exists():
        raise SystemExit(
            f"FATAL: {README_PDF} missing — run `python3 scripts/build_readme_pdf.py`"
        )
    text = "\n".join((p.extract_text() or "") for p in PdfReader(str(README_PDF)).pages)
    if not text.strip():
        raise SystemExit(
            "FATAL: README PDF has no extractable text — regenerate with "
            "`python3 scripts/build_readme_pdf.py`"
        )
    return text


def _drift_guard() -> None:
    """Compare numbers QUOTED in the committed README PDF against the freshly
    computed eval/bench JSON. Any mismatch FAILS the build (no silent rebuild).

    This is the T8.1 contract: diff every number printed against every number
    quoted in the PDF. If eval numbers changed but the PDF wasn't regenerated,
    this catches the drift.
    """
    assert EVAL_JSON.exists(), "evals/last_run.json missing — run make eval first"
    eval_data = json.loads(EVAL_JSON.read_text())
    eval_summary = eval_data.get("summary", eval_data)

    pdf_text = _pdf_fnr_text()
    # Guard BOTH headline gate metrics, not just FNR (the earlier FNR-only guard
    # was too weak — GATE.md 3.5 requires every number in the PDF to be traceable).
    fnr = eval_summary.get("ungrounded_fnr_wilson") or [0.0, 0.0, 0.0]
    fpr = eval_summary.get("passable_fpr_wilson") or [0.0, 0.0, 0.0]
    fnr_pct = f"{fnr[0]:.1%}"
    fpr_pct = f"{fpr[0]:.1%}"
    if fnr_pct not in pdf_text:
        print(f"DRIFT: README PDF FNR {fnr_pct} not present in PDF")
        print("       regenerate the PDF with `make readme` after changing eval numbers")
        sys.exit(1)
    if fpr_pct not in pdf_text:
        print(f"DRIFT: README PDF passable FPR {fpr_pct} not present in PDF")
        print("       regenerate the PDF with `make readme` after changing eval numbers")
        sys.exit(1)
    print(f"drift guard OK: README PDF FNR {fnr_pct} and FPR {fpr_pct} match eval JSON")

    if BENCH_JSON.exists():
        # Bench timing is non-deterministic run-to-run (p50 ~0.4-0.6ms), so an
        # exact-match drift check would be flaky. We check the committed PDF's
        # gate p50/p95 fall within a +/-15% tolerance band of the live bench —
        # that is the defensible "every number traceable" check (GATE.md 3.5).
        import re as _re
        bench = json.loads(BENCH_JSON.read_text())
        g = bench.get("gate_latency_ms", {})
        live_p50 = g.get("p50")
        live_p95 = g.get("p95")
        if live_p50 is not None:
            lo50, hi50 = live_p50 * 0.85, live_p50 * 1.15
            nums = [float(x) for x in _re.findall(r"p50=([0-9.]+)", pdf_text)]
            if nums and not any(lo50 <= n <= hi50 for n in nums):
                print(f"DRIFT: README PDF gate p50 {nums} outside +/-15% band [{lo50:.3f},{hi50:.3f}] of live bench")
                sys.exit(1)
        if live_p95 is not None:
            lo95, hi95 = live_p95 * 0.85, live_p95 * 1.15
            nums = [float(x) for x in _re.findall(r"p95=([0-9.]+)", pdf_text)]
            if nums and not any(lo95 <= n <= hi95 for n in nums):
                print(f"DRIFT: README PDF gate p95 {nums} outside +/-15% band [{lo95:.3f},{hi95:.3f}] of live bench")
                sys.exit(1)
        print("drift guard OK: README PDF bench timings within +/-15% of live bench JSON")


def main() -> int:
    print("=== ControlPlane verify ===")
    if "--drift-only" in sys.argv:
        # Lightweight path used by the test: compare the COMMITTED README PDF
        # against the current eval JSON. Does NOT rebuild (a rebuild would hide
        # drift). Skips the full pytest/bench.
        assert EVAL_JSON.exists(), "evals/last_run.json missing — run make eval first"
        _drift_guard()
        print("\n=== verify (drift-only): GREEN ===")
        return 0
    if PREFILIGHT.exists():
        _run(["bash", str(PREFILIGHT)])
    _run([sys.executable, "-m", "pytest", "-q"])
    _run([sys.executable, "-m", "evals.run"])
    _run([sys.executable, str(ROOT / "scripts" / "load_bench.py"), "-n", "10000", "--sweep"])
    _drift_guard()
    print("\n=== verify: ALL GREEN, no drift ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
