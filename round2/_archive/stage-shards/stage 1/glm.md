# Stage 1: Scope Lock + Prototype Boundary + Explicit Assumptions

---

## 1. Core Thesis for Round 2

The frozen Round 1 mechanism — provenance captured at context assembly, inverted burden of proof, entitlement checking, blast-radius-priced verification — is not a feature to be added to an enterprise AI stack. It is the admission-control layer that the stack is missing, and it scales across use cases not by adding new detectors but by calibrating the same graph reads per route. Round 2 demonstrates that one graph — STEP → SPAN → CLAIM → ACTION — produces three different actuators on the same response, catches the failure mode that output-only tools are structurally blind to, and does it in the latency budget of the action it is gating.

---

## 2. Selected Use Cases for the Prototype

### Use Case A: Customer Support Refund Agent

**Concrete description:** An AI agent handles refund requests against a vendor agreement knowledge base. It reads the agreement, assesses eligibility, and issues a refund via a payment tool call.

**Risk signature:** Fabricated policy citations (hallucination) + over-permissioned retrieval leaking cross-tenant clause data (entitlement) + irreversible financial action.

**Latency budget:** Text to user ≤400ms perceived; action gate ≤40ms added on top of 200ms–2s tool round-trip.

**Dominant blast-radius tier(s):** R1 (text shown to customer) and R3 (irreversible payment) — simultaneously, on the same response.

**Frozen mechanism most powerfully demonstrated:** The two-pending-actions resolution. One response, two actuators (Edit on text, Escalate on action), driven by the exact same claim set read against two different R-tiers. This is the single most sophisticated matrix read possible, and no competitor can do it because none of them separate text from action.

### Use Case B: Internal Knowledge Assistant (Cross-Departmental)

**Concrete description:** An employee queries an internal knowledge base containing HR compensation bands, legal contracts, and engineering documentation. Different departments have different read entitlements per document class.

**Risk signature:** Pure entitlement leakage — no hallucination, no fabrication. The model correctly retrieves and accurately states a fact from a document the caller is not authorised to read.

**Latency budget:** ≤200ms p95 added (R0/R1 text-only, Lane 1 deterministic only).

**Dominant blast-radius tier(s):** R0 (internal draft) and R1 (user-visible, read-only).

**Frozen mechanism most powerfully demonstrated:** The entitlement check in isolation. This is the mechanism the architecture document calls "the most differentiated single mechanism" and "structurally impossible for any output-only competitor to replicate." By removing hallucination from the scenario entirely, the demo proves the check catches a real failure mode that has nothing to do with whether the model is "right" — only whether it was allowed to know what it is saying.

### Why this combination is the strongest possible demonstration

The two use cases are orthogonal on the failure mode axis (fabrication vs. leakage) and span four of the five R-tiers (R0, R1, R3). Use Case A exercises the full matrix with two actuators on one response. Use Case B exercises the entitlement check in its purest form, proving the mechanism is not just a hallucination detector with an ACL stapled on. Together they demonstrate that the one graph handles incommensurable failure modes without adding a new detector — it just reads a different axis. No third use case adds a mechanism the judge hasn't already seen; a third use case only adds breadth, and breadth is what the architecture explicitly refuses.

---

## 3. Prototype Boundary (Hard)

### What the working prototype WILL demonstrate (observable by a judge)

1. **Real-time graph construction:** As simulated model output streams in, the UI constructs the STEP → SPAN → CLAIM → ACTION graph node-by-node. Spans appear first (captured at "context assembly"), then claims light up as they are extracted, then bindings draw edges.

2. **Claim binding in real-time:** At least one claim visibly binds to a span (edge turns green, verdict flips from UNSUPPORTED to SUPPORTED). At least one claim fails to bind (no edge drawn, verdict stays UNSUPPORTED).

3. **Entitlement violation detection:** An entity in the output binds to a span whose ACL excludes the calling principal. The span turns red. The verdict flips to a specific entitlement-violation state (not a generic "risk score").

4. **Two actuators on one response (Use Case A):** The same response produces Edit on the R1 text component and Escalate on the R3 action component. The matrix cell that produced each actuator is highlighted on-screen.

5. **Evidence packet on Escalate:** The Escalate actuator opens to show: the unsupported claim, the candidate spans that were checked, the verdict on each, and the diff between what the model said and what the evidence supports.

6. **Per-claim user surface:** Each claim in the final output shows exactly one of: Verified / Uncertain / Blocked. No raw scores, no confidence percentages.

7. **Empty gate-report schema:** The audit output ships as a typed JSON schema with placeholder fields for per-route FNR — fields filled with null, not fabricated numbers.

### What it will deliberately NOT demonstrate (and why)

| Excluded | Reason |
|---|---|
| Live LLM inference | The architecture is API-layer-only; the model is a black box. Simulating the output stream proves the control plane works without requiring us to also be a model provider. Claiming live inference would imply we need model access, which the architecture explicitly rejects. |
| Async lanes (semantic-entropy, counterfactual bias) | These are real mechanisms but they are Lane 3 — off the critical path by construction. Demonstrating them would consume demo time on the least differentiated part of the system and invite "LLM-as-judge" pattern-matching. |
| Cost/waste measurement (dead compute) | The mechanism is correct and defensible, but it is a backward graph read, not a forward control decision. It belongs in the business proposal, not the live demo. A judge who asks about it gets the exact explanation; a judge who doesn't isn't distracted. |
| Multi-tenant concurrent load | Demonstrates operational maturity, not architectural differentiation. The mechanisms are identical on one trace or ten thousand; showing ten thousand adds engineering complexity with zero additional insight. |
| Non-convergence breaker (loop termination) | An edge case handler. Correct to include in the architecture, fatal to include in a 5-minute demo if it crowds the core mechanism. |
| Real IAM integration | The ACLs are hard-coded on the span set. Claiming real IAM integration would require a real enterprise directory, which we don't have, and would invite "but your demo isn't really checking their IAM" — a true but irrelevant attack. The mechanism is identical either way. |
| Actual proxy deployment | The prototype runs as a standalone application with a simulated input stream. Showing an OpenAI-compatible proxy is a deployment detail, not an architectural proof. |

### Minimum viable demo that still feels advanced

**One trace through Use Case A (the refund), followed by one trace through Use Case B (the entitlement leak).** Total runtime: under 5 minutes. The UI is a graph visualisation panel on the left, the streaming model output with per-claim annotations on the right, and the matrix + actuator state at the bottom. No dashboard. No charts. No metrics. A graph, a verdict stream, and two different actuators on the same response. An engineer watching this should think "that's a privilege-ring implementation for LLM outputs" — not "another safety dashboard."

---

## 4. Explicit Assumptions

**Data sources:**
- Hand-crafted span sets: 10–20 spans per demo trace, each carrying source_id, ACL (principal list), content hash, and character offsets
- Spans are pre-loaded into the Provenance Recorder before the demo begins (simulating real-time context-assembly capture)
- Use Case A spans derive from a simulated "vendor agreement" document; Use Case B spans derive from simulated HR, legal, and engineering documents with overlapping entity references

**Model output:**
- Pre-recorded streaming text simulating an LLM response (not a live model call)
- Output includes: factual claims with matching spans, one fabricated claim (clause 7.2 in Use Case A), one correctly-stated claim from an unauthorised source (Use Case B), and one tool-call action (refund issuance in Use Case A)
- Streaming is simulated at ~50 tokens/second to replicate real-time perception

**Claim extraction:**
- For deterministic demo: claims are pre-computed and time-stamped to appear at sentence boundaries during the stream
- If compute allows: a small local model (1–3B, e.g., via Ollama) performs live extraction — but the demo does not depend on this; pre-computed claims are the baseline

**NLI binding:**
- A pre-trained cross-encoder (e.g., DeBERTa-v3-base fine-tuned on MNLI/SNLI) runs locally for the textual binding path
- Numeric/structural claims are verified deterministically against span content (regex + recomputation)
- Binding runs at sentence-boundary triggers during the stream

**Entitlement check:**
- ACLs are hard-coded dictionaries on the span set: `{source_id: [allowed_principals]}`
- The calling principal is set per demo trace (e.g., "agent-cs-emea" for Use Case A, "eng-lead-west" for Use Case B)
- Check is pure set-membership: is the principal in the span's ACL list? No model involved.

**Traffic shape:**
- Single trace at a time, sequential
- No concurrent requests, no load testing

**Regulatory posture:**
- Generic enterprise — no specific jurisdiction (GDPR, HIPAA, etc.) is claimed or simulated
- The architecture is jurisdiction-agnostic by design (ACLs and blast-radius tiers are not regulatory constructs); pinning a jurisdiction would add a claim we can't defend

**Integration surface:**
- Standalone application: Provenance Recorder (simulated) → Claim Extractor → Prosecutor → Entitlement Auditor → Action Interlock → UI
- No real LLM API integration in the prototype
- No real application backend integration

**Evaluation data:**
- Claims and their ground-truth verdicts are pre-labeled for the demo traces
- The empty gate-report schema uses typed null placeholders, not estimated numbers
- No claim is made about measured FNR — the format is demonstrated, the values are left for production

**Tool calls:**
- Use Case A includes one pending tool call (issue_refund, args: {amount: 184000, clause: "7.2"})
- The tool call is not actually executed — it is intercepted at the Action Interlock and the actuator is applied

---

## 5. Success Criteria for the Prototype

Each criterion is binary — a judge can say yes or no after watching the demo.

1. **Graph constructed live:** The STEP → SPAN → CLAIM → ACTION graph is visibly built node-by-node during the streaming output. [ ] Yes / [ ] No

2. **Claim binds to span:** At least one claim transitions from UNSUPPORTED to SUPPORTED with a visible binding edge to a specific span. [ ] Yes / [ ] No

3. **Claim fails to bind:** At least one claim remains UNSUPPORTED with no binding edge, and this state is visibly different from SUPPORTED. [ ] Yes / [ ] No

4. **Entitlement violation detected:** An entity in the output binds to a span whose ACL excludes the calling principal, and this is flagged as a distinct verdict (not merged with hallucination). [ ] Yes / [ ] No

5. **Two actuators on one response:** The same Use Case A response produces exactly two actuators: Edit (on text) and Escalate (on action). [ ] Yes / [ ] No

6. **Evidence packet visible:** The Escalate actuator displays a packet containing: the unsupported claim, the spans checked, the verdict per span, and the diff. [ ] Yes / [ ] No

7. **Matrix cells highlighted:** The R×S matrix cells that produced each actuator are explicitly highlighted during the demo. [ ] Yes / [ ] No

8. **No unearned SUPPORTED:** No claim transitions to SUPPORTED without a visible binding event occurring first. [ ] Yes / [ ] No

9. **Per-claim surface, no scores:** Each claim in the final output shows exactly one of {Verified, Uncertain, Blocked}. No confidence score, no risk score, no 0–100 number appears on the claim-level UI. [ ] Yes / [ ] No

10. **Empty schema, not fabricated numbers:** The gate-report output contains typed fields for FNR populated with null — not with estimated or plausible numbers. [ ] Yes / [ ] No

**Prototype succeeds if and only if all 10 criteria are met.**

---

## 6. Fidelity Self-Check

| Frozen non-negotiable | Status in this proposal | Tension? |
|---|---|---|
| Default = UNSUPPORTED | Claims start UNSUPPORTED, must earn SUPPORTED via visible binding. Criterion 8 enforces this. | None |
| Entitlement / ACL check | Use Case B is built entirely around this mechanism. Criterion 4 tests it. | None |
| The exact R×S matrix | Criterion 7 requires the matrix cells to be highlighted — meaning the matrix is present, transcribed, and read from. No redrawing. | None |
| Hard gate on actions, not tokens | Use Case A: text streams (Edit actuator), action is gated (Escalate actuator). Criterion 5 tests the split. | None |
| Published own FNR as a format | Criterion 10: empty schema with typed null placeholders. | None |
| The two-pending-actions resolution | Use Case A produces R1 × entitlement → Edit AND R3 × unsupported-categorical → Escalate on the same response. Criterion 5 tests this. | None |

**Resolution if tension existed:** Any tension would be resolved in favour of the freeze. In this case, no tension exists. The prototype is a direct rendering of the frozen architecture on two hand-crafted traces.

---

## 7. Biggest Scope Risk + Exact Mitigation

**Risk:** The demo feels like a visualisation of a pre-computed result rather than a live system making decisions — the judge sees an animation, not a mechanism.

**Why it is the biggest risk:** The prototype uses pre-recorded model output and pre-computed claims for deterministic demo behaviour. If the UI simply "plays back" a pre-baked sequence of graph-node appearances, a technically literate judge will correctly identify that the control plane isn't actually running — it's a PowerPoint with a frame rate. This kills credibility instantly because the architecture's entire claim is that it runs at inference time, in the commit path.

**Exact mitigation:** The binding step runs live. Even though the claims are pre-computed, the NLI cross-encoder runs in real-time against the span set when the claim arrives at the binding checkpoint. The judge sees: claim appears → a brief processing state (~50–100ms) → the binding edge draws or doesn't. If the demo environment permits, the claim extraction also runs live via a small local model — but the binding is non-negotiable. The entitlement check is already deterministic and instantaneous, so it provides no latency signal; the binding is the proof that computation is occurring. If a judge asks "is this pre-computed," the honest answer is "claims are pre-extracted for demo stability; binding runs live — watch the latency counter on the edge." That answer survives. "Everything is pre-computed" does not.

**Secondary mitigation:** Include one unscripted moment. After the two scripted traces, offer the judge the ability to modify the calling principal (e.g., switch from "eng-lead-west" to "hr-director") and re-run Use Case B. The entitlement verdicts flip in real-time because the ACL check is live set-membership. This is trivial to implement and proves the system is a running engine, not a recording.