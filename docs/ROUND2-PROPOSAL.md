# ControlPlane.ai — Round 2 Detailed Business Proposal

**Accenture Innovation Challenge 2026 · Problem Track 1 · Team ControlPlane**  
Choda Srujan Sai · Dhrithika — IIT Gandhinagar

> Companion to the frozen system of record: [ARCHITECTURE.md](ARCHITECTURE.md).  
> Positioning: [NARRATIVE.md](NARRATIVE.md). Hostile Q&A: [QA.md](QA.md).  
> Prototype: `python3 examples/refund_trace_demo.py` and `python3 examples/multi_usecase_demo.py`.

This document is the Round 2 business proposal. It cites the architecture; it does not reopen it.

---

## 1. Problem framing

An AI response is not text to be scored — it is a set of **claims requesting permission to act**.

Enterprises no longer run one assistant. They run three at once: a customer-facing support chatbot, an internal knowledge copilot, and a decision-support agent that can refund, file, send, or write to production. Each has a different blast radius, a different latency budget, and a different owner. Oversight tooling is still built for the answering era: score the finished paragraph, chart the failure, review the log next week.

That category error now has a rupee figure attached.

A refund agent emits: *“Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.”* Every filter passes it. Confidence 0.94. Money moves Tuesday, found Friday. **Clause 7.2 does not exist.** The company wrongly pays out ₹1,84,000. The system did not fail a classifier. **It was never asked to prove anything.**

The cost of a wrong output changed category: it used to be a bad paragraph. It is now an executed transaction.

Three things make this hard in a real enterprise, and they are the same three the Round 2 brief names:

1. **One-size-fits-all checking fails.** A hedged warranty guess on a support reply is not the same object as an ungrounded clause authorizing a payment. Treating them as one “risk score” either over-flags the first (alert fatigue, the plane gets switched off) or under-flags the second (liability).
2. **There is often no ground truth at decision time.** The knowledge gap that caused the hallucination is the same gap a checker would need. If the plane requires a labelled gold answer, it cannot stand in front of an action.
3. **The model is consumed via API.** There are no weights, no logits, no hidden states to inspect. Anything that needs model internals is a paper design.

ControlPlane is an **admission-control layer**. It captures the evidence the model was actually given *before generation*, binds each claim in the output back to a span of that evidence, and refuses to let an unproven claim cross into an action. Verification effort is priced by blast radius: a draft is checked cheaply, a payment is not.

We do not claim to eliminate hallucinations. We claim that ungrounded claims cannot authorise actions, and we report what we miss.

---

## 2. Solution design

### 2.1 One graph, three axes

Everything downstream reads a single structure, assembled *while* the response is produced rather than reconstructed afterwards ([ARCHITECTURE.md](ARCHITECTURE.md) §2):

```
  STEP ──produces──▶ SPAN ──binds──▶ CLAIM ──authorizes──▶ ACTION
 (tool call,       (retrieved chunk,   (typed atomic      (pending side
  retrieval,        tool row, DB        proposition        effect: tool +
  model turn)       record — with       from the output     args +
                    source_id, ACL,     stream)             irreversibility)
                    hash, offsets)
```

- **Performance reads it forward** — does each claim bind to a span?
- **Cost reads it backward** — did each step produce a span that grounded any accepted claim?
- **Responsibility reads its labels** — is the caller entitled to every span a claim binds to, and does the action fall inside its typed interlock?

One structure, three axes, three actuators. That is why this is a control plane and not three classifiers in a trench coat.

The verdict is a **set-membership test** against receipts captured outside the model — not an opinion about finished text. Default verdict is **UNSUPPORTED**. A claim must earn SUPPORTED. `UNKNOWN` is a first-class verdict that *routes*; it never collapses into SUPPORTED.

### 2.2 The keystone: Provenance Recorder

If exactly one thing gets built, build the Provenance Recorder ([ARCHITECTURE.md](ARCHITECTURE.md) §2, §12). It hooks **context assembly**, not the model. Every span is captured with `source_id`, ACL, content hash and offsets. Context then freezes: the model cannot invent a span after the fact, and it has no channel to declare a binding.

Every other mechanism degrades to a generic guardrail without this hook. Model-emitted citations are rejected for the same reason: a model that fabricates a fact fabricates the citation with equal fluency ([ARCHITECTURE.md](ARCHITECTURE.md) §8).

The Round 2 prototype *is* this keystone, plus the three reads that become possible once it exists: deterministic binding, entitlement as ACL set-membership, and the Action Interlock on the frozen blast-radius matrix. See [Appendix A](#appendix-a--prototype-evidence).

### 2.3 Decision policy — transcribed, never redrawn

Two inputs govern every decision: **blast radius R** (what this response can break) and **verdict severity S** (what the evidence says).

**R = irreversibility × audience × data class × autonomy level**

| Tier | Meaning |
|---|---|
| **R0** | internal draft, a human reads it first |
| **R1** | user-visible, read-only |
| **R2** | reversible write / external send |
| **R3** | irreversible or regulated — payment, deletion, publication, regulated advice |

|  | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** | **Block** | Escalate | Escalate | Escalate |
| **R2** | **Block** | Edit | Edit | Escalate |
| **R1** | Edit | Edit | Pass + annotate | Pass + annotate |
| **R0** | Pass + annotate | Pass + annotate | Pass | Pass |

**The verdict is hostile; the action is proportionate.** A claim must earn SUPPORTED, but merely failing to earn it only blocks where the blast radius justifies blocking. That is the over/under-flag tradeoff, encoded rather than “tuned away.”

Actuators are exactly **Block · Edit · Escalate · Pass** (plus autonomy downgrade and circuit breaker, spoken not drawn):

- **Edit is surgical, never generative.** Strip the unsupported or unentitled claim. Free-form rewriting produces a new unverified artifact.
- **Escalate ships an evidence packet, not an alert:** the claim, the candidate spans, the verdict, the diff.
- Fail stance belongs to the **tier**, not a global default: R0/R1 fail open with annotation; R2/R3 fail closed or escalate. A universal fail-open makes the plane bypassable by anyone who can induce load.

User surface: three states — **Verified / Uncertain / Blocked** — one claim-level line each. No raw scores.

### 2.4 Latency and deployment shape

The expensive part is precomputed: provenance is indexed at context-assembly time, so binding is a lookup against a small in-memory set, not a search over a corpus.

- Hard gate sits on **actions**, not tokens. Users perceive speed from text; harm lives in the commit path.
- Three lanes. Lane 1 — inline, deterministic only (span membership, ACL, typed interlocks, arithmetic). Lane 2 — NLI binding for flagged claims and high-R traffic. Lane 3 — async (semantic-entropy, counterfactual bias replay, shadow audit).
- **Budget follows blast radius.** R0/R1 is 80–90% of volume and gets Lane 1 only.
- Targets: **≤40 ms p50 and ≤200 ms p95** added on R0/R1 text. Never quote 40 ms as p95.
- Deployment: an **OpenAI-compatible reverse proxy** plus a thin context-assembly SDK hook. No application rewrite, no model access, no weights, no logits, no fine-tuning. Integration is real and is the moat — we say so.

The prototype implements Lane 1 of this design on fixtures (no LLM, no network). Lane 2/3 and the proxy are roadmap, not pretended.

### 2.5 Why the overlapping failures are not a category crisis

The brief notes that bias, hallucination and privacy often overlap — a fabricated detail about a person can be both a hallucination and a privacy concern. We do not collapse them into one classifier. They have different mathematics, error costs and owners, and they land as **different labels on the same graph**:

| Apparent mix | What the graph actually says | Who acts |
|---|---|---|
| Fabricated personal detail (no span) | Performance: UNSUPPORTED. Leakage: PII-shaped entity binding to **no span** = model-memory leak → **Block** | Entitlement Auditor + Interlock |
| True HR fact from an over-permissioned index | Performance: SUPPORTED (it *is* in the evidence). Responsibility: span ACL excludes the caller → entitlement violation → **Block** on R2/R3, **Edit** on R1 | Entitlement Auditor — structurally impossible for any output-only checker |
| Decision-shaped output that flips when a protected attribute is perturbed | **Not a per-response property.** Bias = counterfactual invariance, route-level, async: decision flip rate with a confidence interval over a rolling window. Flag when the CI excludes zero. | Adjudicator (Lane 3) |

Do not drop bias. State it in measurement terms, never moral ones.

### 2.6 What we refuse to claim

About ourselves, not competitors ([NARRATIVE.md](NARRATIVE.md) §5):

- We do **not** eliminate hallucinations.
- We do **not** claim zero integration or “drop it in.” We hook context assembly.
- We do **not** claim zero added latency. We never make the model feel slow; we make the action wait.
- We do **not** quote one accuracy number across performance, cost and responsibility.

---

## 3. Target users

One plane, three buyers. They share a ledger and disagree about which column they read.

| User | Reads | Job on the plane | What they will switch it off for |
|---|---|---|---|
| **Platform / SRE** | Cost axis + latency SLOs + circuit breaker | Own the reverse proxy and the SDK hook. Kill runaway loops (non-convergence breaker). Keep p50/p95 inside budget. Canary and auto-rollback threshold changes. | Added latency on R0/R1 text; a plane that is a single point of failure for the whole product |
| **Risk / compliance / audit** | Responsibility axis + append-only ledger | Entitlement (who was allowed to know); typed interlocks on irreversible actions; hash-chained evidence packet on every hold. Policy as a versioned DAG, not a slide. | A composite 0–100 score they cannot decompose; a miss they cannot explain to a regulator |
| **App owners** — support, copilot, agents | Performance axis + the matrix cell for *their* route | Support owner wants replies to stream. Copilot owner wants drafts edited, not blocked. Agent owner wants payments held until a claim binds. Enforcement is earned **per route** through shadow evidence. | Over-blocking of ordinary text; a global switch that treats a chatbot like a wire |

The same pending response can serve two of them at once. In the refund running example the customer-visible text is **Edited** (R1 × entitlement) while the refund is **held and escalated with the evidence packet** (R3 × unsupported-categorical). Both are correct simultaneously. Proof scales with consequence.

---

## 4. Business case & impact

Reference parameters from the Round 2 brief, adopted as directional assumptions (not a measured dataset):

| Parameter | Directional assumption |
|---|---|
| Weekly volume | **~40,000 interactions/week** across the three use cases combined (“tens of thousands”) |
| Mix | Support chatbot ~70% (R1, latency-sensitive); internal copilot ~25% (R1/R2); decision-support / acting agents ~5% (R2/R3) |
| Blast-radius volume | R0/R1 ≈ 80–90% of traffic → Lane 1 only ([ARCHITECTURE.md](ARCHITECTURE.md) §5) |
| Data | Mix of well-governed sources (ACL’d systems of record) and loosely governed ones (wikis, FAQs, pasted tickets) |
| Unit of irreversible harm | The running example: **₹1,84,000 wrongly paid** on an ungrounded clause |

We do **not** put a savings percentage, a catch rate, or a payback period on this page. Those numbers are knowable only on the buyer’s traffic, which is why the gate report ships as an **empty schema with typed placeholders** ([ARCHITECTURE.md](ARCHITECTURE.md) §10.7). What is knowable at design time is *which quantities the graph makes exact*.

### 4.1 Three quantities a buyer can cash

**Held irreversible actions.** R3 × unsupported-categorical does not “block the refund” as a slogan — it **holds and escalates with the evidence packet**. On ~2,000 decision-support interactions/week, even a thin tail of R3 attempts is a budget line: a single miss at the running-example amount is already material, and the plane’s job is to make that miss a held packet rather than a Tuesday payout found Friday. The prototype produces this actuator on the real matrix cell `R3 × Unsupported + categorical` (Appendix A).

**Entitlement incidents prevented.** The most common real enterprise incident is not a jailbreak. It is an over-permissioned RAG index faithfully leaking HR data to the wrong employee. Output-only wrappers cannot catch it: they never carry caller identity into verification. ControlPlane does — ACL set-membership, microseconds, near-zero FP. The prototype’s `hr_side` claim is this incident: span ACL `{hr-confidential}` vs caller clearance `{vendor-public}` → **Edit** on the R1 text path.

**Dead compute, named exactly.** Walk the graph backward: every SUPPORTED claim in the accepted answer points to a span, which points to the step that produced it. Any step grounding zero accepted claims is dead compute — no model, no estimation. In the refund fixture, five assembly steps run; `faq_search` and `crm_lookup` ground nothing. A dashboard can say the trace cost ₹8. Walking the graph can say ₹5 of it grounded nothing. We will measure that yield on their traffic in shadow; we will not invent the percentage here.

### 4.2 Why this is cheaper than the alternative at 40k/week

Uniform deep checking at this volume is how planes get disabled. Spending Lane 2/3 on 80–90% of R0/R1 traffic is wasted verification compute *and* alert fatigue. Pricing verification by blast radius is the cost model: the expensive work is reserved for the fraction that can move money or leak an ACL’d span. Shadow mode is the default deployment, so the first artefact a sceptical stakeholder receives is the counterfactual — *would have held N, of which M were true positives* — not a block.

Net of verification vs waste is also not a slide percentage ([QA.md](QA.md) D2). Day one we can name the spend that grounded nothing. Net savings is a Phase-0 output, not an input.

---

## 5. Phased roadmap

Enforcement is earned per route, never switched on globally. Shadow is the default ([ARCHITECTURE.md](ARCHITECTURE.md) §5.9).

### Phase 0 — Shadow (weeks 0–6)

- Deploy the OpenAI-compatible reverse proxy + context-assembly SDK hook on one support route and one acting route.
- Dual-emit: gated vs ungated. No user-facing hold.
- Every deterministic mechanism works from the first request: span membership, entitlement, arithmetic, typed interlocks ([QA.md](QA.md) C3).
- Output: the counterfactual *would have held N, of which M were true positives*, plus dead-compute named per trace.
- Capture a human-override baseline (needed later for the 3× auto-rollback rule).
- **Exit:** platform/SRE accepts p50/p95 on R0/R1; risk accepts the evidence-packet format.

### Phase 1 — Enforce R3 (weeks 6–12)

- Turn the matrix on for **R3 only**: payment, deletion, publication, regulated advice.
- Fail closed or escalate when evidence does not arrive in time.
- Co-pending R1 text on the same response still follows the matrix (the refund demo: Edit the customer-visible line, hold the payout).
- Surgical Edit only; no free-form rewrite.
- **Exit:** zero ungated R3 actions; override rate inside baseline; ledger verify_chain holds.

### Phase 2 — Enforce R2 (weeks 12–20)

- Reversible writes and external sends (the copilot “draft email to partner” class).
- Autonomy downgrade (act → propose) instead of blocking ordinary work.
- Per-route circuit breaker: when gate-fail rate exceeds budget, the route drops an autonomy tier until it recovers.
- Lane 2 NLI binding for textual claims on high-R traffic only.
- **Exit:** R2 Edit/Escalate cells match shadow predictions within the canary window.

### Phase 3 — Feedback loops and FNR publishing (from week 16, overlapping)

- Stratified shadow audit: **100% of holds and escalations** plus a random slice of passes, sampled to expensive ground truth.
- Publish the plane’s own **per-route false-negative rate** with confidence intervals — not what we caught, what we missed. Format below; values filled only with measurements.
- Every threshold change: shadow replay over the last N traces showing FP/FN delta; canary by route; **auto-rollback if human-override rate exceeds 3× baseline**.
- Override capture is the feedback loop the brief asks for: humans correct a packet, the correction is a labelled span, calibration moves, the DAG versions.
- Lane 3: semantic-entropy on ungrounded routes; counterfactual bias replay on decision-shaped routes.
- Geographic / sector policy packs land here as **content** on the versioned DAG, not as a rewrite of the engine.

### Gate report — empty schema (the credibility play)

```
route                <id>
window               <start>–<end>
volume               <n>
holds                <n>   escalations <n>   edits <n>   blocks <n>
shadow_would_have_held   <n>
true_positives_in_holds  <n>   (sampled)
false_negatives          <n>   (sampled passes that should have held)
FNR                      <measured>%  ± <CI>   per route
dead_compute_share       <measured>%  of steps grounding zero accepted claims
override_rate            <measured>   vs baseline <measured>
p50_added_ms             ≤40 (target)    p95_added_ms  ≤200 (target)
policy_version           <id>
```

The emptiness is the claim: we know which fields are knowable at design time and which are not.

### Explicitly later (not in this prototype)

Named so they are not pretended: OpenAI-compatible proxy in production form; streaming 1–3B claim extractor; NLI Prosecutor (~300M) for textual claims; Economist yield dashboard; Adjudicator/Red Team; full multi-turn session store; Aho-Corasick PII gazetteer; geographic policy packs. Spec follow-ons: [docs/superpowers/specs/2026-08-23-provenance-recorder-design.md](superpowers/specs/2026-08-23-provenance-recorder-design.md) §10.

---

## 6. Key risks & mitigations

Mapped to [ARCHITECTURE.md](ARCHITECTURE.md) §7–8. Residual risks we will say out loud; rejected approaches we will not re-import.

| Risk | Where | Mitigation |
|---|---|---|
| **False assurance on derived / multi-hop claims.** Entailment is weakest where the value is highest. A shallow span that “looks similar” marked SUPPORTED is **strictly worse than no control plane**, because humans stop checking. | §7 — strongest residual risk | Derived claims are **never** marked SUPPORTED by entailment. Arithmetic/aggregative → recompute from spans. Neither recomputable nor directly entailed → **UNKNOWN**. **UNKNOWN never collapses into SUPPORTED.** Verifiers from a different model family than the generator; deterministic checks carry majority enforcement weight. Publish per-route FNR. Prototype: `ClaimKind.DERIVED` binds to `UNKNOWN` (`tests/test_binder.py`). |
| **Alert fatigue / over-flag.** Over-flagging is how every guardrail gets switched off; under-flagging is liability. | §4 matrix; §8 composite score rejected | Hostile verdict, proportionate action. Identical UNSUPPORTED is Pass+annotate on R1-hedged and Escalate on R3-categorical (Appendix A). User surface is three states, never a 0–100 score. **You cannot block, edit or escalate on 87.** R0/R1 fail open with annotation so ordinary text is not held hostage. Shadow before enforce. |
| **API-only visibility.** No weights, logits, or hidden states. Purely parametric answers have nothing to bind to. | §5 deployment; §8 model-emitted citations rejected; [QA.md](QA.md) B1 | We work at the I/O layer by design: context-assembly hook + reverse proxy. Binding is undefined without an evidence set, and we do not pretend otherwise. Ungrounded routes are *declared* ungrounded; blast radius still applies — an ungrounded answer can annotate a draft but cannot authorise a payment. Async semantic-entropy is calibration, never the token stream. *We do not claim to verify what we were never given. We claim that what we were never given cannot authorise an action.* |
| **The plane is bypassed by load, or disabled by the team.** | §8 universal fail-open; [QA.md](QA.md) C4–C5 | Fail stance belongs to the tier. The plane is a single point of failure only for dangerous actions. Hard gate is on actions, not text; R0/R1 — the majority of volume — pass with annotation. Enforcement earned per route. |
| **We enforce a wrong ACL perfectly.** | [QA.md](QA.md) B4 | We do not invent access rights and we do not fix IAM. We stop the model silently bypassing the rights the source already carries, and we log principal × source on every entitlement decision so the over-permissioned index becomes visible. |
| **Prompt injection makes a false claim “bind.”** | [QA.md](QA.md) B5 | Binding is computed by us, not asserted by the model. Injection can change what the model says; it cannot change which spans were captured, nor the entailment verdict, nor the ACL. The attack that does work is poisoning a source document — a supply-chain attack on the corpus, forensically traceable via source ID and content hash. *We defend the claim-to-evidence link, not the truth of the evidence.* |
| **Speculative release with post-hoc recall.** | §8 | Rejected. Hold-back buffer (~150–300 ms trailing delay). Failures inside the buffer never reach the user. No liability gap. |
| **Integration cost discovered after a “drop-in” sale.** | [QA.md](QA.md) C2; [NARRATIVE.md](NARRATIVE.md) §5 | Said out loud: one SDK hook plus a proxy; days, not quarters, on a standard retrieval stack; not zero. The integration cost is the moat. |

Nine mechanisms were removed outright ([ARCHITECTURE.md](ARCHITECTURE.md) §8). We will not re-import them under Round 2 pressure: model-emitted citations, speculative release, universal fail-open, cosine-similarity as a verdict, rolling z-score cost anomaly, GBDT rework predictors, demographic parity vs undefined base rates, “interrogator” LLMs, composite risk scores — plus LLM-as-judge on the critical path, confidence/logprob as the hallucination signal, static keyword guardrails as the product, dashboards as the deliverable, debate/voting for real-time gating, uniform validation depth, and any design that assumes access to weights, logits or fine-tuning.

---

## 7. Explicit assumptions

Stated so they can be attacked directly.

1. **API-consumed foundation models.** The enterprise does not own the weights. ControlPlane sits at the input/output layer: context-assembly hook + OpenAI-compatible proxy. No logits, no hidden states, no fine-tuning. This is a constraint we designed for, not a gap we paper over ([QA.md](QA.md) B1, C2).
2. **Mixed data governance.** A minority of sources are systems of record with real ACLs (orders DB, vendor agreement). A majority are loosely governed (FAQ, wiki, CRM notes, pasted tickets). The plane must still freeze whatever was actually retrieved — including the loose sources — because those are the spans the model was allowed to know. Entitlement is only as good as the ACL the source carries; see §6.
3. **India / enterprise regulated workflows as the primary lens.** Running example is an INR refund on a vendor-agreement clause; irreversible actions are payment, deletion, publication, regulated advice. Data-protection frame: Digital Personal Data Protection Act, 2023, plus sector rules on the acting routes (payments). We do **not** ship a hardcoded India/EU/US rule catalogue in the prototype — regulations differ by geography and age quickly, which is why policy is a **versioned DAG of 4-tuples** `(signal, threshold, action, latency_budget)`, not nested conditionals ([ARCHITECTURE.md](ARCHITECTURE.md) §4). Geographic packs are Phase 3 content.
4. **Tens of thousands of interactions per week** across three concurrent use cases (support, copilot, decision-support), with 80–90% at R0/R1. Directional, from the Round 2 brief, not a measured production trace.
5. **Caller identity is available at request time.** Entitlement is set-membership against `principal.clearance`. If the host application cannot name the principal, the entitlement axis degrades and we will say so rather than fake an ACL.
6. **The prototype is fixtures-and-Lane-1.** Claims in the demos are authored, not extracted by a 1–3B model. Binding is exact/fixture lookup, not NLI. That is sufficient to prove the keystone and the matrix; it is not a production claim extractor.

---

## 8. Round 2 “Real-World Complexity” coverage

Every Track 1 bullet from the Round 2 brief, addressed or explicitly deferred.

| Brief complexity | Stance | Where |
|---|---|---|
| Different use cases have different risk tolerance and latency budgets; one-size-fits-all fails | **Addressed.** Blast-radius matrix + budget-follows-R. Prototype: three use cases, three actuators. | §2.3, §4, Appendix A |
| Bias, hallucination and privacy overlap in practice | **Addressed.** Same graph, different labels; fabricated PII is UNSUPPORTED *and* a no-span leak; true HR fact is SUPPORTED *and* an ACL miss. Bias kept, as route-level counterfactual flip rate with CI, async — never a per-response verdict. | §2.5 |
| No reliable real-time ground truth | **Addressed.** Default UNSUPPORTED; absence of evidence (clause 7.2 does not exist) stays UNSUPPORTED, not CONTRADICTED. The plane does not need a gold answer to refuse an unproven action. | §1, §2.1, Appendix A |
| Over-flagging vs under-flagging | **Addressed.** Hostile verdict, proportionate action. Encoded in the matrix, not “solved away.” Three user states, no scores. | §2.3, §6 |
| Multi-turn conversations and agents that take actions; compounding risk | **Addressed in mechanism; session store deferred.** Each pending action on a response is priced separately (refund: R1 Edit + R3 Escalate). An unproven claim cannot authorise the *next* tool call on that ledger. **Deferred:** a full multi-turn session store that parents ledgers across turns. Reason: the primitive is per-request frozen provenance; wrapping it in a chatbot memory layer without that freeze would be slideware. Roadmap after Phase 2. | §2.3, §5, Appendix A |
| Regulatory expectations differ by geography and industry and evolve | **Addressed in mechanism; packs deferred.** Versioned policy DAG, not hard-coded rules. Shadow replay + auto-rollback on threshold changes. **Deferred:** geographic/sector policy *content* packs (DPDP, EU AI Act, sector payment rules as data). Reason: that is a catalogue on top of the engine; shipping a fake pack would age in the room. Primary lens is India/enterprise (assumption 3). | §5 Phase 3, §7.3 |
| Foundation model consumed via API; checker limited to the I/O layer | **Addressed.** Keystone is the context-assembly hook. No weights, logits, or fine-tuning. Parametric-only routes are declared ungrounded; they cannot authorise R2/R3. | §2.2, §2.4, §6, §7.1 |

Solutioning areas from the brief, mapped without expanding scope:

| Brief area | Our answer |
|---|---|
| Detection | Binding against provenance (not LLM-as-judge). Deterministic recompute for numeric/structural. Derived → UNKNOWN. Leakage = set-membership. Bias = counterfactual invariance async. **Rejected on the critical path:** AI-as-judge, confidence scores, cosine thresholds. |
| Decision logic | Frozen R × S matrix. Actuators Block / Edit / Escalate / Pass. Pure rule engine at decision time — zero LLM reasoning. |
| Architecture | Inline middleware on the commit path; text streams behind a hold-back; three lanes; speculative *verification* never speculative *release*. |
| Governance | Versioned DAG, `policy_version` on every ledger, hash-chained audit trail, canary + 3×-override rollback. |
| Feedback loops | Override capture → labelled spans → shadow replay → versioned threshold. Phase 3, not coded in the MVP. |
| Metrics | Publish **FNR per route**, dead-compute share, override rate, p50/p95. Empty schema until measured. |

---

## Appendix A — Prototype evidence

Working proof of the keystone on illustrative fixtures. Not production-grade, not real enterprise data, and not a claim extractor. Commands below were run for this proposal; actuators are locked by tests.

### A.1 Dual-action refund (Edit + Escalate)

```bash
python3 examples/refund_trace_demo.py
```

**Expected actuators (do not invert):**

| Pending action | Tier | Driving finding | Matrix cell | Actuator |
|---|---|---|---|---|
| `show_text` — Show text to the customer | **R1** | `hr_side` grounded on span ACL `{hr-confidential}` while caller clearance is `{vendor-public}` | `R1 × Contradicted / entitlement violation` | **Edit** — unentitled span stripped |
| `issue_refund` — Issue the refund (irreversible, ₹1,84,000, ORD-9) | **R3** | `clause_72` (“Clause 7.2 permits this refund”) binds to no span | `R3 × Unsupported + categorical` | **Escalate** — **held and escalated with the evidence packet** |

Never say the refund was “blocked.” R3 × unsupported-categorical = Escalate.

**Observed in the demo run:**

- Ungated response: `Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.`
- Principal `cs-agent-17`, clearance `{vendor-public}`, policy `matrix-v1`.
- Five spans at context assembly; **no span for clause 7.2**.
- `clause_72` verdict **UNSUPPORTED** (absence of evidence, not conflicting evidence — the clause does not exist, it does not “cap” or “deny”).
- `hr_side` verdict SUPPORTED via `span-3` **and** entitlement **VIOLATION**.
- `faq_search` / `crm_lookup` produce spans that ground no accepted claim (dead compute, named by walking the graph backward).
- `show_text` actuator **Edit**; driving `hr_side, clause_72`; evidence packet attached.
- `issue_refund` actuator **Escalate**; driving `clause_72`; packet carries the unproven clause.
- `verify_chain() = True`.

Locked by `tests/test_refund_scenario.py` (`show_text` → Edit, `issue_refund` → Escalate, chain holds).

### A.2 Three use cases, three R-tiers, three actuators

Round 2 reference: customer support assistant, internal knowledge assistant, decision-support tool.

```bash
python3 examples/multi_usecase_demo.py
```

**Expected actuators:**

| Use case | Action | Tier | Claim | Cell | Actuator |
|---|---|---|---|---|---|
| Customer support chatbot | `show_reply` | R1 | hedged warranty guess, UNSUPPORTED | `R1 × Unsupported + hedged` | **Pass + annotate** |
| Internal knowledge copilot | `draft_partner_email` (external send) | R2 | categorical partner SLA, UNSUPPORTED | `R2 × Unsupported + categorical` | **Edit** |
| Decision-support refund | `issue_refund` | R3 | “Clause 7.2 permits this refund,” UNSUPPORTED | `R3 × Unsupported + categorical` | **Escalate** |

**Observed in the demo run:**

```
1. Customer support chatbot
   action     show_reply  (Show reply to the customer, R1)
   cell       R1 × Unsupported + hedged  →  Pass + annotate
   actuator   Pass + annotate

2. Internal knowledge copilot
   action     draft_partner_email  (Draft email to partner (external send), R2)
   cell       R2 × Unsupported + categorical  →  Edit
   actuator   Edit

3. Decision-support refund
   action     issue_refund  (Issue the refund, R3)
   cell       R3 × Unsupported + categorical  →  Escalate
   actuator   Escalate
```

Same plane. Three R-tiers. Three actuators. Hash chain verifies on each ledger.

Locked by `tests/test_multi_usecase.py`.

### A.3 What the prototype is — and is not

| In this slice | Not in this slice |
|---|---|
| Provenance Recorder (record step/span, freeze context) | OpenAI-compatible reverse proxy |
| Append-only hash-chained Evidence Ledger | Streaming 1–3B claim extractor |
| Deterministic binder, default UNSUPPORTED; derived → UNKNOWN | NLI Prosecutor / semantic-entropy probe |
| Entitlement Auditor (ACL ⊂ clearance) | Counterfactual bias replay (specified, async, not coded) |
| Action Interlock on the frozen matrix | Economist live breaker / FNR publisher |
| Refund dual-action + three-use-case fixtures | Multi-turn session store, geographic policy packs, PII NER model |

No LLM and no network on the critical path. That is a fidelity choice, not a missing detector: Lane 1 is where 80–90% of volume and all of R3 entitlement/interlock already live.

---

*Design is closed in [ARCHITECTURE.md](ARCHITECTURE.md). This proposal is a rendering of that file for Round 2, plus evidence that the keystone runs.*

## Appendix B — Live control plane (production elevation)

The core mechanism is no longer CLI-only. On branch `feature/round2-controlplane`:

```bash
uvicorn controlplane.server.app:create_app --factory --host 127.0.0.1 --port 8787
# Judge console: http://127.0.0.1:8787
# Or: docker compose up --build  → http://localhost:8080
```

| Surface | Proof |
|---|---|
| OpenAI-compatible gate | `POST /v1/chat/completions` with `scenario=refund` returns Edit+Escalate in `controlplane` extension |
| Enforce overlay | User-visible text strips clause 7.2; irreversible refund `action_allowed=false` |
| Shadow / FNR | `GET /v1/controlplane/metrics` publishes would-have counters and labeled FNR shape |
| Policy packs | `policies/*.yaml` — support / copilot / decision-support |
| Audit | `GET /v1/controlplane/requests/{id}/audit.jsonl` |

Lane 1 remains deterministic. No LLM on the critical path. Matrix transcribed, never redrawn.
