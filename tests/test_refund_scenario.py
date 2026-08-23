from controlplane.models import Actuator, Verdict
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
    assert all("7.2" not in span.content for span in led.spans.values())


def test_show_text_driven_by_entitlement():
    led = run_refund_scenario()
    d = led.decisions["show_text"]
    assert d.actuator == Actuator.EDIT
    assert d.matrix_row == "R1"
    assert d.matrix_col == "Contradicted / entitlement violation"
    assert "hr_side" in d.driving_claim_ids


def test_refund_held_not_blocked():
    led = run_refund_scenario()
    d = led.decisions["issue_refund"]
    assert d.actuator == Actuator.ESCALATE
    assert d.actuator != Actuator.BLOCK
    assert d.matrix_row == "R3"
    assert d.matrix_col == "Unsupported + categorical"
    assert d.driving_claim_ids == ("clause_72",)


def test_principal_excludes_hr_and_hr_span_is_present():
    led = run_refund_scenario()
    assert led.principal.clearance == frozenset({"vendor-public"})
    assert "hr-confidential" not in led.principal.clearance
    hr_spans = [s for s in led.spans.values() if "hr-confidential" in s.acl]
    assert len(hr_spans) == 1
    assert led.bindings["hr_side"].span_ids == (hr_spans[0].span_id,)
    assert led.bindings["amount"].verdict == Verdict.SUPPORTED
