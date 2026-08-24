from controlplane.binder import bind_claims
from controlplane.entitlement import audit_claim
from controlplane.models import (
    AssertionStrength,
    Claim,
    ClaimKind,
    Principal,
    StepKind,
)
from controlplane.recorder import ProvenanceRecorder
from controlplane.scenarios.knowledge import (
    analyst_01,
    hr_partner_01,
    run_knowledge_scenario,
)
from controlplane.scenarios.refund import run_refund_scenario


def test_acl_mismatch_is_entitlement_violation():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "r",
        Principal(id="customer-bot", clearance=frozenset({"public"})),
        "show",
    )
    sid = rec.record_step(led, StepKind.RETRIEVAL, "hr_doc")
    span = rec.record_span(
        led,
        sid,
        source_id="doc:hr-salary",
        acl=frozenset({"hr-confidential"}),
        content="Employee compensation band L5.",
    )
    rec.finish_context_assembly(led)
    claim = Claim(
        "c1",
        "Employee compensation band L5.",
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
        role_in_action={"show": 1.0},
    )
    bind_claims(led, [claim], fixture_map={"c1": (span,)})
    finding = audit_claim(led, "c1")
    assert finding.violated is True
    assert span in finding.offending_span_ids
    assert "ENTITLEMENT_VIOLATION" in finding.detail


def test_acl_subset_is_not_violation():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "r",
        Principal(
            id="hr-bot",
            clearance=frozenset({"public", "hr-confidential"}),
        ),
        "show",
    )
    sid = rec.record_step(led, StepKind.RETRIEVAL, "hr_doc")
    span = rec.record_span(
        led,
        sid,
        source_id="doc:hr-salary",
        acl=frozenset({"hr-confidential"}),
        content="Employee compensation band L5.",
    )
    rec.finish_context_assembly(led)
    claim = Claim(
        "c1",
        "Employee compensation band L5.",
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
        role_in_action={"show": 1.0},
    )
    bind_claims(led, [claim], fixture_map={"c1": (span,)})
    finding = audit_claim(led, "c1")
    assert finding.violated is False
    assert finding.offending_span_ids == ()


def test_refund_fin_internal_excludes_agent():
    led = run_refund_scenario()
    finding = audit_claim(led, "internal_note")
    assert finding.violated is True
    assert "refund_agent" in led.principal.clearance
    fin = [s for s in led.spans.values() if s.source_id == "FIN-INTERNAL-NOTE"]
    assert len(fin) == 1
    assert not fin[0].acl.issubset(led.principal.clearance)


def test_knowledge_principal_flip_entitlement():
    bad = run_knowledge_scenario(analyst_01())
    good = run_knowledge_scenario(hr_partner_01())
    assert audit_claim(bad, "l6_band").violated is True
    assert audit_claim(good, "l6_band").violated is False
