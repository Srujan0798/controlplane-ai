# Stage 1 — Scope Lock, Prototype Boundary, Explicit Assumptions

---

## 1. Round 2 Core Thesis

Round 1 proved the mechanism on one trace: provenance captured outside the model, inverted burden of proof, blast-radius-priced verification, entitlement as a deterministic gate. Round 2 proves the same architecture governs heterogeneous enterprise routes — a customer refund agent, an internal knowledge assistant, a regulated decision-support copilot — without a single new mechanism, without one-size-fits-all thresholds, and without diluting the core differentiator: **the graph is assembled before the model runs, the matrix is a pure rule engine at decision time, and the entitlement check is structurally impossible for any output-only competitor to replicate.** The prototype makes this visible by showing the same response hitting different actuators at different blast-radius tiers on the same graph.

---

## 2. Use-Case Selection for the Prototype

### Use Case 1 — Customer Support Refund Agent

**Concrete description.** An AI agent handles customer refund and dispute requests. It retrieves the customer's purchase history, applicable refund policies from an internal policy repository, and generates a response that may include issuing a refund via a payment API. This is the frozen running example (₹1,84,000, clause 7.2).

**Risk signature.** High. Refunds are irreversible financial actions. The agent cites policy clauses that may or may not exist in the retrieval set. Customer-facing text must be accurate. Internal policy documents carry role-based ACLs (back-office only, not customer-visible).

**Latency budget.** Text response: ≤500ms perceived (hold-back buffer handles this; the user sees the model's speed). Refund action gate: ≤40ms additional on top of the payment API round-trip (~200ms–2s), amortized inside the tool's own latency.

**Dominant blast-radius tiers.** R1 (customer-visible text) and R3 (irreversible refund execution).

**Most powerfully demonstrated mechanism.** Two pending actions on one response. The matrix produces **Edit** for the text (entitlement violation — a span from a back-office-only document grounds a claim in customer-visible output) and **Escalate** for the refund (unsupported-categorical — clause 7.2 has no span). This is the single strongest demonstration of the matrix doing something no composite risk score can do: identical response, two different actions, both correct simultaneously. **Proof scales with consequence.**

---

### Use Case 2 — Internal HR/Policy Knowledge Assistant

**Concrete description.** An employee queries the internal AI assistant about parental leave entitlements, salary bands for a specific role, or upcoming org changes. The assistant retrieves from an internal knowledge base with mixed governance — some documents are company-wide, some are HR-only, some are department-scoped.

**Risk signature.** Medium. No financial action, but cross-department data leakage is a real and expensive enterprise incident. An Engineering manager must not see HR salary bands for other departments, even if those documents are indexed in the same RAG store. Information is read-only but sensitive.

**Latency budget.** ≤300ms perceived. No hard action gate — this is R0/R1 traffic only. The system should feel fast and non-intrusive.

**Dominant blast-radius tiers.** R0 (internal draft, human reads first) and R1 (user-visible, read-only).

**Most powerfully demonstrated mechanism.** The **entitlement/ACL check**. A span from an HR-restricted document binds to a claim in the response, but the calling principal's role does not have ACL permission for that source. This is caught **deterministically — no LLM call, no classifier, no embedding distance.** Sub-millisecond. This use case also demonstrates that R0/R1 traffic passes with annotation rather than blocking — the system does not create alert fatigue on low-risk routes. The contrast with Use Case 1 (where the same architecture holds a payment) is the matrix working as designed.

---

### Use Case 3 — Insurance Claims Decision-Support Copilot

**Concrete description.** An AI copilot assists claims adjusters by reviewing submitted insurance claims, retrieving applicable policy terms, and recommending approve/deny/pending with cited justification. In autonomous mode (for claims below a monetary threshold), it can auto-approve without human review.

**Risk signature.** High. Regulatory exposure (insurance regulation mandates auditable decision trails). Auto-approval is an irreversible financial commitment. Policy citations must be verifiable against actual policy text. Bias in approve/deny recommendations carries legal liability under anti-discrimination statutes.

**Latency budget.** Recommendation text: ≤1s perceived (adjuster reviews asynchronously). Auto-approval gate: ≤40ms additional on top of the approval API round-trip. The adjuster-facing path is more latency-tolerant; the autonomous path is not.

**Dominant blast-radius tiers.** R2 (reversible write — adjuster can override a recommendation) and R3 (irreversible — auto-approved claim commits funds).

**Most powerfully demonstrated mechanism.** The **R3 hard gate on an irreversible action**. A claim recommendation cites a policy clause that does not bind to any captured span. The system holds the auto-approval and escalates with an evidence packet (the claim, the candidate spans searched, the verdict, the diff). This also demonstrates the **audit trail**: every decision is hash-chained, carries the exact evidence fragment, and is reviewable — satisfying the regulatory requirement that any AI-assisted decision in insurance must be explainable and overridable by a licensed adjuster.

---

### Why This Combination

These three use cases span R0 through R3, exercise all four actuators (Pass, Pass+annotate, Edit, Escalate), demonstrate the entitlement check on a real enterprise failure mode, show the two-pending-actions resolution, and force the matrix to produce different actions for the same verdict at different blast-radius tiers. No two of these use cases alone demonstrate all of those properties. The combination also mirrors the reference parameter set (customer-facing, internal, decision-support) exactly.

---

## 3. Prototype Boundary (Hard)

### What the Working Prototype WILL Demonstrate

A judge must be able to observe each of the following in a live or recorded demo:

1. **Provenance Recorder in action.** For every query, the prototype captures spans at context-assembly time with `source_id`, `ACL`, `content_hash`, and `offsets`. The judge sees the span set before the model's output is evaluated.

2. **Claim extraction at sentence boundaries.** The model's output is decomposed into typed, check-worthy propositions (numeric, entity, date, policy, causal). Each tagged categorical or hedged.

3. **Binding engine — two paths.** Numeric/structural/temporal claims are **recomputed deterministically** against the span set. Textual/factual claims are evaluated by an **NLI cross-encoder** against the provenance set only (never the open web). The judge sees the verdict per claim: SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN.

4. **Default = UNSUPPORTED enforced.** Every claim starts red. The judge sees claims remain UNSUPPORTED when no binding exists. SUPPORTED is earned, never assumed.

5. **The R×S matrix producing different actuators.** The same response (the refund trace) hits R1 and R3 simultaneously. The judge sees Edit for the text and Escalate for the refund — two pending actions, two actuators, one response. Separately, the judge sees an R0/R1 knowledge query pass with annotation on the same verdict type that would Escalate at R3.

6. **Entitlement/ACL violation caught deterministically.** A span whose ACL excludes the calling principal binds to a claim. The system blocks or edits without any LLM call in the decision path. The judge sees: no model invocation, sub-millisecond verdict, the ACL mismatch surfaced explicitly.

7. **Gate report as empty schema.** The per-route false-negative rate is displayed as a typed placeholder structure — not a fabricated number. The judge sees the format and understands that the emptiness is the credibility play.

8. **Per-route latency measurement.** The prototype displays p50 and p95 latency per route, measured on the demo traces. The judge can verify the numbers against the architecture's claims.

9. **Evidence packet on Escalate.** When the matrix routes to Escalate, the judge sees the packet: the claim text, the candidate spans searched, the verdict, the diff between what was claimed and what was found.

### What the Prototype Will Deliberately NOT Demonstrate

| Excluded | Precise Reason |
|---|---|
| **Async lane: semantic-entropy probe** | Requires k=5 resamples per claim with no retrieval context. This is a statistical mechanism that needs a rolling sample to calibrate. It belongs in the business proposal as the parametric-answer mitigation (QA B1), not in the core demo. The demo shows the deterministic path, which carries 80–90% of enforcement weight. |
| **Async lane: counterfactual bias replay** | Requires perturbing protected attributes over a rolling window and measuring decision flip rate. This is a distributional property — it cannot be shown on a single trace. Describe in the business proposal; the demo states the mechanism and shows the route-level configuration. |
| **Economist: dead compute, non-convergence breaker** | Requires multi-step agent traces with tool-call graphs. The prototype uses single-turn traces. Dead compute is the most defensible number (Architecture §6), but computing it requires the backward graph walk on a real multi-step agent. Describe in the proposal; show the backward-walk logic on a simplified two-step trace if time permits. |
| **Red Team (offline adversarial probing)** | Not a live-path mechanism. It probes ControlPlane's own validators offline. Describe in the proposal. |
| **Production-scale throughput** | Tens of thousands of interactions/week is a production claim. The prototype demonstrates correctness and mechanism, not throughput. Latency is measured on individual traces, not at scale. |
| **Real regulatory compliance (HIPAA/GDPR/DPDPA)** | The prototype uses simulated data. The audit trail structure is shown, but no real compliance certification is claimed. The business proposal addresses regulatory posture. |
| **Multi-turn compounding risk** | The prototype demonstrates single-turn traces. Multi-turn risk (where one questionable output shapes downstream decisions) is addressed in the business proposal as a design extension — the graph structure supports it (STEP → SPAN → CLAIM → ACTION chains across turns), but the prototype does not demo it. |
| **LLM-as-judge or confidence thresholding** | Deliberately excluded. These are the rejected approaches (Architecture §8). The prototype demonstrates why they are unnecessary by showing deterministic and NLI-based binding doing the work. |

### Minimum Viable Live Demonstration

The demo that still feels advanced and differentiated (not a toy):

1. **Three routes configured** with different R-tier profiles (customer refund, internal knowledge, claims copilot).
2. **One end-to-end trace per route**, pre-scripted with known ground truth, executed live.
3. **The refund trace resolving to two pending actions** with two different actuators — this is the moment that separates the pitch from every guardrail demo in the room.
4. **One entitlement violation caught** on the knowledge assistant route — deterministic, no LLM, visible ACL mismatch.
5. **The gate report and per-route latency** displayed after each trace.
6. **Total demo time: 8–12 minutes.** Three traces, each showing the graph building in real-time, the matrix decision, and the actuator.

---

## 4. Explicit Assumptions

### Data

| # | Assumption |
|---|---|
| D1 | Simulated enterprise data across three source systems: customer records DB, policy document repository, internal knowledge base (wiki/Confluence-style). |
| D2 | ~50 documents across sources, with known ground truth for every claim in the demo traces. Ground truth is manually verified before the demo. |
| D3 | Each source has role-based ACLs: `customer-visible`, `agent-only`, `back-office`, `hr-restricted`, `engineering-only`, `company-wide`. These are realistic simplifications of enterprise RBAC. |
| D4 | Mix of well-governed (policy docs with strict ACLs, versioned) and loosely governed (internal wiki with broad permissions, no versioning). This mirrors the reference parameter set. |
| D5 | The 15–20 demo traces include: the refund running example, at least one entitlement violation, at least one clean SUPPORTED path, at least one UNKNOWN verdict, at least one hedged claim that passes at R0/R1. |

### Models

| # | Assumption |
|---|---|
| M1 | Primary LLM: any OpenAI-compatible API endpoint. The system is model-agnostic; the demo uses one model but the architecture does not depend on which one. |
| M2 | Claim extraction: hybrid — rule-based patterns for numeric/structural/temporal claims (deterministic, near-zero cost) plus a small model (~1–3B) for textual claim boundary detection. For the prototype, the rule-based tier carries the majority of extraction. |
| M3 | NLI cross-encoder: DeBERTa-v3-base or equivalent (~300M parameters), run locally. Batched inference, 5–15ms per claim. |
| M4 | No access to model weights, logits, or fine-tuning for the primary LLM. The system works at the input/output layer only. This is stated as a constraint, not a limitation — it is the design point. |
| M5 | Deterministic recomputation for numeric claims uses exact arithmetic against span values. No approximation. |

### Traffic

| # | Assumption |
|---|---|
| T1 | Prototype: single-request interactive demo plus batch replay of 50–100 pre-scripted traces for validation. |
| T2 | Production target: tens of thousands of interactions/week across all routes combined. This is a business-proposal claim, not a prototype claim. |
| T3 | Traffic distribution: ~60% R0–R1, ~25% R2, ~15% R3. This drives the latency budget allocation (Lane 1 carries 80–90% of volume). |
| T4 | The three use cases run concurrently on the same engine, differentiated by route configuration — not by separate code paths. |

### Regulatory Posture

| # | Assumption |
|---|---|
| R1 | Dual jurisdiction: GDPR (EU operations) + DPDPA 2023 (Indian operations). This is the most relevant dual jurisdiction for an IIT Gandhinagar team presenting to Accenture. |
| R2 | Audit trail: append-only, hash-chained ledger per request, carrying principal, action intent, R-tier, spans, claims, bindings, verdicts, policy version, verifier versions, latency. Retained for configurable period (default 90 days). |
| R3 | Consent model: legitimate interest for internal tools (knowledge assistant, decision-support), explicit consent for customer-facing interactions. The prototype simulates both. |
| R4 | Clinician/adjuster override must legally record: who overrode, what was overridden, the original recommendation, the replacement decision, timestamp, and the evidence packet. The prototype captures this in the ledger. |

### Integration Surface

| # | Assumption |
|---|---|
| I1 | Deployment shape: OpenAI-compatible reverse proxy + thin context-assembly SDK hook (Python). No application rewrite. |
| I2 | The existing retrieval stack provides `source_id` for each retrieved chunk. The integration adds `ACL` and `content_hash`. This is the minimal integration surface. |
| I3 | The context-assembly hook is the keystone. If exactly one thing gets built, build the Provenance Recorder. Every other mechanism degrades to a generic guardrail without it. |
| I4 | The prototype runs locally or on a single cloud instance. No distributed deployment. The architecture supports distribution, but the prototype does not demonstrate it. |

---

## 5. Success Criteria for the Prototype

Each criterion is binary and observable. A judge watching the demo can say "yes" or "no."

| # | Criterion | Observable in Demo |
|---|---|---|
| S1 | The graph (STEP → SPAN → CLAIM → ACTION) is populated in real-time for every query, and the judge can see spans captured before the model's output is evaluated. | Yes — visual display of the graph building. |
| S2 | Every claim starts at UNSUPPORTED. No claim is marked SUPPORTED without a binding to a captured span. | Yes — the judge sees claims transition from red to green only when a binding is found. |
| S3 | The same verdict (UNSUPPORTED categorical) produces **Edit** at R1 and **Escalate** at R3, visible in the same demo run on the refund trace. | Yes — two pending actions, two actuators, one response. |
| S4 | An entitlement/ACL violation is caught without any LLM call in the decision path. The judge sees the ACL mismatch surfaced and the deterministic verdict. | Yes — the knowledge assistant trace demonstrates this. |
| S5 | The gate report displays as an empty schema with typed placeholders for per-route FNR. No fabricated numbers. | Yes — the judge sees the format and understands the design choice. |
| S6 | Per-route latency (p50, p95) is measured and displayed. The judge can verify that R0/R1 text latency is ≤40ms p50 and ≤200ms p95. | Yes — latency dashboard per route. |
| S7 | The Escalate actuator produces an evidence packet (claim, candidate spans, verdict, diff), not just an alert. | Yes — the judge sees the packet contents. |
| S8 | The three routes (refund, knowledge, claims) run on the same engine with different route configurations. No separate code paths. | Yes — the judge can see the route config and the shared engine. |
| S9 | No sentence in the demo uses the vocabulary "monitor," "detect," "observe," "watch," "guard," "trust score," "risk score," or "responsible AI" as a standalone concept. | Yes — the judge hears "authorise," "bind," "prove," "refuse," "gate," "escalate." |
| S10 | The demo shows at least one claim returning UNKNOWN (bounded proof depth or insufficient evidence), and the matrix routes it correctly rather than blocking or fabricating a verdict. | Yes — UNKNOWN is a first-class verdict that routes. |

---

## 6. Fidelity Self-Check

| Frozen Element | Status | Notes |
|---|---|---|
| **Default = UNSUPPORTED** | Preserved. Every claim in every use case starts UNSUPPORTED. SUPPORTED is earned through binding. The demo makes this visually explicit. | No tension. |
| **Entitlement / ACL check** | Preserved. Use Case 2 is specifically designed to demonstrate this. The check is deterministic, sub-millisecond, and carries identity into the verification layer — the structural property no output-only competitor can replicate. | No tension. |
| **Exact R×S matrix** | Preserved. The matrix is transcribed exactly from Architecture §4. The demo shows different cells being hit. The matrix is never redrawn — axis labels, column vocabulary, and cell values are load-bearing. | No tension. The two-pending-actions resolution (Edit at R1, Escalate at R3) is the strongest proof that the matrix is working as designed. |
| **Hard gate on actions, not tokens** | Preserved. Text streams optimistically behind the hold-back buffer. Only actions (refund execution, auto-approval) are gated. The demo shows text arriving fast and actions waiting for proof. | No tension. |
| **Published own FNR as a format** | Preserved. The gate report ships as an empty schema with typed placeholders. The prototype does not fabricate numbers. The emptiness is the credibility play — a judge who tests it finds honesty, not a bluff. | No tension. The business proposal describes the stratified shadow audit that would populate the schema over time. |
| **Two-pending-actions resolution** | Preserved. Use Case 1 (the refund trace) demonstrates this explicitly: R1 × entitlement → Edit for text; R3 × unsupported-categorical → Escalate for refund. Both correct simultaneously. | No tension. This is the centrepiece of the demo. |

**No tensions identified. Nothing in this proposal contradicts, softens, or reinterprets any frozen element.**

---

## 7. Biggest Scope Risk + Exact Mitigation

### The Risk

**The prototype looks like a RAG groundedness checker with a nicer UI.** This is the single most likely failure mode in front of judges. It happens if the demo does not make the **entitlement check** and **blast-radius differentiation** visually undeniable within the first three minutes. If the judge's first impression is "they check if the model's output matches the retrieved documents," the architecture never gets evaluated on its merits — and the narrative risk identified in the NARRATIVE document materialises exactly as predicted: *"judges pattern-match this to another AI safety tool inside the first twenty seconds."*

### The Exact Mitigation

**The demo opens on a transaction, not on a risk statement.** The first thing on screen is the refund trace: ₹1,84,000, clause 7.2, money moved Tuesday, found Friday. The judge sees the graph build, sees clause 7.2 remain UNSUPPORTED, sees the matrix produce two different actuators for two different pending actions on the same response. This takes 90 seconds and establishes that this is an **authorisation system**, not a text-scoring system.

**Within the next 60 seconds**, the knowledge assistant trace shows an entitlement violation caught without any LLM call — a deterministic ACL check on a span whose source excludes the calling principal. The judge now has two data points: (1) the matrix differentiates by blast radius, and (2) the entitlement check is structurally impossible for output-only tools. Both points are established before any explanation of the architecture is needed.

**The third trace** (claims copilot) reinforces the R3 hard gate and the evidence packet, but by this point the differentiation is already established. The demo is front-loaded on the two moments that separate this from every other pitch in the room.

**Backup mitigation:** if the demo environment fails or latency spikes, the team can run the same traces in batch mode with pre-recorded graph states, narrating the matrix decisions. The architecture is the product; the demo is the proof. If the demo breaks, the proof degrades but the architecture does not.

---

*Stage 1 complete. Scope is locked. Prototype boundary is hard. Every assumption is stated. The frozen architecture is preserved without exception. Ready for Stage 2: prototype build.*