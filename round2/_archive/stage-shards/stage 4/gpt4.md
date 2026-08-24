# 1. Problem Framing

The enterprise problem is no longer primarily **incorrect text**. It is that AI systems now emit outputs that can trigger refunds, sends, writes, deletions, publications, and other consequential actions; the economic failure therefore moves from *bad paragraph* to **executed transaction**. ControlPlane's running example makes that concrete: a fabricated Clause 7.2 can survive ordinary lexical checks and still authorize a ₹1,84,000 refund unless the action is tied to a proof obligation. 

Existing approaches fail because they inspect the wrong object at the wrong boundary. Static guardrails are surface- and identity-blind; groundedness checkers typically inspect retrieval rather than the complete context/tool/DB evidence path, average claims, and do not know what the output is about to do; LLM-as-judge systems produce another model opinion without necessarily possessing the original evidence or caller identity; observability systems report failures after the action rather than controlling the commit path.  

The enterprise consequence is asymmetric. A false positive on an internal draft is annoying; a false negative on a payment or regulated action is a liability event. That is why the frozen architecture separates **verdict severity** from **blast radius** and prices verification effort by consequence rather than using one global threshold. 

The official Round 2 brief makes the deployment problem harder: routes have different latency/risk budgets, there may be no reliable real-time ground truth, actions compound across turns, regulation changes, and models are consumed through APIs rather than exposed internals. 

---

# 2. Solution Design Summary

ControlPlane.ai is an **admission-control layer** placed between AI generation/context assembly and consequential execution.

The system captures provenance **outside the model** at context assembly, including source identity and ACL information; every check-worthy claim starts **UNSUPPORTED** and must earn support against that captured evidence; entitlement is a deterministic caller-vs-source ACL set-membership test; and the same `STEP → SPAN → CLAIM → ACTION` graph feeds performance, responsibility, and cost reads.  

The Action Interlock then computes blast radius `R` and combines it with verdict severity `S` through the **immutable R×S matrix**, per pending action. Text can proceed behind a short hold-back; consequential actions cross a hard commit gate. 

The business proposition is therefore narrow:

> **ControlPlane does not promise to make AI truthful. It makes an unproven or unauthorized claim unable to authorize an action, and measures what the plane itself misses.**

That is also the correct boundary of the claim: the architecture explicitly refuses to claim elimination of hallucination, zero integration, zero added latency, or one universal accuracy number. 

---

# 3. Target Users & Buyers

The frozen sources define the operating problem and enterprise routes, but they do **not** name a formal purchasing org chart. The following is therefore the recommended buying/operating structure derived from the architecture, rather than a source-stated fact.

| Role                                                                                    | Why they care                                                                               | ControlPlane value                                                                                       |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Economic buyer — AI/technology executive**                                            | AI adoption creates financial and operational exposure once systems can act                 | Establishes a common execution-control plane across AI routes rather than buying separate point controls |
| **Technical buyer — AI platform / enterprise architecture / security engineering lead** | Must integrate API-consumed models without model internals and control heterogeneous routes | SDK context hook + API proxy + one Evidence Ledger + deterministic Interlock                             |
| **Risk / security / compliance stakeholder**                                            | Needs identity-aware authorization, traceability, policy versioning, and evidence           | ACL decisions, hash-chained ledger, matrix-cell auditability, FNR reporting                              |
| **Day-to-day operator — AI platform / SRE / route owner**                               | Needs to tune enforcement without creating alert fatigue or breaking latency                | Shadow → canary → enforce, route profiles, overrides, error budgets, circuit breaker                     |
| **Application / agent team**                                                            | Owns the AI workflow and downstream actions                                                 | Action adapters and pre-commit interlock without requiring access to model weights                       |

The strongest initial buyer is the enterprise already deploying **customer-facing or internal AI agents with consequential writes**, because the economic case is clearest when one model response can cross an execution boundary. The reference environment explicitly includes customer support, internal knowledge, and decision-support routes.  

The product should therefore enter through a **high-consequence route**, not as an enterprise-wide "AI safety" purchase.

---

# 4. Business Case & Impact Logic

The business case should be expressed as **measurable avoided cost and controlled exposure**, not fabricated ROI percentages.

## A. Avoided wrong actions

Primary value:

```text
Exposure
= frequency of consequential AI actions
× probability of an unproven/unauthorized claim
× loss per wrong action
```

ControlPlane changes the last step from:

```text
AI output → action
```

to:

```text
AI output
→ claim proof
→ entitlement
→ R×S
→ action admitted / edited / escalated / blocked
```

The refund example demonstrates the economic category directly: without the interlock, the company wrongly pays ₹1,84,000; with the interlock, the refund is **held and escalated with the evidence packet**. 

Do not claim a universal savings percentage. The correct commercial conversation is:

> **What consequential actions does this route perform today, what is the loss if one is wrong, and what fraction of those actions can we place behind an earned admission boundary?**

## B. Lower verification cost through blast-radius pricing

Not every interaction deserves the same verification budget.

The architecture gives R0/R1 traffic a primarily deterministic low-latency path, while higher-consequence traffic receives deeper verification. Lane 1 remains always-on; Lane 2 is bounded; Lane 3 is asynchronous. 

This creates an operational value equation:

```text
Verification cost
↓
because expensive proof is concentrated where consequence is high
```

rather than:

```text
Verification cost
↑
because every response gets the same expensive checker
```

That directly addresses the official brief's one-size-fits-all latency problem. 

## C. Reduced dead compute

The Evidence Ledger can walk backward from accepted claims and identify steps that produced evidence grounding **zero accepted claims**. This is exact rather than estimated. 

Business value:

```text
dead compute
→ unnecessary model/tool spend
→ measurable source of waste
```

This is particularly relevant to agentic workloads where repeated tool calls and non-convergent traces can become a direct operating-cost problem.

The proposal should sell this as **a second value stream from the same graph**, not as a separate optimization product.

## D. Reduced alert fatigue

The frozen system does not "flag everything."

Low-consequence findings can produce annotation or pass; high-consequence findings receive proportionate intervention. This is the function of the matrix. 

The business metric is therefore:

```text
human overrides
gate-fail rate
edit/escalation rate
per route
```

not "number of alerts generated."

Policy changes are replayed and canary-tested, with automatic rollback if override rate exceeds 3× baseline or the route error budget is breached. 

## E. Auditability

Every consequential decision can be reconstructed from:

```text
action
→ matrix cell
→ claim verdict
→ bound/missing span
→ source + hash + ACL
→ principal entitlement
→ policy version
→ verifier versions
→ latency + lane
```

That is substantially stronger than a post-hoc "the model produced this answer" trace. 

## F. Trustworthiness measurement

The enterprise contract is to publish **what ControlPlane missed**, not merely what it caught. FNR remains a typed measurement format whose values stay unavailable until legitimate ground truth exists. 

That changes the buyer conversation from:

> "Trust our AI safety score."

to:

> "Here is the route, the evaluation population, what we missed, and the uncertainty around that measurement."

---

# 5. Phased Roadmap

The roadmap should be an **earn-out**, not a feature calendar.

## Phase 0 — Stage 3 Prototype

**State:** Demonstration-only.

Contains exactly the frozen dual-action refund flow and knowledge principal flip, with the Evidence Ledger, matrix, action gate, packet, and empty FNR schema. 

**What is earned:** mechanism credibility.

**What is not earned:** production enforcement.

---

## Phase 1 — Shadow Deployment on One Real Route

Select one real enterprise route, preferably a consequential support/action workflow.

Deploy:

* context-assembly hook;
* API proxy;
* Evidence Ledger;
* ACL capture;
* deterministic proof;
* Action Interlock;
* shadow dual-emit.

All decisions are advisory/counterfactual at this stage.

Measure:

* intervention distribution;
* latency;
* entitlement violations;
* override reasons;
* evidence coverage;
* initial FNR where ground truth permits.

This follows the frozen day-one posture: every route starts in **shadow**. 

**What is earned:** a route-specific evidence baseline.

---

## Phase 2 — Canary Enforcement on High-Consequence Actions

Move only a bounded slice of the route into enforcement.

The policy lifecycle is:

```text
immutable policy draft
→ static invariant validation
→ replay previous traces
→ bounded canary
→ auto-rollback if thresholds breached
→ named-principal approval
→ gradual promotion
```



The first production enforcement should be the **R3 action path**, because that is where the economic liability is concentrated. R1 text can remain shadow/canary initially. The route profile explicitly supports this posture. 

**What is earned:** evidence that the route can enforce without unacceptable operational disruption.

---

## Phase 3 — Second Route + Enterprise Governance

Deploy the internal knowledge route.

Add:

* broader ACL/source integrations;
* versioned policy overlays;
* geography/industry configuration;
* evidence retention;
* override adjudication;
* route-specific FNR/FP reporting;
* circuit-breaker controls.

The same graph and same matrix remain unchanged; only route policy changes. 

**What is earned:** repeatability across heterogeneous routes.

---

## Phase 4 — Broader Enterprise Rollout

Extend the plane across:

* customer support;
* internal knowledge;
* decision-support;
* agentic workflows.

Add enterprise integrations and multi-tenant HA/failover, production-scale traffic validation, broader IAM/action connectors, and production feedback pipelines. The source explicitly places those beyond the Stage 1 prototype. 

Decision-support adds the existing enterprise-only asynchronous bias measurement:

```text
decision route
→ counterfactual replay
→ protected-attribute perturbation
→ flip rate + CI
→ route policy/autonomy review
```

Never:

```text
claim → bias verdict → matrix
```



**What is earned:** enterprise-scale operating capability, not a new safety mechanism.

---

# 6. Key Risks & Mitigations

## Risk 1 — False assurance on derived or multi-hop claims

**Problem:** shallow entailment can mark a synthesized claim `SUPPORTED`.

**Mitigation:**

* derived/aggregative claims bypass ordinary NLI;
* recompute from spans or return `UNKNOWN`;
* timeout → `UNKNOWN`;
* `UNKNOWN` never becomes `SUPPORTED`;
* publish FNR stratified by claim type.

This is explicitly the architecture's strongest residual technical risk. 

---

## Risk 2 — Bad source data or broken upstream ACLs

**Problem:** ControlPlane can faithfully enforce an incorrect ACL or poisoned source.

**Mitigation:**

* immutable `source_id` + content hash;
* missing ACL becomes an explicit gap;
* entitlement violations reported by source;
* connector quarantine through policy version;
* forensic ledger enables rollback.

The boundary is explicit: ControlPlane protects the **claim-to-evidence relationship**; it does not certify source truth or repair IAM. 

---

## Risk 3 — Over-intervention causes users to disable the system

**Problem:** too many edits/escalations create bypass pressure; too few create liability.

**Mitigation:**

* blast-radius-priced verification;
* R0/R1 lower-cost handling;
* R2/R3 fail closed or escalate;
* shadow before enforcement;
* replay before every policy release;
* canary;
* auto-rollback at >3× baseline human override;
* circuit breaker;
* hard interlock in the **action executor**, not just the UI.



---

## Risk 4 — Integration friction

**Problem:** provenance must be captured at context assembly, so "zero integration" is impossible.

**Mitigation:**

* thin context-assembly SDK hook;
* OpenAI-compatible reverse proxy;
* no model-weight dependency;
* preserve existing application workflow where possible.

The source is deliberately honest: the integration cost is real, and it is part of the structural moat rather than something to hide. 

---

## Risk 5 — Model/runtime dependency

**Problem:** generator models change, but the control plane must remain stable.

**Mitigation:**

* API-only boundary;
* typed Evidence Ledger contract;
* offline, versioned binder/claim-extractor releases;
* deterministic Action Interlock;
* no online weight updates from human feedback.

Live feedback changes policy candidates, not the security boundary or model weights on the critical path. 

---

# 7. Differentiation Anchor

These are the five points that should survive in every commercial artifact.

### 1. **Evidence, not model opinion**

Typical LLM-as-judge systems ask:

> "Does this look right?"

ControlPlane asks:

> **"Which externally captured span proves it?"**

The evidence record exists before generation, and the model cannot author the binding.  

### 2. **Identity-aware entitlement**

LlamaGuard-style/static controls can inspect the output string but do not establish whether the **caller is entitled to the source** behind the claim.

ControlPlane carries:

```text
principal → claim → span → source ACL
```

and evaluates that relationship deterministically.  

### 3. **Admission at the action boundary**

Observability tools explain what happened after the trace; groundedness systems can tell you something about the text.

ControlPlane sits in the commit path:

```text
claim proof
→ entitlement
→ R×S
→ action admission
```

The text may stream; the action does not execute without the required decision. 

### 4. **Blast radius is orthogonal to verdict**

The same `UNSUPPORTED + categorical` finding does not have one universal response.

It yields:

```text
R1 → Edit
R3 → Escalate
```

because consequence and evidence are separate axes. That is why the matrix is not merely renamed severity. 

### 5. **Publish the miss rate**

Most systems emphasize precision/alerts.

ControlPlane's trust contract is the inverse:

> **publish the false-negative rate per route when legitimate measurement exists.**

Until then, the field stays empty rather than being manufactured. 

---

# 8. Fidelity Self-Check

| Frozen invariant                         | Business Proposal status                                                                                                                                                                  |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Default = UNSUPPORTED**                | **Preserved.** The business model never turns absence of proof into implicit allow.                                                                                                       |
| **Entitlement / ACL**                    | **Preserved.** It remains deterministic, always-on, zero-LLM, and tied to caller/source identity.                                                                                         |
| **Exact R×S matrix**                     | **Preserved.** Routes supply R inputs; they never receive route-specific matrix cells.                                                                                                    |
| **Hard gate on actions**                 | **Preserved.** The proposal explicitly sells commit-path control, not token blocking.                                                                                                     |
| **No elimination claim**                 | **Preserved.** We do not claim to eliminate hallucination, bias, or privacy risk; the claim is narrower: unproven/unauthorized claims cannot authorize actions, and misses are measured.  |
| **No LLM-as-judge primary mechanism**    | **Preserved.** Model-assisted binding may exist, but decision-time policy evaluation remains deterministic.                                                                               |
| **No confidence-score disposition**      | **Preserved.** No confidence/logprob/composite risk score controls the actuator.                                                                                                          |
| **Bias not a live per-response verdict** | **Preserved.** Bias remains route-level asynchronous counterfactual measurement.                                                                                                          |
| **Two-pending-actions resolution**       | **Preserved.** The business case uses the exact `R1 → Edit` + `R3 → Escalate` story and never collapses it to a single response disposition.                                              |
| **FNR remains a format until earned**    | **Preserved.** No fabricated production number enters the business case.                                                                                                                  |

## Business proposal spine

The proposal should therefore tell one economic story:

```text
AI can now ACT
      ↓
wrong output became executed loss
      ↓
existing tools inspect text / logs
      ↓
they do not own the evidence contract or commit boundary
      ↓
ControlPlane captures provenance outside the model
      ↓
claims start UNSUPPORTED
      ↓
entitlement is checked
      ↓
blast radius prices verification
      ↓
the same graph controls the action
      ↓
shadow evidence earns enforcement
      ↓
the plane publishes what it missed
```

That keeps the business proposal downstream of the frozen architecture rather than turning it into a generic AI-governance narrative. The official Round 2 brief asks for the business proposal, working prototype, and pitch as separate deliverables; the business proposal should therefore explain **how the already-proven mechanism becomes an enterprise operating system**, not introduce another mechanism. 
