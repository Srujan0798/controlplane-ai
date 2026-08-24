# Stage 2: Expanded Solution Architecture

> Accenture Innovation Challenge 2026 · Round 2 · Stage 2  
> Sources of truth: `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` (frozen)  
> Status: **FROZEN Stage 1 inputs are non-negotiable.** This document extends; it does not overwrite.

---

## 1. Expanded Core Thesis

The frozen admission-control layer scales across heterogeneous enterprise routes not by adding detectors but by configuring the same graph reads: each route declares its blast-radius mapping, entitlement sources, and lane budget, and the identical `STEP → SPAN → CLAIM → ACTION` primitive produces different actuators on different routes without becoming a different product. The single sharpest differentiator — provenance captured outside the model, inverted burden of proof, deterministic entitlement, blast-radius-priced verification — is structurally preserved because it lives in the graph primitive and the matrix, neither of which is route-configurable. The enterprise system is one graph engine reading one matrix across many routes; the variety is in the inputs, not the mechanism.

---

## 2. Multi-Route Architecture

### What is shared (identical across every route)

| Shared component | Why it must be shared |
|---|---|
| The graph primitive: `STEP → SPAN → CLAIM → ACTION` | This is the control plane. Fork it and it is three classifiers in a trench coat. |
| The Evidence Ledger schema | One append-only, hash-chained structure per request. All three reads (performance, cost, responsibility) operate on this single artifact. |
| The verdict set: `SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN` | A claim leaving one route and entering another carries its verdict. The vocabulary must be identical. |
| The R×S matrix | Transcribed, never redrawn. Routes provide R; evidence provides S; the matrix emits the actuator. The matrix is a pure function — it has no route parameter. |
| The four actuators: `Block · Edit · Escalate · Pass` | Plus autonomy downgrade and circuit breaker (spoken architecture, not invented demo labels). |
| Claim-type routing | Numeric/structural/temporal → deterministic recomputation. Textual/factual → NLI binding against provenance set only. Derived/multi-hop → recompute from spans or `UNKNOWN`. This routing is not a tuneable knob. |
| The entitlement check | Caller principal vs. source ACL, set-membership, Lane 1, zero LLM. Not configurable per route — only the *sources* of ACLs are route-configured. |
| `UNKNOWN` never collapses into `SUPPORTED` | Structural invariant. No policy change, route configuration, or threshold adjustment can violate this. |
| Fail stance per tier | R0/R1 fail open with annotation; R2/R3 fail closed or escalate. Not a global default — but the tier-to-fail-stance mapping is shared. |
| Surgical edit rule | Strip the failing claim, or re-invoke once with constrained instruction naming the exact failing span. Edited output re-enters the gate. Second failure → Escalate. |
| Evidence-packet format for Escalate | Claim, candidate spans, verdict, diff. Identical structure across all routes. |
| Hard gate on actions, not tokens | Text streams with hold-back; actions gated at the commit boundary. |

### What is configured per route

| Per-route configuration | What it controls | Constraints |
|---|---|---|
| **Blast-radius mapping** | Which action patterns on this route map to which R-tier | Locked action classes (payment, deletion, publication, regulated advice) are forced to R3 by global invariant. Route can only map route-specific actions. |
| **Action grammar** | Allowed `tool × argument_schema × irreversibility` combinations | Allow-list only. Anything not listed fails at parse time. Adding a payment tool to an R1 route's grammar does not downgrade the payment's R-tier — the locked mapping overrides. |
| **Entitlement sources** | Which source system IDs feed ACLs for this route | The check mechanism is shared; the source set is route-specific. A knowledge-assistant route includes HR and engineering sources; a refund route includes vendor-agreement and order sources. |
| **Lane configuration** | Which lanes are active, and per-lane latency budget in ms | A pure R0 draft route may disable Lane 2 entirely (NLI never runs). An R3 route may increase Lane 2 budget. Lane 1 (deterministic) cannot be disabled. |
| **Claim extraction specificity** | What claim types are flagged as check-worthy on this route | E.g., a code-generation route may flag API-call claims; a refund route flags monetary amounts and policy clauses. Extraction is still by type, not by one universal detector. |
| **Enforcement mode** | `shadow` or `enforced` | Earned per route through shadow evidence. Cannot be set to `enforced` without meeting the earn-out criteria (minimum shadow window, FNR measured with sufficient sample, override rate within bounds). |
| **Override policy** | Which actuators a route-level operator can override, and the required authorization level | `Block` overrides require higher authorization than `Edit` overrides. `Escalate` overrides (human approving a held action) are always permitted — that is the designed workflow. |

### How the matrix applies without becoming a different product

The matrix is a pure function: `f(R, S) → actuator`. It has no route parameter. Routes do not customize the matrix; they customize the **inputs** to the matrix:

- **R is determined by the route's blast-radius mapping** applied to the pending action. The same "send email" action might be R1 on an internal draft route and R2 on a customer-facing route. The matrix cell changes because R changed — the matrix did not.
- **S is determined by the evidence** — the claim, the spans, the binding verdict, the entitlement check. These are route-independent facts. A claim that is unsupported-categorical is unsupported-categorical on every route.
- **The actuator is the matrix output.** The same R3 × unsupported-categorical produces Escalate on a refund route, on a decision-support route, and on any future route that carries an R3 action with an unsupported categorical claim.

This is why the system scales without becoming a different product: the configuration surface controls *what reaches the matrix*, not *what the matrix does*. A new route is a new set of blast-radius mappings, action grammars, and entitlement sources — not a new control logic.

### Multi-turn and compounding risk

The Evidence Ledger is per-request, but the provenance set **accumulates across turns** within a session. Spans captured in turn N remain available for binding claims in turn N+1. This is not a new mechanism — it is the graph primitive applied over a longer time horizon.

Compounding risk is handled by the existing architecture without extension:

- An unproven claim in turn 1 that passed with annotation (R0/R1) does **not** retroactively gain proof in turn 3. If turn 3's response uses that claim as the basis for an R3 action, the claim still has no supporting span, and the matrix still routes to Escalate.
- A claim that bound in turn 1 and was SUPPORTED carries its binding forward. If the underlying span is later determined to be from a poisoned source, the span's `source_id` and `content_hash` enable forensic tracing across all turns that consumed it — but this is an offline audit capability, not a live re-verification of historical turns.
- No "conversation-state validator" or "turn-level risk accumulator" is added. The graph is additive; the matrix is stateless per decision. Compounding risk is the same unproven claim reaching a higher-R action — and the existing mechanism already catches it.

---

## 3. Governance & Policy Layer

### Structure: versioned DAG of 4-tuples with global invariants

The policy engine evaluates rules of the form `(signal, threshold, action, latency_budget)` arranged in a DAG. This is already frozen in ARCHITECTURE.md §4. The expanded governance layer adds the configuration surface and the validation pipeline around it.

```
Policy Version: <content_hash>
│
├── GLOBAL INVARIANTS (not patchable, enforced at parse time)
│   ├── default_verdict = UNSUPPORTED
│   ├── UNKNOWN → SUPPORTED transition: FORBIDDEN
│   ├── entitlement_check: always active, Lane 1, zero LLM
│   ├── locked_action_classes → R3: [payment, deletion, publication, regulated_advice]
│   ├── R3 fail_stance = closed | escalate
│   └── matrix: immutable (transcribed, not configurable)
│
├── ROUTE DEFINITIONS
│   └── route_id: string
│       ├── blast_radius_map: {action_pattern → R_tier}
│       │   └── cannot override locked_action_classes
│       ├── action_grammar: [tool × schema × irreversibility]
│       ├── entitlement_sources: [source_system_id]
│       ├── lane_config: {lane_id: {enabled: bool, budget_ms: int}}
│       │   └── Lane 1 cannot be disabled
│       ├── claim_extraction_patterns: [claim_type_filter]
│       ├── enforcement_mode: shadow | enforced
│       │   └── enforced requires earn-out criteria met
│       └── override_policy: {actuator: {allowed: bool, auth_level: string}}
│
├── GEOGRAPHY PATCHES (additive only — cannot remove constraints)
│   └── geo_region: string
│       └── patch: {route_id → field_overrides}
│           └── overrides must pass invariant check
│           └── example: EU-GDPR → add PII entity classes to Aho-Corasick set
│
└── REGULATORY POSTURE TAGS (additive only)
    └── tag: string
        └── patch: {route_id → field_overrides}
            └── example: "financial-services" → external_send on PII → R3
```

### How behaviour varies by the four required dimensions

| Dimension | Mechanism | Example |
|---|---|---|
| **Use case / route** | Route definition block | Refund route: payment tool → R3, Lane 2 enabled, NLI budget 400ms. Knowledge route: no actions, Lane 2 disabled, Lane 1 only. |
| **Risk appetite** | Enforcement mode + override policy + Lane budget | Aggressive route: enforced mode, Lane 2 budget tight (200ms), Edit overrides allowed at L1. Conservative route: shadow mode, Lane 2 budget generous (400ms), no overrides without L3 approval. |
| **Geography** | Additive geography patch | EU-GDPR patch: adds named-entity PII classes to Aho-Corasick; any external send containing matched entities is re-mapped from R2 to R3. The patch cannot remove the entitlement check or soften the default. |
| **Blast-radius tier** | The matrix itself (shared, not configurable) + tier-specific fail stance | R0/R1: fail open with annotation. R2/R3: fail closed or escalate. This mapping is a global invariant — geography and route patches cannot change it. |

### Versioning and audit trail

- Every policy version is identified by a content hash of its full serialized form.
- Every decision in the Evidence Ledger carries `policy_version: <hash>`, making the decision reproducible under the exact rules that produced it.
- Policy versions are append-only. Old versions are retained for the retention period required by the governing jurisdiction (configured per geography patch). The ledger can be replayed against any historical policy version.
- A policy diff (version A → version B) is a typed change set: which route fields changed, which patches were added, which invariants were checked. The diff is itself hash-chained and append-only.

### Validation before live traffic

No policy change reaches enforcement mode without this pipeline:

```
Proposed change
    │
    ▼
Parse + invariant check ─── FAIL → reject (cannot activate)
    │
    ▼ PASS
Shadow replay over last N traces (N ≥ 1000 per affected route)
    │
    ▼
Compare actuator distribution: old policy vs new policy
    │
    ├── Block/Escalate rate drops > 30% → FLAG for human review
    ├── Block/Escalate rate increases > 50% → FLAG (possible over-correction)
    └── Within bounds → proceed
    │
    ▼
Canary deployment: 5% of traffic on affected route(s) under new policy
    │
    ▼
Monitor for canary window (configurable, minimum 24h or 5000 traces)
    │
    ├── Human-override rate exceeds 3× baseline → AUTO-ROLLBACK to previous version
    └── Within bounds → proceed
    │
    ▼
Human approval (named principal, recorded in policy ledger)
    │
    ▼
Promote to enforcement for canary shard
    │
    ▼
Gradual rollout: 25% → 50% → 100% (each step repeats canary monitoring)
```

**Zero LLM reasoning at decision time remains mandatory.** The policy engine evaluates 4-tuples against the Evidence Ledger. It does not interpret policy language, weigh competing objectives, or "decide what the policy means." Policy is declarative code, not prompt. If a policy author writes an ambiguous rule, it fails at parse time — it does not get interpreted by a model at inference time.

---

## 4. Feedback & Learning Loops

### What is learned (rule parameters calibrated from evidence)

| Parameter | Learned from | How | Bounds |
|---|---|---|---|
| Per-route NLI entailment threshold | Stratified shadow audit FP/FN rates | Automated adjustment within guard rails | Max step size per adjustment; minimum sample size (≥500 adjudicated claims per stratum); CI on FNR must narrow before any adjustment is applied |
| Per-route check-worthiness filter patterns | FP/FN samples from shadow audit | Human review of the FP sample (claims flagged but benign) and FN sample (claims missed) → pattern additions/removals | Automated pattern suggestion; human approval required for each change |
| Per-route dead-compute baseline | Continuous graph backward walk | Streaming median + 3.5×MAD over rolling window | Pure statistics, no learning in the ML sense |
| Action grammar allow-lists | Escalation outcomes + dead-compute analysis | If a specific `tool × schema` combination consistently escalates (high Escalate rate, low override-rejection rate), flag for review. If it consistently produces dead compute, flag for removal. | Human decides to add or remove; system flags, does not act autonomously |
| Per-route enforcement earn-out | Shadow mode counterfactual | Track "would have held N, of which M were true positives" over minimum window. When FNR is measured with sufficient sample and override rate is within bounds, system recommends enforcement mode. | Human approves the transition. System does not self-promote. |

### What remains rule-based (never learned, never calibrated by feedback)

- The R×S matrix
- The entitlement check logic (set-membership has no parameters)
- `UNKNOWN` never collapses into `SUPPORTED`
- Claim-type routing (numeric→deterministic, textual→NLI, derived→recompute or `UNKNOWN`)
- The surgical edit rule (strip or single constrained re-invocation)
- Fail stance per tier
- Evidence-packet format
- The requirement that enforcement is earned per route before activation

### What is never learned from

| Never learned from | Why |
|---|---|
| Human overrides that approve an Escalated action | The override is a human decision, not a training signal. The system does not become more permissive over time because "humans keep approving these." |
| The content of escalated claims | The evidence packet is a human decision aid. It is not fed into a model that learns to auto-approve similar cases. |
| User acceptance rates of annotated (Pass + annotate) outputs | The system does not learn that "users don't mind unsupported claims on this route" and relax the default. |
| Model outputs (generator or verifier) | The control plane never feeds outputs back into a training loop. The generator is a black box by design. |
| Override rejection rates as a signal to tighten | If humans reject many overrides, the system flags it for review. It does not automatically tighten thresholds — because the direction of the error (too permissive vs. too strict) requires human judgment about the route's risk appetite. |

### The structural distinction

The learning loop is **calibration**, not adaptation. The mechanisms stay fixed; the thresholds on the probabilistic paths (NLI entailment, check-worthiness filtering) are calibrated against measured error rates within declared bounds. The deterministic paths (entitlement, arithmetic recomputation, typed interlocks) have no thresholds to calibrate. A control plane's behaviour is determined by its rules and its inputs. A trained model's behaviour is determined by its weights. This system has rules, not weights.

---

## 5. Metrics, Monitoring & Trustworthiness Reporting

### Per-route false-negative rate (the credibility move)

**Definition:** Among claims that the plane passed as `SUPPORTED` or routed to `Pass + annotate`, the fraction that would have been judged `UNSUPPORTED` or worse by the expensive ground-truth path.

**Measurement method: stratified shadow audit.**
- 100% of holds and escalations are sampled to ground truth (they are already flagged; the marginal cost is the ground-truth verification).
- A random slice of passes (configurable rate, minimum 5% per route per window) is also sampled.
- Ground truth = a slower, more thorough verification path: human expert review for high-R routes; a high-compute multi-verifier ensemble (multiple NLI models from different families, plus deterministic recomputation on a wider span set) for lower-R routes. The ground-truth method is authoritative for measurement purposes only — it never runs on the critical path.

**Reporting format** (the empty schema from the prototype, now with the measurement method specified):

```json
{
  "route_id": "refund-agent-emea",
  "measurement_window": {"start": "<ISO8601>", "end": "<ISO8601>"},
  "sample_size": null,
  "stratification": ["claim_type", "verdict_at_gate", "R_tier"],
  "fn_rate": {
    "value": null,
    "ci_lower": null,
    "ci_upper": null,
    "measurement_status": "insufficient_sample"
  },
  "fp_rate": {
    "value": null,
    "ci_lower": null,
    "ci_upper": null,
    "measurement_status": "insufficient_sample"
  },
  "ground_truth_method": "human_expert_review | multi_verifier_ensemble",
  "policy_version_at_measurement": "<content_hash>",
  "minimum_sample_for_measurement": 500,
  "maximum_ci_width_for_measurement": 0.05
}
```

**Population rules:**
- Value fields start `null`. They become populated only when sample size ≥ minimum and CI width ≤ maximum.
- They transition to `"stale"` if no new measurement is taken within a configured window (e.g., 7 days).
- A stakeholder sees either a measured number with a confidence interval, or `"insufficient_sample"` / `"stale"` — never a fabricated estimate, never an interpolated number.

### False-positive and override rates

| Metric | Definition | Granularity |
|---|---|---|
| Override rate | Fraction of non-`Pass` actuators overridden by a human operator | Per route, per actuator (Edit / Escalate / Block separately — they have different costs) |
| Auto-rollback rate | Fraction of policy changes auto-rolled back during canary | Per route, per policy change |
| Override rejection rate | Fraction of overrides where the human, after seeing the evidence packet, decided **not** to proceed | Per route, per actuator — distinguishes "humans keep overriding" from "humans override then agree the plane was right" |

### Dead compute

| Metric | Definition | Computation |
|---|---|---|
| Dead-compute amount | Total step-cost (tokens, tool calls, retrieval calls) minus cost of steps that grounded ≥1 accepted claim | Exact: walk the graph backward per request |
| Dead-compute fraction | Dead-compute amount / total step-cost | Per route, per request |
| Dead-compute trend | Streaming median + 3.5×MAD of dead-compute fraction over rolling window | Per route |

### Latency by lane

| Metric | Granularity |
|---|---|
| p50, p95, p99 of time spent in each lane | Per route, per lane |
| Timeout rate: fraction of checks that exceeded lane budget and fell to `UNKNOWN` | Per route, per lane |

### Entitlement violations

| Metric | Purpose |
|---|---|
| Violation count and rate per route | Operational volume of entitlement failures |
| Violation count per source system | **Over-permissioned index detector**: if source X consistently produces violations across multiple principals, the index is likely over-permissioned. This is the operational signal that QA.md B4 describes. |
| Violation count per principal | Anomalous access pattern detection |
| Violation count per `source_id × principal` pair | The most granular audit point — which person was denied access to which specific document |

### How a sceptical stakeholder is shown the plane measures its own misses

The dashboard's primary surface is the per-route FNR schema. Every other metric is secondary and accessible via drill-down.

The stakeholder sees:

1. **Which routes have measured FNR** (value + confidence interval) and which are `"insufficient_sample"` or `"stale"`. Routes in shadow mode that haven't earned enforcement will show `"insufficient_sample"` — this is honest and expected.
2. **The trend**: is the FNR CI narrowing, stable, or widening over successive measurement windows?
3. **The ground-truth method**: what expensive path produced the authoritative label? This is disclosed so the stakeholder can evaluate the measurement quality.
4. **The policy version at measurement time**: was this measured under the same rules currently enforced?
5. **Drill-down to the underlying sample**: the specific claims that were passed but flagged as false negatives by ground truth, with their full Evidence Ledger entries — the claim text, the spans checked, the binding result, the verdict, the matrix cell, the actuator that was applied.

This is not a dashboard that says "we're 97% accurate." It is a dashboard that says: *"On this route, in this window, we missed X% of ungrounded claims [CI: Y%–Z%]. Here are the specific claims. Here is what the plane did. Here is why it didn't catch them."* The stakeholder can evaluate the measurement, attack the method, and disagree with the ground-truth label — all of which are legitimate and all of which are possible because the evidence is exposed, not hidden behind a composite score.

---

## 6. Complete Enterprise Solution vs. Prototype

### Full solution contains (not all demonstrated live)

**Core mechanism (prototype demonstrates):**
- One-graph construction (`STEP → SPAN → CLAIM → ACTION`)
- Default = `UNSUPPORTED` → claim must earn `SUPPORTED`
- Claim-type routing (numeric→deterministic, textual→NLI, derived→recompute or `UNKNOWN`)
- Deterministic entitlement check
- Exact R×S matrix producing multiple actuators on one response
- Hard gate on actions, hold-back on text
- Surgical edit and evidence-packet escalation
- Per-claim user surface (`Verified / Uncertain / Blocked`)
- Empty FNR schema

**Enterprise scaling (proposal-only):**
- Multi-route policy engine with versioned DAG, geography patches, regulatory posture tags, global invariants
- Per-route blast-radius mapping and action grammar configuration
- Shadow mode with counterfactual recording (gated-vs-ungated dual-emit)
- Per-route enforcement earn-out (shadow evidence threshold before enforcement activates)
- Stratified shadow audit pipeline with expensive ground-truth path
- Per-route FNR, FP, override, dead-compute, latency-by-lane, entitlement-violation metrics with populated values
- Policy change validation: shadow replay → canary → auto-rollback → human approval → gradual rollout
- Circuit breaker per route (SRE-style error budget on gate-fail rate)
- Non-convergence breaker (cost lane — terminates runaway agent loops)
- Async counterfactual bias measurement (route-level, decision flip rate with CI, off critical path)
- Multi-turn provenance accumulation across conversation sessions
- Append-only hash-chained decision ledger with policy version
- OpenAI-compatible reverse proxy with per-route sharding
- Context-assembly SDK hook distribution to application teams
- Enterprise integration: principal resolution from identity provider, ACL ingestion from source systems

### Stage 1 prototype deliberately shows (live)

Exactly the items listed in R2S1 §3 "Will Demonstrate" and §5 "Success Criteria." No more, no less. The prototype's job is to make the graph and the matrix undeniable. The proposal's job is to show how they scale.

### Proposal-only (described in business proposal, never demonstrated live)

- Multi-route policy configuration surface and geography patches
- Shadow mode and counterfactual recording at enterprise scale
- Per-route enforcement earn-out workflow
- Stratified shadow audit pipeline and FNR measurement methodology
- Policy change validation and rollout pipeline
- Circuit breaker and non-convergence breaker
- Dead-compute measurement and cost reporting
- Async counterfactual bias measurement
- Multi-turn provenance accumulation
- Production deployment topology
- Enterprise identity and ACL integration
- Phased roadmap and business case

---

## 7. Residual Risks & Explicit Mitigations

### Risk 1: False assurance on derived and multi-hop claims

**Already named in ARCHITECTURE.md §7 as "the single strongest residual risk."** If a subtly-wrong synthesized claim is marked `SUPPORTED` because a shallow span looks similar under NLI, ControlPlane delivers false assurance — strictly worse than no control plane, because humans stop checking.

**Frozen mitigation (unchanged):**
- Derived claims route away from NLI entirely. Arithmetic/aggregative → recomputed from spans. Neither recomputable nor directly entailed → `UNKNOWN`.
- `UNKNOWN` never collapses into `SUPPORTED`.
- Verifiers from a different model family than the generator.

**Expanded mitigation for multi-route deployment:**
- The policy layer allows per-route declaration of claim patterns as `"derived"` — a configuration escape hatch that forces specific claim types into the recompute-or-`UNKNOWN` path even if the claim extractor doesn't tag them as such. This is a configuration overlay, not a new mechanism. The underlying rule (no NLI on derived claims) is unchanged.
- The per-route FNR measurement stratifies by claim type. If the "derived" stratum shows unexpected `SUPPORTED` rates, it signals either a misclassification (claims tagged as non-derived that should be derived) or a recompute-path failure — both trigger a review.

### Risk 2: Enforcing wrong ACLs from over-permissioned source systems

**Already addressed in QA.md B4.** The plane enforces what the source system declares; it doesn't fix IAM. If the index is over-permissioned, the plane faithfully enforces a wrong policy — but makes it visible.

**Expanded mitigation:**
- The per-source-system entitlement-violation rate (§5) is the **operational detector** for over-permissioned indexes. If source X produces entitlement violations across multiple principals at a rate significantly above the route median, the system flags source X as a likely over-permissioned index.
- This flag is a **reporting signal**, not a remediation. The remediation is fixing the source system's ACLs — which is outside ControlPlane's scope. The value is making the problem **visible and measurable**, which it was not before.
- The flag includes: source ID, violation count, affected principals, sample violations with full Evidence Ledger entries. A stakeholder can take this to the source-system owner and say: "your index is leaking to these people — here is the evidence."

### Risk 3: Policy configuration misconfiguration — the matrix stays pure but the route configuration surface becomes a new attack surface

If a route operator maps a payment action to R1 instead of R3, the matrix would correctly apply R1 semantics to an R3 action — the matrix didn't fail, but the input was wrong.

**Mitigation:**
- **Global invariants are structurally enforced at parse time.** The locked action classes (`payment`, `deletion`, `publication`, `regulated_advice`) are forced to R3. A route configuration that maps payment to R1 fails validation and cannot be activated. This is not a policy recommendation — it is a parse-time rejection.
- **Route configuration can only add R-tier assignments for route-specific actions** that are not in the locked set. A route-specific action like "update_internal_ticket" can be mapped by the route operator; "issue_refund" cannot.
- **Policy validation pipeline (§3)** catches downstream misconfiguration: shadow replay compares the actuator distribution under the new policy against the old. If Block/Escalate rates drop sharply on an R3-heavy route without a corresponding change in claim quality, the validation flags it for human review before canary deployment.
- **Audit trail**: every blast-radius mapping change is recorded in the policy ledger with the authorizing principal and the diff. If a misconfiguration does reach production, it is forensically traceable to a specific change by a specific person at a specific time.

---

## 8. Fidelity Self-Check

| Frozen invariant | Status in this document | Evidence |
|---|---|---|
| **Default = UNSUPPORTED** | Untouched. Global invariant in §3. Claims start `UNSUPPORTED` on every route. Policy cannot change the default. | §3: "default_verdict = UNSUPPORTED" listed under GLOBAL INVARIANTS, "not patchable, enforced at parse time" |
| **Entitlement / ACL check** | Untouched. Runs on Lane 1 for all routes. Cannot be disabled. Zero LLM. | §2: "The entitlement check" in shared components table. §3: "entitlement_check: always active, Lane 1, zero LLM" under GLOBAL INVARIANTS |
| **Exact R×S matrix** | Untouched. One object, identical across all routes. Never forked, never soft-configured. Routes provide R, evidence provides S, matrix emits actuator. | §2: "The matrix is a pure function: f(R, S) → actuator. It has no route parameter." Not redrawn anywhere in this document. |
| **Hard gate on actions, not tokens** | Untouched. Text streams with hold-back; actions gated at commit boundary. Global invariant. | §2: shared components table. §3: global invariant "R3 fail_stance = closed \| escalate" (action-level, not token-level) |
| **Published FNR as a format** | Untouched. Schema with null placeholders, population rules, measurement method. No fabricated numbers. | §5: full JSON schema with all values `null`, explicit population rules ("minimum_sample_for_measurement: 500", "maximum_ci_width_for_measurement: 0.05") |
| **Two-pending-actions resolution** | Untouched. Each pending action gets its own R-tier, its own worst-claim selection, its own matrix cell. | §2: "Each pending action on a route gets its own R-tier lookup, its own worst-claim selection (weighted by that claim's role in that action), and its own matrix cell." |
| **No LLM-as-judge on critical path** | Untouched. Policy engine is pure rule engine. NLI cross-encoder is a classifier producing a verdict, not a judge producing an opinion. | §3: "Zero LLM reasoning at decision time remains mandatory." §2: NLI listed under shared components as producing "SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN" — a verdict, not an opinion |
| **Bias is not a per-response verdict** | Untouched. Route-level, async, counterfactual flip rate with CI. Off critical path. | §6: "Async counterfactual bias measurement (route-level, decision flip rate with CI, off critical path)" listed under proposal-only. Not mentioned as a live mechanism anywhere. |
| **UNKNOWN never collapses into SUPPORTED** | Untouched. Global invariant. | §3: "UNKNOWN → SUPPORTED transition: FORBIDDEN" under GLOBAL INVARIANTS |
| **Surgical edit only** | Untouched. | §2: shared components table. |
| **Evidence-packet escalation** | Untouched. | §2: shared components table. |
| **No composite risk score** | Untouched. No 0–100 number appears in this document. | Actuator is determined by R × S, not by a scalar score. |

**Tension check:** The brief asks for "different AI use cases have different risk tolerance and latency budgets — a single, one-size-fits-all checking approach rarely works well everywhere." This document resolves the tension by making the *configuration* per-route (blast-radius mapping, lane budget, enforcement mode) while keeping the *mechanism* identical (one graph, one matrix, one set of actuators). The checking approach is one-size-fits-all; the inputs to that approach are route-specific. This is the CPU privilege-mode analogy from NARRATIVE.md — the x86 page-protection mechanism is identical across every process; what varies is the page table entries. No tension with the freeze.

**No competing mechanism enters this document.** No LLM-as-judge, no confidence thresholding, no composite risk score, no open-web truth layer, no per-response bias classifier, no redrawn matrix, no model-emitted citations, no speculative release with post-hoc recall.

---

*End of Round 2 Stage 2 document. Stage 1 freeze is fully preserved. No architectural change is introduced; only configuration surfaces, validation pipelines, and measurement methods are added around the frozen primitive.*