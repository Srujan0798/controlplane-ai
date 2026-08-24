**1. Prototype Goal**

This working prototype exists to prove one thing: an unproven or unauthorized claim cannot authorize an action, because provenance is captured outside the model, every claim starts UNSUPPORTED, entitlement is deterministic set-membership, and the exact frozen R×S matrix prices the outcome by blast radius. It demonstrates the two-pending-actions resolution on the refund running example and the principal-flip entitlement check on the knowledge route, both reading the same STEP → SPAN → CLAIM → ACTION Evidence Ledger. Nothing else is in scope.

**2. Exact Functional Scope**

**Implemented and runnable**
- Context-assembly Provenance Recorder that writes spans with `source_id · ACL · content_hash · offsets · principal` before any claim is judged.
- Typed Evidence Ledger (append-only) for a single request/session.
- Claim extraction into typed check-worthy propositions (categorical / hedged).
- Claim-type routing: numeric/date/ID → deterministic recomputation; textual → binding against the captured provenance set only; derived → recompute or UNKNOWN.
- Default = UNSUPPORTED; a claim becomes SUPPORTED only by proof against the ledger.
- Deterministic Entitlement Auditor (caller vs source ACL, zero LLM).
- Action Interlock that applies the exact frozen R×S matrix **per pending action**.
- Surgical Edit (strip failing claim or one constrained regeneration naming the failing span; re-gate).
- Evidence-packet Escalation (claim + candidate spans + verdict + diff).
- Hard gate on the mock refund tool: the tool cannot commit while Escalate or Block is in force.
- Text hold-back buffer.
- Empty typed FNR schema (null / placeholder / labelled prototype-corpus only).
- Live principal switch on the knowledge route that flips entitlement outcomes.

**Deliberately mocked**
- Generator: OpenAI-compatible stub or thin real API call that emits pre-scripted or lightly prompted responses for the demo traces.
- Refund tool: deterministic mock that logs “would have committed” vs “held” and never moves money.
- Source stores: in-memory or local JSON/SQLite corpora with synthetic ACLs.
- NLI cross-encoder: optional thin real model or deterministic mock for the demo traces (binding still runs against the provenance set).
- Human escalation target: display of the evidence packet only; no queue/SLA UI.

**Completely out of scope (re-affirm Stage 1 exclusions)**
- Third live decision-support / bias route.
- Per-response bias verdicts or any live bias actuator.
- Production-scale load, real payments, real PII, live IAM remediation.
- LLM-as-judge on the critical path, confidence/risk scores, open-web verification.
- Generative full-answer rewrite, fabricated production FNR numbers.
- Lane-3 critical-path demo, multi-agent conversation, human triage SLA UI.
- Model weights, logits, or fine-tuning.

**3. Synthetic Data & Corpora Requirements**

Minimum enterprise-shaped corpora (no real PII):

**Refund route corpus**
- Vendor agreement document(s) that deliberately **omit** any clause 7.2 (absence is the failure mode).
- Order/account record containing the amount ₹1,84,000 and related identifiers.
- One policy/HR span whose ACL excludes the default customer-support principal (for the R1 entitlement path inside the same response).
- Clean supporting spans for at least one non-refund claim so a SUPPORTED path is visible.
- Numeric fields that support deterministic recomputation (amount, date, order ID).

**Knowledge route corpus**
- Mixed well-governed and loosely governed internal documents (policy, HR-shaped, project notes).
- At least one span whose ACL includes principal P1 and excludes principal P2 (or vice versa) so the same claim flips authorization when only the caller changes.
- At least one clean, fully entitled, bindable answer path.

**Shared requirements**
- Every span carries `source_id`, `ACL`, `content_hash`, offsets.
- Tool-result spans treated identically to retrieved spans.
- At least one purely parametric (no-retrieval) claim path for the declared-ungrounded case.
- Prompt-injection attempt present as untrusted input that cannot modify the ledger.

**4. Core Components to Implement**

| Component | Responsibility | Real / Mock |
|---|---|---|
| Provenance Recorder | Captures every span at context assembly with source · ACL · hash · offsets · principal | **Real** |
| Evidence Ledger | Append-only, hash-chained store of STEP → SPAN → CLAIM → ACTION for one request | **Real** |
| Claim Extractor | Emits typed check-worthy claims (categorical/hedged) from the response stream | Real or thin model |
| Prosecutor / Binder | Attempts to prove each claim against the provenance set only; default UNSUPPORTED; routes by claim type | Real (deterministic + optional NLI) |
| Entitlement Auditor | Caller principal vs source ACL; Lane-1; zero LLM | **Real** |
| Action Interlock | Computes R, applies exact frozen matrix per pending action, emits actuator | **Real** (pure rule engine) |
| Surgical Editor | Strips failing claim or issues one constrained regeneration; re-gates | Real |
| Evidence Packet Builder | Packages claim + candidate spans + verdict + diff on Escalate | **Real** |
| Text Hold-back | Short trailing buffer before release | Real |
| Mock Refund Tool | Deterministic side-effect that respects the interlock (commit or hold) | **Mock** |
| OpenAI-compatible Proxy / Stub | Intercepts generation and tool calls | Thin real or stub |
| FNR Schema Surface | Renders the typed empty schema | **Real** (display only) |
| Principal Switch Control | Changes only the calling principal and re-runs entitlement | **Real** |
| Demo UI (Ledger-first) | Majority screen real-estate for the live graph + matrix cells + packet | **Real** |

**5. Demo Flows (Judge-Facing)**

**Primary flow — Refund dual-action (build backward from the action gate), ≤5 min**

1. Context is assembled; spans with source · ACL · hash appear in the ledger **before** any claim.
2. Response is generated containing:
   - at least one bindable claim,
   - one claim grounded in an ACL-excluded span,
   - the categorical claim “Refund of ₹1,84,000 issued under clause 7.2 …”,
   - a pending refund tool call.
3. Ledger shows every claim starting UNSUPPORTED.
4. Clause 7.2 has no span → remains UNSUPPORTED (categorical).
5. Action Interlock evaluates two pending actions simultaneously:
   - Show text → R1 × entitlement violation → **Edit** (surgical strip).
   - Issue refund → R3 × unsupported-categorical → **Escalate** (held).
6. Evidence packet is visible (claim, candidate spans, verdict, diff).
7. Mock refund tool does **not** commit; “held” is visible.
8. Exact matrix cells are highlighted for both actuators.
9. Empty FNR schema is visible.

**Secondary flow — Principal-flip entitlement, ≤2 min**

1. Same or equivalent knowledge claim and span.
2. Change **only** the calling principal.
3. Entitlement outcome flips (authorized → unauthorized or reverse).
4. ACL decision uses zero LLM; ledger records principal + source_id.
5. Matrix cell updates accordingly (R1 × entitlement → Edit).

**Optional third beat (only if time and clarity allow)**
- Same claim consequence forced to R1 vs R3 → actuator changes solely because R changed, not because any score changed.

**Governing demo rule:** majority UI = Evidence Ledger. If the graph can be removed and the demo still looks the same, the prototype has failed.

**6. Evidence Ledger & UI Requirements**

Visible on screen for every demo run:
- Full STEP → SPAN → CLAIM → ACTION graph for the current request.
- Every span’s source_id, ACL, content_hash, offsets, principal.
- Every claim’s starting verdict (UNSUPPORTED) and final binding status.
- Per-pending-action matrix cell that fired and the resulting actuator.
- Evidence packet on Escalate.
- Action disposition (held / committed) for the mock refund tool.
- Empty typed FNR schema (nulls or labelled prototype-corpus only).
- Latency / lane indicators for the checks that ran.

No composite risk score, no confidence number, no “blocked response” label for the refund, no LLM-as-judge output pane.

**7. Success Criteria → Implementation Checks**

| # (R2S1 §5) | Criterion | Concrete implementation / runtime check |
|---|---|---|
| 1 | Provenance outside the model | Spans written to ledger with source/ACL/hash **before** claim extraction runs; model has no write path to the ledger. |
| 2 | One-graph invariant | Single Evidence Ledger object per request; UI renders one connected graph. |
| 3 | UNSUPPORTED default | Claim objects are created with verdict = UNSUPPORTED; only the binder can promote them. |
| 4 | Absence ≠ contradiction | Clause 7.2 has zero matching spans; verdict stays UNSUPPORTED; UI never displays “caps/denies/doesn’t cover”. |
| 5 | Claim-level proof | Supported claim shows explicit span binding edge; unsupported claim shows empty binding set. |
| 6 | Two pending actions | Interlock emits two independent actuators (Edit + Escalate) from the same response; both visible. |
| 7 | Hard action gate | Mock refund tool checks interlock result; commit path is unreachable while Escalate/Block is active. |
| 8 | Entitlement independence | Same span + claim under two principals produces different ACL outcomes; zero LLM in the path. |
| 9 | Exact matrix fidelity | Actuator table is hard-coded to the frozen R×S cells; no invented labels or composite scores. |
| 10 | Evidence packet | Escalate always materializes claim + spans + verdict + diff object and renders it. |
| 11 | Surgical edit | Failing claim is removed or one constrained regeneration is issued; result re-enters the gate. |
| 12 | FNR format honesty | Schema rendered with null/placeholder or clearly labelled prototype-corpus values only. |
| 13 | No confidence driver | Disposition function signature is `(R, S) → actuator`; no score parameter. |
| 14 | Prompt injection cannot author provenance | Injected text has no API to write spans or bindings; ledger remains append-only from the recorder. |
| 15 | Refund language fidelity | UI and logs use “held and escalated with the evidence packet”; the word “blocked” is never emitted for the R3 refund path. |

**8. Build Order Recommendation**

1. Evidence Ledger + Provenance Recorder (keystone).  
2. Action Interlock with the exact frozen matrix (hard-coded).  
3. Mock refund tool that respects the interlock.  
4. Entitlement Auditor (deterministic).  
5. Claim extraction + default-UNSUPPORTED + binding against ledger only.  
6. Surgical Edit + evidence-packet builder.  
7. Text hold-back.  
8. Demo UI that makes the ledger the majority of the screen.  
9. Principal-switch control.  
10. Empty FNR schema surface.  
11. Optional NLI or numeric recomputation polish.  

Never invert this order. The differentiation moment (action gate + dual actuators + ledger) must exist before any secondary surface is built.

**9. Fidelity Self-Check**

- Default = UNSUPPORTED — protected; claims are born UNSUPPORTED and must earn promotion.  
- Entitlement / ACL check — protected; deterministic, always-on, zero LLM, identity-carrying.  
- Exact R×S matrix — used verbatim; never redrawn.  
- Hard gate on actions — protected; text hold-back only; tool commit is gated.  
- FNR as empty typed schema — protected; no fabricated production numbers.  
- Two-pending-actions resolution — centrepiece of the primary demo; R1 Edit + R3 Escalate simultaneous and distinct.  
- No LLM-as-judge on the critical path — Action Interlock is a pure rule engine.  
- Bias is not a live per-response verdict — not present in the prototype.  

No competing mechanism, composite score, or confidence-driven disposition is specified. The prototype is the frozen core made executable and visible.