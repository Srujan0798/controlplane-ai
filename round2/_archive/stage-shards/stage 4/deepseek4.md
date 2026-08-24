## 1. Problem Framing

Enterprises have moved from AI that answers to AI that acts. The unit of failure is no longer a bad paragraph; it is an executed transaction — and the executed transaction is authorised by a set of **claims** the system never had to prove.

The frozen running example is the clean version: *“Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.”* Clause 7.2 does not exist. The response can be fluent, confident, and lexically clean. If ungated, the company wrongly pays out. The customer did not lose money. The cost changed category: it used to be a bad paragraph; it is now an executed transaction.

Existing approaches fail because they inspect the **output**, not the **context contract**.

- **LLM-as-judge / groundedness scorers** ask “does this look right?” without knowing who asked, without capturing what the model was actually given, and without standing in the commit path.
- **Static guardrails** match banned surface forms. A fabricated invoice number, a correct answer, and an unauthorized HR disclosure can all be lexically clean.
- **Observability tools** tell you what went wrong after the action fired.
- **Confidence/logprob thresholds** fail by definition: the named failure is *confidently* wrong.
- **Composite risk scores** collapse leakage, hallucination, and safety into one number that cannot be blocked, edited, or escalated.

The specific failure modes ControlPlane addresses are:

1. A categorical claim with **no supporting provenance** authorising an irreversible action.
2. A claim that binds to real evidence the **caller is not entitled to read**.
3. A response carrying **two pending actions with different blast radii**, where one text path should be edited while the payment path should be held.
4. No reliable real-time ground truth — so the system cannot assume verification; it must invert the burden.

ControlPlane is therefore not an AI-safety dashboard. It is admission control for claims requesting permission to act.

---

## 2. Solution Design Summary

ControlPlane is an **admission-control layer** deployed as an OpenAI-compatible reverse proxy plus a thin context-assembly SDK hook. It does not require model weights, logits, or fine-tuning. It works at the input/output layer only.

The core mechanism is fixed:

- **Provenance is captured outside the model at context assembly.** Every retrieved chunk, tool result, DB row, and system context item is recorded as a span with `source_id · ACL · content_hash · offsets`. The model cannot author, alter, or self-report provenance.
- **Every check-worthy claim starts `UNSUPPORTED`.** A claim becomes `SUPPORTED` only by deterministic recomputation or binding against the captured provenance set. `UNKNOWN` never collapses into `SUPPORTED`.
- **Entitlement is deterministic set-membership.** Caller principal vs span ACL. Zero LLM in the entitlement path.
- **One graph governs three reads.** `STEP → SPAN → CLAIM → ACTION` is read forward for performance, backward for cost, and by label for responsibility. Performance, cost, and responsibility are not three classifiers; they are three queries on one structure.
- **Blast radius prices verification.** The exact frozen R×S matrix maps verdict severity and blast radius to one actuator: `Pass`, `Pass + annotate`, `Edit`, `Escalate`, or `Block`. Verification effort follows consequence; low-R text gets fast deterministic checks, high-R actions get proof before commit.
- **The hard gate is on actions, not tokens.** Text streams optimistically behind a short hold-back. The commit path for an action is interlocked.
- **Escalation ships an evidence packet**, not a bare alert.
- **Every decision is written to an append-only, hash-chained Evidence Ledger.**

The prototype demonstrates the strongest single path: one response carrying two pending actions. Text shows to customer → `R1 × entitlement → Edit`. Refund executes → `R3 × unsupported-categorical → Escalate`. The refund is **held and escalated with the evidence packet**, never called “blocked.” The company does not wrongly pay out.

The enterprise envelope adds route configuration, governance, feedback, and measurement around this same primitive. It does not add a second detector.

---

## 3. Target Users & Buyers

**Economic buyer: enterprise Chief Information Officer / Chief Technology Officer / Head of AI Platform.**  
This buyer owns the move from AI that answers to AI that acts, and owns the downside of an irreversible wrong action. ControlPlane is infrastructure: it reduces tail liability, creates an audit trail, and does not require replacing the model stack.

**Technical buyer / operator: head of AI platform engineering, MLOps, or enterprise security engineering.**  
This buyer must integrate and operate the control plane. The decision criterion is structural: provenance outside the model, deterministic entitlement, hard action gate, latency budget, and policy versioning. The integration cost is real and must be visible — one SDK hook plus proxy, not a zero-integration claim.

**Day-to-day users and approvers: AI product owners, risk/compliance officers, and human escalation reviewers.**  
Product owners operate routes and decide shadow/canary/enforce lifecycle. Compliance reviewers consume the per-route evidence ledger and FNR schema. Human escalation reviewers receive evidence packets instead of raw alert queues.

**Buyer not addressed:** ControlPlane does not sell “responsible AI” as a moral service. It sells authorisation infrastructure.

---

## 4. Business Case & Impact Logic

Value is created through four mechanisms. No fabricated ROI percentages are used. The logic is directional and auditable once the system is live.

1. **Avoided wrong actions.**  
   The value is the tail risk, not the average case. A single unauthorised payment, deletion, publication, or regulated-advice action can create regulator action, contractual loss, legal liability, and operational cleanup. ControlPlane changes the cost of that event from “happened and discovered later” to “held and escalated.” The prototype shows the mechanism: `refund.execute` does not commit when a categorical claim has no supporting span.

2. **Reduced dead compute.**  
   The graph gives an exact backward walk: a step that grounded zero accepted claims is dead compute. That number exists because provenance and claim-binding exist. It is not estimated from traces or predicted by a model.

3. **Reduced alert fatigue without lowering the gate.**  
   The matrix applies proportionate actuators. R0/R1 text mostly passes with annotation, while R2/R3 actions are gated. Over-flagging is controlled by blast-radius pricing, not by weakening the burden of proof.

4. **Auditability as an operating asset.**  
   Every decision can be reconstructed from the append-only Evidence Ledger: action → matrix cell → claim verdict → bound or missing span → source ACL → principal → policy version. That audit trail reduces the cost of internal review and external demonstration.

The business case is therefore:

> **ControlPlane does not promise to make AI safe. It makes unproven or unauthorized claims unable to authorise actions, and it publishes what it missed.**

The value is strongest for enterprises with a small number of high-consequence action routes and a large volume of low-consequence read-only routes.

---

## 5. Phased Roadmap

Every phase earns enforcement. No phase switches enforcement on globally.

### Phase 0 — Working Prototype (Stage 3)

**What exists:** single-node prototype with synthetic corpora, two routes, live provenance, graph UI, mock action executor, dual-action refund gate, entitlement flip, and empty FNR schema.  
**What is proven:** an unproven or unauthorized claim cannot authorise an action.  
**Exit condition:** all 25 binary Stage 1 success criteria pass.

### Phase 1 — Shadow Deployment on One or Two Real Routes

**What changes:** deploy behind real AI applications but in **shadow mode**. Gated-vs-ungated dual-emit; no production action is held.  
**What is earned:** per-route counterfactual data — *would have held N, of which M were true positives* — plus first real latency and evidence coverage measurements.  
**Enforcement:** none.  
**Exit condition:** shadow data is sufficient to open a canary without blind intervention.

### Phase 2 — Canary Enforcement on R0/R1 Routes

**What changes:** enable enforcement only on low-consequence read-only routes. Human-visible text may be edited or annotated; no R2/R3 action is gated in production.  
**What is earned:** measured intervention precision, override rate, and operational tolerability.  
**Exit condition:** override rate below threshold; edited text does not produce material user-visible regressions.

### Phase 3 — Limited Enforcement on R2/R3 Actions

**What changes:** enable the action gate on selected reversible and irreversible actions. The frozen matrix applies per pending action. Escalation ships evidence packets to the configured human reviewer.  
**What is earned:** per-route FNR schema begins to fill only with trustworthy ground truth; every populated field carries `measurement_status` and confidence intervals.  
**Exit condition:** FNR and FP/override metrics meet buyer-defined thresholds; audit trail is reproducible.

### Phase 4 — Broader Enterprise Rollout with Governance Overlays

**What changes:** add route packs, decision-support routes, jurisdiction-specific additive overlays, and policy DAG validation pipeline. Bias measurement remains route-level, asynchronous, counterfactual — never per-response.  
**What is earned:** operational control across heterogeneous routes without changing the core matrix.  
**Exit condition:** policy lifecycle demonstrably safe; no policy change ships without shadow replay, canary, and auto-rollback.

At every phase, **publication of misses is mandatory**. The FNR schema is shown before any production percentage exists. Emptiness is the credibility play.

---

## 6. Key Risks & Mitigations

### Risk 1 — False assurance on derived and multi-hop claims

**Risk:** a synthesised or multi-hop claim is superficially bound to a span and marked `SUPPORTED`. This creates false assurance — worse than no control plane because humans stop checking.

**Mitigation:**

- Derived/aggregative claims bypass ordinary entailment; they are recomputed from spans or returned `UNKNOWN`.
- `UNKNOWN` never collapses into `SUPPORTED`.
- Proof depth is bounded; timeout returns `UNKNOWN`, routed by matrix and fail stance.
- Verifiers are decorrelated from the generator.
- Per-route FNR is stratified by claim type, so residual misses on derived claims are published.

### Risk 2 — Wrong or missing upstream ACLs / over-permissioned indexes

**Risk:** ControlPlane enforces the ACLs carried by the source. If the source ACL is wrong or missing, the plane can enforce a wrong policy or create false safety.

**Mitigation:**

- Every span carries `source_id` and content hash. Missing ACL is recorded as `acl_unknown` and treated as unentitled on privileged routes.
- Entitlement-violation rate by source is a first-class operational signal for over-permissioned indexes.
- The plane does not claim to repair IAM; it makes IAM failures visible and measurable.
- Quarantine/de-rank is performed via policy version, not runtime model judgment.

### Risk 3 — Over-flagging causes bypass; under-flagging creates liability

**Risk:** if the plane blocks or escalates too much, operators will bypass it. If it passes too much, liability returns.

**Mitigation:**

- R0/R1 fail open with annotation; R2/R3 fail closed or escalate.
- The hard gate is on actions, not text. Low-consequence volume stays fast and low-friction.
- Routes start in shadow; enforcement is earned.
- Policy changes require shadow replay + canary + auto-rollback on override rate above 3× baseline.
- Circuit breaker downgrades autonomy before operators feel forced to switch the plane off.

### Risk 4 — Integration cost and provenance coverage gaps

**Risk:** if the context-assembly hook misses spans, the graph is incomplete and the gate can produce false `UNSUPPORTED` or miss evidence.

**Mitigation:**

- The integration surface is explicit: one SDK hook plus OpenAI-compatible proxy. It is not advertised as zero integration.
- Provenance scope is defined per route; source classes and metadata requirements are declarative.
- Evidence coverage is a measured metric, not an assumption.
- Missing ACL or missing source metadata is treated conservatively on high-R routes.

---

## 7. Differentiation Anchor

**1. Set-membership test, not judgment call.**  
Competitors ask *“does this look right?”* ControlPlane asks *“which span proves it?”* A claim binds to captured provenance or it does not. The default is `UNSUPPORTED`. That is not a score; it is a query with an answer.

**2. Identity lives in the verification layer.**  
ControlPlane carries caller principal and source ACL on every span. The same semantically correct claim produces different outcomes for different principals. LLM-as-judge and RAG groundedness checkers are identity-blind. Entitlement is deterministic set-membership, zero LLM.

**3. Hard gate on actions, not tokens.**  
Guardrails block or score text. ControlPlane streams text behind a hold-back and gates the commit path. Harm lives in the action, not the prose.

**4. Exact blast-radius × verdict matrix, never a composite score.**  
The identical verdict annotates a draft and holds a payment. That is a structural decision, not a threshold on a 0–100 trust score. The matrix is frozen and applied per pending action.

**5. Publishes its own per-route false-negative rate.**  
Competitors publish precision — the rate at which they bother the user. ControlPlane publishes the rate at which it **missed**. The FNR is a format with nulls until measured. That is the credibility move none of them make.

**Bonus, from the same graph:** dead compute is exact. A dashboard can report spend. ControlPlane can report which steps grounded nothing.

---

## 8. Fidelity Self-Check

Explicit confirmation:

| Frozen invariant | Status in Business Proposal |
|---|---|
| **Default = `UNSUPPORTED`** | Preserved. The proposal never implies pass-by-default or confidence-driven approval. |
| **Entitlement / ACL check** | Preserved. Identity and source ACL remain deterministic and central. |
| **Exact R×S matrix** | Preserved. The proposal refers to the frozen matrix and never redraws or softens it. |
| **Hard gate on actions, not tokens** | Preserved. Text may stream/edit; actions are gated. |
| **Eliminate hallucinations / bias / privacy risk** | Not claimed. The proposal claims only that unproven or unauthorized claims cannot authorise actions. |
| **LLM-as-judge or confidence scores as primary mechanism** | Not introduced. Decision time is a pure rule engine. |
| **Bias as live per-response verdict** | Not introduced. Bias remains route-level, asynchronous, proposal-only measurement. |

Also preserved:

- Two-pending-actions resolution: `R1 Edit` + `R3 Escalate`, never one response-level verdict.
- Refund language: *held and escalated with the evidence packet*, never “blocked.”
- FNR as empty typed schema until earned.
- Surgical edit only.
- Evidence-packet escalation.
- API-only integration, no weights/logits.
- One graph, three reads.

The business proposal makes the frozen architecture the only acceptable design: once you accept that an AI response is a set of claims requesting permission to act, you must capture provenance outside the model, you must invert the burden of proof, you must check entitlement, and you must price verification by blast radius. Any softer design is a different product.

---

*End of Stage 4 Business Proposal Spine.*