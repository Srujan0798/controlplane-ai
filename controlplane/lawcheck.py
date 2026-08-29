"""Content-law checkers — ARCHITECTURE.md §10, made executable.

Nine facts were corrupted repeatedly across five adversarial merges: seven
models tested them against each other and each fact was broken by at least one.
Prose in a spec cannot stop that from happening again. These checkers can.

Two suites consume this module:

* `tests/test_lawcheck.py` proves each checker can fail, by feeding it text that
  violates its law.
* `tests/test_content_laws.py` applies them to the real corpus — code, docs, and
  the sources that generate the proposal PDF and the pitch deck.

Text checkers take `(text, source=...)` and return `list[Violation]` carrying a
line number, so a failure points at a line rather than a file. Laws 8 and 9 are
document-level presence checks and are excluded from `check_text`; applying them
to a snippet would flag every snippet.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# --- The frozen matrix, transcribed. Never redrawn. -------------------------

COL_CONTRADICTED = "Contradicted / entitlement violation"
COL_UNSUPPORTED_CATEGORICAL = "Unsupported + categorical"
COL_UNSUPPORTED_HEDGED = "Unsupported + hedged"
COL_UNKNOWN = "Unknown"

FROZEN_MATRIX: dict[tuple[str, str], str] = {
    ("R3", COL_CONTRADICTED): "Block",
    ("R3", COL_UNSUPPORTED_CATEGORICAL): "Escalate",
    ("R3", COL_UNSUPPORTED_HEDGED): "Escalate",
    ("R3", COL_UNKNOWN): "Escalate",
    ("R2", COL_CONTRADICTED): "Block",
    ("R2", COL_UNSUPPORTED_CATEGORICAL): "Edit",
    ("R2", COL_UNSUPPORTED_HEDGED): "Edit",
    ("R2", COL_UNKNOWN): "Escalate",
    ("R1", COL_CONTRADICTED): "Edit",
    ("R1", COL_UNSUPPORTED_CATEGORICAL): "Edit",
    ("R1", COL_UNSUPPORTED_HEDGED): "Pass + annotate",
    ("R1", COL_UNKNOWN): "Pass + annotate",
    ("R0", COL_CONTRADICTED): "Pass + annotate",
    ("R0", COL_UNSUPPORTED_CATEGORICAL): "Pass + annotate",
    ("R0", COL_UNSUPPORTED_HEDGED): "Pass",
    ("R0", COL_UNKNOWN): "Pass",
}

REAL_ACTUATORS = ("Pass", "Pass + annotate", "Edit", "Escalate", "Block")

LAWS: dict[int, str] = {
    1: "Clause 7.2 does not exist — absence, never conflict",
    2: "The refund is held and escalated, never blocked",
    3: "The company wrongly pays; the customer does not lose money",
    4: "The matrix is transcribed, never redrawn",
    5: "Exactly five actuators; the rest are invented",
    6: "Latency is 40ms p50 / 200ms p95 — never 40ms as p95",
    7: "The gate report is an empty schema, never fabricated numbers",
    8: "The refuse-to-claim list is about us",
    9: "Bias is kept, stated in measurement terms",
}


@dataclass(frozen=True)
class Violation:
    law: int
    name: str
    source: str
    line: int
    excerpt: str
    detail: str


# --- Shared machinery -------------------------------------------------------

# Most of this corpus is drill material — hostile-QA tables, kill-shot cards,
# pre-flight checklists — that quotes the banned phrasing precisely so nobody
# says it in a room. A checker that cannot tell a correction from a violation
# floods the suite, and a flooded suite gets switched off. That is the
# alert-fatigue failure the architecture warns about, reproduced in our own
# tooling. Two mechanisms keep it out: a prohibition marker anywhere in a
# one-line window, and a per-law corrective (below) on the line itself.
# Deliberately not here: a bare "not", which appears inside the very phrasings
# these laws forbid ("clause 7.2 does not cover"), and a bare "verify", which
# hides inside the invented actuator "Hold & Re-verify". Both were tried and
# both silenced real violations.
_EXEMPT = re.compile(
    r"\b(never|no|don'?t|do\s+not|does\s+not\s+appear|must\s+not|avoid|"
    r"invent\w*|rejected|cut|forbidden|banned|wrong|incorrect|corrupt\w*|"
    r"refuse\w*|content\s+law|law\s*#?\d)\b",
    re.IGNORECASE,
)

# How far the prohibition may sit from the phrase it forbids. One line, because
# ARCHITECTURE.md wraps its list of invented actuators mid-sentence — and no
# further, or a single "never" near the top would absolve a whole file.
_WINDOW = 1


def _exempt(lines: list[str], index: int) -> bool:
    lo = max(0, index - _WINDOW)
    hi = min(len(lines), index + _WINDOW + 1)
    return any(_EXEMPT.search(lines[i]) for i in range(lo, hi))


# A heading scopes everything beneath it. "Boundary — out" and "Rejected
# approaches" sections exist to enumerate what the system does not do, and that
# enumeration has to spell out the forbidden phrasing to be worth anything. The
# prohibition lives in the heading, often many lines above the item, which is
# further than the line window can reach. The next ordinary heading ends it.
_HEADING = re.compile(
    r"^\s{0,3}#{1,6}\s+(?P<md>.*?)\s*$|^\s*<h[1-6][^>]*>(?P<html>.*?)</h[1-6]>",
    re.IGNORECASE,
)
_SECTION_EXEMPT = re.compile(
    r"(boundary|out[-\s]of[-\s]scope|\bout\b|rejected|refuse\w*|never|do\s+not|"
    r"anti-?pattern|mistake|forbidden|drill|hostile|\btrap\b|failure\s+mode|"
    r"content\s+law)",
    re.IGNORECASE,
)


def _section_flags(lines: list[str]) -> list[bool]:
    """For each line, whether the nearest heading above it forbids rather than asserts."""
    flags: list[bool] = []
    inside = False
    for line in lines:
        match = _HEADING.match(line)
        if match:
            title = match.group("md") or match.group("html") or ""
            inside = bool(_SECTION_EXEMPT.search(title))
        flags.append(inside)
    return flags


def _scan(
    text: str,
    pattern: re.Pattern[str],
    law: int,
    source: str,
    detail: str,
    *,
    require: re.Pattern[str] | None = None,
    corrective: re.Pattern[str] | None = None,
) -> list[Violation]:
    """Report every line matching `pattern` (and `require`, when given).

    A line is left alone when it states this law's corrective alongside the
    banned phrasing — that is a correction pair, not a breach — or when a
    prohibition marker sits within `_WINDOW` lines of it.
    """
    lines = text.splitlines()
    sections = _section_flags(lines)
    out: list[Violation] = []
    for index, line in enumerate(lines):
        if not pattern.search(line):
            continue
        if require is not None and not require.search(line):
            continue
        if corrective is not None and corrective.search(line):
            continue
        if sections[index] or _exempt(lines, index):
            continue
        out.append(
            Violation(
                law=law,
                name=LAWS[law],
                source=source,
                line=index + 1,
                excerpt=line.strip()[:160],
                detail=detail,
            )
        )
    return out


# --- Law 1: clause 7.2 does not exist ---------------------------------------

# "permits" is deliberately absent: the running example's claim *asserts* that
# 7.2 permits the refund. That assertion is the thing the plane fails to prove.
# The corruption to catch is describing 7.2 as existing-but-restrictive, which
# turns absence of evidence into conflicting evidence and would make Block
# correct instead of Escalate.
_CLAUSE_CONFLICT = re.compile(
    r"clause\s*7\.2\b[^.\n]{0,80}?\b("
    r"caps?|capped|denies|deny|denied|limits?|limited|excludes?|excluded|"
    r"prohibits?|prohibited|covers?|covered|restricts?|"
    r"does\s+not\s+cover|doesn'?t\s+cover|does\s+not\s+apply"
    r")\b",
    re.IGNORECASE,
)


_CLAUSE_CORRECTIVE = re.compile(
    r"(does\s+not\s+exist|no\s+span|absence|absent|unsupported)", re.IGNORECASE
)


def check_clause_absence(text: str, *, source: str = "") -> list[Violation]:
    return _scan(
        text,
        _CLAUSE_CONFLICT,
        1,
        source,
        "clause 7.2 described as existing-but-restrictive; the failure is absence",
        corrective=_CLAUSE_CORRECTIVE,
    )


# --- Law 2: never "blocked" about the refund --------------------------------

_BLOCK_WORD = re.compile(r"\bblock(?:ed|ing|s)?\b", re.IGNORECASE)
_REFUND_WORD = re.compile(r"\brefund\w*\b", re.IGNORECASE)


# "held" / "escalate" mark the correction. `Actuator.` marks code referring to
# the enum member, whose real name is Block. "Verified / Uncertain" marks the
# three-state user surface, where Blocked is a legitimate label.
_REFUND_CORRECTIVE = re.compile(
    r"(\bheld\b|escalat\w*|Actuator\.|verified\s*/\s*uncertain)", re.IGNORECASE
)


def check_refund_never_blocked(text: str, *, source: str = "") -> list[Violation]:
    return _scan(
        text,
        _BLOCK_WORD,
        2,
        source,
        "refund described as blocked; R3 x unsupported-categorical is Escalate",
        require=_REFUND_WORD,
        corrective=_REFUND_CORRECTIVE,
    )


# --- Law 3: the company pays; the customer does not lose money --------------

_INVERTED_VICTIM = re.compile(
    r"\b(customer\s+(?:lost|loses|lose|was\s+charged|paid)"
    r"|refund\s+(?:was\s+)?(?:denied|refused|rejected)"
    r"|(?:denied|denies|refused|rejected)\s+the\s+refund)\b",
    re.IGNORECASE,
)


_VICTIM_CORRECTIVE = re.compile(
    r"(wrongly\s+pa\w*|company\s+pa\w*|did\s+not\s+lose|found\s+friday)",
    re.IGNORECASE,
)


def check_who_loses_money(text: str, *, source: str = "") -> list[Violation]:
    return _scan(
        text,
        _INVERTED_VICTIM,
        3,
        source,
        "premise inverted; the company wrongly pays and the refund is not denied",
        corrective=_VICTIM_CORRECTIVE,
    )


# --- Law 4: the matrix is transcribed, never redrawn ------------------------

def _live_matrix() -> dict[tuple[str, str], str]:
    from controlplane.interlock import MATRIX

    return {(tier.value, col): act.value for (tier, col), act in MATRIX.items()}


def check_matrix_transcription(
    actual: dict[tuple[str, str], str] | None = None,
) -> list[Violation]:
    """Compare the live matrix against the transcription, cell by cell."""
    live = _live_matrix() if actual is None else actual
    out: list[Violation] = []

    def flag(detail: str) -> None:
        out.append(
            Violation(
                law=4,
                name=LAWS[4],
                source="controlplane/interlock.py",
                line=0,
                excerpt="MATRIX",
                detail=detail,
            )
        )

    for cell, expected in FROZEN_MATRIX.items():
        if cell not in live:
            flag(f"cell {cell} is missing from the matrix")
        elif live[cell] != expected:
            flag(f"cell {cell} is {live[cell]!r}; the transcription says {expected!r}")
    for cell in live:
        if cell not in FROZEN_MATRIX:
            flag(f"cell {cell} was added to the matrix")
    return out


# --- Law 5: exactly five actuators ------------------------------------------

_INVENTED_ACTUATORS = (
    "Kill Span",
    "Terminate Step",
    "Hold & Re-verify",
    "Hold and Re-verify",
    "Redact & Flag",
    "Redact and Flag",
)

_INVENTED_RE = re.compile(
    "|".join(re.escape(name) for name in _INVENTED_ACTUATORS), re.IGNORECASE
)


def check_actuator_enum() -> list[Violation]:
    from controlplane.models import Actuator

    live = tuple(a.value for a in Actuator)
    if live == REAL_ACTUATORS:
        return []
    return [
        Violation(
            law=5,
            name=LAWS[5],
            source="controlplane/models.py",
            line=0,
            excerpt="Actuator",
            detail=f"actuators are {live!r}; the law says {REAL_ACTUATORS!r}",
        )
    ]


def check_no_invented_actuators(text: str, *, source: str = "") -> list[Violation]:
    return _scan(
        text,
        _INVENTED_RE,
        5,
        source,
        "invented actuator; the five are Pass, Pass + annotate, Edit, Escalate, Block",
    )


# --- Law 6: never quote 40ms as p95 -----------------------------------------

# Adjacency only. "40ms p50 and 200ms p95" pairs each number with the percentile
# beside it and is correct, so the window has to be too small to jump over the
# intervening "p50 and 200ms".
_LATENCY_ERROR = re.compile(
    r"(?:\b40\s*(?:ms|milliseconds?)\b[^.\n]{0,6}?\bp95\b"
    r"|\bp95\b[^.\n]{0,10}?\b40\s*(?:ms|milliseconds?)\b)",
    re.IGNORECASE,
)


# A line that also names p50 is stating the correct pairing, or correcting the
# error by showing both halves.
_LATENCY_CORRECTIVE = re.compile(r"\bp50\b", re.IGNORECASE)


def check_latency_claim(text: str, *, source: str = "") -> list[Violation]:
    return _scan(
        text,
        _LATENCY_ERROR,
        6,
        source,
        "40ms quoted as p95; that is a five-fold overclaim. p50 is 40ms, p95 is 200ms",
        corrective=_LATENCY_CORRECTIVE,
    )


# --- Law 7: no fabricated rates ---------------------------------------------

_DETECTION_CLAIM = re.compile(
    r"\b(we\s+catch|ungrounded\s+claims|accuracy|precision|recall|"
    r"false[\s-]negative|false[\s-]positive|\bfnr\b|\bfpr\b|detection\s+rate)\b",
    re.IGNORECASE,
)
_BARE_PERCENT = re.compile(r"(?<!<measured>)\b\d+(?:\.\d+)?\s*%")
_MEASURED = re.compile(
    r"(<measured>|\bmeasured\b|\beval\s+corpus\b|\bCI\b|confidence\s+interval"
    r"|\bplaceholder\b|\bschema\b|\bempty\b|typed\s+null)",
    re.IGNORECASE,
)


# Quotation marks are the difference between reporting a number and claiming it.
# NARRATIVE.md quotes the industry's "99% accuracy" boast in order to reject it.
_QUOTED = re.compile(r"\"[^\"]*\"|\u201c[^\u201d]*\u201d|\u2018[^\u2019]*\u2019|`[^`]*`")


def _all_quoted(line: str, matches: list[re.Match[str]]) -> bool:
    """True when every match sits inside quotation marks."""
    spans = [(m.start(), m.end()) for m in _QUOTED.finditer(line)]
    if not spans:
        return False
    return all(
        any(lo <= m.start() and m.end() <= hi for lo, hi in spans) for m in matches
    )


def check_no_fabricated_rates(text: str, *, source: str = "") -> list[Violation]:
    """A detection rate is legal only once something has measured it."""
    lines = text.splitlines()
    sections = _section_flags(lines)
    out: list[Violation] = []
    for index, line in enumerate(lines):
        if not _DETECTION_CLAIM.search(line):
            continue
        percents = list(_BARE_PERCENT.finditer(line))
        if not percents:
            continue
        if _all_quoted(line, percents):
            continue
        if sections[index] or _MEASURED.search(line) or _exempt(lines, index):
            continue
        out.append(
            Violation(
                law=7,
                name=LAWS[7],
                source=source,
                line=index + 1,
                excerpt=line.strip()[:160],
                detail=(
                    "detection rate quoted without measurement; the gate report "
                    "ships as an empty schema with typed placeholders"
                ),
            )
        )
    return out


# --- Law 8: the refuse-to-claim list is about us ----------------------------

_REFUSE_MARKER = re.compile(
    r"(refuse[\s-]*to[\s-]*claim|we\s+do\s+not\s+claim|what\s+we\s+don'?t\s+claim"
    r"|will\s+not\s+claim)",
    re.IGNORECASE,
)
_REFUSE_ITEMS = re.compile(
    r"(eliminat\w*\s+hallucinat\w*|zero\s+integration|zero\s+(?:added\s+)?latency"
    r"|one\s+accuracy\s+number|single\s+accuracy\s+number)",
    re.IGNORECASE,
)


def check_refuse_to_claim_present(text: str, *, source: str = "") -> list[Violation]:
    """Document-level. Every deck disclaims competitors; almost none disclaim themselves."""
    if _REFUSE_MARKER.search(text) and _REFUSE_ITEMS.search(text):
        return []
    return [
        Violation(
            law=8,
            name=LAWS[8],
            source=source,
            line=0,
            excerpt="(document)",
            detail=(
                "no self-directed refuse-to-claim list; this is not the "
                "rejected-approaches list, which is about everyone else"
            ),
        )
    ]


# --- Law 9: do not drop bias ------------------------------------------------

_BIAS = re.compile(r"\bbias(?:ed|es)?\b", re.IGNORECASE)


def check_bias_present(text: str, *, source: str = "") -> list[Violation]:
    """Document-level. The brief names bias explicitly; omitting it scores against us."""
    if _BIAS.search(text):
        return []
    return [
        Violation(
            law=9,
            name=LAWS[9],
            source=source,
            line=0,
            excerpt="(document)",
            detail="bias is absent; the brief names it under responsibility",
        )
    ]


# --- Composite --------------------------------------------------------------

TEXT_CHECKERS = (
    check_clause_absence,
    check_refund_never_blocked,
    check_who_loses_money,
    check_no_invented_actuators,
    check_latency_claim,
    check_no_fabricated_rates,
)

DOCUMENT_CHECKERS = (
    check_refuse_to_claim_present,
    check_bias_present,
)


def check_text(text: str, *, source: str = "") -> list[Violation]:
    """Every line-level checker. Document-level presence laws are excluded."""
    out: list[Violation] = []
    for checker in TEXT_CHECKERS:
        out.extend(checker(text, source=source))
    return sorted(out, key=lambda v: (v.line, v.law))


def format_violations(violations: list[Violation]) -> str:
    if not violations:
        return "no content-law violations"
    lines = [f"{len(violations)} content-law violation(s):"]
    for v in violations:
        where = f"{v.source}:{v.line}" if v.line else v.source
        lines.append(f"  [law {v.law}] {where}\n      {v.excerpt}\n      -> {v.detail}")
    return "\n".join(lines)
