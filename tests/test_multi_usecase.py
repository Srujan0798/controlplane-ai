from controlplane.models import Actuator, AssertionStrength, Verdict
from controlplane.scenarios.multi_usecase import (
    run_acl_violation_refund,
    run_customer_support,
    run_decision_refund,
    run_knowledge_copilot,
)


def test_three_distinct_actuators_from_three_ledgers():
    support = run_customer_support()
    copilot = run_knowledge_copilot()
    refund = run_decision_refund()

    assert support.request_id != copilot.request_id != refund.request_id
    actuators = {
        support.decisions["show_reply"].actuator,
        copilot.decisions["draft_partner_email"].actuator,
        refund.decisions["issue_refund"].actuator,
    }
    assert actuators == {Actuator.PASS_ANNOTATE, Actuator.EDIT, Actuator.ESCALATE}
    assert support.decisions["show_reply"].actuator == Actuator.PASS_ANNOTATE
    assert copilot.decisions["draft_partner_email"].actuator == Actuator.EDIT
    assert refund.decisions["issue_refund"].actuator == Actuator.ESCALATE
    assert support.verify_chain() is True
    assert copilot.verify_chain() is True
    assert refund.verify_chain() is True


def test_support_r1_unsupported_hedged_pass_annotate():
    led = run_customer_support()
    d = led.decisions["show_reply"]
    assert d.actuator == Actuator.PASS_ANNOTATE
    assert d.matrix_row == "R1"
    assert d.matrix_col == "Unsupported + hedged"
    claim_id = d.driving_claim_ids[0]
    assert led.bindings[claim_id].verdict == Verdict.UNSUPPORTED
    assert led.claims[claim_id].assertion == AssertionStrength.HEDGED


def test_copilot_r2_unsupported_categorical_edit():
    led = run_knowledge_copilot()
    d = led.decisions["draft_partner_email"]
    assert d.actuator == Actuator.EDIT
    assert d.matrix_row == "R2"
    assert d.matrix_col == "Unsupported + categorical"
    claim_id = d.driving_claim_ids[0]
    assert led.bindings[claim_id].verdict == Verdict.UNSUPPORTED
    assert led.claims[claim_id].assertion == AssertionStrength.CATEGORICAL


def test_refund_r3_unsupported_categorical_escalate():
    led = run_decision_refund()
    d = led.decisions["issue_refund"]
    assert d.actuator == Actuator.ESCALATE
    assert d.matrix_row == "R3"
    assert d.matrix_col == "Unsupported + categorical"
    claim_id = d.driving_claim_ids[0]
    assert led.bindings[claim_id].verdict == Verdict.UNSUPPORTED
    assert led.claims[claim_id].assertion == AssertionStrength.CATEGORICAL
    assert all("7.2" not in span.content for span in led.spans.values())
    # F7: mixed-ACL set present — principal cannot read hr-confidential
    assert led.principal.clearance == frozenset({"vendor-public"})
    assert any("hr-confidential" in s.acl for s in led.spans.values())


def test_acl_violation_route_blocks_at_r3():
    led = run_acl_violation_refund()
    d = led.decisions["issue_refund"]
    assert d.actuator == Actuator.BLOCK
    assert d.matrix_row == "R3"
    assert "Contradicted" in d.matrix_col or "entitlement" in d.matrix_col.lower()
