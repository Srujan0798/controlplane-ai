# Stage 2 — Expanded Solution Architecture

---

## 1. Expanded Core Thesis

ControlPlane is an admission-control layer that treats every AI response as a set of claims requesting permission to act. As an enterprise deploys it across heterogeneous routes — customer-facing agents, internal knowledge assistants, regulated decision-support copilots — the same `STEP → SPAN → CLAIM → ACTION` graph governs every route; what changes is the **route configuration** that maps blast radius, latency lane, policy version, and fail stance to that route's risk signature. The single sharpest differentiator survives intact: provenance is captured outside the model at context assembly, every claim starts UNSUPPORTED and must earn proof, entitlement is deterministic set-membership against caller identity and source ACL, and verification effort is priced by blast radius on the frozen R×S matrix. The enterprise system is not a new detector per route — it is a **policy-configured deployment of one graph across many routes**, with a governance layer that lets behaviour vary without forking the architecture.

---

## 2. Multi-Route Architecture

### What Is Shared

Every route in the enterprise shares the same core structure. There is one graph, one Evidence Ledger schema, one claim-extraction pipeline, one binding engine, one entitlement auditor, one action interlock, and one matrix. The shared components are:

| Shared Component | Description |
|---|---|
| **Provenance Recorder** | Hooks context assembly on every route. Captures `source_id · ACL · content_hash · offsets · principal` for every span. This is the keystone — identical on every route, because the model cannot declare its own provenance regardless of the use case. |
| **Evidence Ledger** | Append-only, hash-chained, one per request. Schema is identical across routes: `{ principal, action_intent, R_tier, spans[], claims[], bindings[], step_yield[], verdicts[], policy_version, verifier_versions, latency_spent }`. The ledger is the single source of truth for every downstream read — performance forward, cost backward, responsibility on labels. |
| **Claim Extractor** | Streaming, sentence-boundary, emitting typed check-worthy propositions tagged categorical or hedged. Same extraction logic on every route; the route configuration determines which extracted claims are worth the expensive binding path. |
| **Binding Engine** | Two paths: deterministic recomputation for numeric/structural/temporal claims; NLI cross-encoder for textual/factual claims against the provenance set only. Same engine, same model, same entailment threshold — but the **lane** the binding runs in is determined by the route's R-tier profile. |
| **Entitlement Auditor** | Deterministic set-membership: caller principal vs source ACL on every span that binds to a claim. Zero LLM. Identical on every route, because the ACL check is a property of the span and the caller, not of the use case. |
| **Action Interlock** | Computes R, applies the frozen matrix, emits the actuator. Pure rule engine, zero LLM reasoning at decision time. The matrix is transcribed identically on every route — axis labels, column vocabulary, and cell values are load-bearing and never redrawn. |
| **Adjudicator** | Stratified shadow audit: 100% of blocks and escalations plus a random slice of passes, sampled to expensive ground truth. Per-route FNR reported with confidence intervals. |

### What Is Configured Per Route

Each route carries a **Route Configuration Object** — a versioned, auditable policy document that governs behaviour without changing the engine. The configuration is a set of typed parameters, not free-form code:

| Configuration Field | Type | What It Controls | Example Values |
|---|---|---|---|
| `route_id` | string | Unique identifier | `cs-refund-v1`, `hr-knowledge-v1`, `claims-copilot-v1` |
| `default_R_tier` | enum {R0, R1, R2, R3} | The baseline blast-radius tier for this route's primary action | `R3` for refund agent, `R1` for knowledge assistant |
| `action_tiers` | map[action_type → R_tier] | Per-action-type override when a single response carries multiple pending actions | `{ "show_text": R1, "execute_refund": R3 }` |
| `latency_lane` | enum {lane1, lane2, lane3} | Which verification lane is the default for this route's traffic | `lane1` for R0/R1 knowledge, `lane1+lane2` for R3 refund |
| `binding_depth` | int (1–2) | Maximum proof hops before returning UNKNOWN | `1` for most routes, `2` for decision-support |
| `fail_stance` | enum {open_annotate, closed_escalate} | Per-tier fail stance override (inherits from architecture default if not set) | R0/R1 default open; R2/R3 default closed |
| `policy_version` | semver | Which versioned policy DAG governs this route | `v2.3.1` |
| `entitlement_sources` | list[source_acl_spec] | Which source systems carry ACL metadata for this route | `[ { source: "policy_repo", acl_field: "role" }, { source: "hr_wiki", acl_field: "dept" } ]` |
| `claim_type_weights` | map[claim_type → weight] | How claim types are weighted in the response verdict (worst claim, weighted by role in pending action) | `{ "policy_clause": 1.0, "numeric": 0.9, "entity": 0.8 }` |
| `edit_policy` | enum {strip, regenerate_once} | Whether surgical edit removes the failing claim or re-invokes the generator once | `strip` for knowledge, `regenerate_once` for refund |
| `shadow_mode` | bool | Whether this route is in shadow (observe-only) or enforcement mode | `true` at deployment, `false` after earning enforcement through shadow evidence |
| `regulatory_posture` | list[jurisdiction_spec] | Applicable regulatory frameworks | `[ { jurisdiction: "EU", framework: "GDPR" }, { jurisdiction: "IN", framework: "DPDPA" } ]` |
| `audit_retention_days` | int | How long the Evidence Ledger is retained for this route | `90` (default), `365` for regulated routes |

### How the Matrix Is Applied Without Becoming a Different Product

The matrix is identical on every route. What varies is the **R-tier assignment per pending action**, which is a configuration decision, not an architectural one. The interlock reads the route configuration to determine the R-tier for each pending action in the response, then applies the frozen matrix cell. The matrix itself is never per-route — it is the same 4×4 grid everywhere.

Concretely: the refund route assigns R1 to "show text to customer" and R3 to "issue refund." The knowledge route assigns R0 or R1 to "show answer." The claims copilot assigns R2 to "show recommendation" and R3 to "auto-approve." In every case, the interlock computes R from the route configuration's `action_tiers` map, looks up the verdict severity from the binding engine's output, and reads the matrix cell. The matrix is a constant; the route configuration is the variable.

This is the architectural answer to the one-size-fits-all problem: **the matrix is one-size-fits-all; the R-tier assignment is per-route.** Collapsing them would mean per-route matrices, which means forking the decision policy, which means losing the single-graph invariant. The route configuration object is the controlled surface that absorbs all the variation the enterprise needs without touching the engine.

### Multi-Turn and Compounding Risk

Multi-turn conversations and action-taking agents introduce compounding risk: one unproven claim in turn N can authorise a tool call in turn N+1 that produces a span in turn N+2 that grounds a claim in turn N+3. The graph handles this by construction — each turn appends to the same Evidence Ledger, and the `STEP → SPAN → CLAIM → ACTION` chain is cumulative across turns. The interlock evaluates each pending action against the ledger state at the time the action is requested, not at the time the conversation started.

The critical rule: **a claim that was UNSUPPORTED in turn N does not become SUPPORTED in turn N+3 just because a new span appeared.** The binding is recomputed against the current span set, but the verdict is per-claim, not per-conversation. If a tool call in turn N+1 produces a span that would have supported the claim from turn N, the claim can be re-evaluated — but only if the route configuration explicitly enables re-evaluation (a boolean flag, defaulting to false for safety-critical routes). This prevents the common failure mode where an agent "recovers" from an unproven claim by generating its own evidence.

For the prototype, multi-turn is not demonstrated (Stage 1 freeze). The architecture supports it through the cumulative ledger; the business proposal describes the re-evaluation policy.

---

## 3. Governance & Policy Layer

### Policy Surface

The governance layer is a **versioned DAG of policy rules**, where each rule is a 4-tuple:

```
(signal, threshold, action, latency_budget)
```

The signal is drawn from the Evidence Ledger — never from a model's self-reported confidence. The threshold is a typed value (numeric, boolean, enum) calibrated per route. The action is one of the four frozen actuators (Block, Edit, Escalate, Pass) plus autonomy downgrade and circuit breaker. The latency budget is the maximum time the rule may consume before the interlock decides on whatever is in the ledger.

The policy DAG is **versioned** with semantic versioning. Every version is immutable once deployed — no in-place edits. A new version is created, validated, and promoted through the deployment pipeline.

### Per-Route Policy Configuration

Each route's `policy_version` field points to a specific version of the policy DAG. This allows:

- **Different risk appetite per route.** A customer-facing refund route may set a lower threshold for UNSUPPORTED + categorical at R3 (always Escalate), while an internal knowledge route may tolerate a higher threshold for UNSUPPORTED + hedged at R1 (Pass + annotate). The matrix cells are the same; the thresholds that classify a claim as "categorical" vs "hedged" may differ.
- **Different regulatory posture per geography.** A route serving EU customers inherits GDPR-specific audit trail requirements (longer retention, explicit consent logging). A route serving Indian operations inherits DPDPA requirements. The policy DAG carries these as tagged branches, not separate engines.
- **Different latency lanes per route.** A real-time customer-facing route runs Lane 1 (deterministic) as the default, with Lane 2 (NLI) reserved for high-R claims. An asynchronous batch decision-support route may run Lane 2 as the default because latency is less constrained.

### Policy Validation Before Deployment

No policy change reaches live traffic without passing through a three-stage validation pipeline:

1. **Schema validation.** The new policy version must parse against the rule schema. Malformed rules are rejected at commit time.
2. **Shadow replay.** The new policy version is applied to the last N traces (configurable, default 1000) from the target route in shadow mode. The output is a diff: how many decisions would have changed, broken down by actuator type. The diff is reported as FP/FN delta with confidence intervals.
3. **Canary deployment.** If the shadow replay passes the team's acceptance criteria (configurable per route), the new policy version is deployed to a canary slice of traffic (default 10%). The canary runs for a configurable window (default 24 hours). If the human-override rate on the canary exceeds 3× the baseline override rate for that route, the canary auto-rolls back to the previous version.

The entire pipeline is logged to the append-only ledger. Every policy version, shadow replay result, canary deployment, and rollback is auditable.

### Audit Trail

Every decision written to the Evidence Ledger carries:

- The exact policy version that governed the decision
- The verifier versions (claim extractor model version, NLI model version, rule engine version)
- The principal (caller identity)
- The source identifiers and ACLs of every span in the provenance set
- The content hash of every span
- The latency spent per lane

The ledger is append-only and hash-chained — each entry includes the hash of the previous entry, making tampering detectable. Retention is per-route, governed by the route configuration's `audit_retention_days` field, and must meet the minimum required by the route's `regulatory_posture`.

### Zero LLM at Decision Time

The policy engine is a pure rule engine. No LLM call occurs between the Evidence Ledger being populated and the actuator being emitted. The claim extractor and NLI cross-encoder run upstream of the decision; the interlock reads their outputs as typed values, not as natural-language opinions. This is a hard architectural constraint, not a preference — it is what makes the decision auditable and deterministic for the majority of traffic.

---

## 4. Feedback & Learning Loops

### What Is Learned

The system learns **thresholds and calibrations**, not models or decision logic. Specifically:

**Per-route binding thresholds.** The entailment confidence threshold that separates SUPPORTED from UNSUPPORTED for textual claims is calibrated per route using the adjudicator's shadow audit data. As the shadow audit accumulates ground-truth labels, the threshold is adjusted to minimise the per-route FNR while keeping the FP rate below a configurable ceiling. This is a statistical calibration, not a model retraining — the NLI model is fixed; only the decision threshold moves.

**Per-route claim-type weights.** The weights that determine how different claim types contribute to the response verdict are calibrated from override data. If clinicians or adjusters consistently override the system on a specific claim type (e.g., hedged policy claims), the weight for that claim type is adjusted upward, causing the system to be more conservative on that type. This is a feedback-driven parameter update, not a model update.

**Route cost baselines.** The streaming median + 3.5×MAD baselines for step yield, token spend, and latency are updated continuously from production traces. Cold-start windows are excluded. These baselines feed the economist's dead-compute and non-convergence detection.

### What Remains Rule-Based

The following are never learned from data and remain as configured, versioned rules:

- The R×S matrix. The matrix is transcribed, never redrawn. No amount of override data changes the matrix cells.
- The entitlement/ACL check. Set-membership against caller identity and source ACL is deterministic and not subject to calibration.
- The fail stance per blast-radius tier. R0/R1 fail open with annotation; R2/R3 fail closed or escalate. This is a design decision, not a learned parameter.
- The actuator set. Block, Edit, Escalate, Pass are the only actuators. No new actuators are learned from data.
- The default = UNSUPPORTED invariant. Every claim starts UNSUPPORTED. No feedback loop can change this default.

### What Is Never Learned From

- **Overridden escalations where the human provides no structured feedback.** An override without a reason code is logged but does not feed calibration. Unstructured overrides are noise.
- **Passes that were never audited.** A claim that passed without being sampled by the adjudicator provides no ground-truth signal. The system does not assume that unaudited passes are correct.
- **Model self-reported confidence.** The generator's confidence, logprobs, or verbalised hedging are never used as a training signal for any system parameter. The named failure mode is confidently wrong; confidence is the broken instrument.
- **Composite scores from other tools.** If the enterprise runs a separate guardrail or observability tool, its scores are not ingested as feedback. The control plane's feedback loop is closed on its own evidence and its own adjudicator's ground truth.

### Human Override Capture

When a human overrides a decision (e.g., a clinician overrides an Escalate to approve, or an adjuster overrides a Pass to hold), the system logs:

- The override type (approve-hold, hold-approve, edit-accept, edit-reject)
- The human's identity and role
- The original decision, the matrix cell, and the evidence packet
- An optional structured reason code (from a controlled vocabulary per route)
- Timestamp

Overrides feed the calibration loops described above. The override rate itself is a monitored metric — a sustained increase in override rate on a route triggers a policy review, not an automatic threshold change.

---

## 5. Metrics, Monitoring & Trustworthiness Reporting

### Per-Route False-Negative Rate (The Credibility Move)

The FNR is measured by the **stratified shadow audit**. The methodology:

1. **Sample definition.** For each route, the audit samples 100% of decisions that resulted in Block or Escalate, plus a configurable random slice (default 10%) of decisions that resulted in Edit or Pass + annotate, plus a smaller random slice (default 2%) of Pass decisions.
2. **Ground-truth labelling.** Each sampled decision is sent to an expensive, more thorough verification path — a slower, deeper binding check, potentially with human adjudication. This produces a ground-truth label for each sampled claim.
3. **FNR computation.** The FNR is the proportion of ground-truth ungrounded claims that the inline system classified as SUPPORTED or allowed to Pass. Reported per route, per claim type, with a confidence interval (Wilson score interval, 95%).
4. **Reporting.** The per-route FNR is published as a typed schema:

```
{
  route_id: string,
  sample_period: { start: timestamp, end: timestamp },
  sample_definition: { block_escalate: "100%", edit_pass_annotate: "10%", pass: "2%" },
  ground_truth_method: "expensive_binding + human_adjudication",
  total_sampled: int,
  ground_truth_ungrounded: int,
  system_missed: int,
  fnr: float,
  fnr_ci_95: { lower: float, upper: float },
  status: "measured" | "insufficient_sample" | "not_yet_populated"
}
```

Where trustworthy ground truth is unavailable (insufficient sample size, cold start), the `status` field is `"not_yet_populated"` and the `fnr` field is `null`. **The emptiness is the credibility play.** A judge who tests it finds honesty rather than a bluff. The prototype displays this schema with null/placeholder values or labelled prototype-corpus values only.

### False-Positive / Override Rates

- **FP rate per route.** The proportion of decisions that resulted in Block or Escalate where the ground-truth label (from the shadow audit) indicates the claim was actually SUPPORTED or the action was actually safe. Reported per route, per actuator type, with confidence intervals.
- **Override rate per route.** The proportion of decisions that a human overrode. Reported per route, per override type. A sustained override rate above a configurable threshold (default 3× baseline) triggers a policy review alert.
- **Alert fatigue indicator.** The ratio of total flagged/escalated decisions to total decisions on the route. If this ratio exceeds a configurable ceiling (route-specific, default 5%), the route is flagged for threshold recalibration. This is the explicit metric for the over-flagging problem — the system monitors its own noise level.

### Dead Compute

Measured exactly by walking the graph backward. For each request:

1. Identify every SUPPORTED claim in the accepted answer.
2. Trace each to the span that grounded it.
3. Trace each span to the step that produced it.
4. Any step that grounded zero accepted claims is dead compute.

Reported per route as:

```
{
  route_id: string,
  period: { start: timestamp, end: timestamp },
  total_steps: int,
  dead_steps: int,
  dead_compute_ratio: float,
  estimated_wasted_tokens: int,
  estimated_wasted_cost: currency
}
```

This is the number a buyer signs a cheque against. No competitor has it, because no competitor has the graph.

### Latency by Lane

Reported per route, per lane:

| Lane | What It Measures | Target |
|---|---|---|
| Lane 1 (inline, deterministic) | Span membership, ACL, typed interlocks, arithmetic, Aho-Corasick PII | ≤40ms p50, ≤200ms p95 |
| Lane 2 (near-line, NLI) | NLI binding for flagged claims and high-R traffic | 100–400ms |
| Lane 3 (async) | Semantic-entropy, counterfactual bias replay, calibration, shadow replay | Off critical path; measured but not gated |

The prototype reports measured demo latency. The business proposal reports production targets. **Never quote 40ms as p95.**

### Entitlement Violations

Reported per route as a count and rate:

```
{
  route_id: string,
  period: { start: timestamp, end: timestamp },
  total_claims_checked: int,
  entitlement_violations: int,
  entitlement_violation_rate: float,
  violations_by_source: map[source_id → int]
}
```

This metric is the operational proof that the entitlement check is working — and the detector for over-permissioned indices. A high violation rate on a specific source is exactly what an over-permissioned RAG index looks like from the inside.

### Trustworthiness Reporting to a Sceptical Stakeholder

The reporting surface is designed for a stakeholder who does not trust the system's own claims. The design principle: **publish what we miss, not just what we catch.**

The stakeholder sees:

1. **Per-route FNR schema** — with nulls where ground truth is insufficient. The schema itself is the claim: we know exactly which fields are knowable at design time and which are not.
2. **Override rate trend** — is the human override rate increasing, stable, or decreasing? An increasing trend means the system is either degrading or the policy needs recalibration.
3. **Dead compute ratio** — how much of the enterprise's AI spend grounded nothing? This is a cost number, not a safety number, and it is the one that gets executive attention.
4. **Entitlement violation count** — how many times did the system catch an ACL violation that would otherwise have been silently leaked? This is the number that justifies the integration cost.
5. **Policy change log** — every policy version, shadow replay result, canary deployment, and rollback. The stakeholder can audit the governance process, not just the outcomes.

No composite 0–100 score. No "trust score." No "responsible AI" dashboard. The reporting surface is a set of typed, auditable metrics — one per concern — that a sceptical engineer can verify against the Evidence Ledger.

---

## 6. Complete Enterprise Solution vs Prototype

### What the Full Enterprise Solution Contains

| Component | Description | Status |
|---|---|---|
| Multi-route deployment | Same engine, per-route configuration objects, policy DAG versioning | Architecture defined; prototype shows two routes |
| Governance & policy layer | Versioned policy DAG, shadow replay validation, canary deployment, auto-rollback | Architecture defined; prototype shows one policy version |
| Feedback & calibration loops | Per-route threshold calibration from shadow audit data, override-driven weight adjustment, cost baseline updates | Architecture defined; prototype shows override capture only |
| Stratified shadow audit | 100% of blocks/escalations + random slice of passes → expensive ground truth → per-route FNR with CI | Architecture defined; prototype shows the FNR schema as empty/placeholder |
| Dead compute measurement | Backward graph walk, per-route waste reporting | Architecture defined; prototype may show a brief backward walk if time permits |
| Multi-turn compounding risk | Cumulative Evidence Ledger across turns, re-evaluation policy, unproven-claim persistence | Architecture defined; not demonstrated in prototype |
| Async bias measurement | Route-level counterfactual flip-rate with CI over rolling window, protected-attribute perturbation | Architecture defined in business proposal; not a live prototype actuator |
| Regulatory posture packs | Per-jurisdiction policy branches (GDPR, DPDPA, sector-specific), retention, consent, audit trail requirements | Architecture defined; prototype shows one default posture |
| Scalability & deployment | OpenAI-compatible reverse proxy + SDK hook, horizontal scaling, per-tenant isolation | Architecture defined; prototype is single-node |
| Circuit breaker & autonomy downgrade | Per-route error budget, SRE-style sliding window, automatic tier demotion | Architecture defined; prototype may narrate but does not demo |
| Red Team (offline) | Adversarial probing of ControlPlane's own validators | Architecture defined; offline only, not demonstrated |
| Entitlement violation analytics | Per-source violation counts, over-permissioned index detection | Architecture defined; prototype shows one violation |

### What the Stage 1 Prototype Deliberately Shows

Per the frozen R2S1 §3:

1. Context-assembly provenance capture (keystone)
2. One request → one typed Evidence Ledger (STEP → SPAN → CLAIM → ACTION)
3. Default = UNSUPPORTED enforced
4. Claim-type routing (numeric → deterministic, textual → NLI binding, derived → UNKNOWN)
5. Deterministic entitlement enforcement (zero LLM in ACL path)
6. Exact frozen R×S matrix applied per pending action
7. Two-pending-actions centrepiece (R1 Edit + R3 Escalate on refund)
8. Hard gate on actions, not tokens
9. Surgical Edit
10. Evidence-packet Escalation
11. Published own FNR as a format (empty schema / placeholder)
12. Measurement surface from the Evidence Ledger
13. Optional principal-flip entitlement replay

### What Remains Proposal-Only

| Item | Why It Is Proposal-Only |
|---|---|
| Async counterfactual bias measurement | Distributional property; requires rolling window; cannot be shown on a single trace; contaminates the claim→action critical path if forced into the live demo |
| Multi-turn compounding risk demonstration | Requires multi-step agent traces; the prototype uses single-turn traces; the architecture supports it through the cumulative ledger |
| Production-scale throughput (tens of thousands/week) | Round 2 allows limited/simulated scope; scale is a deployment claim, not a mechanism claim |
| Full regulatory compliance certification | Versioned policy configuration is shown; jurisdiction-specific packs are described in the proposal |
| Dead compute as centrepiece | Valid graph read but secondary to admission control; may be narrated briefly if it does not crowd the dual-action |
| Circuit breaker and autonomy downgrade in action | SRE-style error budget mechanism; described in proposal; the prototype focuses on the matrix, not on operational resilience |
| Policy validation pipeline (shadow replay → canary → auto-rollback) | Governance mechanism; described in proposal; the prototype shows one policy version applied |
| Lane 3 mechanisms (semantic-entropy, counterfactual replay, calibration) | Off the critical path by construction; described in proposal |

---

## 7. Residual Risks & Explicit Mitigations

### Risk 1: False Assurance on Derived Claims

**The risk.** Multi-hop, aggregated, and synthesised claims are where entailment is weakest. If the NLI cross-encoder marks a subtly-wrong synthesised claim SUPPORTED because a shallow span looks similar, ControlPlane delivers false assurance — strictly worse than no control plane, because humans stop checking.

**Mitigation (three lines, as stated in Architecture §7):**

1. **Route derived claims away from NLI entirely.** Arithmetic or aggregative claims are recomputed from spans. Claims neither recomputable nor directly entailed return UNKNOWN. UNKNOWN never collapses into SUPPORTED — that one rule is the boundary between a control plane and false assurance.
2. **Decorrelate by construction.** Verifiers come from a different model family than the generator. Deterministic checks carry the majority of enforcement weight precisely because they cannot share the generator's failure modes.
3. **Publish the plane's own error bars.** Stratified shadow audit — 100% of blocks and escalations plus a random slice of passes — sampled to expensive ground truth. The per-route FNR schema is the published format.

**Residual after mitigation.** The risk is not eliminated; it is bounded and measured. The claim is never "we catch hallucinations." It has the shape: "On this route we catch X% of ungrounded claims at 40ms p50 — and here is the Y% we don't."

### Risk 2: Over-Permissioned Source Indices Undermining Entitlement

**The risk.** ControlPlane enforces the ACLs carried by the source system. If the source system's ACLs are wrong (over-permissioned), ControlPlane faithfully enforces a wrong policy. The system does not fix IAM — it makes violations visible.

**Mitigation:**

1. **Entitlement violation analytics.** Per-source violation counts are reported. A high violation rate on a specific source is the operational signal that the source's ACLs need remediation. The system does not fix IAM; it detects when IAM is broken.
2. **Every entitlement decision is logged against a named principal and a named source.** The audit trail makes over-permissioning forensic — an auditor can trace every decision back to the specific ACL that allowed or denied it.
3. **The query-time check is the detector.** A span sitting in provenance whose ACL excludes the caller is exactly what an over-permissioned index looks like from the inside. The system does not need to audit the index; it audits the decisions.

**Residual after mitigation.** The risk is not eliminated; it is surfaced. The enterprise must fix its own IAM. ControlPlane stops IAM failures from being silently bypassed by a model.

### Risk 3: Alert Fatigue from Over-Escalation on High-Volume R0/R1 Routes

**The risk.** If the UNSUPPORTED default and the claim extractor are too aggressive on high-volume, low-risk routes (internal knowledge assistant), the system escalates or annotates too many responses, creating alert fatigue. Users ignore or bypass warnings, and the team switches the system off — the fate of every guardrail.

**Mitigation:**

1. **The matrix is deliberately graduated.** R0/R1 traffic with unsupported hedged claims gets Pass + annotate or Pass — not Escalate. The matrix exists specifically to prevent over-blocking on low-risk routes. The R-tier assignment in the route configuration determines how aggressively the system acts.
2. **Check-worthiness filtering.** The claim extractor's first job is to determine whether a claim is worth checking at all. Trivially true claims, boilerplate, and hedged filler are filtered before any binding runs. This removes the largest false-positive class before any model call.
3. **Alert fatigue indicator.** The system monitors its own noise level per route. If the ratio of flagged/escalated decisions to total decisions exceeds a configurable ceiling (default 5%), the route is flagged for threshold recalibration. The system does not wait for humans to complain; it measures its own noise.
4. **Shadow mode is the default.** Enforcement is earned per route through shadow evidence. Nobody is asked to trust the system before it has produced its own counterfactual — "would have held N, of which M were true positives." The counterfactual is the evidence that earns enforcement.
5. **R0/R1 traffic passes with annotation, not blocking.** The overwhelming majority of volume (80–90%) is R0/R1. On these routes, the system annotates rather than blocks. The user sees the annotation and can ignore it without the system preventing them from working. This is the design choice that prevents the team from switching it off.

**Residual after mitigation.** The risk is managed, not eliminated. Per-route calibration is a continuous process. The override rate and alert fatigue indicator are the leading signals.

---

## 8. Fidelity Self-Check

| Frozen Invariant | Status | Evidence in This Expansion |
|---|---|---|
| **Default = UNSUPPORTED** | Untouched. | §2: "every claim starts UNSUPPORTED and must earn proof." §4: "No feedback loop can change this default." |
| **Entitlement / ACL check** | Untouched. | §2: "Deterministic set-membership: caller principal vs source ACL on every span that binds to a claim. Zero LLM." §7 (Risk 2): entitlement violation analytics, audit trail, query-time check as detector. |
| **Exact R×S matrix** | Untouched. | §2: "The matrix is identical on every route." "The matrix is transcribed, never redrawn." "Axis labels, column vocabulary, and cell values are load-bearing." §4: "The R×S matrix... is never learned from data." |
| **Hard gate on actions, not tokens** | Untouched. | §2: "The interlock evaluates each pending action against the ledger state at the time the action is requested." §6: prototype shows "Hard gate on actions, not tokens." |
| **Published FNR as a format** | Untouched. | §5: Full FNR schema defined with typed fields. "Where trustworthy ground truth is unavailable... the fnr field is null. The emptiness is the credibility play." §6: prototype shows "empty schema / placeholder." |
| **Two-pending-actions resolution** | Untouched. | §2: "the refund route assigns R1 to 'show text to customer' and R3 to 'issue refund.'" §6: prototype shows "R1 Edit + R3 Escalate on refund." |
| **No LLM-as-judge on critical path** | Untouched. | §3: "The policy engine is a pure rule engine. No LLM call occurs between the Evidence Ledger being populated and the actuator being emitted." |
| **No composite risk score** | Untouched. | §5: "No composite 0–100 score. No 'trust score.'" §4: "Composite scores from other tools... are not ingested as feedback." |
| **No per-response bias verdict** | Untouched. | §6: "Async counterfactual bias measurement... not a live prototype actuator." §4: bias is not listed in "What Is Learned" — it is a distributional measurement, not a per-response classification. |
| **Surgical edit only** | Untouched. | §2: route configuration includes `edit_policy` with values `strip` or `regenerate_once`. No free-form rewrite. |
| **Evidence-packet escalation** | Untouched. | §6: prototype shows "Evidence-packet Escalation." §5: override capture logs "the original decision, the matrix cell, and the evidence packet." |
| **One graph, three reads** | Untouched. | §2: "Every route in the enterprise shares the same core structure. There is one graph, one Evidence Ledger schema." |

**No competing mechanism enters the architecture.** LLM-as-judge, confidence thresholding, composite risk scores, open-web truth layers, per-response bias classifiers, and redrawn matrices are all absent. The expansion adds configuration, governance, feedback, and measurement — not new detectors.

**Deliberate scope tension (resolved in favour of the freeze):** The official brief names bias, hallucination, and privacy as overlapping risks. The frozen architecture separates them: hallucination is per-claim binding, privacy/leakage is per-claim entitlement, bias is per-route async counterfactual measurement. The overlap is acknowledged (a fabricated detail about a person can be both a hallucination and a privacy concern) and handled by the claim extractor emitting both a factual claim and an entity claim for the same sentence — each routed through its own mechanism. The mechanisms are different because the failure modes are different, even when they co-occur in the same sentence. Collapsing them into one detector is the generic move; the architecture refuses it.

---

*Stage 2 complete. The frozen core is preserved without exception. The expansion adds configuration, governance, feedback, and measurement — the surfaces an enterprise needs to deploy one graph across many routes — without inventing a single new detector or softening a single invariant.*