**1. Problem Framing**

Enterprises have moved from AI that answers to AI that acts. A wrong output used to be a bad paragraph. It is now an executed transaction: a refund issued, a record written, a message sent, a regulated recommendation delivered. The cost category changed; the tooling did not.

Existing layers still inspect finished text. Guardrails match surface forms and are identity-blind. LLM-as-judge wrappers form opinions without the evidence the model was given and without knowing who is asking. RAG groundedness checkers average, so one wrong figure drowns in nine correct sentences, and they are action-blind: the same score means the same thing on a draft and on a wire transfer. Observability tools produce excellent post-hoc traces after the harm has already landed. None of them capture provenance outside the model, none invert the burden of proof, none carry caller identity into verification, and none price verification by what the response is about to do. The result is predictable: either over-flagging that creates alert fatigue and bypass, or under-flagging that creates liability, while unproven claims continue to authorize irreversible actions.

**2. Solution Design Summary**

ControlPlane is an admission-control layer. Every AI response is treated as a set of claims requesting permission to act. At context assembly, outside the model, the system records the exact evidence the model was given (`source_id · ACL · content_hash · offsets`) together with the calling principal. Every check-worthy claim starts **UNSUPPORTED** and must earn proof against that captured provenance set. Entitlement is deterministic set-membership: a claim that binds to a span whose ACL excludes the caller is unauthorized regardless of semantic correctness. The Action Interlock applies the exact frozen R×S matrix **per pending action**, so the identical unsupported claim produces Edit on an R1 text path and Escalate (held, with evidence packet) on an R3 payment path. Text streams behind a short hold-back; the hard gate sits on the action/commit boundary. Performance, cost, and responsibility are three reads of one graph — STEP → SPAN → CLAIM → ACTION — not three separate detectors. The plane publishes its own per-route false-negative rate as a typed schema; emptiness is the credibility statement until measurement is earned.

**3. Target Users & Buyers**

- **Economic buyer**: Head of AI / AI Governance, Chief Risk Officer, or business-unit owner of a high-stakes AI route (payments, regulated advice, customer-facing agents). They feel the liability of an executed wrong action and the cost of alert fatigue that causes teams to switch layers off.
- **Technical buyer**: Platform / ML engineering lead responsible for the retrieval and agent stack. They feel the integration cost of another opaque wrapper and the absence of a verifiable audit trail that can be reconstructed from evidence rather than model opinion.
- **Day-to-day operators**: Support operations, knowledge-base owners, and the human escalators who receive evidence packets. They need a clear Verified / Uncertain / Blocked surface per claim and a packet that does not require reconstructing reasoning from raw logs.
- **Secondary stakeholders**: Internal audit and compliance, who require an append-only ledger with policy version, principal, and evidence fragment for every decision.

**4. Business Case & Impact Logic**

Value is created in four concrete, measurable places:

1. **Avoided wrong actions.** An unproven categorical claim on an R3 path is held and escalated with an evidence packet instead of executing. The company does not wrongly pay out; the customer does not lose money. The impact is the prevented irreversible side-effect, not a precision score.
2. **Reduced dead compute.** Walking the graph backward yields an exact number: every STEP that grounded zero accepted claims is waste. This is observable without estimation and is the number a cost owner can act on.
3. **Reduced alert fatigue.** Verification budget follows blast radius. R0/R1 traffic (the majority) receives deterministic Lane-1 checks and proportionate actuators (Pass + annotate). Enforcement is earned per route through shadow counterfactuals, so teams are never forced to trust an unproven block rate. Over-blocking is what causes layers to be switched off; the matrix exists to prevent it.
4. **Auditability and liability posture.** Every decision carries principal, evidence fragment, matrix cell, actuator, and policy version in an append-only ledger. When regulation or internal audit asks “why was this action allowed or held?”, the answer is reconstructible from evidence, not from a model’s self-report.

Impact logic is directional and falsifiable: fewer irreversible actions that lack proof, measurable waste on the graph, lower override rates once enforcement is earned, and a ledger that survives scrutiny. No fabricated ROI percentage is claimed.

**5. Phased Roadmap**

**Phase 0 — Prototype (current Stage 3 scope)**  
Two routes only (refund dual-action + knowledge principal-flip). Synthetic corpora. Mock refund tool. Empty FNR schema. Live Evidence Ledger. Goal: prove the admission primitive is executable and visible in ≤8 minutes.

**Phase 1 — Limited production routes (shadow-first)**  
Deploy the same plane on 1–2 real enterprise routes under shadow mode. Emit gated-vs-ungated counterfactuals. Collect override rates and stratified samples. Enforcement remains off. Goal: earn the first route-level evidence that the plane would have held true positives without excessive friction.

**Phase 2 — Earned enforcement on high-R routes**  
Promote routes that meet earn-out criteria (stable override rate, measured FNR strata, no auto-rollback triggers). R3 actions move to hard gate; R0/R1 remain predominantly annotate. Goal: first irreversible actions that are held by proof rather than by policy preference.

**Phase 3 — Multi-route enterprise envelope**  
Add decision-support routes under the same graph and matrix. Introduce versioned geography/sector overlays (additive only). Activate full Adjudicator pipeline for continuous FNR reporting. Goal: one control plane across heterogeneous risk and latency profiles without inventing a second detector.

**Phase 4 — Operational maturity**  
Circuit-breaker autonomy tiers, dead-compute cost reporting into FinOps, source-hygiene tickets from entitlement-violation rates, and formal integration with existing IAM as the source of ACLs (ControlPlane still does not repair IAM; it makes violations visible). Goal: the plane becomes infrastructure that is audited by the standard it enforces.

Enforcement is never switched on enterprise-wide from a slide. It is earned per route.

**6. Key Risks & Mitigations**

| Risk | Why it matters | Mitigation (from freeze) |
|---|---|---|
| False assurance on derived / multi-hop claims | Highest residual technical risk; shallow entailment can mark a synthesized claim SUPPORTED | Derived claims bypass ordinary NLI → recompute or UNKNOWN; UNKNOWN never becomes SUPPORTED; timeout routes via matrix + fail stance |
| Poisoned or over-permissioned sources | Plane proves claim↔evidence and enforces carried ACLs; it does not prove the source is true or repair IAM | Immutable source_id + content hash; missing ACL treated as unentitled on privileged routes; entitlement-violation rate per source is the operational detector; forensic ledger |
| Over-flagging → alert fatigue → bypass | Classic failure mode of guardrail layers | Shadow default; enforcement earned per route; blast-radius pricing (R0/R1 mostly Lane-1 + annotate); auto-rollback on override rate >3× baseline |
| Under-flagging / R mis-mapping | Payment mapped to low R applies the wrong matrix row | Locked action classes (payment, deletion, publication, regulated advice) → R3 at parse time; hard interlock in the action executor, not only the UI |
| Integration friction | Teams abandon layers that require rewrite or model access | Thin context-assembly SDK hook + OpenAI-compatible proxy; no weights, logits, or fine-tuning; days, not quarters |
| Plane itself becomes a single point of failure | Load-induced bypass or outage | Fail stance is tier-owned: R0/R1 fail open with annotation; R2/R3 fail closed or escalate. Universal fail-open is forbidden |

**7. Differentiation Anchor**

1. **Provenance outside the model** turns verification into a set-membership test against evidence assembled before generation, not an opinion formed after the fact.
2. **Default = UNSUPPORTED** inverts the burden of proof. Nothing passes because nobody objected; a claim must earn SUPPORTED.
3. **Entitlement as deterministic set-membership** carries caller identity into the verification layer. Identity-blind output scorers and LLM-as-judge wrappers cannot do this.
4. **Blast-radius × verdict matrix applied per pending action** means the identical unsupported claim produces Edit on text and Escalate (held) on payment. Proof scales with consequence. Composite risk scores cannot do this.
5. **Published own per-route false-negative rate as a format** (empty until earned). Competitors publish precision — the rate at which they bother the user. ControlPlane publishes the rate at which it missed.

These five points are the load-bearing differentiators against NeMo Guardrails, LlamaGuard, RAG groundedness checkers, LLM-as-judge wrappers, and post-hoc observability tools. They are architectural, not rhetorical.

**8. Fidelity Self-Check**

- Default = UNSUPPORTED — preserved; claims must earn proof.  
- Entitlement / ACL check — preserved; deterministic, always-on, zero LLM, identity-carrying.  
- Exact R×S matrix — preserved; never redrawn; applied per pending action.  
- Hard gate on actions, not tokens — preserved.  
- No claim that the system eliminates hallucinations, bias, or privacy risk — preserved (refuse-to-claim list intact).  
- No LLM-as-judge or confidence score as primary mechanism — preserved; Action Interlock is a pure rule engine.  
- Bias remains route-level asynchronous counterfactual measurement only — preserved; never a live per-response verdict.  

The business proposal is configuration, governance, and impact logic around the frozen admission primitive. It does not reopen Stages 1–3 and does not introduce a competing mechanism.