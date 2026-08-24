# ControlPlane.ai — Round 2 Stage 4: Business Proposal Spine

> Accenture Innovation Challenge 2026 · Round 2 · Stage 4 — Detailed Business Proposal
> Sources of truth (absolute): `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` (frozen) · `R2S2.md` (frozen) · `R2S3.md` (frozen)
> Status: **DRAFT** — Stage 1–3 are non-negotiable. This document does not reopen any frozen invariant, prototype boundary, dual-action resolution, or fidelity confirmation.
> This proposal is a rendering of the frozen architecture. It does not soften, extend, or re-interpret it.

---

## 1. Problem Framing

### The cost of a wrong output changed category

Enterprises have moved from AI that answers to AI that acts. A customer-support agent does not return a paragraph — it issues a refund. An internal copilot does not summarise a document — it drafts an email to an external partner. A decision-support tool does not display a number — it executes a transaction.

The existing oversight stack was built for the answering era. It scores text, charts failure rates, and asks a human to review the log next week. **This is an audit trail, not an interlock.** The failure mode has shifted from "bad paragraph" to "executed transaction" — and no existing tool sits in the commit path where the harm actually occurs.

### Why every current approach fails against the specific failure modes the freeze addresses

| Approach | What it does | Why it fails against the frozen failure modes |
|---|---|---|
| **LLM-as-judge** (NeMo Guardrails, most AI-safety wrappers) | A second model evaluates the first model's output | Uses the same reasoning that produced the error, from the same family of blind spots. Cannot state its own error rate. Too slow for the commit path. Does not carry caller identity into verification — so entitlement checking is structurally impossible. |
| **Static guardrails** (LlamaGuard, Lakera, regex) | Match banned surface forms at the perimeter | A fabricated invoice number, a salary leaked from an over-permissioned index, and a correct answer are all lexically clean. Guardrails see none of them. They are identity-blind: the same string is fine for one caller and a breach for another. |
| **RAG groundedness checkers** | Check whether output is supported by retrieval context | See retrieval only — not tool results, DB rows, computed values, or system context. Average across the response, so one wrong figure drowns in nine correct sentences. Action-blind: 0.82 means the same thing on a draft and on a wire transfer. None carry caller identity. |
| **Confidence thresholding** (logprobs, self-reported certainty) | Gate on the model's self-reported confidence | The named failure mode is **confidently** wrong. Confidence is the broken instrument. You cannot detect a calibration failure with the calibration. |
| **Post-hoc observability** (LangSmith, Helicone, Arize) | Record traces, chart failure rates, alert on anomalies | Tell you what went wrong after a user acted on it — the precise thing the brief asks to eliminate. They measure spend rather than waste: they can tell you the trace cost ₹8, but not that ₹5 of it grounded nothing. |
| **Composite risk scores** (Azure AI Content Safety, Bedrock Guardrails) | Collapse multiple signals into a single 0–100 number | Three failure modes with three different owners, costs, and remedies, collapsed into one number that maps to no intervention. You cannot block, edit, or escalate on 87. |

**What all six share:** they inspect the output, not the context contract. They score text rather than verify claims. They gate on words rather than on actions. **And not one of them publishes its own false-negative rate.**

### The specific failure mode that motivated the freeze

A refund agent responds: *"Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement."* Every filter passes it. Confidence reads 0.94. The company pays out ₹1,84,000. Clause 7.2 does not exist.

The failure is **absence** of evidence, not conflicting evidence — which is what makes it invisible to contradiction-based detectors. The company wrongly pays out; the customer did not lose money. Money moved Tuesday, found Friday.

This is not a hypothetical. This is the exact failure mode the architecture was designed against, and it is the centrepiece of the prototype demonstration.

---

## 2. Solution Design Summary

ControlPlane is an **admission-control layer** for AI systems. It does not score text. It does not monitor outputs. It treats every AI response as a set of **claims requesting permission to act**, captures the evidence the model was actually given at context-assembly time — outside the model, where it is tamper-proof — and refuses to let an unproven claim cross into an action.

### Core primitive: one graph, built during generation

```
STEP ──produces──▶ SPAN ──binds──▶ CLAIM ──authorizes──▶ ACTION
(tool call,       (retrieved chunk,  (typed atomic       (pending side
 retrieval,        tool row, DB       proposition         effect: tool +
 model turn)       record — with      from the output     args +
                   source_id, ACL,    stream)             irreversibility)
                   hash, offsets)
```

- **Performance reads it forward** — does each claim bind to a span?
- **Cost reads it backward** — did each step produce a span that grounded any accepted claim?
- **Responsibility reads its labels** — is the caller entitled to every span a claim binds to, and does the action fall inside its typed interlock?

One structure. Three axes. Three actuators.

### Non-negotiable invariants

1. **Provenance is captured outside the model.** The model cannot declare, author, or alter provenance. Context-assembly hooks record spans with `source_id · ACL · content_hash · offsets` before any claim is judged.

2. **Default = UNSUPPORTED.** Every check-worthy claim starts unsupported. `SUPPORTED` is earned only by binding or recomputation against the captured provenance set. `UNKNOWN` never collapses into `SUPPORTED`.

3. **Entitlement is deterministic set-membership.** Caller principal vs source ACL. Identity is in the verification layer. Zero LLM in the ACL decision path. This catches the most common real enterprise incident: an over-permissioned RAG index faithfully leaking HR data to the wrong employee.

4. **One graph, three reads.** Performance, cost, and responsibility are not three detectors bolted together — they are three reads of one `STEP → SPAN → CLAIM → ACTION` graph.

5. **Verification is priced by blast radius.** The exact frozen R×S matrix (`R0–R3` × `Contradicted/entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown`) determines the actuator. The matrix is transcribed, never redrawn. It is a pure function `f(R, S) → actuator` with no route parameter.

6. **Hard gate on actions, not tokens.** Text streams optimistically behind a ~150–300ms hold-back. The gate sits on the action commit path — where harm lives. Gating a tool call costs 20–40ms against a 200ms–2s round-trip.

7. **Actuators are exactly Block · Edit · Escalate · Pass** (plus autonomy downgrade and circuit breaker, which are spoken controls). No invented actuator labels.

8. **The plane publishes its own false-negative rate.** Per route, as a typed schema. The emptiness of the schema is the credibility play — a judge who tests it finds honesty rather than a bluff.

### Deployment shape

An OpenAI-compatible reverse proxy plus a thin context-assembly SDK hook. No application rewrite. No model access. No weights. No logits. No fine-tuning.

---

## 3. Target Users & Buyers

### Economic buyer

**VP/Director of AI Platform or CTO office.** Owns the risk of AI systems acting in production. Feels the pain when a wrong AI output becomes a wrong transaction — customer complaints, regulatory exposure, financial loss. Signs the budget because the cost of a wrong action has changed category.

### Technical buyer

**Platform / SRE lead responsible for the AI serving stack.** Evaluates whether the interlock can be integrated without rewriting the application. Needs the SDK hook + proxy deployment model. Cares about latency budgets (≤40ms p50 / ≤200ms p95 for R0/R1 text) and the fact that the plane does not require model access.

### Day-to-day operator

**App owner / product team building the AI feature.** Interacts with the evidence packet on escalation. Receives the structured output (claim + candidate spans + verdict + diff) rather than a bare alert. Needs the surgical edit to strip failing claims without re-running the full generation pipeline.

### Why the pain is acute for enterprises specifically

Enterprises run multiple AI use cases simultaneously — customer-facing chatbots, internal copilots, decision-support tools — each with a different risk signature. A single one-size-fits-all checking approach fails because:
- The same claim carries different consequences depending on what action it authorises (R0 text vs R3 payment).
- Caller identity determines whether a fact is authorised — the same span is fine for one principal and a breach for another.
- Regulatory expectations differ by geography and industry, and evolve continuously.

ControlPlane handles this by routing through the same matrix with different R-tier assignments and route configurations — never by inventing a second detector.

---

## 4. Business Case & Impact Logic

The value proposition is not "we catch hallucinations." It has a precise shape:

> **On this route we catch \<measured\>% of ungrounded claims at 40ms p50 — and here is the \<measured\>% we don't.**

### Value lever 1: Avoided wrong actions

When an AI system acts — refunds, sends, deletes, publishes — a wrong output becomes a wrong transaction. The cost is not a bad paragraph; it is ₹1,84,000 paid out under a clause that does not exist.

ControlPlane's value is proportional to the **blast radius of the actions it gates**. On R3 routes (irreversible or regulated: payment, deletion, publication), every held escalation is a prevented wrong action. On R2 routes (reversible write / external send), every surgical edit is a correction before the error reaches the user.

The logic of impact is: **the plane catches what the model cannot prove, at the point where the consequence is highest.** A wrong answer that stays in an R0 draft costs nothing. The same wrong answer authorising an R3 payment costs the full transaction value.

### Value lever 2: Exact dead-compute accounting

Walk the graph backward: every SUPPORTED claim in the accepted answer points to a span, which points to the step that produced it. **Any step that grounded zero accepted claims is dead compute** — computed exactly, not estimated.

An enterprise running tens of thousands of interactions per week with mixed retrieval, tool calls, and multi-step reasoning can identify the exact fraction of compute spend that produced nothing. No competitor has this number, because no competitor has the graph.

### Value lever 3: Reduced alert fatigue via proportionate intervention

The matrix prices verification by blast radius. R0/R1 traffic — the overwhelming majority of volume — passes with annotation through Lane 1 deterministic checks only (no LLM, no network hop). Expensive binding (Lane 2 NLI) runs only where blast radius justifies it.

This means: the plane does not generate alerts for draft text. It does not flag low-consequence claims. It intervenes only where the action carries consequence. The result is fewer, more meaningful interventions — the opposite of the alert-fatigue pattern that gets guardrail layers disabled.

### Value lever 4: Auditability without overhead

Every decision writes to an append-only, hash-chained ledger: `principal · evidence fragment · claim verdict · matrix cell · actuator · policy_version · verifier_versions · latency · lane · route_id`. An auditor can reconstruct any actuator from the ledger, policy version, and frozen matrix.

This is not a dashboard. It is a forensic trail that produces itself as a side-effect of the verification path. The compliance team gets a structured record without running a separate audit pipeline.

### What we refuse to quantify without measurement

We do not claim "99% detection accuracy." We do not claim "zero latency." We do not claim "eliminates hallucinations." Every numerical claim we make will be produced by the system's own published FNR pipeline — per route, with confidence intervals, and with honest null fields where ground truth is not yet trustworthy.

---

## 5. Phased Roadmap

Enforcement is **earned per route from counterfactual evidence** — never switched on globally. Production enforcement follows shadow → canary → enforce. Each phase must produce the evidence that justifies the next.

### Phase 0 — Shadow (prototype deployment)

**Scope:** One or two low-consequence internal routes (R0/R1).

**What runs:** The full verification pipeline — provenance capture, claim extraction, binding, entitlement, matrix lookup — operates in shadow mode. Actions proceed unmodified. The plane records what it *would have* done.

**Evidence produced:** The counterfactual — "would have held N actions, of which M were true positives and K were false positives." Latency impact measured. Override rate baseline established.

**Enforcement:** None. Text and actions flow unimpeded. The plane is an observer that records its own proposed interventions.

**What is earned:** Permission to deploy the gate on low-consequence routes, with auto-rollback if override rate exceeds 3× baseline.

### Phase 1 — Enforcement on R3 routes

**Scope:** The highest-consequence actions: payments, deletions, regulated advice.

**What runs:** The hard gate activates on the action commit path for R3 actions. R0/R1 traffic remains annotated only. Shadow dual-emit continues alongside enforcement to maintain the counterfactual.

**Evidence produced:** Real intervention data on R3 routes. FNR pipeline begins producing per-route measurements (initially `insufficient_sample`, transitioning to `prototype_corpus` as sample sizes grow).

**Enforcement:** Active on R3 only. R2/R1 remain in shadow.

**What is earned:** Permission to extend enforcement to R2 routes.

### Phase 2 — Enforcement on R2 routes

**Scope:** Reversible writes, external sends, non-irreversible side effects.

**What runs:** Gate activates on R2 actions. R3 enforcement continues. R0/R1 remain annotated.

**Evidence produced:** Broader FNR measurements. Route-specific calibration data. Override rate trends.

**Enforcement:** Active on R2 + R3. R0/R1 annotated.

**What is earned:** Permission to extend enforcement to R1 routes where blast radius justifies it.

### Phase 3 — Full enterprise envelope

**Scope:** All routes. Multi-tenant. Geographic and regulatory overlays.

**What runs:** Complete governance layer: versioned policy DAG, geo overlays (additive only), shadow → canary → rollback lifecycle, circuit breakers, per-route error budgets, counterfactual bias measurement (async, never per-response).

**Evidence produced:** Production FNR values per route with confidence intervals. Dead-compute percentages. Entitlement-violation rates by source and principal. Override-rate trends.

**Enforcement:** Full matrix enforcement on all routes, earned per route from Phase 0–2 evidence.

**What exists that did not exist in Phase 0:** Enterprise IAM integration, real payment adapters, production-scale feedback pipeline, full bias measurement program, jurisdiction packs, production FNR publication.

### Governance throughout every phase

- Every policy change requires shadow replay over the last N traces showing the FP/FN delta.
- Every change canaries by route and auto-rolls back if human-override rate exceeds 3× baseline.
- Fail stance belongs to the tier: R0/R1 fail open with annotation; R2/R3 fail closed or escalate. A universal fail-open is forbidden — it makes the plane bypassable by anyone who can induce load.
- The Action Interlock is a pure rule engine: zero LLM reasoning at decision time. Policy is declarative code, not a prompt.

---

## 6. Key Risks & Mitigations

### Technical risk 1: False assurance on derived / multi-hop claims

**Why it is the highest-stakes risk:** Multi-hop, aggregated, and synthesised claims are where entailment is weakest and where the value is highest. If the Prosecutor marks a subtly-wrong synthesised claim SUPPORTED because a shallow span looks similar, ControlPlane delivers false assurance — strictly worse than no control plane, because humans stop checking.

**Exact mitigation (from frozen architecture):**
- Derived/aggregative claims bypass ordinary NLI → recompute from spans or return `UNKNOWN`.
- `UNKNOWN` never becomes `SUPPORTED`. That one rule is the boundary between a control plane and false assurance.
- Timeout → `UNKNOWN` → matrix + fail stance (never silent allow).
- Verifier model family decorrelated from generator.
- FNR stratified by claim type publishes residual misses.

### Technical risk 2: Poisoned source evidence or wrong upstream ACLs

**Why it remains:** ControlPlane proves `claim ↔ captured evidence` and enforces carried ACLs. It does not prove the source is true and does not repair IAM.

**Exact mitigation:**
- Immutable `source_id` + content hash on every accepted binding.
- Missing ACL recorded as gap; treated as unentitled on privileged routes.
- Entitlement-violation rate per source = operational detector for over-permissioned indexes (reporting signal, not silent AI remediation).
- Boundary stated out loud: we defend the claim-to-evidence link, not the truth of the evidence.

### Operational risk 3: Over-flagging creates alert fatigue; under-flagging creates liability

**Why it is inherent:** The brief requires this tradeoff to be deliberately tuned, not solved away.

**Exact mitigation:**
- Shadow default before production enforcement; earn-out per route.
- Blast-radius-priced verification depth: R0/R1 gets Lane 1 only (80–90% of volume).
- R0/R1 fail open with annotation; R2/R3 fail closed or escalate.
- Auto-rollback on override rate > 3× baseline.
- Circuit breaker downgrades autonomy.
- Hard interlock in the action executor, not only the UI.

### Adoption risk 4: Integration cost perceived as too high

**Why it matters:** A team that discovers the integration cost after being sold "drop-in" churns.

**Exact mitigation (stated honestly):**
- SDK hook at context assembly (where you already assemble context) + OpenAI-compatible reverse proxy.
- No model access, no weights, no logits, no fine-tuning, no application rewrite.
- If you are on a standard retrieval stack, the retriever already knows the source ID — you are adding the access rights and a hash.
- **The integration cost is the moat.** Say it out loud. Trading our strongest structural claim for a weaker convenience claim is a bad trade.

### Adoption risk 5: The plane gets disabled in a quarter, like every other guardrail

**Why it is the right question:** Over-blocking is what gets these layers disabled.

**Exact mitigation (why it is different here):**
- The hard gate is on actions, not text. R0/R1 — the overwhelming majority of volume — passes with annotation.
- Enforcement is earned per route through shadow evidence, so nobody is asked to trust it before it has produced its own counterfactual.
- The matrix exists specifically to prevent over-blocking: the identical verdict annotates a draft and holds a payment.

### Judge-facing risk 6: Pattern-matched as "another RAG groundedness checker"

**Why it matters:** If a judge categorises us in the first twenty seconds, everything after is heard as a variant of decks they have already sat through.

**Exact mitigation:**
- Open on a blocked transaction with a rupee figure, never on risk.
- The dual-action centrepiece (R1 Edit + R3 Escalate) proves the plane is not a groundedness checker — a groundedness checker does not have blast-radius pricing, entitlement, or action interlocks.
- "Everyone watches the exit. Nobody records the entrance." — permitted because it indicts what everyone else built.

---

## 7. Differentiation Anchor

Five points that separate ControlPlane from every existing category. Each is grounded in the frozen architecture and defensible against hostile questioning.

### 1. We query the evidence, not the model

Every other approach inspects the output. ControlPlane binds each claim back to a specific span of evidence the model was actually given, captured outside the model at context-assembly time — with source identity and access rights attached. The verdict is a set-membership test: which span proves it? — not an opinion formed after the fact.

### 2. Default = UNSUPPORTED — the burden of proof is on the claim

Common approaches default to allow: flag what looks wrong, but nothing passes because nobody objected. ControlPlane inverts the burden: nothing passes because nobody proved it. A claim must earn `SUPPORTED`. Absence of proof is not low confidence and not implicit allow.

### 3. Entitlement is identity, not classification

The most common real enterprise incident is not a hallucinated fact — it is a correct fact leaking to the wrong person via an over-permissioned RAG index. ControlPlane carries caller identity into the verification layer and performs deterministic ACL set-membership. No LLM. No classifier. Sub-millisecond. Structurally impossible for any output-only competitor to replicate.

### 4. Proof scales with consequence

The exact same verdict produces four different actuators depending on what the response is about to do. An unsupported claim in a draft text is annotated. The same unsupported claim authorising a ₹1,84,000 refund is held and escalated with an evidence packet. Blast-radius pricing means the plane stays fast on low-consequence traffic without weakening truth semantics on high-consequence traffic.

### 5. We publish what we miss

Every team will claim detection. Publishing your own false-negative rate — per route, with confidence intervals, with honest null fields where ground truth is not yet trustworthy — is the move none of them will make. The emptiness of the FNR schema is the credibility play. The plane is audited by the standard it enforces.

---

## 8. Fidelity Self-Check

This proposal is a rendering of the frozen architecture. It does not introduce, soften, or re-interpret any frozen invariant.

| Frozen invariant | Status in this proposal |
|---|---|
| **Default = UNSUPPORTED** | Untouched. Claims must earn SUPPORTED. Absence of proof is not low confidence. |
| **Entitlement / ACL check** | Untouched. Deterministic set-membership; identity in the verification layer; zero LLM in the ACL path. |
| **Exact R×S matrix** | Untouched. Transcribed from the frozen spec; never redrawn; no route parameter; no cell edits. |
| **Hard gate on actions, not tokens** | Untouched. Hold-back for text; commit boundary for tools/actions. |
| **Published FNR as a format** | Untouched. Typed schema; null/unavailable until earned; no fabricated production numbers. |
| **Two-pending-actions resolution** | Untouched. R1 Edit + R3 Escalate on the refund running example, simultaneously; never one response-level verdict. |
| **No LLM-as-judge on the critical path** | Untouched. Action Interlock is a pure rule engine; no confidence score disposition. |
| **Bias remains route-level / async only** | Untouched. Counterfactual flip-rate + CI; never a per-response matrix verdict. |

**This proposal does not:**
- Soften Default = UNSUPPORTED
- Weaken entitlement
- Redraw the matrix
- Move the hard gate from actions to tokens
- Claim the system eliminates hallucinations, bias, or privacy risk
- Introduce LLM-as-judge or confidence scores as the primary mechanism
- Treat bias as a live per-response verdict
- Invent new actuator labels
- Fabricate production FNR numbers
- Add a third live prototype route

**What this proposal does:** describes the enterprise operating envelope around the frozen admission primitive. The architecture is the system of record; this document is how we say it.

---

## Appendix A: Prototype Evidence (cross-reference)

The working prototype (R2S3) demonstrates:
- Live `STEP → SPAN → CLAIM → ACTION` Evidence Ledger
- Dual-action: R1 Edit on customer-visible text + R3 Escalate on ₹1,84,000 refund (held, never "blocked")
- Principal-flip entitlement check with zero LLM
- Empty FNR schema with typed placeholders
- Exact frozen 16-cell matrix with cells highlighted before actuators
- All 15 R2S1 success criteria mapped to implementation checks

Prototype commands: `python examples/refund_trace_demo.py` and `python examples/multi_usecase_demo.py`

---

*End of Round 2 Stage 4 — Business Proposal Spine.*
