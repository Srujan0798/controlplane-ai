## 1. Round 2 Core Thesis

ControlPlane.ai expands from the frozen claim-verification mechanism into an enterprise admission-control plane that applies the same `STEP → SPAN → CLAIM → ACTION` graph across multiple AI routes, with route-specific latency and blast-radius policies rather than separate detectors. Its differentiation remains unchanged: provenance is captured outside the model, every claim starts **UNSUPPORTED** and must earn proof, entitlement is checked against the caller and source ACL, and verification effort is priced by blast radius. The Round 2 expansion is therefore breadth of deployment and governance around the frozen graph—not a new safety mechanism.  

---

## 2. Selected Use Cases for the Prototype

### Use Case 1 — Customer Support Agent with Transactional Actions

**Concrete description**

An AI customer-support agent answers account/refund questions and may initiate downstream actions such as sending a customer-visible response, issuing a refund, or invoking another reversible/irreversible support tool. This is the primary prototype route because the same response can contain claims with materially different consequences. The frozen architecture already defines the canonical demonstration: one response can simultaneously contain an unentitled customer-visible claim and an unsupported refund-policy claim, yielding different actuators for the two pending actions. 

**Risk signature**

* Hallucinated policy/factual claims.
* Unsupported categorical assertions that influence a financial action.
* Retrieval-side entitlement leakage.
* Numeric/date/identifier errors affecting transactions.
* Multi-turn compounding risk because one answer can lead directly to a tool call.
* No dependable external real-time ground truth is assumed; proof comes from the captured evidence set and deterministic recomputation where applicable. The official brief explicitly identifies overlapping hallucination/privacy risk and compounding risk from action-taking agents. 

**Latency budget**

* Customer-visible text: target **≤40 ms p50 / ≤200 ms p95 added latency**.
* Action verification: completed inside the tool-call latency budget; speculative verification is permitted, speculative release is not.
* A short text hold-back buffer is used so verification does not require post-hoc recall.  

**Blast-radius profile**

* **R0:** internal support draft.
* **R1:** customer-visible read-only response.
* **R2:** reversible write / external send.
* **R3:** refund or other irreversible/regulated action.

The architecture explicitly defines these tiers by consequence, not by model confidence. 

**Frozen mechanism demonstrated most powerfully**

**The exact R×S matrix applied per pending action.** This use case demonstrates why one response cannot have one global verdict: the text path and action path can require different actuators. The frozen example resolves:

* `R1 × entitlement violation → Edit`
* `R3 × Unsupported + categorical → Escalate`

simultaneously. 

That is the strongest live demonstration of **blast-radius pricing**, the **hard action gate**, and the fact that the system does not collapse multiple actions into one response-level block/allow decision.

---

### Use Case 2 — Internal Knowledge Assistant over Mixed-Governance Enterprise Data

**Concrete description**

An employee-facing knowledge assistant answers questions over a mixture of well-governed and loosely governed internal sources such as policy documents, HR material, project documents, and operational records. The prototype intentionally includes one over-permissioned or incorrectly exposed source so the same answer can be semantically correct yet unauthorized for the caller.

This directly matches the official brief's reference environment of multiple AI use cases and mixed well-governed/loosely governed data sources. 

**Risk signature**

* Correct-but-unauthorized disclosure.
* Fabricated entities or sensitive facts with no supporting span.
* Claims grounded in a source whose ACL excludes the caller.
* Paraphrased claims that require entailment rather than string matching.
* The prototype does **not** attempt to repair the enterprise IAM system; it enforces the ACL carried by the source and makes violations explicit. 

**Latency budget**

* Normal R1 interaction: **≤40 ms p50 / ≤200 ms p95** added verification latency.
* Deterministic span-membership and ACL checks remain inline; probabilistic binding is reserved for claims that require it.
* The target is consistent with the frozen architecture's three-lane design rather than introducing a second latency architecture. 

**Blast-radius profile**

* Dominantly **R1** because the prototype interaction is read-only and user-visible.
* The underlying graph is still capable of representing higher-R actions, but those action types are demonstrated primarily in the customer-support route.

**Frozen mechanism demonstrated most powerfully**

**Provenance captured outside the model + deterministic entitlement check.**

The critical demonstration is not "the model said something sensitive." It is:

`CALLER → CLAIM → SPAN → SOURCE ACL`

and the system independently determines that the caller is not entitled to that span. This is exactly the distinction the architecture makes between lexical inspection and authorization. 

---

**Why these two together are the strongest prototype combination**

The pair is deliberately asymmetric.

* **Customer support** proves consequence-aware admission control: one graph, multiple pending actions, all four blast-radius tiers, hard gating, surgical edit, and evidence-packet escalation.
* **Internal knowledge** proves that the graph is not merely RAG groundedness: provenance contains **identity + ACL + source + hash**, allowing the same semantic claim to produce different outcomes for different principals.
* Together they exercise both sides of the architecture: **"is this claim proven?"** and **"is this caller entitled to use that proof?"** 
* The prototype intentionally does **not** add decision-support as a third live route. Bias is defined by the frozen architecture as a route-level, asynchronous counterfactual property, not a per-response verdict; adding that to the core live demo would consume scope without strengthening the central graph mechanism. 

The matrix is therefore demonstrated through **different action consequences on the same graph**, not by building three shallow applications.

---

## 3. Prototype Boundary (Hard)

### What the working prototype WILL demonstrate

The prototype will be an end-to-end executable path, not a simulated dashboard.

**1. Context-assembly provenance capture**

At the point where context is assembled, the prototype records, outside the model:

`source_id · ACL · content_hash · offsets · principal`

This is the keystone of the frozen architecture. 

**2. One request becomes one typed graph**

The live trace visibly reconstructs:

`STEP → SPAN → CLAIM → ACTION`

with no separate "hallucination detector," "privacy detector," and "action safety detector." 

**3. Claims begin UNSUPPORTED**

Every check-worthy claim starts `UNSUPPORTED`. A claim becomes `SUPPORTED` only when the frozen binding/recomputation path proves it. `UNKNOWN` remains distinct and never collapses into `SUPPORTED`.  

**4. Claim-specific verification**

At minimum:

* numeric/date/identifier claims → deterministic recomputation;
* textual claims → binding against the provenance set;
* derived claims → recomputation or `UNKNOWN`;
* no open-web verification;
* no model-emitted citation treated as evidence. 

**5. Entitlement enforcement**

The same claim is tested against the caller's identity and the span's source ACL. An unauthorized span produces an entitlement violation independently of semantic correctness. 

**6. Exact frozen R×S matrix**

The prototype must visibly execute all four rows and all four severity columns of the frozen matrix, not a simplified "low/medium/high" derivative. The matrix is transcribed exactly:

|        | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown             |
| ------ | ------------------------------------ | ------------------------- | -------------------- | ------------------- |
| **R3** | **Block**                            | **Escalate**              | **Escalate**         | **Escalate**        |
| **R2** | **Block**                            | **Edit**                  | **Edit**             | **Escalate**        |
| **R1** | **Edit**                             | **Edit**                  | **Pass + annotate**  | **Pass + annotate** |
| **R0** | **Pass + annotate**                  | **Pass + annotate**       | **Pass**             | **Pass**            |



**7. Surgical Edit**

The prototype demonstrates that editing removes only the failing claim or performs one constrained regeneration tied to the failing span. The edited output re-enters the gate; free-form rewriting is excluded. 

**8. Evidence-packet escalation**

Escalation produces the claim, candidate spans, verdict, and diff—not merely an alert. 

**9. Action gate with optimistic text**

Text uses a short hold-back; the hard gate is placed on the action/commit boundary rather than token generation. 

**10. Two-pending-action trace**

The primary demo reproduces the frozen resolution:

* customer-visible text → `R1` entitlement violation → `Edit`
* refund action → `R3` unsupported categorical → `Escalate`

Both decisions occur from the same response and graph. 

**11. Adversarial inputs**

At least these live/recorded cases:

* fabricated policy clause;
* unauthorized HR/customer field;
* paraphrase of a valid source statement;
* incorrect numerical figure;
* no-retrieval/parametric claim;
* prompt injection attempting to manipulate the binding.

The prompt-injection case must demonstrate that the model cannot author its own binding; binding comes from ControlPlane's captured provenance. 

**12. Measurement surface**

The prototype exposes:

* decision latency;
* lane used;
* claim verdict;
* selected matrix cell;
* actuator;
* provenance identifiers;
* evidence packet;
* action disposition;
* route identifier.

The architecture's evidence ledger is the correct underlying artifact. 

### What it will deliberately NOT demonstrate

| Excluded from working prototype                       | Precise reason                                                                                                                                                                                                                                                                                        |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Production-scale tens-of-thousands/week load test** | Round 2 allows limited/simulated scope; scale belongs in the business proposal and deployment model, not the mechanism proof.                                                                                                                                                                         |
| **Live enterprise IAM remediation**                   | ControlPlane enforces source ACLs; it does not replace or repair IAM. Claiming otherwise contradicts the frozen boundary.                                                                                                                                                                             |
| **Real payment execution**                            | Unsafe and unnecessary for proof. Use a deterministic mock tool with real gate semantics so the commit boundary is observable without creating actual financial consequences.                                                                                                                         |
| **Decision-support / regulated-advice live workflow** | Bias is intentionally modeled as route-level asynchronous counterfactual analysis, not a per-response classifier. Adding it would create another proof problem rather than strengthen the frozen graph.                                                                                               |
| **Per-response bias verdicts**                        | Explicitly contrary to the frozen architecture. Bias is a distributional property.                                                                                                                                                                                                                    |
| **LLM-as-judge as the primary verifier**              | Structurally duplicates the category being rejected and destroys the deterministic provenance/entitlement differentiation.                                                                                                                                                                            |
| **Confidence score / global risk score**              | The frozen architecture rejects confidence as the primary signal and uses verdict + blast radius instead.                                                                                                                                                                                             |
| **Full autonomous multi-agent swarm**                 | The architecture's internal workers are specialized deadline-driven components over a typed ledger; demonstrating conversation among agents adds no proof value.                                                                                                                                      |
| **Open-web factual verification**                     | Binding is intentionally limited to the captured provenance set.                                                                                                                                                                                                                                      |
| **Production regulatory certification**               | Round 2 can demonstrate the control mechanism; certification, retention, jurisdiction-specific legal mapping, and enterprise deployment belong in the business proposal.                                                                                                                              |
| **Real measured enterprise FNR**                      | There is no legitimate enterprise ground-truth population available. The prototype may report measurements on its adjudicated test corpus, but must not present synthetic evaluation as a production FNR. The frozen design explicitly calls for stratified shadow auditing and measured error bars.  |

### Minimum viable live demonstration that still feels advanced

**One trace. One graph. Two pending actions.**

1. Employee/customer context is assembled from two sources with distinct ACLs.
2. The model produces one response containing:

   * a valid claim;
   * a claim grounded in a span the caller cannot read;
   * a categorical policy claim for which no supporting span exists;
   * a refund/tool action.
3. The screen simultaneously shows the `STEP → SPAN → CLAIM → ACTION` graph.
4. The entitlement violation causes **R1 → Edit** for the visible text.
5. The unsupported categorical refund claim causes **R3 → Escalate**; the refund is held.
6. The escalation packet appears with claim, spans, verdict, and diff.
7. A second trace changes only the caller identity and demonstrates that the same underlying source produces a different authorization outcome.
8. A third trace changes only the action consequence and demonstrates that the same claim changes actuator because **R changes**, not because the claim's "confidence" changed.
9. The screen then shows the exact frozen matrix and the measured latency for the run.

That is the minimum that proves the architecture rather than merely describing it.

---

## 4. Explicit Assumptions

### Data

1. The prototype uses synthetic but enterprise-shaped documents and records because the official brief explicitly says teams are not expected to possess proprietary company data. 
2. Each provenance span contains at minimum `source_id`, `ACL`, `hash`, and offsets.
3. At least two source classes exist:

   * customer-support policy/account records;
   * internal knowledge documents containing both broadly accessible and restricted material.
4. The dataset deliberately contains both:

   * correctly governed spans;
   * an over-permissioned/restricted span scenario.
5. The evaluation corpus contains known expected claim outcomes so a controlled adjudication set can be constructed.
6. Derived numerical claims have deterministic source values available for recomputation.
7. Some claims intentionally have no supporting span to test the UNSUPPORTED default.
8. Prompt injection is represented as untrusted source/input text; it cannot directly modify the provenance ledger.

### Models

9. The generator is accessed through a standard API interface.
10. No model weights, logits, hidden states, or fine-tuning access are assumed.
11. Claim extraction may use a small model; textual binding may use the frozen NLI cross-encoder design. The core decision policy itself is deterministic and contains zero LLM reasoning. 
12. Model output format can be intercepted before release and before action execution.
13. No assumption is made that the generator is intrinsically truthful.

### Traffic and workload

14. The reference enterprise scale is **tens of thousands of interactions per week**, but the live prototype is a single-node/small-scale functional implementation. The official brief describes this scale as directional rather than a fixed dataset. 
15. The prototype traffic mix is intentionally skewed toward ordinary R0/R1 interactions, with a small number of R2/R3 actions, consistent with the architecture's blast-radius economics.
16. The prototype does not claim production throughput from a demonstration environment.

### Latency

17. The authoritative target is **≤40 ms p50 and ≤200 ms p95** added R0/R1 text latency.
18. Action gating is measured against tool round-trip latency rather than treated as equivalent to token-generation latency. 
19. If a proof path times out, the result becomes `UNKNOWN` and is routed through the matrix rather than silently downgraded to `PASS`. 

### Regulatory posture

20. The prototype assumes an enterprise-general governance posture rather than claiming compliance certification for one jurisdiction.
21. Jurisdiction-specific policy packs, retention requirements, and sector rules are configuration/business-proposal scope, not claims of legal compliance.
22. The prototype does not interpret regulation as model reasoning; versioned policy rules remain deterministic infrastructure.

### Integration surface

23. The prototype exposes two integration points:

* an OpenAI-compatible reverse proxy;
* a thin SDK hook at context assembly.

24. The application is assumed not to require a rewrite.
25. Source systems already expose enough identity/ACL metadata for the provenance hook to capture it. 
26. The prototype does not assume direct access to foundation-model internals.

### Evaluation

27. The evaluation set is manually constructed/adjudicated for the prototype and is not represented as enterprise ground truth.
28. Any FNR value shown is explicitly labeled by route and evaluation corpus.
29. Where trustworthy ground truth is unavailable, the report shows the field as unavailable rather than fabricating a percentage; the architecture explicitly requires measured error reporting rather than invented numbers. 
30. Shadow mode is the default conceptual deployment posture before enforcement; the prototype can run the same gated-vs-ungated counterfactual without claiming that a production route has already earned enforcement. 

---

## 5. Success Criteria for the Prototype

Each criterion is binary.

| #      | Judge-verifiable criterion                               | Pass condition                                                                                                                                                       |
| ------ | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**  | Provenance exists outside model output                   | Every retrieved/tool span shown in the trace contains source, ACL, hash, and offsets.                                                                                |
| **2**  | One-graph invariant holds                                | The UI/log shows one `STEP → SPAN → CLAIM → ACTION` graph for a complete request.                                                                                    |
| **3**  | UNSUPPORTED default is real                              | Every newly extracted claim enters the verifier as `UNSUPPORTED`; no claim begins as `SUPPORTED`.                                                                    |
| **4**  | Claim-level proof works                                  | A supported claim visibly binds to a specific captured span; an unsupported claim visibly lacks such proof.                                                          |
| **5**  | Paraphrase does not break valid binding                  | A paraphrased supported claim is accepted when the captured span entails it.                                                                                         |
| **6**  | Numeric verification is deterministic                    | An intentionally altered numeric claim is rejected by recomputation against the captured spans.                                                                      |
| **7**  | ACL enforcement is independent of semantic correctness   | A semantically correct claim backed by an unauthorized span is routed as an entitlement violation.                                                                   |
| **8**  | Exact matrix is implemented                              | All tested verdict/action combinations map to the exact frozen R×S cells, with no invented severity tier.                                                            |
| **9**  | Two pending actions resolve independently                | One response can simultaneously yield `R1 → Edit` and `R3 → Escalate`.                                                                                               |
| **10** | Action gate is real                                      | The mock refund/tool side effect does not execute while its required gate outcome is `Escalate` or `Block`.                                                          |
| **11** | Text is not globally blocked by an action failure        | A response can remain user-visible subject to its own matrix result while the higher-radius action is held.                                                          |
| **12** | Edit is surgical                                         | The failing claim is removed or regenerated once under the specified failing-span constraint; the edited result is re-verified.                                      |
| **13** | Escalation contains an evidence packet                   | Claim, candidate spans, verdict, and diff are visible without asking a human to reconstruct the reasoning from logs.                                                 |
| **14** | Caller identity changes outcome when entitlement changes | The same source/claim tested under two principals produces different authorization outcomes when their ACLs differ.                                                  |
| **15** | Prompt injection cannot author provenance                | An injected instruction cannot create or modify a provenance span or binding edge.                                                                                   |
| **16** | Action consequence changes actuator                      | The same or equivalent claim routed as R1 vs R3 produces the corresponding different matrix action.                                                                  |
| **17** | Latency target is measured, not asserted                 | Prototype records p50/p95 added latency and reports them separately; it does not relabel p50 as p95.                                                                 |
| **18** | FNR reporting format exists                              | Per-route FNR fields identify evaluation population, numerator, denominator, interval/measurement status, and whether the value is actually measured or unavailable. |
| **19** | No global confidence score drives disposition            | The final actuator is traceable to verdict severity × blast radius, not to a scalar trust/confidence score.                                                          |
| **20** | The prototype can survive hostile inspection             | A judge can replay at least one supported, unsupported, entitlement-violating, contradictory, unknown, R1, R2, and R3 case from the same executable control path.    |

---

## 6. Fidelity Self-Check

| Frozen invariant                            | Status                | Resolution                                                                                                                            |
| ------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Default = UNSUPPORTED**                   | **Preserved**         | Every claim begins unsupported and must earn support. No "confidence threshold" replaces this.                                        |
| **Entitlement / ACL check**                 | **Preserved**         | Provenance retains ACL and caller identity; unauthorized spans are an explicit entitlement violation.                                 |
| **Exact R×S matrix**                        | **Preserved exactly** | No new rows, columns, severity labels, or composite scores are introduced.                                                            |
| **Hard gate on actions, not tokens**        | **Preserved**         | Text uses hold-back; action commit is the enforcement boundary.                                                                       |
| **Own per-route FNR as a reporting format** | **Preserved**         | The prototype reports only measured/adjudicated values; unavailable ground truth remains explicitly unavailable.                      |
| **Two-pending-actions resolution**          | **Preserved**         | Customer-visible text is `R1 → Edit`; refund is `R3 → Escalate`, simultaneously. They are never collapsed into one response verdict.  |
| **Surgical edit only**                      | **Preserved**         | No unconstrained rewriting loop.                                                                                                      |
| **Evidence-packet escalation**              | **Preserved**         | Escalation carries evidence and diff, not just an alert.                                                                              |
| **No LLM-as-judge substitution**            | **Preserved**         | The verifier binds against captured evidence; no second general-purpose model becomes the final arbiter.                              |
| **No response-level bias verdict**          | **Preserved**         | Bias remains route-level asynchronous counterfactual analysis, so it is not incorrectly forced into the live claim verdict path.      |

**One deliberate scope tension:** the official brief encourages decision-support and bias handling, but the frozen architecture says bias is a **distributional, asynchronous property**, while the prototype must primarily prove the claim-to-action control mechanism. The resolution is to keep decision-support and counterfactual bias measurement in the **complete enterprise solution/business proposal**, while refusing to contaminate the live core prototype with a second decision mechanism. That is a scope restriction, not an architectural change.

---

## 7. Biggest Scope Risk + Exact Mitigation

**Risk:** The prototype becomes a visually impressive "AI safety dashboard" that demonstrates several detections but fails to prove that the frozen architecture actually controls execution. A judge then reduces it to "another RAG/LLM checker with a score," and the strongest differentiation disappears.

**Exact mitigation:** **Freeze the demo around one executable customer-support trace and force every screen to resolve to the same graph.** The live path must start at context assembly, show the captured `source + ACL + hash`, show claims entering `UNSUPPORTED`, traverse the exact matrix, produce the two simultaneous outcomes `R1 → Edit` and `R3 → Escalate`, and demonstrate that the R3 action cannot execute. The internal-knowledge scenario then changes only the principal/source entitlement to prove that authorization is part of the same graph. Do not add a third live application until this trace can be executed deterministically from start to finish.

The governing test is simple: **if the judge can remove the graph from the screen and the demo still looks the same, the scope has already failed.**
