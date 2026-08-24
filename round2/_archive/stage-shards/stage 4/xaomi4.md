# Stage 4 — Business Proposal Spine

---

## 1. Problem Framing

### The Category Shift

The cost of a wrong AI output has changed category. It used to be a bad paragraph — embarrassing, reversible, low-stakes. It is now an executed transaction: a refund paid to a fraudster, a salary band leaked to the wrong department, a regulated recommendation acted on without proof, a deletion committed against production data. Enterprises have moved from AI that answers to AI that acts — it refunds, files, sends, books, and writes to production — while oversight tooling is still built for the answering era.

The failure is not that AI is "risky" in the abstract. The failure is specific and structural: **the system was never asked to prove anything.** A refund agent cites clause 7.2 of a vendor agreement. Confidence reads 0.94. Every existing filter passes it. Money moves on Tuesday. The clause does not exist. It is found on Friday.

This is not a hallucination problem in the way the market frames it. It is an **authorisation problem**: an unproven claim was allowed to authorize an irreversible action. The distinction matters because the solution is not better text scoring — it is admission control.

### Why Existing Approaches Fail Against These Failure Modes

| Approach | What It Does | Why It Fails Against the Specific Failure Modes |
|---|---|---|
| **LLM-as-judge** (NeMo Guardrails, most "AI safety" wrappers) | A second model forms an opinion about whether the first was right | The judge asks "does this look right?" — an unfalsifiable question. It produces an opinion using the same reasoning that produced the error, from the same family of blind spots. It cannot state its own error rate. It is too slow to stand in front of an action. It does not know who is asking. |
| **Static guardrails** (LlamaGuard, Lakera, regex/deny-lists) | Match banned surface forms | A fabricated invoice number, a salary leaked from an over-permissioned index, and a correct answer are all lexically clean. Guardrails see none of them. They are identity-blind: the same string is fine for one caller and a breach for another. |
| **Post-hoc observability** (LangSmith, Helicone, Arize, WhyLabs) | Trace, dashboard, weekly review | Beautifully engineered, exactly the wrong product. They tell you what went wrong after a user acted on it. A dashboard can tell you the trace cost ₹8. It cannot tell you that ₹5 of it grounded nothing in the final answer. Observation without execution control is an audit trail, not architecture. |
| **Confidence thresholding** | Gate on logprobs or self-reported certainty | The named failure mode is *confidently* wrong. You cannot detect a calibration failure with the calibration. Confidence 0.94 on a fabricated clause is the problem, not the signal. |
| **RAG groundedness checkers** | Check whether output matches retrieved documents | The closest cousin, structurally short in three ways. They see retrieval only — not tool results, DB rows, computed values, or system context, which is where agents actually get their facts. They average, so one wrong figure drowns in nine correct sentences. And they are action-blind, so 0.82 means the same thing on a draft and on a wire transfer. None of them carry caller identity, so none of them can do entitlement at all. |
| **Composite risk scores** (Azure AI Content Safety, Bedrock Guardrails) | Collapse failure modes into one number | "Trust: 87/100." Three failure modes with three different owners, costs, and remedies, collapsed into one number that maps to no intervention. You cannot block, edit, or escalate on 87. |

**What all six share:** they inspect the output, not the context contract. They score the text rather than verify the claim. They gate on words rather than on actions. And not one of them publishes its own false-negative rate.

### The Enterprise Reality

In practice, enterprises run generative AI across many different use cases at once — customer-facing chatbots, internal copilots for employees, decision-support tools embedded in regulated workflows — and each carries a different risk signature. A one-size-fits-all checking approach fails because:

- **Different risk tolerance and latency budgets.** A customer-facing refund agent and an internal knowledge assistant cannot share the same threshold, the same actuator, or the same fail stance.
- **Bias, hallucination, and privacy risks overlap.** A fabricated detail about a person can simultaneously be a hallucination and a privacy concern. Collapsing these into one classifier is the generic move; separating them by mathematics and owner is the engineering move.
- **No reliable real-time ground truth.** The same knowledge gaps that cause hallucination make automated verification difficult. The system must work without a truth oracle.
- **Over-flagging creates alert fatigue; under-flagging creates liability.** Most systems have to deliberately tune this tradeoff rather than solve it away. A system that blocks everything is a system that gets switched off.
- **Multi-turn agents introduce compounding risk.** One questionable output can shape several downstream decisions. The oversight layer must track provenance across turns, not just score individual responses.
- **Regulatory expectations differ and evolve.** Rigid, hard-coded rules age quickly. The system needs a configurable policy layer with versioning and audit trails.
- **Models are consumed via API.** The enterprise does not own the model. The oversight layer must work at the input/output layer — no weights, no logits, no fine-tuning.

---

## 2. Solution Design Summary

### What ControlPlane Is

ControlPlane.ai is an **admission-control layer** for AI systems. It treats every AI response as a set of **claims requesting permission to act**. It captures the evidence the model was actually given at context-assembly time — with source identity and access rights attached — binds each claim in the output back to a specific span of that evidence, and refuses to let an unproven claim cross into an action.

Verification effort is priced by what the response is about to do: a draft is checked cheaply, a payment is not. Performance, cost, and responsibility stop being three tools and become **three reads of one graph**.

### The Core Mechanism

Everything reads a single structure, assembled while the response is produced:

```
STEP ──produces──▶ SPAN ──binds──▶ CLAIM ──authorizes──▶ ACTION
```

- **STEP** = tool call, retrieval, model turn
- **SPAN** = retrieved chunk, tool row, DB record — with `source_id`, `ACL`, `content_hash`, `offsets`
- **CLAIM** = typed atomic proposition from the output stream
- **ACTION** = pending side effect: tool + args + irreversibility

**Performance** reads the graph forward — does each claim bind to a span? **Cost** reads it backward — did each step produce a span that grounded any accepted claim? **Responsibility** reads the labels — is the caller entitled to every span a claim binds to, and does the action fall inside its typed interlock?

### Five Non-Negotiable Properties

1. **Provenance captured outside the model.** The Provenance Recorder hooks context assembly. The model receives ordinary context and cannot declare, author, or alter its own provenance. This turns verification from a judgment call into a set-membership test.

2. **Default = UNSUPPORTED.** Every check-worthy claim starts unproven. A claim must earn SUPPORTED by binding to a captured span. Unsupported is not "low confidence" — it is unproven. UNKNOWN never collapses into SUPPORTED.

3. **Entitlement is deterministic set-membership.** Caller principal versus source ACL on every span that binds to a claim. Zero LLM in the decision path. This catches the most common real enterprise incident — an over-permissioned RAG index leaking HR data to the wrong employee — and no output-only competitor can replicate it because none of them carry identity into the verification layer.

4. **One graph, blast-radius pricing.** The exact frozen R×S matrix maps verdict severity (what the evidence says) against blast radius (what the response can break) to produce one of four actuators: Block, Edit, Escalate, Pass. The identical verdict annotates a draft and holds a payment. The matrix is a pure function of R and S — no route parameter, no confidence score, no composite number.

5. **Hard gate on actions, not tokens.** Text streams optimistically behind a short hold-back buffer. The hard gate sits on the action/commit boundary. Users perceive speed from text; harm lives in the commit path. The system never makes the model feel slow; it makes the action wait.

### Multi-Route Deployment

The same graph, the same matrix, the same entitlement check governs every enterprise route. What changes is the **route configuration** — which actions exist, how they map to blast-radius tiers, which verification lanes are enabled, and what the fail stance is. Low-consequence traffic does not get weaker truth semantics; it gets less verification budget and a proportionate actuator.

The governance layer is a versioned DAG of deterministic policy rules. Zero LLM reasoning at decision time. Every policy change is validated through shadow replay, canary deployment, and auto-rollback before it affects live traffic. Every decision is written to an append-only, hash-chained audit trail.

### What ControlPlane Refuses to Claim

These four refusals are about the system itself — not about competitors:

1. **"We eliminate hallucinations."** Anyone who has shipped knows this is false. We claim something narrower and much harder to attack: ungrounded claims cannot authorise actions, and we report what we miss.

2. **"Zero integration, drop it in."** We hook context assembly. That is real integration work, and it is the exact reason the design works. The integration cost is the moat.

3. **"Zero added latency."** We never make the model feel slow; we make the action wait. Deterministic checks carry 80–90% of traffic in tens of milliseconds. Expensive binding runs only where blast radius justifies it.

4. **"One accuracy number across failure modes."** Hallucination, leakage, and bias have different mathematics, error costs, and owners. Collapsing them into one score is the generic move.

---

## 3. Target Users & Buyers

### Economic Buyer — The Person Who Signs

**Role:** Chief Information Security Officer (CISO), Chief Risk Officer (CRO), or VP of AI/Data Platform.

**Pain:** The enterprise has deployed or is deploying AI agents that take actions — refunding, filing, sending, writing to production. The economic buyer knows that a single wrong action can cost orders of magnitude more than the AI system saves. They need a control layer that is auditable, measurable, and defensible to regulators and boards — not a dashboard that tells them what went wrong after the fact.

**What convinces them:**
- The published per-route false-negative rate. Every other tool publishes precision (the rate at which it bothers the user). ControlPlane publishes the rate at which it missed. The economic buyer can audit the system by the standard it enforces.
- Dead compute measurement. The exact amount of AI spend that grounded nothing in the final answer. This is the number that justifies the investment to a CFO.
- The audit trail. Every decision is hash-chained, carrying the exact evidence fragment that caused it. An auditor can reconstruct any actuator from the ledger plus the policy version plus the frozen matrix.

### Technical Buyer — The Person Who Evaluates

**Role:** Principal Engineer, Staff Engineer, or AI Platform Lead.

**Pain:** They have tried guardrails and found them wanting. They know that LLM-as-judge is slow, unreliable, and cannot state its own error rate. They know that confidence thresholding fails on the exact failure mode they care about. They need an architecture they can reason about, extend, and defend to their own engineering leadership.

**What convinces them:**
- The architecture is a graph, not a classifier. A serious engineer can trace from action to claim to externally captured span to principal entitlement decision. The mechanisms are trace-independent — span membership, ACL comparison, arithmetic recomputation, and backward attribution are the same operations on any trace.
- The integration surface is honest. One SDK hook at context assembly, plus an OpenAI-compatible reverse proxy. No model access, no weights, no logits, no fine-tuning, no application rewrite. Days, not quarters.
- The system works from day one. Every deterministic mechanism works from the first request. Shadow mode is the default deployment, so the first output is the counterfactual — "would have held N, of which M were true positives" — not a block.

### Day-to-Day User — The Person Who Interacts

**Role:** Customer support agent, internal knowledge worker, claims adjuster, or the AI agent itself (in autonomous mode).

**Pain:** They do not want another alert. They want the system to either let them work or give them a specific, actionable reason why it intervened. Over-flagging creates alert fatigue and pushes users to ignore or bypass warnings.

**What convinces them:**
- R0/R1 traffic — the overwhelming majority of volume — passes with annotation, not blocking. The user sees the annotation and can ignore it without the system preventing them from working.
- When the system does intervene (Edit or Escalate), it ships an evidence packet: the claim, the candidate spans, the verdict, and the diff. Not a bare alert. Not a confidence score. A specific, auditable reason.
- The system does not block their text. The hard gate is on actions. They can still see the model's response while the system evaluates whether the action should proceed.

### Operator — The Person Who Maintains

**Role:** Platform engineer or SRE responsible for the AI infrastructure.

**Pain:** They have been burned by tools that require constant manual tuning, produce opaque failures, and cannot be reasoned about when something goes wrong.

**What convinces them:**
- The policy layer is a versioned DAG with shadow replay, canary deployment, and auto-rollback. No policy change reaches live traffic without validation. Every change can be audited.
- The circuit breaker is SRE-style: per-route error budget, sliding window, automatic autonomy downgrade when the budget is exceeded.
- Fail stance is per blast-radius tier, not a global default. R0/R1 fail open with annotation; R2/R3 fail closed or escalate. The plane is never a single point of failure for the whole product — only for dangerous actions.

---

## 4. Business Case & Impact Logic

### How Value Is Created

ControlPlane creates value through four mechanisms, each traceable to a specific architectural property:

**1. Avoided wrong actions (the primary value driver).**

When an unproven claim would have authorized an irreversible action — a refund, a deletion, a publication, a regulated recommendation — ControlPlane holds the action and escalates with an evidence packet. The value is the cost of the wrong action avoided, minus the cost of the hold and escalation.

The logic: enterprises deploying AI agents that take actions are exposed to a new category of loss that did not exist when AI only generated text. The cost of a single wrong refund, wrong deletion, or wrong regulated recommendation can be orders of magnitude larger than the cost of the AI system. ControlPlane does not claim to eliminate this risk; it claims to make unproven claims unable to authorize actions, and to publish exactly what it misses.

The blast-radius matrix ensures that verification budget is spent where the harm is. R0/R1 traffic — 80–90% of volume — gets cheap deterministic checks. R3 traffic — irreversible actions — gets the full verification pipeline. This is not a tradeoff between safety and speed; it is pricing verification by consequence.

**2. Reduced dead compute (the most defensible number).**

ControlPlane measures dead compute exactly: every step in the agent's execution that grounded zero accepted claims in the final answer, found by walking the graph backward. No model, no estimation.

The logic: a dashboard can tell you the trace cost ₹8. It cannot tell you that ₹5 of it grounded nothing in the final answer. Walking the backward graph can — because the graph that verifies is the graph that accounts. This is the number a buyer signs a cheque against, because it names the exact spend that produced no value.

No competitor has this number, because no competitor has the graph. Observability tools measure spend; ControlPlane measures waste.

**3. Reduced alert fatigue (the adoption enabler).**

The blast-radius matrix is deliberately graduated. R0/R1 traffic with unsupported hedged claims gets Pass + annotate — not Escalate. The system monitors its own noise level per route: if the ratio of flagged/escalated decisions to total decisions exceeds a configurable ceiling, the route is flagged for threshold recalibration.

The logic: every guardrail that has been deployed and then switched off failed because of over-blocking. The matrix exists specifically to prevent this. R0/R1 traffic — the overwhelming majority — passes with annotation. Enforcement is earned per route through shadow evidence, so nobody is asked to trust the system before it has produced its own counterfactual.

**4. Auditability and regulatory defensibility (the compliance value).**

Every decision is written to an append-only, hash-chained ledger carrying the exact evidence fragment that caused it. An auditor can reconstruct any actuator from the ledger plus the policy version plus the frozen matrix. The per-route FNR schema is published as a typed format — with nulls where ground truth is insufficient.

The logic: regulatory expectations differ by geography and industry, and continue to evolve. A rigid, hard-coded compliance layer ages quickly. ControlPlane's versioned policy DAG with additive regulatory overlays provides a configurable, auditable foundation that can adapt without forking the architecture. The published FNR format gives regulators something no other tool provides: the system's own assessment of what it missed.

### What ControlPlane Does Not Claim to Measure (Yet)

- Production-scale FNR values. These require stratified shadow audit over real traffic with human adjudication. The schema is published; the values are earned.
- Net cost savings. Dead compute names the waste; the net depends on the enterprise's traffic, model costs, and verification overhead. ControlPlane does not put a savings percentage on a slide because it has not measured it on their traffic.
- Bias elimination. Bias is measured as a distributional property — counterfactual flip rate with a confidence interval over a rolling window — not as a per-response verdict. The measurement is described in the enterprise solution; it is not a live prototype actuator.

---

## 5. Phased Roadmap

### Phase 0 — Prototype (Current — Round 2)

**What exists:** A working proof-of-concept demonstrating the admission primitive on exactly two routes — Customer Support Refund Agent (R1+R3 dual-action) and Internal Knowledge Assistant (R0/R1 entitlement flip) — on one `STEP → SPAN → CLAIM → ACTION` Evidence Ledger.

**What is proven:**
- Provenance captured outside the model before claims are judged
- Default = UNSUPPORTED enforced; claims must earn proof
- Deterministic entitlement as set-membership (zero LLM)
- Exact frozen R×S matrix producing different actuators for different pending actions on the same response
- Hard gate on actions; mock refund does not commit when Escalate is in force
- Evidence-packet escalation; surgical edit
- Published FNR as empty typed schema (the credibility play)

**What is not claimed:** Production throughput, real regulatory compliance, populated FNR values, live bias measurement.

**Enforcement posture:** Shadow mode only. The prototype demonstrates the mechanism; it does not claim that any production route has earned enforcement.

---

### Phase 1 — First Production Routes (Months 1–3)

**What is earned:** Production deployment on 2–3 high-value routes in shadow mode, then canary, then enforcement — earned per route through counterfactual evidence.

**Routes:**
- Customer support refund agent (highest blast radius, most visible failure mode)
- Internal knowledge assistant (highest volume, entitlement leakage risk)
- One additional route selected by the enterprise (decision-support, document generation, or regulated workflow)

**What happens:**
1. **Integration.** SDK hook at context assembly + OpenAI-compatible reverse proxy. The enterprise's existing retrieval stack already provides source IDs; the integration adds ACLs and content hashes. Estimated: days to weeks, not quarters.
2. **Shadow deployment.** All three routes run in shadow mode. Every response is verified; no actions are gated. The output is the counterfactual: "would have held N, of which M were true positives." This is the evidence that earns enforcement.
3. **Canary enforcement.** Routes that produce sufficient shadow evidence (configurable threshold) are promoted to canary: a bounded slice of traffic is gated. The canary runs for a configurable window. If the human-override rate exceeds 3× baseline, the canary auto-rolls back.
4. **Production enforcement.** Routes that pass canary are promoted to full enforcement. The hard gate is live. The per-route FNR schema begins accumulating measured values from the stratified shadow audit.

**What is measured:**
- Per-route FNR (from shadow audit, initially with wide confidence intervals that narrow over time)
- Dead compute (exact, from the backward graph walk)
- Override rate and reason codes
- Entitlement violation rate by source (the operational detector for over-permissioned indexes)
- Latency by lane (p50/p95 per route)

**What is earned, not switched on:**
- Enforcement is earned per route through shadow evidence. No route goes from zero to enforcement without producing its own counterfactual.
- Policy changes are validated through shadow replay and canary before reaching live traffic.
- The FNR schema accumulates measured values as the shadow audit produces ground truth. Nulls are replaced with measured values only when sufficient sample size and adjudication are available.

---

### Phase 2 — Enterprise Rollout (Months 4–9)

**What is earned:** Broader deployment across the enterprise's AI portfolio, with per-route configuration, governance, and measurement infrastructure matured from Phase 1.

**What happens:**
1. **Additional routes.** Decision-support tools, document generation copilots, regulated workflow assistants. Each route gets its own configuration object: action grammar, R-tier mapping, verification profile, fail stance, enforcement mode.
2. **Governance maturation.** The versioned policy DAG is operational. Regulatory overlays for applicable jurisdictions (e.g., DPDPA 2023, GDPR, sector-specific rules) are configured as additive layers. The policy-change lifecycle (draft → validation → shadow replay → canary → approval → promote) is the standard operating procedure.
3. **Feedback loops operational.** Human overrides with structured reason codes feed threshold calibration. Escalation adjudication (confirmed / false positive / source error / ACL gap) feeds source governance and policy review. The system learns calibrations, not models.
4. **Metrics and reporting.** The sceptical-stakeholder surface is operational: per-route FNR with confidence intervals, dead compute, override rates, entitlement violation rates, latency by lane. The FNR schema is populated with measured values where ground truth is available; nulls remain where it is not.

**What is earned, not switched on:**
- Each new route earns enforcement through its own shadow → canary → enforce lifecycle.
- Regulatory overlays are additive; they cannot loosen the frozen invariants.
- The feedback loop proposes policy versions; it does not silently alter live enforcement.

---

### Phase 3 — Platform (Months 9–18)

**What is earned:** ControlPlane as a platform capability — not a per-application tool, but an infrastructure layer that every AI route in the enterprise passes through.

**What happens:**
1. **Multi-tenant deployment.** Per-tenant isolation, per-tenant policy configuration, per-tenant FNR reporting.
2. **Connector ecosystem.** Standard connectors for common retrieval stacks, vector databases, IAM systems, and action executors. The integration cost decreases as the connector library grows, but the architecture never claims "zero integration" — the integration cost is the moat.
3. **Async bias measurement operational.** For decision-shaped routes, the counterfactual flip-rate measurement is running in Lane 3. Routes where the confidence interval excludes zero are flagged for policy review. Bias is never a per-response verdict; it is a distributional measurement that informs governance.
4. **Cost optimisation.** Dead compute measurement drives retrieval and tool-call optimisation. The backward graph walk identifies exactly which steps grounded nothing, enabling targeted cost reduction without guessing.

**What remains true at every phase:**
- Default = UNSUPPORTED on every route.
- Entitlement is deterministic set-membership, zero LLM.
- The matrix is the same 16-cell table on every route.
- The hard gate is on actions, not tokens.
- The FNR is published as a format — measured where possible, null where not.
- Enforcement is earned per route, never globally switched on.

---

## 6. Key Risks & Mitigations

### Risk 1 — False Assurance on Derived Claims

**The risk.** Multi-hop, aggregated, and synthesised claims are where entailment is weakest. If the binding engine marks a subtly-wrong synthesised claim SUPPORTED because a shallow span looks similar, ControlPlane delivers false assurance — strictly worse than no control plane, because humans stop checking.

**The mitigation (three lines, from Architecture §7):**
1. Derived claims bypass ordinary NLI. Arithmetic or aggregative claims are recomputed from spans. Claims neither recomputable nor directly entailed return UNKNOWN. UNKNOWN never collapses into SUPPORTED — that one rule is the boundary between a control plane and false assurance.
2. Verifiers are decorrelated from the generator by construction. Different model families. Deterministic checks carry the majority of enforcement weight precisely because they cannot share the generator's failure modes.
3. The plane publishes its own error bars. Stratified shadow audit — 100% of blocks and escalations plus a random slice of passes — sampled to expensive ground truth. The per-route FNR schema is the published format.

**The honest boundary:** the claim is never "we catch hallucinations." It has the shape: "On this route we catch X% of ungrounded claims at 40ms p50 — and here is the Y% we don't."

---

### Risk 2 — Over-Permissioned Source Indices Undermining Entitlement

**The risk.** ControlPlane enforces the ACLs carried by the source system. If the source system's ACLs are wrong — over-permissioned — ControlPlane faithfully enforces a wrong policy. The system does not fix IAM; it makes violations visible.

**The mitigation:**
1. Every entitlement decision is logged against a named principal and a named source. The audit trail makes over-permissioning forensic.
2. The entitlement violation rate per source is the operational detector. A high violation rate on a specific source is exactly what an over-permissioned index looks like from the inside. The system does not need to audit the index; it audits the decisions.
3. Missing ACLs are treated as unentitled on privileged routes. The system defaults to the safer assumption.

**The honest boundary:** we enforce the access rights the source system already carries. We do not invent them. We stop them being silently bypassed by a model.

---

### Risk 3 — Alert Fatigue Leading to Abandonment

**The risk.** If the UNSUPPORTED default and the claim extractor are too aggressive on high-volume, low-risk routes, the system escalates or annotates too many responses. Users ignore or bypass warnings. The team switches the system off — the fate of every guardrail.

**The mitigation:**
1. The matrix is deliberately graduated. R0/R1 traffic with unsupported hedged claims gets Pass + annotate — not Escalate. The matrix exists specifically to prevent over-blocking.
2. Check-worthiness filtering removes the largest false-positive class before any model call. Trivially true claims, boilerplate, and hedged filler are filtered before binding runs.
3. The system monitors its own noise level per route. If the ratio of flagged/escalated decisions to total decisions exceeds a configurable ceiling, the route is flagged for threshold recalibration.
4. Shadow mode is the default. Enforcement is earned through shadow evidence. Nobody is asked to trust the system before it has produced its own counterfactual.
5. R0/R1 traffic passes with annotation, not blocking. The user can ignore the annotation without the system preventing them from working. This is the design choice that prevents the team from switching it off.

---

### Risk 4 — Prompt Injection / Source Poisoning

**The risk.** An attacker manipulates the model's output through prompt injection, or poisons a source document so that a genuine span supports a false claim.

**The mitigation:**
1. The binding is computed by ControlPlane, not asserted by the model. The model has no channel to declare a binding. An injection can change what the model says; it cannot change which spans were captured at context assembly, nor the entailment verdict, nor the ACL.
2. Source poisoning is a supply-chain attack on the corpus, not on the plane. The source ID and content hash on every span make it forensically traceable. The system defends the claim-to-evidence link; it does not claim to defend the truth of the evidence.

**The honest boundary, stated out loud:** we defend the claim-to-evidence link, not the truth of the evidence.

---

### Risk 5 — Integration Effort Exceeds Expectations

**The risk.** The enterprise discovers that hooking context assembly is harder than expected — the retrieval stack does not expose source IDs cleanly, the ACL metadata is scattered across systems, or the action executor needs modification.

**The mitigation:**
1. The integration surface is honest from day one. One SDK hook at context assembly, plus an OpenAI-compatible reverse proxy. No model access, no weights, no logits, no fine-tuning, no application rewrite.
2. If the enterprise is on a standard retrieval stack, the retriever already knows the source ID. The integration adds the access rights and a hash. This is real work, and we say so — because a team that discovers the integration cost after being sold "drop-in" churns.
3. Shadow mode means the system produces value from the first request — the counterfactual — even before enforcement. The enterprise sees what the system would have held, which is the evidence that justifies the integration investment.

---

### Risk 6 — Regulatory Expectations Outpace the Policy Layer

**The risk.** New AI-specific regulation emerges that the current policy DAG does not anticipate. The system becomes non-compliant.

**The mitigation:**
1. The policy layer is a versioned DAG with additive regulatory overlays. New regulation is implemented as a new overlay — it adds constraints, it does not rewrite the base policy.
2. The governance hierarchy narrows only: enterprise baseline → geography overlay → tenant → route → action class. Overlays may only add constraints; they cannot loosen frozen invariants.
3. The audit trail carries the exact policy version that governed every decision. An auditor can reconstruct the decision context for any historical actuator, regardless of subsequent policy changes.

---

## 7. Differentiation Anchor

Five points that separate ControlPlane from every competitor in the room. Each is traceable to a specific architectural property that no output-only tool can replicate.

### 1. Provenance Outside the Model — The Set-Membership Test

Every other tool inspects what the model said. ControlPlane inspects the evidence the model was given — captured at context assembly, outside the model, with source identity and access rights attached. Verification is a set-membership test against a known evidence set, not a judgment call about finished text.

The load-bearing phrase: **set-membership test.** It is what makes the insight concrete for a technical judge. A binding either exists or it does not. There is no score, no threshold, no opinion.

### 2. Entitlement as Deterministic Authorization — Identity in the Verification Layer

No output-only tool carries caller identity into the verification layer. ControlPlane does. The same semantic claim produces different outcomes for different principals — not because of a classifier, but because of a deterministic ACL lookup. Zero LLM. Sub-millisecond. Structurally impossible for any tool that only sees the output text.

This catches the most common real enterprise incident: an over-permissioned RAG index faithfully leaking data to the wrong employee. Every LLM-as-judge wrapper misses it because none of them know who is asking.

### 3. Blast-Radius Pricing — Proof Scales with Consequence

Every other tool applies one threshold to all traffic. ControlPlane prices verification by what the response is about to do. The identical verdict annotates a draft and holds a payment. R0/R1 traffic — 80–90% of volume — gets cheap deterministic checks. R3 traffic — irreversible actions — gets the full pipeline.

This is not a tradeoff between safety and speed. It is the architectural answer to the one-size-fits-all problem: the matrix is one-size-fits-all; the R-tier assignment is per-route.

### 4. Published Own False-Negative Rate — The Credibility Move

Every other tool publishes precision — the rate at which it bothers the user. ControlPlane publishes the rate at which it missed. Per route. With confidence intervals. Where trustworthy ground truth does not exist, the field stays null — not fabricated.

The plane is audited by the standard it enforces. This is the line that wins the room: "We publish our own miss rate. Per route. Not what we caught — what we missed."

### 5. One Graph, Three Reads — Not Three Tools Bolted Together

Performance, cost, and responsibility are not three separate products. They are three reads of one `STEP → SPAN → CLAIM → ACTION` graph. The same structure that verifies a claim also prices the waste and checks the entitlement. Everywhere else, that is three products. Here, it is three questions on one graph.

The backward graph walk — identifying exactly which steps grounded nothing in the accepted answer — is the most defensible number in the proposal. No competitor has it, because no competitor has the graph.

---

## 8. Fidelity Self-Check

| Frozen Invariant | Status in This Proposal |
|---|---|
| **Default = UNSUPPORTED** | Untouched. §2: "Every check-worthy claim starts unproven. A claim must earn SUPPORTED by binding to a captured span." §5: "Default = UNSUPPORTED on every route" at every phase. |
| **Entitlement / ACL check** | Untouched. §2: "Deterministic set-membership. Zero LLM in the decision path." §7: "Structurally impossible for any tool that only sees the output text." |
| **Exact R×S matrix** | Untouched. §2: "The exact frozen R×S matrix maps verdict severity against blast radius." §5: "The matrix is the same 16-cell table on every route." No matrix is redrawn anywhere in the proposal. |
| **Hard gate on actions, not tokens** | Untouched. §2: "The hard gate sits on the action/commit boundary." §4: "The system never makes the model feel slow; it makes the action wait." |
| **Published FNR as a format** | Untouched. §2: "Published FNR as empty typed schema." §4: "The per-route FNR schema is published as a typed format — with nulls where ground truth is insufficient." §5: "Nulls are replaced with measured values only when sufficient sample size and adjudication are available." |
| **Two-pending-actions resolution** | Untouched. §2: "The identical verdict annotates a draft and holds a payment." §7: "The identical verdict annotates a draft and holds a payment." The proposal references the dual-action throughout without collapsing it. |
| **No LLM-as-judge on critical path** | Untouched. §1: LLM-as-judge is listed as a failing approach. §2: "Zero LLM reasoning at decision time." §7: Entitlement is "Zero LLM. Sub-millisecond." |
| **No per-response bias verdict** | Untouched. §2: "Bias is measured as a distributional property — counterfactual flip rate with a confidence interval over a rolling window — not as a per-response verdict." §5 Phase 3: "Bias is never a per-response verdict; it is a distributional measurement that informs governance." |
| **No composite risk/confidence score** | Untouched. §1: Composite risk scores listed as failing. §2: "No route parameter, no confidence score, no composite number." §7: "There is no score, no threshold, no opinion." |
| **UNKNOWN never → SUPPORTED** | Untouched. §2: "UNKNOWN never collapses into SUPPORTED." §6 Risk 1: "UNKNOWN never collapses into SUPPORTED — that one rule is the boundary between a control plane and false assurance." |
| **Refuse-to-claim list** | Untouched. §2: Four explicit refusals about the system itself. §4: "What ControlPlane Does Not Claim to Measure (Yet)." |
| **Content laws** | Untouched. §1: "Money moves on Tuesday. The clause does not exist. It is found on Friday." The proposal never says the refund is "blocked." It never says clause 7.2 "caps" or "denies" anything. |

**No competing mechanism enters the proposal.** LLM-as-judge, confidence thresholding, composite risk scores, open-web verification, per-response bias classifiers, and redrawn matrices are all absent or explicitly rejected. The proposal adds business framing, impact logic, roadmap, and risk analysis around the frozen architecture — not new mechanisms.

**The proposal makes the frozen architecture feel inevitable, not optional.** The problem framing establishes that the cost category has changed. The existing approaches are shown to fail against the specific failure modes. The solution design is the only architecture that addresses the problem as stated: provenance outside the model, inverted burden of proof, entitlement as set-membership, blast-radius pricing, hard gate on actions. The business case is built on defensible impact logic — avoided wrong actions, exact dead compute, reduced alert fatigue, auditability — not on fabricated ROI percentages. The roadmap earns enforcement per route through shadow evidence, never switches it on globally.

---

*Stage 4 complete. The business proposal spine is built on the frozen architecture without softening, reopening, or inventing. Every claim is traceable to a specific architectural property. Every risk has a precise mitigation drawn from the frozen sources. The proposal makes the architecture feel inevitable — because the problem demands it.*