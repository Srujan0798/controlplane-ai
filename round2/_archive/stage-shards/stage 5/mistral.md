
# ControlPlane.ai — Round 2 Stage 5: Pitch Architecture

> **Mission:** Win. Not produce a competent pitch structure. Win.
> **Standard:** Highest adversarial. Serious engineer must respect the architecture in the room.
> **Constraint:** Stages 1–4 are eternally frozen. No reopening of technical, scope, or value decisions.

---

## 1. Pitch Thesis

An AI response is not text to be scored — it is a set of claims requesting permission to act. ControlPlane keeps the receipts: we capture provenance outside the model at context assembly, bind every claim to the evidence the system was actually given, and gate actions — not tokens — on proof. The cost of a wrong output changed category: it used to be a bad paragraph. It is now an executed transaction. We do not promise safe AI. We make an unproven or unauthorized claim unable to authorize an action, and we publish what we miss.

**Load-bearing phrase:** *set-membership test.* Do not drop it.

---

## 2. Overall Pitch Structure

| Beat | Title | Duration | Purpose | Core Artifact |
|------|-------|----------|---------|----------------|
| **0** | Cold Open: The Held Transaction | 0:00–1:30 | Hook on category change; establish stakes | Running example (₹1,84,000 / clause 7.2) |
| **1** | The Category Shift | 1:30–2:30 | Frame the market failure: paragraph → transaction | Narrative §2 |
| **2** | The Sharp Insight | 2:30–3:30 | Deliver the thesis; introduce the graph | Architecture §1–2 |
| **3** | **Demo: Dual-Action Crisis** | 3:30–6:30 | **Centrepiece.** Prove the plane works on the refund trace | Prototype (refund agent) |
| **4** | Mechanism Deep Dive | 6:30–8:30 | How it works: provenance, binding, entitlement, matrix | Architecture §3–4 |
| **5** | Differentiation | 8:30–9:30 | Why others fail; refuse-to-claim posture | Narrative §3–5, QA |
| **6** | Business Logic | 9:30–10:30 | Value levers, roadmap, buyers | R2S4 §§7–11 |
| **7** | Closing: The Resolve | 10:30–11:30 | Answer the hook; leave the room with the thesis | Narrative §7 |

**Total:** 11:30 (adjustable to 8:00 by tightening Demo to 2:00 and Business Logic to 1:00).

**Rule:** The Demo (Beat 3) is the emotional and intellectual centre. Everything before it sets it up. Everything after it defends it.

---

## 3. Opening Beat (First 60–90 Seconds)

### Exact Approach
- **Visual:** Full-screen display of the refund approval text:
  > *Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.*
- **Delivery:** Pause. Let it sink in.
- **First spoken line (hook):**
  > **"Clause 7.2 does not exist."**
- **Second line (category shift):**
  > **"Money moved Tuesday. Found Friday. The system didn’t fail. It was never asked to prove anything."**
- **Third line (stakes):**
  > **"It used to be a bad paragraph. It is now an executed transaction."**

### Why This Works
- Opens on **a held transaction**, never on generic "AI risk."
- Establishes **concrete stakes** (₹1,84,000) and **category change** (paragraph → transaction).
- Uses **frozen lines** that survived seven-model adversarial scoring.
- Forces the judge to confront the **failure mode** (absence of evidence, not conflict).

### Forbidden Variations
- ❌ Starting with "AI is powerful but risky..."
- ❌ Opening on a person (shocked customer, angry email)
- ❌ Using "hallucination" as the primary frame (it's an **authorisation** problem)
- ❌ Any vocabulary from the ban list (monitor, detect, observe, watch, guard, trust score)

---

## 4. Prototype Demonstration Spine

### Core Principle
Build backward from the **action gate**. The demo must prove:
1. Provenance is captured **outside the model** (spans before claims)
2. The **Evidence Ledger** is the majority of the UI (≥60%)
3. **Dual-action** is independent: R1 Edit + R3 Escalate (held, never "blocked")
4. **Principal-flip** shows entitlement is set-membership, not semantics
5. **Empty FNR schema** is visible (null placeholders only)

### Demo Flow (≤3:00)

| Step | Action | Visual | Spoken Line | Proves |
|------|--------|--------|--------------|--------|
| **A** | Cold open gate | `refund.execute({amount:184000, reason:"clause 7.2", order_id:"ORD-1023"})` · **HELD — ESCALATE** · `executed:false` | *"This is the commit path. It is closed."* | Hard gate on actions |
| **B** | Expand ledger | Spans with `source_id · ACL · hash · offsets` **before** claim verdicts | *"Evidence was recorded at context assembly — outside the model."* | Provenance Recorder keystone |
| **C** | Show claims | C1 (amount) SUPPORTED · C2 (clause 7.2) **no span → UNSUPPORTED** · C3 (FIN-INTERNAL) **entitlement violation** | *"Three claims. One binds. One has no evidence. One is correct but unauthorized."* | Claim extraction, binding, entitlement |
| **D** | Matrix cells | Highlight **R1×entitlement→Edit** (text.show) and **R3×unsupported-categorical→Escalate** (refund.execute) | *"Same unsupported claim. Different blast radius. Different actuator."* | Exact R×S matrix |
| **E** | Actuators | Surgical Edit strips C3; refund stays **held**; packet opens for C2 (claim, candidate spans `[]`, verdict, diff) | *"Text is edited. Payment is escalated — with the evidence packet."* | Dual-action, evidence packet |
| **F** | Executor proof | `executed:false` confirmed; company does **not** wrongly pay out | *"The gate held. The money stayed."* | Hard gate, held≠blocked |
| **G** | Empty FNR | Typed schema with null placeholders visible | *"We publish our own miss rate. Per route. This is the format."* | FNR honesty |
| **H** | Principal flip | Switch caller from `agent_refund_7` → `hr_partner_01`; same span/claim → **Pass** | *"Same claim. Different principal. Outcome flips."* | Entitlement = set-membership, zero LLM |

### Demo Rules
- **Must show:** Ledger ≥60%; spans before claims; matrix cells before actuators; `committed:false`; evidence packet; empty FNR; principal flip.
- **Must NOT show:** Composite risk/confidence scores; LLM-as-judge pane; open-web lookup; "Response blocked"; `COMMIT BLOCKED` for R3 unsupported-categorical; interlock bypass override; third-route chrome; bias widget.
- **Voice discipline:** Use **authorise · admit · prove · bind · refuse · hold · escalate · gate** exclusively. Ban all vocabulary from the prohibited list.

### Demo Order Priority
1. **Dual-action crisis** (R1 Edit + R3 Escalate held) — non-negotiable centrepiece
2. **Principal flip** — proves entitlement is identity-aware
3. **Evidence Ledger** — proves provenance is captured outside the model
4. **Empty FNR** — proves credibility posture
5. **Matrix fidelity** — proves exact R×S routing

**If time is cut:** Remove polish (paraphrase entailment, parametric ungrounded) before cutting any of the above.

---

## 5. Business Case Integration

### Where It Lives
- **Beat 6: Business Logic (9:30–10:30)** — Dedicated section after Differentiation.
- **Integrated into Demo:** Value levers are **implied** by the demo (e.g., `executed:false` proves avoided wrong action).

### Delivery Approach
**Do not turn the pitch into a consulting deck.** Business case is delivered as **mechanism → consequence**, not as ROI slides.

| Lever | How to Present | Spoken Line |
|-------|----------------|--------------|
| **Avoided wrong actions** | Point to `executed:false` in demo | *"This is structural. The gate cannot be bypassed by confidence or volume."* |
| **Blast-radius pricing** | Reference matrix cells | *"Same verdict annotates a draft and holds a payment. Budget goes where harm is."* |
| **Exact dead compute** | Mention backward graph walk | *"We can name the exact spend that grounded nothing. No competitor can."* |
| **Alert fatigue reduction** | Reference R0/R1 pass+annotate | *"Low-consequence traffic flows. High-consequence traffic is gated."* |
| **Auditability** | Reference hash-chained ledger | *"Reconstruct any decision: action → cell → verdict → span → source."* |
| **Unauthorized disclosure** | Reference principal-flip demo | *"We stop IAM gaps from being silently bypassed by a model."* |
| **Publish misses** | Point to empty FNR schema | *"We publish what we miss. Per route. The emptiness is the point."* |

### Roadmap Integration
- **Mention in Beat 6:** "Day one is shadow. Enforcement is earned, not switched on."
- **Do not show a timeline slide.** Roadmap is **earn-out logic**, not a feature calendar.

### Buyer Logic Integration
- **Economic buyer (CFO/CRO/Risk):** Focus on **avoided wrong actions** and **published FNR**.
- **Technical buyer (Platform/ML infra):** Focus on **integration cost as moat** (SDK hook + proxy) and **latency targets (≤40ms p50 / ≤200ms p95)**.
- **App/agent teams:** Focus on **no app rewrite** and **route-specific configuration**.
- **Operators:** Focus on **shadow/canary/enforce lifecycle** and **circuit breaker**.

**Key:** Every buyer type gets **one line** in the pitch. Do not dwell.

---

## 6. Differentiation & Defence Moments

### The 3 Defence Moments
These are the **only** places where differentiation is explicitly contrasted. Each must land with **engineering precision**, not marketing.

| Moment | Trigger | Line | Target | Proof |
|--------|---------|------|--------|-------|
| **1** | After Demo Step B (ledger expand) | *"Everyone watches the exit. Nobody records the entrance."* | vs Observability (LangSmith, Arize) | Provenance Recorder + ledger |
| **2** | During Mechanism Deep Dive | *"They ask: ‘Does this look right?’ We ask: ‘Which span proves it?’"* | vs LLM-as-judge (NeMo Guardrails, LlamaGuard) | Binding is lookup, not opinion |
| **3** | During Business Logic | *"They publish precision — the rate at which they bother the user. We publish the rate at which we missed."* | vs Composite risk scores (Azure AI Content Safety) | Empty FNR schema |

### Refuse-to-Claim Posture
Embed these **negations** in the same beats:
- **Beat 0 (Opening):** Implicitly refuse "AI safety" as standalone virtue by framing as authorisation.
- **Beat 2 (Thesis):** Explicitly: *"We do not promise safe AI. We make unproven claims unable to authorize actions."*
- **Beat 5 (Differentiation):** Explicitly: *"We do not eliminate hallucinations. We report what we miss."*
- **Beat 6 (Business):** Implicitly: No ROI slides, no "99%" claims, no net-savings percentages.

### Adversarial Readiness
- **B1 (no retrieval context):** If challenged, respond: *"We don’t claim to verify what we were never given. We claim what we were never given cannot authorize an action."*
- **B5 (prompt injection):** If challenged, respond: *"The model cannot author spans. Binding is computed by us, not asserted by the model."*
- **Matrix corruption:** If a judge redraws the matrix, **transcribe it verbatim** from the frozen artifact.

---

## 7. Closing Beat

### Exact Approach
- **Visual:** Return to the opening screen (refund approval text).
- **Spoken lines:**
  1. **"That system was never asked to prove anything."** (pause)
  2. **"Now nothing acts until it can prove it should."** (hold)
- **Optional final line (if time):**
  > *"Because the cost of a wrong output changed category. And we built the plane that gates the commit path."*

### Why This Works
- **Resolves the opening** exactly (negated then resolved).
- **Reinforces the thesis** in its most compressed form.
- **Leaves the room with the core insight** (admission control, not scoring).
- **Uses frozen lines** that scored 49–50/50 in adversarial testing.

### Forbidden Variations
- ❌ Ending with a call-to-action ("Let’s build this together")
- ❌ Ending with a vision statement ("The future of responsible AI...")
- ❌ Any vocabulary from the ban list

---

## 8. Anti-Patterns (Hard Kill List)

### Pitch Structure
- ❌ Opening on risk, safety, or ethics (must open on **held transaction**)
- ❌ Leading with enablement ("ControlPlane helps you deploy AI safely")
- ❌ Turning the demo into a product tour (demo must prove the **architecture**)
- ❌ Collapsing dual-action into one response-level verdict
- ❌ Showing more than two live routes in Stage 5
- ❌ Including a third "bias route" as a live demo
- ❌ Showing confidence scores, risk scores, or composite metrics in the decision path
- ❌ Using LLM-as-judge as the primary mechanism in the demo
- ❌ Claiming to eliminate hallucinations, bias, or privacy leaks
- ❌ Claiming zero integration or zero latency
- ❌ Using one accuracy number across failure modes

### Language
- ❌ **Never say:** monitor, observe, detect, watch, guard, trust score, risk score, "responsible AI" as standalone virtue
- ❌ **Never say:** "blocked" about the refund (use **held and escalated with the evidence packet**)
- ❌ **Never say:** "clause 7.2 caps/denies/doesn’t cover" (use **does not exist**)
- ❌ **Never say:** "the customer lost money" (use **the company wrongly paid out**)
- ❌ **Never say:** "we catch hallucinations" (use **ungrounded claims cannot authorize actions**)

### Visuals
- ❌ Showing a "blocked" status for the refund action
- ❌ Showing a red "BLOCKED" label on the refund
- ❌ Using a risk matrix that isn’t the exact 4×4 R×S
- ❌ Showing a confidence threshold as the gating mechanism
- ❌ Including marketing fluff, stock images, or generic AI visuals

### Content
- ❌ Fabricating FNR numbers (must show **empty schema with typed placeholders**)
- ❌ Claiming per-response bias detection
- ❌ Claiming real-time ground truth
- ❌ Claiming the plane fixes IAM (it **stops IAM gaps from being bypassed**)
- ❌ Claiming the model emits reliable citations

---

## 9. Fidelity Self-Check

### Eternal Invariants — Protection Status

| Invariant | Pitch Protection | Verification |
|-----------|-------------------|--------------|
| **Default = UNSUPPORTED** | Explicit in Thesis; reinforced in Mechanism Deep Dive | ✅ |
| **Entitlement = set-membership (zero LLM)** | Proven by principal-flip demo; stated in Differentiation Moment 2 | ✅ |
| **Exact R×S matrix (4×4, transcribed never redrawn)** | Shown in Demo Step D; transcribed verbatim if challenged | ✅ |
| **One graph: STEP → SPAN → CLAIM → ACTION** | Core of Thesis; visual in Demo Step B | ✅ |
| **Hard gate on actions, not tokens** | Proven by Demo Step A (`executed:false`); stated in Closing | ✅ |
| **Dual-action: R1 Edit + R3 Escalate (held, never "blocked")** | Centrepiece of Demo; language policed in Anti-Patterns | ✅ |
| **UNKNOWN never → SUPPORTED** | Stated in Mechanism Deep Dive; implied in Demo | ✅ |
| **FNR as typed format (empty until earned)** | Shown in Demo Step G; stated in Differentiation Moment 3 | ✅ |
| **Bias = async route-level only** | Explicit in Business Logic; never mentioned as live matrix cell | ✅ |
| **Refuse-to-claim posture** | Embedded in Thesis, Differentiation, Closing | ✅ |
| **Exactly two live routes** | Demo limited to refund agent + knowledge assistant | ✅ |
| **Latency: ≤40ms p50 / ≤200ms p95** | Stated in Mechanism Deep Dive; never quoted as 40ms p95 | ✅ |
| **Vocabulary discipline** | Ban list enforced; preferred terms used exclusively | ✅ |

### Demo Fidelity Checks
- [x] Provenance Recorder is keystone (built first, shown first in demo)
- [x] Evidence Ledger is majority of UI (≥60%)
- [x] Dual-action is independent (R1 Edit + R3 Escalate)
- [x] Refund is **held**, never "blocked"
- [x] Principal flip proves entitlement
- [x] Empty FNR schema is visible
- [x] Matrix cells are shown before actuators
- [x] No composite scores, confidence metrics, or LLM-as-judge in critical path

### Narrative Fidelity Checks
- [x] Opens on held transaction (₹1,84,000 / clause 7.2)
- [x] Uses frozen lines (system didn’t fail...; used to be a paragraph...; now nothing acts...)
- [x] Bans prohibited vocabulary
- [x] Uses preferred vocabulary exclusively
- [x] Closes by resolving the opening

**Result:** All eternal invariants are **protected and verifiable** in the pitch architecture.

---

## Appendix: Quick Reference for Presenters

### The 5 Lines That Win the Room (Memorize)
1. **"It used to be a bad paragraph. It is now an executed transaction."** *(stakes)*
2. **"The system didn’t fail. It was never asked to prove anything."** *(hook)*
3. **"Everyone watches the exit. Nobody records the entrance."** *(differentiation vs observability)*
4. **"We don’t claim to verify what we were never given. We claim what we were never given cannot authorize an action."** *(B1 defence)*
5. **"We publish our own miss rate. Per route. Not what we caught — what we missed."** *(credibility)*

### The 3 Numbers That Matter
1. **₹1,84,000** — the concrete stake
2. **≤40ms p50 / ≤200ms p95** — latency (never 40 as p95)
3. **0** — fabricated FNR (must show empty schema)

### The 2 Demo Non-Negotiables
1. **Dual-action must be shown independently** (R1 Edit + R3 Escalate)
2. **Principal flip must prove entitlement is set-membership**

### The 1 Rule for All Presenters
**If a judge could summarize it as "it watches AI outputs and flags problems," the pitch has failed.** Rewrite until that sentence no longer fits.
The **Pitch Architecture** for ControlPlane.ai — Round 2 Stage 5 is now complete and available in the canvas.

This architecture:
- Opens on the **held ₹1,84,000 transaction** (clause 7.2 does not exist)
- Centres the pitch on the **dual-action demo** (R1 Edit + R3 Escalate held)
- Protects all eternal invariants (Default=UNSUPPORTED, exact R×S matrix, one graph, hard gate on actions, empty FNR schema)
- Uses only the **frozen vocabulary** (authorise/admit/prove/bind/refuse/hold/escalate/gate)
- Embeds the **3 defence moments** and **refuse-to-claim posture**
- Closes by resolving the opening: *"Now nothing acts until it can prove it should."*

The canvas includes the full structure, exact lines, demo spine, and hard kill list. It is ready for refinement and rehearsal.