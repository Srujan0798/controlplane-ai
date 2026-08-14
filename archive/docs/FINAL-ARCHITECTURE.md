# ControlPlane.ai — Frozen Stage 2 Architecture

### Adversarial merge of 7 independent proposals (claude · gpt · kimi · glm · gemini · minimax · mistral)

**Problem statement:** Accenture Innovation Challenge 2026, Round 1, PS #1 — ControlPlane.ai.
**Deliverable constraint:** 3-slide concept deck + 3-minute video.
**Merge weighting:** claude / gpt / kimi read twice and treated as primary; glm / gemini / minimax / mistral mined for surviving mechanisms.

---

# PART A — MECHANISM INVENTORY & SCORING

74 distinct mechanisms were extracted across the seven proposals. Each is scored 1–10 on
**C**oncreteness (explainable in 20–30s) · **D**ifferentiation (more than "ask another LLM") ·
**S**ystems depth · **L**atency realism · **E**vidence-gate fit. Total /50.

Verdicts: **KEEP** (survives into the final design) · **FOLD** (absorbed into a stronger mechanism) · **KILL** (removed).

## A1 — Performance detection


| #   | Mechanism                                                                       | Source                             | C   | D   | S   | L   | E   | Σ      | Verdict                                                                          |
| --- | ------------------------------------------------------------------------------- | ---------------------------------- | --- | --- | --- | --- | --- | ------ | -------------------------------------------------------------------------------- |
| 1   | **Provenance set captured at context-assembly** (source id, ACL, hash, offsets) | claude                             | 9   | 10  | 10  | 10  | 10  | **49** | **KEEP — keystone**                                                              |
| 2   | Streaming atomic claim extraction, typed + check-worthy only                    | claude, glm, gpt, minimax, mistral | 9   | 7   | 8   | 8   | 9   | 41     | KEEP                                                                             |
| 3   | **Assertion strength** (categorical vs hedged) as the *"confidently"* term      | claude                             | 10  | 9   | 7   | 10  | 9   | 45     | KEEP                                                                             |
| 4   | NLI binding with **inverted burden of proof** (default UNSUPPORTED)             | claude                             | 8   | 9   | 9   | 8   | 10  | 44     | KEEP                                                                             |
| 5   | **Deterministic recomputation** of numeric/structural claims (bypass NLI)       | claude                             | 10  | 9   | 10  | 10  | 10  | **49** | **KEEP**                                                                         |
| 6   | Worst-claim-governs, weighted by role in the pending action                     | claude                             | 10  | 8   | 8   | 10  | 9   | 45     | KEEP                                                                             |
| 7   | Evidence Coverage Score (fraction of claims with a source)                      | gpt, minimax                       | 9   | 5   | 5   | 8   | 7   | 34     | FOLD → #4 (it is the *aggregate of bindings*; a reported metric, not a detector) |
| 8   | Cosine-similarity threshold 0.7 / 0.85 as the verdict                           | gemini, glm, mistral               | 7   | 3   | 3   | 9   | 4   | 26     | **KILL**                                                                         |
| 9   | Semantic-entropy probe (k=5 resamples, meaning-clustered, dispersion)           | kimi                               | 7   | 9   | 8   | 3   | 6   | 33     | FOLD → async lane, ungrounded routes only                                        |
| 10  | Cached knowledge-graph lookup <5ms                                              | kimi                               | 6   | 5   | 5   | 8   | 6   | 30     | FOLD → KG is just another span source                                            |
| 11  | Model emits `<claim>X</claim><source>Y</source>` hidden trace                   | gemini                             | 8   | 2   | 2   | 8   | 2   | 22     | **KILL**                                                                         |
| 12  | Citation-wrapper prompt template forcing `[CLAIM:][EVIDENCE:]`                  | mistral                            | 7   | 2   | 3   | 7   | 2   | 21     | **KILL**                                                                         |
| 13  | High verbal confidence ∧ low ECS conjunction                                    | gpt, minimax, mistral              | 7   | 4   | 4   | 9   | 5   | 29     | FOLD → survives only as #3                                                       |
| 14  | Flag only CONTRADICTED, never UNSUPPORTED                                       | glm                                | 8   | 5   | 6   | 9   | 4   | 32     | FOLD → resolved by the R×S matrix (see C2)                                       |




## A2 — Cost detection


| #   | Mechanism                                                                                    | Source                | C   | D   | S   | L   | E   | Σ      | Verdict                                                                           |
| --- | -------------------------------------------------------------------------------------------- | --------------------- | --- | --- | --- | --- | --- | ------ | --------------------------------------------------------------------------------- |
| 15  | **Dead compute** via backward evidence attribution (step → span → claim)                     | claude                | 9   | 10  | 10  | 10  | 10  | **49** | **KEEP — headline metric**                                                        |
| 16  | Rework detection: duplicate tool calls, retry loops, re-retrieval                            | claude, gpt, minimax  | 10  | 7   | 8   | 10  | 7   | 42     | KEEP                                                                              |
| 17  | Per-route cost baselines, flag >p95 with no quality gain                                     | claude                | 8   | 6   | 8   | 10  | 6   | 38     | KEEP (statistic upgraded by #20)                                                  |
| 18  | Non-convergence breaker (evidence yield decays as step count climbs)                         | claude                | 8   | 9   | 9   | 9   | 8   | 43     | KEEP                                                                              |
| 19  | MCUT / CPUT — useful-token ratio                                                             | gpt, minimax, mistral | 8   | 6   | 6   | 9   | 7   | 36     | FOLD → #15 computes the same thing *exactly* instead of by ratio                  |
| 20  | Robust statistic: streaming **median + 3.5×MAD**, per-tenant, cold-start excluded            | mistral               | 8   | 6   | 9   | 10  | 6   | 39     | KEEP → becomes the statistic for #17                                              |
| 21  | Rolling z-score over 1h baseline                                                             | gpt, minimax          | 8   | 4   | 5   | 10  | 5   | 32     | **KILL** (not robust; MAD supersedes)                                             |
| 22  | Token-to-state velocity (tokens per confirmed state change)                                  | gemini                | 9   | 7   | 7   | 10  | 6   | 39     | KEEP → cheap inline signal for #18                                                |
| 23  | Semantic loop detector + **plan-state advancement** check                                    | glm                   | 8   | 7   | 8   | 9   | 6   | 38     | KEEP → plan-state check is the FP control for #18                                 |
| 24  | GBDT rework-probability predictor on historical telemetry                                    | kimi                  | 6   | 7   | 6   | 8   | 4   | 31     | **KILL** (needs per-class labels, cold-start hostile, predicts what #16 observes) |
| 25  | Semantic-hash cache hit (>95% similar output already produced at <10% cost)                  | kimi                  | 9   | 7   | 7   | 9   | 6   | 38     | KEEP                                                                              |
| 26  | **Out-of-band stop-sequence injection** into the provider API — kills billing mid-generation | glm                   | 10  | 10  | 9   | 10  | 7   | **46** | **KEEP — the only real-time cost *actuator* in any proposal**                     |
| 27  | Rework ratio — user re-asks same intent within 3 turns                                       | gpt, minimax          | 8   | 5   | 5   | 9   | 5   | 32     | FOLD → Lane 3 session metric                                                      |




## A3 — Responsibility detection


| #   | Mechanism                                                                             | Source                     | C   | D   | S   | L   | E   | Σ      | Verdict                                                                          |
| --- | ------------------------------------------------------------------------------------- | -------------------------- | --- | --- | --- | --- | --- | ------ | -------------------------------------------------------------------------------- |
| 28  | **Entitlement check** — output entity → span → *calling principal's* ACL              | claude                     | 10  | 10  | 10  | 10  | 10  | **50** | **KEEP — most differentiated mechanism in the entire set**                       |
| 29  | Set-membership leak rule (PII-shaped entity bound to **no** span = memory leak)       | claude                     | 10  | 9   | 9   | 10  | 10  | **48** | **KEEP**                                                                         |
| 30  | Counterfactual invariance — protected-attribute replay, route-level, CI excludes zero | claude, kimi               | 9   | 9   | 9   | 8   | 8   | 43     | KEEP                                                                             |
| 31  | **Typed action interlocks** (tool × arg schema × irreversibility)                     | claude, kimi               | 10  | 9   | 10  | 10  | 9   | **48** | **KEEP**                                                                         |
| 32  | Aho-Corasick / DFA PII scan in microseconds                                           | gemini, mistral, glm, kimi | 10  | 4   | 8   | 10  | 6   | 38     | KEEP → as the *implementation* of #29's entity pass, not as the product          |
| 33  | Distilled safety classifier ≤1B params                                                | gpt, minimax, mistral      | 8   | 4   | 6   | 8   | 4   | 30     | FOLD → cheap Lane-1 tier only                                                    |
| 34  | Contextual NER (DeBERTa-v3-base, ~8ms)                                                | minimax, glm               | 8   | 4   | 7   | 8   | 5   | 32     | FOLD → entity extractor feeding #28/#29                                          |
| 35  | Demographic parity vs "base rates from the source dataset"                            | gpt, minimax               | 6   | 5   | 5   | 8   | 5   | 29     | **KILL** (base rate undefined in most deployments; #30 is causal and measurable) |
| 36  | Constrained action grammar, rejected at parse time                                    | kimi                       | 9   | 8   | 9   | 10  | 8   | 44     | FOLD → #31 (same mechanism; kimi's parse-time framing is the implementation)     |




## A4 — Decision policy


| #   | Mechanism                                                                                 | Source       | C   | D   | S   | L   | E   | Σ      | Verdict                                                                                  |
| --- | ----------------------------------------------------------------------------------------- | ------------ | --- | --- | --- | --- | --- | ------ | ---------------------------------------------------------------------------------------- |
| 37  | **Blast radius R0–R3 × verdict severity matrix**                                          | claude       | 10  | 10  | 10  | 10  | 10  | **50** | **KEEP — the spine**                                                                     |
| 38  | Policy as a **DAG of 4-tuples** `(signal, threshold, action, latency_budget)`             | gpt, minimax | 9   | 6   | 9   | 9   | 7   | 40     | KEEP → the encoding of #37                                                               |
| 39  | Latency-breach auto-downgrade Block → Escalate → Flag                                     | gpt, minimax | 9   | 7   | 8   | 10  | 6   | 40     | FOLD → superseded by per-tier declared fail stance (#46), which is strictly more precise |
| 40  | **Edit is surgical, never generative** (strip or one constrained re-ground, then re-gate) | claude       | 10  | 9   | 9   | 9   | 10  | 47     | KEEP                                                                                     |
| 41  | **Escalate ships an evidence packet**, target <20s human resolution                       | claude       | 10  | 9   | 9   | 10  | 10  | 48     | KEEP                                                                                     |
| 42  | Autonomy downgrade (route demoted *act* → *propose*)                                      | claude       | 9   | 9   | 10  | 10  | 8   | 46     | KEEP                                                                                     |
| 43  | Circuit breaker on per-route error budget                                                 | claude       | 9   | 8   | 10  | 10  | 8   | 45     | KEEP                                                                                     |
| 44  | Policy change requires **shadow replay** over last N traces before enforcing              | claude       | 9   | 9   | 10  | 10  | 10  | 48     | KEEP                                                                                     |
| 45  | Canary deploy + auto-rollback if human-override rate spikes >3× baseline                  | gpt, minimax | 9   | 7   | 9   | 10  | 7   | 42     | KEEP                                                                                     |
| 46  | **Declared fail stance per blast-radius tier**                                            | claude       | 10  | 9   | 10  | 10  | 9   | 48     | KEEP                                                                                     |
| 47  | Hard state machine, per-validator TTL, safe default at deadline                           | kimi         | 9   | 7   | 9   | 10  | 8   | 43     | FOLD → #38 + #46                                                                         |
| 48  | Universal fail-open when a Block misses its SLA                                           | mistral, gpt | 9   | 2   | 3   | 10  | 2   | 26     | **KILL**                                                                                 |
| 49  | Hash-chained, tamper-evident decision log                                                 | mistral      | 9   | 7   | 9   | 10  | 9   | 44     | KEEP                                                                                     |
| 50  | Three-state user surface: **Verified / Uncertain / Blocked**, one line each               | kimi         | 10  | 7   | 7   | 10  | 8   | 42     | KEEP                                                                                     |




## A5 — Latency & non-blocking


| #   | Mechanism                                                                    | Source                        | C   | D   | S   | L   | E   | Σ      | Verdict                                                      |
| --- | ---------------------------------------------------------------------------- | ----------------------------- | --- | --- | --- | --- | --- | ------ | ------------------------------------------------------------ |
| 51  | Verify at **sentence boundaries during generation**, not after               | claude, glm                   | 9   | 9   | 9   | 9   | 9   | 45     | KEEP                                                         |
| 52  | **Hold-back buffer** (~150–300ms trailing), not binary blocking              | claude                        | 10  | 9   | 9   | 9   | 8   | 45     | KEEP                                                         |
| 53  | **The hard gate is on actions, not tokens**                                  | claude                        | 10  | 10  | 10  | 10  | 10  | **50** | **KEEP — the latency argument that actually holds**          |
| 54  | Three lanes: inline deterministic / near-line NLI / async                    | claude, gpt, minimax          | 9   | 7   | 10  | 10  | 8   | 44     | KEEP                                                         |
| 55  | **Speculative gating** — verify tool args *while the tool call is in flight* | claude                        | 9   | 10  | 10  | 10  | 9   | 48     | KEEP                                                         |
| 56  | Provenance indexed at retrieval time → binding is a **lookup, not a search** | claude                        | 8   | 10  | 10  | 10  | 10  | 48     | **KEEP — this is what makes the latency budget real**        |
| 57  | Verification budget follows blast radius                                     | claude                        | 10  | 9   | 10  | 10  | 9   | 48     | KEEP                                                         |
| 58  | Shadow mode as default deployment + 5% dual-emit                             | claude, gpt, minimax          | 9   | 8   | 10  | 10  | 9   | 46     | KEEP                                                         |
| 59  | **Speculative release** — emit immediately, recall/edit post-hoc             | gpt, minimax, mistral, gemini | 9   | 4   | 4   | 10  | 3   | 30     | **KILL**                                                     |
| 60  | Proof cache — precomputed evidence bundles keyed by context hash             | kimi, mistral                 | 9   | 6   | 8   | 10  | 7   | 40     | KEEP                                                         |
| 61  | Bounded recursive proof, max 2 hops, timeout → UNKNOWN                       | kimi                          | 9   | 7   | 8   | 10  | 8   | 42     | KEEP                                                         |
| 62  | UI "Verifying…" progressive-disclosure box                                   | gemini, kimi                  | 9   | 5   | 5   | 9   | 5   | 33     | FOLD → the *rendering* of #52; a demo asset, not a mechanism |
| 63  | Sidecar / OpenAI-compatible reverse proxy                                    | gemini, gpt, minimax, glm     | 10  | 6   | 9   | 10  | 7   | 42     | KEEP → deployment shape                                      |
| 64  | Sentence-boundary buffer to prevent fragmented claims                        | glm                           | 9   | 6   | 8   | 10  | 7   | 40     | FOLD → #51's FP control                                      |




## A6 — Internal multi-agent structure


| #   | Mechanism                                                                  | Source                        | C   | D   | S   | L   | E   | Σ      | Verdict                         |
| --- | -------------------------------------------------------------------------- | ----------------------------- | --- | --- | --- | --- | --- | ------ | ------------------------------- |
| 65  | **Evidence Ledger** — shared typed artifact, nothing passed as free text   | claude, kimi                  | 9   | 9   | 10  | 10  | 10  | 48     | KEEP                            |
| 66  | **Deadline-driven, not consensus-driven**; missed deadline returns UNKNOWN | claude, kimi                  | 9   | 9   | 10  | 10  | 9   | 47     | KEEP                            |
| 67  | Only the Interlock/Arbiter decides; every other role advises               | claude, kimi, gemini, minimax | 10  | 9   | 10  | 10  | 9   | 48     | KEEP                            |
| 68  | Provenance Recorder hooks **context assembly**, not output                 | claude                        | 9   | 10  | 10  | 10  | 10  | **49** | **KEEP**                        |
| 69  | Prosecutor must *prove*; default verdict unsupported                       | claude, kimi                  | 10  | 9   | 9   | 9   | 10  | 47     | KEEP                            |
| 70  | Adjudicator publishes the plane's **own precision / recall / FNR**         | claude                        | 9   | 10  | 10  | 10  | 10  | **49** | **KEEP — the credibility play** |
| 71  | Economist owns dead compute and the ROI number                             | claude                        | 9   | 8   | 9   | 10  | 8   | 44     | KEEP                            |
| 72  | **Red Team probes ControlPlane's own validators**, offline                 | kimi                          | 9   | 9   | 9   | 10  | 8   | 45     | KEEP                            |
| 73  | Fast roles may block; slow roles may only annotate or re-gate              | gpt, minimax                  | 10  | 7   | 9   | 10  | 8   | 44     | KEEP                            |
| 74  | "Interrogator" LLM attacking the generator's reasoning trace               | gemini                        | 7   | 4   | 4   | 4   | 4   | 23     | **KILL**                        |


---



# PART B — THE KILL LIST (and why)

Nine mechanisms are removed outright. Each was proposed by at least one model and each is a trap.


| Killed                                                                       | Proposed by                                 | Why it dies                                                                                                                                                                                                                                                                                                                                          |
| ---------------------------------------------------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Model-emitted citations / hidden** `<claim><source>` **traces** (#11, #12) | gemini, mistral                             | The model grades its own homework. A model that fabricates a fact will fabricate the citation for it with equal fluency. Provenance must be captured **outside** the model at context-assembly time, where it is tamper-proof by construction. Killing this is also what *unlocks* the entitlement check (#28) — self-reported sources carry no ACL. |
| **Speculative release with post-hoc recall** (#59)                           | gpt, minimax, mistral, gemini               | A liability gap by construction: the harm is delivered, then withdrawn. Kimi independently named this as its own single greatest risk. You cannot un-ring the bell. The hold-back buffer (#52) buys the same perceived speed with no gap.                                                                                                            |
| **Universal fail-open on SLA breach** (#48)                                  | mistral, gpt                                | "Prefer false negatives over latency violations" makes the entire plane bypassable by inducing load — an attacker's first move. Fail stance must be a declared property of the blast-radius tier (#46), not a global default.                                                                                                                        |
| **Cosine-similarity threshold as a verdict** (#8)                            | gemini, glm, mistral                        | `0.7` and `0.85` are magic numbers on an embedding distance, not a decision. Domain drift moves them constantly. NLI entailment plus deterministic recomputation supersede it on every axis.                                                                                                                                                         |
| **Rolling z-score cost anomaly** (#21)                                       | gpt, minimax                                | Not robust. A handful of pathological traces drag the mean and mask everything else. Median + MAD (#20) is the same idea done correctly.                                                                                                                                                                                                             |
| **GBDT rework-probability predictor** (#24)                                  | kimi                                        | Requires labelled history per query class, is hostile to cold start, and *predicts* what direct trace inspection (#16) simply *observes*. Complexity with no marginal signal.                                                                                                                                                                        |
| **Demographic parity vs source-dataset base rates** (#35)                    | gpt, minimax                                | The base rate is undefined in most real deployments and contested in the rest. Counterfactual replay (#30) measures a causal, auditable quantity instead: does the decision flip when only the protected attribute changes?                                                                                                                          |
| **"Interrogator" LLM attacking the generator** (#74)                         | gemini                                      | LLM-as-judge wearing a costume, plus it depends on the already-killed self-reported trace. Same model family means correlated blind spots, so the "ensemble" is not independent.                                                                                                                                                                     |
| **Composite 0–100 risk score**                                               | (rejected by all 7 — recorded for the deck) | Unanimous. Cannot be decomposed by policy or acted on by a user. A demo affordance.                                                                                                                                                                                                                                                                  |


---



# PART C — THE FOUR REAL CONTRADICTIONS, RESOLVED

The seven proposals disagreed substantively in exactly four places. Each is resolved in favour of the cleaner overall system, not by keeping both.

### C1 — Where does evidence come from?

- **gemini / mistral:** ask the model to self-report claims and sources.
- **gpt / minimax / glm / kimi:** match the finished output against a vector DB or knowledge graph after the fact.
- **claude:** capture the provenance set at context-assembly time, with ACL and hash.

**Resolved → context-assembly capture.** It is (a) untamperable by the generator, (b) turns binding from a corpus *search* into a set *lookup*, which is where the entire latency budget comes from, and (c) is the only option that carries an ACL, which is what makes the leakage mechanism deterministic instead of probabilistic. This one decision cascades through every other section.

### C2 — Does absence of evidence justify action?

- **claude:** default verdict is UNSUPPORTED; a claim must *earn* SUPPORTED.
- **glm:** never act on "unverified," only on "contradicted" — false positives on semantic blocking destroy trust.

**Resolved → both, at different layers.** The *verdict* is hostile (glm is wrong here: silently treating unverified as fine is exactly how false assurance enters). The *action* is proportionate (glm is right here: blocking read-only text on absence of evidence kills adoption). The R × S matrix holds both without compromise — UNSUPPORTED passes with annotation at R0/R1 and escalates at R3. Neither proposal alone expressed this.

### C3 — Emit-then-recall, or hold-then-emit?

- **gpt / minimax / mistral / gemini:** speculative release, user sees the model not the gate.
- **claude / kimi:** gated pipe, hold buffer on high-risk markers.

**Resolved → hold-then-emit for text, hard-gate on actions, and speculative *verification* (not speculative *release*).** The insight that makes this cheap rather than slow: users perceive speed from *text*, but harm lives in the *commit path*. Text streams on a 150–300ms trailing buffer; tool calls are verified concurrently with their own network round-trip and cost nothing observable.

### C4 — Is cost a report or an actuator?

- **gpt / minimax / mistral:** cost never blocks; alert ops and downgrade routing.
- **claude:** breaker trips on non-convergence.
- **glm:** inject an out-of-band stop sequence and terminate provider billing instantly.

**Resolved → cost never blocks a user's answer, but it kills a runaway loop.** These are different objects. The brief demands "watch, **catch, and act**"; a cost axis that only reports is a dashboard, which the brief explicitly rejects. glm's stop-sequence injection is the only mechanism in all seven proposals where the cost axis saves actual money in real time, and it survives because it targets the agent loop, not the user.

---

---



# PART D — THE FINAL MERGED ARCHITECTURE



## 1. Core Thesis

> **An AI response is not text to be scored — it is a set of claims requesting permission to act.** ControlPlane binds every claim to the evidence the model was actually given, and spends verification budget in proportion to what the response is about to do. Performance, cost and responsibility are not three detectors bolted together; they are **three reads of one graph.**

---



## 2. Detection Layer



### The primitive: one graph, built during generation

Everything downstream reads a single structure, assembled while the response is being produced rather than reconstructed afterwards:

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

*One structure, three axes, three actuators.* This is why it is a control plane and not three classifiers in a trench coat — and it is the single most explainable idea in the deck.

### Performance — "confidently wrong"

**Signal:** assertion strength × groundedness deficit. *Not confidence.* The brief names the failure as **confidently** wrong; confidence is therefore the broken instrument and cannot also be the detector.

**Computation, in strict cost order:**

1. **Claim extraction at sentence boundaries** by a small streaming model (1–3B), emitting only *check-worthy typed* propositions — numbers, entities, dates, quantities, causal and policy assertions. Each is tagged **categorical** or **hedged**. Sentence-boundary buffering prevents claims fragmenting across token boundaries.
2. **Route by claim type, not through one detector:**
  - **Numeric / structural / temporal → deterministic recomputation** against the span set. Does the figure appear in a tool result; does the arithmetic reconcile; is the date inside the source's range. Sub-millisecond, near-zero false positives, and it covers the errors that actually cost money.
  - **Textual / factual → binding.** Hybrid retrieval over the *provenance set only* (never the open web) → NLI cross-encoder (~300M, 5–15ms batched) → `SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN`. **Default verdict is UNSUPPORTED. A claim must earn SUPPORTED.**
  - **Derived / multi-hop / aggregative → never entailed.** Recompute from spans, or return UNKNOWN. (See §7 — this is the boundary against false assurance.)
3. **Ungrounded routes** (no retrieval context — a purely parametric answer) have no binding to perform. The async lane runs a **semantic-entropy probe**: k=5 resamples, clustered by meaning, dispersion measured. High dispersion + categorical assertion = confidently wrong. Off the critical path by construction; it feeds route-level calibration and the R2/R3 gate, never the token stream.
4. **Response verdict = worst claim, weighted by that claim's role in the pending action.** Never an average. One contradicted refund amount outranks nine correct sentences.

**FP control:** check-worthiness filtering removes the largest false-positive class before any model runs; the cheap tier flags and the expensive tier confirms; `UNKNOWN` is a first-class verdict that *routes* rather than blocks; thresholds are calibrated **per route**, never globally.

### Cost — waste and rework

**Signal:** evidence yield per unit of spend, and non-convergence.

1. **Dead compute, computed exactly.** Walk the graph backward: every SUPPORTED claim in the accepted answer points to a span, which points to the step that produced it. **Any step grounding zero accepted claims is dead compute** — no model required, no estimation. Headline metric: *the fraction of spend that produced no evidence used in the answer.* No competitor will have this number, because no competitor has the graph.
2. **Rework, deterministically.** Near-duplicate tool calls in-trace (exact arg hash first, then arg-embedding cosine), retry loops, re-retrieval of spans already in context, and semantic-hash hits against recent outputs — a >95%-similar answer already produced at a fraction of the cost.
3. **Non-convergence breaker, live.** Track evidence-yield-per-step, token-to-state velocity, and plan-state advancement together. When spend climbs while evidence yield decays **and** plan state fails to transition, the agent is looping — the three-signal conjunction is what separates a genuine loop from legitimate repetition. ControlPlane then **injects an out-of-band stop sequence into the provider API and terminates the call.** Billing stops mid-generation. *Cost never blocks a user's answer; it kills a runaway loop.*
4. **Route baselines on robust statistics.** Cost-per-successfully-gated-response tracked per route as a streaming **median + 3.5×MAD** — not mean and σ, which a handful of pathological traces would drag until nothing else fires. Cold start (first N requests per route) excluded; baselines held per route and per tenant so a traffic-mix shift does not read as a regression.



### Responsibility — three problems, three mechanisms

Leakage, bias and safety have different mathematics, different error costs and different owners. Collapsing them into one classifier is the generic move.

1. **Leakage = set membership + entitlement, not classification.** Two deterministic rules over the graph:
  - **(a)** A PII/secret-shaped entity in the output that binds to **no span** is model-memory leak or fabrication → **Block.**
  - **(b)** An entity that binds to a span whose **source ACL excludes the calling principal** → *retrieval-side authorization failure* → **Block.**
   Rule (b) catches the most common real enterprise incident — an over-permissioned RAG index faithfully leaking HR data to the wrong employee — and **no LLM-judge wrapper catches it, because none of them carry identity into the verification layer.** Implementation is an Aho-Corasick pass over the entity set plus an ACL lookup: microseconds, near-zero FP.
2. **Bias = counterfactual invariance, route-level, async.** For decision-shaped outputs (approve / deny / rank / score), the shadow lane replays requests with protected attributes perturbed — name, gender marker, pincode, institution — and measures **decision flip rate with a confidence interval over a rolling window.** Flag when the CI excludes zero. Per-response bias verdicts are statistically illiterate; bias is a distributional property or it is nothing.
3. **Safety = typed interlocks on the action, not on the prose.** Declarative versioned rules over `tool × argument schema × irreversibility`: no `send_email` to an external domain carrying a span from a `confidential` source; no DDL in `execute_sql`; no financial write above threshold without a SUPPORTED numeric binding. Any proposed call outside the allow-listed action grammar fails at parse time. Text toxicity classifiers remain a cheap Lane-1 tier — they detect banned surface forms, not wrongness — never the product.

---



## 3. Decision Policy Engine

Two inputs govern every decision: **blast radius R** (what this response can break) and **verdict severity S** (what the evidence says).

**R = irreversibility × audience × data class × autonomy level**


| Tier   | Meaning                                                                      |
| ------ | ---------------------------------------------------------------------------- |
| **R0** | internal draft, a human reads it first                                       |
| **R1** | user-visible, read-only                                                      |
| **R2** | reversible write / external send                                             |
| **R3** | irreversible or regulated — payment, deletion, publication, regulated advice |



|        | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown         |
| ------ | ------------------------------------ | ------------------------- | -------------------- | --------------- |
| **R3** | **Block**                            | Escalate                  | Escalate             | Escalate        |
| **R2** | **Block**                            | Edit                      | Edit                 | Escalate        |
| **R1** | Edit                                 | Edit                      | Pass + annotate      | Pass + annotate |
| **R0** | Pass + annotate                      | Pass + annotate           | Pass                 | Pass            |


This matrix is where C2 resolves: **the verdict is hostile, the action is proportionate.** A claim must earn SUPPORTED, but merely failing to earn it only blocks where the blast radius justifies blocking.

### Four actuators, not three

- **Edit is surgical, never generative.** Either strip the unsupported claim, or re-invoke the generator **once** with a constrained instruction naming the exact failing span. Edited output re-enters the gate; a second failure falls through to Escalate. Free-form LLM rewriting would produce a new *unverified* artifact — that is moving the problem, not solving it.
- **Escalate ships an evidence packet, not an alert:** the claim, the candidate spans, the verdict, the diff. Design target is a human resolving it in **under 20 seconds**. Escalation without a packet is what everyone else builds.
- **Autonomy downgrade** — demote a route from *act* to *propose* instead of blocking it outright.
- **Circuit breaker** — per-route error budget, SRE-style. When gate-fail rate over a sliding window exceeds budget, the route drops an autonomy tier until it recovers. That is catch-and-act at the *system* level, not just per response.



### How the policy is encoded and governed

Rules are 4-tuples `(signal, threshold, action, latency_budget)` in a **versioned DAG**, not nested conditionals — so multiple axes fire independently and every violation path is separately testable. The engine is a **pure rule engine: zero LLM reasoning at decision time.**

**Fail stance is not the same object as the action.** The matrix above says what to do when the evidence *arrives* and is bad. Fail stance says what to do when the evidence *does not arrive in time*. Conflating the two is the most common way a gating system silently fails, because a timeout then inherits whichever behaviour happens to be listed for that tier.

Every rule declares a **fail stance, and the stance belongs to the tier, not to a global default**: R0/R1 fail **open with annotation**; R2/R3 fail **closed or escalate**. Undeclared timeout behaviour is the most common silent failure of gating systems, and a universal fail-open makes the plane bypassable by anyone who can induce load.

The plane earns its own authority. Policies are versioned artifacts; no threshold change ships without a **shadow replay over the last N traces** showing the FP/FN delta; every change canaries by route and **auto-rolls back if the human-override rate exceeds 3× the prior baseline.** Every decision is written to an **append-only, hash-chained ledger** carrying the exact evidence fragment that caused it.

**User surface: three states — Verified / Uncertain / Blocked** — each with one claim-level line. No raw scores; scores produce alert fatigue and cannot be acted on.

---



## 4. Latency & Non-Blocking Design

**The core move: the expensive part is precomputed by construction.** Provenance is indexed at context-assembly time, so binding is a **lookup against a small in-memory set, not a search over a corpus.** That single choice removes most of the apparent cost of verification, and it is the reason the numbers below are defensible.

1. **Verify the stream, not the finished response.** Extraction and binding run at sentence boundaries *during* generation. When the last token lands, only the final sentence remains to verify. Marginal latency ≈ one sentence, not one response.
2. **Hold-back buffer, not binary blocking.** Stream to the user on a ~150–300ms trailing delay. Failures inside the buffer never reach the user. Chosen deliberately over emit-then-recall: post-hoc retraction has a liability gap by construction.
3. **The hard gate is on actions, not tokens.** Read-only text streams optimistically; anything crossing a side-effect boundary is hard-gated. Users perceive speed from *text*; harm lives in the *commit path*. Gating a tool call costs 20–40ms against a 200ms–2s tool round-trip — invisible.
4. **Three lanes.**
  - **Lane 1 — inline, hard 30–60ms p95, deterministic only.** Span membership, ACL, typed interlocks, arithmetic recomputation, Aho-Corasick PII. No LLM, no network hop, sidecar-colocated.
  - **Lane 2 — near-line, 100–400ms.** NLI binding, for flagged claims and high-R traffic only.
  - **Lane 3 — async.** Semantic-entropy probes, counterfactual bias replay, adversarial verification, calibration, root-cause clustering, policy shadow replay.
5. **Speculative gating.** Verify tool-call arguments *while the tool call is in flight*; verification completes inside the tool's own latency and is effectively free. (Speculative **verification**, not speculative **release** — that distinction is the liability gap.)
6. **Proof cache.** Repeat context/prompt pairs carry precomputed evidence bundles keyed by context hash with a short TTL. Cache hit → suite skipped, sub-millisecond.
7. **Budget follows blast radius.** R0/R1 is 80–90% of volume and gets Lane 1 only. Expensive verification is spent on the 5–10% that can actually cause harm. Mean added latency stays in tens of milliseconds; the tail lands where it is justified.
8. **Bounded proof depth.** Any claim needing deeper evidence gathering gets **max 2 hops**. Unresolved at timeout → UNKNOWN → routed by the matrix. Nothing stalls.
9. **Shadow is the default deployment mode.** Every route runs gated-vs-ungated dual-emit before enforcement is switched on, producing the counterfactual — *"would have blocked N, of which M were true positives."* It is also the only realistic enterprise adoption path.
10. **Deployment shape:** an **OpenAI-compatible reverse proxy** plus a thin context-assembly SDK hook. No application rewrite, no model access, no weights, no logits, no fine-tuning. Works with closed APIs.

**Targets to defend on the slide: ≤40ms p50 and ≤200ms p95 added on R0/R1 text; action gating amortized inside tool latency.**

---



## 5. Internal Multi-Agent Structure

**Yes — but it is a deadline-driven pipeline over a typed artifact, and most of the workers are not LLMs.** Multi-agent here means specialization and isolation, not conversation. No debate, no voting, no chain-of-thought passed between roles.

**Shared artifact — the Evidence Ledger** (append-only, hash-chained, one per request):

```
{ principal, action_intent, R_tier, spans[], claims[], bindings[],
  step_yield[], verdicts[], policy_version, verifier_versions, latency_spent }
```

Every role reads and appends structured entries. **Nothing is passed as free text.**


| Role                    | Lane         | Owns                                                                                                                                                                                                                                  | LLM?         |
| ----------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| **Provenance Recorder** | inline, ~0ms | Hooks context assembly; captures every span with source, ACL, hash, offsets. Ground truth of *what the model was allowed to know*. Hooking context assembly rather than only the output is what makes this a plane and not a wrapper. | No           |
| **Claim Extractor**     | streaming    | Typed check-worthy claims + assertion strength                                                                                                                                                                                        | Small (1–3B) |
| **Prosecutor**          | 1 + 2        | Attempts to *prove* each claim; default verdict unsupported. Hostile validation made structural.                                                                                                                                      | NLI ~300M    |
| **Entitlement Auditor** | 1            | Output entities vs caller identity and source ACLs. Owns leakage.                                                                                                                                                                     | No           |
| **Economist**           | 1 + 3        | Step yield, dead compute, non-convergence breaker, route baselines. Owns the loop-kill and the ROI number.                                                                                                                            | No           |
| **Action Interlock**    | 1            | Computes R, applies the matrix, emits the actuator. Small, auditable, no ML. **Everything else advises; only this decides.**                                                                                                          | No           |
| **Adjudicator**         | 3            | Stratified sampling to expensive ground truth; per-route precision / recall / FNR. Owns the plane's own error bars.                                                                                                                   | Mixed        |
| **Red Team**            | offline      | Adversarially probes **ControlPlane's own validators** to find blind spots; findings update validator schemas. Never touches the live path.                                                                                           | Yes          |


**Coordination under time pressure:** every role has a hard deadline and a declared degraded output. Missing the deadline returns `UNKNOWN`, which the Interlock resolves via that tier's fail stance. No role can block another. **The Interlock decides on whatever is in the ledger when the clock expires — deadline-driven, not consensus-driven.** Fast deterministic roles may block; slow probabilistic roles may only annotate or trigger a re-gate. **A slow check never overturns a fast decision.**

---



## 6. Explicitly Rejected Approaches

1. **LLM-as-judge on the critical path.** Slow (300ms–2s), uncalibrated, and — when drawn from the same model family as the generator — sharing its blind spots, so the "ensemble" is not independent. Judges live in Lane 3, sampled, and are themselves audited by the Adjudicator.
2. **Model-emitted citations or reasoning traces as the evidence source.** The model grading its own homework: a model that fabricates a fact fabricates its citation with equal fluency. Provenance is captured *outside* the model, at context assembly, where it is tamper-proof — and only then does it carry the ACL that makes leakage detection deterministic.
3. **Speculative release with post-hoc recall.** A liability gap by construction — the harm is delivered, then withdrawn. Replaced by the hold-back buffer for text and hard gating on actions, which buys the same perceived speed with no gap.
4. **Confidence / logprob thresholding as the hallucination signal.** The named failure mode is *confidently* wrong. Confidence is the broken instrument; it cannot also be the detector. Assertion strength is used only as a severity modifier on top of a groundedness verdict.
5. **A single composite 0–100 risk score.** Three axes with different actuators, owners and error costs. One number cannot be decomposed by the policy or acted on by the user. It is a demo affordance.
6. **Static keyword/toxicity guardrails as the product, and dashboards as the deliverable.** Both retained in their proper place — a cheap Lane-1 tier, and a projection of the ledger — but neither is the system. If the primary artifact is a chart, oversight is still after the fact.
7. **Universal fail-open on SLA breach.** Makes the plane bypassable under induced load. Fail stance is declared per blast-radius tier instead.
8. **Debate / multi-agent voting for real-time gating.** Non-deterministic latency, no calibration story. Adversarial work runs offline in the Red Team role.
9. **Uniform validation depth across all traffic.** Spending the same proof budget on a weather lookup and a payment authorization is how a gating layer becomes a latency tax. Depth is a function of blast radius or the system is not a control plane.
10. **Any design assuming access to weights, logits, or fine-tuning.** The plane must sit on top of any model, including closed APIs. Everything works from context, output and trace — nothing from inside the model.

---



## 7. Strongest Remaining Technical Risk + Mitigation



### Risk: false assurance on derived claims

Multi-hop, aggregated and synthesized claims are exactly where entailment is weakest and exactly where the value is highest. If the Prosecutor marks a subtly-wrong synthesized claim SUPPORTED because a shallow span looks similar, ControlPlane delivers **false assurance — strictly worse than no control plane, because humans stop checking.** The risk compounds if the verifier shares the generator's model family and therefore its blind spots.

### Mitigation — three lines that fit on a slide

- **Route derived claims away from NLI entirely.** Anything arithmetic or aggregative is *recomputed* from spans, not entailed. Anything neither recomputable nor directly entailed returns UNKNOWN. **UNKNOWN never collapses into SUPPORTED** — that one rule is the boundary between a control plane and false assurance.
- **Decorrelate by construction.** Verifiers come from a different model family than the generator, and the deterministic checks — span membership, entitlement, arithmetic — carry the majority of enforcement weight *precisely because* they cannot share the generator's failure modes. The Red Team role exists to attack ControlPlane's validators, not the generator's output.
- **Publish the plane's own error bars.** Stratified shadow audit — 100% of blocks and escalations plus a random slice of passes — sampled to expensive ground truth. The Adjudicator reports per-route precision, recall and FNR with confidence intervals.

The claim is never *"we catch hallucinations."* It is:

> **"On this route we catch 94% of ungrounded claims at 40ms p50 — and here is the 6% we don't."**

Every team will claim detection. **Publishing your own false-negative rate is the move none of them will make.**

---

---



# PART E — DELIVERABLE MAPPING (3 slides + 3 minutes)



## The one demo that carries all three axes

A refund agent, one trace, three catches — same graph read three ways:


| Axis               | What happens                                                                                                                                               | What ControlPlane does                                                                                                         |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Performance**    | Agent says *"your refund is ₹4,820."* No span contains that figure; arithmetic does not reconcile against the order rows.                                  | `CONTRADICTED` + pending R2 write → **Block**, with the correct figure and its source span attached.                           |
| **Responsibility** | Agent surfaces a note from the internal fraud-review file. The span **is** in provenance — but its ACL is `risk-team-only` and the caller is the customer. | Entitlement violation → **Block**. This is a *retrieval-side authorization failure*, invisible to every output-only guardrail. |
| **Cost**           | Agent re-queried the order service 6 times with identical arguments; those steps grounded zero claims in the final answer.                                 | 71% dead compute + plan state not advancing → breaker trips, **stop sequence injected, billing ends mid-generation.**          |


One trace. Three axes. One graph. That is the whole pitch, and it fits in 40 seconds.

## Slide plan

**Slide 1 — The reframe.**
Headline: *"An AI response is a set of claims requesting permission to act."*
Centre: the STEP → SPAN → CLAIM → ACTION graph, with three coloured arrows — Performance reads forward, Cost reads backward, Responsibility reads the labels. One structure, three axes.
Footer: the three-catch refund example in one line each.

**Slide 2 — The decision.**
The R × S matrix, full size — it is the most credible object in the deck.
Right rail: the four actuators (surgical Edit · evidence-packet Escalate · autonomy downgrade · circuit breaker).
Left rail: the three lanes with their latency budgets (30–60ms deterministic / 100–400ms NLI / async), and the hold-back buffer.
Headline: *"The verdict is hostile. The action is proportionate."*

**Slide 3 — Why we should be believed.**
Left half: the rejection list — no LLM judge on the path, no model-reported citations, no emit-then-recall, no composite score. *This is what separates us from every other team's slide.*
Right half: the self-audit — shadow by default, hash-chained ledger, red team against our own validators, published FNR.
Close on: *"On this route we catch 94% of ungrounded claims at 40ms p50 — and here is the 6% we don't."*

## Video plan (3:00)


| Time          | Beat                                                                                                                                                                                                                          |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **0:00–0:30** | The failure. A refund agent states a wrong amount with total confidence and issues the refund. Discovered a week later, in a reconciliation report. *"The problem isn't that AI is wrong. It's that we find out afterwards."* |
| **0:30–1:15** | The reframe + the graph. Build STEP → SPAN → CLAIM → ACTION on screen; show the three reads.                                                                                                                                  |
| **1:15–2:15** | The live path. Claim binds ✓ / claim fails to bind ✗. The entitlement catch (HR record, wrong employee). The loop kill (billing counter stops mid-generation).                                                                |
| **2:15–2:45** | The matrix. Why we don't block everything — over-blocking gets the layer disabled in a quarter.                                                                                                                               |
| **2:45–3:00** | The FNR line. End there. Say nothing after it.                                                                                                                                                                                |


---



## Freeze notes

- **The keystone is the context-assembly hook.** If exactly one thing gets built for Round 2, build the Provenance Recorder. Every other mechanism degrades to a generic guardrail without it.
- **The most differentiated single mechanism is the entitlement check** (scored 50/50). It is deterministic, sub-millisecond, catches a real and expensive enterprise incident, and is structurally impossible for any output-only competitor to replicate.
- **The most defensible number is dead compute.** It is computed exactly, needs no model, and is the number a buyer signs a cheque against.
- **The line that wins the room is the published FNR.** Do not cut it for time.

