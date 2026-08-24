# hy3

Model: `opencode/hy3-free`

Stage 4 — Business Proposal Spine
Accenture Innovation Challenge 2026 · Round 2

---

# ControlPlane.ai — Round 2 Stage 4: Business Proposal Spine (Frozen-aligned)

> Sources of truth (absolute): `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` · `R2S2.md` · `R2S3.md`
> Stages 1–3 are non-negotiable. This document does not reopen the prototype boundary, the dual-action resolution, the matrix, the entitlement check, or any fidelity invariant. It renders the frozen admission primitive as a business case.

---

## 1. Problem Framing

The cost of a wrong AI output **changed category**. It used to be a bad paragraph; it is now an **executed transaction**. The decisive failure the freeze addresses is not "toxicity," not "low confidence," not "a risky response" — it is an *unsupported categorical claim bound to an action*.

The running example is the only one that matters:

> *"Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement."*

**Clause 7.2 does not exist.** The failure is *absence of evidence*, not conflicting evidence. Every ordinary filter passed it. Confidence read 0.94. Money moved Tuesday, found Friday. If ungated, **the company wrongly pays out ₹1,84,000** — the customer did not lose money.

The indictment that follows is not rhetoric; it is the architecture's premise: *the system didn't fail. It was never asked to prove anything.*

**Why existing approaches fail against this specific failure mode:**

- **LLM-as-judge** (NeMo Guardrails, most "AI safety" wrappers) asks *"does this look right?"* — an unfalsifiable question, using the same reasoning that produced the error, from the same family of blind spots, usually without the source documents and always without knowing who was asking. Too slow to stand in front of an action. *We ask "which span proves it?" — a query with an answer.*
- **Static guardrails** (LlamaGuard, deny-lists) match banned surface forms. A fabricated clause number is lexically clean, so they see nothing — and they are **identity-blind**: the same string is fine for one caller and a breach for another. Deterministic entitlement is a different question, not a better classifier.
- **RAG groundedness checkers** see retrieval only, **average** over claims (one wrong figure drowns in nine correct sentences), and are **action-blind** (0.82 means the same on a draft and on a wire transfer). *Retrieval is not permission.*
- **Post-hoc observability** (LangSmith, Arize, et al.) tells you what went wrong *after a user acted on it* — the precise thing the brief asks to eliminate. Beautiful dashboards, wrong product. They also measure spend, not waste: a trace can cost ₹8 while ₹5 of it grounded nothing.
- **Confidence thresholding** fails by definition: the named failure mode is *confidently* wrong. You cannot detect a calibration failure with the calibration.
- **Composite risk scores** collapse three incommensurable failure modes into one number that maps to no intervention. *You cannot block, edit or escalate on 87.*

The load-bearing line that separates ControlPlane from all six: *everyone watches the exit. Nobody records the entrance.* The entrance is the evidence assembled **before** the model ran — and that record is thrown away the moment generation starts. That is the record ControlPlane keeps.

---

## 2. Solution Design Summary

ControlPlane is an **admission-control layer** at the action commit boundary. It treats every AI response as a set of **claims requesting permission to act**, not text to be scored. The design is tied to the frozen architecture on six load-bearing points:

1. **Provenance captured outside the model.** The Provenance Recorder (the keystone — *if exactly one thing gets built, build this*) hooks context assembly and writes every span with `source_id · ACL · content_hash · offsets` plus the calling principal, **before** any claim is judged. The model has no write path to provenance. This is what makes entitlement possible and what turns hallucination detection from a judgment call into a **set-membership test**.
2. **Default = UNSUPPORTED.** Every check-worthy claim is born unsupported and must *earn* `SUPPORTED` by binding to a captured span or by deterministic recomputation. `UNKNOWN` never collapses into `SUPPORTED`. *Not low confidence. Unproven.*
3. **Entitlement as deterministic set-membership.** The Entitlement Auditor compares caller clearance against the source ACL bound to each span — `span.acl ⊆ principal.clearance` — on Lane 1, **zero LLM**, always on, cannot be disabled. It is independent of semantic correctness: a correct answer on an unauthorized span is still a violation.
4. **One graph, three reads.** `STEP → SPAN → CLAIM → ACTION` is the single structure. Performance reads it forward (does each claim bind?), cost reads it backward (did each step ground an accepted claim?), responsibility reads its labels (is the caller entitled, does the action fall inside its typed interlock?). Not three detectors — three questions on one graph.
5. **Blast-radius pricing.** `R = irreversibility × audience × data class × autonomy` (R0 internal draft → R3 irreversible/regulated). Verification budget follows consequence: R0/R1 is 80–90% of volume and gets the deterministic Lane 1 only; a payment gets the expensive binding. The identical verdict annotates a draft and holds a payment. *Proof scales with consequence.*
6. **Hard gate on actions, not tokens.** The matrix cell `f(R, S)` is computed and highlighted **before** the actuator fires. The action executor honors the interlock; text streams optimistically behind a ~150–300 ms hold-back so users perceive the model's speed while harm lives in the commit path. Decision time is a **pure rule engine — zero LLM reasoning**. Latency added is **≤40 ms p50 / ≤200 ms p95** (never quote 40 ms as p95); action gating is amortized inside the tool round-trip, so it is invisible.

The centrepiece is the **two-pending-actions resolution** on the refund trace: the customer-visible text → R1 × entitlement → **Edit** (stripped), while the refund → R3 × unsupported-categorical → **Escalate** (held with the evidence packet). Both are correct simultaneously; nothing is collapsed into one response-level verdict. The refund is **never "blocked"** — it is *held and escalated with the evidence packet*.

---

## 3. Target Users & Buyers

The pain, the signature, and the operation are held by three different roles — and conflating them is how generic pitches lose the room.

- **Economic buyer — who feels the pain.** CFO, Chief Risk Officer, or Head of Compliance at a regulated enterprise where AI touches money or regulated actions: banking, insurance, payments, telecom, public sector. This person is **liable for the executed transaction** — the wrongly authorized payout, the over-permissioned index leaking HR data to the wrong employee, the regulated-advice failure. They do not run the stack; they sign for the consequence.

- **Technical buyer — who signs the build.** VP Engineering, ML Platform lead, or Chief Architect who must deploy AI agents without becoming the party that *authorized an unsupported action*. They own the integration (one SDK hook at context assembly + an OpenAI-compatible reverse proxy — no model access, no weights, no application rewrite) and the versioned policy DAG. They are the ones who will be asked, post-incident, "did your system let an unproven claim cross into an action?"

- **Day-to-day operator — who runs it.** Two distinct actors: (a) the agent/runtime that calls ControlPlane on every action — it is an API-layer interceptor, so adoption is a hook, not a rewrite; and (b) the human reviewer who sees **Escalate evidence packets** (claim, candidate spans, verdict, diff) and decides whether to release a held action. The operator is not the economic buyer and is not the technical buyer.

The differentiation point for the room: the person who **pays when it fails** (economic buyer) is structurally separated from the person who **runs it daily** (operator). ControlPlane is sold to the former on avoided executed-error, and adopted by the latter because the gate sits on actions, not on their text.

---

## 4. Business Case & Impact Logic

No fabricated ROI percentages. The value is stated as **mechanism → consequence**, in a form a sceptical buyer can stress-test.

- **Avoided wrong actions (primary).** The gate deterministically prevents an unsupported or unentitled claim from authorizing a transaction. Value = avoided cost of the specific wrong action × its frequency on in-scope routes. We do not claim a catch-rate percentage up front; we claim a **mechanism that intercepts the class by construction**, and we publish our own false-negative rate so the buyer sizes the residual themselves. The escape is structural, not statistical: an unsupported categorical on an R3 action routes to Escalate and the mock executor refuses to commit (`executed:false`).

- **Reduced dead compute (the defensible number).** Dead compute is computed **exactly, with no model and no estimation**, by walking the graph backward: any step grounding zero accepted claims is waste. The honest claim is the one ARCHITECTURE makes — a trace costing ₹8 where ₹5 grounded nothing. That is the number a buyer signs a cheque against, because it needs no benchmark we haven't run.

- **Reduced alert fatigue (the adoption number).** Competitors emit a "risky" flag and a dashboard; reviewers learn to ignore both. ControlPlane ships an **evidence packet** and a **proportionate actuator** (Edit on a draft, Escalate on a payment), and it tracks the override/flagged ratio to recalibrate. Because over-blocking is the historical reason guardrails get switched off, the matrix exists specifically to prevent it — so reviewers trust the escalations instead of bypassing them.

- **Auditability (the regulator number).** Every decision writes to an append-only, hash-chained ledger carrying `principal · evidence fragment · claim verdict · matrix cell · actuator · policy_version · verifier_versions · latency`. Any actuator is reconstructable from ledger + policy version + the frozen matrix. This is the instrument an internal audit and a regulator respect, and it is why the product is infrastructure, not an ethics wrapper.

- **The credibility play (the close).** We publish what we **miss**, per route, with confidence intervals — not what we caught. *"On this route we catch \<measured\>% of ungrounded claims at 40 ms p50 — and here is the \<measured\>% we don't."* The emptiness of the schema at demo time is the claim: we know exactly which fields are knowable at design time and which are not. A judge who tests it finds honesty, not a bluff.

---

## 5. Phased Roadmap (earned, not switched on)

The governing principle from the frozen envelope: **nothing enforces on day one; enforcement is earned per route from counterfactual evidence.** Determinism works from the first request; the statistical parts earn their thresholds.

**Phase 0 — Prototype (Stage 3, complete).**
Dual-action refund (R1 Edit + R3 Escalate) plus the principal-flip entitlement replay on one `STEP → SPAN → CLAIM → ACTION` ledger. *Earned:* proof that the admission primitive works and that an unproven claim cannot authorize an action — demonstrated against all 25 success criteria, not a slide.

**Phase 1 — Limited production routes.**
Turn on for 1–2 high-consequence routes only: refund release (R3) and external PII send (R2). Routes start in **shadow** (the default deployment shape) — dual-emit gated-vs-ungated, producing the counterfactual *"would have held N, of which M were true positives."* *Earned before enforce:* a populated FNR stratum **only after** minimum sample (≥500 per stratum, CI width ≤ 0.05); until then `measurement_status = insufficient_sample` / null — never a fabricated percentage. Canary dual-emit on a bounded slice; auto-rollback if human-override rate exceeds 3× baseline. No global "enable enforcement" switch.

**Phase 2 — Broader enterprise rollout.**
Add the decision-support route (bias remains **async route-level counterfactual flip-rate + CI**, never a live per-response verdict), governance overlays (geo/industry **additive only** — they cannot loosen matrix cells or remove ACL), the policy lifecycle (shadow replay → canary → named-principal approval → gradual promote), multi-tenant operation, and the circuit breaker. *Earned:* enforcement only after a minimum shadow window **and** sufficient FNR sample **and** override rate within bounds. Human override (approving a held action) is always permitted; Block-overrides require higher authority than Edit-overrides. The plane fails per blast-radius tier, never globally (R0/R1 fail open with annotation; R2/R3 fail closed or escalate) — so a single point of failure cannot disable the whole product.

Each phase is defined by what is **earned** (evidence, sample, override rate) rather than what is **switched on** (a config flag). That asymmetry is the deployment story a serious evaluator trusts.

---

## 6. Key Risks & Mitigations

**Technical risks**

- **False assurance on derived / multi-hop claims** (the architecture's named strongest residual risk). Shallow entailment can mark a synthesized claim `SUPPORTED`. Mitigation: derived/aggregative claims are routed *away from NLI entirely* → recomputed from spans or returned `UNKNOWN`; `UNKNOWN` never becomes `SUPPORTED`; verifiers are from a different model family than the generator (decorrelation by construction); FNR is stratified by claim type so residual misses are visible, not hidden.

- **Poisoned or wrong source evidence, or over-permissioned upstream IAM.** ControlPlane proves `claim ↔ captured evidence` and enforces **carried** ACLs; it does not prove the source is true and does not repair IAM. Mitigation: immutable `source_id` + content hash on every accepted binding; a missing ACL is recorded as a gap and treated as unentitled on privileged routes; the per-source entitlement-violation rate is itself the detector for an over-permissioned index (visible and measurable, not silently "fixed"). The honest boundary is stated out loud: *we defend the claim-to-evidence link, not the truth of the evidence.*

- **Prompt injection.** The binding is computed by us, not asserted by the model — the generator has no channel to declare a binding edge. Injection can change what the model *says*, not which spans were captured, nor the entailment verdict, nor the ACL. The one working attack (poison a source document) becomes a supply-chain problem on the corpus, and the source ID + content hash make it forensically traceable.

**Operational risks**

- **Alert fatigue / over-flag (the historical killer of guardrails).** Shadow earn-out before enforce; blast-radius-priced verification depth (R0/R1 mostly Lane 1); per-tier fail stance; locked R3 action classes at parse time; no policy ships without replay + canary; auto-rollback on override > 3× baseline; override-rate trend surfaced to operators. Over-blocking is prevented by design because the matrix prices the actuator to the consequence.

- **Plane downtime.** Fail stance is declared per blast-radius tier, not globally. R0/R1 fail open with annotation; R2/R3 fail closed or escalate. The plane is never a single point of failure for the whole product — only for dangerous actions.

**Adoption risks**

- **Switch-off after a quarter.** The hard gate sits on actions; R0/R1 — the overwhelming majority of volume — passes with annotation and never touches the operator's text. Enforcement is earned via shadow evidence, so nobody is asked to trust it before it has produced its own counterfactual. This directly answers "why won't they just turn it off like every other guardrail?"

- **Integration cost mis-sold.** We state the integration cost **out loud** as the moat: one SDK hook where context is already assembled, plus an OpenAI-compatible proxy — days, not quarters, on a standard retrieval stack. Trading this for a "zero-integration drop-in" claim is the bad trade that makes teams churn when they discover the cost later. The integration cost *is* the reason the design works.

---

## 7. Differentiation Anchor

The five sharpest points, each consistent with `NARRATIVE.md` and `QA.md`:

1. **Set-membership, not scoring.** Everyone else inspects the *output*. We keep the *receipts* — evidence captured outside the model, before it ran, with source identity and access rights attached. The verdict is a binding that either exists or doesn't. *They ask "does this look right?" We ask "which span proves it?"*

2. **Default = UNSUPPORTED — the burden of proof is on the claim.** Monitor-and-alert tools default to allow and flag exceptions. We invert it: nothing passes because nobody objected. A claim must earn `SUPPORTED`. This is a posture change, not a threshold tweak.

3. **Hard gate on actions, not tokens; blast-radius × verdict severity.** The identical verdict annotates a draft and holds a payment. They gate on words; we gate on the commit path. *Retrieval is not permission.* This is why we stay fast: the expensive verification is precomputed by construction and spent only where harm lives.

4. **Identity inside the verification layer.** Entitlement is deterministic caller-vs-span-ACL, zero LLM, on the critical path. This catches the most common real enterprise incident — an over-permissioned RAG index faithfully leaking HR data to the wrong employee — and **no LLM-judge wrapper catches it, because none of them carry identity into the verification layer.** It is the single most differentiated mechanism in the architecture.

5. **We publish what we miss, and we refuse to claim we eliminate the problem.** Per-route FNR with confidence intervals, empty until earned. And we explicitly do **not** claim to eliminate hallucinations, bias, or privacy risk — we claim ungrounded claims cannot authorize actions, and we report what we miss. Every deck in the room disclaims its rivals; almost none disclaim themselves. That honesty is the credibility play, and it is what none of the six competitor classes do.

---

## 8. Fidelity Self-Check

Explicit confirmation that nothing in this business proposal:

- **Softens Default = UNSUPPORTED** — preserved: claims must earn `SUPPORTED`; absence of proof is *unproven*, not "low confidence" and not implicit allow.
- **Weakens entitlement** — preserved: deterministic set-membership (`span.acl ⊆ principal.clearance`), zero LLM, always on, cannot be disabled; independent of semantic correctness.
- **Redraws the matrix** — preserved: the exact 16-cell `R × S` table is transcribed, never redrawn; no route parameter; axis labels, column vocabulary, and cell values are load-bearing.
- **Moves the hard gate from actions to tokens** — preserved: the matrix cell is computed and shown before the actuator; the action executor honors the interlock; text streams behind hold-back.
- **Claims the system eliminates hallucinations / bias / privacy risk** — explicitly disclaimed: we claim ungrounded claims cannot authorize actions and we report our own miss rate. Bias is kept (the brief requires it) as **route-level async counterfactual flip-rate + CI**, never a live per-response verdict.
- **Introduces LLM-as-judge or confidence scores as the primary mechanism** — rejected: decision time is a pure rule engine, zero LLM reasoning; no composite risk/confidence score drives disposition.
- **Treats bias as a live per-response verdict** — never: bias is a distributional property measured asynchronously at route level, or it is nothing.

**Vocabulary discipline honored:** authorise · admit · prove · bind · refuse · hold · escalate · gate — never monitor · detect · observe · watch · guard · trust score · risk score · "responsible AI" as a standalone virtue. The refund is **held and escalated with the evidence packet**, never "blocked." Latency is quoted only as **≤40 ms p50 / ≤200 ms p95**, never 40 ms as p95. The FNR ships as an **empty typed schema**; no fabricated production percentages appear anywhere.

This proposal renders the frozen architecture as a business case. It does not broaden Stage 1, reopen Stage 2, or introduce a competing mechanism. It makes the admission primitive feel inevitable, not optional.

---

*End of Round 2 Stage 4 — Business Proposal Spine. Stages 1–3 freeze fully preserved.*
