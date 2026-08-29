# ControlPlane.ai — Round 2 Final
## Admission Control for AI That Acts

> Accenture Innovation Challenge 2026 · Round 2 · dense hybrid (R2S1–R2S4)  
> **ETERNAL:** Default = UNSUPPORTED · entitlement = set-membership (zero LLM) · exact R×S matrix · one graph · hard gate on actions · FNR as typed format · two-pending-actions (R1 Edit + R3 Escalate **held**, never “blocked”) · `UNKNOWN` never → `SUPPORTED` · bias async-only · refuse-to-claim (about *us*)  
> Sources: `docs/ARCHITECTURE.md` · `docs/reference/NARRATIVE.md` · `docs/reference/QA.md` · `docs/ps.md` · Stages 1–4 absorbed in this FINAL (locks deleted after merge).

| Official deliverable (`docs/ps.md`) | Artifact |
|---|---|
| **Detailed Business Proposal** | **This document** |
| **Working Prototype** | `controlplane/` · `examples/` · `tests/` |
| **Pitch Presentation** | R2S5.md + submission/ControlPlane_Round2_Pitch.pptx |

---

## Stage Check (compact)

| Stage | Locked into | Status |
|---|---|---|
| **R2S1** prototype scope | §§1–4 | **PASS** |
| **R2S2** enterprise envelope | §5 | **PASS** |
| **R2S3** build/demo | §6 | **PASS** |
| **R2S4** buyers/value/rollout | §§7–11 | **PASS** |

| # | Eternal invariant | Status |
|---|---|---|
| 1 | Default = `UNSUPPORTED` | **PASS** |
| 2 | Entitlement = `span.acl ⊆ principal.clearance`; zero LLM | **PASS** |
| 3 | Exact R×S matrix; never redrawn; no route parameter | **PASS** |
| 4 | One graph: `STEP → SPAN → CLAIM → ACTION` | **PASS** |
| 5 | Hard gate on **actions**, not tokens | **PASS** |
| 6 | Dual-action: R1 **Edit** + R3 **Escalate** (**held**, never “blocked”) | **PASS** |
| 7 | `UNKNOWN` never → `SUPPORTED` | **PASS** |
| 8 | FNR as typed format; empty until earned | **PASS** |
| 9 | Bias = async route-level only (never live matrix cell) | **PASS** |
| 10 | Refuse-to-claim list (about *us*) | **PASS** |

---

## 1. Problem

Enterprises moved from AI that **answers** to AI that **acts**. Failure changed category: bad paragraph → **executed transaction**.

> *“Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.”*

**Clause 7.2 does not exist.** Failure is *absence* of evidence, not conflict. Filters pass it. Confidence can read 0.94. Money moved Tuesday, found Friday. If ungated, **the company wrongly pays out ₹1,84,000** — the customer did not lose money.

This is not “hallucination” as the market frames it. It is an **authorisation** problem: an unproven claim authorized an irreversible action. Solution is not better text scoring — it is **admission control**.

> *The system didn’t fail. It was never asked to prove anything.*  
> *Everyone watches the exit. Nobody records the entrance.*

Three structural reasons existing approaches fail:

1. **Inspect output, not context contract.** Without recording what the model was *given*, verification is unfalsifiable opinion. With it, verification is set-membership: *which span proves this claim?*
2. **Score the response, not the action.** Groundedness 0.82 means the same on a draft and a wire transfer. One threshold cannot price both.
3. **Identity-blind.** The common enterprise incident is a **correct answer to the wrong person**. No output-only inspector carries caller identity into verification.

| Approach | Why it fails here |
|---|---|
| Post-hoc observability (LangSmith, Arize, …) | Traces *after* commit — audit trail, not interlock |
| LLM-as-judge / wrappers | Opinion, identity-blind, too slow for commit, cannot state own error rate |
| Static guardrails | Miss lexically clean fabrications and ACL failures |
| RAG groundedness | Averages (one wrong figure drowns); action-blind; **retrieval ≠ permission** |
| Confidence / logprob | Named failure is *confidently* wrong |
| Composite risk scores | Three owners/costs collapsed into one number that maps to no actuator |

Failure modes this plane addresses: (1) categorical claim with **no provenance** authorizing R3; (2) claim bound to evidence the **caller may not read**; (3) **two pending actions, different blast radii** on one response; (4) no real-time ground truth → **invert burden of proof**.

| Overlap (brief) | Treatment on one graph |
|---|---|
| Fabricated personal detail, no span | Unsupported + no-span PII/secret shape; stays UNSUPPORTED |
| Correct HR fact, ACL excludes caller | Entitlement violation — independent of semantic correctness |
| Absent policy clause authorizing refund | Unsupported categorical on R3 → Escalate (**held**) |
| Bias on decision-shaped outputs | **Not** a per-response verdict; async flip-rate + CI |

Multi-turn = more STEPs on the **same session ledger** — not a separate product. Prior assistant text is never evidence by reappearance. Unproven turn-1 claim used to authorize R3 in turn N remains unproven. Tool results enter as SPANs, not automatic authorization. Compounding risk = same unproven claim reaching higher R — already covered by the frozen graph.

Enterprise question is not “how do we score AI responses?” It is: *What evidence is required before a claim may authorize a specific action, for this caller, on this route?*

Buyer question a sceptic can answer without our slide: *What consequential actions does this route perform today, what is the loss if one is wrong, and what fraction can sit behind an earned admission boundary?*

---

## 2. Solution

ControlPlane.ai is an **admission-control layer** (firewall / transaction validator class — not observability, not a second model). Deployed as thin context-assembly SDK hook + OpenAI-compatible reverse proxy. No weights, logits, or fine-tuning. Integration cost is real — **and is the moat**.

```text
AI output → claim proof → entitlement → R×S → action admitted / edited / escalated / held
```

One primitive, three reads:

```text
STEP ──produces──▶ SPAN ──binds──▶ CLAIM ──authorizes──▶ ACTION
```

Performance reads forward. Cost reads backward (exact dead compute). Responsibility reads labels. One structure — not three detectors.

**Load-bearing primitives**

1. **Provenance outside the model** at context assembly — keystone: `source_id · ACL · content_hash · offsets` + calling principal. Model has **no write path**. Binding computed by the plane; model-emitted citations are not evidence; no open-web rescue.
2. **Default = UNSUPPORTED.** Earn `SUPPORTED` via recomputation or binding. Unsupported ≠ low confidence — **unproven**. `UNKNOWN` never → `SUPPORTED`.
3. **Claim-type routing.** Numeric/date/ID → recompute. Textual → bind (entailment, not string match). Derived/multi-hop → recompute or `UNKNOWN`.
4. **Entitlement = set-membership** (`CALLER → CLAIM → SPAN → SOURCE ACL`; `span.acl ⊆ principal.clearance`). Zero LLM. Lane 1 always on. Semantically correct + unauthorized still fails. **Most differentiated mechanism** — competitors cannot replicate without carrying identity into verification.
5. **Exact R×S matrix per pending action.** Disposition = **worst claim for that action — never an average**. `R = irreversibility × audience × data class × autonomy`. Action Interlock = sole final decider; pure rule engine.
6. **Hard gate on actions, not tokens.** Text hold-back ~150–300 ms. Speculative verification OK; **speculative release forbidden**.
7. **Escalate → evidence packet** (claim, spans, verdict, diff). Surgical Edit only (strip or one constrained regen; re-gate; second fail → Escalate).
8. **Publish own per-route FNR as typed format** — empty until earned. Emptiness is the credibility play.

**Ungrounded / parametric:** when no provenance spans exist for a route, it is declared ungrounded by construction; such claims **cannot authorize any action** regardless of blast radius. *We don’t claim to verify what we were never given. We claim what we were never given cannot authorize an action.*

**Refuse-to-claim (about *us*, not competitors)**

1. **“We eliminate hallucinations.”** False if shipped. Narrower claim: ungrounded claims cannot authorise actions, and we report what we miss.
2. **“Zero integration, drop it in.”** We hook context assembly — real work, exact reason the design works. Scope = one SDK hook + OpenAI-compatible proxy (days on a standard retrieval stack, not quarters) — never sold as drop-in. Integration cost is the moat.
3. **“Zero added latency.”** We never make the model feel slow; we make the action wait. Quote only **≤40 ms p50 / ≤200 ms p95** — never 40 as p95.
4. **“One accuracy number across failure modes.”** Hallucination, leakage, and bias have different mathematics, error costs, and owners.

**Operating claim:** ControlPlane does not promise “safe” or “truthful” AI. It makes an unproven or unauthorized claim unable to authorize an action beyond the route’s admitted boundary — and publishes what the plane missed.

---

## 3. Matrix

Exact frozen 16-cell R×S — transcribed, never redrawn, **no route parameter**:

|  | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** | **Block** | **Escalate** | **Escalate** | **Escalate** |
| **R2** | **Block** | **Edit** | **Edit** | **Escalate** |
| **R1** | **Edit** | **Edit** | **Pass + annotate** | **Pass + annotate** |
| **R0** | **Pass + annotate** | **Pass + annotate** | **Pass** | **Pass** |

**R tiers:** R0 = internal draft · R1 = user-visible read-only · R2 = reversible write / external send · R3 = irreversible or regulated (payment, deletion, publication, regulated advice).  
**Actuators (exact):** Block · Edit · Escalate · Pass / Pass + annotate. Forbidden inventions: `STREAM`, `Kill Span`, `Hold & Re-verify`, `Redact & Flag`, `COMMIT BLOCKED` as R3 unsupported-categorical label. Autonomy downgrade / circuit breaker = spoken controls, not inventable demo labels.

**Fail stance ≠ matrix:** Matrix answers “evidence arrived and is bad → actuator?” Fail stance answers “evidence did not arrive in time?” Floors: R0/R1 fail **open + annotate**; R2/R3 fail **closed or escalate**. Universal fail-open forbidden.

**Centrepiece cells (simultaneous on one refund response):**

| Pending action | Tier | Finding | Cell | Actuator |
|---|---|---|---|---|
| Show text | **R1** | Unentitled span grounds a claim (C3) | R1 × entitlement | **Edit** |
| Issue refund | **R3** | Clause 7.2 has no span (C2) | R3 × unsupported-categorical | **Escalate** — **held** with packet |

Never collapse into one response-level verdict. **Never say “blocked” about the refund.** Same unsupported+categorical claim yields R1→Edit on a draft and R3→Escalate on a payment — proof scales with consequence; the matrix is not renamed severity.

---

## 4. Prototype

Exactly **two** live routes. Third live decision-support / bias route **refused**. Bias = proposal measurement only. Scope tension (resolved): brief names decision-support and bias; architecture defines bias as distributional/async — both stay in the **enterprise envelope**, never contaminate the live core.

| Route | Dominant R | Mechanism proved | Live? |
|---|---|---|---|
| **A. Refund agent** | R1 text + R3 refund | Two-pending-actions | **YES** |
| **B. Knowledge assistant** | R0/R1 | Provenance + entitlement flip | **YES** |
| Decision-support / bias | — | Async counterfactual | **NO** — envelope only |

**Refund risk signature:** absent clause · numeric/ID error · entitlement leak into customer text · irreversible payment on same response · no real-time ground truth. Latency: R0/R1 text **≤40 ms p50 / ≤200 ms p95** (never quote 40 as p95); action verify amortised in tool RTT; text hold-back ~150–300 ms. Speculative verification OK; speculative release forbidden.

**Knowledge:** correct-but-unauthorized disclosure; fabrication; ACL-excluded span. Demo stages ACL-excluded → R1 × entitlement = Edit (not no-span PII → Block). Plane enforces carried ACLs — does **not** repair IAM. Authorization path: `CALLER → CLAIM → SPAN → SOURCE ACL` — set-membership, **zero LLM**.

**Why this pair:** Refund proves one graph, two actuators, hard gate, surgical edit, packet. Knowledge proves graph ≠ RAG groundedness: same claim, different principal → different outcome (RAG averages; ControlPlane prices worst claim per pending action). Together: *is this claim proven?* and *is this caller entitled to that proof?* A third live bias route adds async measurement without strengthening the dual-action centrepiece.

**Assumptions (load-bearing):** synthetic enterprise-shaped corpora only — no real PII; every span carries source/ACL/hash/offsets; generator via OpenAI-compatible API only (no weights/logits); decision policy = pure rule engine; traffic directional tens of thousands/week (prototype = curated single-node — no throughput claim); FNR null without trustworthy ground truth; corpus poisoning outside truth guarantee (hash makes source auditable, not factually true); DPDPA/GDPR as config packs — not certification.

### Boundary — in

| Prove | How |
|---|---|
| Provenance outside model | Spans before claims; model cannot author |
| One typed ledger | `STEP → SPAN → CLAIM → ACTION` |
| Default UNSUPPORTED | Earn via bind/recompute; UNKNOWN never → SUPPORTED |
| Claim-type routing | Numeric recompute; textual entailment; derived → UNKNOWN |
| Deterministic entitlement | Set-membership; zero LLM |
| Exact 16-cell matrix | Per pending action; worst-claim weighting |
| Dual-action centrepiece | R1 Edit + R3 Escalate held |
| Hard action gate | Mock refund `committed:false` while Escalate |
| Surgical Edit + evidence packet | Strip/regen once; packet = claim+spans+verdict+diff |
| Empty FNR schema | Typed nulls only — no fabricated % |
| Principal flip | Change only caller → outcome flips |
| Per-claim surface | Verified / Uncertain / Blocked; refund action = Held/Escalate |
| Ungrounded / parametric | No provenance → cannot authorize any action |
| Live compute | Binding/entitlement/interlock visible (~20–80 ms) |

### Boundary — out

Third live bias route · per-response bias · production load as mechanism proof · real payments/PII · live IAM repair · LLM-as-judge primary · confidence/risk scores · open-web truth · generative rewrite · fabricated FNR · Lane-3 on critical path · triage SLA UI · weights/logits · collapsing dual-action · calling refund “blocked.”

### Measured results (this build)

All numbers are produced by `make eval` and `make bench` and regenerate on every run — they are measured, never asserted. The capability ledger and per-route Wilson CIs live in the generated README PDF (`submission/ControlPlane_Round2_README.pdf`) and `evals/last_run.json`.

**This build earns the FNR on a 168-case self-authored corpus.** The committed run reports:

- **Ungrounded FNR ≤ 4.0%** (95% Wilson upper bound; n=93 ungrounded claims; point estimate ≈1.1%).
  We publish the upper bound — the interval is the honest claim, not the point estimate.
- **Passable-action FPR ≤ 15.5%** (95% Wilson upper bound; n=21 passable claims).
- **Hard-negative hold rate 64% [0.51, 0.76].** 53/168 cases are hard negatives (31.7%, above the
  20% floor). We over-flag — that is our named next milestone. Clean strata hold 0/13.
- **One published miss:** `struct-miss-000` — a response citing "Clause 4.1 permits this refund"
  where the span only says clause 4.1 *covers shipping delays*. Structural symbol lookup matches →
  SUPPORTED → low-tier action slips through. We show the judge exactly which case we got wrong.
- **No production proof.** Production FNR is unknown until shadow replay over live traffic
  (ARCHITECTURE §7, §12). The honest claim: "on this self-authored corpus we miss ≤4.0% of ungrounded
  low-tier claims (95% Wilson upper bound; n=93); production is unknown."
- **Refuse-to-claim:** we do not eliminate hallucinations; we do not claim drop-in integration; we do
  not claim zero added latency; we do not claim one accuracy number; we do not fill FNR with fabricated
  percentages.

Shape of the published claim (ARCHITECTURE §7): we hold **X%** of ungrounded responses at **Y ms** p50 —
and here is the **Z%** we don't, with a Wilson interval.

---

## 5. Enterprise Envelope

Same plane on every route. Runtime:

```text
App/Agent → Context SDK Hook (SPAN: source·ACL·hash·offsets)
         → OpenAI-compatible proxy
         → Evidence Ledger STEP→SPAN→CLAIM→ACTION
         → Action Interlock  exact R×S = f(R,S)  [no route param]
         → Pass / Pass+annotate / Edit / Escalate / Block
         → Text hold-back · Action commit boundary
```

**Shared (not soft-configurable):** Provenance Recorder · Ledger · typed claims · proof paths · verdict set · Entitlement Auditor · Interlock · exact matrix · fail-stance floors · hard gate · surgical edit · packet · claim-level surface · FNR schema · Lane 1 always on.

**RoutePolicy one-liner (configures budget, not truth):**

```text
RoutePolicy { route_id · tenant · use_case · provenance_scope · action_grammar
  · action_to_R_mapping (locked R3: payment|deletion|publication|regulated_advice)
  · verification_profile · fail_stance_by_R (may NOT loosen R2/R3 to fail-open)
  · enforcement_mode shadow|canary|enforce · error_budget · escalation_target
  · sampling_policy · geography_overlay (additive only) · latency_budget ≤40/≤200 }
```

Routes may change actions, R-mapping (except locked classes), Lane-2 budget, shadow/enforce, sampling, additive geo. Routes may **not** change: UNSUPPORTED default · entitlement · matrix cells · hard gate location · UNKNOWN→SUPPORTED · composite scores · Stage 1 dual-action scope. Low-consequence traffic gets **less verification budget and a proportionate actuator — not weaker truth semantics**.

| Route profile | Dominant R | Lane posture | Enforcement |
|---|---|---|---|
| Customer-support refund | R1+R3 simultaneous | Lane 1 text; Lane 1+2 + interlock for R3 | Shadow/canary before enforce; **demo still shows hard gate on mock refund** |
| Internal knowledge | R0/R1 | Lane 1 dominant; ACL always inline | Enforce after shadow evidence |
| Decision-support | R0/R1 memo + R2/R3 action | Lane 2 derived; Lane 3 async bias | Action gate when earned; bias always async — **not Stage 1 live** |

| Lane | Runs | Path |
|---|---|---|
| **1** | Span membership, ACL, arithmetic, typed interlocks, PII shapes | Inline; always on; no LLM |
| **2** | NLI/binding for flagged textual / high-R | Near-line; timeout → UNKNOWN |
| **3** | Semantic-entropy, bias replay, calibration, shadow audit | Async; **never** critical path |

**Governance:** versioned DAG of `(signal, threshold, action, latency_budget)`; decision time = pure rule engine. Hierarchy narrows only: Enterprise baseline → geo overlay (additive) → tenant → route → action class. Overlays cannot loosen frozen invariants. Global parse-time invariants include: default UNSUPPORTED · UNKNOWN→SUPPORTED forbidden · entitlement always on · Lane 1 cannot disable · locked R3 classes · matrix immutable · R2/R3 fail closed/escalate · hard gate on actions · no composite score · no LLM at decision · bias never a matrix verdict · Stage 1 scope unreopened.

**Policy lifecycle:** Draft (hashed) → static validation → shadow replay → canary → auto-rollback if override >3× baseline or error budget breached → named-principal approval → promote. Day-one = **shadow**. Production enforce is **earned**.

**Audit:** `principal · evidence · claim verdict · matrix cell · actuator · policy_version · verifier_versions · latency · lane · route_id` — reconstructible from ledger + policy + frozen matrix.

**Feedback = calibration, not adaptation.** Learn thresholds/error-budget candidates via shadow→canary. Never learn: confidence/logprobs · silence-as-safety · aggregate override as permission to loosen · poisoned sources · prior assistant text as evidence · LLM-as-judge opinions · online weight updates. Override = evaluation evidence, not real-time security rewrite.

**FNR schema (null until earned):**

```text
route_id · policy_version · evaluation_window · strata_definitions
· sampled_count_per_stratum · false_negative_count · ground_truth_positive_count
· FNR_estimate · CI_lower · CI_upper · ground_truth_method
· measurement_status  # null|insufficient_sample|prototype_corpus|production_measured|stale
· limitations
```

Method: stratified shadow audit — 100% of Block/Escalate/Edit + sample of Pass; ground truth = human / expensive multi-verifier — **never** LLM-as-judge. Claim shape when earned: *“On this route we catch \<measured\>% of ungrounded claims at 40 ms p50 — and here is the \<measured\>% we don’t.”*

**Bias (brief requirement, frozen stance):** async route-level counterfactual flip-rate + CI; flag when CI excludes zero. **Never** `claim → bias verdict → matrix`. Never dropped; never a Stage 1 live route.

| Layer | Enterprise | Stage 1 live | Proposal-only |
|---|---|---|---|
| Routes | Support + knowledge + decision + agentic | **Exactly two** | Extra packs |
| Core | Full plane | Dual-action + flip + ledger + empty FNR | Multi-tenant HA |
| Bias / FNR values | Async + measured when earned | Absent / null placeholders | Full programs |
| Scale | Tens of thousands/week (directional) | Curated single-node traces | Load/HA |

**Prototype = proof the plane works. Envelope = proof the plane can be operated. Pitch = both.** Envelope residual risks (architecture): (1) derived/multi-hop false SUPPORTED → recompute-or-UNKNOWN + stratified FNR; (2) poisoned sources / wrong ACLs → hash + entitlement-by-source detector — defend claim↔evidence link, not source truth; (3) over/under-flag + R mis-mapping → shadow earn-out, locked R3, interlock in executor. Stage 2 IS configuration/governance/lifecycle around the primitive. Stage 2 IS NOT a second mechanism, redrawn matrix, live bias product, or trained safety model.

---

## 6. Build & Demo

### Corpora (essentials — no breadth)

| Source | ACL | Purpose |
|---|---|---|
| `AGR-VENDOR-v3` | agent-readable | Clauses 1–6 only; **no clause 7.2 anywhere** |
| `ORD-1023` | `refund_agent` | amount=184000 INR — C1 SUPPORTED |
| `FIN-INTERNAL-NOTE` | `internal_analyst` (excludes `agent_refund_7`) | C3 entitlement → Edit |
| `INJECT-NOTICE` | untrusted | Cannot author provenance |
| `HR-COMP-L6` | `hr_partner` | Principal-flip span |

Principals: `agent_refund_7` · `analyst_01` · `hr_partner_01`. Canonical fixture: *“Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.”* + one FIN-INTERNAL sentence. Span contract: `span_id · source_id · ACL · content_hash · offsets · text · step_id`.

| Claim | Finding | Feeds |
|---|---|---|
| **C1** amount/order numeric | Binds `ORD-1023` → **SUPPORTED** | Proof works |
| **C2** “under clause 7.2 …” categorical | **No span** → stays **UNSUPPORTED** (absence ≠ contradiction) | `refund.execute` → R3 **Escalate** |
| **C3** grounded on FIN-INTERNAL | ACL excludes caller → **entitlement** | `text.show` → R1 **Edit** |

All three born UNSUPPORTED. Optional polish only after dual-action+flip green: paraphrase entailment · parametric ungrounded · numeric near-miss — cut polish before cutting dual-action.

### Components

Real: Recorder · Ledger · Claim Extractor (fixture) · Numeric Recomputer · Entitlement Auditor · Interlock · Surgical Editor · Packet · Hold-back · Policy loader · Principal switch · FNR renderer · Trace Console · harness. Thin mock: generator stub · refund executor (`REFUND HELD` / `committed:false` — never `COMMIT BLOCKED`) · NLI labels. No LLM at decision time. No confidence field in the decision path.

### Demo order (≤8 min; UI ≥60% ledger)

**Governing test:** if removing the graph leaves the demo looking the same, scope failed. Open on held transaction — never a risk statement. Core crisis ≤90s. First spoken sentence about failure contains **claim**, not response.

| Must show | Must NOT show |
|---|---|
| Ledger ≥60%; spans before claims; matrix cells before actuators | Composite risk/confidence scores |
| Action Gate cold-open with `committed` boolean | “Response blocked” / `COMMIT BLOCKED` for R3 unsupported-categorical |
| Per-claim Verified/Uncertain/Blocked; refund = Held/Escalate | LLM-as-judge pane · open-web lookup |
| Evidence packet on every Escalate; empty FNR | Interlock bypass override · third-route chrome · bias widget · chatbot-majority |

1. **Cold open gate:** `refund.execute` `{amount:184000, reason:"clause 7.2", order_id:"ORD-1023"}` · R3 · **HELD — ESCALATE** · `executed:false`
2. Expand ledger — spans with source·ACL·hash **before** claim verdicts
3. C1 SUPPORTED · C2 no span UNSUPPORTED · C3 entitlement violation
4. Highlight cells **before** actuators: `text.show` → R1×entitlement→**Edit**; `refund.execute` → R3×unsupported-categorical→**Escalate**
5. Surgical Edit strips C3; refund stays held; packet opens for C2 (claim, candidate spans `[]`, verdict, diff)
6. Executor proves not committed — company does **not** wrongly pay out in the gated demo
7. Empty FNR schema visible (null placeholders only)
8. **Principal flip (≤2 min):** `analyst_01` → Edit; flip only to `hr_partner_01` → Pass. Zero LLM.

Optional third beat (cut first): same unsupported claim as R1 vs R3 → actuator changes solely because R changed — or numeric `14` vs span `11` → R1 Edit.

Voice: authorise · admit · prove · bind · refuse · hold · escalate · gate — not monitor · detect · observe · watch · guard · trust score · risk score.

### Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python3 -m pytest tests/ -v
python3 examples/refund_trace_demo.py
python3 examples/knowledge_flip_demo.py
```

| Command | Proves |
|---|---|
| `pytest tests/ -v` | Matrix, entitlement, UNSUPPORTED default, hard gate, held≠blocked, R2S1 criteria on fixtures |
| `refund_trace_demo.py` | Dual-action: Edit + Escalate held; never collapsed; never “blocked” |
| `knowledge_flip_demo.py` | Same span/claim; outcome flips with clearance only |

---

## 7. Buyers

### Target users

Beachhead = high-consequence routes (refund-class R3 + mixed-governance knowledge) — not “all enterprise AI safety.”

| Role | Who | Buys / operates |
|---|---|---|
| **Economic buyer** | Ops / CS / CHRO / CRO / CFO / CISO / Risk | Action authorisation + per-route error budgets. Responds to: *unproven claim cannot authorise an action.* Not: *we detect 95% of hallucinations.* |
| **Technical buyer** | Platform / ML infra / Identity | SDK hook + proxy + adapters; wants graph, not second black box; ≤40/≤200 ms |
| **App / agent team** | Route owners | Wire adapters; no app rewrite |
| **Day-to-day actor** | Support / knowledge worker | Sees Verified/Uncertain/Blocked per claim; Held/Escalate on action — never enforces |
| **Operator / governor** | Route owners, SRE, Risk Ops | Shadow/canary/enforce; rollback; circuit breaker; ledger reconstruct |
| **Escalation reviewer** | Risk / ops | Evidence packet, not bare alert |
| **Compliance / audit** | Legal / DPO / audit | Influences via reconstructible trail |

Split that matters: who **pays when it fails** ≠ who **runs it** ≠ who **types the answer**. Interlock enforces; plane publishes miss rate.

---

## 8. Impact Logic

### Business case

No fabricated ROI. No “99%.” No net-savings slide. Value = **mechanism → consequence**; buyer fills middle terms. Tail risk, not average case.

```text
Exposure = freq(consequential AI actions) × P(unproven/unauthorized claim) × loss/wrong action
```

| Lever | Mechanism → consequence |
|---|---|
| **A — Avoided wrong actions** (primary) | R3 Escalate held (`executed:false`) is structural escape. Value = held true-positives × buyer’s direct cost of that action class; residual sized by published FNR. Artifact: attempted commit · matrix cell · gap · `committed=false`. |
| **B — Blast-radius pricing** | Lane 1 majority volume; expensive proof where R justifies. Same verdict annotates a draft and holds a payment. Answers brief’s one-size-fits-all latency problem. |
| **C — Exact dead compute** | Backward walk: STEP grounding zero accepted claims = waste (exact). Observability measures spend; this measures waste. Expose number; enterprise prices own traffic — no % saved on slide. |
| **D — Alert fatigue without lowering gate** | Matrix prices actuators; R0/R1 unsupported+hedged → Pass+annotate. Shadow earn-out. Metrics: overrides · gate-fail · edit/escalation **per route**. |
| **E — Auditability** | Hash-chained ledger + versioned policy. Reconstruct: action → cell → verdict → span → source/hash/ACL → principal → policy → latency. Regulator answer = pointer. |
| **E2 — Unauthorized disclosure** | ACL-excluded span caught when semantically correct. Does not fix IAM — stops IAM gaps being **silently bypassed by a model**. |
| **F — Publish misses** | Per-route FNR typed format; null until earned. Conversation: route · population · miss · CI — not “trust our safety score.” |
| **G — Earned autonomy** (secondary) | Shadow → enforce only where counterfactuals justify. More AI action **after** evidence — never lead claim. |

---

## 9. Roadmap

Earn-out, not feature calendar. Enforcement earned, not switched on. Day-one = shadow. Misses published every phase.

| Phase | What | Exit |
|---|---|---|
| **0 — Prototype** | Two live routes; synthetic corpora; ledger ≥60%; empty FNR | All R2S1/R2S3 criteria; dual-action crisis ≤90s |
| **1 — Shadow production** | 1–2 real routes matching pattern; dual-emit; no production hold yet. Determinism works day one; statistics earn thresholds | Counterfactuals enough to open canary |
| **2 — Canary R0/R1** | Full policy lifecycle; enforce Edit/Pass+annotate on read-only | Tolerable ops; no material edit regression |
| **3 — Limited R2/R3 enforce** | Hard-gate selected actions; packets to humans; fill FNR only with trustworthy GT; locked R3 at parse | Buyer FNR/FP/override thresholds; `committed=false` on held TPs |
| **4 — Broader envelope** | More routes (decision-support **template**); additive geo; async bias; dead-compute FinOps; circuit breaker; fail stance tier-owned | Multi-route without second detector |

---

## 10. Risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| False assurance on derived/multi-hop | Shallow entailment → false SUPPORTED — worse than no plane | Bypass NLI → recompute or UNKNOWN; UNKNOWN never SUPPORTED; timeout→matrix; FNR by claim type |
| Poisoned sources / wrong ACLs | Plane proves claim↔evidence + carried ACLs — not source truth / not IAM repair | Immutable source+hash; missing ACL→unentitled; entitlement-violation **by source**; quarantine via policy |
| Prompt injection / model-declared bindings | Invent evidence edges | Plane computes bindings; model cannot author spans; disposition = rule engine |
| Over-flag → bypass; under-flag → liability | Classic guardrail death | Shadow default; blast-radius pricing; fail-stance floors; override>3× rollback; circuit breaker |
| R mis-mapping (payment as R1) | Wrong row without “breaking” matrix | Locked R3 at parse; interlock in **executor**, not only UI |
| Integration / provenance gaps | Incomplete spans → false UNSUPPORTED | Honest hook+proxy; evidence coverage measured; conservative high-R |
| Plane as SPOF | Outage / load-induced bypass | Tier-owned fail stance; universal fail-open forbidden |
| Feedback misuse / weight access | Train on overrides; require logits | API-only; feedback→policy candidates only; calibration ≠ trained judge |
| Switch-off after a quarter | Layers that interrupt low-blast text die | Gate on actions; majority Pass+annotate; earn-out before trust; integration cost stated as moat |
| Pattern-match as RAG/safety dashboard | Differentiation dismissed | Open on held ₹1,84,000; ledger majority UI; ban monitor/detect/risk-score vocabulary |

---

## 11. Differentiation

| ControlPlane | Everyone else |
|---|---|
| Provenance outside model at context assembly | Inspect output; treat model citations as evidence |
| Default = UNSUPPORTED | Default allow; flag what looks wrong |
| Entitlement = ACL set-membership | Identity-blind scorers |
| One graph, three reads | Three bolted tools |
| Exact R×S per pending action | Composite risk / confidence |
| Hard gate on actions | Gate on text/tokens |
| Publish per-route FNR (misses) | Publish precision (bother rate) |

**Ordered contrast**

1. **vs observability** — post-hoc traces after harm. Observation without commit control is audit trail, not architecture. ControlPlane records entrance and interlocks commit; same graph yields exact dead compute.
2. **vs LLM-as-judge / static guardrails** — *does this look right?* vs *which span proves it?* Decision time = pure rule engine. Entitlement = identity, not classification. Default UNSUPPORTED is posture, not threshold tweak.
3. **vs RAG groundedness** — closest cousin, still short: retrieval-only, averages, action-blind. ControlPlane binds full provenance, prices **worst claim per action**, same unsupported claim → R1 Edit vs R3 Escalate. **Retrieval ≠ permission. Proof scales with consequence.**

**Closer:** Competitors publish precision. ControlPlane publishes misses and **refuses** to claim it eliminates hallucination/bias/privacy. Almost none disclaim themselves. Plane audited by the standard it enforces.

---

## 12. Fidelity + Content Laws

| Invariant | Status |
|---|---|
| Default = UNSUPPORTED | Untouched |
| Entitlement / ACL set-membership; zero LLM | Untouched |
| Exact R×S; no route parameter | Untouched |
| Hard gate on actions; speculative release forbidden | Untouched |
| Dual-action R1 Edit + R3 Escalate **held** (never “blocked”) | Untouched |
| FNR typed format; empty until earned | Untouched |
| `UNKNOWN` never → `SUPPORTED` | Untouched |
| No LLM-as-judge / confidence as primary path | Untouched |
| Bias = async route-level only | Untouched |
| Refuse-to-claim (about *us*) | Untouched |
| Exactly two Stage 1 live routes | Untouched |
| Latency ≤40 ms p50 / ≤200 ms p95 | Untouched |
| Surgical edit · evidence packet · Lane 1 always on · locked R3 | Untouched |

| Law | Exact rule |
|---|---|
| **Clause 7.2** | Does **not** exist. Absence ≠ conflict. Never “caps/denies/doesn’t cover.” → Unsupported+categorical → **Escalate**, not Block. |
| **Held ≠ blocked** | Refund **held and escalated with the evidence packet** — never “blocked.” |
| **Who pays** | **Company wrongly pays out.** Customer did not lose money. |
| **Dual action** | Text → R1×entitlement→Edit (C3). Refund → R3×unsupported-categorical→Escalate (C2). Both simultaneous. |
| **Latency** | ≤40 ms p50 / ≤200 ms p95. Never quote 40 as p95. Speculative verify OK; speculative release forbidden. Hold-back ~150–300 ms. |
| **Refuse-to-claim** | No: eliminate hallucinations · zero integration · zero added latency · one accuracy number. |

**Closing spine:** AI can act → unproven claim must not authorize → provenance outside model → Default UNSUPPORTED → entitlement set-membership → R×S prices by consequence → hard gate on commit → publish misses.

Vocabulary: authorise · admit · prove · bind · refuse · hold · escalate · gate — not monitor · detect · observe · watch · guard · trust score · risk score · “responsible AI” as virtue.

*Once you accept that an AI response is a set of claims requesting permission to act, you must capture provenance outside the model, invert the burden of proof, carry identity into verification, and gate the commit path. Any softer design is a different product.*

---

## Appendix — Official brief coverage

| Brief requirement (`docs/ps.md`) | Where | Freeze stance |
|---|---|---|
| Different risk/latency by use case | §5 RoutePolicy + profiles | Same graph/matrix; config only |
| Overlapping bias/hallucination/privacy | §§1, 5 | Not one classifier |
| No reliable real-time ground truth | §§1–2; FNR null | Honesty over bluff |
| Over-/under-flag tradeoff | §§5, 8–10 | Shadow earn-out; blast-radius pricing |
| Multi-turn / agents that act | §§1, 5 session ledger | No separate product |
| Evolving geo/industry regulation | §5 additive overlays | Cannot loosen matrix |
| API-only foundation models | §§2, 6 | No weights/logits |
| Detection options (AI-as-judge, confidence) | §§2, 11 | **Reject** as primary |
| Decision logic allow/edit/flag/block | §3 matrix | Transcribed |
| Architecture placement | §§2, 5–6 | Pre-commit interlock + hold-back |
| Governance / audit | §5 | Zero LLM at decision time |
| Feedback loops | §5 | Calibration, not trained model |
| Metrics / FP/FN / trustworthiness | §§5, 8F | Publish misses as format |
| Multi use-case, tens of thousands/week, mixed governance | §§4–5 | Directional; prototype simulated |
| Deliverables: proposal + prototype + pitch | Header map | Proposal=this · Prototype=`controlplane/` · Pitch=next |

---

*End of ControlPlane.ai Round 2 Dense Final Hybrid — Stage Check PASS. Pitch from this file + live demo.*
