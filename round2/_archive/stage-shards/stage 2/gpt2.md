## 1. Expanded Core Thesis

ControlPlane.ai becomes an enterprise admission-control plane by instantiating the same `STEP → SPAN → CLAIM → ACTION` graph for every AI route, while changing only route configuration, verification depth, latency budget, action grammar, and governance policy. The structural invariant does not change: provenance is captured outside the model, every claim begins **UNSUPPORTED**, entitlement is checked against caller and source ACL, and the frozen R×S matrix determines the actuator from consequence and evidence. This makes heterogeneous routes different configurations of one control plane rather than different safety products.  

---

## 2. Multi-Route Architecture

### 2.1 Enterprise topology

The enterprise deployment has one logical ControlPlane with three surfaces:

```text
AI Application / Agent Route
        │
        ├── Context-Assembly SDK Hook
        │        └── Provenance Recorder
        │
        └── OpenAI-Compatible Reverse Proxy
                 │
                 ▼
        ┌──────────────────────┐
        │   Evidence Ledger    │
        │ STEP → SPAN → CLAIM   │
        │       → ACTION        │
        └──────────┬───────────┘
                   │
       ┌───────────┼────────────┐
       ▼           ▼            ▼
  Performance  Responsibility  Cost
       │           │            │
 Claim/Binding   ACL/Interlock  Yield/Rework
       └───────────┼────────────┘
                   ▼
             Action Interlock
                   │
             Exact R × S Matrix
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      Pass       Edit    Escalate/Block
```

The core implementation remains the frozen typed pipeline over one Evidence Ledger; workers do not exchange free-form messages, and only the Action Interlock makes the final control decision. 

### 2.2 What is shared across every route

The following are **enterprise-wide invariants**:

| Shared mechanism        | Enterprise invariant                                                                                                          |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Provenance Recorder** | Captures `source_id · ACL · hash · offsets · principal` at context assembly, outside the model.                               |
| **Evidence Ledger**     | One append-only, hash-chained request artifact.                                                                               |
| **Claim extraction**    | Produces typed, check-worthy claims and assertion strength.                                                                   |
| **Proof path**          | Numeric/structural → deterministic recomputation; factual/textual → provenance binding; derived → recomputation or `UNKNOWN`. |
| **Entitlement**         | Caller identity compared directly against source ACL.                                                                         |
| **Action grammar**      | Typed `tool × argument schema × irreversibility` validation.                                                                  |
| **R calculation**       | `irreversibility × audience × data class × autonomy level`.                                                                   |
| **R×S matrix**          | Exactly one enterprise decision table.                                                                                        |
| **Actuators**           | `Block · Edit · Escalate · Pass`; autonomy downgrade and circuit breaker remain route controls, not replacement actuators.    |
| **Fail stance**         | Tier-based, not globally configured.                                                                                          |
| **Audit**               | Every decision records evidence, policy version, verifier versions and latency.                                               |
| **FNR reporting**       | Same per-route reporting contract everywhere.                                                                                 |

These are the architectural control plane. They are not cloned per application.  

### 2.3 What is configured per route

A route is a **policy profile over the shared graph**, not a new product.

Each route declares at minimum:

```text
route_id
tenant
use_case
principal_source
data_classes
geography / regulatory_profile
latency_budget
allowed_claim_types
verification_policy
action_grammar
blast_radius_mapping
fail_stance
shadow / enforcement_state
threshold_version
```

Critically, these fields select or parameterize existing mechanisms rather than introducing new ones.

#### Customer support refund route

```text
latency        → low
dominant R     → R1 + R3
action grammar → refund / customer-send
verification   → deterministic + binding where required
fail stance    → R3 closed/escalate
```

#### Internal knowledge route

```text
latency        → low
dominant R     → R0 + R1
action grammar → read-only
verification   → mostly Lane 1 + binding when needed
fail stance    → R0/R1 open with annotation
```

#### Enterprise decision-support route

This exists in the complete architecture but remains outside the Stage 1 live prototype.

```text
latency        → higher tolerance
dominant R     → R0/R1 or R3 depending on downstream use
verification   → claim proof + derived-value recomputation
bias           → Lane 3 route-level measurement
action grammar → propose / regulated decision path
```

The official brief explicitly establishes that these routes have different risk signatures and latency budgets; therefore the architecture varies **configuration**, not control semantics. 

### 2.4 How the matrix remains one product

The matrix is evaluated **per pending action**, not once per response.

That distinction is what allows the same response to contain:

```text
CLAIM A ──► ACTION: customer-visible text ──► R1
CLAIM B ──► ACTION: refund                ──► R3
```

and resolve them independently:

```text
R1 × entitlement violation     → Edit
R3 × unsupported categorical   → Escalate
```

The route can change which actions exist and how the action maps to R, but it cannot change the matrix semantics. The Stage 1 freeze explicitly makes this per-pending-action behavior non-negotiable. 

### 2.5 Multi-turn and agentic routes

Multi-turn execution is represented as **more STEPs in the same graph**, not as a separate architecture.

```text
STEP 1: retrieve account
    ↓
SPAN
    ↓
CLAIM
    ↓
ACTION: query vendor record
    ↓
STEP 2
    ↓
SPAN
    ↓
CLAIM
    ↓
ACTION: prepare refund
```

This matters because compounding risk comes from downstream actions being based on earlier claims. The graph therefore preserves the lineage from the final action backward through all intermediate evidence-producing steps.

The cost and performance reads remain graph traversal operations, while the final Action Interlock evaluates the current ledger state. The architecture explicitly requires deadline-driven coordination and says a late verification returns `UNKNOWN` rather than silently becoming support. 

---

## 3. Governance & Policy Layer

### 3.1 Policy is configuration, not model reasoning

The governance layer is a **versioned rule registry** feeding the frozen rule engine.

Each rule retains the existing primitive:

```text
(signal, threshold, action, latency_budget)
```

and is stored in a versioned DAG. Decision-time execution remains deterministic with **zero LLM reasoning**. 

The governance hierarchy is:

```text
Enterprise baseline
      ↓
Geography / regulatory profile
      ↓
Tenant
      ↓
Route
      ↓
Action class / blast radius
```

The hierarchy only narrows or selects existing controls. It cannot redefine the R×S matrix.

### 3.2 Configuration dimensions

#### Use case / route

Controls:

* allowed action types;
* expected latency;
* claim categories emphasized;
* verification lane budget;
* shadow/enforcement state.

#### Risk appetite

Not a scalar "risk score."

Risk appetite is expressed structurally through:

* which actions may reach R2/R3;
* whether a route may autonomously act or only propose;
* route error budget;
* route-specific thresholds;
* fail stance within the already frozen R tier model.

#### Geography / regulatory posture

A regulation profile selects:

* data classes;
* retention period;
* audit fields;
* allowed destinations;
* action restrictions;
* escalation requirements.

The underlying graph and matrix remain unchanged.

#### Blast radius

Blast radius is calculated from the action's consequence:

`R = irreversibility × audience × data class × autonomy level`

The policy layer therefore controls **what action is possible**, while the matrix decides **what happens when proof is insufficient**. 

### 3.3 Policy-change lifecycle

No policy change goes directly to production.

```text
Draft policy
   ↓
Static validation
   ↓
Replay last N traces
   ↓
Compare FP / FN / override deltas
   ↓
Canary one route / tenant
   ↓
Observe override + gate-fail behavior
   ↓
Promote or rollback
```

This is already supported by the frozen architecture: threshold changes require shadow replay, are canaried by route, and can auto-roll back when human-override behavior exceeds the defined baseline multiplier. Decisions are written to the append-only ledger with the evidence fragment that caused them. 

### 3.4 Day-one deployment

Every route begins in **shadow mode**.

The plane computes:

> "Would have held N, of which M were true positives."

Only after route-level evidence exists does enforcement become appropriate. This directly addresses the official brief's over-flagging/under-flagging tradeoff without weakening the control plane. 

---

## 4. Feedback & Learning Loops

The control plane learns **operational parameters and evidence quality**, not a new "safety model."

### 4.1 What is learned

#### A. Threshold calibration

Per-route calibration can change:

* check-worthiness thresholds;
* verification depth;
* route-specific thresholds already supported by the architecture;
* shadow/enforcement readiness.

The change is derived from replayed evidence, then promoted through the policy lifecycle.

#### B. Human overrides

A human override becomes an **adjudication observation**:

```text
original verdict
original matrix action
human disposition
reason code
route
policy version
evidence packet
```

This is used to measure:

* false positives;
* override rate;
* route calibration;
* whether enforcement should be retained or downgraded.

It does **not** directly rewrite the matrix or mutate a verdict rule in real time.

#### C. Escalations

Escalated cases become high-value audit samples because the packet already contains:

`claim + candidate spans + verdict + diff`

Those cases are fed into the adjudication process and later replay.

#### D. Shadow outcomes

Shadow mode supplies the counterfactual population needed to decide whether a route is ready for enforcement.

### 4.2 What remains rule-based

These never become learned model behavior:

* provenance capture;
* source/hash/ACL recording;
* entitlement comparison;
* numeric recomputation;
* derived-claim recomputation;
* action-schema validation;
* R calculation;
* exact R×S matrix;
* fail stance;
* hard action gate;
* Evidence Ledger integrity;
* evidence-packet construction.

This separation is essential: the thing that decides authorization must remain inspectable and deterministic. 

### 4.3 What is never learned from feedback

Do **not** learn these from user overrides or traffic behavior:

* "users usually accept this hallucination";
* "humans often approve refunds, so allow them";
* ACL membership;
* source truth;
* matrix semantics;
* action safety from aggregate acceptance;
* a global confidence threshold;
* a composite risk score.

A human override is evidence for **evaluation and calibration**, not permission to rewrite the security boundary.

### 4.4 Bias

Bias remains exactly where the freeze places it:

```text
decision route
      ↓
async shadow replay
      ↓
protected-attribute perturbation
      ↓
decision flip rate
      ↓
confidence interval
      ↓
route-level measurement
```

It is never turned into:

```text
claim → bias verdict → matrix cell
```

because that would violate the architecture's statement that bias is distributional rather than a per-response property. 

---

## 5. Metrics, Monitoring & Trustworthiness Reporting

The control plane publishes **misses, not just catches**.

### 5.1 Per-route false-negative rate

The enterprise report uses a typed schema:

```text
route_id
evaluation_window
sample_definition
stratification
ground_truth_source
false_negative_count
ground_truth_positive_count
FNR
confidence_interval
policy_version
verifier_versions
measurement_status
```

Conceptually:

`FNR = missed ground-truth violations / all ground-truth violations`

The critical qualifier is **ground-truth population**. Where trustworthy ground truth does not exist, the field remains `null` or explicitly "unavailable." Stage 1 already freezes this reporting behavior.  

No enterprise number is invented here.

### 5.2 False positives and override rate

For each route:

```text
FP / adjudicated cases
human overrides / enforced decisions
override reason distribution
gate-fail rate
edit rate
escalation rate
```

The important metric is not merely "how many things were flagged." It is whether operators are being repeatedly forced to undo the plane's decisions.

Override behavior therefore feeds the policy rollback mechanism already frozen in architecture. 

### 5.3 Dead compute

Dead compute is exact:

```text
STEP → SPAN → CLAIM
```

Walk backward from **accepted supported claims**.

Any step that produced spans grounding zero accepted claims is dead compute.

This works without ground truth, without a trained model, and without estimating what "should" have been useful. 

Enterprise reporting:

```text
route
model / tool
steps executed
steps yielding accepted claims
dead steps
dead tokens / spend where available
```

The metric belongs to the same graph that verifies the response; it is therefore not a separate observability subsystem.

### 5.4 Latency by lane

Report:

```text
Lane 1:
  span membership
  ACL
  arithmetic
  typed interlock

Lane 2:
  binding / NLI

Lane 3:
  semantic-entropy
  calibration
  shadow adjudication
```

And separately:

* p50;
* p95;
* timeout rate;
* cache-hit rate;
* verification depth;
* action-gate latency.

The frozen targets remain:

* **≤40 ms p50**
* **≤200 ms p95**

for R0/R1 added text latency. The architecture deliberately does not claim zero latency. 

### 5.5 Entitlement violations

Report per route and source:

```text
principal
source_id
ACL version
claim
action
entitlement outcome
matrix cell
actuator
```

This creates a measurable distinction between:

1. **unsupported claim**, and
2. **supported but unauthorized claim**.

That distinction is one of the reasons output-only checking cannot reproduce the ControlPlane mechanism. 

### 5.6 Trust report

A skeptical buyer should be able to query one route and obtain:

```text
Route
 ├─ traffic
 ├─ R-tier distribution
 ├─ latency by lane
 ├─ entitlement violations
 ├─ dead compute
 ├─ edits / escalations / blocks
 ├─ human overrides
 ├─ shadow counterfactuals
 └─ FNR
```

And every aggregate row must drill into ledger traces.

The architecture therefore provides evidence for the claim **"the plane measures its own misses"** rather than asking the buyer to trust a dashboard percentage. 

---

## 6. Complete Enterprise Solution vs Prototype

### Full enterprise solution

The complete platform contains:

**Core admission plane**

* context-assembly SDK;
* OpenAI-compatible reverse proxy;
* Provenance Recorder;
* Evidence Ledger;
* claim extraction;
* proof/binding;
* deterministic recomputation;
* entitlement auditor;
* Action Interlock;
* exact R×S matrix;
* surgical edit;
* evidence-packet escalation.

**Route governance**

* route profiles;
* tenant configuration;
* geography/regulatory profiles;
* versioned policy DAG;
* shadow replay;
* canary and rollback;
* route-specific fail stance;
* autonomy downgrade;
* circuit breaker.

**Operational control**

* latency by lane;
* proof cache;
* dead compute;
* rework;
* non-convergence breaker;
* route cost baselines.

**Trust and evaluation**

* adjudication;
* per-route FNR;
* FP/override reporting;
* stratified shadow audit;
* red-team validation.

**Advanced route capability**

* agentic multi-step traces;
* decision-support routes;
* asynchronous semantic-entropy analysis;
* route-level counterfactual bias measurement.

These components are extensions and operationalizations of the existing architecture rather than replacement mechanisms. 

### What Stage 1 deliberately shows

Stage 1 shows only the two frozen live routes:

1. Customer Support Refund Agent
2. Internal Knowledge Assistant

with the central proof:

* provenance outside model;
* one Evidence Ledger;
* UNSUPPORTED default;
* entitlement;
* exact matrix;
* dual pending actions;
* action gate;
* surgical edit;
* evidence packet;
* principal-flip replay;
* FNR schema.



### Proposal-only

The following remain proposal architecture rather than live prototype scope:

* live decision-support route;
* counterfactual bias measurement;
* production-scale traffic;
* full geography/industry policy packs;
* real enterprise IAM remediation;
* real payments;
* human triage queue;
* full multi-agent autonomy;
* Lane-3 statistical workloads as a live critical path.

Stage 1 explicitly freezes these exclusions to protect the graph/matrix proof. 

The important distinction is:

**prototype = proof that the control plane works**

**enterprise proposal = proof that the control plane can be operated across an enterprise**

---

## 7. Residual Risks & Explicit Mitigations

### Risk 1 — False assurance on derived / multi-hop claims

This remains the most serious technical risk.

A shallow entailment match can falsely mark a synthesized claim as supported.

**Mitigation**

* derived/aggregative claims bypass ordinary NLI;
* recompute arithmetic from spans;
* otherwise return `UNKNOWN`;
* `UNKNOWN` never becomes `SUPPORTED`;
* use verifier/model-family decorrelation;
* stratified shadow adjudication measures the residual miss rate.

This is explicitly identified as the architecture's strongest residual risk. 

---

### Risk 2 — The source itself is wrong or poisoned

ControlPlane proves the relationship:

```text
claim ↔ captured evidence
```

It does **not** prove that the underlying evidence is true.

A poisoned document can therefore produce a genuine binding for a false claim.

**Mitigation**

* source identity and content hash are captured outside the model;
* every entitlement decision names principal and source;
* corpus provenance remains auditable;
* source-level remediation stays with the enterprise source system rather than pretending ControlPlane repairs IAM or source truth.

This is the correct security boundary: protect the claim-to-evidence link, not the truth of the evidence itself. 

---

### Risk 3 — Operational tuning creates either alert fatigue or liability

A control plane that over-intervenes will be bypassed; one that under-intervenes creates liability. The official brief explicitly requires this tradeoff to be addressed. 

**Mitigation**

* shadow mode before enforcement;
* route-specific calibration;
* blast-radius-dependent verification depth;
* R0/R1 fail-open with annotation;
* R2/R3 fail-closed or escalate;
* route-level error budgets;
* human overrides become adjudication evidence;
* policy changes require replay + canary;
* automatic rollback when override behavior exceeds the defined baseline.

This is not solved with a global threshold. The architecture explicitly rejects that approach. 

---

## 8. Fidelity Self-Check

| Frozen condition                       | Expansion status                                                                                                                      |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Default = UNSUPPORTED**              | **Untouched.** Multi-route deployment never changes the starting verdict. Every route inherits the burden-of-proof rule.              |
| **Entitlement / ACL check**            | **Untouched.** Route configuration selects data/action context; it never removes caller-vs-source ACL verification.                   |
| **Exact R×S matrix**                   | **Untouched.** Routes map their actions into R tiers; no route gets a different matrix. The matrix remains one enterprise primitive.  |
| **Hard gate on actions, not tokens**   | **Untouched.** Latency optimization changes verification placement, not the commit boundary.                                          |
| **No LLM-as-judge on critical path**   | **Untouched.** LLMs may assist extraction/binding where already specified, but the decision policy remains a pure rule engine.        |
| **Two-pending-actions resolution**     | **Untouched.** Multiple actions are evaluated independently on the same graph; the refund remains `R1 → Edit` and `R3 → Escalate`.    |
| **Bias is not a per-response verdict** | **Untouched.** Bias remains route-level asynchronous counterfactual measurement.                                                      |
| **No confidence/composite score**      | **Untouched.** Route policy selects deterministic thresholds and verification depth; no scalar score becomes the actuator driver.     |
| **API-only operation**                 | **Untouched.** Reverse proxy + context hook; no weights, logits or hidden-state dependency.                                           |
| **One graph, three reads**             | **Untouched.** Performance, cost and responsibility continue to read the same Evidence Ledger.                                        |

### Final architectural invariant

The expansion introduces **configuration, governance, deployment, measurement and operating loops** around the frozen mechanism.

It does **not** introduce a second mechanism for deciding whether an AI action should happen.

That boundary is the entire Stage 2 design:

```text
                 ENTERPRISE ROUTES
        ┌────────────┬────────────┐
        │            │            │
     Support      Knowledge    Decision
        │            │            │
        └────────────┴────────────┘
                     │
                     ▼
          SAME CONTROL PLANE
                     │
       STEP → SPAN → CLAIM → ACTION
                     │
          SAME PROOF / ACL / R×S
                     │
          SAME ACTION INTERLOCK
                     │
       PASS / EDIT / ESCALATE / BLOCK
```

The official brief asks for a complete enterprise solution capable of heterogeneous use cases, differing risk/latency budgets, feedback loops, governance and metrics; the frozen design supplies the underlying control primitive, and Stage 2 should add the operating envelope around it rather than weaken the primitive. 
