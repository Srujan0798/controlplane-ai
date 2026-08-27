from controlplane.binder import bind_claims
from controlplane.models import (
    AssertionStrength, Claim, ClaimKind, Principal, StepKind, Verdict,
)
from controlplane.recorder import ProvenanceRecorder


def _ledger_with_span(content: str, acl=frozenset({"public"})):
    rec = ProvenanceRecorder()
    led = rec.begin_request("r", Principal(id="u", clearance=frozenset({"public"})), "t")
    sid = rec.record_step(led, StepKind.RETRIEVAL, "search")
    rec.record_span(led, sid, source_id="doc:1", acl=acl, content=content)
    rec.finish_context_assembly(led)
    return led


def test_default_unsupported_when_no_match():
    led = _ledger_with_span("Clause 4.1 covers shipping.")
    claim = Claim("c1", "Clause 7.2 permits this refund", ClaimKind.STRUCTURAL,
                  AssertionStrength.CATEGORICAL)
    bindings = bind_claims(led, [claim])
    assert bindings[0].verdict == Verdict.UNSUPPORTED
    assert bindings[0].span_ids == ()


def test_fixture_binding_supports():
    led = _ledger_with_span("Refund amount for order ORD-9 is 184000 INR.")
    span_id = next(iter(led.spans))
    claim = Claim("c2", "Refund is ₹1,84,000", ClaimKind.NUMERIC,
                  AssertionStrength.CATEGORICAL)
    bindings = bind_claims(led, [claim], fixture_map={"c2": (span_id,)})
    assert bindings[0].verdict == Verdict.SUPPORTED


def test_derived_never_supported_by_shallow_match():
    led = _ledger_with_span("A is 2. B is 3.")
    claim = Claim("c3", "A+B is 5", ClaimKind.DERIVED, AssertionStrength.CATEGORICAL)
    bindings = bind_claims(led, [claim])
    assert bindings[0].verdict == Verdict.UNKNOWN
