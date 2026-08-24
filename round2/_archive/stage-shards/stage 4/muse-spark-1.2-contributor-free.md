# ControlPlane.ai — Round 2 Stage 4: Business Proposal Spine

> Accenture Innovation Challenge 2026 · Round 2 · Stage 4 — Detailed Business Proposal (Spine)  
> Sources of truth (absolute, frozen): `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` · `R2S2.md` · `R2S3.md` · Official Round 2 ControlPlane.ai brief (`docs/ps.md`)  
> Status: **FROZEN up to Stage 3 — This document extends; it does not reopen**  
> Stage 1 prototype scope · Stage 2 enterprise envelope · Stage 3 build/demo spec are non-negotiable. Stage 4 adds only the buyer, value, and rollout logic around the **same** admission primitive.

---

## 1. Problem Framing — not “AI risk,” a change in category of cost

**Before:** a wrong AI output was a bad paragraph. Someone read it, noticed, corrected it. Cost = rework.

**Now:** the same output is an executed transaction. It refunds, files, sends, books, deletes, publishes. `Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.` Every filter passed it. Confidence 0.94. **Clause 7.2 does not exist.** Failure = absence of evidence, not conflicting evidence. Money moved Tuesday, found Friday. **The company wrongly pays out ₹1,84,000** — the customer did not lose money.

This is the shift the enterprise has already made — from AI that answers to AI that acts — while oversight is still built for the answering era: score the text, chart the failure, review the log next week.

**Why the installed tooling cannot cover this shift:**

| Installed approach | What it does | Why it fails on the frozen failure modes |
|---|---|---|
| **LLM-as-judge / NeMo Guardrails wrappers** | Second model opines “does this look right?” without the source documents, without knowing who asked | Same family blind spots as the generator; unfalsifiable question; cannot state own FNR; too slow to stand in front of an R3 commit. `which span proves it?` has an answer; `does this look right?` does not. `QA.md:A1` |
| **Static guardrails / LlamaGuard / Lakera** | Regex / deny-list on banned surface forms | Lexically clean failures: fabricated invoice number, paraphrased policy claim, salary leaked from over-permissioned index all pass. Identity-blind — same string is fine for one caller, a breach for another. Cannot do `CALLER→CLAIM→SPAN→SOURCE ACL` `ARCHITECTURE.md:3:1` |
| **RAG groundedness checkers** | Average embedding similarity over retrieved chunks | See retrieval only — not tool rows / DB records / system context where agents get facts. Average, so one wrong figure drowns in nine correct sentences — `worst claim weighted by role in pending action, never an average` `R2S1.md:42`. Action-blind — 0.82 means same thing on draft and wire transfer. No caller identity → no entitlement. `QA.md:A3` |
| **Post-hoc observability (LangSmith / Helicone / Arize)** | Beautiful traces, weekly dashboards | Tell you what went wrong after a user acted on it — the thing the brief asks to eliminate. Measure spend, not waste: can tell you trace cost ₹8, cannot tell you ₹5 grounded nothing. Only the forward-and-backward graph walk can. `NARRATIVE.md:3` |
| **Confidence / logprob thresholding** | Block when confidence < X | Named failure is *confidently* wrong. You cannot detect a calibration failure with the calibration. `ARCHITECTURE.md:3:1` |
| **Composite 0–100 risk / trust / safety score** | Collapse hallucination + privacy + bias into one number | **You cannot block, edit or escalate on 87.** Three failure modes, three owners, three remedies. `ARCHITECTURE.md:8` |

All six inspect the *output*. None records the *entrance* — the evidence assembled before the model ran. That record is thrown away the moment generation starts. Whoever controls that record controls the proof. That is the problem to solve.

> Everyone watches the exit. Nobody records the entrance. `NARRATIVE.md:6:1` — permitted exception; the indictment.

---

## 2. Solution Design Summary — the same frozen primitive, no new mechanism

**Category noun:** `admission-control layer`. Not guardrail, not observability, not verification proxy. `NARRATIVE.md:2` Reference class = firewall, transaction validator, CPU privilege mode.

**One primitive, three reads:**

```
STEP ──produces──▶ SPAN ──binds──▶ CLAIM ──authorizes──▶ ACTION
(tool call,       (retrieved chunk, (typed atomic      (pending side
 retrieval,        tool row, DB      proposition        effect: tool +
 model turn)       record — with     from the output     args +
                  source_id, ACL,   stream)            irreversibility)
                  hash, offsets)
```

*Performance reads it forward* — does each claim bind to a span? *Cost reads it backward* — did each step ground zero accepted claims (dead compute, exact)? *Responsibility reads its labels* — is the caller entitled to every span a claim binds to, and does the action fall inside its typed interlock? **One structure, three axes, three actuators.** `ARCHITECTURE.md:2`

**Invariants preserved from freeze (Stage 4 does not tune them):**

| Invariant | Frozen rule |
|---|---|
| **Provenance outside the model** | Context-assembly SDK hook writes `source_id · ACL · content_hash · offsets` + principal on the request. Model has no write path. Keystone — if one thing is built, build this. `ARCHITECTURE.md:2` |
| **Default = UNSUPPORTED** | Every check-worthy claim starts UNSUPPORTED. `SUPPORTED` only via binding / deterministic recomputation against captured set. `UNKNOWN` never → `SUPPORTED`. Not low confidence. Unproven. `R2S1.md:3:3` |
| **Entitlement = set-membership test** | `principal ∈ span.ACL` / `span.acl ⊆ principal.clearance` — Lane 1, deterministic, sub-millisecond, zero LLM, cannot be disabled. Same claim, different principal → different outcome. `R2S1.md:2:B` |
| **One graph per request/session** | `STEP→SPAN→CLAIM→ACTION` append-only, hash-chained Evidence Ledger. All verifiers, all lanes, all routes read the same object. Multi-turn = more STEPs on same session ledger. Prior assistant text is never evidence by reappearing. `R2S2.md:2` |
| **Claim-type routing, not one detector** | Numeric/date/ID → deterministic recomputation. Textual → bind against provenance set only (entailment, not string match; paraphrase binds). Derived/multi-hop/aggregative → recompute or `UNKNOWN`. No open web. No model-emitted citation is evidence. `R2S1.md:3:4` |
| **Blast-radius pricing** | `R = irreversibility × audience × data class × autonomy level` → R0 internal draft / R1 user-visible read-only / R2 reversible write or external send / R3 irreversible or regulated (payment, deletion, publication, regulated advice). Same verdict annotates a draft and holds a payment. `ARCHITECTURE.md:4` |
| **Exact frozen R×S matrix, per pending action** | Transcribed, never redrawn. 16 cells, four actuators `Block · Edit · Escalate · Pass / Pass+annotate` (autonomy downgrade / circuit breaker are spoken controls). Matrix is pure `f(R, S) → actuator` with no route parameter. `worst claim weighted by role in pending action, never an average.` Two-pending-actions centrepiece: `R1×entitlement→Edit` (text) + `R3×unsupported-categorical→Escalate — held with evidence packet` (refund), same response, same graph. Never say “blocked” about the refund. `R2S1.md:3:6` |
| **Hard gate on actions, not tokens** | Text holds behind ~150–300 ms buffer; action commits gated on tool round-trip (20–40 ms vs 200 ms–2 s). Speculative verification permitted, speculative release forbidden. Fail stance per tier: R0/R1 fail open with annotation; R2/R3 fail closed or escalate. Timeout → `UNKNOWN` → matrix + tier fail stance. `ARCHITECTURE.md:5` |
| **Pure rule engine at decision time** | Action Interlock sole decider; policy as versioned DAG of `4-tuple (signal, threshold, action, latency_budget)`, declarative code not a prompt. Zero LLM reasoning at decision time. `R2S2.md:3` |
| **Published FNR as empty typed format** | Per-route schema `route_id · policy_version · window · strata · sampled_count_per_stratum · false_negative_count · ground_truth_positive_count · FNR_estimate · CI_lower/upper · ground_truth_method · measurement_status` — null / `insufficient_sample` until earned. Emptiness is the credibility play. `R2S2.md:5` Never fabricate production numbers. |

**What varies per route (configuration, not fork):** `RoutePolicy { route_id · tenant · use_case · provenance_scope · action_grammar (allow-list) · action_to_R_mapping (subject to locked R3: payment/deletion/publication/regulated_advice) · verification_profile (lane enablement, proof depth, timeout) · fail_stance_by_R (must match tier floors) · enforcement_mode shadow|canary|enforce · error_budget · escalation_target · sampling_policy · geography/regulatory_overlay (additive only) · latency_budget ≤40 p50/≤200 p95 for R0/R1}` `R2S2.md:2` Low-consequence traffic gets less verification budget and a proportionate actuator — not weaker truth semantics.

**Bias posture (brief requirement, frozen stance):** Bias = `async route-level counterfactual flip-rate + CI over rolling window; flag when CI excludes zero` — never a per-response claim verdict, never a matrix cell, never a Stage 1 live route. `ARCHITECTURE.md:3:2` Do not drop bias — stated in measurement terms, never moral ones. `NARRATIVE.md:8`

---

## 3. Target Users & Buyers

| Role | Who | Pain | What they sign / operate |
|---|---|---|---|
| **Day-to-day user (actor)** | Support agent, knowledge worker, adjuster/analyst whose answer may auto-act | Lives inside the liability gap: writes an answer, tool fires, money moves. Needs proof without workflow drag. | **Experiences** `Verified / Uncertain / Blocked` per claim + `Held/Escalate` on action. Never a raw score. `R2S3.md:6` |
| **Economic buyer (owns P&L and liability)** | Head of Operations / Head of Customer Service (refund route), CHRO / Head of HR Systems (knowledge route), Risk / Compliance officer (decision route) | Owns wrong-payout budget, leakage liability, audit exposure. Current controls either over-block (team disables) or under-block (incident). | **Signs** per-route error budget, enforcement earn-out, policy DAG version. Approves shadow→canary→enforce promotion after counterfactual `would have held N, M true positives`. `R2S2.md:3` |
| **Technical buyer (owns the pipe)** | Platform / AI Infra lead, Identity & Data lead (owns retrieval stack, IAM, source ACLs) | Owns the integration moat honestly: thin SDK hook where context is already assembled + OpenAI-compatible reverse proxy. Wants deterministic latency and auditability, not a second black box. | **Operates** context-assembly hook, reverse proxy, action adapters, Evidence Ledger; validates `source_id·ACL·hash·offsets` ingestion. Validates `≤40 p50 / ≤200 p95` on R0/R1. `ARCHITECTURE.md:5:10` |
| **Operator / Governor** | SRE / Risk Ops, Auditor | Needs replayable evidence and failure asymmetry that does not make the plane bypassable under load. | **Operates** versioned DAG, shadow replay over last N traces, auto-rollback if override rate >3× baseline, hash-chained ledger reconstruction: `principal·evidence fragment·claim verdict·matrix cell·actuator·policy_version·verifier_versions·latency·lane·route_id`. `R2S2.md:3` |

**Why the split matters:** The actor never enforces — the Interlock does. The buyer never trusts a score — the plane publishes its own miss rate per route and the actor drills `Action → matrix cell → claim verdict → bound/missing span → source_id/hash/ACL → principal entitlement → policy/verifier version → lane/latency → later adjudication`. `R2S2.md:5`

---

## 4. Business Case & Impact Logic — defensible, not decorative

No invented ROI percentages. No `eliminate hallucination`. No `one accuracy number`. No `zero latency`. `NARRATIVE.md:5`

#### Logic 1 — Avoided wrong actions (hard-gate value)

*Mechanism:* `refund.execute` (R3) cannot commit while `R3×unsupported-categorical → Escalate — held with evidence packet`. The demo state is `HELD—ESCALATE, executed:false` made visible before ledger expansion. `R2S3.md:5`

*Impact logic:* Each true-positive hold prevents a class of cost that observability cannot: wrong payout, deletion, publication, regulated advice delivered, then retracted. Liability gap of `emit-then-recall` is structural — hold-back eliminates it. Value = `held true-positive actions × average direct cost of that action class` — measured on *your* adjudicated sample, not our slide. `QA.md:D1` Shadow `gated-vs-ungated dual-emit` produces the counterfactual before enforcement, so the buyer sees evidence, not a forecast.

*Why not overclaim:* We report `FNR(route, policy_version, window) = FN/(TP+FN)` with Wilson/bootstrap CI only when stratified shadow audit (100% of Block/Escalate/Edit + random slice of Pass/Pass+annotate, ground truth = human/exspensive multi-verifier, never LLM-as-judge `R2S2.md:5`) has enough sample. Otherwise `measurement_status = null|insufficient_sample|stale`. The claim shape is always *“on this route we catch <measured>% of ungrounded claims at 40 ms p50 — and here is the <measured>% we don’t”* `ARCHITECTURE.md:7`.

#### Logic 2 — Dead compute: waste named exactly, not estimated

*Mechanism:* Walk graph backward: every SUPPORTED claim in accepted answer → span → step that produced it. **Any step grounding zero accepted claims is dead compute — no model, no estimation.** `ARCHITECTURE.md:3:2` + `R2S2.md:5`

*Impact logic:* Buyer sees `₹8 trace, ₹5 grounded nothing` `NARRATIVE.md:3` — exact, per route, per request. Retrieval re-planning, duplicate tool calls, and non-convergence termination (`evidence-yield-per-step + token-to-state velocity + plan-state advancement → out-of-band stop sequence` `ARCHITECTURE.md:3:2`) save spend without guessing. The number competitors cannot produce is the number the buyer signs against. `ARCHITECTURE.md:12`

*No net-savings slide:* We do not put a percentage saved on a slide — we expose exact waste and let the enterprise price its own traffic. `QA.md:D2`

#### Logic 3 — Alert fatigue avoided by construction (why this layer does not get switched off in a quarter)

*Mechanism:* Matrix prices proof by consequence. R0/R1 draft/read-only: `Unsupported+hedged / Unknown → Pass+annotate`. Lane 1 deterministic only (Aho-Corasick PII/secret shapes, ACL, arithmetic, typed interlocks, 30–60 ms p95) carries 80–90% of volume; Lane 2 NLI binding (5–15 ms batched) only where blast radius justifies it. `ARCHITECTURE.md:3,5`

*Impact logic:* `C5`-style hedged claims do not interrupt a draft; same verdict on a payment holds. Team keeps the tool because it rarely blocks their text. Enforcement is earned per route through shadow evidence — nobody trusts before counterfactual exists. `QA.md:C5`

#### Logic 4 — Auditability that survives a serious question

*Mechanism:* Append-only hash-chained ledger + versioned policy DAG + per-route FNR/FP/override/actuator distribution/latency/entitlement violation metrics `R2S2.md:5`.

*Impact logic:* Regulator / auditor asks “why did this refund hold?” Answer is a pointer, not a paragraph: `policy_version + matrix cell + claim verdict + source_id/hash/ACL + principal entitlement`. `R2S1.md:7` success condition: judge can point from action → claim → externally captured span → principal entitlement and mark every R2S1 §5 criterion yes/no in ≤8 minutes.

#### Directional scale (honest)

Reference parameter = tens of thousands interactions/week across monthly routes, well-governed + loosely governed sources `docs/ps.md:38`. Prototype does not claim that throughput — it proves the control plane works (single-node curated traces). Enterprise proves it can be operated (`R2S2.md:6`).

---

## 5. Phased Roadmap — each phase earns enforcement, never switches it on

| Phase | Duration | What ships | What is demonstrated live | Enforcement state | Earned gate (phase cannot exit until green) |
|---|---|---|---|---|---|
| **0 — Prototype (Stage 3)** | Now | `R2S3.md:4–6` 18 components: Provenance Recorder + Evidence Ledger + Claim Extractor (rule/fixture) + Numeric Recomputer + Binder (pre-annotated entailment, optional local NLI polish) + Entitlement Auditor (set-membership, zero LLM) + Interlock (pure rule engine, frozen 16 cells) + Surgical Editor + Packet Builder + Mock Action Executor (commit boundary) + Hold-back 150–300 ms + Policy Loader (locked R3) + Eval harness (25 criteria) | `Primary: refund dual-action` single response → `R1×entitlement→Edit` + `R3×unsupported-categorical→Escalate (held)` with packet + `Secondary: principal-flip` `analyst_01→hr_partner_01` flips authorization · Ledger ≥60% UI · Governing test `if you remove the graph the demo fails` | **Simulated** — mock refund `executed:false` while held; text hold-back | `FIRST END-TO-END SUCCESS GATE: CLI/fixture refund dual-action passes 1–7,9–11,14–15,19,21 before any UI` `R2S3.md:8` |
| **1 — Shadow on one real route** | Weeks 2–8 | Production `SDK hook + reverse proxy` deployed on **one** route (refund R1/R3 or knowledge R0/R1). One policy DAG version applied. Real `source_id·ACL·hash·offsets` ingestion verified. Append-only ledger on. | Same traces on real spans, gated-vs-ungated dual-emit. Dashboard shows per-route FNR *schema* still null/insufficient_sample — honesty preserved. | **Shadow (observe-only)** — would-have-held counterfactual `would have held N, of which M true positives` recorded, nothing blocked downstream | Shadow window (≥N traces, e.g. 1k+) + latency `≤40 p50/≤200 p95` verified per lane + override baseline established. No enforcement without this packet. |
| **2 — Canary + earn-out** | Weeks 8–14 per route | `R2S2.md:3` lifecycle: `Draft (content-hashed) → Static validation (schema, invariants, fail-stance floors, no-LLM nodes, locked R3) → Shadow replay (actuator/latency/FP/FN deltas) → Canary on bounded slice / dual-emit → Auto-rollback if override >3× baseline OR error budget breached → Named-principal approval → Gradual promote` | Canary cohort shows `Edit` on R1 head + `Escalate` on R3 refund held with packet; text streams, payment waits. | **Canary** on 5–10% of that route; rest remains shadow | FNR CI tightens with adjudicated sample (100% of holds/escalates + random Pass sample to expensive ground truth) `R2S2.md:5`. Where ground truth missing, stays `null`. |
| **3 — Route-generalization** | Weeks 14–24 | Second live route (knowledge) on same plane — same graph, same matrix, **no fork**. `RoutePolicy` varies only `provenance_scope · action_grammar (allow-list) · action_to_R_mapping (subject to locked R3) · verification_profile · fail_stance_by_R (must match tier floors) · latency_budget`. Add decision-support **template** in proposal only — not a live third demo route. | Principal-flip + `UNKNOWN never→SUPPORTED` derived-claim boundary (recompute or `UNKNOWN`) visible on both routes. `ARCHITECTURE.md:7` | **Enforce per route** only where earned; shadow remains default elsewhere. Day-one posture for every new route = shadow. | Per-route earn-out satisfied independently; matrix never parameterized by route. |
| **4 — Operating rigor** | Continuous | Per-route `FNR/FP/override/dead-compute/rework/non-convergence/latency by lane/entitlement violations/actuator distribution/circuit-breaker state/evidence coverage` with CIs when earned. Circuit breaker downgrades autonomy on gate-fail rate sliding window. Policy overlays additive only (geography/industry cannot loosen matrix). `R2S2.md:3` | Skeptic surface: `FNR schema first` (with nulls where unearned) → drill `Action→cell→verdict→span→source/hash/ACL→principal→policy+verifier versions→lane→adjudication` → override trend + rollback evidence | **Enforce earned; degrade gracefully** R0/R1 open+annotate, R2/R3 closed/escalate — universal fail-open forbidden (bypassable by load). `R2S2.md:3` | Governance audit reconstructs every actuator from `ledger + policy_version + frozen matrix`. |

**Hard cut rule every phase:** Any feature that cannot be shown as a read of `STEP→SPAN→CLAIM→ACTION` is cut from the prototype/demo and moved to the proposal or later phase. `R2S1.md:7`

---

## 6. Key Risks & Mitigations

**Scope = technical + operational + adoption — the buyer’s real risks, not our feature list.**

### Risk 1 — False assurance on derived / multi-hop / aggregative claims (strongest residual technical risk `ARCHITECTURE.md:7`)

*Why it remains:* Entailment is weakest exactly where value is highest (synthesized conclusions). Shallow span can look entailed; marking it `SUPPORTED` is **strictly worse than no plane — humans stop checking.**

*Mitigation (frozen, three lines):*

1. **Route derived claims away from NLI entirely.** Arithmetic/aggregative → recomputed from spans. Neither recomputable nor directly entailed → `UNKNOWN`. **`UNKNOWN` never collapses into `SUPPORTED`** — the boundary between plane and false assurance.
2. **Decorrelate by construction.** Verifiers (NLI ~300 M) from different model family than generator; deterministic checks carry majority enforcement weight because they cannot share failure modes.
3. **Publish our own error bars.** Stratified shadow audit stratified by claim type; FNR publishes miss rate `FNR = FN/(TP+FN)` inverse-weighted, Wilson/bootstrap CI `R2S2.md:5`. Routes may declare claim patterns as `derived` (config overlay forcing recompute-or-UNKNOWN) `R2S2.md:7`.

### Risk 2 — Source itself is poisoned / stale / wrong, or ACLs are wrong / missing (over-permissioned index — the most common real incident `ARCHITECTURE.md:3:1`)

*Why it remains:* Plane proves `claim ↔ captured evidence` and enforces *carried* ACLs. It does not prove the source is true and does not repair IAM. `QA.md:B4`

*Mitigation:*

* Immutable `source_id + content_hash` on every accepted binding; forensic ledger for rollback.
* ACL fidelity contract `source_id · ACL · hash · offsets` at assembly; missing ACL = gap recorded as `unentitled` on privileged routes, counted as `ACL-missing` `R2S2.md:5`.
* **Entitlement-violation rate per source = detector** for over-permissioned indexes (reporting signal — not silent remediation). Quarantine / de-rank connectors via policy version. Boundary stated: defend link, make IAM failure visible and measurable. `R2S2.md:7`

### Risk 3 — Over-flag / under-flag tradeoff + R mis-mapping (bypass or liability)

*Why it remains:* Over-intervention → bypass (`QA.md:C5` “switched off in a quarter”); under-intervention → liability. Mis-mapping `payment→R1` applies wrong row without “breaking” the matrix. Brief requires this tradeoff deliberately.

*Mitigation:*

* Shadow default before enforcement; earn-out per route.
* Blast-radius-priced verification depth (R0/R1 mostly Lane 1) — price stays proportionate.
* `R0/R1 fail open + annotate; R2/R3 fail closed/escalate` — universal fail-open forbidden.
* **Locked action classes `payment·deletion·publication·regulated_advice → R3` parse-time reject** — route cannot map refund to R1. `R2S2.md:2`
* No policy ships without replay + canary; auto-rollback on `>3×` override; circuit breaker downgrades autonomy; publish `intervention_precision / override_rate` per route; hard interlock in **action executor**, not only UI. `R2S2.md:7`

### Risk 4 — Latency / placement risk (“this will make the product slow”)

*Why it matters:* Wrong placement makes any check feel like product lag.

*Mitigation:* Expensive part precomputed — provenance indexed at assembly, so binding is lookup against small in-memory set `ARCHITECTURE.md:5`. Stream verification at sentence boundaries (marginal ≈ one sentence), hold-back 150–300 ms (liability gap of `emit-then-recall` eliminated), hard gate only on actions (20–40 ms inside 200 ms–2 s tool RTT — invisible), three lanes with hard budgets `Lane1 30–60 p95 deterministic no LLM no hop / Lane2 100–400 ms bounded / Lane3 async`. Budget follows blast radius; 80–90% of volume is R0/R1 Lane 1 only. Proof cache keyed by context hash. Targets honest: `≤40 p50 / ≤200 p95` on R0/R1 text; **never quote 40 as p95**. `ARCHITECTURE.md:5` `QA.md:C1`

### Risk 5 — “Another dashboard / RAG groundedness / AI-safety tool” pattern-match (narrative risk)

*Why it kills:* Judge pattern-matches first 20 seconds and stops hearing architecture. Trigger = any opening that starts from risk. `NARRATIVE.md:6`

*Mitigation (four corrections):*

1. **Open on held transaction, never on risk.** First thing on screen = pending ₹1,84,000 `R3×unsupported-categorical→Escalate` with evidence packet — not a person, not a risk header.
2. **Ban the vocabulary.** `monitor/observe/detect/watch/guard/trust score/risk score/observability/guardrail/responsible AI` → `authorise/admit/prove/bind/refuse/hold/escalate/gate`; first failure sentence contains `claim`, safety only after deterministic entitlement check. One permitted exception `Everyone watches the exit. Nobody records the entrance.` `NARRATIVE.md:6`
3. **One trace end to end** — same refund in hook, mechanism, matrix, closing line. Depth reads as production experience; breadth reads as slideware.
4. **Infrastructure position** — firewall / transaction validator / CPU privilege mode, not AI-safety wrapper.

### Risk 6 — Prompt injection / self-reported provenance / poisoning the corpus

*Why it matters:* Attacker tries to make a false claim bind to a real span or author its own evidence.

*Mitigation:* Binding computed by plane, not asserted by model — model has no channel to declare bindings `QA.md:B5`. Injected instruction cannot create/modify `SPAN` or `ACL` or `binding edge` (`R2S1 §4:5,14`, `R2S3 §7:14,22`). Attack that does work = poisoning a source document — supply-chain attack; `source_id + content_hash` makes it forensically traceable. Boundary stated: defend `claim→evidence` link, not truth of evidence.

### Risk 7 — “It works in demo, does not generalise”

*Why it matters:* Single trace ≠ enterprise.

*Mitigation:* Mechanisms are trace-independent — span membership, ACL comparison, arithmetic recomputation, backward attribution same on any trace. What varies = per-route verification budget, governed by versioned DAG and earned per-route calibration. Shadow counters across `tens of thousands/week` directional scale `docs/ps.md`; probe replays already defined. `QA.md:D3`

---

## 7. Differentiation Anchor — the 5 points that survive a hostile room

| # | Point (one line) | ControlPlane | The six they brought |
|---|---|---|---|
| **1** | **We read receipts, not minds — set-membership test** `NARRATIVE.md:1` | `which span proves it?` — lookup against `source_id·ACL·hash·offsets` captured **before** the model ran, with source identity and access rights attached | LLM-as-judge asks `does this look right?` — unfalsifiable, same-family blind spots, no source docs, no identity |
| **2** | **Entitlement is authorization, not classification** `ARCHITECTURE.md:3:1` | Correct HR fact on an ACL-excluded span → violation → `R1×entitlement→Edit` or `R3→Escalate`. Same claim, different principal → different outcome. Deterministic Aho-Corasick + ACL lookup, microseconds, zero LLM. No output-only tool can replicate — none carry caller identity into verification layer. Over-permissioned RAG leak is the most common real incident and they are structurally blind to it. | Guardrails (LlamaGuard) identity-blind; RAG checkers average scores; observability has no identity |
| **3** | **Proof scales with consequence — worst claim per pending action, never an average** | Same response, two pending actions: `text.show → R1×entitlement→Edit` (stripped) + `refund.execute → R3×unsupported-categorical→Escalate — held` (packet) — both correct simultaneously. Identical verdict annotates a draft and holds a payment — budget spent where harm is. `NARRATIVE.md:2` | RAG averages (one wrong figure drowns); composite 87/100 maps to nothing; uniform validation depth wastes budget |
| **4** | **`Not low confidence. Unproven.` Default = UNSUPPORTED, burden of proof inverted** | Claim carries burden — nothing passes because nobody objected. Confidently wrong treated as what it is: absence of proof, not low score. `NARRATIVE.md:7` Fail stance tiered — universal fail-open forbidden (bypassable by load). | Confidence/logprob thresholding — broken instrument detecting its own failure; flag-what-looks-wrong-default-allow |
| **5** | **We publish what we missed — and we instrument waste exactly** | Per-route FNR schema published with `null/insufficient_sample` where unearned; stratified shadow audit `100% of Block/Escalate/Edit + random slice of Pass/Pass+annotate` → human/exspensive-verifier ground truth → CI. Emptiness is credibility — judge finds honesty not bluff. **Plus** dead compute exact: `₹5 of ₹8 grounded nothing` `ARCHITECTURE.md:7` — the number a buyer signs against; no competitor has the graph to compute it. `NARRATIVE.md:7` | They publish precision — how often they bother the user. No one publishes FNR. No one has backward dead-compute. Dashboards measure spend, not waste. |

> *Naming real products is itself a differentiator — nobody else in the room will name names.* `NARRATIVE.md:3` — we named NeMo Guardrails, LlamaGuard, Lakera, LangSmith/Helicone/Arize/WhyLabs, Azure AI Content Safety / Bedrock Guardrails.

---

## 8. Fidelity Self-Check — explicit confirmation

This proposal does **not** reopen, soften, or reinterpret anything frozen in `R2S1.md`, `R2S2.md`, `R2S3.md`, `ARCHITECTURE.md`, `NARRATIVE.md`, `QA.md`.

| Check | Status | Evidence in this spine |
|---|---|---|
| **Soften Default = UNSUPPORTED** | **No** — untouched | §2 Default row: every check-worthy claim starts UNSUPPORTED, must earn SUPPORTED; UNKNOWN never → SUPPORTED. No confidence threshold replaces it. `R2S1 §3:3`, `R2S2 §3` global invariant 1/2 |
| **Weaken entitlement / ACL check** | **No** — untouched | §2 Entitlement = `principal∈ACL` deterministic, Lane 1, zero LLM, cannot be disabled; per-source violation rate is detector (not IAM fix). `R2S1 §3:5`, `R2S2 §3:3` |
| **Redraw the matrix** | **No** — untouched | §2 16-cell table transcribed exactly, column vocabulary `Contradicted/entitlement violation · Unsupported+categorical · Unsupported+hedged · Unknown` + rows R3–R0. Matrix = `f(R,S)` no route parameter; locked R3 classes. No new tiers/actuators/scores. `R2S1 §3:6`, `R2S2 §2:0` |
| **Move hard gate from actions to tokens** | **No** — untouched | §2, §5 Hard gate on commit path; text hold-back 150–300 ms; R0/R1 open+annotate / R2/R3 closed/escalate; speculative release forbidden. `R2S1 §3:8`, `ARCHITECTURE.md:5` |
| **Claim we eliminate hallucination / bias / privacy risk or fully solve it** | **No** — refuse-to-claim preserved (about *us*) | §4 + §6 state: eliminate hallucinations / zero integration / zero latency / one accuracy number not claimed. Plane publishes own FNR; bias = async route-level flip-rate+CI, privacy = entitlement visible. `NARRATIVE.md:5`, `R2S1 §4:28`, `ARCHITECTURE.md:10:8` |
| **Introduce LLM-as-judge / confidence scores as primary mechanism** | **No** — rejected category | No LLM reasoning at decision time; NLI is binding classifier producing `SUPPORTED/CONTRADICTED/UNSUPPORTED/UNKNOWN`, not a judge opinion. No scalar trust/risk/confidence drives actuator — only `R×S`. `ARCHITECTURE.md:8`, `R2S2 §3:11` |
| **Treat bias as live per-response verdict** | **No** — untouched | §2 + §6 Bias = async counterfactual replay, protected-attribute perturbation, flip-rate + CI, flag when CI excludes zero, feeds route policy review — never `claim→bias verdict→matrix cell`. No third live bias route. `ARCHITECTURE.md:3:2`, `R2S2 §4:loop`, `R2S3 §3` mocked bias absent |

**Also untouched:** surgical Edit only; evidence-packet escalation (claim+candidate spans+verdict+diff); one graph three reads; Lane 1 always on; API-layer only (SDK hook + reverse proxy, no weights/logits/fine-tuning); content laws `clause 7.2 does not exist / never “blocked” about refund / company wrongly pays out / ≤40 p50/≤200 p95 / empty FNR emptiness is credibility`; vocabulary `authorise/admit/prove/bind/refuse/hold/escalate/gate`; `UNKNOWN` timeout → matrix + tier fail stance; no competing mechanism added.

**Rule obeyed:** the proposal makes the frozen architecture feel *inevitable* — heterogeneous routes with different blast radius × latency × regulation posture can only be governed by varying what reaches the matrix (R inputs, provenance scope, action grammar, lane budget), never by forking the matrix itself.

---

*End of Round 2 Stage 4 Business Proposal Spine. Stages 1–3 are rendered, not reopened. A judge can stress the logic on this spine and attack the design on the architecture — no benchmark needs to be trusted.*

