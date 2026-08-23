import pytest
from controlplane.interlock import MATRIX, decide
from controlplane.ledger import EvidenceLedger
from controlplane.models import (
    Action, Actuator, AssertionStrength, Binding, BlastTier, Claim, ClaimKind,
    EntitlementFinding, Principal, Verdict,
)


def _led():
    return EvidenceLedger.begin("r", Principal(id="u", clearance=frozenset()), "x")


def test_r3_unsupported_categorical_escalates():
    led = _led()
    led.claims["c"] = Claim("c", "Clause 7.2 permits refund", ClaimKind.STRUCTURAL,
                            AssertionStrength.CATEGORICAL, {"refund": 1.0})
    led.bindings["c"] = Binding("c", (), "none", Verdict.UNSUPPORTED)
    action = Action("refund", "issue_refund", BlastTier.R3, irreversibility=True)
    d = decide(led, action)
    assert d.actuator == Actuator.ESCALATE
    assert d.matrix_col == "Unsupported + categorical"


def test_r1_entitlement_edits():
    led = _led()
    led.claims["c"] = Claim("c", "secret", ClaimKind.TEXTUAL,
                            AssertionStrength.CATEGORICAL, {"show": 1.0})
    led.bindings["c"] = Binding("c", ("s1",), "fixture", Verdict.SUPPORTED)
    # mark entitlement via special binding note: interlock reads findings passed in ledger decisions helper
    # decide() must accept optional findings map — see implementation
    action = Action("show", "show_text", BlastTier.R1)
    d = decide(led, action, findings={"c": EntitlementFinding("c", True, ("s1",), "acl")})
    assert d.actuator == Actuator.EDIT


@pytest.mark.parametrize(
    "tier,col,expected",
    [
        (BlastTier.R3, "Contradicted / entitlement violation", Actuator.BLOCK),
        (BlastTier.R3, "Unsupported + categorical", Actuator.ESCALATE),
        (BlastTier.R3, "Unsupported + hedged", Actuator.ESCALATE),
        (BlastTier.R3, "Unknown", Actuator.ESCALATE),
        (BlastTier.R2, "Contradicted / entitlement violation", Actuator.BLOCK),
        (BlastTier.R2, "Unsupported + categorical", Actuator.EDIT),
        (BlastTier.R2, "Unsupported + hedged", Actuator.EDIT),
        (BlastTier.R2, "Unknown", Actuator.ESCALATE),
        (BlastTier.R1, "Contradicted / entitlement violation", Actuator.EDIT),
        (BlastTier.R1, "Unsupported + categorical", Actuator.EDIT),
        (BlastTier.R1, "Unsupported + hedged", Actuator.PASS_ANNOTATE),
        (BlastTier.R1, "Unknown", Actuator.PASS_ANNOTATE),
        (BlastTier.R0, "Contradicted / entitlement violation", Actuator.PASS_ANNOTATE),
        (BlastTier.R0, "Unsupported + categorical", Actuator.PASS_ANNOTATE),
        (BlastTier.R0, "Unsupported + hedged", Actuator.PASS),
        (BlastTier.R0, "Unknown", Actuator.PASS),
    ],
)
def test_matrix_transcribed_never_redrawn(tier, col, expected):
    assert MATRIX[(tier, col)] == expected


def test_supported_not_violated_is_pass():
    led = _led()
    led.claims["c"] = Claim("c", "ok", ClaimKind.TEXTUAL,
                            AssertionStrength.CATEGORICAL, {"show": 1.0})
    led.bindings["c"] = Binding("c", ("s1",), "fixture", Verdict.SUPPORTED)
    d = decide(led, Action("show", "show_text", BlastTier.R3))
    assert d.actuator == Actuator.PASS


def test_worst_claim_among_role_in_action():
    led = _led()
    led.claims["ok"] = Claim("ok", "ok", ClaimKind.TEXTUAL,
                             AssertionStrength.CATEGORICAL, {"refund": 1.0})
    led.bindings["ok"] = Binding("ok", ("s",), "fixture", Verdict.SUPPORTED)
    led.claims["ghost"] = Claim("ghost", "Clause 7.2 permits refund", ClaimKind.STRUCTURAL,
                                AssertionStrength.CATEGORICAL, {"refund": 1.0})
    led.bindings["ghost"] = Binding("ghost", (), "none", Verdict.UNSUPPORTED)
    led.claims["other"] = Claim("other", "secret", ClaimKind.TEXTUAL,
                                AssertionStrength.CATEGORICAL, {"show": 1.0})
    led.bindings["other"] = Binding("other", ("s1",), "fixture", Verdict.CONTRADICTED)
    d = decide(led, Action("refund", "issue_refund", BlastTier.R3, irreversibility=True))
    assert d.actuator == Actuator.ESCALATE
    assert d.driving_claim_ids == ("ghost",)
    assert d.matrix_col == "Unsupported + categorical"
