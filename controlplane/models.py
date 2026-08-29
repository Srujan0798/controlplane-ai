from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class StepKind(str, Enum):
    RETRIEVAL = "retrieval"
    TOOL = "tool"
    DB = "db"
    SYSTEM = "system"


class AssertionStrength(str, Enum):
    CATEGORICAL = "categorical"
    HEDGED = "hedged"


class ClaimKind(str, Enum):
    NUMERIC = "numeric"
    STRUCTURAL = "structural"
    TEMPORAL = "temporal"
    TEXTUAL = "textual"
    DERIVED = "derived"


class Verdict(str, Enum):
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"


class BlastTier(str, Enum):
    R0 = "R0"
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"


class Actuator(str, Enum):
    PASS = "Pass"
    PASS_ANNOTATE = "Pass + annotate"
    EDIT = "Edit"
    ESCALATE = "Escalate"
    BLOCK = "Block"


@dataclass(frozen=True)
class Principal:
    id: str
    roles: frozenset[str] = field(default_factory=frozenset)
    clearance: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class Step:
    step_id: str
    kind: StepKind
    name: str


@dataclass(frozen=True)
class Span:
    span_id: str
    step_id: str
    source_id: str
    acl: frozenset[str]
    content: str
    content_hash: str
    offsets: tuple[int, int] | None = None


@dataclass(frozen=True)
class Claim:
    claim_id: str
    text: str
    kind: ClaimKind
    assertion: AssertionStrength
    role_in_action: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class Binding:
    claim_id: str
    span_ids: tuple[str, ...]
    method: str
    verdict: Verdict
    rationale: str = ""


@dataclass(frozen=True)
class Action:
    action_id: str
    name: str
    tier: BlastTier
    args: dict[str, Any] = field(default_factory=dict)
    irreversibility: bool = False


@dataclass(frozen=True)
class EntitlementFinding:
    claim_id: str
    violated: bool
    offending_span_ids: tuple[str, ...]
    detail: str


@dataclass(frozen=True)
class EvidencePacket:
    """Attached on Escalate: claim + candidate spans + verdict + diff stub."""

    claim_id: str
    claim_text: str
    verdict: str
    candidate_span_ids: tuple[str, ...]
    diff: str | None = None
    proposed_actuator: str = "Escalate"
    action_id: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Decision:
    action_id: str
    actuator: Actuator
    matrix_row: str
    matrix_col: str
    driving_claim_ids: tuple[str, ...]
    packet: dict[str, Any]
