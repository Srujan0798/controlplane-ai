"""T3.2 — eval harness with confidence intervals.

``python -m evals.run`` (or ``make eval``) prints PER ROUTE a binding
distribution (never an undefined precision) plus action-level FPR/FNR with
Wilson score intervals, a per-stratum table, abstention (UNKNOWN) rate, and a
threshold-sensitivity curve for the BM25 coverage constants.

Hard rule (ARCHITECTURE §8, T3.2 contract): NO single accuracy number anywhere.
The published claim takes the §7 shape — "on this corpus we miss X% of
ungrounded claims (CI) — production FNR is unknown."

Ground truth: the corpus `label` field (should_hold | should_pass |
hard_negative). Per-claim `expected_verdicts` keys in the committed corpus are
inconsistent (action-id vs claim-id, verdict vs actuator), so per-route metrics
score the *binding route* against the *document-level* label — a defensible,
single source of truth.

Writes ``evals/last_run.json``; never invents numbers beyond measured counts.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from controlplane.binder import bind_claims
from controlplane.bm25 import COVERAGE_SUPPORTED, COVERAGE_UNKNOWN
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

ROUTE_ORDER = ["numeric", "structural", "textual", "derived", "temporal", "none"]

_COV_RX = re.compile(r"coverage=([0-9.]+)")

DERIVED_ROUTE_NOTE = (
    "Derived route publishes a BINDING DISTRIBUTION, not precision. "
    "CONTRADICTED on derived-trap is a true catch (sum does not recompute). "
    "SUPPORTED on clean-derived is a true recompute. Per-route precision is "
    "undefined here and is not published — a silent precision=0 would be a "
    "metric-definition error (scoring CONTRADICTED-as-correct as FP)."
)


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


def _route_for_method(method: str) -> str:
    """Map a binder method string onto one of the pipeline routes."""
    m = (method or "").lower()
    if m.startswith("numeric"):
        return "numeric"
    if m.startswith("structural"):
        return "structural"
    if m.startswith("derived"):
        return "derived"
    if "temporal" in m:
        return "temporal"
    if "bm25" in m or "textual" in m:
        return "textual"
    if m == "fixture" or m == "fixture-unresolved":
        return m  # never occurs in enforce / corpus runs
    return "none"


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

    would_hold = any(
        d.actuator.value in ("Escalate", "Block", "Edit") for d in decisions.values()
    )

    routes: dict[str, dict[str, Any]] = {}
    coverages: list[float] = []
    methods: dict[str, str] = {}
    for cid, b in led.bindings.items():
        route = _route_for_method(b.method)
        methods[cid] = b.method
        verdict = b.verdict.value
        routes.setdefault(
            route,
            {"n": 0, "supported": 0, "unsupported": 0, "unknown": 0, "contradicted": 0},
        )
        routes[route]["n"] += 1
        routes[route][verdict.lower()] = routes[route].get(verdict.lower(), 0) + 1
        if route in ("textual", "temporal"):
            m = _COV_RX.search(b.rationale or "")
            if m:
                coverages.append(float(m.group(1)))

    return {
        "id": case["id"],
        "stratum": case.get("stratum"),
        "use_case": case.get("use_case"),
        "label": case.get("label", ""),
        "would_hold": would_hold,
        "action_tiers": {a.action_id: a.tier.value for a in actions},
        "routes": routes,
        "bindings": {cid: b.verdict.value for cid, b in led.bindings.items()},
        "binding_methods": methods,
        "textual_coverages": coverages,
        "by_kind": {
            cid: led.claims[cid].kind.value
            for cid in led.claims
            if cid in led.bindings
        },
        "actuators": {aid: d.actuator.value for aid, d in decisions.items()},
    }


def _route_distribution(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Per-route BINDING DISTRIBUTION (real, never undefined).

    n is the binding count (not the case count). We do NOT publish a per-route
    precision/FPR: that metric is undefined when a route has zero true
    negatives, and it mislabels correctly-grounded claims on `should_hold`
    docs as false positives. The honest per-route view is the distribution of
    verdicts the binder produced and the abstention (UNKNOWN) rate.
    """
    agg: dict[str, dict[str, int]] = defaultdict(
        lambda: {"n": 0, "supported": 0, "unsupported": 0, "unknown": 0, "contradicted": 0}
    )
    for r in results:
        for route, blk in r["routes"].items():
            a = agg[route]
            a["n"] += int(blk.get("n") or 0)
            for v in ("supported", "unsupported", "unknown", "contradicted"):
                a[v] += blk.get(v, 0)
    out: dict[str, dict[str, Any]] = {}
    for route in ROUTE_ORDER:
        if route not in agg:
            continue
        a = agg[route]
        abstr = a["unknown"] / a["n"] if a["n"] else 0.0
        out[route] = {
            "n": a["n"],
            "supported": a["supported"],
            "unsupported": a["unsupported"],
            "unknown": a["unknown"],
            "contradicted": a["contradicted"],
            "abstention_rate": round(abstr, 4),
        }
        if route == "derived":
            out[route]["note"] = DERIVED_ROUTE_NOTE
    return out


def _action_level(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Action-level FPR/FNR -- the real gate metric (ARCHITECTURE §7 shape).

    For each case we look at whether the gate HELD the action vs the doc label:
      should_hold  -> correct gate HOLDS (true negative for a miss)
      should_pass  -> correct gate PASSES (true negative for a false alarm)
      hard_negative-> looks wrong but correct; holding is fail-closed CAUTION,
                      reported separately (not a false positive)

    Irreversible actions (R2/R3) are escalated by design (fail-closed), so they
    are reported as a distinct "fail-closed escalation" band and excluded from
    the passable-action FPR -- otherwise the metric would penalise caution.
    """
    pass_hold = pass_pass = 0
    irr_hold = irr_pass = 0
    sh_hold = sh_miss = 0
    hn_hold = hn_total = 0
    miss_ids: list[str] = []
    for r in results:
        label = r["label"]
        held = r["would_hold"]
        tiers = r.get("action_tiers") or {}
        is_irr = any(str(t) in ("R2", "R3") for t in tiers.values())
        if label == "should_hold":
            if held:
                sh_hold += 1
            else:
                sh_miss += 1
                miss_ids.append(r["id"])
        elif label == "should_pass":
            if is_irr:
                irr_pass += 1 if not held else 0
                irr_hold += 1 if held else 0
            else:
                if held:
                    pass_hold += 1
                else:
                    pass_pass += 1
        elif label == "hard_negative":
            hn_total += 1
            hn_hold += 1 if held else 0
    fnr = wilson_ci(sh_miss, sh_miss + sh_hold)
    fpr = (
        wilson_ci(pass_hold, pass_hold + pass_pass)
        if (pass_hold + pass_pass)
        else (0.0, 0.0, 0.0)
    )
    hn_rate = wilson_ci(hn_hold, hn_total) if hn_total else (0.0, 0.0, 0.0)
    return {
        "passable": {"fp": pass_hold, "tn": pass_pass, "fpr": fpr},
        "irreversible_fail_closed": {"held": irr_hold, "passed": irr_pass},
        "ungrounded": {
            "held": sh_hold,
            "missed": sh_miss,
            "miss_ids": miss_ids,
            "fnr": fnr,
        },
        "hard_negative_caution": {
            "held": hn_hold,
            "total": hn_total,
            "hold_rate": hn_rate,
        },
    }


def _stratum_table(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    strata: dict[str, dict[str, int]] = defaultdict(
        lambda: {"n": 0, "would_hold": 0, "should_hold": 0, "should_pass": 0, "hard_negative": 0}
    )
    for r in results:
        s = strata[r["stratum"] or "unknown"]
        s["n"] += 1
        if r["label"] == "should_hold":
            s["should_hold"] += 1
        elif r["label"] == "should_pass":
            s["should_pass"] += 1
        elif r["label"] == "hard_negative":
            s["hard_negative"] += 1
        if r["would_hold"]:
            s["would_hold"] += 1
    return {k: dict(v) for k, v in strata.items()}


def _threshold_calibration(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sweep candidate coverage thresholds over measured textual coverages.

    Same stored coverages, different cut-points — a real FP/FN-adjacent curve
    (abstention vs support share), not a hypothetical row of nulls. No
    threshold is asserted as ground truth; they ship only after shadow replay.
    """
    coverages = [c for r in results for c in (r.get("textual_coverages") or [])]
    total = len(coverages)
    rows: list[dict[str, Any]] = []
    sweeps = (
        (COVERAGE_SUPPORTED, COVERAGE_UNKNOWN, "observed committed constants"),
        (0.80, 0.45, "tighter — measured on this corpus only; ship after shadow replay"),
        (0.60, 0.30, "looser — measured on this corpus only; ship after shadow replay"),
    )
    for sup_t, unk_t, note in sweeps:
        n_sup = sum(1 for c in coverages if c >= sup_t)
        n_unk = sum(1 for c in coverages if unk_t <= c < sup_t)
        n_unsup = total - n_sup - n_unk
        rows.append(
            {
                "coverage_supported": sup_t,
                "coverage_unknown": unk_t,
                "textual_bound": total,
                "supported_count": n_sup,
                "unknown_count": n_unk,
                "unsupported_count": n_unsup,
                "abstention_rate": round(n_unk / total, 4) if total else 0.0,
                "note": note,
            }
        )
    return rows


def _corpus_block(results: list[dict[str, Any]], action: dict[str, Any]) -> dict[str, Any]:
    n = len(results)
    hn_total = action["hard_negative_caution"]["total"]
    missed = action["ungrounded"]["missed"]
    held = action["ungrounded"]["held"]
    return {
        "self_authored": True,
        "production_fnr": "unknown",
        "n_cases": n,
        "hard_negative_n": hn_total,
        "hard_negative_share": (hn_total / n) if n else 0.0,
        "ungrounded_n": missed + held,
        "miss_ids": list(action["ungrounded"]["miss_ids"]),
        "fnr_definition": (
            "action-level: should_hold cases the gate did not hold "
            "(Edit/Escalate/Block)"
        ),
        "fpr_definition": (
            "action-level: should_pass R0/R1 cases the gate held; "
            "hard negatives and R2/R3 fail-closed holds are not FPR"
        ),
        "wilson": "95% Wilson score interval on the binomial proportion",
        "published_fnr_source": "eval-corpus",
    }


def _summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    per_route = _route_distribution(results)
    per_stratum = _stratum_table(results)
    action = _action_level(results)
    abstain = sum(
        1 for r in results for v in r["bindings"].values() if v == Verdict.UNKNOWN.value
    )
    total_bindings = sum(len(r["bindings"]) for r in results)
    calibration = _threshold_calibration(results)
    corpus = _corpus_block(results, action)
    hn_share = corpus["hard_negative_share"]

    return {
        "n_cases": len(results),
        "n_bindings": total_bindings,
        "abstention_unknown": abstain,
        "abstention_rate": round(abstain / total_bindings, 4) if total_bindings else 0.0,
        "per_route": per_route,
        "per_stratum": per_stratum,
        "action_level": action,
        "passable_fpr": action["passable"]["fpr"][0],
        "passable_fpr_wilson": list(action["passable"]["fpr"]),
        "ungrounded_fnr": action["ungrounded"]["fnr"][0],
        "ungrounded_fnr_wilson": list(action["ungrounded"]["fnr"]),
        "hard_negative_hold_rate": action["hard_negative_caution"]["hold_rate"][0],
        "hard_negative_hold_wilson": list(action["hard_negative_caution"]["hold_rate"]),
        "hard_negative_n": corpus["hard_negative_n"],
        "hard_negative_share": hn_share,
        "threshold_calibration": calibration,
        "corpus": corpus,
        "published_fnr_source": "eval-corpus",
        "production_fnr": "unknown",
        "derived_route_note": DERIVED_ROUTE_NOTE,
        "note": (
            "No single accuracy number. Per-route binding DISTRIBUTION + abstention; "
            "action-level FPR/FNR take the ARCHITECTURE §7 shape (the gate metric). "
            "Corpus is self-authored with hard negatives; numbers are measured on "
            "this run only. Production FNR is unknown."
        ),
    }


def _compute() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    cases = _load_cases()
    if not cases:
        raise RuntimeError("No eval cases found under evals/cases/")
    results = [run_case(c) for c in cases]
    return _summarize(results), results


def build_report() -> dict[str, Any]:
    rep, _ = _compute()
    return rep


def _fmt_ci(triple: tuple[float, float, float] | list[float]) -> str:
    p, lo, hi = triple
    return f"{p:.1%} (95% CI {lo:.1%}–{hi:.1%})"


def _print_report(rep: dict[str, Any]) -> None:
    print(f"cases: {rep['n_cases']}  bindings: {rep['n_bindings']}")
    print(
        f"abstention (UNKNOWN): {rep['abstention_unknown']} "
        f"({rep['abstention_rate']:.1%} of bindings)"
    )
    print("corpus: self-authored  production FNR: UNKNOWN")
    print(
        f"hard negatives: {rep['hard_negative_n']}/{rep['n_cases']} "
        f"= {rep['hard_negative_share']:.1%}  (≥20% floor)"
    )
    print("\n-- per-route BINDING DISTRIBUTION (supported/unknown/contradicted/unsupported) --")
    for route, m in rep["per_route"].items():
        extra = ""
        if route == "derived":
            extra = "  [distribution, not precision — see README]"
        print(
            f"  {route:10s} n={m['n']:4d}  sup={m['supported']:3d}  unk={m['unknown']:3d}  "
            f"contrad={m['contradicted']:3d}  unsup={m['unsupported']:3d}  "
            f"abstain={m['abstention_rate']:.1%}{extra}"
        )
    print("\n-- ACTION-LEVEL (the §7 gate metric) --")
    a = rep["action_level"]
    u = a["ungrounded"]
    miss_ids = ",".join(u.get("miss_ids") or []) or "(none)"
    print(
        f"published FNR (ungrounded, this corpus): {_fmt_ci(rep['ungrounded_fnr_wilson'])}  "
        f"missed={u['missed']}/{u['missed'] + u['held']}  ids={miss_ids}"
    )
    print("production FNR: UNKNOWN")
    print(
        f"  passable-action false-hold (FPR): {_fmt_ci(rep['passable_fpr_wilson'])}  "
        f"-> we wrongly hold {rep['passable_fpr']:.1%} of clean R0/R1 responses"
    )
    print(
        f"  irreversible actions escalated (fail-closed, by design): "
        f"held={a['irreversible_fail_closed']['held']} "
        f"passed={a['irreversible_fail_closed']['passed']}"
    )
    print(
        f"  fail-closed caution on hard-negatives: {_fmt_ci(rep['hard_negative_hold_wilson'])}  "
        f"(held but defensible — not a false positive)"
    )
    print("\n-- per-stratum holds --")
    for stratum, s in sorted(rep["per_stratum"].items()):
        print(
            f"  {stratum:24s} n={s['n']:3d}  should_hold={s['should_hold']:3d}  "
            f"held={s['would_hold']:3d}  hard_neg={s['hard_negative']:2d}"
        )
    print("\n-- threshold sensitivity (ship only after shadow replay, T5.3) --")
    for row in rep["threshold_calibration"]:
        print(
            f"  cov_sup={row['coverage_supported']}  "
            f"abstention={row['abstention_rate']}  "
            f"sup={row['supported_count']} unk={row['unknown_count']}  "
            f"{row['note']}"
        )


def main() -> int:
    try:
        rep, results = _compute()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    _print_report(rep)

    payload = {
        "summary": rep,
        "results": [
            {
                k: v
                for k, v in r.items()
                if k not in ("binding_methods", "textual_coverages", "action_tiers")
            }
            for r in results
        ],
    }
    LAST_RUN.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nwrote {LAST_RUN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
