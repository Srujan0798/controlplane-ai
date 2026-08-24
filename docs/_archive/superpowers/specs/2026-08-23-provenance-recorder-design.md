# Provenance Recorder MVP — Design Spec

**Date:** 2026-08-23  
**Challenge:** Accenture Innovation Challenge 2026 · PS #1 · Team ControlPlane  
**Status:** Approved  
**Source of truth:** [`docs/ARCHITECTURE.md`](../../ARCHITECTURE.md) (frozen)  
**Round 2 brief:** [`docs/Accenture Innovation Challenge - Round2 - Detailed Problem Statements.pdf`](../../Accenture%20Innovation%20Challenge%20-%20Round2%20-%20Detailed%20Problem%20Statements.pdf)  
**Slice:** Round 2 first build — keystone prototype (Phases A–B of the Round 2 plan)

---

## 1. Goal

Prove the architectural keystone in working code:

> Provenance is captured **outside** the model at context-assembly time. Claims must earn
> `SUPPORTED` by binding to those spans. Entitlement is a deterministic ACL check. Pending
> actions are priced by blast radius, not by a composite score.

**Done means:** a Python library + CLI demo that replays the frozen refund running example and
emits the dual-action outcome (R1 Edit + R3 Escalate) from a real ledger, not from narrative.

---

## 2. Non-goals (this slice)

- OpenAI-compatible reverse proxy
- Real LLM / NLI / Claim Extractor model
- Economist, Adjudicator, Red Team roles
- Shadow deployment, circuit breakers, versioned policy DAG persistence
- Framework adapters (LangChain, etc.)
- Network services / HTTP API

These may wrap the same ledger later. They must not reshape the ledger.

---

## 3. Core types

All artifacts are typed. **Nothing is passed as free text between roles.**

### 3.1 Principal

```text
Principal { id: str, roles: set[str], clearance: set[str] }
```

`clearance` is the set of ACL labels the caller is entitled to read.

### 3.2 Step

A context-assembly or tool event that *produces* spans.

```text
Step {
  step_id: str
  kind: "retrieval" | "tool" | "db" | "system"
  name: str                 # e.g. tool name
  started_at / ended_at: optional timestamps
}
```

### 3.3 Span

Ground truth of what the model was allowed to know.

```text
Span {
  span_id: str
  step_id: str              # producing step
  source_id: str
  acl: set[str]             # labels required to read this span
  content: str              # the evidence fragment
  content_hash: str         # sha256 of normalized content
  offsets: (start, end) | None
}
```

Spans are appended only through the Provenance Recorder. Model output never creates spans.

### 3.4 Claim

Typed atomic proposition extracted from the response (fixtures in this MVP).

```text
Claim {
  claim_id: str
  text: str
  kind: "numeric" | "structural" | "temporal" | "textual" | "derived"
  assertion: "categorical" | "hedged"
  role_in_action: dict[action_id, weight]   # which pending actions this claim authorizes
}
```

Default verdict before binding: **`UNSUPPORTED`**. A claim must earn `SUPPORTED`.

### 3.5 Binding & verdict

```text
Binding {
  claim_id: str
  span_ids: list[str]       # empty if unbound
  method: "exact" | "recompute" | "fixture" | "none"
  verdict: "SUPPORTED" | "CONTRADICTED" | "UNSUPPORTED" | "UNKNOWN"
}
```

**Rules for this slice:**

- Binding is a **lookup against the in-memory provenance set**, not a corpus search.
- Derived / multi-hop claims are never marked `SUPPORTED` by shallow text match → `UNKNOWN`
  or recompute-only. (`UNKNOWN` never collapses into `SUPPORTED`.)
- Absence of evidence (clause 7.2 does not exist) stays `UNSUPPORTED`, not `CONTRADICTED`.

### 3.6 Action

```text
Action {
  action_id: str
  name: str                 # e.g. "show_text", "issue_refund"
  tier: "R0" | "R1" | "R2" | "R3"
  args: dict                # structured, not free text
  irreversibility: bool
}
```

### 3.7 Evidence Ledger

Append-only, hash-chained, one per request:

```text
EvidenceLedger {
  request_id: str
  principal: Principal
  action_intent: str
  policy_version: str
  entries: list[LedgerEntry]   # each entry: {seq, type, payload, prev_hash, hash}
  spans, claims, bindings, steps, actions, decisions
}
```

Each append computes `hash = sha256(prev_hash || canonical_json(payload))`. Tampering breaks the chain.

---

## 4. Components

| Module | Role | LLM? |
|---|---|---|
| `controlplane.models` | Typed dataclasses / enums | No |
| `controlplane.ledger` | Evidence Ledger (append-only, hash-chained) | No |
| `controlplane.recorder` | Provenance Recorder — hooks context assembly | No |
| `controlplane.binder` | Deterministic claim→span binding | No |
| `controlplane.entitlement` | Entitlement Auditor — caller vs span ACL | No |
| `controlplane.interlock` | Action Interlock — matrix lookup, sole decider | No |
| `examples/refund_trace_demo.py` | Frozen running-example replay | No |
| `tests/` | Unit tests for chain, bind, entitle, matrix | No |

### 4.1 Provenance Recorder

```text
recorder.begin_request(principal, action_intent) -> EvidenceLedger
recorder.record_step(kind, name) -> step_id
recorder.record_span(step_id, source_id, acl, content, offsets=None) -> span_id
recorder.finish_context_assembly()  # freezes span set for binding
```

After `finish_context_assembly()`, new spans for that request are rejected (tamper boundary).

### 4.2 Binder

```text
binder.bind_claims(ledger, claims) -> list[Binding]
```

For the MVP, binding uses explicit fixture maps plus simple exact/substring match against span
content for textual claims. Default remains `UNSUPPORTED` when no span matches.

### 4.3 Entitlement Auditor

```text
entitlement.audit(ledger, claim_id) -> EntitlementFinding
```

If any span in a claim's binding has `acl` not ⊆ `principal.clearance`, finding =
`ENTITLEMENT_VIOLATION`. Deterministic. No classifier.

### 4.4 Action Interlock

Sole decider. Transcribe the frozen matrix — **never redraw**:

|  | Contradicted / entitlement | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** | Block | Escalate | Escalate | Escalate |
| **R2** | Block | Edit | Edit | Escalate |
| **R1** | Edit | Edit | Pass + annotate | Pass + annotate |
| **R0** | Pass + annotate | Pass + annotate | Pass | Pass |

```text
interlock.decide(ledger, action) -> Decision
```

Decision carries: actuator, matrix cell, driving claim_id(s), evidence packet fields
(claim, candidate spans, verdict, diff stub).

**Multi-action rule:** each pending action is priced separately (*worst claim weighted by that
claim's role in the pending action*). Both actuators can be correct simultaneously.

---

## 5. Demo scenario (frozen)

Refund agent response:

> `Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.`

Facts encoded as fixtures:

1. **Clause 7.2 does not exist** — no span contains it → claim stays `UNSUPPORTED` (absence).
2. At least one grounding span for another claim comes from a document whose ACL excludes the caller → entitlement violation on the user-visible text path.
3. Multiple tool steps; some produce spans that ground nothing → visible in ledger walk-back (cost axis demo, informational in this slice).

Pending actions:

| Action | Tier | Expected finding | Actuator |
|---|---|---|---|
| Show text to customer | R1 | entitlement violation on a claim in the text | **Edit** |
| Issue the refund | R3 | unsupported categorical (clause 7.2) | **Escalate** |

Demo CLI prints the ledger summary, bindings, entitlement findings, and both decisions.

---

## 6. Repository layout

```text
controlplane/
  __init__.py
  models.py
  ledger.py
  recorder.py
  binder.py
  entitlement.py
  interlock.py
examples/
  refund_trace_demo.py
tests/
  test_ledger.py
  test_binder.py
  test_entitlement.py
  test_interlock.py
  test_refund_scenario.py
pyproject.toml
README.md
```

Python ≥ 3.11. Stdlib-first; no ML deps in this slice.

---

## 7. Testing

| Test | Asserts |
|---|---|
| Ledger hash chain | Append order; tamper detection on mutated entry |
| Recorder freeze | Spans rejected after `finish_context_assembly` |
| Binder default | Unmatched claim → `UNSUPPORTED`, never silent `SUPPORTED` |
| Absence ≠ contradiction | Missing clause 7.2 → `UNSUPPORTED` |
| Entitlement | ACL mismatch → `ENTITLEMENT_VIOLATION` without model |
| Matrix transcription | R3×unsupported-categorical → Escalate; R1×entitlement → Edit |
| Dual-action scenario | Same ledger yields Edit + Escalate together |
| Derived claims | Marked derived → not `SUPPORTED` via shallow match |

---

## 8. Success criteria

1. `python -m examples.refund_trace_demo` (or `python examples/refund_trace_demo.py`) exits 0 and
   prints both expected actuators.
2. `pytest` passes all tests above.
3. No LLM / network calls on the critical path.
4. Architecture content laws preserved in code comments / demo output where they are load-bearing
   (clause 7.2 *does not exist*; matrix transcribed; default unsupported).

---

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Demo looks like a scripted story, not a system | Ledger hashes + matrix cell IDs printed; tests lock the dual-action outcome |
| Binder accidentally “supports” via fuzzy match | Exact/fixture only; derived route forced to `UNKNOWN` |
| Scope creep into proxy/NLI | Explicit non-goals; reject PRs that add model calls to interlock |
| Matrix redraw | Matrix encoded as a frozen constant table; tests pin every cell used by the demo |

---

## 10. Follow-ons (explicitly later)

1. OpenAI-compatible reverse proxy wrapping the recorder hook  
2. Streaming Claim Extractor (small model) replacing fixture claims  
3. NLI Prosecutor for textual claims only  
4. Shadow mode + published FNR pipeline  

---

## 11. Approval gate

Implementation starts only after this spec is reviewed and approved.
