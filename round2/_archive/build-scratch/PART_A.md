# ControlPlane.ai — Round 2 Final Hybrid (Eternal)
## Admission-Control Layer for AI That Acts

> Accenture Innovation Challenge 2026 · Round 2 · Final Hybrid (Stages 1–2)  
> Status: **ETERNALLY FROZEN**  
> Sources of truth (absolute): `docs/ARCHITECTURE.md` · `docs/NARRATIVE.md` · `docs/QA.md` · Official Round 2 ControlPlane.ai brief (`docs/ps.md`) · frozen stage locks `R2S1.md` · `R2S2.md`  
> **This file is THE one deliverable for Stages 1–2.** It merges prototype proof (R2S1) and enterprise operating envelope (R2S2) around the same admission primitive. Do not reopen.  
> Code / architecture pointers: Evidence Ledger `STEP → SPAN → CLAIM → ACTION` · Action Interlock as pure `f(R, S)` · Provenance Recorder outside the model · thin context-assembly SDK hook + OpenAI-compatible reverse proxy + mock refund action adapter.

**Non-negotiable freeze:** Default = UNSUPPORTED · entitlement/ACL · exact R×S matrix · one graph · hard gate on actions · published FNR as format · two-pending-actions resolution.

---

## 0. One-Sentence Thesis + Stack Map

**Thesis:** ControlPlane is an admission-control layer that treats every AI claim as requesting permission to act — not a response to be scored — so an unproven or unauthorized claim cannot authorize an action, and the plane publishes per-route what it missed.

**What this hybrid contains (one product, four lenses — not four products):**

| Lens | What it locks |
|---|---|
| **Prototype proof** | Exactly two live routes — Refund (R1+R3 dual-action) and Knowledge (R0/R1 entitlement flip) — on one Evidence Ledger |
| **Enterprise envelope** | Multi-route via `RoutePolicy` configuration, governance lifecycle, feedback as calibration, FNR typed schema, residual-risk mitigations |
| **Build / demo authority** | Will / Will-Not, assumptions, 25 binary success criteria, ≤8-minute live demo built backward from the action gate |
| **Business spine (deferred)** | Buyer / value / rollout lives in Part B (R2S4 material) — not written here |

Round 2 scales across heterogeneous routes by changing **route configuration, verification budget, action grammar, enforcement lifecycle, and reporting** — never by inventing a second detector, a confidence score, or a trained safety model.

---

## 1. Problem Framing

### Running example (clause 7.2)

Canonical frozen failure:

> *“Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.”*

**Clause 7.2 does not exist.** The failure is *absence* of evidence, not conflicting evidence. Ordinary filters can pass it. Confidence can read high. If ungated, **the company wrongly pays out ₹1,84,000**; the customer did not lose money. Money moved Tuesday, found Friday.

### Structural failures this plane exists to catch

| Failure mode | Why ordinary stacks miss it | ControlPlane treatment |
|---|---|---|
| Absent policy clause authorizing refund | Filters look for conflict; confidence scores the text | Unsupported + categorical on R3 → **Escalate** (held with evidence packet) |
| Correct-but-unauthorized disclosure | RAG groundedness averages semantic match; ignores principal | Entitlement = set-membership `CALLER → CLAIM → SPAN → SOURCE ACL` → matrix by R |
| Numeric / date / identifier error on a transaction | LLM-as-judge guesses; logprobs do not detect confidently-wrong | Deterministic recomputation against captured spans |
| Irreversible payment on the same response as customer-visible text | One “response blocked” collapses two different blast radii | Two pending actions, independently priced on the matrix |
| No reliable real-time external ground truth | Open-web “truth layers” invent authority | Proof = captured evidence set + deterministic recomputation only |

### Content laws (locked)

| Law | Exact rule |
|---|---|
| Clause 7.2 | **Does not exist.** Absence of evidence, not conflict. Never “caps,” “denies,” or “doesn’t cover.” Absence (not contradiction) puts the claim in the *Unsupported + categorical* column — which is why the correct actuator is **Escalate**, not Block. |
| Refund language | Never say the refund was **“blocked.”** Say **held and escalated with the evidence packet.** |
| Who pays | **The company wrongly pays out.** The customer did not lose money. |
| Dual action | Show text → **R1 × entitlement → Edit** (C3). Issue refund → **R3 × unsupported-categorical → Escalate** (C2). Both correct simultaneously. Never one response-level verdict. |
| Latency | R0/R1 added text: **≤40 ms p50 / ≤200 ms p95**. Speculative verification OK; speculative release forbidden. Never quote 40 ms as p95. |
| Refuse-to-claim (about *us*) | Do **not** claim: eliminate hallucinations · zero integration · zero added latency · one accuracy number across failure modes. |

### Scope tension (resolved for the freeze)

The brief names decision-support and bias; the architecture defines bias as distributional/async. Resolution: decision-support and counterfactual bias measurement stay in the **enterprise envelope**; they do **not** contaminate the live core prototype. A third live decision-support / bias route is **refused**. Bias stays as **measurement** language only — never as a per-response verdict.

---

## 2. Core Thesis & Admission Primitive

### Stage 1 thesis (prototype)

ControlPlane is an admission-control layer that treats every AI **claim** as requesting permission to act — not a response to be scored. Provenance captured outside the model turns verification into a **set-membership test** against evidence assembled before generation (`source_id · ACL · hash · offsets`). Every claim starts **UNSUPPORTED** and must earn proof; entitlement is deterministic set-membership against caller and source ACL; verification is priced by blast radius on the frozen R×S matrix, with the hard gate on actions, not tokens.

**This Stage 1 prototype proves the admission primitive on exactly two live routes — Refund (R1+R3 dual-action) and Knowledge (R0/R1 entitlement flip) — on one `STEP → SPAN → CLAIM → ACTION` Evidence Ledger.**

### Stage 2 expanded thesis (enterprise envelope)

ControlPlane is one admission-control plane: every AI response is a set of claims requesting permission to act. Provenance is captured outside the model at context assembly (`source_id · ACL · hash · offsets`); the calling principal is recorded with the request; every check-worthy claim starts **UNSUPPORTED** and must earn proof against that provenance; entitlement is deterministic caller-vs-source ACL set-membership; the Action Interlock applies the exact frozen R×S matrix and hard-gates actions, not tokens. Round 2 scales across heterogeneous routes by changing **route configuration, verification budget, action grammar, enforcement lifecycle, and reporting** — never by inventing a second detector, a confidence score, or a trained safety model. An unproven or unauthorized claim cannot authorize an action. The plane publishes per-route what it missed.

### Load-bearing primitives

| Primitive | Exact meaning |
|---|---|
| **Provenance outside the model** | Spans recorded at context assembly with `source_id · ACL · content_hash · offsets` (and calling principal). The model cannot declare, author, or alter provenance. Prompt injection / fake citations cannot write ledger edges. |
| **Default = UNSUPPORTED** | Every check-worthy claim starts unsupported. `SUPPORTED` only via binding/recomputation against the captured provenance set. `UNKNOWN` never collapses into `SUPPORTED`. Unsupported is **not low confidence. Unproven.** |
| **Entitlement** | Caller vs source ACL as a **set-membership test**; independent of semantic correctness; Lane 1; **zero LLM** in the ACL decision path. |
| **One graph** | Live `STEP → SPAN → CLAIM → ACTION`. No separate hallucination / privacy / action detectors. Performance, cost, and responsibility are three reads of one graph. |
| **Matrix pricing** | Exact frozen 4×4 R×S table applied **per pending action**. Proof scales with consequence. Pending-action disposition = **worst claim weighted by that claim’s role in the pending action — never an average**. |
| **Hard gate on actions, not tokens** | Text hold-back ~150–300 ms; tool commit boundary. Speculative verification permitted; **speculative release forbidden**. |

### Verdict set

`SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN` — default **UNSUPPORTED**; `UNKNOWN` never → `SUPPORTED`.

### Claim-type routing (not one detector)

- Numeric / date / identifier → deterministic recomputation
- Textual / factual → bind to provenance only (never open web); **paraphrase survives via entailment, not string match**
- Derived / multi-hop → recompute or `UNKNOWN`
- No model-emitted citation treated as evidence

### Ungrounded / purely parametric handling

When no provenance spans exist for a route, it is **declared ungrounded by construction**; such claims **cannot authorize any action** regardless of blast radius. Semantic-entropy probe (if any) is **Lane-3 async only**, never on the critical path.

*We don’t claim to verify what we were never given. We claim what we were never given cannot authorize an action.*

---

## 3. Exact Frozen R×S Matrix

**Transcribed — never redrawn.** Axis labels, column vocabulary, and cell values are load-bearing. All four rows × all four columns (16 cells). Applied **per pending action**. No low/medium/high simplification. **No route parameter** — the matrix is a pure function `f(R, S) → actuator`.

|  | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** | **Block** | **Escalate** | **Escalate** | **Escalate** |
| **R2** | **Block** | **Edit** | **Edit** | **Escalate** |
| **R1** | **Edit** | **Edit** | **Pass + annotate** | **Pass + annotate** |
| **R0** | **Pass + annotate** | **Pass + annotate** | **Pass** | **Pass** |

### R tiers

| Tier | Meaning |
|---|---|
| **R0** | Internal draft |
| **R1** | User-visible read-only |
| **R2** | Reversible write / external send |
| **R3** | Irreversible or regulated (payment, deletion, publication, regulated advice) |

**R formula:** `irreversibility × audience × data class × autonomy level`.

### Actuators vocabulary (exact)

**Block · Edit · Escalate · Pass / Pass + annotate.**

- **Edit is surgical, never generative.** Strip the unsupported claim, or re-invoke the generator **once** with a constrained instruction naming the exact failing span. Edited output re-enters the gate; a second failure falls through to Escalate. Free-form LLM rewriting produces a new *unverified* artifact — that is moving the problem, not solving it.
- **Escalate ships an evidence packet, not an alert:** the claim, the candidate spans, the verdict, the diff.
- Autonomy downgrade and circuit breaker are spoken controls — **not inventable demo labels**. Forbidden inventions include `STREAM`, `Kill Span`, `Hold & Re-verify`, `Redact & Flag`.

### Fail stance floors (≠ matrix action)

| Object | Answers |
|---|---|
| **Matrix** | Evidence *arrived* and is bad → what actuator? |
| **Fail stance** | Evidence *did not arrive in time* → open with annotation (R0/R1) or closed/escalate (R2/R3)? |

| Tier | Fail stance floor |
|---|---|
| **R0 / R1** | Fail **open with annotation** |
| **R2 / R3** | Fail **closed or escalate** |

Conflating matrix action with fail stance is how gating systems silently fail. Universal fail-open is forbidden — it makes the plane bypassable under load. Routes may **not** loosen R2/R3 to fail-open. Timeout → `UNKNOWN` → matrix + tier fail stance — **never implicit support**.

### Content law on held vs blocked

**Never say “blocked” about the refund.** R3 × unsupported-categorical = **Escalate**. Say *held and escalated with the evidence packet.* “Hold” is not a separate actuator — refund state = held while Escalate is in force. Customer-visible text can remain subject to its own R1 matrix result while the R3 refund stays held (never one collapsed “response blocked”).

**The verdict is hostile; the action is proportionate.** A claim must earn SUPPORTED, but merely failing to earn it only blocks where the blast radius justifies blocking.

> **Load-bearing.** Axis labels, column vocabulary and cell values are all load-bearing. **Transcribe it. Never redraw it.**

---

## 4. Prototype Scope (exactly two live routes)

Exactly **two** live routes. A third live decision-support / bias route is **refused**. Bias is a route-level asynchronous counterfactual property and must not enter the claim→action critical path.

| Route | Dominant blast radius | Strongest frozen mechanism | Stage 1 live? |
|---|---|---|---|
| **A. Customer Support Refund Agent** | R1 text + R3 refund, same response | Two-pending-actions (C2→Escalate, C3→Edit) | **YES** |
| **B. Internal Knowledge Assistant** | R0 / R1 | Provenance outside model + deterministic entitlement flip | **YES** |
| Decision-support / bias measurement | R0–R3 depending on action | Async route-level counterfactual bias | **NO** — enterprise / proposal only |

### Use Case A — Customer Support Refund Agent

- **Concrete description:** An AI support agent retrieves order and vendor-agreement context, emits customer-visible text, and proposes a refund tool call. Canonical frozen running example:

  > *“Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.”*

  **Clause 7.2 does not exist.** The failure is *absence* of evidence, not conflicting evidence. Ordinary filters can pass it. Confidence can read high. If ungated, **the company wrongly pays out ₹1,84,000**; the customer did not lose money. Money moved Tuesday, found Friday.

- **Risk signature:**
  - Absent policy clause (unsupported categorical — not contradiction)
  - Numeric / date / identifier error on the transaction
  - Retrieval-side entitlement leakage into customer-visible text
  - Irreversible payment on the same response as the text
  - No reliable real-time external ground truth; proof is only the captured evidence set and deterministic recomputation

- **Latency budget:**
  - Customer-visible text: **≤40 ms p50 / ≤200 ms p95** added (**never quote 40 ms as p95**)
  - Action verification amortised inside the tool round-trip; speculative verification permitted; **speculative release forbidden**
  - Text hold-back **~150–300 ms** so verification does not require post-hoc recall

- **Dominant blast-radius tier(s):** **R1** (show text) + **R3** (issue refund), simultaneously. Live centrepiece is the R1/R3 dual-action. **Proof scales with consequence.**

- **Frozen mechanism most powerfully demonstrated:** **Two-pending-actions resolution** on one graph. Pending-action disposition = **worst claim weighted by that claim’s role in the pending action — never an average** (one wrong figure must not drown in nine correct sentences):

  | Pending action | Tier | Finding | Matrix cell (ARCHITECTURE §9 shorthand) | Actuator |
  |---|---|---|---|---|
  | Show text to the customer | **R1** | Unentitled span grounds a claim in the text | R1 × entitlement (= column *Contradicted / entitlement violation*) | **Edit** — stripped |
  | Issue the refund | **R3** | Clause 7.2 has no span | R3 × unsupported-categorical (= column *Unsupported + categorical*) | **Escalate** — held with evidence packet |

  Both are correct simultaneously. Never collapse into one response-level verdict. **Never say “blocked” about the refund.** Say *held and escalated with the evidence packet.*

### Use Case B — Internal Knowledge Assistant (Mixed Governance)

- **Concrete description:** An employee-facing assistant over mixed well-governed and loosely governed internal sources. One ACL-restricted / over-permissioned span is intentional so a semantically correct answer can still be unauthorized for the caller.

- **Risk signature:**
  - Correct-but-unauthorized disclosure
  - Fabrication with no supporting span
  - Claim grounded in a span whose ACL excludes the caller
  - Prototype enforces carried ACLs; it does **not** repair enterprise IAM

- **Latency budget:** R0/R1 Lane-1 deterministic path: **≤40 ms p50 / ≤200 ms p95** added. NLI binding only when a claim requires it.

- **Dominant blast-radius tier(s):** **R0** / **R1**

- **Frozen mechanism most powerfully demonstrated:** Provenance outside the model + deterministic entitlement as a **set-membership test**:

  `CALLER → CLAIM → SPAN → SOURCE ACL`

  Authorization is set-membership. **Zero LLM** in the ACL decision path.

  **Demo staging rule:** Use Case B = ACL-excluded span → **R1 × entitlement = Edit**. It is **not** staged as no-span PII → Block (that would obscure the matrix cell used in the running example). The no-span PII rule remains in architecture / proposal; it is not this demo’s matrix case.

### Why this pair (and not three)

- Refund proves one graph, two pending actions, hard gate, surgical edit, evidence-packet escalation — **proof scales with consequence**.
- Knowledge proves the graph is not RAG groundedness: same semantic claim, different principal → different outcome (set-membership, not text scoring). RAG checkers **average**, so one wrong figure can drown in nine correct sentences; ControlPlane prices the **worst claim for each pending action**.
- Together: **“is this claim proven?”** and **“is this caller entitled to that proof?”**
- A third live decision-support route adds async bias measurement without strengthening the dual-action centrepiece. Bias is acknowledged per the brief and kept as route-level asynchronous counterfactual measurement in the proposal only.

### What is refused (live)

Third live decision-support / bias route · per-response bias verdicts · collapsing dual-action into one response-level verdict · calling the R3 unsupported-categorical refund “blocked.”

---

## 5. Prototype Boundary (Hard)

### Will Demonstrate

Observable and concrete:

1. **Context-assembly provenance capture (keystone)** — spans recorded outside the model with `source_id · ACL · content_hash · offsets` (and calling principal). The model cannot declare, author, or alter provenance.

2. **One request → one typed Evidence Ledger** — live `STEP → SPAN → CLAIM → ACTION`. No separate hallucination / privacy / action detectors. Performance, cost, and responsibility are three reads of one graph.

3. **Default = UNSUPPORTED** — every check-worthy claim starts unsupported. `SUPPORTED` only via binding/recomputation against the captured provenance set. `UNKNOWN` never collapses into `SUPPORTED`. Unsupported is **not low confidence. Unproven.**

4. **Claim-type routing (not one detector)**
   - Numeric / date / identifier → deterministic recomputation
   - Textual / factual → bind to provenance only (never open web); **paraphrase survives via entailment, not string match**
   - Derived / multi-hop → recompute or `UNKNOWN`
   - No model-emitted citation treated as evidence
   - Pending-action disposition = **worst claim weighted by that claim’s role in the pending action — never an average**

5. **Deterministic entitlement** — caller vs source ACL (**set-membership test**); independent of semantic correctness. Shown on Use Case B and inside the refund dual-action text path. Zero LLM.

6. **Exact frozen R×S matrix** — transcribed, never redrawn; **all four rows × all four columns** (16 cells); applied **per pending action**. No low/medium/high simplification. Actuators are exactly **Block · Edit · Escalate · Pass / Pass + annotate**. Forbidden inventions include `STREAM`, `Kill Span`, `Hold & Re-verify`, `Redact & Flag`.

7. **Two-pending-actions centrepiece** — same refund response:
   - customer-visible text → R1 × entitlement → **Edit**
   - refund → R3 × unsupported-categorical → **Escalate**

8. **Hard gate on actions, not tokens** — text hold-back **~150–300 ms**; mock refund cannot commit while **Escalate** is in force (refund state = held; “hold” is not a separate actuator).

9. **Surgical Edit** — strip the failing claim, or one constrained regeneration naming the failing span; re-gate; second failure → Escalate. No free-form rewrite.

10. **Evidence-packet Escalation** — claim, candidate spans, verdict, diff — not a bare alert.

11. **Published FNR as a format** — full per-route typed schema (route_id, policy_version, window, strata, counts, FNR, CI, measurement_status, …). Live demo shows **empty typed placeholders / null**. Emptiness is the credibility play: the eventual claim shape is *“on this route we catch \<measured\>% of ungrounded claims at 40 ms p50 — and here is the \<measured\>% we don’t.”* Never fabricate production accuracy.

12. **No composite confidence / risk score** drives disposition — only verdict severity × blast radius.

13. **Required secondary beat — principal flip** — change only the calling principal on Use Case B (or same ledger); entitlement outcome flips because ACL check is live set-membership. Zero LLM.

14. **Per-claim user surface** — each claim shows exactly one of **Verified / Uncertain / Blocked** — no raw scores. **Carve-out:** the refund *action* is shown as **Held / Escalate**, never “blocked” (content law).

15. **Ungrounded / purely parametric handling** — when no provenance spans exist for a route, it is **declared ungrounded by construction**; such claims **cannot authorize any action** regardless of blast radius. Semantic-entropy probe (if any) is **Lane-3 async only**, never on the critical path.

16. **Model cannot author bindings** — the generator has no channel to declare or supply its own provenance bindings (prompt injection / fake citations cannot write ledger edges).

17. **Live binding / gate compute visible** — claim→span binding (or another live compute step) shows real work (~tens of ms), not a pre-baked animation. If claims are pre-extracted for demo stability, binding/entitlement/interlock still run live.

18. **Text / action separation** — customer-visible text can remain subject to its own R1 matrix result while the R3 refund stays held (never one collapsed “response blocked”).

19. **Shadow counterfactual (optional demo beat)** — gated-vs-ungated “would have held” emission for ≥1 route, labelled shadow — not claimed as production enforcement.

### Will Deliberately Not Demonstrate

| Exclusion | Precise reason |
|---|---|
| Third live decision-support / bias route | Dilutes the dual-action / entitlement proof; bias is distributional + async |
| Per-response bias verdicts | Contrary to frozen architecture |
| Production tens-of-thousands/week load test | Brief allows simulated scope; scale is proposal-only |
| Real payment execution | Unsafe; mock tool with real gate semantics |
| Real customer/employee PII | Unnecessary; legal risk |
| Live enterprise IAM remediation | Plane enforces carried ACLs; does not repair IAM |
| LLM-as-judge as primary verifier | Rejected category; destroys provenance/entitlement differentiation |
| Confidence / logprob / global risk scores | Confidently-wrong cannot be detected by confidence |
| Open-web factual verification | Binding is provenance-set only. *We don’t claim to verify what we were never given — we claim what we were never given cannot authorize an action.* |
| Generative full-answer rewrite | Edit is surgical only |
| Fabricated production FNR / “fully solve hallucination/bias/privacy” | Refuse-to-claim list is load-bearing |
| Full regulatory certification / geo-industry packs | Proposal/config scope |
| Lane-3 critical-path demo (semantic-entropy, bias replay) | Off critical path by construction |
| Multi-agent swarm / conversation-among-agents demo | No proof value for the typed ledger + matrix |
| Human triage queue / SLA UI | Evidence packet is the deliverable |
| Dead-compute / non-convergence as centrepiece | Secondary graph read; must not crowd dual-action |
| Model weights, logits, fine-tuning | API-layer only |

### Minimum Viable Live Demonstration

Judge must see in one interactive session (**≤8 minutes**), **not slides**:

1. Context assembled from sources with distinct ACLs; spans (`source · ACL · hash`) appear in the ledger **before** claim verdicts.
2. One refund response containing at least these check-worthy claims (all born **UNSUPPORTED**):
   - **C1** numeric amount/order → binds → **SUPPORTED**
   - **C2** categorical “clause 7.2 …” → **no span** → stays **UNSUPPORTED** (absence, not contradiction)
   - **C3** claim grounded on an ACL-excluded span → **entitlement violation**
   - plus a pending `refund.execute` tool action
3. Live `STEP → SPAN → CLAIM → ACTION` Evidence Ledger occupies **majority** UI (≥60%) — not chatbot chrome.
4. C3 path → **R1 × entitlement → Edit** (surgical) on visible text.
5. C2 path → **R3 × unsupported-categorical → Escalate**; refund **held** with evidence packet; mock refund **does not commit**.
6. Exact frozen matrix cells highlighted for **both** actuators **before** they fire.
7. Principal flip (required secondary): change only the caller → authorization flips; ACL path uses **zero LLM**.
8. FNR schema visible as **empty typed placeholders / null only**.

**Governing test:** if removing the graph from the screen leaves the demo looking the same, scope has failed.

**Time budget:** Core dual-action crisis (held R3 + R1 Edit + packet + graph) ≤ **90 seconds**. Full session including principal-flip ≤ **8 minutes**. Anything that cannot be shown live visually is cut.

**Demo ordering (anti pattern-match):** open on the held transaction, never on a risk statement. First visible crisis = pending ₹1,84,000 refund held at **R3 × unsupported-categorical** with the evidence packet. Only then show the R1 text path edited. Binding/entitlement/interlock run **live** (visible compute), not as a recording. No risk score. No “blocked response.” No LLM-as-judge output.

### Biggest scope risk + exact mitigation

**Risk:** Judges pattern-match the demo as another RAG-groundedness checker / AI-safety dashboard — flags and UI without proving that unproven claims cannot authorize actions.

Decisive failure modes:

- Collapsing dual-action into one “response blocked”
- Failing to make the held R3 commit visually undeniable
- Looking like a pre-computed animation rather than a running control plane
- Letting secondary surfaces (bias stats, dead-compute charts, regulatory packs, chatbot chrome) crowd out the matrix

**Exact mitigation:**

1. Open with the indictment line (permitted exception): **“Everyone watches the exit. Nobody records the entrance.”** Then prove we record the entrance (provenance) and gate the exit (action).
2. Build the demo **backward from the action gate**: first crisis = pending ₹1,84,000 refund held at **R3 × unsupported-categorical** with the evidence packet visible — not a risk dashboard.
3. Immediately show the same response’s R1 path surgically **Edited** — two actuators, one graph. **Proof scales with consequence.** Show that disposition is **worst claim for that pending action**, not an average.
4. Majority UI = **Evidence Ledger**; highlight the matrix cell **before** the actuator. First spoken sentence about the failure contains **“claim,”** not “response.”
5. Follow with one **principal-flip** entitlement replay — authorization is a **set-membership test**, not text classification.
6. Binding (or another live compute step) must show real work if claims are pre-extracted — a hostile judge must not dismiss the path as a recording.
7. **Hard cut rule:** any feature that cannot be shown as a read of `STEP → SPAN → CLAIM → ACTION` is cut from the prototype and moved to the business proposal.
8. Demo vocabulary: authorise · admit · prove · bind · refuse · hold · escalate · gate — not monitor · detect · observe · watch · guard · trust score · risk score · “responsible AI” as a standalone virtue.

**Success condition:** a judge can point from **action → claim → externally captured span → principal entitlement**, and mark every row in §7 yes/no in under eight minutes.

---

## 6. Explicit Assumptions

### Data and provenance

1. Synthetic / enterprise-shaped corpora only. **No real customer, employee, financial, or health PII.**
2. Every span carries `source_id`, `ACL`, `content_hash`, offsets.
3. At least two source classes; deliberate over-permissioned / ACL-restricted scenario included.
4. Tool results are provenance-bearing spans.
5. Generator cannot write, alter, or self-report provenance bindings — including fake citations / self-graded “sources.”
6. Clause 7.2 has no supporting span by construction; numeric claims used for recomputation have deterministic source values.
7. Prompt injection is untrusted input; it cannot modify the provenance ledger or create binding edges.
8. At least one paraphrase fixture exists where entailment succeeds without string match; at least one purely parametric (no-retrieval) fixture is declared ungrounded by construction.

### Models and verification

9. Generator via OpenAI-compatible API only. **No weights, logits, hidden states, or fine-tuning.**
10. Claim extraction may use a small model and/or deterministic patterns; textual binding may use NLI against the provenance set only (entailment, not string match).
11. **Decision policy is a pure rule engine: zero LLM reasoning at decision time.**
12. Output interceptable before release and before action execution.
13. Generator is not assumed truthful.

### Traffic and latency

14. Reference scale is tens of thousands of interactions/week (directional). Live prototype is curated traces on a single node — **no production throughput claim**.
15. Traffic skewed to R0/R1; R2/R3 are a minority.
16. Authoritative R0/R1 added latency: **≤40 ms p50 / ≤200 ms p95**. Demo latency reported separately; **never quote 40 ms as p95**; never relabel p50 as p95.
17. Action gating measured against tool RTT, not token generation. Speculative verification OK; speculative release forbidden. Hold-back **~150–300 ms**.
18. Proof timeout → `UNKNOWN` → matrix + tier fail stance (R0/R1 fail open with annotation; R2/R3 fail closed or escalate). Timeout is never implicit support.

### Regulatory and evaluation

19. Enterprise-general posture for the prototype; proposal may reference dual jurisdiction relevant to team/context (e.g. **DPDPA 2023 + GDPR**) as configuration packs — **not** certification claims.
20. Evaluation traces are hand-crafted/adjudicated. Not enterprise ground truth. **Corpus poisoning is outside the prototype’s truth guarantee** — provenance makes source+hash auditable; it does not prove the source is factually true.
21. Any FNR field without trustworthy ground truth stays **null / unavailable**.
22. Shadow is the conceptual default before enforcement; demo may emit gated-vs-ungated counterfactual without claiming earn-out.
23. Bias = async route-level counterfactual flip-rate + CI in the **business proposal only** — not a live prototype actuator (**do not drop bias** from the Round 2 story; do not make it a live per-response verdict).
24. Escalation displays an evidence packet; no full human triage queue/SLA simulation.

### Integration

25. Thin context-assembly SDK hook + OpenAI-compatible reverse proxy + mock refund action adapter. No application rewrite.
26. Identity/ACL metadata available from upstream or simulated.
27. Demo action executor honors the interlock; UI cannot bypass it.
28. Prototype does **not** claim (refuse-to-claim list is about *us*, not competitors): eliminate hallucinations · zero integration · zero added latency · one accuracy number across failure modes.

---

## 7. Success Criteria for the Prototype

Each criterion is **binary**. A judge marks yes/no. Prototype succeeds **iff all are yes**.

| # | Criterion | Pass condition |
|---|---|---|
| 1 | Provenance outside the model | Every displayed retrieved/tool span shows source, ACL, hash, and offsets **before** claim verdicts. |
| 2 | One-graph invariant | UI/log shows one `STEP → SPAN → CLAIM → ACTION` ledger for the request. |
| 3 | UNSUPPORTED default is real | Every newly extracted check-worthy claim enters as `UNSUPPORTED`; none begin as `SUPPORTED`. Label is unproven — not “low confidence.” |
| 4 | Absence ≠ contradiction | Clause 7.2 has no span → stays `UNSUPPORTED` (never “caps,” “denies,” or “doesn’t cover”). |
| 5 | Claim-level proof works | A supported claim visibly binds to a specific captured span; an unsupported claim visibly lacks such proof. |
| 6 | Two pending actions resolve independently | One refund response simultaneously yields **R1 → Edit** and **R3 → Escalate**. |
| 7 | Hard action gate is real | Mock refund does **not** execute while gate outcome is Escalate or Block; text is not collapsed into one “response blocked.” |
| 8 | Entitlement independence | Semantically correct claim on an unauthorized span → entitlement violation; same source/claim under two principals flips when ACLs differ; zero LLM in the ACL path. |
| 9 | Exact matrix fidelity | Demonstrated cells match the frozen 4×4 transcription (all 16 cells load-bearing); no invented tiers, actuators, or composite scores. |
| 10 | Evidence packet | Escalate shows claim + candidate spans + verdict + diff. |
| 11 | Surgical edit | Failing claim stripped or regenerated once under the failing-span constraint; edited result re-gated. |
| 12 | FNR format honesty | Per-route FNR schema present with null/empty placeholders — no fabricated production accuracy. |
| 13 | No confidence driver | Final actuator traces to verdict × blast radius, not a scalar trust/confidence/risk score. |
| 14 | Prompt injection cannot author provenance | Injected instruction cannot create or modify a provenance span or binding edge. |
| 15 | Refund language fidelity | Demo never describes the R3 unsupported-categorical refund as “blocked”; it is held and escalated with the packet. |
| 16 | Paraphrase binding | A paraphrased supported claim still binds via entailment; string-only match is insufficient alone. |
| 17 | Per-claim user surface | Each claim shows exactly one of Verified / Uncertain / Blocked — no raw scores; refund *action* remains Held/Escalate. |
| 18 | Ungrounded / parametric gate | A no-provenance parametric claim cannot authorize any action (declared ungrounded by construction). |
| 19 | Worst-claim weighting | Pending-action disposition uses worst relevant claim for that action — not an average across claims. |
| 20 | `UNKNOWN` never → `SUPPORTED` | Timeout or non-recomputable derived path yields `UNKNOWN` and routes via matrix — never silent allow. |
| 21 | Speculative release forbidden | Tool commit path never releases before interlock decision (speculative verification may run; release may not). |
| 22 | Model cannot self-declare binding | Removing/changing a model-emitted citation does not create or alter externally captured provenance or ACL result. |
| 23 | Hold-back present | Text path uses ~150–300 ms hold-back (or equivalent visible buffer) before release. |
| 24 | Full 4×4 matrix present | UI/log shows the exact frozen matrix (four rows × four columns), not a low/medium/high collapse. |
| 25 | Set-membership entitlement visible | Entitlement decision shows principal vs span ACL as set-membership (not a classifier score). |

### Fidelity invariants (completely untouched)

| Frozen invariant | Status |
|---|---|
| **Default = UNSUPPORTED** | Untouched. Claims must earn `SUPPORTED`. Absence of proof is not low confidence and not implicit allow. |
| **Entitlement / ACL check** | Untouched. Caller vs source ACL on captured spans; deterministic; identity in the verification layer; zero LLM. |
| **Exact R×S matrix** | Untouched. Transcribed; never redrawn; axis labels, column vocabulary, and cell values are load-bearing; **no route parameter**. |
| **Hard gate on actions, not tokens** | Untouched. Hold-back for text; commit boundary for tools/actions. |
| **Published FNR as a format** | Untouched. Empty typed schema; emptiness is the credibility play. |
| **Two-pending-actions resolution** | Untouched. R1 Edit + R3 Escalate on the refund running example, simultaneously; never one response-level verdict; never call the refund “blocked.” |
| **`UNKNOWN` never → `SUPPORTED`** | Untouched. Derived/timeout paths return `UNKNOWN` and route via the matrix — never silent allow. |
| **Zero LLM at decision time** | Untouched. Action Interlock is a pure rule engine. |
| **Bias remains route-level / async only** | Untouched. Counterfactual flip-rate + CI; never a per-response matrix verdict; not a Stage 1 live route. |

**Also untouched:** Surgical edit only · evidence-packet escalation · No LLM-as-judge on the critical path · One graph, three reads · Lane 1 always on · locked R3 action classes · Content laws (clause 7.2; company wrongly pays out; latency floors; refuse-to-claim list).

**No competing mechanism enters the prototype:** LLM-as-judge primary path · confidence thresholding as hallucination signal · composite risk score · open-web truth layer · per-response bias classifier · redrawn matrix.

---

## 8. Enterprise Envelope — Multi-Route Architecture

### Runtime sequence (identical on every route)

```text
AI Application / Agent Route
        │
        ├── Context-Assembly SDK Hook → Provenance Recorder
        │        SPAN: source_id · ACL · hash · offsets
        │        (caller principal bound to the request / ledger)
        │
        └── OpenAI-compatible Reverse Proxy
                 │
                 ▼
        Evidence Ledger  STEP → SPAN → CLAIM → ACTION
                 │
     ┌───────────┼────────────┐
     ▼           ▼            ▼
 Performance  Responsibility  Cost
 (bind/prove) (ACL/interlock) (yield/rework)
     └───────────┼────────────┘
                 ▼
          Action Interlock
          Exact R × S Matrix   ← pure f(R,S); no route parameter
                 │
     Pass / Pass+annotate / Edit / Escalate / Block
                 │
     Text hold-back  ·  Action commit boundary
```

One graph. Three reads. No separate hallucination / privacy / action products.

### What is shared across every route (enterprise invariants)

| Shared component | Invariant — not soft-configurable |
|---|---|
| Provenance Recorder | Outside the model; model cannot author/alter spans |
| Evidence Ledger | Append-only, hash-chained; one typed graph per request/session |
| Claim extraction | Typed check-worthy claims; categorical vs hedged |
| Proof path | Numeric/date/ID → deterministic recomputation; textual → bind to provenance only (no open web); derived/multi-hop → recompute or `UNKNOWN` |
| Verdict set | `SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN`; default = **UNSUPPORTED**; `UNKNOWN` never → `SUPPORTED` |
| Entitlement Auditor | Caller vs source ACL; Lane 1; **zero LLM**; cannot be disabled |
| Action Interlock | Sole final decider; pure rule engine |
| Exact R×S matrix | One table (§3); **no route-specific cells**; no route parameter |
| Fail stance floors | R0/R1 fail **open with annotation**; R2/R3 fail **closed or escalate** |
| Hard gate | Actions / commit path — not tokens |
| Surgical Edit | Strip failing claim or **one** constrained regeneration naming failing span; re-gate; second failure → Escalate |
| Evidence packet | Claim + candidate spans + verdict + diff |
| Claim-level user surface | Verified / Uncertain / Blocked — no raw scores. **Refund action language remains Held/Escalate — never “blocked” about the refund.** |
| FNR contract | Same per-route typed schema everywhere |
| Lane 1 | Deterministic only — **cannot be disabled** |

### RoutePolicy (per-route configuration — not a new product)

```text
RoutePolicy {
  route_id
  tenant / principal_source
  use_case
  provenance_scope              # allowed source classes; required span metadata
  action_grammar                # tool × argument schema × irreversibility (allow-list)
  action_to_R_mapping           # subject to locked R3 classes
  verification_profile          # lane enablement, proof depth, timeouts, budgets
  fail_stance_by_R              # must match tier floors (R0/R1 open+annotate; R2/R3 closed/escalate); may NOT loosen R2/R3 to fail-open
  enforcement_mode              # shadow | canary | enforce
  error_budget                  # circuit-breaker sensitivity
  escalation_target
  sampling_policy               # FNR/FP strata and rates
  geography / regulatory_overlay  # additive only
  latency_budget                # must respect ≤40 ms p50 / ≤200 ms p95 for R0/R1 text
}
```

**Locked action classes** (parse-time reject if mapped below R3): `payment` · `deletion` · `publication` · `regulated_advice`. A route **cannot** map `issue_refund` / payment to R1.

### What routes may / may not change

| Routes may change | Routes may NOT change |
|---|---|
| Which actions exist | Default = UNSUPPORTED |
| How an action maps to R (except locked classes) | Entitlement logic |
| Lane-2 budget / proof depth | Matrix cells, columns, rows, actuators |
| Shadow vs enforce (enterprise deployment) | Hard gate location (actions, not tokens) |
| Sampling / escalation targets | Meaning of verdicts; `UNKNOWN` → `SUPPORTED` |
| Additive geo overlays | Composite risk/confidence as disposition driver |
| | Stage 1 live dual-action or two-route scope |

Low-consequence traffic does **not** get weaker truth semantics — it gets less verification budget and a proportionate actuator. Matrix evaluation is **per pending action**, preserving Stage 1 (C3/C2 centrepiece):

```text
R1 × entitlement                 → Edit      (C3 — unauthorized span in customer text)
R3 × unsupported + categorical   → Escalate  (C2 — clause 7.2 absent; held; never “blocked”)
```

### Enterprise route profiles

| Route | Dominant R | Lane posture | Enterprise enforcement posture | Stage 1 live? |
|---|---|---|---|---|
| Customer-support refund | R1 + R3 simultaneous | Lane 1 text; Lane 1+2 + interlock for R3 | Shadow/canary before production enforce; **Stage 1 live demo still shows the hard gate working on the mock refund** | **YES** |
| Internal knowledge | R0 / R1 | Lane 1 dominant; ACL always inline | Enforce after shadow evidence | **YES** |
| Decision-support | R0/R1 memo + R2/R3 action | Lane 2 for derived; Lane 3 async bias | Action gate when earned; bias measurement always async | **NO** (enterprise / proposal) |

Brief reference parameters (directional only): multiple AI use cases; tens of thousands of interactions/week; mix of well-governed and loosely governed sources. Prototype does **not** claim that throughput.

### Three lanes (shared; budgets configured)

| Lane | What runs | Path |
|---|---|---|
| **Lane 1** | Span membership, ACL, arithmetic, typed interlocks, Aho-Corasick PII/secret shapes | Inline; hard budget; no LLM; **always on** |
| **Lane 2** | NLI / binding for flagged textual claims; high-R traffic | Near-line; bounded; timeout → `UNKNOWN` |
| **Lane 3** | Semantic-entropy, counterfactual bias replay, calibration, shadow adjudication | Async; **never** on critical path |

### Multi-turn / agent compounding

Multi-turn = **more STEPs on the same session ledger**, not a separate architecture.

- Prior assistant text is **not** evidence merely by reappearing in context.
- Unproven turn-1 claim used to authorize an R3 action in turn N remains unproven → matrix still holds/escalates.
- Tool results enter as provenance **SPANs**, not automatic authorization for the next action.
- If source hash or ACL changes before a later action, re-verify → `UNKNOWN` or entitlement violation → matrix routes the action.
- No conversation-state “risk accumulator” product. Compounding risk is the same unproven claim reaching higher R — already covered by the frozen graph.

### Overlapping failure modes (brief: bias ∩ hallucination ∩ privacy)

| Situation | Treatment |
|---|---|
| Fabricated personal detail, no span | Unsupported + no-span PII/secret shape; claim stays UNSUPPORTED |
| Correct HR fact, ACL excludes caller | Entitlement violation (independent of semantic correctness) → matrix by R |
| Absent policy clause authorizing refund | Unsupported categorical on R3 → Escalate (held) |
| Bias on decision-shaped outputs | **Not** a per-response claim verdict; async route-level counterfactual flip-rate + CI |

Different mathematics, different owners — one graph, not one classifier.

### Envelope closure

```text
        ENTERPRISE ROUTES
   Support · Knowledge · Decision*
            │
            ▼
     SAME CONTROL PLANE
   STEP → SPAN → CLAIM → ACTION
            │
   SAME PROOF / ACL / R×S
   (matrix = f(R,S); no route parameter)
            │
   SAME ACTION INTERLOCK
            │
 PASS · PASS+ANNOTATE · EDIT · ESCALATE · BLOCK

* Decision-support exists in the enterprise envelope;
  it is NOT a Stage 1 live prototype route.
```

**Stage 2 IS:** configuration, governance, deployment lifecycle, feedback calibration, measurement, and enterprise operating loops around the frozen admission primitive.

**Stage 2 IS NOT:** a second mechanism for deciding whether an AI action should happen; a redrawn matrix; a live third bias product; a trained safety model; a reopening of Stage 1 use cases or prototype boundary; a claim that the plane eliminates hallucination, bias, or privacy risk.

---

## 9. Governance & Policy Layer

### Policy object

Versioned DAG of deterministic 4-tuples:

```text
(signal, threshold, action, latency_budget)
```

**Decision time = pure rule engine: zero LLM reasoning.** Policy is declarative code, not a prompt. Ambiguous rules fail at **parse time**.

### Configurable surfaces

| Dimension | Configures | Forbidden |
|---|---|---|
| **Use case / route** | Sources, action grammar, proof depth, lane budgets, audit strata, shadow/enforce | Soften UNSUPPORTED; disable entitlement; redraw matrix; reopen Stage 1 live scope |
| **Risk appetite** | Act vs propose; error budget; override auth; earn-out criteria | Replace matrix with risk score; fail-open R3 by default |
| **Geography / industry** | Additive: data classes, retention, escalation owners, action allow/deny, packet fields | Loosen matrix cells; remove ACL; mark unproven SUPPORTED |
| **Blast-radius tier** | Inputs to R assignment | Invent new R tiers or actuators |

### Governance hierarchy (narrows only)

```text
Enterprise baseline (frozen invariants)
        ↓
Geography / regulatory overlay (additive only)
        ↓
Tenant
        ↓
Route
        ↓
Action class / blast radius
```

Overlays may **only add constraints**. They may not loosen frozen invariants.

### Global invariants (not patchable; parse-time enforced)

1. `default_verdict = UNSUPPORTED`
2. `UNKNOWN → SUPPORTED` forbidden (strongest residual-risk boundary)
3. Entitlement check always active, Lane 1, zero LLM
4. Lane 1 cannot be disabled
5. Locked action classes → R3
6. Exact R×S matrix immutable (no route parameter; no cell edits)
7. R2/R3 fail stance = closed or escalate (tier property — may NOT loosen to fail-open)
8. Hard gate on actions, not tokens
9. Stage 1 live scope unreopened (exactly two live routes; dual-action centrepiece; no third live bias route)
10. No composite confidence/risk score as disposition driver
11. No LLM node in decision-time policy evaluation
12. Bias never becomes a per-response matrix verdict

### Policy-change lifecycle (mandatory)

```text
Draft version (immutable, content-hashed)
  → Static validation (schema, invariants, fail-stance floors, no-LLM nodes, locked R3)
  → Shadow replay over last N traces (actuator deltas, latency deltas, FP/FN where adjudicated)
  → Canary on bounded route slice / dual-emit
  → Auto-rollback if human-override rate > 3× baseline OR error budget breached
  → Named-principal human approval
  → Gradual promote
```

Enterprise day-one posture: routes start in **shadow**. Production enforcement is **earned** per route from counterfactual evidence (“would have held N, of which M were true positives”). This does **not** replace the Stage 1 live demo, which must still show the mock R3 gate holding the refund.

### Audit trail

Every decision writes to the append-only hash-chained ledger:

`principal · evidence fragment · claim verdict · matrix cell · actuator · policy_version · verifier_versions · latency · lane · route_id`

An auditor can reconstruct any actuator from ledger + policy version + frozen matrix.

---

## 10. Feedback, Metrics, FNR, Bias Posture

### Feedback & learning loops

The plane learns **operational parameters and evidence quality**. It does **not** become a trained safety model. **Feedback = calibration, not adaptation** — fixed mechanisms; rules, not weights; parameters are evidence-gated through shadow→canary→rollback. No online weight updates on the critical path.

#### What is learned (only via validated policy release)

| Channel | Recorded | May update after shadow→canary |
|---|---|---|
| Human override (structured reason code + packet) | Original actuator, human disposition, reason, policy version | Threshold calibration candidates; R-mapping defect review; error-budget / circuit-breaker sensitivity |
| Escalation adjudication | `confirmed` / `false_positive` / `source_error` / `acl_gap` / `model_error` | Per-route thresholds; source-governance alerts |
| Shadow counterfactual | Gated vs ungated disposition | Enforcement readiness; FNR/FP estimates |
| Graph-derived signals | Dead compute, rework, non-convergence, ACL gaps | Cost baselines; source hygiene tickets; workflow remediation |

NLI binder / claim extractor change only by **offline, versioned model releases**. Live feedback **never** updates weights online. Feedback may **propose** a policy version; it may not silently alter live enforcement.

#### What remains strictly rule-based (never learned)

- Default UNSUPPORTED  
- Entitlement / ACL comparison  
- Numeric / structural recomputation  
- Derived → recompute or UNKNOWN  
- Typed action interlocks  
- R calculation + exact R×S matrix lookup  
- Fail stance floors  
- Hard action gate  
- Evidence Ledger integrity + evidence-packet structure  
- Enforcement earn-out requirement  
- Locked R3 action classes  
- Stage 1 dual-action semantics  

#### What is never learned from

- Model confidence / logprobs / self-reported citations  
- User acceptance or “no complaint” silence as a safety label  
- Aggregate human approval of refunds/escalations as permission to loosen the boundary  
- Poisoned sources merely because they retrieve often  
- Prior assistant utterances copied into later context as evidence  
- LLM-as-judge opinions on sampled ambiguity  
- Unstructured overrides without reason codes  
- “Users usually accept this hallucination”  

A human override is **evaluation and calibration evidence**, not permission to rewrite the security boundary in real time.

#### Bias feedback loop (enterprise / proposal — never Stage 1 live actuator)

```text
decision-shaped route
  → async shadow replay
  → protected-attribute perturbation (non-protected inputs held fixed)
  → decision flip rate + confidence interval
  → flag when CI excludes zero
  → feed route policy / source / autonomy review
```

**Never:** `claim → bias verdict → matrix cell`.  
**Never:** a third Stage 1 live route for bias.

### Metrics, monitoring & trustworthiness reporting

The plane publishes **misses, not just catches**. Metrics are ledger-backed. Where trustworthy ground truth does not exist, fields stay **null / unavailable**. Emptiness is the credibility play. **No fabricated production numbers. No composite AI-safety score.**

#### Per-route FNR (published format)

**Method — stratified shadow audit (Adjudicator, Lane 3, off critical path):**

- 100% of `Block` / `Escalate` / `Edit` interventions  
- Random sample of `Pass` / `Pass + annotate` (oversample high-R, entitlement routes, recently changed policies)  
- Ground truth = human adjudication and/or expensive multi-verifier path  
- **Never** LLM-as-judge as authority; **never** on the critical path  

```text
FNR(route, policy_version, window) = FN / (TP + FN)
```

(Inverse-sampling weights; Wilson/bootstrap CI when measured.)

**Schema (values null until earned):**

```text
route_id
policy_version
evaluation_window
strata_definitions
sampled_count_per_stratum
false_negative_count
ground_truth_positive_count
FNR_estimate
CI_lower
CI_upper
ground_truth_method
measurement_status    # null | insufficient_sample | prototype_corpus | production_measured | stale
limitations
```

**Stage 1 live demo:** show the schema with **empty typed placeholders / null** only. Emptiness is the credibility play.  
**Enterprise claim shape (when earned):** *“On this route we catch \<measured\>% of ungrounded claims at 40 ms p50 — and here is the \<measured\>% we don’t.”* A numeric FNR appears only when `measurement_status` is earned (`production_measured` or explicitly labelled `prototype_corpus`). Never invent a production percentage. Never quote 40 ms as p95.

#### Other key metrics

| Metric | Definition | Why it matters |
|---|---|---|
| FP / intervention precision | Adjudicated non-Pass that were not gate-worthy | Avoidable friction |
| Override rate + reason codes | Overrides / eligible holds·edits·escalations | Alert fatigue; auto-rollback trigger |
| Dead compute | Exact backward walk from accepted SUPPORTED claims → spans → steps; any step grounding zero accepted claims is dead compute (exact, not estimated — e.g. “₹5 of ₹8 grounded nothing”) | Waste without estimation |
| Rework / non-convergence | Duplicate tools; declining evidence yield + stalled plan | Agent-loop cost |
| Latency by lane | p50/p95 Lane 1 / Lane 2 / action-gate; timeout→UNKNOWN | Budget honesty; R0/R1 targets ≤40/≤200 ms |
| Entitlement violations | By source, principal, `source×principal`; no-span PII vs ACL-excluded; ACL-missing gaps | Authorization failures made visible |
| Actuator / matrix-cell distribution | Pass / Pass+annotate / Edit / Escalate / Block by R + policy version | Makes the matrix operational |
| Circuit-breaker state | Gate-fail rate, autonomy tier, recovery | Prevents silent degradation |
| Evidence coverage | Share of claims with direct support / recompute / unknown / no-span | Source/retrieval quality |

#### Sceptical-stakeholder surface

1. Show **FNR schema first** — with nulls / `insufficient_sample` where unearned.  
2. Drill any material decision:

```text
Action
  → matrix cell
  → claim verdict + assertion form
  → bound or missing span
  → source_id / hash / ACL
  → principal entitlement
  → policy_version + verifier_versions
  → latency + lane
  → later adjudication (if any)
```

3. Show override-rate trend and auto-rollback evidence.

---

## 11. Complete Enterprise vs Prototype

| Layer | Full enterprise solution | Stage 1 live prototype (frozen — unreopened) | Proposal-only / phased |
|---|---|---|---|
| **Routes** | Support + knowledge + decision-support + agentic | **Exactly two:** refund + knowledge | Extra route packs |
| **Core plane** | SDK hook + proxy + recorder + ledger + binder + entitlement + interlock + matrix + surgical edit + evidence packet | Live dual-action refund + required principal-flip + ledger UI + **empty FNR placeholders** | Full multi-tenant HA / failover |
| **Governance** | Versioned DAG, geo overlays, shadow→canary→rollback, earn-out, circuit breaker | One default policy version applied | Full jurisdiction/industry packs |
| **Feedback** | Override adjudication, threshold calibration, shadow counterfactuals | Capture/describe only — not live calibration loops | Production-scale feedback pipeline |
| **Bias** | Async route-level counterfactual flip-rate + CI | **Not demonstrated** | Full bias measurement program |
| **Metrics** | Populated FNR/FP/override/dead-compute/latency with CIs when earned | **Empty typed FNR schema only** | Production FNR values |
| **Cost controls** | Dead compute, rework, non-convergence breaker | Brief backward walk only if it does not crowd dual-action | Full spend/ROI program |
| **Integrations** | Real IAM/ACL connectors, action adapters, human queue/SLA | Synthetic ACL + mock refund tool | Real payments, triage UI, compliance certification |
| **Scale** | Tens of thousands interactions/week (directional) | Single-node curated traces | Load/HA validation |
| **Data** | Enterprise connectors (challenge teams not expected to have proprietary data) | Synthetic enterprise-shaped corpora; no real PII | Broader corpora |

**Prototype = proof the control plane works** (R2S1).  
**Enterprise envelope = proof the control plane can be operated** (R2S2).  
**Pitch = both**, without softening either.

### Stage 1 exclusions remain locked

Third live decision-support/bias route · per-response bias verdicts · production load test as mechanism proof · real payments · real PII · live IAM remediation · LLM-as-judge primary verifier · confidence/global risk scores · open-web truth verification · generative full-answer rewrite · fabricated production FNR · “we fully solve hallucination/bias/privacy” · Lane-3 as critical-path demo · human triage SLA UI as architecture proof · model weights/logits/fine-tuning · collapsing dual-action into one response-level verdict · calling the R3 unsupported-categorical refund “blocked.”

---

## 12. Residual Technical Risks (architecture envelope)

### Risk 1 — False assurance on derived / multi-hop claims

**Why it remains:** Shallow entailment can mark a synthesized claim `SUPPORTED`. ARCHITECTURE names this the strongest residual technical risk. Multi-route expansion (especially decision-support) widens the surface.

**Exact mitigation:**

- Derived/aggregative claims **bypass ordinary NLI** → recompute from spans or return `UNKNOWN`
- `UNKNOWN` **never** becomes `SUPPORTED`
- Timeout → `UNKNOWN` → matrix + fail stance (never silent allow)
- Verifier model family decorrelated from generator
- Routes may declare claim patterns as `"derived"` (config escape hatch forcing recompute-or-UNKNOWN even if the extractor mistags them — overlay, not a new mechanism)
- FNR stratified by claim type publishes residual misses; unexpected SUPPORTED rates in the derived stratum trigger review
- Entitlement-violation rate **by source** is the operational detector for over-permissioned indexes (reporting signal to source owners)

### Risk 2 — Poisoned / wrong source evidence, or wrong / missing upstream ACLs

**Why it remains:** ControlPlane proves `claim ↔ captured evidence` and enforces **carried** ACLs. It does **not** prove the source is true and does **not** repair IAM.

**Exact mitigation:**

- Immutable `source_id` + content hash on every accepted binding
- Missing ACL recorded as gap; treated as **unentitled** on privileged routes
- Entitlement-violation rate **per source** = operational detector for over-permissioned indexes (reporting signal — not silent “AI remediation”)
- Quarantine / de-rank connectors via policy version
- Forensic ledger for rollback
- Boundary: defend the claim-to-evidence link; make IAM failures visible and measurable

### Risk 3 — Operational tuning → alert fatigue or liability (over-flag / under-flag), including R mis-mapping

**Why it remains:** Brief requires this tradeoff. Over-intervention → bypass. Under-intervention → liability. Mis-mapping payment to low R applies the wrong matrix row without “breaking” the matrix.

**Exact mitigation:**

- Shadow default before production enforcement; earn-out per route
- Blast-radius-priced verification depth (R0/R1 mostly Lane 1)
- R0/R1 fail-open with annotation; R2/R3 fail-closed/escalate
- Locked action classes → R3 at parse time
- No policy ships without replay + canary
- Auto-rollback on override rate > 3× baseline
- Circuit breaker downgrades autonomy
- Publish precision/override per route
- Hard interlock in the **action executor**, not only the UI

---

*End of Round 2 Final Hybrid Part A (Stages 1–2). Prototype freeze and enterprise envelope fully preserved. No competing mechanism introduced. Business buyers / roadmap continue in Part B.*
