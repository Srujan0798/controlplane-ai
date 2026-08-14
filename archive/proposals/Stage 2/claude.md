# ControlPlane.ai — Architecture

## 1. Core Thesis

An AI response is not text to be scored — it is a set of claims requesting permission to act. ControlPlane verifies each claim against the evidence the model was actually given, and spends verification budget in proportion to what the response is about to do, making oversight **admission control in the commit path** rather than analytics on a log.

---

## 2. Detection Layer

### Performance — confidently wrong

**Mechanism: Claim–Evidence Binding (CEB), with inverted burden of proof.**

*Observed:* the token stream, plus the **provenance set** — every retrieved chunk, tool result, DB row and system-context span that entered the model's context, captured at context-assembly time with source ID, ACL, hash, and offsets.

*Computed:*

1. **Atomic claim extraction** (small streaming model, 1–3B): typed check-worthy propositions only — numbers, entities, dates, quantities, causal and policy assertions. Hedging language is scored as **assertion strength** (categorical vs hedged).
2. **Binding**: hybrid retrieval over the provenance set → NLI cross-encoder (~300M, 5–15ms batched) → `SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN`. Default verdict is UNSUPPORTED; a claim must *earn* SUPPORTED.
3. **Numeric and structural claims bypass NLI entirely** into deterministic recomputation: does the figure exist in a tool result, does the arithmetic reconcile, is the date inside the source's range. Highest precision, and it covers the errors that actually cost money.
4. **Response verdict is worst-claim-governs**, weighted by the claim's role in the pending action — not an average. One contradicted refund amount outranks nine correct sentences.

"Confidently wrong" = **assertion strength × groundedness deficit**. A categorical unsupported claim is the flag; a hedged one is a lower tier. That operationalizes the brief's exact phrase instead of measuring "wrong."

*False-positive control:* check-worthiness filtering removes the largest FP class; cheap tier flags, expensive tier confirms; `UNKNOWN` is a first-class verdict that routes rather than blocks; thresholds are calibrated **per route**, not globally.

### Cost — waste and rework

**Mechanism: Marginal Evidence Yield + deterministic rework detection.**

*Observed:* per-step tool calls, arguments, retrieved spans, tokens, latency, outcomes.

*Computed:*

1. **Evidence attribution backwards through the trace.** Every SUPPORTED claim points to a provenance span, which points to the step that produced it. Any step grounding **zero** claims in the accepted answer is **dead compute** — computed exactly, no model required. The headline metric: *fraction of spend that produced no evidence used in the answer.*
2. **Rework detection**: near-duplicate tool calls within a trace (arg-embedding cosine or exact hash), retry loops, re-retrieval of spans already in context.
3. **Route cost baselines**: cost-per-successfully-gated-response distribution per route; flag >p95 traces with no quality gain — this catches "the new prompt made the agent 3× chattier for identical output."
4. **Live intervention, not a report**: forecast remaining steps from trace shape; trip a breaker when evidence-yield-per-step decays while step count climbs (non-converging agent).

*FP control:* dead compute only counts on accepted answers (exploration ending in correct abstention is legitimate); duplicates require N≥2 in-window; baselines are per-route so traffic-mix shifts don't fire.

### Responsibility — leakage, bias, safety

These are three different problems and get three different mechanisms. Collapsing them into one classifier is the generic move.

**Leakage — set membership + entitlement, not classification.** Every entity in the output must trace to a provenance span *that the calling principal is entitled to read*. Two deterministic rules: (a) a PII/secret-shaped entity **not** in the provenance set is model-memory leak or fabrication → block; (b) a span **in** provenance whose source ACL excludes the caller → **retrieval-side authorization failure** → block. This catches the most common real enterprise incident: an over-permissioned RAG index where the model faithfully leaks HR data to the wrong employee. Sub-millisecond, near-zero FP. No LLM-judge wrapper does this, because they never carry identity into the verification layer.

**Bias — counterfactual invariance, sampled, async, route-level.** For decision-shaped outputs (approve/deny/rank/score), the shadow lane replays requests with protected attributes perturbed (name, gender marker, pincode, institution) and measures **decision flip rate with a confidence interval over a rolling window**. Flag when the CI excludes zero. Per-response bias verdicts are statistically illiterate; this is a distributional property or it is nothing.

**Safety — typed interlocks on the action, not the prose.** Declarative, versioned rules over `tool + argument schema + irreversibility`: no `send_email` to an external domain carrying a span from a `confidential` source; no DDL in `execute_sql`; no financial write above threshold without a SUPPORTED numeric binding. Text classifiers remain as a cheap tier, never as the product.

---

## 3. Decision Policy Engine

Two inputs govern every decision: **blast radius R** and **verdict severity S**, modulated by calibrated verifier confidence.

**R = irreversibility × audience × data class × autonomy level**

- **R0** internal draft, human reads first
- **R1** user-visible, read-only
- **R2** reversible write / external send
- **R3** irreversible or regulated (payment, deletion, publication, regulated advice)

| | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown (low verifier confidence) |
|---|---|---|---|---|
| **R3** | Block | Escalate | Escalate | Escalate |
| **R2** | Block | Edit | Edit | Escalate |
| **R1** | Edit | Edit | Pass + annotate | Pass + annotate |
| **R0** | Pass + annotate | Pass + annotate | Pass | Pass |

**Edit is surgical, never generative.** Either strip the unsupported claim, or re-invoke the generator with a constrained instruction naming the exact failing span ("re-grounding retry"), capped at one attempt. Edited output re-enters the gate; a second failure falls through to Escalate. Free-form LLM rewriting would produce a new unverified artifact — that is moving the problem, not solving it.

**Escalate ships an evidence packet**, not an alert: the claim, the candidate spans, the verdict, the diff. Design target is a human resolving in under 20 seconds. Escalation without a packet is what everyone else builds.

**Two additional actuators beyond block/edit/escalate:**

- **Autonomy downgrade** — demote a route from *act* to *propose* rather than blocking it outright.
- **Circuit breaker** — per-route error budget (SRE framing). When gate-fail rate over a sliding window exceeds budget, the route drops an autonomy tier until recovery. That is "catch and act" at the system level, not just per response.

**How the policy stays evidence-gated:** policies are versioned artifacts. No threshold change ships without a **shadow replay** over the last N traces showing the FP/FN delta. Every policy deploys in shadow first, enforces second. The control plane never grants itself authority it hasn't demonstrated.

**How it stays latency-aware:** every policy carries a latency budget and a **declared fail stance** — R0/R1 fail open with annotation, R2/R3 fail closed or escalate. Undeclared timeout behaviour is the most common silent failure of gating systems.

---

## 4. Latency & Non-Blocking Design

1. **Verify the stream, not the finished response.** Claim extraction and binding run at sentence boundaries during generation. When the last token lands, only the final sentence remains to verify. Marginal latency ≈ one sentence, not one response.
2. **Hold-back buffer, not binary blocking.** Stream to the user with a ~150–300ms trailing delay. Failures inside the buffer never reach the user; already-emitted text is retracted or annotated. Most designs pretend block-vs-stream is binary — it isn't.
3. **The hard gate is on actions, not tokens.** Read-only text streams optimistically; anything crossing a side-effect boundary is hard-gated. Users perceive speed from text; safety comes from the commit path. Tool-call gating costs 20–40ms against a 200ms–2s tool round-trip: invisible.
4. **Three lanes.** Lane 1 inline, hard 30–60ms p95 budget, **deterministic only** — provenance membership, ACL, typed interlocks, arithmetic. No LLM, no network hop, sidecar-colocated. Lane 2 near-line 100–400ms — NLI entailment, only for flagged claims or high-R traffic. Lane 3 async — adversarial verification, bias probes, calibration, root-cause clustering, policy replay.
5. **Speculative gating.** Verify tool-call arguments *while the tool call is in flight*; verification completes inside the tool's own latency and is effectively free.
6. **The evidence index is built during generation, not after.** Provenance is indexed at retrieval time, so binding is a lookup rather than a search. This one choice removes most of the apparent cost.
7. **Budget follows blast radius.** R0/R1 is 80–90% of volume and gets Lane 1 only. Expensive verification is spent on the 5–10% that can actually cause harm. Mean added latency stays in tens of milliseconds; the tail lands where it's justified.
8. **Shadow mode is the default deployment**, producing the counterfactual — "would have blocked N, of which M were true positives" — before enforcement is switched on. Also the only realistic enterprise adoption path.
9. **Fail-open with fingerprint.** If the plane is down or over budget, R0/R1 proceeds annotated; R2/R3 falls closed. The plane is never a single point of failure for the whole product, only for dangerous actions.

---

## 5. Internal Multi-Agent Structure

Specialized workers with strict contracts and hard deadlines — **most of them not LLMs**. Coordination is a deadline-driven pipeline over a shared typed artifact, not a conversation between agents.

**Shared artifact — the Evidence Ledger** (append-only, per request):
`{principal, action_intent, R_tier, provenance_spans[], claims[], bindings[], verdicts[], policy_version, verifier_versions, latency_spent}`. Every role reads and appends structured entries. Nothing is passed as free text.

| Role | Lane | Owns |
|---|---|---|
| **Provenance Recorder** | inline, ~0ms | Instruments context assembly; captures every span with source, ACL, hash. Ground truth of *what the model was allowed to know*. Hooking context assembly — not just output — is what makes this a plane and not a wrapper. |
| **Claim Extractor** | streaming | Typed atomic claims + assertion strength |
| **Prosecutor / Binder** | 1+2 | Attempts to *prove* each claim; default verdict is unsupported. Hostile validation made structural. |
| **Entitlement Auditor** | 1, deterministic | Output spans vs caller identity and source ACLs. Owns leakage. |
| **Action Interlock** | 1, deterministic | Computes R, applies the policy table, emits the actuator. Small, auditable, no ML. **Everything else advises; only this decides.** |
| **Adjudicator** | 3, async | Stratified sampling to expensive ground truth; per-route precision/recall/FNR; threshold updates. Owns the plane's own error bars. |
| **Economist** | 3, async | Dead compute, MEY, route baselines, verification spend vs prevented loss. Owns the ROI number the buyer actually cares about. |

**Coordination under time pressure:** every role has a hard deadline and a declared degraded output. Missing the deadline returns `UNKNOWN`, which the Interlock resolves via that tier's fail stance. No role can block another. The Interlock decides on whatever is in the ledger when the clock expires — **deadline-driven, not consensus-driven.**

---

## 6. What This Deliberately Does NOT Do

- **No LLM-as-judge on the critical path.** Slow, uncalibrated, and — when drawn from the same model family as the generator — sharing its blind spots, so the "ensemble" isn't independent. Judges live in the async lane, sampled, and are themselves audited.
- **No confidence or logprob thresholding as the hallucination signal.** The named failure is *confidently* wrong. Confidence is the broken instrument; it cannot be the detector.
- **No static keyword/toxicity guardrail as the core.** Retained as a cheap tier. It detects banned surface forms, not wrongness.
- **No dashboard-first framing.** The dashboard is a projection of the ledger. If the primary artifact is a chart, oversight is still after-the-fact.
- **No free-form LLM rewriting of flagged output.** Subtractive or constrained regeneration only, always re-gated.
- **No single 0–100 "AI safety score."** Three axes with different actuators, owners, and error costs. One number is a demo affordance.
- **No weights, logits, or fine-tuning assumed.** Must sit on any model including closed APIs — everything works from context, output, and trace.
- **No per-response bias verdicts.** Route-level distributions with confidence intervals, or nothing.
- **No blocking read-only text by default.** Over-blocking kills adoption faster than any failure. Enforcement authority is earned per route through shadow evidence.

---

## 7. Strongest Technical Risk

**The binder's false-negative rate on derived claims — and correlated blind spots.**

Multi-hop, aggregated, and synthesized claims are exactly where entailment is weakest and exactly where the value is highest. If the binder marks a subtly-wrong synthesized claim SUPPORTED because a shallow span looks similar, the plane delivers **false assurance** — strictly worse than no plane, because humans stop checking. Worse if the verifier shares the generator's model family and therefore its failure modes.

**Mitigation, in three lines that fit on a slide:**

- **Route derived claims away from NLI.** Anything arithmetic or aggregative is **recomputed** from provenance spans, not entailed. Anything neither recomputable nor directly entailed is `UNKNOWN`. **`UNKNOWN` never collapses into `SUPPORTED`** — that single rule is the boundary between a control plane and false assurance.
- **Decorrelate by construction.** Verifiers come from a different model family than the generator, and the deterministic checks — provenance membership, entitlement, arithmetic — carry the majority of enforcement weight precisely because they cannot share the generator's blind spot.
- **Publish the plane's own error bars.** Stratified shadow audit (100% of blocks and escalations, plus a random slice of passes) to expensive ground truth; the Adjudicator reports per-route precision, recall and FNR with confidence intervals. The claim is never "we catch hallucinations." It is: *"on this route we catch 94% of ungrounded claims at 40ms p95, and here is the 6% we don't."*

That last line is the credibility play. Every team will claim detection. Stating your own false-negative rate is the move none of them will make.
