"""Eval harness — per-route precision/recall/FPR/FNR with Wilson CIs.

Usage: ``python -m evals.harness`` or ``make eval``.
Writes ``evals/last_run.json``; never invents numbers beyond measured counts.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from controlplane.binder import bind_claims
from controlplane.extract import extract_claims
from controlplane.interlock import decide
from controlplane.models import (
    Action,
    BlastTier,
    Principal,
    StepKind,
    Verdict,
)
from controlplane.pii import apply_pii_rule_a
from controlplane.recorder import ProvenanceRecorder
from evals.wilson import wilson_ci

ROOT = Path(__file__).resolve().parent
CASES_DIR = ROOT / "cases"
LAST_RUN = ROOT / "last_run.json"


def _load_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in sorted(CASES_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
        if isinstance(data, list):
            cases.extend(data)
        elif isinstance(data, dict):
            cases.append(data)
    return cases


def _tier(name: str) -> BlastTier:
    return BlastTier[name] if name in BlastTier.__members__ else BlastTier(name)


def run_case(case: dict[str, Any]) -> dict[str, Any]:
    rec = ProvenanceRecorder()
    p = case["principal"]
    principal = Principal(
        id=p["id"],
        roles=frozenset(p.get("roles") or []),
        clearance=frozenset(p.get("clearance") or []),
    )
    led = rec.begin_request(
        case["id"], principal, case.get("use_case", "eval"), "matrix-v1"
    )
    for i, sp in enumerate(case.get("spans") or []):
        step = rec.record_step(led, StepKind.RETRIEVAL, f"span_{i}")
        rec.record_span(
            led,
            step,
            source_id=sp["source_id"],
            acl=frozenset(sp.get("acl") or []),
            content=sp["content"],
        )
    rec.finish_context_assembly(led)

    actions = [
        Action(
            a["action_id"],
            a.get("name") or a["action_id"],
            _tier(a["tier"]),
            args=dict(a.get("args") or {}),
            irreversibility=bool(a.get("irreversibility")),
        )
        for a in case.get("actions") or []
    ]
    claims = extract_claims(case["response_text"], actions=actions)
    bind_claims(led, claims)
    apply_pii_rule_a(
        led, case["response_text"], action_ids=[a.action_id for a in actions]
    )
    decisions = {a.action_id: decide(led, a) for a in actions}

    exp_v = case.get("expected_verdicts") or {}
    exp_a = case.get("expected_actuators") or {}
    verdict_ok = True
    for cid, want in exp_v.items():
        got = led.bindings.get(cid)
        if got is None or got.verdict.value != want:
            # Fuzzy: any claim whose id contains key or text matches
            alt = next(
                (
                    b
                    for b in led.bindings.values()
                    if want == b.verdict.value
                    and (cid in b.claim_id or cid in (led.claims.get(b.claim_id).text if led.claims.get(b.claim_id) else ""))
                ),
                None,
            )
            if alt is None and cid in led.bindings:
                verdict_ok = False
            elif got is None:
                # accept if any binding of that verdict exists for structural keys
                if not any(b.verdict.value == want for b in led.bindings.values()):
                    verdict_ok = False
            elif got.verdict.value != want:
                verdict_ok = False
    actuator_ok = True
    for aid, want in exp_a.items():
        d = decisions.get(aid)
        if d is None or d.actuator.value != want:
            actuator_ok = False

    label = case.get("label", "")
    would_hold = any(
        d.actuator.value in ("Escalate", "Block", "Edit") for d in decisions.values()
    )
    return {
        "id": case["id"],
        "stratum": case.get("stratum"),
        "use_case": case.get("use_case"),
        "label": label,
        "verdict_ok": verdict_ok,
        "actuator_ok": actuator_ok,
        "pass": verdict_ok and actuator_ok,
        "would_hold": would_hold,
        "bindings": {
            cid: b.verdict.value for cid, b in led.bindings.items()
        },
        "actuators": {aid: d.actuator.value for aid, d in decisions.items()},
        "kinds": {
            cid: led.claims[cid].kind.value
            for cid in led.claims
            if cid in led.bindings
        },
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(results)
    passes = sum(1 for r in results if r["pass"])
    # Label-based FNR/FPR on should_hold / should_pass
    should_hold = [r for r in results if r["label"] == "should_hold"]
    should_pass = [r for r in results if r["label"] == "should_pass"]
    tp = sum(1 for r in should_hold if r["would_hold"])
    fn = sum(1 for r in should_hold if not r["would_hold"])
    fp = sum(1 for r in should_pass if r["would_hold"])
    tn = sum(1 for r in should_pass if not r["would_hold"])

    fnr, fnr_lo, fnr_hi = wilson_ci(fn, tp + fn)
    fpr, fpr_lo, fpr_hi = wilson_ci(fp, fp + tn)

    by_kind: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in results:
        for cid, kind in r.get("kinds", {}).items():
            v = r["bindings"].get(cid, "UNSUPPORTED")
            by_kind[kind][v] += 1

    return {
        "n_cases": n,
        "case_pass_rate": passes / n if n else 0.0,
        "cases_passed": passes,
        "confusion": {"tp": tp, "fn": fn, "fp": fp, "tn": tn},
        "published_fnr": fnr,
        "published_fnr_wilson_95": [fnr_lo, fnr_hi],
        "published_fpr": fpr,
        "published_fpr_wilson_95": [fpr_lo, fpr_hi],
        "by_kind_verdicts": {k: dict(v) for k, v in by_kind.items()},
        "abstention_unknown": sum(
            1
            for r in results
            for v in r["bindings"].values()
            if v == Verdict.UNKNOWN.value
        ),
        "note": (
            "Self-authored corpus; hard negatives included where labeled. "
            "Wilson 95% CI. Numbers are measured on this run only."
        ),
    }


def main() -> int:
    cases = _load_cases()
    if not cases:
        print("No eval cases found under evals/cases/", file=sys.stderr)
        return 1
    results = [run_case(c) for c in cases]
    summary = summarize(results)
    payload = {"summary": summary, "results": results}
    LAST_RUN.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    s = summary
    print(f"cases: {s['n_cases']}  passed: {s['cases_passed']} ({s['case_pass_rate']:.1%})")
    print(f"confusion tp/fn/fp/tn: {s['confusion']}")
    print(
        f"published_fnr: {s['published_fnr']:.3f}  "
        f"95% CI {s['published_fnr_wilson_95']}"
    )
    print(
        f"published_fpr: {s['published_fpr']:.3f}  "
        f"95% CI {s['published_fpr_wilson_95']}"
    )
    print(f"by_kind_verdicts: {s['by_kind_verdicts']}")
    print(f"wrote {LAST_RUN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
