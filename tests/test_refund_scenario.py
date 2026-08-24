from controlplane.mock_refund import execute_refund
from controlplane.models import Actuator, EvidencePacket, Verdict
from controlplane.scenarios.knowledge import run_principal_flip
from controlplane.scenarios.refund import run_refund_scenario


def test_dual_action_edit_and_escalate():
    led = run_refund_scenario()
    assert led.decisions["show_text"].actuator == Actuator.EDIT
    assert led.decisions["issue_refund"].actuator == Actuator.ESCALATE
    assert led.verify_chain() is True


def test_clause_72_is_absence_not_contradiction():
    led = run_refund_scenario()
    binding = led.bindings["clause_72"]
    assert binding.verdict == Verdict.UNSUPPORTED
    assert binding.span_ids == ()
    # Corpus law: no clause 7.2 in AGR-VENDOR-v3 content
    agr = [s for s in led.spans.values() if s.source_id == "AGR-VENDOR-v3"]
    assert agr
    assert "7.2" not in agr[0].content
    assert all(
        "7.2" not in s.content
        for s in led.spans.values()
        if s.source_id != "INJECT-NOTICE"
    )


def test_show_text_driven_by_entitlement():
    led = run_refund_scenario()
    d = led.decisions["show_text"]
    assert d.actuator == Actuator.EDIT
    assert d.matrix_row == "R1"
    assert d.matrix_col == "Contradicted / entitlement violation"
    assert "internal_note" in d.driving_claim_ids


def test_refund_held_not_blocked():
    led = run_refund_scenario()
    d = led.decisions["issue_refund"]
    assert d.actuator == Actuator.ESCALATE
    assert d.actuator != Actuator.BLOCK
    assert d.matrix_row == "R3"
    assert d.matrix_col == "Unsupported + categorical"
    assert d.driving_claim_ids == ("clause_72",)
    assert isinstance(d.packet, EvidencePacket)
    assert d.packet.candidate_span_ids == ()

    result = execute_refund(allowed=(d.actuator == Actuator.PASS))
    assert result["committed"] is False
    assert result["status"] == "REFUND HELD"
    assert "BLOCK" not in result["status"].upper()


def test_principal_and_frozen_sources():
    led = run_refund_scenario()
    assert led.principal.id == "agent_refund_7"
    assert led.principal.clearance == frozenset({"refund_agent"})
    sources = {s.source_id for s in led.spans.values()}
    assert sources == {
        "AGR-VENDOR-v3",
        "ORD-1023",
        "FIN-INTERNAL-NOTE",
        "INJECT-NOTICE",
    }
    assert led.bindings["amount"].verdict == Verdict.SUPPORTED


def test_mock_refund_vocabulary():
    held = execute_refund(False)
    committed = execute_refund(True)
    assert held == {"committed": False, "status": "REFUND HELD"}
    assert committed == {"committed": True, "status": "REFUND COMMITTED"}


def test_knowledge_flip_edit_vs_pass():
    unauthorized, entitled = run_principal_flip()
    assert unauthorized.decisions["show_text"].actuator == Actuator.EDIT
    assert entitled.decisions["show_text"].actuator == Actuator.PASS
