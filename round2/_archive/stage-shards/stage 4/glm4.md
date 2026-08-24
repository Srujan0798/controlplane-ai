# ControlPlane.ai — Stage 4: Business Proposal Spine (Frozen)

> Accenture Innovation Challenge 2026 · Round 2 · Stage 4  
> Sources of truth (absolute): `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` · `R2S2.md` · `R2S3.md`  
> Status: **FROZEN** — Stages 1–3 non-negotiable. This document renders the frozen architecture into business-proposal form without softening any invariant.

---

## 1. Problem Framing

The cost of a wrong AI output has changed category. It used to be a bad paragraph — a customer saw an incorrect sentence, a report carried a fabricated figure, and the damage ended there. It is now an executed transaction — a refund is issued, a payment is authorised, a record is deleted, regulated advice is delivered to a patient. The failure mode is identical in both cases: the model asserted something it could not prove. But the consequence has moved from *misinformation* to *unauthorised action*, and the tooling has not moved with it.

Existing approaches fail against this shift for three structural reasons, not implementation gaps:

**First, they inspect the output, not the context contract.** Every major oversight tool — LLM-as-judge wrappers, groundedness checkers, content-safety classifiers — examines what the model *said* and forms an opinion about it. None of them record what the model was *given*. That record is thrown away the moment generation starts. Without it, verification becomes a judgment call: *does this look right?* With it, verification becomes a set-membership test: *which span proves this claim?* The first question is unfalsifiable; the second has an answer.

**Second, they score the response, not the action.** A groundedness checker produces a single number — 0.82, 0.91 — that means the same thing on an internal draft and on a wire transfer. Guardrails apply one threshold to all traffic. Neither mechanism prices verification by what the response is about to do. The result is a binary tradeoff: tighten the threshold and you over-block low-consequence traffic (alert fatigue, bypass); loosen it and you under-protect high-consequence actions (the ₹1,84,000 refund that moves because nine correct sentences drowned one absent clause).

**Third, they are identity-blind.** The most common real enterprise AI incident is not a fabrication — it is a correct answer delivered to the wrong person. An over-permissioned RAG index faithfully returns HR compensation data, the model states it accurately, and a non-HR employee reads it. No output-only inspector can catch this, because none of them carry the caller's identity into the verification layer. The failure is not in the text; it is in the authorisation — and it is deterministic, not probabilistic.

The problem is not "AI risk." It is that enterprises have moved from AI that answers to AI that acts, while oversight is still built for the answering era.

---

## 2. Solution Design Summary

ControlPlane is an admission-control layer that sits between an AI system and the actions it requests permission to perform. It treats every AI response as a set of *claims requesting permission to act* — not text to be scored.

**The primitive:** At context-assembly time, before the model runs, a Provenance Recorder captures every piece of evidence the model will receive — retrieved chunks, tool results, database rows — as typed spans carrying `source_id`, access-control list, content hash, and byte offsets. This record is assembled *outside the model*, where the model cannot author, alter, or fabricate it. During generation, check-worthy claims are extracted and each is born **UNSUPPORTED** — the burden of proof is inverted. A claim earns `SUPPORTED` only by binding to a specific captured span via deterministic recomputation (for numbers, dates, identifiers) or entailment (for textual claims, against the provenance set only — never the open web). Claims that cannot bind stay `UNSUPPORTED`; derived or multi-hop claims that cannot be recomputed return `UNKNOWN`, and `UNKNOWN` never collapses into `SUPPORTED`.

**The graph:** Performance (is this claim proven?), cost (did this step produce anything useful?), and responsibility (is this caller entitled to this proof?) are not three detectors — they are three reads of one structure: `STEP → SPAN → CLAIM → ACTION`. One graph. Three axes. Three actuators.

**The decision:** Every pending action is assigned a blast-radius tier `R` (from R0 = internal draft to R3 = irreversible or regulated). The Action Interlock — a pure rule engine, zero LLM at decision time — applies the exact R×S matrix: the identical verdict produces four different actuators depending on what the response is about to do. **Proof scales with consequence.**

**The gate:** The hard gate sits on *actions*, not tokens. Customer-visible text streams behind a short hold-back buffer (~150–300 ms) and may be surgically edited. A tool call — a refund, a payment, a deletion — does not commit until the interlock decides. The same response can simultaneously produce an `Edit` on the text path and an `Escalate` on the action path, because each pending action is evaluated independently against the worst claim that feeds it.

**Entitlement** is a deterministic set-membership test — caller clearance versus source ACL — in Lane 1, with zero LLM, and cannot be disabled. It is the mechanism that catches the most common real enterprise incident (correct answer, wrong person) and is structurally impossible for any output-only competitor to replicate.

**Deployment** is an OpenAI-compatible reverse proxy plus a thin context-assembly SDK hook. No model access, no weights, no logits, no fine-tuning, no application rewrite.

---

## 3. Target Users & Buyers

### Who feels the pain most acutely

The head of AI/ML platform engineering or AI governance at a large enterprise that has moved — or is moving — from read-only copilots to agentic systems that execute transactions: issue refunds, book shipments, send external communications, write to production databases. They have already had at least one incident where an AI system took an action it should not have, or they are one deployment away from it. They have tried LLM-as-judge wrappers or groundedness checkers and found them either too slow to stand in front of an action, too coarse to price by consequence, or too identity-blind to catch authorisation failures.

### Economic buyer

**Chief Information Security Officer (CISO) or Chief Risk Officer (CRO)** — or, in regulated industries, the Chief Compliance Officer. They sign because the cost category has changed: a wrong paragraph is a support ticket; a wrong transaction is a financial loss, a regulatory breach, or a litigation event. They are buying *action authorisation*, not "AI safety." The contract language they respond to is: *an unproven claim cannot authorise an action.* They do not respond to: *we detect 95% of hallucinations.*

### Technical buyer

**Head of AI Platform / ML Engineering** — the person who owns the retrieval stack, the agent framework, and the model API contracts. They evaluate whether the Provenance Recorder hook is feasible in their context-assembly path, whether the proxy deployment model works with their existing providers, and whether the system can operate without model weights or logits. They also evaluate the hardest technical question: *does this actually catch what our current stack misses?* — which is where the entitlement check and the dual-action resolution become the proof points.

### Day-to-day operator

**AI operations engineer / SRE** — configures route policies, monitors per-route FNR and override rates, responds to escalation evidence packets, and manages policy-version lifecycles (shadow → canary → enforce → rollback). They interact with the system through typed policy objects and ledger-backed metrics, not through free-text prompts or subjective ratings.

---

## 4. Business Case & Impact Logic

Value is created through four mechanisms, each with a defensible causal chain. No composite ROI percentage is offered, because the numbers depend on the enterprise's traffic mix and action distribution — and a fabricated percentage is a liability the first time a buyer tests it.

### 4.1 Avoided wrong actions

The highest-value mechanism, but the hardest to quantify without the buyer's incident history. The logic: if an irreversible action (R3) requires every claim feeding it to carry a supported binding, and the default is `UNSUPPORTED`, then a claim with no evidence *cannot* authorise that action — it is held and escalated with the evidence packet. The ₹1,84,000 refund under clause 7.2 (which does not exist) is the canonical case: confidence was 0.94, every surface filter passed it, money moved Tuesday, found Friday. ControlPlane holds it because the claim has no span — not because it scored low, but because it has no proof. The directional impact: every R3 action that would have proceeded on an unproven claim is a prevented loss. The buyer supplies the loss magnitude; the system supplies the prevention mechanism.

### 4.2 Reduced dead compute

This is the most defensible number, because it is computed *exactly*, not estimated. The Evidence Ledger records every step (retrieval call, tool invocation, model turn) and every claim it grounded. Walking the graph backward: any step that grounded zero accepted claims is dead compute. A dashboard can tell you a trace cost ₹8; walking the graph tells you that ₹5 of it grounded nothing in the final answer. No competitor has this number, because no competitor has the graph. The impact logic: dead compute is spend that produced no value — and it is measurable from day one, before any shadow calibration, because it requires no ground truth, only the ledger.

### 4.3 Reduced alert fatigue

Alert fatigue is what causes teams to disable oversight layers. ControlPlane addresses it structurally, not by tuning a threshold: (a) R0/R1 traffic — 80–90% of volume — passes with annotation, not with a block; the hard gate is on actions, not tokens, so the majority of traffic is never interrupted. (b) The matrix prices the actuator by blast radius, so a draft gets `Pass + annotate` where a payment gets `Escalate` — the same verdict, different consequence, different friction. (c) Enforcement is earned per route through shadow evidence before it is switched on, so nobody is asked to trust the system before it has produced its own counterfactual. The impact logic: a system that does not over-block low-consequence traffic is a system that does not get disabled in quarter two.

### 4.4 Auditability

Every decision writes to an append-only, hash-chained ledger carrying the exact evidence fragment, the claim, the verdict, the matrix cell, the actuator, the policy version, and the principal. An auditor can reconstruct any action authorisation or denial from the ledger + the frozen matrix + the policy version that was live at the time. This is not a dashboard — it is a forensic trail. The impact logic: in regulated industries, the ability to prove *why* an action was held — with the specific missing span, not a "risk score of 23" — is the difference between a satisfactory audit and a findings letter.

---

## 5. Phased Roadmap

Each phase states what is *earned*, not what is switched on. Enforcement is never gifted; it is earned through shadow evidence.

### Phase 0 — Prototype (current)

**What exists:** Two live routes on one `STEP → SPAN → CLAIM → ACTION` Evidence Ledger — a customer-support refund agent (R1 + R3 dual-action) and an internal knowledge assistant (R0/R1 entitlement flip). The refund dual-action is the centrepiece: the same response simultaneously produces R1 × entitlement → **Edit** on the customer-visible text and R3 × unsupported-categorical → **Escalate** on the refund, which is held with the evidence packet and does not commit.

**What is proved:** The admission primitive. An unproven claim cannot authorise an action. Provenance captured outside the model, entitlement as deterministic set-membership, the frozen matrix pricing outcome by blast radius per pending action.

**What is not claimed:** Production scale, production FNR values, multi-tenant high-availability, live bias measurement.

### Phase 1 — Shadow deployment on 2–3 production routes

**What is deployed:** The Provenance Recorder hook is integrated into the enterprise's context-assembly path for 2–3 real routes (e.g., customer support, internal knowledge, one decision-support route). ControlPlane runs in **shadow mode**: every request produces both the ungated disposition and the gated disposition. No action is actually held or edited.

**What is earned:** The counterfactual. *On this route, the plane would have held N actions, of which M were confirmed true positives by human adjudication.* This is the evidence that justifies moving from shadow to canary. Per-route FNR schema is populated with `prototype_corpus` or `insufficient_sample` status — never fabricated production numbers.

**What is also earned:** Dead-compute measurements on real traffic. The exact spend that grounded nothing, route by route. This number requires no ground truth and is available from the first shadow trace.

**Duration:** Weeks, not months. Deterministic mechanisms (span membership, entitlement, arithmetic, typed interlocks) work from the first request. Only statistical signals (route cost baselines, counterfactual bias replay) need accumulation windows.

### Phase 2 — Canary enforcement on highest-R routes

**What changes:** On routes where shadow evidence shows acceptable false-positive rates and where the action blast radius justifies it (R2/R3 routes — payments, deletions, external sends), the interlock is switched from shadow to **canary**: a bounded percentage of traffic is actually gated. The remainder continues in shadow for ongoing comparison.

**What is earned:** Live enforcement evidence. *On this route, in canary mode, the plane held X actions; human override rate was Y; zero false negatives were confirmed in the adjudicated sample.* Auto-rollback triggers if override rate exceeds 3× baseline.

**What is also earned:** Policy-version lifecycle discipline. Every threshold or R-mapping change goes through shadow replay over the last N traces, canary on a bounded slice, and named-principal approval before promotion. The organisation learns to operate the governance layer, not just install the software.

### Phase 3 — Broad enterprise rollout

**What changes:** Enforcement is promoted route by route as each earns its canary evidence. Additional route packs are configured (new action grammars, new R mappings, additive geography/industry overlays). The bias measurement program — async route-level counterfactual flip-rate with confidence intervals — operates continuously on decision-shaped routes. The FNR schema begins to show `production_measured` status on mature routes.

**What is earned:** An operating control plane, not a installed tool. The organisation has per-route enforcement evidence, per-route FNR with confidence intervals, dead-compute baselines, entitlement-violation rates by source (which are also the operational detector for over-permissioned indexes), and a policy-version audit trail that can survive regulatory examination.

**What remains honestly bounded:** The system does not claim to eliminate hallucinations, bias, or privacy risk. It claims that unproven claims cannot authorise actions, and it publishes per-route what it misses.

---

## 6. Key Risks & Mitigations

### Risk 1 — False assurance on derived and multi-hop claims

**What it is:** A synthesised or aggregated claim is marked `SUPPORTED` because a shallow span looks similar via entailment, but the actual derivation is wrong. This is strictly worse than no control plane, because humans stop checking what the plane has stamped as verified. The architecture names this as the single strongest residual technical risk.

**Exact mitigation from the freeze:**
- Derived, aggregative, and multi-hop claims are **routed away from NLI entirely**. Arithmetic or aggregative claims are recomputed from spans. Claims that are neither recomputable nor directly entailed return `UNKNOWN`.
- `UNKNOWN` **never** collapses into `SUPPORTED`. That one rule is the boundary between a control plane and false assurance.
- Verifiers are from a different model family than the generator, so they cannot share the generator's failure modes.
- The FNR schema is stratified by claim type. An unexpected `SUPPORTED` rate in the derived stratum triggers a review — the plane audits its own assurance boundary.
- The published claim shape is never *"we catch hallucinations"* — it is *"on this route we catch X% of ungrounded claims, and here is the Y% we don't."*

### Risk 2 — Poisoned or incorrect source evidence

**What it is:** A source document in the corpus contains false information. The model retrieves it, ControlPlane binds the claim to the span, and the claim is marked `SUPPORTED` — but the evidence itself is wrong. The plane proves the claim-to-evidence link; it does not prove the evidence is true.

**Exact mitigation from the freeze:**
- Every accepted binding carries an immutable `source_id` and `content_hash`. If a source is discovered to be poisoned, every claim ever bound to it is forensically traceable.
- Entitlement-violation rate **per source** is reported to source owners — this is the operational detector for over-permissioned or degraded indexes, not a silent "AI remediation" claim.
- Sources can be quarantined or de-ranked via policy version without altering the control plane's logic.
- The honest boundary, stated to the buyer: *we defend the claim-to-evidence link, not the truth of the evidence.* A supply-chain attack on the corpus is outside the plane's truth guarantee — but the source ID and hash make it forensically traceable in a way that an output-only scorer cannot.

### Risk 3 — Over-permissioned upstream indexes

**What it is:** The RAG index itself grants access to documents the caller should not see. ControlPlane enforces the ACLs the source system carries — it does not invent them. If the index is over-permissioned, the plane will faithfully enforce a wrong policy.

**Exact mitigation from the freeze:**
- The entitlement check makes the failure *visible*: every decision logs the principal, the span, the ACL, and the verdict. An over-permissioned index shows up as a stream of entitlement violations by source — a measurable signal that the upstream IAM has a gap.
- The plane does not claim to fix enterprise IAM. It claims to stop IAM gaps being silently bypassed by a model — which is the actual incident pattern. The distinction is critical in buyer conversations.

### Risk 4 — Operational bypass and alert fatigue

**What it is:** The team disables the plane because it over-blocks, or an attacker induces load to trigger a universal fail-open and bypass the gate.

**Exact mitigation from the freeze:**
- R0/R1 traffic — 80–90% of volume — passes with annotation. The hard gate is on actions, not tokens. Over-blocking is structurally limited because most traffic is never interrupted.
- Fail stance is declared **per blast-radius tier**, not globally. R0/R1 fail open with annotation; R2/R3 fail **closed or escalate**. A universal fail-open — which makes the plane bypassable under load — is architecturally forbidden.
- Enforcement is earned per route through shadow evidence before it is switched on. Nobody is asked to trust the plane before it has produced its own counterfactual.
- Auto-rollback if human-override rate exceeds 3× baseline. Circuit breakers downgrade autonomy rather than blocking all traffic.

### Risk 5 — Integration friction

**What it is:** The Provenance Recorder hook requires changes to the context-assembly path. This is real work, and misrepresenting it as "zero integration" causes churn when the buyer discovers the cost.

**Exact mitigation from the freeze:**
- The integration is honestly scoped: one SDK hook where context is already assembled, plus an OpenAI-compatible reverse proxy. If the enterprise is on a standard retrieval stack, the retriever already knows the source ID — the hook adds access rights and a hash.
- The integration cost is stated as a strength, not a weakness: *the integration cost is the moat*, because it is the reason the provenance record exists outside the model, which is the reason entitlement is possible, which is the thing no output-only competitor can replicate.
- Day-one mechanisms that work without any history: span membership, entitlement, arithmetic recomputation, typed interlocks. Only statistical signals need accumulation.

### Risk 6 — Adoption — "another guardrail that gets switched off in a quarter"

**What it is:** The buyer's organisation has installed and disabled three oversight layers in the last two years. Why is this different?

**Exact mitigation from the freeze:**
- It does not block their text. The hard gate is on actions. R0/R1 passes with annotation. The thing their users see — the text — is not interrupted.
- Enforcement is earned, not declared. Shadow mode produces the counterfactual before any action is actually held. The organisation sees the evidence before it accepts the friction.
- The evidence packet ships proof, not an alert. When an action is held, the packet contains the claim, the candidate spans (or their absence), the verdict, and the diff. A human reviewer can see *exactly* why the action was held — not a "risk score of 73" but "clause 7.2 has no span."
- Override rates and reason codes are tracked. If the plane is wrong, the data shows it — and the auto-rollback mechanism acts on it.

---

## 7. Differentiation Anchor

Five sharpest points, each tied to a structural property of the frozen architecture, each naming the specific competitor category it defeats:

**1. Provenance outside the model vs. model-emitted citations.**
NeMo Guardrails and most LLM-as-judge wrappers accept the model's own trace — including self-reported "sources" — as evidence. A model that fabricates a fact fabricates the citation with equal fluency. ControlPlane captures provenance at context-assembly time, outside the model, where the model cannot author or alter it. This is not a better detector — it is a different evidence source. Without it, entitlement checking is impossible, because the model cannot carry the caller's identity into a self-reported trace.

**2. Set-membership entitlement vs. identity-blind scoring.**
LlamaGuard, Lakera, regex deny-lists, and all output-only classifiers are identity-blind: the same string is fine for one caller and a breach for another. The most common real enterprise AI incident — a correct answer leaked to the wrong person via an over-permissioned index — is invisible to all of them. ControlPlane carries the caller's identity into the verification layer and checks `span.acl ⊆ principal.clearance` as a deterministic set-membership test in Lane 1, with zero LLM. This is not a better classifier — it is a different question.

**3. Per-action blast-radius pricing vs. one-threshold scoring.**
RAG groundedness checkers produce a single number (e.g., 0.82) that means the same thing on a draft and on a wire transfer. Azure AI Content Safety and Bedrock Guardrails produce a composite risk score ("Trust: 87/100") that maps to no intervention — you cannot block, edit, or escalate on 87. ControlPlane applies the identical verdict to four different actuators depending on the blast radius of the pending action. The same unsupported claim annotates a draft and holds a payment. This is not a finer threshold — it is a different decision geometry.

**4. Worst-claim-per-action weighting vs. response averaging.**
Groundedness checkers average across all claims in a response. One wrong figure in a nine-sentence answer drowns in the average. ControlPlane evaluates the *worst claim* for each pending action independently — the refund is held because clause 7.2 has no span, even if the order number and amount are correct. The same response produces two different actuators on two different pending actions. This is not a stricter threshold — it is a different aggregation rule.

**5. Published per-route false-negative rate vs. precision-only reporting.**
Every competitor publishes precision — the rate at which the tool bothers the user. None publish their own miss rate. ControlPlane ships a per-route FNR schema with typed fields and confidence intervals. In the prototype, the fields are null — the emptiness is the credibility play, because it says we know exactly which fields are knowable at design time and which are not. In production, the fields are populated through stratified shadow audit. The claim shape: *"On this route we catch X% of ungrounded claims at 40 ms p50 — and here is the Y% we don't."* This is not a stronger accuracy claim — it is a different standard of honesty.

---

## 8. Fidelity Self-Check

This business proposal does **not**:

- [x] **Soften Default = UNSUPPORTED.** Every claim is described as born unsupported and must earn proof. No language implies claims start neutral or pass unless flagged.
- [x] **Weaken entitlement.** Entitlement is described as deterministic set-membership, Lane 1, zero LLM, cannot be disabled. No language implies it is a classifier, a score, or optional.
- [x] **Redraw the matrix.** The matrix is referenced as the exact frozen 4×4 table. No simplified low/medium/high version, no route-specific cell overrides, no invented actuators.
- [x] **Move the hard gate from actions to tokens.** The gate is described as sitting on the commit path for actions, with text streaming behind a hold-back buffer. No language implies token-level blocking or post-hoc recall as the primary mechanism.
- [x] **Claim the system eliminates hallucinations / bias / privacy risk.** The refuse-to-claim list is preserved. The system claims that unproven claims cannot authorise actions and publishes what it misses.
- [x] **Introduce LLM-as-judge or confidence scores as the primary mechanism.** The Action Interlock is described as a pure rule engine. No confidence, logprob, or risk score drives any actuator.
- [x] **Treat bias as a live per-response verdict.** Bias is described only as async route-level counterfactual flip-rate with confidence intervals — a distributional property, never a per-claim matrix input.
- [x] **Say the refund was "blocked."** The refund is described as "held and escalated with the evidence packet." The word "blocked" does not appear in relation to the R3 × unsupported-categorical path.
- [x] **Invent production ROI percentages.** Impact logic is directional and causal. No fabricated savings or accuracy numbers.
- [x] **Reopen Stage 1–3 scope.** The prototype boundary, the two-route live scope, the dual-action centrepiece, and all R2S1–R2S3 fidelity invariants are treated as immutable inputs.

---

*End of frozen Round 2 Stage 4 Business Proposal Spine.*