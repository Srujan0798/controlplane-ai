import pytest
from controlplane.models import Principal, StepKind
from controlplane.recorder import ProvenanceRecorder


def test_records_span_with_hash_and_freezes():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        request_id="r1",
        principal=Principal(id="agent", clearance=frozenset({"vendor-public"})),
        action_intent="refund",
    )
    sid = rec.record_step(led, StepKind.RETRIEVAL, "policy_search")
    span_id = rec.record_span(
        led, sid, source_id="doc:vendor-v3", acl=frozenset({"vendor-public"}),
        content="Clause 4.1 covers shipping delays.",
    )
    assert span_id in led.spans
    assert led.spans[span_id].content_hash
    rec.finish_context_assembly(led)
    with pytest.raises(RuntimeError, match="frozen"):
        rec.record_span(
            led, sid, source_id="doc:x", acl=frozenset({"vendor-public"}), content="late",
        )
