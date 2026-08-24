## 1. Expanded Core Thesis

ControlPlane expands from a single-path gate to a multi-route admission-control plane by treating **route** as a policy envelope around the unchanged graph. The shared engine still captures provenance outside the model, holds every claim `UNSUPPORTED` until proven against that provenance, applies deterministic entitlement and the frozen R×S matrix, and prices verification by blast radius. What differs per route is evidence scope, action-to-R mapping, proof budget, fail stance, enforcement lifecycle and reporting calibration — all versioned configuration, not new detectors. The sharpest differentiator remains identical: an unproven or unauthorized claim cannot cross into an action, and the plane publishes per-route what it missed.

## 2. Multi-Route Architecture

### Shared across every route

- **Provenance Recorder** — captures every span at context assembly with `source_id · ACL · hash · offsets`.
- **Graph builder** — constructs the same `STEP → SPAN → CLAIM → ACTION` ledger per request/session.
- **Verifier pool** — deterministic recomputation, span-membership, ACL/entitlement, typed action interlocks, NLI binder.
- **Action Interlock** — the only component that emits an actuator.
- **Pure rule engine** — evaluates typed policy DAGs; zero LLM at decision time.
- **Append-only ledger** — hash-chained, one record per decision with evidence fragment.
- **Measurement/reporting schema** — same fields and statistical machinery for every route.

### Configured per route

A route is declared as a `RoutePolicy`, not as a new engine:

```text
RoutePolicy {
  route_id
  principal_source
  provenance_scope          # allowed source classes, required span metadata
  action_tool_schema        # tools/actions permitted on this route
  action_to_R_mapping       # which action intents are R0/R1/R2/R3
  verification_profile      # lane assignment, proof depth, timeout, lane budgets
  fail_stance_by_R          # must respect tier floors
  enforcement_mode          # shadow | canary | enforce
  error_budget              # circuit breaker sensitivity
  escalation_target         # evidence-packet destination
  sampling_policy           # FNR/FP sampling strata and rates
}
```

Example route differentiation:

| Route | R profile | Lanes | Enforcement posture |
|---|---|---|---|
| Customer refund | R1 text + R3 refund action | Lane 1 for text; Lane 1+2+interlock for R3 | R3 action gate enforce; R1 text canary |
| Internal knowledge | R0/R1 read-only | Lane 1 only; ACL always inline | Enforce after shadow evidence earned |
| Decision-support | R0/R1 memo + R2 workflow submission | Lane 1 for text; Lane 2 for derived claims; Lane 3 async bias replay | R2 submission gate enforce; bias measurement shadow |

### Matrix application without becoming different products

The R×S matrix is a single immutable lookup inside the interlock. A route cannot:

- add or remove columns, rows, or actuators;
- change a matrix cell;
- convert an R-tier into a soft label;
- replace severity with a route-specific “risk score.”

A route can only change what enters the matrix:

- which pending action is R1, R2, or R3;
- which claims receive which verdict via the shared verifiers;
- whether the route is in shadow, canary, or enforce.

If an engineer opens the interlock source, there is exactly one matrix. If they open route config, they see inputs, not cells.

### Multi-turn and agent compounding

For agentic routes, the graph persists as a **session ledger**. Every turn appends new steps, spans, claims and pending actions to the same session graph. A claim accepted in turn 1 and reused by an action in turn 4 remains bound to its original span. If source hash or ACL changes before the action, re-verification returns `UNKNOWN` or entitlement violation, and the matrix routes the action accordingly. No turn is re-authorized from memory alone.

## 3. Governance & Policy Layer

### Policy surface

Governance is a layered, versioned DAG, not nested conditionals:

```text
PolicyVersion {
  version_id
  parent_version
  route_selector
  layers: [
    route_policy,
    risk_appetite,
    jurisdiction_overlay
  ]
  rule_dag
  fail_stance_by_R
  validation_report_ref
  approved_by
  effective_time
  rollback_pointer
}
```

The layers behave as follows:

| Layer | Controls |
|---|---|
| **Base/frozen** | Graph semantics, default `UNSUPPORTED`, entitlement logic, exact R×S matrix, action gate on actions. Not editable by route policy. |
| **Route policy** | Provenance scope, action-to-R mapping, verification profile, lane budgets, fail stance, enforcement mode. |
| **Risk appetite** | Error budgets, calibrated per-route thresholds, sampling rates, circuit breaker sensitivity, escalation thresholds. |
| **Jurisdiction/regulatory overlay** | Additive restrictions on data classes, source ACLs, retention, evidence-packet fields, escalation routing, action allow/deny per geography or industry. |

The jurisdiction layer is additive only. It may tighten a route — for example, map a previously R1 disclosure to R2, or require fail-closed on a regulated action — but it may not loosen the matrix, remove entitlement, or turn `UNSUPPORTED` into `SUPPORTED`.

### Rule format and zero-LLM enforcement

Rules are deterministic 4-tuples:

```text
(signal, threshold, action, latency_budget)
```

All signals are typed fields from the ledger: `claim.verdict`, `claim.assertion`, `span.acl`, `principal`, `source_id`, `action.R`, `action.tool_schema`, `lane_deadline`. No rule may call an LLM, embedding service, or external model at decision time.

The matrix itself is enforced by the interlock, not authored as a mutable policy rule. Policy DAGs may add predicates that produce verdicts — such as ACL exclusion — but they cannot override the matrix cell that follows.

### Versioning, audit, and validation before live traffic

Every policy version is immutable and hash-chained. Each request ledger records `policy_version` and the exact `rule_id`s that fired. An auditor can reconstruct any actuator from ledger fields, policy version, and matrix cell.

Before any policy change touches live traffic:

1. **Static validation** — schema check, matrix-invariant check, fail-stance floor check, rule-conflict detection, no-LLM-node check.
2. **Shadow replay** — run old and new policy over the last N traces or a representative replay corpus.
3. **Validation report** — produces disposition deltas by matrix cell, new blocks/edits/escalations, removed enforcements, latency deltas by lane, fail-open/closed changes, and expected FP/FN delta.
4. **Canary** — route segment or low-risk route receives the new policy with old/new dual-emit.
5. **Auto-rollback** — if human-override rate exceeds 3× baseline or route error budget breaches, the policy reverts to the previous version.

A policy change that cannot produce a clean validation report does not ship.

## 4. Feedback & Learning Loops

Feedback changes configuration, thresholds, and policy versions. It does not train the control plane into a model.

### Feedback channels

| Channel | Produces | What is updated |
|---|---|---|
| **Human override** | `override_event` attached to original ledger: original actuator, human actuator, reason code, principal, policy version | Calibration candidates for route thresholds, R mapping defects, error budget/circuit breaker threshold |
| **Escalation review** | Label on evidence packet: `confirmed`, `false_positive`, `source_error`, `acl_gap`, `model_error` | Per-route threshold calibration, source-governance alerts, R mapping proposals |
| **Shadow counterfactual** | `would_have_held` / `would_have_passed` events from gated-vs-ungated dual-emit | FNR/FP estimation, earned enforcement per route |
| **Graph-derived signals** | Dead compute, rework, non-convergence terminations, ACL gaps | Route baselines, cost thresholds, source hygiene alerts |

### What is learned / updated

- Per-route NLI acceptance threshold.
- Claim check-worthiness threshold.
- Proof depth and lane budget by route/R tier.
- Error budgets and circuit-breaker sensitivity.
- FNR/FP sampling strata and rates.
- Source/ACL metadata completeness requirements.

These are updated only through a policy release with validation, canary, and rollback.

### What remains rule-based

- Default `UNSUPPORTED`.
- Entitlement/ACL comparison.
- Deterministic numeric/structural recomputation.
- Typed action interlocks.
- Fail stance.
- Matrix cell lookup and actuator emission.

### What is never learned from

- Model confidence or logprobs.
- Model self-reported citations or trust statements.
- User satisfaction as a safety signal.
- Raw production text without evidence labels.
- LLM-as-judge opinions on sampled ambiguity.

The NLI binder and claim extractor change only by offline, versioned model releases. Live feedback never updates weights online.

## 5. Metrics, Monitoring & Trustworthiness Reporting

Measurement has two sources: exact graph observations and statistically valid sampled estimates. No metric assumes a reliable real-time ground truth. Where ground truth is absent, the field stays empty.

### Per-route false-negative rate — the credibility move

Ground truth is obtained by the Adjudicator via stratified sampling:

- 100% of `Block`, `Escalate`, and `Edit` interventions.
- A random slice of `Pass` and `Pass + annotate`.
- Sampled traces go to deterministic source verification and/or human adjudication of ambiguity. No LLM-as-judge.

For route `r`, policy version `v`, window `w`:

```text
FNR(r,v,w) = FN_w / (TP_w + FN_w)
```

Where:

- `TP_w` = weighted count of non-Pass interventions adjudicated gate-worthy.
- `FN_w` = weighted count of Pass / Pass+annotate traces adjudicated gate-worthy.
- Weights = inverse sampling probability per stratum.
- Confidence interval computed by Wilson or bootstrap.

The report schema contains:

```text
route_id
policy_version
window
strata_definitions
sampled_count_per_stratum
stratum_weights
TP
FN
FNR_estimate
CI_lower
CI_upper
ground_truth_method
reviewer/auditor
limitations
value_status: null | prototype_corpus | production_measured
```

Production numbers are not invented. The emptiness is the honesty mechanism.

### False-positive / override rates

Separate metrics, never collapsed:

```text
intervention_precision = TP / (TP + FP)   # among sampled non-Pass interventions
override_rate = human_overrides / sampled_decisions
```

- `FP` = non-Pass intervention adjudicated not gate-worthy.
- `override_rate` is an operational signal for alert fatigue and policy misconfiguration.
- R0/R1 pass+annotate volume is reported separately so over-annotation is visible, not buried.

### Dead compute

Computed exactly from the graph:

```text
dead_step_ratio = steps_with_zero_accepted_claims / total_steps
dead_spend_ratio = cost_of_dead_steps / total_step_cost
rework_rate = near_duplicate_tool_calls / total_tool_calls
non_convergence_terminations = count
estimated_spend_stopped = currency/token sum at termination
```

No model, no estimation.

### Latency by lane

All latency is recorded from ledger timestamps:

```text
lane1_added_p50
lane1_added_p95
lane2_added_p50
lane2_added_p95
action_gate_ms_by_R
hold_back_buffer_ms
timeout_UNKNOWN_count
```

Reported per route. Prototype values are labelled as prototype measurements, not production p95s.

### Entitlement violations

Reported as first-class events:

```text
entitlement_violation_count
breakdown_by_source_class
breakdown_by_principal_class
no_span_pii_secret_count
acl_excluded_span_count
acl_missing_gap_count
overpermissioned_index_incident_count
```

Each event carries `principal`, `source_id`, `source_acl`, `claim_id`, `span_id`, `actuator`. The ACL-gap count is an operational defect signal: a span entering provenance without an ACL must never be treated as public.

### Trustworthiness reporting

The skeptic-facing report is a per-route Gate Report generated from the append-only ledger. It includes:

- `policy_version`
- `enforcement_mode` — shadow, canary, enforce
- matrix cell distribution
- actuator counts
- FNR schema with nulls or measured values
- precision and override rates
- dead compute and rework
- latency by lane
- entitlement violation events
- fail-stance activations

A stakeholder can query any `trace_id`, inspect the graph, and reproduce the actuator from ledger fields, policy version, and the frozen matrix. No composite score appears anywhere.

## 6. Complete Enterprise Solution vs Prototype

| Capability | Full enterprise solution | Stage 1 prototype | Proposal-only |
|---|---|---|---|
| Multi-route route registry | Yes — customer support, internal knowledge, decision-support, agentic routes | Two synthetic routes: refund + internal knowledge | Additional route packs |
| Provenance capture outside model | Production SDK hook + proxy | Live synthetic context assembly hook | Full enterprise source connectors |
| STEP → SPAN → CLAIM → ACTION graph | Yes, per request/session | Yes, live ledger UI | Multi-tenant session graph |
| Default `UNSUPPORTED` | Yes | Yes, visible claim state | — |
| Deterministic entitlement/ACL | Enterprise IAM + source ACL integration | Live synthetic ACL comparison; principal flip | IAM remediation tooling |
| Exact R×S matrix | Immutable interlock lookup | Live matrix cell highlight per actuator | — |
| Two-pending-actions resolution | Yes, all routes with multi-action responses | Refund trace: R1 Edit + R3 Escalate | — |
| Hard action gate | Production action adapter | Mock refund tool cannot commit while held | Real payment/execution integration |
| Surgical Edit | Production edit policy | Live surgical strip/constrained re-invoke | Full regenerative-edit controls |
| Evidence-packet Escalation | Human queue/SLA integration | Live packet display | Triage UI, routing, SLA |
| Cost measurement | Dead compute, rework, non-convergence breaker | Brief backward graph walk if it does not crowd matrix | Full spend/ROI model |
| Policy DAG governance | Layered route/risk/jurisdiction policies, canary, rollback | One default policy version | Jurisdiction-specific packs |
| Feedback loops | Shadow replay, override review, calibration | Not live; described as proposal mechanism | Production-scale feedback pipeline |
| Bias measurement | Async route-level counterfactual replay with CI on decision-shaped routes | Not demonstrated | Full proposal-only bias program |
| Per-route FNR format | Production sampled ground truth | Empty typed schema / labelled prototype values only | Production FNR values |
| Production scale | Tens of thousands of interactions/week, HA, failover | Single-node synthetic traces | Load/HA validation |
| Regulatory posture | Versioned jurisdiction overlays, audit retention, compliance mapping | Not demonstrated | Certification/reporting integration |

**Bias remains proposal-only:** route-level, asynchronous, counterfactual flip-rate with confidence interval. It never becomes a live prototype actuator or a per-response verdict.

## 7. Residual Risks & Explicit Mitigations

### Risk 1 — False assurance on derived/no-ground-truth claims

The plane can still be wrong when a derived or synthesized claim looks supported by a shallow span. Multi-route expansion increases this surface, especially in decision-support routes.

**Mitigation:**

- Derived claims are recomputed from spans or returned `UNKNOWN`; they are never marked `SUPPORTED` by entailment alone.
- `UNKNOWN` never collapses into `SUPPORTED`.
- Proof depth is bounded; timeout returns `UNKNOWN` and is routed by the matrix, not silently accepted.
- Verifiers are decorrelated from the generator.
- FNR sampling publishes the plane’s own miss rate rather than claiming detection.

### Risk 2 — Entitlement enforcement depends on upstream ACL fidelity

If a source system supplies stale, missing, or incorrect ACLs, the deterministic check becomes false safety or operational noise.

**Mitigation:**

- Provenance contract requires `source_id · ACL · hash · offsets` at assembly.
- Missing ACL is recorded as `acl_unknown` and treated as unentitled for privileged routes.
- ACL gaps are a first-class metric and source-governance incident.
- The plane never infers ACLs from model behavior, embeddings, or content.
- Enterprise IAM integration is a stated dependency, not an assumed capability.

### Risk 3 — Policy/config drift causing over-flagging and bypass

If routes are over-tuned to block or escalate, users will bypass the plane. If under-tuned, liability returns. This is the exact over-flagging/under-flagging tradeoff.

**Mitigation:**

- No policy change ships without shadow replay validation and a canary.
- Auto-rollback triggers on human override rate > 3× baseline or error budget breach.
- R0/R1 defaults to `Pass` or `Pass + annotate`; the hard gate is only on actions.
- Circuit breaker downgrades autonomy rather than blocking all traffic.
- Precision/override rates are published per route, so over-flagging is visible and correctable.

## 8. Fidelity Self-Check

| Frozen invariant | Status |
|---|---|
| **Default = `UNSUPPORTED`** | Confirmed. Claims must earn `SUPPORTED` against captured spans. |
| **Entitlement / ACL check** | Confirmed. Caller principal vs source ACL remains deterministic and inline. |
| **Exact R×S matrix** | Confirmed. Transcribed or referenced, never redrawn. No route or policy layer may alter cells, columns, rows, or actuators. |
| **Hard gate on actions, not tokens** | Confirmed. Text may stream behind hold-back; action commit is gated. |
| **LLM-as-judge on the critical path** | Not introduced. Decision-time evaluation is deterministic; no LLM at policy evaluation or matrix lookup. |
| **Two-pending-actions resolution** | Confirmed. Refund trace remains R1 Edit + R3 Escalate, never collapsed into one response-level verdict. |
| **Bias as per-response verdict** | Not introduced. Bias is route-level async counterfactual measurement in the full solution, not a live actuator or matrix verdict. |

No new detector, composite score, confidence threshold, or open-web truth layer enters the system. The multi-route expansion is configuration, evidence, and measurement around the same admission-control core.