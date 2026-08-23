# Round 2 ControlPlane.ai Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver Accenture Innovation Challenge Round 2 Track 1 (ControlPlane.ai): a working core-mechanism prototype, a detailed business proposal, and a pitch presentation — all grounded in the frozen architecture.

**Architecture:** Capture provenance **outside** the model at context assembly into an append-only Evidence Ledger (`STEP → SPAN → CLAIM → ACTION`). Bind claims deterministically; run entitlement as ACL set-membership; decide with the frozen blast-radius matrix. Demo the refund agent dual-action (R1 Edit + R3 Escalate), then show the same plane across three enterprise use cases with different R-tiers.

**Tech Stack:** Python ≥ 3.11, stdlib + `pytest`, CLI demo; proposal/pitch as Markdown → PDF/PPTX in a later packaging pass.

**Spec:** [`docs/superpowers/specs/2026-08-23-provenance-recorder-design.md`](../specs/2026-08-23-provenance-recorder-design.md)  
**Round 2 brief:** [`docs/Accenture Innovation Challenge - Round2 - Detailed Problem Statements.pdf`](../../Accenture%20Innovation%20Challenge%20-%20Round2%20-%20Detailed%20Problem%20Statements.pdf)  
**Frozen design:** [`docs/ARCHITECTURE.md`](../../ARCHITECTURE.md)

## Global Constraints

- Provenance is captured **outside** the model — model output never creates spans.
- Default claim verdict is **`UNSUPPORTED`**; a claim must earn `SUPPORTED`.
- **Clause 7.2 does not exist** — absence → `UNSUPPORTED`, never “caps/denies/doesn’t cover”.
- Decision matrix is **transcribed, never redrawn** (R0–R3 × contradicted/entitlement | unsupported+categorical | unsupported+hedged | unknown).
- Action Interlock is the **sole decider**; other roles only advise.
- `UNKNOWN` never collapses into `SUPPORTED`.
- No LLM / NLI / network on the critical path in Phase A–B.
- Content laws in `ARCHITECTURE.md` §10 are load-bearing — do not “improve” the wording in demo copy.
- Round 2 official deliverables (from brief p.7): **(1) Detailed Business Proposal (2) Working Prototype (3) Pitch Presentation**.

## Round 2 brief → our answer (coverage map)

| Brief requirement | How we address it | Plan phase |
|---|---|---|
| Working prototype of core mechanism | Provenance Recorder + bind + entitlement + interlock + refund demo | A |
| Different use cases / risk / latency | Three fixtures: support (R1), internal copilot (R1/R2), refund decision-support (R3) | B |
| Agents that take actions, not just text | Dual pending actions on one response | A |
| No reliable ground truth | Absence-of-evidence path (clause 7.2); default UNSUPPORTED | A |
| Over/under-flag tradeoff | Hostile matrix: verdict hostile, action proportionate | A + C |
| Bias + privacy overlap | Entitlement ACL as privacy; keep bias as measurement note in proposal | A + C |
| API-only models (I/O layer) | Context-assembly hook; no weights/logits | A + C |
| Tiered allow / edit / escalate / block | Frozen matrix actuators | A |
| Configurable policy / audit trail | `policy_version` + hash-chained ledger | A + C |
| Metrics / FNR to skeptical stakeholder | Proposal + pitch: publish FNR shape; prototype prints decision cells | C + D |
| Feedback loops | Proposal roadmap (shadow → override capture); not coded in MVP | C |
| Business proposal | New `docs/ROUND2-PROPOSAL.md` from ARCHITECTURE/NARRATIVE/QA | C |
| Pitch presentation | `docs/ROUND2-PITCH.md` outline + slide-ready sections | D |

**Selective non-coverage (allowed by brief):** real PII NER model, AI-as-judge on critical path, full multi-turn session store, geographic policy packs — called out as Phase-2 roadmap, not pretended in the prototype.

## File structure (locked)

```text
controlplane/
  __init__.py              # public exports + version
  models.py                # Principal, Step, Span, Claim, Binding, Action, Decision, enums
  ledger.py                # EvidenceLedger append-only hash chain
  recorder.py              # Provenance Recorder
  binder.py                # claim → span binding
  entitlement.py           # Entitlement Auditor
  interlock.py             # Action Interlock + frozen MATRIX
  scenarios/
    __init__.py
    refund.py              # frozen running example fixtures
    multi_usecase.py       # support / copilot / decision-support fixtures
examples/
  refund_trace_demo.py
  multi_usecase_demo.py
tests/
  test_ledger.py
  test_recorder.py
  test_binder.py
  test_entitlement.py
  test_interlock.py
  test_refund_scenario.py
  test_multi_usecase.py
pyproject.toml
README.md
docs/ROUND2-PROPOSAL.md
docs/ROUND2-PITCH.md
docs/superpowers/specs/2026-08-23-provenance-recorder-design.md
docs/Accenture Innovation Challenge - Round2 - Detailed Problem Statements.pdf
```

---

## Phase A — Working Prototype (core mechanism)

### Task 1: Project scaffold + typed models

**Files:**
- Create: `pyproject.toml`
- Create: `controlplane/__init__.py`
- Create: `controlplane/models.py`
- Create: `tests/test_models_smoke.py`
- Create: `README.md`

**Interfaces:**
- Produces: `Principal`, `StepKind`, `AssertionStrength`, `ClaimKind`, `Verdict`, `BlastTier`, `Actuator`, `Step`, `Span`, `Claim`, `Binding`, `Action`, `Decision`, `EntitlementFinding`

- [ ] **Step 1: Write `pyproject.toml`**

```toml
[project]
name = "controlplane"
version = "0.1.0"
description = "Admission-control layer: STEP → SPAN → CLAIM → ACTION"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0"]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
include = ["controlplane*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

- [ ] **Step 2: Write failing smoke test**

```python
# tests/test_models_smoke.py
from controlplane.models import BlastTier, Verdict, Actuator

def test_enums_exist():
    assert BlastTier.R3.value == "R3"
    assert Verdict.UNSUPPORTED.value == "UNSUPPORTED"
    assert Actuator.ESCALATE.value == "Escalate"
```

- [ ] **Step 3: Run test — expect FAIL (import error)**

Run: `python -m pytest tests/test_models_smoke.py -v`  
Expected: FAIL with `ModuleNotFoundError` or import error for `controlplane.models`

- [ ] **Step 4: Implement `controlplane/models.py`**

```python
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
class Decision:
    action_id: str
    actuator: Actuator
    matrix_row: str
    matrix_col: str
    driving_claim_ids: tuple[str, ...]
    packet: dict[str, Any]
```

- [ ] **Step 5: Export from `controlplane/__init__.py` and re-run tests**

```python
"""ControlPlane.ai — admission-control layer prototype."""
from controlplane.models import (
    Actuator, Action, AssertionStrength, Binding, BlastTier, Claim, ClaimKind,
    Decision, EntitlementFinding, Principal, Span, Step, StepKind, Verdict,
)

__all__ = [
    "Actuator", "Action", "AssertionStrength", "Binding", "BlastTier", "Claim",
    "ClaimKind", "Decision", "EntitlementFinding", "Principal", "Span", "Step",
    "StepKind", "Verdict",
]
__version__ = "0.1.0"
```

Run: `python -m pytest tests/test_models_smoke.py -v`  
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml controlplane/ tests/test_models_smoke.py README.md
git commit -m "feat: scaffold controlplane package and typed models"
```

---

### Task 2: Evidence Ledger (append-only, hash-chained)

**Files:**
- Create: `controlplane/ledger.py`
- Create: `tests/test_ledger.py`

**Interfaces:**
- Consumes: models types
- Produces: `EvidenceLedger.begin(...)`, `.append(entry_type, payload) -> str`, `.verify_chain() -> bool`, `.get(entry_type) -> list`, attributes `request_id`, `principal`, `policy_version`, `spans`, `claims`, `bindings`, `steps`, `actions`, `decisions`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_ledger.py
from controlplane.ledger import EvidenceLedger
from controlplane.models import Principal

def test_hash_chain_links_entries():
    led = EvidenceLedger.begin(
        request_id="req-1",
        principal=Principal(id="u1", clearance=frozenset({"public"})),
        action_intent="demo",
        policy_version="matrix-v1",
    )
    h1 = led.append("note", {"n": 1})
    h2 = led.append("note", {"n": 2})
    assert h1 != h2
    assert led.verify_chain() is True

def test_tamper_breaks_chain():
    led = EvidenceLedger.begin(
        request_id="req-1",
        principal=Principal(id="u1", clearance=frozenset({"public"})),
        action_intent="demo",
        policy_version="matrix-v1",
    )
    led.append("note", {"n": 1})
    led._entries[0].payload["n"] = 99  # intentional tamper for test
    assert led.verify_chain() is False
```

- [ ] **Step 2: Run tests — expect FAIL**

Run: `python -m pytest tests/test_ledger.py -v`  
Expected: FAIL (`ModuleNotFoundError: controlplane.ledger`)

- [ ] **Step 3: Implement `controlplane/ledger.py`**

```python
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from controlplane.models import (
    Action, Binding, Claim, Decision, Principal, Span, Step,
)


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class LedgerEntry:
    seq: int
    entry_type: str
    payload: dict[str, Any]
    prev_hash: str
    hash: str


@dataclass
class EvidenceLedger:
    request_id: str
    principal: Principal
    action_intent: str
    policy_version: str
    _entries: list[LedgerEntry] = field(default_factory=list)
    steps: dict[str, Step] = field(default_factory=dict)
    spans: dict[str, Span] = field(default_factory=dict)
    claims: dict[str, Claim] = field(default_factory=dict)
    bindings: dict[str, Binding] = field(default_factory=dict)
    actions: dict[str, Action] = field(default_factory=dict)
    decisions: dict[str, Decision] = field(default_factory=dict)
    context_frozen: bool = False

    @classmethod
    def begin(
        cls,
        request_id: str,
        principal: Principal,
        action_intent: str,
        policy_version: str = "matrix-v1",
    ) -> "EvidenceLedger":
        return cls(
            request_id=request_id,
            principal=principal,
            action_intent=action_intent,
            policy_version=policy_version,
        )

    def append(self, entry_type: str, payload: dict[str, Any]) -> str:
        prev = self._entries[-1].hash if self._entries else "GENESIS"
        digest = _sha256(prev + _canonical({"type": entry_type, "payload": payload}))
        self._entries.append(
            LedgerEntry(
                seq=len(self._entries),
                entry_type=entry_type,
                payload=dict(payload),
                prev_hash=prev,
                hash=digest,
            )
        )
        return digest

    def verify_chain(self) -> bool:
        prev = "GENESIS"
        for entry in self._entries:
            if entry.prev_hash != prev:
                return False
            expected = _sha256(prev + _canonical({"type": entry.entry_type, "payload": entry.payload}))
            if expected != entry.hash:
                return False
            prev = entry.hash
        return True
```

- [ ] **Step 4: Run tests — expect PASS**

Run: `python -m pytest tests/test_ledger.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add controlplane/ledger.py tests/test_ledger.py
git commit -m "feat: append-only hash-chained Evidence Ledger"
```

---

### Task 3: Provenance Recorder

**Files:**
- Create: `controlplane/recorder.py`
- Create: `tests/test_recorder.py`

**Interfaces:**
- Consumes: `EvidenceLedger`, `Principal`, `StepKind`
- Produces: `ProvenanceRecorder.begin_request`, `.record_step`, `.record_span`, `.finish_context_assembly`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_recorder.py
import pytest
from controlplane.models import Principal, StepKind
from controlplane.recorder import ProvenanceRecorder

def test_records_span_with_hash_and_freezes():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        request_id="r1",
        principal=Principal(id="agent", clearance=frozenset({"vendor-public"})),
        action_intent="refund",
    )
    sid = rec.record_step(led, StepKind.RETRIEVAL, "policy_search")
    span_id = rec.record_span(
        led, sid, source_id="doc:vendor-v3", acl=frozenset({"vendor-public"}),
        content="Clause 4.1 covers shipping delays.",
    )
    assert span_id in led.spans
    assert led.spans[span_id].content_hash
    rec.finish_context_assembly(led)
    with pytest.raises(RuntimeError, match="frozen"):
        rec.record_span(
            led, sid, source_id="doc:x", acl=frozenset({"vendor-public"}), content="late",
        )
```

- [ ] **Step 2: Run — expect FAIL**

Run: `python -m pytest tests/test_recorder.py -v`  
Expected: FAIL (missing `recorder`)

- [ ] **Step 3: Implement `controlplane/recorder.py`**

```python
from __future__ import annotations
import hashlib
import itertools
from controlplane.ledger import EvidenceLedger
from controlplane.models import Principal, Span, Step, StepKind


def _content_hash(content: str) -> str:
    normalized = " ".join(content.split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


class ProvenanceRecorder:
    def __init__(self) -> None:
        self._step_seq = itertools.count(1)
        self._span_seq = itertools.count(1)

    def begin_request(
        self,
        request_id: str,
        principal: Principal,
        action_intent: str,
        policy_version: str = "matrix-v1",
    ) -> EvidenceLedger:
        led = EvidenceLedger.begin(request_id, principal, action_intent, policy_version)
        led.append("request_begin", {
            "request_id": request_id,
            "principal": principal.id,
            "action_intent": action_intent,
        })
        return led

    def record_step(self, led: EvidenceLedger, kind: StepKind, name: str) -> str:
        if led.context_frozen:
            raise RuntimeError("context assembly frozen; cannot record step")
        step_id = f"step-{next(self._step_seq)}"
        step = Step(step_id=step_id, kind=kind, name=name)
        led.steps[step_id] = step
        led.append("step", {"step_id": step_id, "kind": kind.value, "name": name})
        return step_id

    def record_span(
        self,
        led: EvidenceLedger,
        step_id: str,
        *,
        source_id: str,
        acl: frozenset[str],
        content: str,
        offsets: tuple[int, int] | None = None,
    ) -> str:
        if led.context_frozen:
            raise RuntimeError("context assembly frozen; cannot record span")
        if step_id not in led.steps:
            raise KeyError(f"unknown step_id: {step_id}")
        span_id = f"span-{next(self._span_seq)}"
        span = Span(
            span_id=span_id,
            step_id=step_id,
            source_id=source_id,
            acl=frozenset(acl),
            content=content,
            content_hash=_content_hash(content),
            offsets=offsets,
        )
        led.spans[span_id] = span
        led.append("span", {
            "span_id": span_id,
            "step_id": step_id,
            "source_id": source_id,
            "acl": sorted(acl),
            "content_hash": span.content_hash,
        })
        return span_id

    def finish_context_assembly(self, led: EvidenceLedger) -> None:
        led.context_frozen = True
        led.append("context_frozen", {"span_count": len(led.spans)})
```

- [ ] **Step 4: Run tests — PASS, then commit**

```bash
python -m pytest tests/test_recorder.py -v
git add controlplane/recorder.py tests/test_recorder.py
git commit -m "feat: Provenance Recorder with context-assembly freeze"
```

---

### Task 4: Claim binder

**Files:**
- Create: `controlplane/binder.py`
- Create: `tests/test_binder.py`

**Interfaces:**
- Consumes: `EvidenceLedger`, `Claim`
- Produces: `bind_claims(ledger, claims, fixture_map=None) -> list[Binding]`  
  `fixture_map: dict[claim_id, tuple[span_ids] | None]` — `None` means force unbound

- [ ] **Step 1: Write failing tests**

```python
# tests/test_binder.py
from controlplane.binder import bind_claims
from controlplane.models import (
    AssertionStrength, Claim, ClaimKind, Principal, StepKind, Verdict,
)
from controlplane.recorder import ProvenanceRecorder

def _ledger_with_span(content: str, acl=frozenset({"public"})):
    rec = ProvenanceRecorder()
    led = rec.begin_request("r", Principal(id="u", clearance=frozenset({"public"})), "t")
    sid = rec.record_step(led, StepKind.RETRIEVAL, "search")
    rec.record_span(led, sid, source_id="doc:1", acl=acl, content=content)
    rec.finish_context_assembly(led)
    return led

def test_default_unsupported_when_no_match():
    led = _ledger_with_span("Clause 4.1 covers shipping.")
    claim = Claim("c1", "Clause 7.2 permits this refund", ClaimKind.STRUCTURAL,
                  AssertionStrength.CATEGORICAL)
    bindings = bind_claims(led, [claim])
    assert bindings[0].verdict == Verdict.UNSUPPORTED
    assert bindings[0].span_ids == ()

def test_fixture_binding_supports():
    led = _ledger_with_span("Refund amount for order ORD-9 is 184000 INR.")
    span_id = next(iter(led.spans))
    claim = Claim("c2", "Refund is ₹1,84,000", ClaimKind.NUMERIC,
                  AssertionStrength.CATEGORICAL)
    bindings = bind_claims(led, [claim], fixture_map={"c2": (span_id,)})
    assert bindings[0].verdict == Verdict.SUPPORTED

def test_derived_never_supported_by_shallow_match():
    led = _ledger_with_span("A is 2. B is 3.")
    claim = Claim("c3", "A+B is 5", ClaimKind.DERIVED, AssertionStrength.CATEGORICAL)
    bindings = bind_claims(led, [claim])
    assert bindings[0].verdict == Verdict.UNKNOWN
```

- [ ] **Step 2: Implement `controlplane/binder.py`**

```python
from __future__ import annotations
from controlplane.ledger import EvidenceLedger
from controlplane.models import Binding, Claim, ClaimKind, Verdict


def bind_claims(
    ledger: EvidenceLedger,
    claims: list[Claim],
    fixture_map: dict[str, tuple[str, ...] | None] | None = None,
) -> list[Binding]:
    fixture_map = fixture_map or {}
    results: list[Binding] = []
    for claim in claims:
        ledger.claims[claim.claim_id] = claim
        if claim.kind == ClaimKind.DERIVED and claim.claim_id not in fixture_map:
            binding = Binding(claim.claim_id, (), "none", Verdict.UNKNOWN)
        elif claim.claim_id in fixture_map:
            span_ids = fixture_map[claim.claim_id]
            if span_ids:
                binding = Binding(claim.claim_id, tuple(span_ids), "fixture", Verdict.SUPPORTED)
            else:
                binding = Binding(claim.claim_id, (), "fixture", Verdict.UNSUPPORTED)
        else:
            # exact/substring lookup against provenance set only
            hits = tuple(
                s.span_id for s in ledger.spans.values()
                if claim.text.lower() in s.content.lower()
                or s.content.lower() in claim.text.lower()
            )
            if hits:
                binding = Binding(claim.claim_id, hits, "exact", Verdict.SUPPORTED)
            else:
                binding = Binding(claim.claim_id, (), "none", Verdict.UNSUPPORTED)
        ledger.bindings[claim.claim_id] = binding
        ledger.append("binding", {
            "claim_id": binding.claim_id,
            "span_ids": list(binding.span_ids),
            "method": binding.method,
            "verdict": binding.verdict.value,
        })
        results.append(binding)
    return results
```

- [ ] **Step 3: Run tests — PASS, commit**

```bash
python -m pytest tests/test_binder.py -v
git add controlplane/binder.py tests/test_binder.py
git commit -m "feat: deterministic claim binder with UNSUPPORTED default"
```

---

### Task 5: Entitlement Auditor + Action Interlock

**Files:**
- Create: `controlplane/entitlement.py`
- Create: `controlplane/interlock.py`
- Create: `tests/test_entitlement.py`
- Create: `tests/test_interlock.py`

**Interfaces:**
- Produces: `audit_claim(ledger, claim_id) -> EntitlementFinding`  
- Produces: `MATRIX` frozen table; `decide(ledger, action) -> Decision`  
- Matrix column selection: entitlement violation ∨ CONTRADICTED → col0; else UNSUPPORTED+categorical → col1; UNSUPPORTED+hedged → col2; UNKNOWN → col3. Worst driving claim among those with `role_in_action[action_id] > 0`.

- [ ] **Step 1: Write entitlement + matrix tests**

```python
# tests/test_entitlement.py
from controlplane.binder import bind_claims
from controlplane.entitlement import audit_claim
from controlplane.models import (
    AssertionStrength, Claim, ClaimKind, Principal, StepKind,
)
from controlplane.recorder import ProvenanceRecorder

def test_acl_mismatch_is_entitlement_violation():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "r", Principal(id="customer-bot", clearance=frozenset({"public"})), "show",
    )
    sid = rec.record_step(led, StepKind.RETRIEVAL, "hr_doc")
    span = rec.record_span(
        led, sid, source_id="doc:hr-salary", acl=frozenset({"hr-confidential"}),
        content="Employee compensation band L5.",
    )
    rec.finish_context_assembly(led)
    claim = Claim("c1", "Employee compensation band L5.", ClaimKind.TEXTUAL,
                  AssertionStrength.CATEGORICAL, role_in_action={"show": 1.0})
    bind_claims(led, [claim], fixture_map={"c1": (span,)})
    finding = audit_claim(led, "c1")
    assert finding.violated is True
    assert span in finding.offending_span_ids
```

```python
# tests/test_interlock.py
from controlplane.interlock import decide
from controlplane.ledger import EvidenceLedger
from controlplane.models import (
    Action, Actuator, AssertionStrength, Binding, BlastTier, Claim, ClaimKind,
    Principal, Verdict,
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
    from controlplane.models import EntitlementFinding
    # decide() must accept optional findings map — see implementation
    action = Action("show", "show_text", BlastTier.R1)
    d = decide(led, action, findings={"c": EntitlementFinding("c", True, ("s1",), "acl")})
    assert d.actuator == Actuator.EDIT
```

- [ ] **Step 2: Implement entitlement + interlock**

`controlplane/entitlement.py`:

```python
from __future__ import annotations
from controlplane.ledger import EvidenceLedger
from controlplane.models import EntitlementFinding


def audit_claim(ledger: EvidenceLedger, claim_id: str) -> EntitlementFinding:
    binding = ledger.bindings[claim_id]
    offending: list[str] = []
    for span_id in binding.span_ids:
        span = ledger.spans[span_id]
        if not span.acl.issubset(ledger.principal.clearance):
            offending.append(span_id)
    return EntitlementFinding(
        claim_id=claim_id,
        violated=bool(offending),
        offending_span_ids=tuple(offending),
        detail="span ACL not subset of principal clearance" if offending else "ok",
    )
```

`controlplane/interlock.py` — encode the **exact** frozen matrix from `ARCHITECTURE.md` §4 as a constant dict keyed by `(BlastTier, column_name) -> Actuator`. Implement `decide(ledger, action, findings=None)`.

Column resolution order for a claim:
1. If finding.violated or verdict == CONTRADICTED → `"Contradicted / entitlement violation"`
2. Elif verdict == UNSUPPORTED and assertion == CATEGORICAL → `"Unsupported + categorical"`
3. Elif verdict == UNSUPPORTED and assertion == HEDGED → `"Unsupported + hedged"`
4. Elif verdict == UNKNOWN → `"Unknown"`
5. Elif verdict == SUPPORTED and not violated → actuator Pass (no matrix severity; treat as clean — return `Actuator.PASS` without looking up fail cells)

Among claims with `role_in_action.get(action.action_id, 0) > 0`, pick worst by severity rank: Block > Escalate > Edit > Pass+annotate > Pass.

- [ ] **Step 3: Fix tests if `findings` API differs; all PASS; commit**

```bash
python -m pytest tests/test_entitlement.py tests/test_interlock.py -v
git add controlplane/entitlement.py controlplane/interlock.py tests/test_entitlement.py tests/test_interlock.py
git commit -m "feat: entitlement auditor and frozen-matrix action interlock"
```

---

### Task 6: Frozen refund scenario + demo CLI

**Files:**
- Create: `controlplane/scenarios/__init__.py`
- Create: `controlplane/scenarios/refund.py`
- Create: `examples/refund_trace_demo.py`
- Create: `tests/test_refund_scenario.py`

**Interfaces:**
- Produces: `run_refund_scenario() -> EvidenceLedger` with both decisions attached  
- Demo prints: spans, claims/bindings, entitlement findings, Decision for `show_text` (Edit) and `issue_refund` (Escalate)

- [ ] **Step 1: Write integration test locking dual-action outcome**

```python
# tests/test_refund_scenario.py
from controlplane.models import Actuator
from controlplane.scenarios.refund import run_refund_scenario

def test_dual_action_edit_and_escalate():
    led = run_refund_scenario()
    assert led.decisions["show_text"].actuator == Actuator.EDIT
    assert led.decisions["issue_refund"].actuator == Actuator.ESCALATE
    assert led.verify_chain() is True
```

- [ ] **Step 2: Implement scenario fixtures**

Encode exactly:
- Principal: customer-support agent clearance `{"vendor-public"}` (NOT `hr-confidential` / internal-legal)
- Spans: ~include vendor clause 4.1 (public), order amount 184000 (public), **one HR/internal span that grounds a side claim but ACL-excludes caller**, **no span for clause 7.2**
- Claims: amount (supported), approval language (supported or unbound), **clause 7.2 categorical unsupported**, one claim grounded on unentitled span
- Actions: `show_text` R1, `issue_refund` R3 irreversible
- Fixture map: bind amount; force clause 7.2 unbound (`None` / empty)

- [ ] **Step 3: Implement `examples/refund_trace_demo.py`** that calls `run_refund_scenario()` and prints a readable report including matrix cells.

- [ ] **Step 4: Run**

```bash
python -m pytest tests/test_refund_scenario.py -v
python examples/refund_trace_demo.py
```

Expected: tests PASS; demo shows Edit + Escalate; mentions “Clause 7.2 does not exist”.

- [ ] **Step 5: Commit**

```bash
git add controlplane/scenarios examples/refund_trace_demo.py tests/test_refund_scenario.py
git commit -m "feat: refund running-example demo with dual-action interlock"
```

---

## Phase B — Multi-use-case prototype (Round 2 reference params)

### Task 7: Three use-case fixtures + demo

**Files:**
- Create: `controlplane/scenarios/multi_usecase.py`
- Create: `examples/multi_usecase_demo.py`
- Create: `tests/test_multi_usecase.py`

**Round 2 reference:** enterprise with customer support assistant, internal knowledge assistant, decision-support tool — different latency/risk.

| Use case | Example action | Tier | Expected story |
|---|---|---|---|
| Customer support chatbot | show reply | R1 | unsupported hedged → Pass + annotate |
| Internal knowledge copilot | draft email to partner (external send) | R2 | unsupported categorical → Edit |
| Decision-support refund | issue_refund | R3 | unsupported categorical → Escalate |

- [ ] **Step 1: Tests asserting three distinct actuators from three ledgers**
- [ ] **Step 2: Implement fixtures + demo**
- [ ] **Step 3: Run pytest + demo; commit**

```bash
git commit -m "feat: multi-use-case demos for Round 2 reference parameters"
```

---

## Phase C — Detailed Business Proposal

### Task 8: Write `docs/ROUND2-PROPOSAL.md`

**Files:**
- Create: `docs/ROUND2-PROPOSAL.md`
- Modify: none of the frozen architecture files (proposal **cites** them)

**Required sections (from Round 2 brief “What Round 2 Asks You to Deliver”):**

1. Problem framing (enterprise multi-use-case AI; cost of wrong output = executed transaction)
2. Solution design (one graph, three axes; keystone = Provenance Recorder; pointer to prototype)
3. Target users (platform/SRE, risk/compliance, app owners for support/copilot/agents)
4. Business case & impact (dead compute, held irreversible actions, entitlement incidents prevented — use directional assumptions: tens of thousands interactions/week)
5. Phased roadmap (Phase 0 shadow → Phase 1 enforce R3 → Phase 2 R2 → feedback/FNR publishing)
6. Key risks & mitigations (false assurance on derived claims; alert fatigue; API-only visibility — map to ARCHITECTURE §7–8)
7. Explicit assumptions (API-consumed foundation models; mix of governed/loose sources; India/enterprise regulated workflows as primary lens unless team chooses otherwise)
8. Prototype evidence appendix (commands to run demos + expected actuators)

- [ ] **Step 1: Draft proposal from `ARCHITECTURE.md` + `NARRATIVE.md` + `QA.md` + Round 2 PDF complexities (selectively)**
- [ ] **Step 2: Self-check — every “Real-World Complexity” bullet either addressed or explicitly deferred with reason**
- [ ] **Step 3: Commit**

```bash
git add docs/ROUND2-PROPOSAL.md
git commit -m "docs: Round 2 detailed business proposal"
```

---

## Phase D — Pitch Presentation

### Task 9: Write pitch outline `docs/ROUND2-PITCH.md` (+ optional PPTX later)

**Files:**
- Create: `docs/ROUND2-PITCH.md`

**Slide arc (10–12 slides):**

1. Title — ControlPlane.ai / Team / AIC 2026 Round 2  
2. Problem — answers → actions; wrong output is now a transaction  
3. Insight — set-membership on receipts, not model mind  
4. Primitive — STEP→SPAN→CLAIM→ACTION diagram  
5. Demo beat 1 — clause 7.2 UNSUPPORTED (absence)  
6. Demo beat 2 — entitlement Edit on R1  
7. Demo beat 3 — Escalate on R3 refund  
8. Why not guardrails / RAG-only / confidence — one slide  
9. Multi-use-case matrix (support / copilot / decision-support)  
10. Business case + roadmap  
11. Risks we publish (FNR shape)  
12. Ask / close  

- [ ] **Step 1: Write speaker-ready markdown with exact lines from NARRATIVE §7 where load-bearing**
- [ ] **Step 2: Dry-run: ensure every pitch claim is backed by prototype output or ARCHITECTURE citation**
- [ ] **Step 3: Commit**

```bash
git add docs/ROUND2-PITCH.md
git commit -m "docs: Round 2 pitch outline"
```

Optional follow-up (separate task if needed): render PPTX with official AIC template if available again.

---

## Phase E — Package & verify

### Task 10: README, graphify refresh, end-to-end gate

**Files:**
- Modify: `README.md`
- Modify: `.gitignore` if needed (`__pycache__/`, `.venv/`)

- [ ] **Step 1: README quickstart**

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python examples/refund_trace_demo.py
python examples/multi_usecase_demo.py
```

- [ ] **Step 2: Run full pytest; fix failures**
- [ ] **Step 3: `graphify update .` after code lands**
- [ ] **Step 4: Final commit**

```bash
git add README.md
git commit -m "docs: Round 2 prototype quickstart and verification gate"
```

---

## Spec coverage self-check

| Spec / brief item | Task |
|---|---|
| Evidence Ledger hash chain | Task 2 |
| Provenance Recorder + freeze | Task 3 |
| Claim bind, default UNSUPPORTED, derived→UNKNOWN | Task 4 |
| Entitlement ACL | Task 5 |
| Frozen matrix Interlock | Task 5 |
| Refund dual-action demo | Task 6 |
| Multi use-case reference params | Task 7 |
| Business proposal deliverable | Task 8 |
| Pitch deliverable | Task 9 |
| Working prototype deliverable | Tasks 1–7 + 10 |
| No LLM on critical path | Global + Tasks 1–7 |

## Execution order

`1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10`  
Prototype (A–B) before proposal/pitch (C–D) so the written materials cite real demo output.
