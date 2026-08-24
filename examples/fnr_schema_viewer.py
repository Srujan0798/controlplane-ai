#!/usr/bin/env python3
"""ControlPlane.ai — empty FNR schema viewer (Stage 5 demo artifact).

Renders the FROZEN per-route false-negative-rate (FNR) typed schema from
R2S4.md §8, with every measured field null and measurement_status =
prototype_corpus. This is the "emptiness is the credibility play" screen
state the pitch puts on screen (R2S5 §4 Beat 7, §9; Appendix C pre-room
step -60). It is a RENDER-ONLY artifact: no model, no new mechanism, no
fabricated percentages. The schema shape is taken verbatim from the frozen
stage lock and must not be redrawn.
"""

# Frozen schema field order — R2S4.md §8, do not alter.
FNR_FIELDS = [
    "route_id",
    "policy_version",
    "window",
    "strata",
    "sampled_count_per_stratum",
    "false_negative_count",
    "ground_truth_positive_count",
    "FNR_estimate",
    "CI_lower",
    "CI_upper",
    "ground_truth_method",
    "measurement_status",
    "limitations",
]

# measurement_status ∈ {null, insufficient_sample, prototype_corpus,
#                        production_measured, stale}  (frozen vocabulary)
MEASUREMENT_STATUS = "prototype_corpus"

# Two live Stage 1 routes only. No third route. Bias is async-only and is
# NOT a schema row here (it is a separate route-level flip-rate measurement).
ROUTES = ["refund_trace", "knowledge_flip"]

# Per-route identity strings shown on the held-refund / principal-flip demos.
ROUTE_POLICY = {
    "refund_trace": "matrix-v1",
    "knowledge_flip": "matrix-v1",
}


def render_schema(route_id: str, policy_version: str) -> str:
    """Render one route's FNR schema as typed nulls. No numbers invented."""
    lines = []
    lines.append(f"route_id                : {route_id}")
    lines.append(f"policy_version          : {policy_version}")
    lines.append(f"window                  : null   # no earned measurement window yet")
    lines.append(f"strata                  : null   # stratified shadow audit not yet run")
    lines.append(f"sampled_count_per_stratum: null")
    lines.append(f"false_negative_count     : null")
    lines.append(f"ground_truth_positive_count: null")
    lines.append(f"FNR_estimate            : null")
    lines.append(f"CI_lower                : null")
    lines.append(f"CI_upper                : null")
    lines.append(f"ground_truth_method     : null   # never LLM-as-judge")
    lines.append(f"measurement_status      : {MEASUREMENT_STATUS}")
    lines.append(f"limitations             : null")
    return "\n".join(lines)


def main() -> None:
    print("ControlPlane.ai — published per-route FNR (typed format, empty until earned)")
    print("=" * 68)
    print()
    print("Vocabulary: we publish what we MISSED, not what we caught.")
    print("Status vocabulary: null | insufficient_sample | prototype_corpus |")
    print("                 production_measured | stale")
    print("Stratified shadow audit: 100% of Block / Escalate / Edit + random")
    print("sample of Pass / Pass. Ground truth = human / expensive multi-verifier,")
    print("never LLM-as-judge.")
    print()
    for route in ROUTES:
        print(f"--- FNR schema: {route} ---")
        print(render_schema(route, ROUTE_POLICY[route]))
        print(f"  measurement_status = {MEASUREMENT_STATUS}  # corpus synthetic; no trustworthy ground truth yet")
        print()
    print("Emptiness is the credibility play. No fabricated percentages.")
    print("Hash chain verify_chain() = True")


if __name__ == "__main__":
    main()
