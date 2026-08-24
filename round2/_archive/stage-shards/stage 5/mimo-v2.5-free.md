# ControlPlane.ai — Stage 5: Pitch Architecture

> Model: `opencode/mimo-v2.5-free`  
> Accenture Innovation Challenge 2026 · Round 2 · Stage 5  
> Sources (frozen, non-negotiable): `CONTROLPLANE_R2_FINAL.md` · `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` · `R2S2.md` · `R2S3.md` · `R2S4.md`  
> Status: Stages 1–4 are eternal. This file designs the pitch structure and nothing else. Do not reopen.

---

## 1. Pitch Thesis

An AI response is a set of claims requesting permission to act. Every existing oversight tool inspects what the model said. None of them recorded what the model was given. ControlPlane captures provenance outside the model, inverts the burden of proof so nothing passes because nobody objected, carries the caller's identity into verification, and sits a hard gate on the commit path — not on the text. The same refund response yields two simultaneous outcomes: the customer text is surgically edited, the ₹1,84,000 refund is held and escalated with an evidence packet. Proof scales with consequence. We publish what we miss.

---

## 2. Overall Pitch Structure

**Total: 10 minutes.** Two presenters. One drives the live demo. One drives the business narrative. Switch once.

| # | Section | Duration | Speaker | What happens |
|---|---------|----------|---------|--------------|
| 1 | Cold open — held transaction | 60s | A | Screen shows the ₹1,84,000 refund HELD. No intro slide. No title. No "AI is risky." |
| 2 | Thesis + one-graph proof | 90s | A | State the thesis. Draw one graph: STEP→SPAN→CLAIM→ACTION. Three reads, one structure. Name the indictment line. |
| 3 | Dual-action demonstration | 180s | A+B | Live demo. Build backward from the action gate. Core crisis ≤90s. Principal flip ≤2min. Ledger ≥60% screen. |
| 4 | The structural failure of everything else | 90s | B | Three reasons existing approaches fail. Named products. "Retrieval is not permission." |
| 5 | Differentiation + refuse-to-claim | 60s | B | Ordered contrast. Published FNR. Refuse-to-claim about *us*. |
| 6 | Enterprise envelope + roadmap | 60s | B | Earn-out, not feature calendar. Shadow→canary→enforce. Beachhead = high-consequence routes. |
| 7 | Close — resolve the opening | 30s | A | "That system was never asked to prove anything. Now nothing acts until it can prove it should." |

**Time allocation by content type:**
- Demo: 300s (50%)
- Architecture/narrative: 210s (35%)
- Business/roadmap: 60s (10%)
- Close: 30s (5%)

**Why this ratio:** The prototype is the proof. The business proposal is the wrapper. A serious judge evaluates the architecture in the room, not the slide deck. The demo must dominate.

---

## 3. Opening Beat (0:00–1:30)

### Approach

**Cold open on the held transaction.** No title slide. No "thank you." No "AI is transforming enterprises." The first thing the judge sees is an action gate panel:

```text
Action:      refund.execute
Args:        { amount: 184000, reason: "clause 7.2", order_id: "ORD-1023" }
R:           R3 — irreversible payment
Status:      HELD — ESCALATE
Executed:    false
```

Silence for 2 seconds. Then:

### Preferred opening lines

> **"₹1,84,000. Refund executed under clause 7.2 of the vendor agreement."**
>
> *[pause]*
>
> **"Clause 7.2 does not exist."**
>
> *[pause]*
>
> **"Every filter passed it. Confidence read 0.94. The money moved on Tuesday. It was found on Friday. If nothing had gated that commit, the company wrongly pays out ₹1,84,000 — the customer did not lose money."**
>
> *[beat]*
>
> **"The system didn't fail. It was never asked to prove anything."**

Then immediately:

> **"Everyone watches the exit. Nobody records the entrance."**

### Rules for the opening

- **Never open on a person.** No shocked customer face. No angry email screenshot. Open on a transaction with a rupee figure.
- **Never open on "AI risk" or "AI safety."** This is an authorisation system, not a safety wrapper.
- **First sentence must contain "claim," not "response."** The word "claim" appears within the first 60 seconds.
- **No title slide before the gate.** The gate IS the title.
- **The word "safety" may appear only after "deterministic entitlement check" — never as a standalone virtue.**

---

## 4. Prototype Demonstration Spine (1:30–6:30)

### Governing constraint

The demo must look fundamentally different if you remove the graph from the screen. If the judge can mentally delete the Evidence Ledger and the demo still makes sense, the prototype scope has failed.

### Demo architecture — embedded inside the pitch

The demo is not a separate segment. It IS the argument. The presenter narrates the architecture AS the demo runs. Every visual beat maps to a frozen invariant.

### Step-by-step flow

**Beat 1 — The gate is already live (0:00 of demo / 1:30 of pitch)**

The screen already shows `HELD — ESCALATE`. The judge's first reaction is: *why is it held?*

> "This refund is held. Not blocked — held, and escalated with an evidence packet. Let me show you why, and let me show you what the system proved before it made that decision."

**Beat 2 — Expand the ledger (30s)**

Screen reveals `STEP → SPAN → CLAIM → ACTION`. Spans are visible BEFORE claim verdicts. Each span shows `source_id · ACL · hash · offsets`.

> "Before the model ran, we captured what it was allowed to know. Every span — source, access rights, content hash. The model cannot write these. It cannot alter them. This is the entrance record nobody else keeps."

**Beat 3 — Claims born UNSUPPORTED (30s)**

Three claims appear on screen. All start as `UNSUPPORTED`:

| Claim | What it says | Type | Finding |
|-------|-------------|------|---------|
| C1 | Refund ₹1,84,000 / order ORD-1023 | numeric | Binds to `ORD-1023` → **SUPPORTED** |
| C2 | "under clause 7.2 …" | categorical | **Zero spans** → stays **UNSUPPORTED** |
| C3 | Text grounded on FIN-INTERNAL-NOTE | textual | ACL excludes `agent_refund_7` → **entitlement violation** |

> "Every claim starts unsupported. Not low confidence — unproven. C1 earns proof: the number matches an order record. C2 finds nothing. Clause 7.2 has no span. It doesn't contradict anything. It's absent. And absence is not contradiction."

**Beat 4 — Matrix cells BEFORE actuators (30s)**

The exact frozen 4×4 matrix is visible. Two cells light up:

| Pending action | Tier | Matrix cell | Actuator |
|----------------|------|-------------|----------|
| `text.show` | R1 | R1 × entitlement | **Edit** |
| `refund.execute` | R3 | R3 × unsupported-categorical | **Escalate** |

> "One response. Two pending actions. The system prices them separately. The text carries a claim grounded on an internal note the refund agent isn't entitled to read — R1, entitlement violation, Edit. The refund carries a claim with no evidence at all — R3, unsupported categorical, Escalate. Same response. Two different consequences. Proof scales with consequence."

**Beat 5 — Surgical Edit + held refund (30s)**

- C3 is stripped from the customer-visible text.
- The refund executor log shows `committed: false`.
- The evidence packet opens: claim C2, candidate spans `[]`, verdict `UNSUPPORTED`, diff.

> "The text is surgically edited — only the failing claim removed. The refund stays held. The company does not wrongly pay out ₹1,84,000. And here is the evidence packet: what was claimed, what evidence existed — nothing — the verdict, and the diff. Not a bare alert. An evidence packet a human reviewer can act on."

**Beat 6 — Empty FNR schema (15s)**

The FNR Gate Report panel appears with typed null placeholders.

> "We publish our own miss rate. Per route. Right now every field is null — because we haven't run a stratified audit on production traffic. The emptiness is the credibility play. When we earn the numbers, the schema is already there. The claim shape is: on this route we catch X% of unproven claims at 40 milliseconds — and here is the Y% we don't."

**Beat 7 — Principal flip (≤2 minutes)**

Switch to the knowledge route.

| Step | What happens |
|------|-------------|
| Principal = `analyst_01` | Claim binds to `HR-COMP-L6`. ACL excludes caller. → **R1 × entitlement → Edit** |
| Principal = `hr_partner_01` | Same span, same claim. ACL includes caller. → **SUPPORTED → Pass** |

> "Same span. Same claim. Same graph. I changed one thing: who is asking. The entitlement check is set-membership — does the caller's clearance include the span's ACL? Zero LLM. Deterministic. Sub-millisecond. This is the mechanism no output-only competitor can replicate, because none of them carry identity into verification."

### Demo hard rules

| Must show | Must NOT show |
|-----------|---------------|
| Ledger ≥60% screen; spans before claims | Composite risk/confidence scores |
| Action Gate cold-open with `committed: false` | "Response blocked" / `COMMIT BLOCKED` |
| Per-claim Verified/Uncertain/Blocked; refund = Held/Escalate | LLM-as-judge pane · open-web lookup |
| Evidence packet on every Escalate; empty FNR | Third-route chrome · bias widget · chatbot-majority layout |
| Matrix cells highlighted BEFORE actuators fire | Any invented actuator (STREAM, Kill Span, Hold & Re-verify) |
| Live binding compute visible (~20–80ms) | Pre-baked animation |

### Voice during demo

Use: **authorise · admit · prove · bind · refuse · hold · escalate · gate**

Never: monitor · detect · observe · watch · guard · trust score · risk score · "responsible AI"

---

## 5. Business Case Integration (6:30–7:30)

### Where it lands

After the demo. The judge has just seen the mechanism work. The business case must NOT feel like a pivot to a consulting deck. It must feel like the natural consequence of what they just witnessed.

### Structure — three beats in 60 seconds

**Beat 1 — The value levers (20s)**

> "You just saw Lever A: an unproven claim structurally cannot execute a payment. That is not a statistical argument. That is an action log showing `committed: false`. The other levers come from the same graph: dead compute measured exactly — not estimated — by walking the graph backward. Blast-radius pricing: the same graph checks a draft cheaply and holds a payment thoroughly. And a per-route false-negative rate we publish ourselves."

**Beat 2 — The roadmap (20s)**

> "Day one is shadow. Every route starts with dual-emit — gated and ungated — producing a counterfactual: would have held N, of which M were true positives. Enforcement is earned per route from that evidence, not switched on from a slide. We don't ask you to trust a score. We ask you to run the counterfactual."

**Beat 3 — The beachhead (20s)**

> "We enter through high-consequence action routes: customer-support refund agents and internal knowledge assistants with mixed-governance data. Not all enterprise AI. Not an AI safety purchase. A route where text causes a financial commitment — and the fraction of those actions that can sit behind an earned admission boundary."

### What must NOT appear in this section

- No fabricated ROI percentages
- No "99% accuracy"
- No "eliminates hallucinations"
- No "net savings" slide
- No "30–50% of steps are waste"
- No enablement language ("empower your teams")
- No generic "responsible AI" framing

---

## 6. Differentiation & Defence Moments (7:30–8:30)

### Where they land

Woven into section 4 (structural failure of everything else), with a focused 60-second block after the demo.

### Three ordered contrasts — delivered in this order

**1. vs observability (LangSmith, Arize, etc.)**

> "Observability tells you what went wrong after a user acted on it. That is the precise failure mode the brief asks to eliminate at the commit path. Observation without execution control is an audit trail, not architecture."

*Beat:* "And they measure spend, not waste. A dashboard can tell you the trace cost ₹8. It cannot tell you that ₹5 of it grounded nothing. Walking the graph backward can."

**2. vs LLM-as-judge / static guardrails (NeMo, LlamaGuard)**

> "A second model asks, 'does this look right?' — an unfalsifiable question, with the same family of blind spots, usually without the source documents, and always without knowing who is asking. We ask, 'which span proves it?' — a query with an answer. Decision time is a pure rule engine. Zero LLM."

**3. vs RAG groundedness (the closest cousin)**

> "Groundedness checkers see retrieval only — not tool results, DB rows, system context. They average, so one wrong figure drowns in nine correct sentences. And they are action-blind: 0.82 means the same on a draft and on a wire transfer. None carry caller identity. None can do entitlement. Retrieval is not permission."

### The credibility closer

> "We publish our own false-negative rate. Per route. Not what we caught — what we missed. The plane is audited by the standard it enforces. Every deck in this room disclaims its competitors. We disclaim ourselves."

### The refuse-to-claim moment

> "We do not claim to eliminate hallucinations. We do not claim zero integration. We do not claim zero added latency. We do not claim one accuracy number across three failure modes. Anyone who has shipped knows those claims are false."

*Beat:* "The integration cost is the moat. We hook context assembly — that is real work, and it is the exact reason the design works."

---

## 7. Closing Beat (8:30–10:00)

### Approach

Resolve the opening. The opening showed a transaction that was never asked to prove anything. The close shows the system where nothing acts until it can prove it should.

### Preferred closing lines

> **"The system you just saw was never asked to prove anything."**
>
> *[pause — callback to the opening line]*
>
> **"Now nothing acts until it can prove it should."**
>
> *[beat]*
>
> **"Provenance outside the model. Default unsupported. Entitlement is set-membership. Proof scales with consequence. Hard gate on the commit path. And we publish what we miss."**
>
> *[final line]*
>
> **"Any softer design is a different product."**

### Rules for the close

- Do not introduce new information.
- Do not say "thank you" before the final line — the final line IS the close.
- Do not show a "next steps" or "contact us" slide before the close. Show it after, silently.
- The final sentence must be the ARCHITECTURE.md closing line: *"Any softer design is a different product."*

---

## 8. Anti-Patterns (Hard Kill List)

These are specific things the pitch must **never** do. Each has been corrupted by at least one model during the freeze process.

| # | Anti-pattern | Why it dies |
|---|-------------|-------------|
| 1 | **Opening on "AI is powerful but risky"** | First line of every guardrail deck. Sets the frame before you say anything original. |
| 2 | **Opening on a person (shocked customer, angry email)** | Emotional manipulation, not architecture. Open on a transaction. |
| 3 | **Saying "the refund was blocked"** | R3 × unsupported-categorical = **Escalate**. Say *held and escalated with the evidence packet.* |
| 4 | **Collapsing dual-action into one "response blocked"** | Destroys the centrepiece. Same response → R1 Edit + R3 Escalate, simultaneously. |
| 5 | **Leading with enablement ("empower your teams")** | Enablement is what every deck says. This is admission control. Lead with the gate. |
| 6 | **Using "safety" as a standalone virtue** | "Safety" may appear only *after* "deterministic entitlement check." Never as a header. |
| 7 | **Quoting 40ms as p95** | 40ms is p50. p95 is ≤200ms. This error was caught in three places during the freeze. |
| 8 | **Filling FNR with fabricated numbers** | Empty typed placeholders. Emptiness is the credibility play. |
| 9 | **Claiming "we eliminate hallucinations"** | Refuse-to-claim list is about *us*. Anyone who has shipped knows this is false. |
| 10 | **Showing a composite risk/confidence score** | You cannot Block, Edit, or Escalate on 87. |
| 11 | **Using monitor/detect/observe/watch/guard vocabulary** | Use: authorise · admit · prove · bind · refuse · hold · escalate · gate. |
| 12 | **Showing a third live route** | Exactly two live routes. Third = enterprise envelope only, never in the demo. |
| 13 | **Running the demo as a recording** | Binding/entitlement/interlock must show real compute (~20–80ms). A hostile judge must not dismiss it as animation. |
| 14 | **Describing clause 7.2 as "caps" or "denies"** | Clause 7.2 does not exist. Absence ≠ contradiction. |
| 15 | **Saying "the customer lost money"** | **The company wrongly pays out.** The customer did not lose money. |
| 16 | **Leading with the FNR or dead-compute as the centrepiece** | Dual-action is the centrepiece. FNR and dead-compute are secondary graph reads. |
| 17 | **Adding a bias widget to the demo screen** | Bias is async route-level measurement in the proposal only. Not a live actuator. |
| 18 | **Saying "zero latency"** | We never make the model feel slow; we make the action wait. |
| 19 | **Saying "zero integration"** | The integration cost is the moat. Say it out loud. |
| 20 | **Introducing a "risk score" or "trust score" as a UI element** | Disposition = verdict × blast radius. No scalar. |

---

## 9. Fidelity Self-Check

Explicit confirmation that the pitch architecture protects every major invariant from Stages 1–4:

| Invariant | How the pitch protects it |
|-----------|--------------------------|
| **Default = UNSUPPORTED** | Demo shows all three claims born UNSUPPORTED. Spoken explicitly: "every claim starts unsupported." |
| **Entitlement = ACL set-membership; zero LLM** | Principal flip is a required secondary demo beat. "Zero LLM" stated on screen and in voice. |
| **Exact R×S matrix; no route parameter** | Full 4×4 visible during demo. Two cells highlighted before actuators fire. No route-specific cells shown. |
| **One graph: STEP→SPAN→CLAIM→ACTION** | Ledger occupies ≥60% screen throughout demo. "Three reads of one graph" stated in thesis section. |
| **Hard gate on actions, not tokens** | Cold-open shows `committed: false`. Hold-back mentioned. "We make the action wait." |
| **Dual-action: R1 Edit + R3 Escalate (held, never "blocked")** | Dual-action is the demo centrepiece. Refund always described as "held and escalated." Never "blocked." |
| **UNKNOWN never → SUPPORTED** | Stated explicitly: "absence is not contradiction." C2 stays UNSUPPORTED; no path to SUPPORTED shown. |
| **FNR as typed format; empty until earned** | FNR schema shown with nulls. "Emptiness is the credibility play" stated aloud. |
| **Bias = async route-level only** | Bias is mentioned once in the roadmap section, in measurement terms. Never shown in demo. |
| **Refuse-to-claim (about us)** | Dedicated beat. All four refusals stated. "We disclaim ourselves." |
| **Exactly two Stage 1 live routes** | Demo shows exactly refund + knowledge. Third route never appears. |
| **Latency ≤40ms p50 / ≤200ms p95** | Numbers stated correctly if latency is discussed. 40ms never called p95. |
| **Surgical edit only** | Demo shows C3 stripped. "Only the failing claim removed." No generative rewrite shown. |
| **Evidence packet on Escalate** | Packet opens during demo: claim, candidate spans, verdict, diff. |
| **Lane 1 always on** | Entitlement and deterministic checks shown running inline. "Sub-millisecond" stated. |
| **Locked R3 classes** | Mentioned in roadmap: "payment, deletion, publication, regulated advice remain R3 at parse time." |
| **Content laws** | Clause 7.2 absence stated. Company wrongly pays out stated. Customer did not lose money stated. |
| **Vocabulary discipline** | All 20 anti-patterns listed. Voice direction explicit. |
| **No confidence/risk score** | None shown in demo. No score drives disposition anywhere in the pitch. |
| **Model cannot author provenance** | Stated: "The model cannot write these spans. It cannot alter them." |

---

## Appendix — Script Discipline

Every spoken line must pass this test before it enters the pitch:

1. **Does it name a claim, a graph, an action, or a measurement?** If it only says "the AI" or "the response" in the abstract, cut it.
2. **Could it survive being moved into a different company's pitch?** If yes, cut it.
3. **Does it use monitor/detect/observe/watch/guard vocabulary?** If yes, rewrite.
4. **Does it say something the frozen architecture does not hold?** If yes, kill it.

**The ship test:** If a judge could summarise the pitch as *"it watches AI outputs and flags problems,"* the narrative has failed regardless of the architecture. Rewrite until that sentence no longer fits.

---

*End of Stage 5: Pitch Architecture. Stages 1–4 remain eternally frozen. Pitch from this file + live demo.*
