from controlplane.binder import bind_claims
from controlplane.entitlement import audit_claim
from controlplane.models import (
    AssertionStrength, Claim, ClaimKind, Principal, StepKind,
)
from controlplane.recorder import ProvenanceRecorder


def test_acl_mismatch_is_entitlement_violation():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "r", Principal(id="customer-bot", clearance=frozenset({"public"})), "show",
    )
    sid = rec.record_step(led, StepKind.RETRIEVAL, "hr_doc")
    span = rec.record_span(
        led, sid, source_id="doc:hr-salary", acl=frozenset({"hr-confidential"}),
        content="Employee compensation band L5.",
    )
    rec.finish_context_assembly(led)
    claim = Claim("c1", "Employee compensation band L5.", ClaimKind.TEXTUAL,
                  AssertionStrength.CATEGORICAL, role_in_action={"show": 1.0})
    bind_claims(led, [claim], fixture_map={"c1": (span,)})
    finding = audit_claim(led, "c1")
    assert finding.violated is True
    assert span in finding.offending_span_ids


def test_acl_subset_is_not_violation():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "r", Principal(id="hr-bot", clearance=frozenset({"public", "hr-confidential"})), "show",
    )
    sid = rec.record_step(led, StepKind.RETRIEVAL, "hr_doc")
    span = rec.record_span(
        led, sid, source_id="doc:hr-salary", acl=frozenset({"hr-confidential"}),
        content="Employee compensation band L5.",
    )
    rec.finish_context_assembly(led)
    claim = Claim("c1", "Employee compensation band L5.", ClaimKind.TEXTUAL,
                  AssertionStrength.CATEGORICAL, role_in_action={"show": 1.0})
    bind_claims(led, [claim], fixture_map={"c1": (span,)})
    finding = audit_claim(led, "c1")
    assert finding.violated is False
    assert finding.offending_span_ids == ()
