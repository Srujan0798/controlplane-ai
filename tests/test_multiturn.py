from controlplane.models import Actuator
from controlplane.scenarios.multiturn import run_multiturn_compounding


def test_multiturn_turn1_unchanged_turn3_escalates():
    led1, led3 = run_multiturn_compounding()
    assert led1.decisions["show_reply"].actuator == Actuator.PASS_ANNOTATE
    assert led1.decisions["show_reply"].matrix_row == "R1"
    # Turn 3 re-evaluates the inherited hedged claim at R3 → Escalate
    assert led3.decisions["issue_refund"].actuator == Actuator.ESCALATE
    assert led3.decisions["issue_refund"].matrix_row == "R3"
    assert "warranty_hedge" in led3.decisions["issue_refund"].driving_claim_ids
    assert led1.verify_chain() and led3.verify_chain()
