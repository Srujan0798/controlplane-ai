# ControlPlane.ai — Architecture

**Accenture Innovation Challenge 2026 · PS #1 · Team ControlPlane**
Choda Srujan Sai · Dhrithika — IIT Gandhinagar

> Frozen at Stage 2, corrected by the Stage-6 elevation pass. This is the system of record.
> Round 1 shipped against it. Round 2 builds against it.

---

## 1. Core thesis

> **An AI response is not text to be scored — it is a set of claims requesting permission to act.**

ControlPlane binds every claim to the evidence the model was actually given, and spends
verification budget in proportion to what the response is about to do. Performance, cost and
responsibility are not three detectors bolted together; they are **three reads of one graph**.

The cost of a wrong output changed category: it used to be a bad paragraph, it is now an
executed transaction.

---

## 2. The primitive — one graph, built during generation

Everything downstream reads a single structure, assembled *while* the response is produced
rather than reconstructed afterwards:

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
- **Responsibility reads its labels** — is the caller entitled to every span a claim binds to,
  and does the action fall inside its typed interlock?

One structure, three axes, three actuators. This is why it is a control plane and not three
classifiers in a trench coat — and it is the single most explainable idea we have.

**The keystone is the context-assembly hook.** If exactly one thing gets built, build the
Provenance Recorder. Every other mechanism degrades to a generic guardrail without it.

---

## 3. Detection

### Performance — "confidently wrong"

**Signal:** assertion strength × groundedness deficit. *Not confidence.* The brief names the
failure as **confidently** wrong; confidence is therefore the broken instrument and cannot
also be the detector.

In strict cost order:

1. **Claim extraction at sentence boundaries** by a small streaming model (1–3B), emitting only
   *check-worthy typed* propositions — numbers, entities, dates, quantities, causal and policy
   assertions. Each tagged **categorical** or **hedged**. Sentence-boundary buffering prevents
   claims fragmenting across token boundaries.
2. **Route by claim type, not through one detector:**
   - **Numeric / structural / temporal → deterministic recomputation** against the span set.
     Sub-millisecond, near-zero false positives, and it covers the errors that cost money.
   - **Textual / factual → binding.** Hybrid retrieval over the *provenance set only* (never the
     open web) → NLI cross-encoder (~300M, 5–15ms batched) → `SUPPORTED / CONTRADICTED /
     UNSUPPORTED / UNKNOWN`. **Default verdict is UNSUPPORTED. A claim must earn SUPPORTED.**
   - **Derived / multi-hop / aggregative → never entailed.** Recompute from spans, or return
     UNKNOWN. This is the boundary against false assurance (§7).
3. **Ungrounded routes** (purely parametric, no retrieval context) have no binding to perform.
   The async lane runs a **semantic-entropy probe**: k=5 resamples, clustered by meaning,
   dispersion measured. High dispersion + categorical assertion = confidently wrong. Off the
   critical path by construction.
4. **Response verdict = worst claim, weighted by that claim's role in the pending action.**
   Never an average.

**FP control:** check-worthiness filtering removes the largest false-positive class before any
model runs; the cheap tier flags and the expensive tier confirms; `UNKNOWN` is a first-class
verdict that *routes* rather than blocks; thresholds calibrated **per route**, never globally.

### Cost — waste and rework

**Signal:** evidence yield per unit of spend, and non-convergence.

1. **Dead compute, computed exactly.** Walk the graph backward: every SUPPORTED claim in the
   accepted answer points to a span, which points to the step that produced it. **Any step
   grounding zero accepted claims is dead compute** — no model, no estimation. No competitor
   will have this number, because no competitor has the graph.
2. **Rework, deterministically.** Near-duplicate tool calls in-trace (exact arg hash, then
   arg-embedding cosine), retry loops, re-retrieval of spans already in context, semantic-hash
   hits against recent outputs.
3. **Non-convergence breaker, live.** Track evidence-yield-per-step, token-to-state velocity and
   plan-state advancement together. When spend climbs while evidence yield decays **and** plan
   state fails to transition, the agent is looping — the three-signal conjunction separates a
   genuine loop from legitimate repetition. ControlPlane then **injects an out-of-band stop
   sequence into the provider API and terminates the call.** Billing stops mid-generation.
   *Cost never blocks a user's answer; it kills a runaway loop.*
4. **Route baselines on robust statistics.** Streaming **median + 3.5×MAD**, not mean and σ.
   Cold start excluded; baselines per route and per tenant.

### Responsibility — three problems, three mechanisms

Leakage, bias and safety have different mathematics, error costs and owners. Collapsing them
into one classifier is the generic move.

1. **Leakage = set membership + entitlement, not classification.** Two deterministic rules:
   - A PII/secret-shaped entity binding to **no span** = model-memory leak or fabrication → **Block.**
   - An entity binding to a span whose **source ACL excludes the calling principal** =
     *retrieval-side authorization failure* → **Block.**

   The second catches the most common real enterprise incident — an over-permissioned RAG index
   faithfully leaking HR data to the wrong employee — and **no LLM-judge wrapper catches it,
   because none of them carry identity into the verification layer.** Aho-Corasick pass over the
   entity set plus an ACL lookup: microseconds, near-zero FP.
2. **Bias = counterfactual invariance, route-level, async.** For decision-shaped outputs the
   shadow lane replays requests with protected attributes perturbed and measures **decision flip
   rate with a confidence interval over a rolling window.** Flag when the CI excludes zero.
   Per-response bias verdicts are statistically illiterate; bias is a distributional property or
   it is nothing.
3. **Safety = typed interlocks on the action, not on the prose.** Declarative versioned rules
   over `tool × argument schema × irreversibility`. Any call outside the allow-listed action
   grammar fails at parse time. Text toxicity classifiers stay a cheap Lane-1 tier — they detect
   banned surface forms, not wrongness — never the product.

---

## 4. Decision policy

Two inputs govern every decision: **blast radius R** (what this response can break) and
**verdict severity S** (what the evidence says).

**R = irreversibility × audience × data class × autonomy level**

| Tier | Meaning |
|---|---|
| **R0** | internal draft, a human reads it first |
| **R1** | user-visible, read-only |
| **R2** | reversible write / external send |
| **R3** | irreversible or regulated — payment, deletion, publication, regulated advice |

### The matrix — transcribed, never redrawn

|  | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** | **Block** | Escalate | Escalate | Escalate |
| **R2** | **Block** | Edit | Edit | Escalate |
| **R1** | Edit | Edit | Pass + annotate | Pass + annotate |
| **R0** | Pass + annotate | Pass + annotate | Pass | Pass |

**The verdict is hostile; the action is proportionate.** A claim must earn SUPPORTED, but merely
failing to earn it only blocks where the blast radius justifies blocking.

> **Load-bearing.** Six of seven models corrupted this matrix when asked to redraw it — inventing
> verdict tiers, putting the three detection axes on the severity axis, or flattening the whole
> R3 row to Block. Axis labels, column vocabulary and cell values are all load-bearing.
> **Transcribe it. Never redraw it.**

### Four actuators

- **Edit is surgical, never generative.** Strip the unsupported claim, or re-invoke the generator
  **once** with a constrained instruction naming the exact failing span. Edited output re-enters
  the gate; a second failure falls through to Escalate. Free-form LLM rewriting produces a new
  *unverified* artifact — that is moving the problem, not solving it.
- **Escalate ships an evidence packet, not an alert:** the claim, the candidate spans, the
  verdict, the diff. Escalation without a packet is what everyone else builds.
- **Autonomy downgrade** — demote a route from *act* to *propose* instead of blocking outright.
- **Circuit breaker** — per-route error budget, SRE-style. When gate-fail rate over a sliding
  window exceeds budget, the route drops an autonomy tier until it recovers.

### Encoding and governance

Rules are 4-tuples `(signal, threshold, action, latency_budget)` in a **versioned DAG**, not
nested conditionals. The engine is a **pure rule engine: zero LLM reasoning at decision time.**

**Fail stance is not the same object as the action.** The matrix says what to do when evidence
*arrives* and is bad. Fail stance says what to do when evidence *does not arrive in time*.
Conflating them is the most common way a gating system silently fails. Every rule declares a
fail stance **belonging to the tier, not to a global default**: R0/R1 fail **open with
annotation**; R2/R3 fail **closed or escalate**. A universal fail-open makes the plane bypassable
by anyone who can induce load.

No threshold change ships without a **shadow replay over the last N traces** showing the FP/FN
delta; every change canaries by route and **auto-rolls back if human-override rate exceeds 3×
baseline.** Every decision is written to an **append-only, hash-chained ledger** carrying the
exact evidence fragment that caused it.

**User surface: three states — Verified / Uncertain / Blocked** — one claim-level line each. No
raw scores; scores produce alert fatigue and cannot be acted on.

---

## 5. Latency

**The core move: the expensive part is precomputed by construction.** Provenance is indexed at
context-assembly time, so binding is a **lookup against a small in-memory set, not a search over
a corpus.** That single choice removes most of the apparent cost of verification.

1. **Verify the stream, not the finished response.** Extraction and binding run at sentence
   boundaries *during* generation. Marginal latency ≈ one sentence, not one response.
2. **Hold-back buffer, not binary blocking.** Stream on a ~150–300ms trailing delay. Failures
   inside the buffer never reach the user. Chosen over emit-then-recall: post-hoc retraction has
   a liability gap by construction.
3. **The hard gate is on actions, not tokens.** Users perceive speed from *text*; harm lives in
   the *commit path*. Gating a tool call costs 20–40ms against a 200ms–2s round-trip — invisible.
4. **Three lanes.** Lane 1 — inline, hard 30–60ms p95, deterministic only (span membership, ACL,
   typed interlocks, arithmetic, Aho-Corasick PII; no LLM, no network hop). Lane 2 — near-line,
   100–400ms, NLI binding for flagged claims and high-R traffic only. Lane 3 — async
   (semantic-entropy, counterfactual bias replay, calibration, shadow replay).
5. **Speculative gating.** Verify tool-call arguments *while the tool call is in flight* —
   speculative **verification**, never speculative **release**.
6. **Proof cache** keyed by context hash, short TTL. Cache hit → suite skipped.
7. **Budget follows blast radius.** R0/R1 is 80–90% of volume and gets Lane 1 only.
8. **Bounded proof depth** — max 2 hops, timeout → UNKNOWN → routed by the matrix.
9. **Shadow is the default deployment mode.** Gated-vs-ungated dual-emit before enforcement,
   producing the counterfactual — *"would have held N, of which M were true positives."*
10. **Deployment shape:** an **OpenAI-compatible reverse proxy** plus a thin context-assembly SDK
    hook. No application rewrite, no model access, no weights, no logits, no fine-tuning.

> **Targets: ≤40ms p50 and ≤200ms p95** added on R0/R1 text; action gating amortized inside tool
> latency. **Never quote 40ms as p95** — that is a five-fold overclaim and dead on contact in
> questioning. This error was live in three places before the elevation pass caught it.

---

## 6. Internal structure

**Yes, multi-agent — but a deadline-driven pipeline over a typed artifact, and most workers are
not LLMs.** Specialization and isolation, not conversation. No debate, no voting, no
chain-of-thought passed between roles.

**Shared artifact — the Evidence Ledger** (append-only, hash-chained, one per request):

```
{ principal, action_intent, R_tier, spans[], claims[], bindings[],
  step_yield[], verdicts[], policy_version, verifier_versions, latency_spent }
```

**Nothing is passed as free text.**

| Role | Lane | Owns | LLM? |
|---|---|---|---|
| **Provenance Recorder** | inline, ~0ms | Hooks context assembly; captures every span with source, ACL, hash, offsets. Ground truth of *what the model was allowed to know*. | No |
| **Claim Extractor** | streaming | Typed check-worthy claims + assertion strength | Small (1–3B) |
| **Prosecutor** | 1 + 2 | Attempts to *prove* each claim; default verdict unsupported | NLI ~300M |
| **Entitlement Auditor** | 1 | Output entities vs caller identity and source ACLs. Owns leakage. | No |
| **Economist** | 1 + 3 | Step yield, dead compute, non-convergence breaker, route baselines | No |
| **Action Interlock** | 1 | Computes R, applies the matrix, emits the actuator. **Everything else advises; only this decides.** | No |
| **Adjudicator** | 3 | Stratified sampling to ground truth; per-route precision / recall / FNR | Mixed |
| **Red Team** | offline | Adversarially probes **ControlPlane's own validators**. Never touches the live path. | Yes |

**Coordination under time pressure:** every role has a hard deadline and a declared degraded
output. Missing the deadline returns `UNKNOWN`, resolved via that tier's fail stance. No role
blocks another. **The Interlock decides on whatever is in the ledger when the clock expires —
deadline-driven, not consensus-driven.** Fast deterministic roles may block; slow probabilistic
roles may only annotate or re-gate. **A slow check never overturns a fast decision.**

---

## 7. Strongest residual risk — false assurance on derived claims

Multi-hop, aggregated and synthesized claims are where entailment is weakest and where the value
is highest. If the Prosecutor marks a subtly-wrong synthesized claim SUPPORTED because a shallow
span looks similar, ControlPlane delivers **false assurance — strictly worse than no control
plane, because humans stop checking.**

**Mitigation, three lines:**

- **Route derived claims away from NLI entirely.** Arithmetic or aggregative → *recomputed* from
  spans. Neither recomputable nor directly entailed → UNKNOWN. **UNKNOWN never collapses into
  SUPPORTED** — that one rule is the boundary between a control plane and false assurance.
- **Decorrelate by construction.** Verifiers come from a different model family than the
  generator, and the deterministic checks carry the majority of enforcement weight *precisely
  because* they cannot share the generator's failure modes.
- **Publish the plane's own error bars.** Stratified shadow audit — 100% of blocks and
  escalations plus a random slice of passes — sampled to expensive ground truth.

The claim is never *"we catch hallucinations."* It has the shape:

> **"On this route we catch \<measured\>% of ungrounded claims at 40ms p50 — and here is the
> \<measured\>% we don't."**

**Every team will claim detection. Publishing your own false-negative rate is the move none of
them will make.**

---

## 8. Rejected approaches — and why

Nine mechanisms were removed outright. Each was proposed by at least one model and each is a trap.

| Rejected | Why it dies |
|---|---|
| **Model-emitted citations / hidden `<claim><source>` traces** | The model grades its own homework. A model that fabricates a fact fabricates the citation with equal fluency. Provenance must be captured **outside** the model, where it is tamper-proof — and only then does it carry the ACL that makes entitlement possible. |
| **Speculative release with post-hoc recall** | A liability gap by construction: the harm is delivered, then withdrawn. The hold-back buffer buys the same perceived speed with no gap. |
| **Universal fail-open on SLA breach** | Makes the plane bypassable by inducing load — an attacker's first move. Fail stance belongs to the tier. |
| **Cosine-similarity threshold as a verdict** | `0.7`/`0.85` are magic numbers on an embedding distance, not a decision. Domain drift moves them constantly. |
| **Rolling z-score cost anomaly** | Not robust; pathological traces drag the mean. Median + MAD is the same idea done correctly. |
| **GBDT rework-probability predictor** | Needs labelled history per query class, hostile to cold start, and *predicts* what direct trace inspection *observes*. |
| **Demographic parity vs source base rates** | Base rate undefined in most deployments. Counterfactual replay measures a causal, auditable quantity instead. |
| **"Interrogator" LLM attacking the generator** | LLM-as-judge in a costume, and it depends on the already-killed self-reported trace. Same model family = correlated blind spots. |
| **Composite 0–100 risk score** | Rejected by all seven models independently. Cannot be decomposed by policy or acted on by a user. **You cannot block, edit or escalate on 87.** |

Also rejected: LLM-as-judge on the critical path · confidence/logprob thresholding as the
hallucination signal · static keyword guardrails as the product · dashboards as the deliverable ·
debate/voting for real-time gating · uniform validation depth across all traffic · any design
assuming access to weights, logits or fine-tuning.

---

## 9. The running example — one trace, three axes

A refund agent. **`Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor
agreement.`** Every filter passed it. Confidence 0.94. Money moved Tuesday, found Friday.

**Clause 7.2 does not exist.**

| Axis | What happens |
|---|---|
| **Performance** | 14 spans captured; the response decomposes into 6 claims, all starting UNSUPPORTED. Five bind. *"Clause 7.2 permits this refund"* finds no span. It stays red — **not low-confidence, unproven.** |
| **Responsibility** | One span that *did* ground a claim came from a document whose ACL excludes the caller. Deterministic. No classifier involved. |
| **Cost** | Walk the graph backward: of 9 tool calls, 4 grounded nothing. The meter ran on all nine. |

### Two pending actions — the resolution that matters

The response carries **two** pending actions, and the architecture prices them separately
(*worst claim, weighted by that claim's role in the pending action*):

| Pending action | Tier | Finding | Matrix cell | Actuator |
|---|---|---|---|---|
| Show text to the customer | **R1** user-visible | unentitled span grounds a claim in the text | R1 × entitlement | **Edit** — stripped |
| Issue the refund | **R3** irreversible | clause 7.2 has no span | R3 × unsupported-categorical | **Escalate** — held |

Both are correct simultaneously. This is the frozen matrix read properly — and it is a *better*
demonstration than a single lookup, because it shows the matrix doing something more
sophisticated. **Proof scales with consequence.**

---

## 10. Content law — nine facts that were corrupted repeatedly

Seven models tested these against each other across five stages. Each was broken by at least one.

1. **Clause 7.2 does not exist.** Never "caps," never "denies," never "doesn't cover." The
   failure is *absence* of evidence, not conflicting evidence — which is what puts it in the
   unsupported column and makes **Escalate** the correct actuator rather than Block.
2. **Never say "blocked" about the refund.** R3 × unsupported-categorical = **Escalate**. Say
   *held and escalated with the evidence packet.*
3. **The company wrongly pays out ₹1,84,000.** The customer did not lose money. Two models
   inverted this; one inverted the entire premise by having the refund *denied*.
4. **The matrix is transcribed, never redrawn.**
5. **Actuators are exactly Block · Edit · Escalate · Pass** (plus autonomy downgrade and circuit
   breaker, which are spoken, not drawn). `STREAM`, `Kill Span`, `Terminate Step`,
   `Hold & Re-verify`, `Redact & Flag` are all invented. Cut.
6. **Latency is ≤40 ms p50 / ≤200 ms p95.** Never quote a number the architecture doesn't hold.
7. **The gate report ships as an empty schema with typed placeholders.** Never fabricated
   numbers. **The emptiness is the credibility play.** A judge who tests it finds the honesty
   rather than the bluff.
8. **The refuse-to-claim list is about *us*** — eliminate hallucinations, zero integration, zero
   latency, one accuracy number. It is *not* the rejected-approaches list. Five of seven models
   confused the two. Every deck disclaims its competitors; almost none disclaim themselves.
9. **Do not drop bias.** The brief names it explicitly under responsibility; omitting it scores
   against the rubric. Keep it, stated in *measurement* terms, never moral ones.

---

## 11. Model reliability — for Round 2's input set

Five stages of adversarial merge plus an elevation pass produced a consistent, diagnosable
pattern:

| Model | Verdict |
|---|---|
| **Claude, Kimi** | Reliable across all stages. Primary inputs. |
| **GLM** | Caught the single biggest logical defect nobody else saw (the entitlement contradiction). Its *fix* was wrong; its *diagnosis* was right. Useful as an adversary, not as an author. |
| **MiniMax, Gemini, Mistral** | Mine for surviving mechanisms and production catches. Gemini and MiniMax each contributed real production rules. Fidelity is inconsistent. |
| **GPT** | **Drop from the input set.** Strong at Stage 2, then off-freeze at Stages 3, 4, 5 *and* the elevation review — four consecutive stages. The failure is specific, not random: **it regenerates from its own Stage 2 proposal rather than from the frozen spec**, re-importing every mechanism the merge demoted. By Stage 5 it inverted the running example. Nothing survived from Stages 4 or 5. |

**Standing rule:** run any proposal through the fidelity check *first*, weight it after. A
narrative proposal can quietly re-import mechanisms the architecture already killed, and that is
harder to see than a bad idea.

---

## 12. Freeze notes

- **The keystone is the context-assembly hook.** Build the Provenance Recorder first.
- **The most differentiated single mechanism is the entitlement check** (scored 50/50 across all
  criteria). Deterministic, sub-millisecond, catches a real and expensive enterprise incident,
  and is structurally impossible for any output-only competitor to replicate. Do not trade it
  away for something that demos more easily.
- **The most defensible number is dead compute.** Computed exactly, needs no model, and is the
  number a buyer signs a cheque against.
- **The line that wins the room is the published FNR.**
- **Design is closed.** It took five adversarial merges plus an elevation pass to reach internal
  consistency. Reopening it re-risks contradictions that were expensive to find. If something
  must change, change it here first — every downstream artifact is a rendering of this file.
