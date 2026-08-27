from controlplane.models import BlastTier, Verdict, Actuator


def test_enums_exist():
    assert BlastTier.R3.value == "R3"
    assert Verdict.UNSUPPORTED.value == "UNSUPPORTED"
    assert Actuator.ESCALATE.value == "Escalate"
