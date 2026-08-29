"""TDD for the content-law checkers themselves.

ARCHITECTURE.md §10 records nine facts that seven models corrupted repeatedly
across five adversarial merges. `tests/test_content_laws.py` applies these
checkers to the real corpus and is expected to stay green — which means it
proves nothing on its own. A guard that has never been seen to fail is
decoration.

This suite is the proof. Every checker is fed text that violates its law and
must catch it, then text that obeys the law and must stay silent.
"""
from __future__ import annotations

import pytest

from controlplane import lawcheck


# --- Law 1: clause 7.2 does not exist. Absence, never conflict. -------------

def test_law1_catches_clause_72_described_as_capping():
    text = "The agent cited clause 7.2, which caps refunds at 50,000."
    violations = lawcheck.check_clause_absence(text, source="deck.md")
    assert violations, "clause 7.2 'caps' must be caught — the failure is absence"
    assert violations[0].law == 1


@pytest.mark.parametrize(
    "verb",
    ["denies", "does not cover", "limits", "excludes", "prohibits", "covers"],
)
def test_law1_catches_every_conflict_verb(verb):
    text = f"Clause 7.2 {verb} this refund."
    assert lawcheck.check_clause_absence(text, source="x.md")


def test_law1_allows_clause_72_described_as_absent():
    text = (
        "Clause 7.2 does not exist. The claim finds no span, so it stays "
        "UNSUPPORTED and the refund is held."
    )
    assert lawcheck.check_clause_absence(text, source="x.md") == []


def test_law1_ignores_other_clauses():
    text = "Clause 4.1 covers shipping delays and restocking."
    assert lawcheck.check_clause_absence(text, source="x.md") == []


# --- Law 2: never say "blocked" about the refund ----------------------------

def test_law2_catches_blocked_refund():
    text = "The unproven claim means the refund is blocked."
    violations = lawcheck.check_refund_never_blocked(text, source="x.md")
    assert violations
    assert violations[0].law == 2


def test_law2_catches_commit_blocked():
    assert lawcheck.check_refund_never_blocked(
        "COMMIT BLOCKED — refund halted.", source="x.md"
    )


def test_law2_allows_held_and_escalated():
    text = "The refund is held and escalated with the evidence packet."
    assert lawcheck.check_refund_never_blocked(text, source="x.md") == []


def test_law2_allows_block_far_from_refund():
    text = (
        "Block is the actuator at R3 x contradicted.\n\n"
        "Separately, the refund is escalated."
    )
    assert lawcheck.check_refund_never_blocked(text, source="x.md") == []


# --- Law 3: the company pays. The customer does not lose money. -------------

def test_law3_catches_inverted_victim():
    text = "The customer lost 1,84,000 because the agent approved the refund."
    violations = lawcheck.check_who_loses_money(text, source="x.md")
    assert violations
    assert violations[0].law == 3


def test_law3_catches_denied_refund_premise():
    assert lawcheck.check_who_loses_money(
        "The refund was denied on the basis of clause 7.2.", source="x.md"
    )


def test_law3_allows_company_wrongly_pays():
    text = "The company wrongly pays 1,84,000. The money moved Tuesday."
    assert lawcheck.check_who_loses_money(text, source="x.md") == []


# --- Law 4: the matrix is transcribed, never redrawn ------------------------

def test_law4_matrix_matches_the_transcription():
    """The 16 frozen cells, compared against a literal held here.

    Six of seven models corrupted this matrix when asked to redraw it.
    """
    assert lawcheck.check_matrix_transcription() == []


def test_law4_detects_a_redrawn_cell():
    """Flattening the R3 row to Block is the exact corruption observed."""
    corrupted = dict(lawcheck.FROZEN_MATRIX)
    corrupted[("R3", lawcheck.COL_UNSUPPORTED_CATEGORICAL)] = "Block"
    violations = lawcheck.check_matrix_transcription(actual=corrupted)
    assert violations
    assert violations[0].law == 4


def test_law4_detects_a_missing_cell():
    truncated = {
        k: v for k, v in lawcheck.FROZEN_MATRIX.items() if k[0] != "R0"
    }
    assert lawcheck.check_matrix_transcription(actual=truncated)


# --- Law 5: exactly five actuators; the rest are invented -------------------

def test_law5_actuator_enum_is_exactly_five():
    assert lawcheck.check_actuator_enum() == []


@pytest.mark.parametrize(
    "invented",
    ["Kill Span", "Terminate Step", "Hold & Re-verify", "Redact & Flag"],
)
def test_law5_catches_invented_actuators(invented):
    text = f"The gate emits {invented} when the claim fails."
    violations = lawcheck.check_no_invented_actuators(text, source="x.md")
    assert violations, f"{invented!r} is invented and must be caught"
    assert violations[0].law == 5


def test_law5_allows_naming_an_invented_actuator_to_reject_it():
    """ARCHITECTURE.md §10 names them precisely so they stay cut."""
    text = "`Kill Span` and `Terminate Step` are invented. Cut."
    assert lawcheck.check_no_invented_actuators(text, source="x.md") == []


def test_law5_allows_the_five_real_actuators():
    text = "Actuators are Block, Edit, Escalate, Pass and Pass + annotate."
    assert lawcheck.check_no_invented_actuators(text, source="x.md") == []


# --- Law 6: never quote 40ms as p95 ----------------------------------------

def test_law6_catches_40ms_as_p95():
    text = "The gate adds 40ms p95 on user-visible text."
    violations = lawcheck.check_latency_claim(text, source="x.md")
    assert violations
    assert violations[0].law == 6


def test_law6_catches_the_reversed_order():
    assert lawcheck.check_latency_claim("p95 of 40 ms", source="x.md")


def test_law6_allows_the_correct_pairing():
    text = "Targets are 40ms p50 and 200ms p95."
    assert lawcheck.check_latency_claim(text, source="x.md") == []


def test_law6_allows_a_warning_about_the_error():
    text = "Never quote 40ms as p95 — that is a five-fold overclaim."
    assert lawcheck.check_latency_claim(text, source="x.md") == []


# --- Law 7: the gate report is an empty schema, never fabricated numbers ----

def test_law7_catches_a_fabricated_fnr():
    text = "On this route we catch 94% of ungrounded claims at 40ms p50."
    violations = lawcheck.check_no_fabricated_rates(text, source="x.md")
    assert violations
    assert violations[0].law == 7


def test_law7_allows_the_typed_placeholder():
    text = (
        "On this route we catch <measured>% of ungrounded claims at 40ms p50 "
        "— and here is the <measured>% we don't."
    )
    assert lawcheck.check_no_fabricated_rates(text, source="x.md") == []


def test_law7_allows_a_measured_rate_marked_as_measured():
    """After `make eval` runs, real numbers are legal if labelled as measured."""
    text = "Measured on the eval corpus: FNR 12.4% (95% CI 8.1-18.2)."
    assert lawcheck.check_no_fabricated_rates(text, source="x.md") == []


# --- Law 8: the refuse-to-claim list is about us ----------------------------

def test_law8_catches_a_missing_refuse_list():
    text = "We reject LLM-as-judge, cosine thresholds and composite risk scores."
    violations = lawcheck.check_refuse_to_claim_present(text, source="x.md")
    assert violations
    assert violations[0].law == 8


def test_law8_allows_a_self_directed_refuse_list():
    text = (
        "What we refuse to claim: we do not eliminate hallucinations, we are "
        "not zero integration, we are not zero latency, and we will not give "
        "you one accuracy number."
    )
    assert lawcheck.check_refuse_to_claim_present(text, source="x.md") == []


# --- Law 9: do not drop bias ------------------------------------------------

def test_law9_catches_a_missing_bias_section():
    text = "Responsibility covers leakage and safety interlocks."
    violations = lawcheck.check_bias_present(text, source="x.md")
    assert violations
    assert violations[0].law == 9


def test_law9_allows_bias_stated_in_measurement_terms():
    text = (
        "Bias is counterfactual invariance measured as decision flip rate "
        "with a confidence interval over a rolling window."
    )
    assert lawcheck.check_bias_present(text, source="x.md") == []


# --- The registry -----------------------------------------------------------

def test_all_nine_laws_are_registered():
    assert sorted(lawcheck.LAWS) == list(range(1, 10))


def test_every_law_has_a_name():
    assert all(name.strip() for name in lawcheck.LAWS.values())


def test_check_text_runs_every_text_checker():
    """One violating passage should trip more than one law at once."""
    text = "Clause 7.2 caps the refund, so the refund is blocked at 40ms p95."
    violations = lawcheck.check_text(text, source="x.md")
    tripped = {v.law for v in violations}
    assert {1, 2, 6} <= tripped


def test_violation_carries_a_locatable_excerpt():
    text = "line one\nline two\nClause 7.2 caps refunds.\nline four"
    (violation,) = lawcheck.check_clause_absence(text, source="deck.md")
    assert violation.source == "deck.md"
    assert violation.line == 3
    assert "7.2" in violation.excerpt


# --- Teaching the law is not breaking it -----------------------------------
#
# The corpus is largely drill material: hostile-QA tables, kill-shot cards and
# pre-flight checklists that quote the banned phrasing precisely so a presenter
# never says it. A checker that cannot tell a correction from a violation floods
# the suite and gets switched off, which is the alert-fatigue failure the
# architecture warns about. Every law therefore recognises its own corrective.


def test_law1_allows_a_correction_pair():
    """docs/reference/KILL_SHOT.md pairs the wrong phrasing with the right one."""
    text = '| "Clause 7.2 caps / denies." | "Clause 7.2 does not exist." |'
    assert lawcheck.check_clause_absence(text, source="x.md") == []


def test_law2_allows_a_correction_pair():
    text = '| "We blocked the refund." | "Refund held and escalated." |'
    assert lawcheck.check_refund_never_blocked(text, source="x.md") == []


def test_law2_allows_the_user_surface_three_states():
    """Verified / Uncertain / Blocked is the user surface, not the refund verdict."""
    text = "| Per-claim surface | Verified / Uncertain / Blocked; refund = Held/Escalate |"
    assert lawcheck.check_refund_never_blocked(text, source="x.md") == []


def test_law2_allows_code_referencing_the_block_actuator():
    """`Actuator.BLOCK` is the enum member's real name, not a claim about a refund."""
    text = "action_allowed = not (refund.actuator in (Actuator.ESCALATE, Actuator.BLOCK))"
    assert lawcheck.check_refund_never_blocked(text, source="pipeline.py") == []


def test_law3_allows_a_correction_pair():
    text = "| Customer lost money | Company wrongly paid out — found Friday. |"
    assert lawcheck.check_who_loses_money(text, source="x.md") == []


def test_law6_allows_a_correction_pair():
    text = '| "40 ms p95." | "40 ms p50 / 200 ms p95 targets." |'
    assert lawcheck.check_latency_claim(text, source="x.md") == []


def test_law7_allows_an_explicitly_empty_fnr():
    text = "| 0 — Prototype | Two live routes; ledger >=60%; empty FNR |"
    assert lawcheck.check_no_fabricated_rates(text, source="x.md") == []


@pytest.mark.parametrize("prefix", ["No", "Do not", "Don't", "Never"])
def test_prohibitions_are_not_violations(prefix):
    text = f'{prefix} quote 40ms as p95.'
    assert lawcheck.check_latency_claim(text, source="x.md") == []


def test_exemption_reaches_across_a_wrapped_sentence():
    """ARCHITECTURE.md wraps its list of invented actuators across two lines."""
    text = (
        "Actuators are exactly Block, Edit, Escalate and Pass.\n"
        "`Kill Span`, `Terminate Step`, `Hold & Re-verify`, `Redact & Flag`\n"
        "are all invented. Cut."
    )
    assert lawcheck.check_no_invented_actuators(text, source="x.md") == []


def test_a_violation_two_lines_from_a_prohibition_is_still_caught():
    """The window is one line, not a blanket amnesty for the whole file."""
    text = (
        "Never invent an actuator.\n"
        "filler line one\n"
        "filler line two\n"
        "The gate emits Kill Span when the claim fails."
    )
    violations = lawcheck.check_no_invented_actuators(text, source="x.md")
    assert violations
    assert violations[0].line == 4


def test_law7_allows_a_quoted_claim_under_criticism():
    """docs/reference/NARRATIVE.md quotes the industry's boast in order to reject it."""
    text = (
        '**"99% accuracy detecting bias, safety and risk."** One accuracy number\n'
        "across three incommensurable failure modes is a demo artifact."
    )
    assert lawcheck.check_no_fabricated_rates(text, source="x.md") == []


def test_law7_still_catches_an_unquoted_rate():
    text = "We catch 94% of ungrounded claims."
    assert lawcheck.check_no_fabricated_rates(text, source="x.md")


# A heading scopes everything beneath it. "Boundary — out" and "Rejected
# approaches" sections exist to enumerate what the system does NOT do, and the
# enumeration necessarily spells out the forbidden phrasing. The prohibition
# sits in the heading, which may be many lines above the item.

def test_a_boundary_section_exempts_the_items_it_lists():
    text = (
        "### Boundary — out\n"
        "\n"
        "Third live bias route · per-response bias · LLM-as-judge primary · "
        'confidence scores · calling refund "blocked."\n'
    )
    assert lawcheck.check_refund_never_blocked(text, source="x.md") == []


def test_an_ordinary_heading_does_not_exempt():
    text = (
        "### How the gate behaves\n"
        "\n"
        "filler\n"
        "The refund is blocked when the claim fails.\n"
    )
    violations = lawcheck.check_refund_never_blocked(text, source="x.md")
    assert violations
    assert violations[0].line == 4


def test_a_later_ordinary_heading_ends_the_exemption():
    """Leaving a boundary section must restore enforcement."""
    text = (
        "### Boundary — out\n"
        'calling refund "blocked."\n'
        "\n"
        "### Behaviour\n"
        "\n"
        "filler\n"
        "The refund is blocked when the claim fails.\n"
    )
    violations = lawcheck.check_refund_never_blocked(text, source="x.md")
    assert [v.line for v in violations] == [7]


def test_law8_accepts_the_hyphenated_spelling():
    """round2/CONTROLPLANE_R2_FINAL.md writes it `Refuse-to-claim`."""
    text = (
        "| **Refuse-to-claim** | No: eliminate hallucinations, zero integration, "
        "zero added latency, one accuracy number. |"
    )
    assert lawcheck.check_refuse_to_claim_present(text, source="x.md") == []
