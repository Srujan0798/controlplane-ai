from controlplane.models import Actuator, BlastTier, EvidencePacket, Verdict


def test_enums_exist():
    assert BlastTier.R3.value == "R3"
    assert Verdict.UNSUPPORTED.value == "UNSUPPORTED"
    assert Actuator.ESCALATE.value == "Escalate"


def test_evidence_packet_fields():
    packet = EvidencePacket(
        claim_id="clause_72",
        claim_text="under clause 7.2",
        verdict="UNSUPPORTED",
        candidate_span_ids=(),
        proposed_actuator="Escalate",
        action_id="issue_refund",
    )
    assert packet.candidate_span_ids == ()
    assert packet.proposed_actuator == "Escalate"
