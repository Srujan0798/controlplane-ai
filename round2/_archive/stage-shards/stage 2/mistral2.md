---
### **1. Expanded Core Thesis**

ControlPlane.ai is an **admission-control layer** that treats every AI action across all enterprise routes as a set of claims requesting permission to act. It captures provenance *outside the model* at context assembly—`source_id · ACL · hash · offsets`—then binds each claim to that evidence with a default of **UNSUPPORTED**. The same **STEP → SPAN → CLAIM → ACTION** graph, the same entitlement checks, and the same frozen R×S matrix apply uniformly across all routes; only the mapping of actions to blast-radius tiers and per-route thresholds vary. This is **configuration over detection**—the control plane scales by evidence and consequence, not by inventing new mechanisms for each use case.

---

---
### **2. Multi-Route Architecture**

**What is shared (immutable across all routes):**
- **Graph structure**: STEP → SPAN → CLAIM → ACTION (one structure, three reads).
- **Evidence Ledger schema**: `principal, action_intent, R_tier, spans[], claims[], bindings[], step_yield[], verdicts[], policy_version, verifier_versions, latency_spent`.
- **Default verdict**: **UNSUPPORTED** (claims must earn SUPPORTED).
- **Entitlement mechanism**: Deterministic ACL set-membership (caller vs source ACL).
- **Decision matrix**: Exact R×S matrix (transcribed, never redrawn).
- **Actuators**: Block, Edit, Escalate, Pass (plus autonomy downgrade/circuit breaker as system-level).
- **Lane architecture**: Lane 1 (inline deterministic), Lane 2 (near-line NLI), Lane 3 (async).
- **Hard gate location**: On **actions**, not tokens (text streams with hold-back).
- **Published format**: Per-route FNR schema with empty placeholders.

**What is configured per route (not mechanism changes):**
- **Action → R-tier mapping**: Which actions belong to which blast-radius tier (e.g., `refund → R3`, `show_text → R1`).
- **Verdict severity thresholds**: What constitutes categorical vs hedged vs contradicted (e.g., `categorical: no_span AND confidence > 0.9`).
- **Lane budget allocation**: Verification budget per R-tier (e.g., `R0: lane1_only`, `R1: lane1 + lane2_for_flagged`).
- **Policy rules**: Which claim types trigger which checks (e.g., `numeric_claims → deterministic_recomputation`).
- **Fail stance per tier**: R0/R1 fail open with annotation; R2/R3 fail closed or escalate.
- **Shadow mode**: Sampling rate for dual-emit (default 5% of passes).

**How the matrix remains universal:**
The matrix is **route-agnostic**. Routes only determine **which actions map to which R-tiers**. The matrix itself—axis labels, column vocabulary, cell values—is **transcribed, never redrawn**. The same cell (e.g., **R3 × unsupported-categorical = Escalate**) produces the same actuator regardless of route.

| **Route** | **Action** | **R-tier** | **Verdict** | **Matrix Cell** | **Actuator** |
|-----------|------------|------------|-------------|-----------------|--------------|
| Customer Support | show_text | R1 | entitlement_violation | R1 × entitlement | **Edit** |
| Customer Support | issue_refund | R3 | unsupported_categorical | R3 × unsupported | **Escalate** |
| Internal Knowledge | share_doc | R2 | unsupported_hedged | R2 × unsupported | **Edit** |
| Decision Support | approve_contract | R3 | contradicted | R3 × contradicted | **Block** |

---
---
### **3. Governance & Policy Layer**

**Policy as code:**
- Policies are **versioned YAML/JSON** artifacts (immutable, append-only).
- Changes follow **pull-request style** workflow: draft → shadow replay → canary → promote → audit.

**Policy structure:**
```yaml
route: "customer-support/refund"
inherits: ["global_base", "finance_common"]

blast_radius:
  show_text: R1
  issue_refund: R3
  internal_note: R0

verdict_thresholds:
  categorical: { no_span: true, confidence: ">0.9" }
  hedged: { partial_span: true, OR: "confidence < 0.9" }
  contradicted: { span_explicitly_denies: true }

entitlement:
  enforce: true
  acl_source: "document_metadata"
  default_deny: true

lane_budget:
  R0: [lane1]
  R1: [lane1, lane2_flagged]
  R2: [lane1, lane2]
  R3: [lane1, lane2, lane3_calibration]

fail_stance:
  R0: pass + annotate
  R1: pass + annotate
  R2: escalate
  R3: escalate

shadow:
  enabled: true
  sample_rate: 0.05
```

**Policy hierarchy:**
```
Global Default → Geography Pack → Industry Pack → Route-Specific
```
**Override order**: Route > Industry > Geography > Global. Routes can **pin** to specific policy versions.

**Policy change workflow (zero LLM reasoning):**
1. **Draft** new version from current.
2. **Shadow Replay** against last N traces (default 1000):
   - Generate FP/FN delta vs current version.
   - Measure latency impact.
3. **Canary** deploy to 5% of route traffic:
   - Monitor human override rate, error rates.
   - **Auto-rollback**: If override rate > 3× baseline, revert within 5 minutes.
4. **Promote** to full traffic after canary period (default 24h).
5. **Audit** every change: version diff, shadow replay results, canary metrics.

**Audit trail:**
- Every policy decision written to **hash-chained ledger** (WORM storage).
- Every change includes: version diff, shadow replay results, canary metrics.
- **Immutable**: Cannot be altered or deleted.

**Regulatory configuration:**
- **Policy packs** are separate, versioned artifacts.
- **Change tracking**: All regulatory changes audited separately from route changes.

**Key principle**: Policies **configure behavior**, they don’t **replace mechanisms**. The core graph, matrix, and entitlement checks are **invariant**.

---
---
### **4. Feedback & Learning Loops**

**What is learned (async, Lane 3 only):**

| **Signal Source** | **What’s Learned** | **Mechanism** | **Output** |
|-------------------|-------------------|---------------|------------|
| Human overrides | FP/FN patterns | Rule-based threshold tuning | Per-route verdict thresholds |
| Shadow replay | Counterfactual outcomes | Statistical aggregation | “Would have held N, M true positives” |
| Entitlement violations | Over-permissioned sources | Pattern detection | ACL violation reports |
| Dead compute | Waste patterns | Graph backward walk | Route-specific dead compute % |
| Binding failures | Claim-type difficulty | Error analysis | Claim-type routing improvements |

**What remains rule-based (never learned):**
- **Core binding**: Claim → span matching is **deterministic lookup**.
- **Entitlement checks**: ACL comparisons are **set-membership tests**.
- **Matrix application**: R×S → actuator is **static mapping**.
- **Numeric recomputation**: Arithmetic verification is **deterministic**.
- **Typed interlocks**: Action grammar validation is **declarative**.

**What is never learned from:**
- ❌ Model outputs (generator’s claims)
- ❌ User feedback on “correctness” (subjective)
- ❌ Confidence scores (broken instrument)
- ❌ Composite scores (unactionable)
- ❌ Open-web “truth” (out of scope)

**Learning architecture principles:**
1. **Offline only**: All learning happens in **Lane 3 (async)**.
2. **No critical-path feedback**: Learning **never** affects real-time decisions.
3. **Human-in-the-loop**: All threshold changes require **review before promotion**.
4. **Explainable**: Every learned pattern is **traceable to source decisions**.
5. **Reversible**: All changes can be **rolled back** automatically.

**Example: Threshold calibration**
- **Signal**: High override rate on “hedged” claims in Route X.
- **Investigation**: Shadow replay shows 80% of hedged claims were correct.
- **Action**: Raise hedged threshold for Route X (e.g., require `partial_span + confidence < 0.7`).
- **Validation**: Canary deployment, monitor override rate.
- **Rollback**: If override rate spikes, auto-revert.

**Boundary**: We **learn thresholds**, not **mechanisms**. The core graph and matrix remain unchanged.

---
---
### **5. Metrics, Monitoring & Trustworthiness Reporting**

**Per-route metrics (published in gate report):**

| **Metric** | **Definition** | **Measurement Method** | **Status** |
|------------|---------------|------------------------|------------|
| **FNR** | % of harmful actions that passed | Stratified shadow audit: 100% of blocks/escalations + random slice of passes | Format (empty in prototype) |
| **FPR** | % of safe actions that were blocked/held | Human override rate on Escalate/Block | Measured |
| **Override Rate** | % of gated actions overridden | Manual override count / total gated | Measured |
| **Dead Compute %** | % of spend that grounded nothing | Graph backward walk: steps with zero accepted claims | Measured |
| **Latency p50/p95** | Added latency | Measured at gate entry/exit | Measured |
| **Entitlement Violations** | ACL-denied span references | Deterministic ACL check failures | Measured |
| **Binding Coverage** | % of claims with span bindings | SUPPORTED claims / check-worthy claims | Measured |
| **UNKNOWN Rate** | % of claims returning UNKNOWN | UNKNOWN verdicts / total claims | Measured |

**Gate Report Schema (published format):**
```json
{
  "route": "customer-support/refund",
  "policy_version": "v1.2.3",
  "reporting_period": "2026-08-16T00:00:00Z/2026-08-23T00:00:00Z",
  "corpus": "prototype_corpus",
  "metrics": {
    "fnr": { "value": null, "status": "prototype_corpus", "sample_size": 100 },
    "fpr": { "value": 0.02, "status": "measured", "sample_size": 100 },
    "override_rate": { "value": 0.05, "status": "measured", "sample_size": 50 },
    "dead_compute_pct": { "value": 0.25, "status": "measured", "sample_size": 100 },
    "latency_p50_ms": { "value": 35, "status": "measured" },
    "latency_p95_ms": { "value": 180, "status": "measured" },
    "entitlement_violations": { "value": 3, "status": "measured" },
    "binding_coverage": { "value": 0.85, "status": "measured" },
    "unknown_rate": { "value": 0.05, "status": "measured" }
  }
}
```

**Trustworthiness principles:**
1. **Honesty over perfection**: FNR is published as **format with status** (`prototype_corpus`, `measured`, etc.).
2. **Traceability**: Every metric ties to **Evidence Ledger** entries.
3. **Granularity**: Per-route reporting shows **where it works and where it doesn’t**.
4. **No fabricated numbers**: Prototype shows **null/placeholder** or **labelled corpus values**.
5. **Sceptical stakeholder test**: A judge can **verify every metric’s definition and measurement method**.

---
---
### **6. Complete Enterprise Solution vs Prototype**

**Full Enterprise Solution Contains:**
✅ **Core Control Plane**: STEP→SPAN→CLAIM→ACTION graph, R×S matrix, entitlement checks.
✅ **Multi-Route Deployment**: Per-route action→R-tier mapping, policy packs.
✅ **Governance Layer**: Versioned policies, audit trails, change workflows, auto-rollback.
✅ **Feedback Loops**: Shadow replay, human override analysis, threshold calibration.
✅ **Metrics & Reporting**: Per-route FNR/FPR, dead compute, latency, entitlement violations.
✅ **Bias Measurement**: Async counterfactual flip-rate with CI, route-level.
✅ **Circuit Breaker**: Per-route error budget with autonomy downgrade.
✅ **Dead Compute Optimization**: Out-of-band stop-sequence injection.
✅ **Regulatory Compliance**: Geography/industry policy packs, retention policies.
✅ **Integration**: OpenAI-compatible proxy, context-assembly SDK, action adapters.

**Stage 1 Prototype Shows:**
✅ **Core graph mechanism**: Live STEP→SPAN→CLAIM→ACTION construction.
✅ **Provenance capture**: Spans with `source · ACL · hash` captured at context assembly.
✅ **Default UNSUPPORTED**: Claims start red, must earn green.
✅ **Three-axis reads**: Performance, Cost, Responsibility on same graph.
✅ **Matrix application**: Exact R×S matrix with correct cell values.
✅ **Two-pending-actions**: R1=Edit (text), R3=Escalate (payment) for same claim.
✅ **Surgical edit**: Unproven claim stripped, not rewritten.
✅ **Evidence packet**: Structured `claim + spans + verdict + diff`.
✅ **Hard action gate**: Payment held while text streams.
✅ **FNR format**: Empty schema with typed placeholders.

**Proposal-Only (Explicitly NOT in Prototype):**
❌ **Bias measurement**: Async counterfactual replay with CI (requires historical data; not core mechanism).
❌ **Circuit breaker**: Per-route error budget (system-level SRE; not architectural proof).
❌ **Dead compute optimization**: Stop-sequence injection (requires provider API integration).
❌ **Production-scale load**: Tens of thousands of interactions/week (prototype is single-node).
❌ **Real payment execution**: Use **mock tool** with real gate semantics.
❌ **Regulatory certification**: Geography/industry compliance packs (business proposal scope).
❌ **Full autonomous multi-agent**: Not needed to prove core mechanism.
❌ **Human triage queue**: Evidence packet is deliverable; triage UI is operational detail.
❌ **Per-response bias verdicts**: Explicitly contrary to frozen architecture.
❌ **Confidence-driven disposition**: The named failure is *confidently* wrong.

---
---
### **7. Residual Risks & Explicit Mitigations**

| **Risk** | **Impact** | **Mitigation** | **Residual** |
|----------|------------|---------------|--------------|
| **False Assurance on Derived Claims** | **High** — subtle wrong synthesized claims marked SUPPORTED. | Route derived claims to **deterministic recomputation**; **UNKNOWN never collapses to SUPPORTED**; decorrelate verifier model family; publish error bars via **stratified shadow audit**. | **Low** — UNKNOWN boundary is absolute. |
| **Over-Permissioned Source Indexes** | **Medium** — faithfully enforces wrong ACLs. | Make violations **visible in ledger**; query-time ACL check **detects over-permissioning**; per-route entitlement violation reports; explicitly state: *we enforce existing ACLs, don’t fix IAM*. | **Low** — detection is deterministic. |
| **Cold-Start Performance** | **Medium** — new routes lack baselines. | Exclude cold-start from cost baselines; **default to pass with annotation** for R0/R1; **shadow mode** default; rapid calibration via canary. | **Low** — conservative defaults. |

**Mitigation architecture:**
- **False Assurance**: The **UNKNOWN never collapses** rule is the **hard boundary**. Derived claims either recompute or return UNKNOWN.
- **Over-Permissioning**: ACL checks are **deterministic set-membership**—over-permissioning is **visible by construction**.
- **Cold Start**: **Shadow mode** ensures no route enforces without earning its counterfactual.

---
---
### **8. Fidelity Self-Check**

**Explicit confirmation of frozen invariants:**

| **Frozen Invariant** | **Status** | **Protection Mechanism** |
|---------------------|------------|--------------------------|
| **Default = UNSUPPORTED** | ✅ **Untouched** | All claims start as UNSUPPORTED; must earn SUPPORTED via binding. |
| **Entitlement / ACL check** | ✅ **Untouched** | Deterministic set-membership: caller principal vs source ACL. |
| **Exact R×S matrix** | ✅ **Untouched** | Transcribed exactly from ARCHITECTURE.md §4; **never redrawn**. |
| **Hard gate on actions, not tokens** | ✅ **Untouched** | Text streams with hold-back; actions gated at **commit boundary**. |
| **Published FNR as format** | ✅ **Untouched** | Empty schema with typed placeholders; **emptiness is the credibility play**. |
| **Two-pending-actions resolution** | ✅ **Untouched** | R1=Edit (text) + R3=Escalate (payment) for **same unproven claim**. |
| **No LLM-as-judge on critical path** | ✅ **Untouched** | Pure rule engine; NLI only in Lane 2 for entailment, **never for decision**. |
| **Bias as distributional/async** | ✅ **Untouched** | Counterfactual flip-rate with CI, **route-level, async only**. |
| **Provenance outside model** | ✅ **Untouched** | Captured at context assembly with `source · ACL · hash · offsets`. |

**Additional protections:**
- ❌ No composite risk scores.
- ❌ No confidence-driven disposition.
- ❌ No response-level bias verdicts.
- ❌ No redrawn matrix or invented actuators.
- ❌ No model-emitted citations.
- ✅ Vocabulary discipline: **authorise · admit · prove · bind · refuse · hold · escalate · gate** only.

**Final verification**: Every element in this expansion **preserves or extends** the frozen architecture. Nothing **softens, weakens, or replaces** the core differentiation.