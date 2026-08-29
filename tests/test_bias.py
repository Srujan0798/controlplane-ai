from controlplane.bias import probe_acl_skew
from controlplane.models import (
    AssertionStrength,
    Claim,
    ClaimKind,
    Principal,
    StepKind,
)
from controlplane.pipeline import ControlPlaneGate
from controlplane.recorder import ProvenanceRecorder
from controlplane.shadow import MetricsStore


def test_acl_skew_zero_when_all_readable():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "r",
        Principal(id="agent", clearance=frozenset({"public", "hr-confidential"})),
        "show",
    )
    sid = rec.record_step(led, StepKind.RETRIEVAL, "doc")
    rec.record_span(
        led,
        sid,
        source_id="doc:1",
        acl=frozenset({"hr-confidential"}),
        content="salary band",
    )
    rec.finish_context_assembly(led)
    out = probe_acl_skew(led)
    assert out == {"acl_skew": 0.0, "flag": False}


def test_acl_skew_fraction_and_flag():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "r",
        Principal(id="cs", clearance=frozenset({"vendor-public"})),
        "show",
    )
    sid = rec.record_step(led, StepKind.RETRIEVAL, "mix")
    rec.record_span(
        led,
        sid,
        source_id="doc:pub",
        acl=frozenset({"vendor-public"}),
        content="ok",
    )
    rec.record_span(
        led,
        sid,
        source_id="doc:hr",
        acl=frozenset({"hr-confidential"}),
        content="secret",
    )
    rec.finish_context_assembly(led)
    out = probe_acl_skew(led)
    assert out["acl_skew"] == 0.5
    assert out["flag"] is True


def test_empty_ledger_skew_is_zero():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "r",
        Principal(id="x", clearance=frozenset({"public"})),
        "show",
    )
    rec.finish_context_assembly(led)
    assert probe_acl_skew(led) == {"acl_skew": 0.0, "flag": False}


def test_gate_public_dict_includes_bias_probe():
    gate = ControlPlaneGate(metrics=MetricsStore())
    result = gate.run_refund_demo(mode_override="enforce")
    pub = result.public_dict()
    probe = pub["responsibility"]["bias_probe"]
    assert probe["flag"] is True
    assert 0 < probe["acl_skew"] < 1
    # refund fixture: 1 hr-confidential of 5 spans
    assert abs(probe["acl_skew"] - 0.2) < 1e-9


def test_counterfactual_flip_rate_with_wilson_ci():
    from controlplane.bias import FlipWindow, counterfactual_flip

    win = FlipWindow(max_n=50)

    def decide_fn(attr: str) -> str:
        # Synthetic: one protected attr flips Edit → Pass
        return "Pass" if attr == "group_b" else "Edit"

    out = counterfactual_flip(
        decide_fn,
        baseline_attr="group_a",
        perturbed_attrs=["group_b", "group_c"],
        window=win,
    )
    assert out["flips"] == 1
    assert out["n"] == 1
    assert out["flip_rate"] == 1.0
    assert len(out["wilson_95"]) == 2
    assert out["baseline"]["decision"] == "Edit"
    assert any(p["flipped"] for p in out["perturbations"])
