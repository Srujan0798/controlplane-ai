# ControlPlane.ai — Round 2 Stage 4: Business Proposal Spine

> Accenture Innovation Challenge 2026 · Round 2 · Stage 4  
> Sources of truth (absolute): `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` (frozen) · `R2S2.md` (frozen) · `R2S3.md` (frozen)  
> Status: **FROZEN** — Stages 1–3 are non-negotiable. This document does not reopen any prototype boundary, mechanism, or fidelity invariant.

---

## 1. Problem Framing

### The category change

The cost of a wrong AI output has changed category.

**Before:** A wrong output was a bad paragraph. Embarrassing, perhaps. Reviewable next week. The failure mode was textual.

**Now:** A wrong output is an executed transaction. A refund issued. A record deleted. A regulated advice published. Code merged to production. The failure mode is **operational and irreversible**.

Enterprises have moved from AI that *answers* to AI that *acts* — it refunds, files, sends, books, writes to production — while oversight tooling is still built for the answering era: score the text, chart the failure, review the log next week. The oversight layer never got the memo that the output is now a **commit**.

### Why existing approaches fail against the specific failure modes

| Approach | What it inspects | What it misses (the freeze addresses) |
|----------|------------------|----------------------------------------|
| **LLM-as-judge** (NeMo Guardrails, most "AI safety" wrappers) | Finished text, usually without source documents, always without caller identity | Cannot detect retrieval-side authorization failure (over-permissioned RAG leaking HR data to wrong employee). Same model family = correlated blind spots. No error rate it can state. Too slow for commit path. |
| **Static guardrails** (LlamaGuard, Lakera, regex/deny-lists) | Banned surface forms | Fabricated invoice number, salary leaked from over-permissioned index, correct answer — all lexically clean. Identity-blind: same string fine for one caller, breach for another. |
| **Post-hoc observability** (LangSmith, Helicone, Arize, WhyLabs) | Traces after user acted | Tells you what went wrong *after* a user acted on it — the precise thing the brief asks to eliminate. Measures spend, not waste (cannot tell you ₹5 of ₹8 grounded nothing). |
| **Confidence thresholding** | Logprobs, self-reported certainty, verbalised hedging | Fails by definition: the named failure mode is *confidently* wrong. You cannot detect a calibration failure with the calibration. |
| **RAG groundedness checkers** | Retrieval only | Blind to tool results, DB rows, computed values, system context — where agents actually get facts. Averages: one wrong figure drowns in nine correct sentences. Action-blind: 0.82 means same thing on draft and wire transfer. |
| **Composite risk scores** (Azure AI Content Safety, Bedrock Guardrails) | "Trust: 87/100" | Three failure modes with three different owners, costs, remedies collapsed into one number mapping to no intervention. You cannot block, edit, or escalate on 87. |

**The common thread:** All six inspect the output, not the context contract. They score text rather than verify claims. They gate on words rather than actions. **Not one publishes its own false-negative rate.**

---

## 2. Solution Design Summary

ControlPlane.ai is an **admission-control layer** for AI systems.

**Core mechanism:** Every AI response is a set of claims requesting permission to act. ControlPlane captures provenance *outside the model* at context assembly (`source_id · ACL · hash · offsets`), binds each claim in the output back to a specific span of that evidence, and refuses to let an unproven or unauthorized claim cross into an action.

**Verification is priced by blast radius** on the frozen R×S matrix. A draft is checked cheaply; a payment is not. The hard gate sits on the **action commit path**, not token generation. Text streams optimistically behind a short hold-back buffer; the refund tool cannot commit while the gate holds it.

**One graph, three reads:** Performance reads forward (does each claim bind?), Cost reads backward (did each step ground any accepted claim?), Responsibility reads labels (is the caller entitled to every span a claim binds to, and does the action fall inside its typed interlock?).

**Frozen invariants (non-negotiable):**
- Default = UNSUPPORTED — every claim starts unproven and must earn SUPPORTED
- Entitlement = deterministic caller-vs-source-ACL set-membership, zero LLM, identity-carrying
- Exact R×S matrix — transcribed, never redrawn; 16 cells, 4 actuators (Block, Edit, Escalate, Pass/Pass+annotate)
- Hard gate on actions, not tokens — hold-back for text, commit boundary for tools
- Published FNR as a format — typed schema, null until earned, emptiness is the credibility play
- Two-pending-actions resolution — same response, R1 Edit on text + R3 Escalate on refund, simultaneously
- No LLM-as-judge on critical path — Action Interlock is a pure rule engine
- Bias = route-level async counterfactual measurement only, never per-response verdict

---

## 3. Target Users & Buyers

| Role | Who | Pain Felt | Decision Authority |
|------|-----|-----------|-------------------|
| **Economic Buyer** | VP Engineering / CTO / CISO | Liability from wrong AI actions (wrong refund, leaked PII, regulatory fine); wasted compute spend; audit failures | Signs contract, owns budget |
| **Technical Buyer** | ML Platform Lead / AI Infrastructure Engineer | Integration complexity; model-agnostic requirement; latency budget; needs proof before enforcement | Evaluates architecture, runs prototype, decides technical fit |
| **Day-to-Day Operator** | Platform Engineer / SRE / AI Safety Engineer | Alert fatigue from false positives; override workflows; policy change governance; on-call for runaway agents | Operates the plane, tunes per-route thresholds, reviews escalations |
| **Compliance / Risk** | DPO / Legal / Risk Officer | Regulatory evidence (GDPR, DPDPA, sector rules); audit trail completeness; data lineage | Mandates requirements, audits deployment |

**Key insight:** The economic buyer cares about *avoided wrong transactions* and *auditability*. The technical buyer cares about *integration surface* (SDK hook + reverse proxy, no model access). The operator cares about *not being woken up by false alarms*. The compliance officer cares about *evidence packets, not dashboards*.

---

## 4. Business Case & Impact Logic

Value is created along four measurable dimensions. No fabricated ROI percentages — directional, defensible logic only.

### A. Avoided Wrong Actions (Liability Reduction)
- **Logic:** Every R2/R3 action that passes through ControlPlane must earn proof. An unsupported categorical claim at R3 → Escalate (held). An entitlement violation at R1 → Edit (stripped).
- **Impact:** The plane stops the specific failure mode the brief names: *confidently wrong output executing an irreversible action*. The running example (₹1,84,000 refund under non-existent clause 7.2) is held with evidence packet. The company does not wrongly pay out.
- **Measurement:** Escalation rate on R3 actions; evidence packet review outcomes; override rate on Escalate (should be low if plane is precise).

### B. Reduced Dead Compute (Direct Cost Savings)
- **Logic:** Walk the graph backward: every STEP grounding zero accepted claims in the final answer is dead compute. No competitor has this number because no competitor has the graph.
- **Impact:** Identifies retrieval calls, tool calls, model turns that contributed nothing to the accepted answer. On typical agent traces, 30–50% of steps ground zero claims.
- **Measurement:** Dead-compute ratio per route (steps grounding zero accepted claims / total steps); estimated wasted tokens/cost per route. This is the number a buyer signs a cheque against.

### C. Reduced Alert Fatigue (Adoption Sustainability)
- **Logic:** R0/R1 traffic (80–90% of volume) passes with annotation, not blocking. Matrix graduates intervention by blast radius. Enforcement is *earned* per route through shadow evidence ("would have held N, of which M were true positives").
- **Impact:** Operators are not asked to trust the system before it produces its own counterfactual. Over-blocking — the reason every guardrail gets disabled — is prevented by the matrix design.
- **Measurement:** Override rate per route per actuator; alert fatigue indicator (flagged/escalated decisions / total decisions); auto-rollback trigger rate.

### D. Auditability & Regulatory Posture (Compliance Leverage)
- **Logic:** Every decision writes to append-only, hash-chained ledger: principal, evidence fragment, claim verdict, matrix cell, actuator, policy version, verifier versions, latency. An auditor reconstructs any actuator from ledger + policy version + frozen matrix.
- **Impact:** Meets "explainable AI decision" requirements in financial services, insurance, healthcare regulations. Evidence packet is the deliverable — not a log dump.
- **Measurement:** Ledger completeness; policy version traceability; time to reconstruct a decision for audit.

---

## 5. Phased Roadmap

Each phase states what is **earned**, not switched on.

| Phase | Scope | Entry Criteria (Earned) | Exit Criteria |
|-------|-------|-------------------------|---------------|
| **Phase 0: Prototype Validation** (Weeks 1–2) | Stage 3 prototype on synthetic corpora: refund dual-action + knowledge principal-flip | R2S3 built, all 15 binary criteria pass, demo ≤8 min | Judge can trace action → claim → span → principal; all fidelity invariants hold |
| **Phase 1: Shadow Deployment — Single Route** (Weeks 3–6) | One production route (e.g., internal knowledge assistant) in shadow mode on live traffic | Prototype validated; route policy configured; synthetic ACLs replaced with real IAM connector | Shadow counterfactual: "would have held N, M true positives" measured over ≥1000 traces; FNR schema populated with prototype_corpus status; override rate <3× baseline |
| **Phase 2: Canary Enforcement — Single Route** (Weeks 7–10) | Same route, canary enforcement (5% traffic) | Phase 1 shadow evidence meets earn-out: FNR CI width ≤0.05, sample ≥500, override rate within bounds | Canary runs 24h+ without auto-rollback; human-override rate stable; latency p50/p95 within budget |
| **Phase 3: Full Enforcement — Single Route** (Weeks 11–14) | Route at 100% enforcement | Phase 2 canary promoted; policy version signed off | Route in production; per-route FNR measured with production_measured status; dead-compute reporting active |
| **Phase 4: Multi-Route Expansion** (Months 4–6) | Add refund route (R1+R3), decision-support route (R2/R3 + async bias) | Each new route repeats Phases 1–3 earn-out independently; route configuration via RoutePolicy object | 3+ routes enforced; geography/regulatory overlays active; circuit breakers calibrated |
| **Phase 5: Enterprise Operating Envelope** (Months 6–12) | Full governance: policy DAG versioning, shadow replay pipeline, auto-rollback, cost optimization, bias measurement program | All routes enforced; operational metrics stable | Policy change lifecycle operational; stratified shadow audit continuous; buyer can stress-test impact logic |

**No phase auto-promotes.** Enforcement is earned per route via evidence. The plane is never "switched on" globally.

---

## 6. Key Risks & Mitigations

### Technical Risks

| Risk | Source | Exact Mitigation (from freeze) |
|------|--------|--------------------------------|
| **False assurance on derived/multi-hop claims** | NLI entailment weakest on synthesized claims; shallow span match marks SUPPORTED | Derived claims bypass NLI → recompute from spans or return UNKNOWN; UNKNOWN never → SUPPORTED; verifier model family decorrelated from generator; FNR stratified by claim type publishes residual misses |
| **Poisoned/wrong source evidence or missing upstream ACLs** | ControlPlane proves claim↔captured-evidence, enforces carried ACLs; does not prove source truth or repair IAM | Immutable source_id + content hash on every binding; missing ACL = unentitled on privileged routes; entitlement-violation rate per source = operational detector for over-permissioned indexes; quarantine/de-rank via policy version |
| **Operational tuning → alert fatigue or liability** | Over-flag → bypass; under-flag → liability; R mis-mapping payment to low R applies wrong matrix row | Shadow default before enforcement; blast-radius-priced verification depth; R0/R1 fail-open with annotation; R2/R3 fail-closed/escalate; locked action classes → R3 at parse time; auto-rollback on override rate >3× baseline; circuit breaker downgrades autonomy; hard interlock in action executor |

### Operational Risks

| Risk | Source | Exact Mitigation |
|------|--------|------------------|
| **Integration friction** | Buyer discovers integration cost after "drop-in" claim | We state integration cost upfront: one SDK hook at context assembly + OpenAI-compatible proxy. Days, not quarters. The integration cost *is* the moat — provenance capture outside the model is why the design works. |
| **Cold-start routes** | New routes lack baselines, FNR, calibration | Exclude cold-start from cost baselines; default to Pass+annotate for R0/R1; shadow mode mandatory; rapid calibration via canary; per-route enforcement earn-out |
| **Policy drift / misconfiguration** | Route maps payment to R1; threshold changes loosen matrix | Parse-time rejection of locked action class mis-mapping; policy validation pipeline (shadow replay → canary → auto-rollback); immutable policy versions; audit trail on every change |

### Adoption Risks

| Risk | Source | Exact Mitigation |
|------|--------|------------------|
| **Team disables it in a quarter** (like every guardrail) | Over-blocking creates friction; no trust before evidence | Hard gate on actions only; R0/R1 passes with annotation; enforcement earned per route via shadow counterfactual; override rate monitored, auto-rollback at 3× baseline |
| **Buyer demands "99% accuracy" single number** | Composite score expectation from market | We refuse to claim it. We publish per-route FNR as a format with CI. The empty schema *is* the credibility play. A judge who tests it finds honesty, not a bluff. |
| **Pattern-matched as "another RAG checker"** | Demo opens on risk vocabulary; looks like safety dashboard | Demo opens on held ₹1,84,000 refund (transaction, not risk). Vocabulary: authorise, admit, prove, bind, refuse, hold, escalate, gate — never monitor, detect, observe, watch, guard, trust score, risk score, "responsible AI" as standalone virtue. Evidence Ledger ≥60% screen. |

---

## 7. Differentiation Anchor

The 3–5 sharpest points that separate ControlPlane from every other category entrant:

| # | Differentiation | Why It Holds |
|---|-----------------|--------------|
| **1** | **Provenance captured outside the model** — the model cannot author, alter, or self-report its own evidence. Entitlement check carries caller identity into verification layer. | Structurally impossible for any output-only competitor (LLM-as-judge, guardrails, groundedness checkers) to replicate. They inspect text; we inspect the context contract. |
| **2** | **Default = UNSUPPORTED** — burden of proof inverted. A claim must earn SUPPORTED via binding/recomputation against captured provenance. Absence of proof ≠ low confidence ≠ implicit allow. | Confidence thresholding fails by definition (confidently wrong). LLM-as-judge inherits same calibration failure. Groundedness checkers average and allow unproven claims through. |
| **3** | **Blast-radius-priced action gate** — identical verdict produces different actuators depending on what the response is about to do (R1→Edit, R3→Escalate). Hard gate on commit path, not tokens. | Composite risk scores, confidence thresholds, and groundedness scores are action-blind. They cannot differentiate draft vs. payment. |
| **4** | **Published per-route false-negative rate** — we report what we *missed*, not what we caught. Typed schema, null until earned, CI when measured. | Every competitor publishes precision (rate they bother the user). None publishes miss rate. The format itself is the claim: we know exactly which fields are knowable at design time. |
| **5** | **One graph, three reads** — Performance, Cost, Responsibility are three reads of `STEP→SPAN→CLAIM→ACTION`, not three separate detectors. Dead compute computed exactly by walking the graph backward. | Competitors bolt three tools together. They measure spend, not waste. They cannot price verification by blast radius because they don't have the graph. |

---

## 8. Fidelity Self-Check

**Explicit confirmation:** Nothing in this business proposal:

- ❌ Softens Default = UNSUPPORTED — claims must earn SUPPORTED; absence of proof is not low confidence
- ❌ Weakens entitlement — deterministic caller-vs-source-ACL set-membership, zero LLM, identity-carrying, always on
- ❌ Redraws the matrix — 16 cells, 4 actuators, axis labels and column vocabulary load-bearing, transcribed never redrawn
- ❌ Moves the hard gate from actions to tokens — hold-back for text, commit boundary for tools/actions
- ❌ Claims the system eliminates hallucinations / bias / privacy risk — refuse-to-claim list is about *us*, not competitors
- ❌ Introduces LLM-as-judge or confidence scores as primary mechanism — Action Interlock is pure rule engine; NLI is entailment classifier producing verdict, not judge producing opinion
- ❌ Treats bias as a live per-response verdict — bias is route-level async counterfactual flip-rate with CI, off critical path, proposal-only for Stage 1/3

**Vocabulary discipline enforced:** authorise · admit · prove · bind · refuse · hold · escalate · gate. Never: monitor · detect · observe · watch · guard · trust score · risk score · "responsible AI" as standalone virtue.

**Content laws preserved:**
- Clause 7.2 does not exist — absence of evidence, not contradiction
- Never say "blocked" about the refund — held and escalated with evidence packet
- Company wrongly pays out if ungated — customer did not lose money
- Latency: ≤40 ms p50 / ≤200 ms p95 added on R0/R1 text; never quote 40 ms as p95
- Refuse-to-claim list is about *us* (no "eliminate hallucinations," "zero integration," "zero added latency," "one accuracy number across three failure modes")

---

*End of Stage 4 Business Proposal Spine. Stages 1–3 frozen invariants fully preserved. No competing mechanism introduced. Ready for pitch alignment.*