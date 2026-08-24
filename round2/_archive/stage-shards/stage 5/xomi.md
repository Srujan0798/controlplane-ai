# Stage 5: Pitch Architecture — ControlPlane.ai Round 2

---

## 1. Pitch Thesis

Every oversight tool inspects what the model said. ControlPlane inspects what the model was given — and refuses to let an unproven claim authorize an irreversible action. The pitch must leave one idea in the room: **an AI response is a set of claims requesting permission to act, and the only honest architecture is one that captures provenance outside the model, inverts the burden of proof, carries identity into verification, and gates the commit path.** Everything else is a different product. The judge must leave believing that the ₹1,84,000 refund was not a hallucination problem — it was an authorization problem — and that the only fix is admission control, not better text scoring.

---

## 2. Overall Pitch Structure

**Total: ~10 minutes.** Tighter is better. Every second must name a claim, a graph, an action, or a measurement.

| # | Beat | Duration | Purpose |
|---|---|---|---|
| **0** | Cold open — Action Gate | 30s | Screen shows held transaction before anyone speaks. Emotional hook. |
| **1** | The category change | 60s | Problem framing. Clause 7.2. The indictment. |
| **2** | The thesis | 45s | One graph, three reads. Admission control, not observability. |
| **3** | Live demo — the crisis | 180s | Dual-action centrepiece. Ledger ≥60% of screen time. |
| **4** | What we refuse to claim | 45s | Refuse-to-claim list. Empty FNR. Publish misses. |
| **5** | Who buys this, and why | 60s | Buyer logic, impact levers, roadmap spine. |
| **6** | Differentiation — the structural contrast | 60s | Three contrasts. The line that wins. |
| **7** | Close | 30s | Resolve the opening. Land the thesis. |

**Total: ~8 minutes 30 seconds.** Leaves ~90 seconds of buffer for transitions, audience reaction, or a single question mid-pitch if format allows.

---

## 3. Opening Beat (first 90 seconds)

### Approach

The screen is dark. A single transaction log appears — no title slide, no team name, no problem statement. The judge reads before anyone speaks.

### Screen content (cold open)

```
ACTION GATE
─────────────────────────────────────────
route:     refund.execute
action:    { amount: 184000, currency: INR,
             reason: "clause 7.2", order: ORD-1023 }
R tier:    R3 — irreversible
status:    HELD — ESCALATE
executed:  false
─────────────────────────────────────────
```

### First spoken words (after 5–8 seconds of silence for the screen to land)

> "This is a refund for ₹1,84,000. The AI approved it. It cited clause 7.2 of the vendor agreement. The confidence score was 0.94. Every filter passed it."

> *[pause]*

> "Clause 7.2 does not exist."

> *[pause]*

> "The failure is not that the model got something wrong. The failure is that nobody asked it to prove anything. The money moved on Tuesday. The error was found on Friday. The company wrongly paid out ₹1,84,000 — the customer did not lose money."

> *[beat]*

> "This is not a hallucination problem. It is an authorization problem. An unproven claim authorized an irreversible action. And the fix is not better text scoring — it is admission control."

### What this achieves

- Opens on a held transaction with a rupee figure — never on risk, never on a person.
- Names the failure as absence of evidence, not conflict — which is what makes Escalate correct, not Block.
- Establishes the category change (bad paragraph → executed transaction) in concrete terms.
- Uses the word "claim" and "authorize" before the word "hallucination."
- The screen already shows `executed: false` — the judge sees the interlock working before hearing the word "architecture."

---

## 4. Prototype Demonstration Spine

The demo is the emotional and intellectual centre. It occupies ~3 minutes and must prove five things in sequence. The governing test from R2S3 applies: **if removing the graph leaves the demo looking the same, scope failed.**

### Demo sequence

**Beat 3a — Expand the ledger (30s)**

Click into the held transaction. The Evidence Ledger fills the screen (≥60% of viewport). Spans appear first — each with `source_id · ACL · content_hash · offsets` — before any claim verdict. The judge sees provenance before judgment.

> "Every span the model was given, captured at context assembly, outside the model. Source identity. Access rights. Content hash. The model has no write path to this record."

**Beat 3b — Three claims, three verdicts (45s)**

Claims decompose from the response. Each starts red (UNSUPPORTED). Verdicts resolve left to right:

| Claim | Verdict | Why |
|---|---|---|
| **C1** — amount/order (₹1,84,000, ORD-1023) | SUPPORTED | Binds to ORD-1023 span. Numeric recomputation. |
| **C2** — "under clause 7.2 of the vendor agreement" | UNSUPPORTED | No span exists. Absence ≠ contradiction. |
| **C3** — grounded on FIN-INTERNAL sentence | Entitlement violation | ACL excludes caller `agent_refund_7`. |

> "All three born unsupported. C1 earned its verdict — the number checks. C2 has no evidence anywhere in the provenance set. C3 is semantically grounded — but the caller is not entitled to read that source. Deterministic. Zero LLM. Sub-millisecond."

**Beat 3c — Matrix cells before actuators (30s)**

Highlight the two matrix cells. Show the cell before showing the actuator. The judge sees the decision logic before the outcome.

> "Two pending actions on one response. Different blast radii. The matrix prices them independently."

| Pending action | Tier | Finding | Cell | Actuator |
|---|---|---|---|---|
| `text.show` | R1 | Entitlement violation (C3) | R1 × entitlement | **Edit** |
| `refund.execute` | R3 | Unsupported + categorical (C2) | R3 × unsupported-categorical | **Escalate — held** |

> "The text is edited — the unentitled reference is stripped. The refund is held and escalated with the evidence packet. Both correct. Both simultaneous. Proof scales with consequence."

**Beat 3d — Evidence packet + executor (30s)**

Open the escalation packet: claim text, candidate spans (empty array for C2), verdict, diff. Then show the executor state: `committed: false`.

> "The packet tells the reviewer exactly what is missing. The refund did not execute. The company does not wrongly pay."

**Beat 3e — Principal flip (30s)**

Switch principal from `agent_refund_7` to `analyst_01`. C3 flips from Edit to Pass. Then switch to `hr_partner_01`. Same span, same claim, different outcome. Zero LLM.

> "Same claim. Same evidence. Different caller. Different result. This is entitlement — identity carried into verification. No classifier involved."

**Beat 3f — Empty FNR (15s)**

Show the FNR schema with typed null placeholders. No fabricated percentages.

> "And here is what we do not know. Per-route false-negative rate — the format, the fields, the confidence interval structure. All null. Because we have not earned the number yet. The emptiness is the credibility play."

### What the demo protects

- Ledger ≥60% of screen time.
- Spans before claims. Matrix cells before actuators.
- Dual-action: R1 Edit + R3 Escalate held. Never collapsed. Never "blocked."
- `executed: false` visible throughout.
- Evidence packet on every Escalate.
- Principal flip proves entitlement is deterministic.
- Empty FNR proves honesty over bluff.
- No composite risk score. No confidence field. No LLM-as-judge pane. No open-web lookup.

---

## 5. Business Case Integration

The business case is delivered in ~60 seconds, immediately after the demo, while the held refund is still on screen. It must not feel like a consulting slide. It must feel like the natural question the demo just raised: *so what is this worth?*

### Delivery approach

> "The question is not 'how do we score AI responses.' The question is: what consequential actions does this route perform today, what is the loss if one is wrong, and what fraction can sit behind an earned admission boundary?"

Then, briefly, the levers — named, not tabulated:

> "The primary value is avoided wrong actions — the refund that does not execute. Sized by the buyer's direct cost of that action class, residual measured by the FNR we publish. Secondary: blast-radius pricing means verification budget follows consequence — a draft is checked cheaply, a payment is not. Dead compute is measured exactly, not estimated — every step that grounded zero accepted claims. And auditability is structural — hash-chained ledger, versioned policy, reconstructible from action to source."

Then the roadmap spine — three sentences:

> "Day one is shadow. Enforcement is earned per route through counterfactual evidence, never switched on globally. The roadmap is not a feature calendar — it is an earn-out sequence: shadow, canary, limited enforce, broader envelope."

Then the buyer — one sentence:

> "The economic buyer is the person who pays when it fails — ops, risk, CISO. They respond to one sentence: an unproven claim cannot authorize an action."

### What this achieves

- Value is mechanism → consequence, not fabricated ROI.
- No "99%." No net-savings slide. No percentage saved.
- Buyer logic is concrete and role-specific.
- Roadmap is an earn-out, not a feature list.
- All delivered while the held refund is still visible on screen — the business case is grounded in the artifact, not abstracted from it.

---

## 6. Differentiation & Defence Moments

Three moments, placed at natural transition points — never clustered into a "competitive landscape" slide.

### Moment 1 — During the demo, after the matrix cells (embedded in Beat 3c)

> "Every other tool in this space inspects the output. We inspect the evidence. They ask 'does this look right?' — an unfalsifiable question. We ask 'which span proves it?' — a query with an answer. They gate on text. We gate on actions. They publish precision — the rate at which they bother the user. We publish the rate at which we missed."

### Moment 2 — After the business case, before the close (standalone beat, ~30s)

> "Three structural reasons existing approaches fail here. Observability traces after commit — audit trail, not interlock. LLM-as-judge produces an opinion using the same reasoning that produced the error, from the same family of blind spots, without knowing who was asking. RAG groundedness averages — one wrong figure drowns in nine correct sentences — and it is action-blind, so 0.82 means the same thing on a draft and on a wire transfer. None of them carry caller identity. None of them can do entitlement. And none of them publish their own miss rate."

### Moment 3 — The refuse-to-claim posture (delivered after the empty FNR, Beat 4)

> "Four things we refuse to claim. We do not claim to eliminate hallucinations — we claim ungrounded claims cannot authorize actions, and we report what we miss. We do not claim zero integration — we hook context assembly, and that integration cost is the exact reason the design works. We do not claim zero latency — we never make the model feel slow, we make the action wait. And we do not claim one accuracy number across failure modes — hallucination, leakage, and bias have different mathematics, different error costs, and different owners."

### What these achieve

- Differentiation is structural, not comparative marketing.
- Naming real product categories (observability, LLM-as-judge, RAG groundedness) is itself a differentiator — nobody else in the room will name names.
- The refuse-to-claim list is about *us*, not competitors — the rarer and stronger move.
- The sharpest line lands in Moment 1: "They publish precision. We publish the rate at which we missed."

---

## 7. Closing Beat (~30 seconds)

The screen returns to the Action Gate from the cold open. Same transaction. Same rupee figure. But now the judge has seen the graph, the matrix, the packet, the flip, and the empty FNR.

> "That system was never asked to prove anything."

> *[hold — 2 seconds]*

> "Now nothing acts until it can prove it should."

> *[screen holds on `executed: false`]*

### What this achieves

- Resolves the opening exactly — first and last claim, negated then resolved.
- The closing line is the thesis in nine words.
- The screen shows the interlock, not a tagline.
- No call to action. No "thank you." No "we're excited." The architecture speaks.

---

## 8. Anti-Patterns (Hard Kill List)

| Never do this | Why |
|---|---|
| Open on risk, AI safety, or "AI is powerful but dangerous" | Sets the guardrail frame. Every competitor opens here. The judge stops listening. |
| Open on a person (shocked customer, angry email) | Opens on emotion, not mechanism. Open on a transaction. |
| Say "blocked" about the refund | R3 × unsupported-categorical = **Escalate — held**. "Blocked" is the wrong actuator and corrupts the matrix. |
| Collapse dual-action into one response-level verdict | Destroys the centrepiece. The whole point is that the same response carries R1 Edit and R3 Escalate simultaneously. |
| Show a composite risk score or confidence number | Rejected by the architecture. Cannot be decomposed by policy or acted on by a user. |
| Use the words monitor, detect, observe, watch, guard, trust score, risk score, responsible AI | Banned vocabulary. Use: authorise, admit, prove, bind, refuse, hold, escalate, gate. |
| Lead with enablement ("AI transforms enterprises…") | Every deck in the room opens here. Lead with the interlock. |
| Claim to eliminate hallucinations | Refuse-to-claim item #1. Invites the one question that ends the pitch: *then what's your miss rate?* |
| Fill FNR placeholders with plausible numbers | The emptiness is the credibility play. Fabricated numbers are a liability the first time a judge tests them. |
| Show a third live bias route or a bias widget | Bias = async route-level measurement. Not a Stage 1 live route. Not a per-response verdict. |
| Spend >90 seconds on the problem before showing the interlock | The problem is established by the cold open. Move to the mechanism. |
| Read the full positioning paragraph verbatim | It runs ~70 seconds aloud. Use the 30-second spoken cut. |
| Show chatbot-majority UI or a dashboard as the deliverable | The deliverable is the interlock and the ledger. A dashboard is what everyone else builds. |
| Say "the system failed" about the refund | The system was never asked to prove anything. That is the point. |
| Invent actuators (STREAM, Kill Span, Hold & Re-verify, Redact & Flag) | Forbidden. Actuators are exactly Block · Edit · Escalate · Pass. |
| Quote 40 ms as p95 | ≤40 ms p50 / ≤200 ms p95. Quoting 40 as p95 is a five-fold overclaim, dead on contact. |

---

## 9. Fidelity Self-Check

Explicit confirmation that the pitch architecture protects every major invariant from Stages 1–4:

| Invariant | Protected where |
|---|---|
| Default = UNSUPPORTED | Demo Beat 3b — all claims born UNSUPPORTED; C2 stays UNSUPPORTED |
| Entitlement = set-membership, zero LLM | Demo Beat 3b (C3) + Beat 3e (principal flip) |
| Exact 4×4 R×S matrix, never redrawn | Demo Beat 3c — cells shown before actuators |
| One graph: STEP → SPAN → CLAIM → ACTION | Beat 2 (thesis) + Demo (ledger shows the graph) |
| Hard gate on actions, not tokens | Cold open (`executed: false`) + Demo Beat 3d (executor) |
| Dual-action: R1 Edit + R3 Escalate held, never "blocked" | Demo Beat 3c — both simultaneous, language verified |
| UNKNOWN never → SUPPORTED | Implicit in claim routing; stated in Beat 2 |
| FNR typed format, empty until earned | Demo Beat 3f — null placeholders, no fabricated % |
| Bias = async route-level only | Beat 4 (refuse-to-claim) — stated in measurement terms; never a live route |
| Refuse-to-claim (about us) | Beat 4 — four refusals delivered explicitly |
| Exactly two Stage 1 live routes | Demo shows refund + knowledge (principal flip); no third route |
| Latency ≤40 ms p50 / ≤200 ms p95 | Stated correctly if pressed; never quoted as 40 p95 |
| Speculative verification OK, speculative release forbidden | Implicit in `executed: false` during Escalate |
| Surgical edit + evidence packet | Demo Beat 3c–3d — strip C3, packet for C2 |
| Lane 1 always on | Stated in architecture beat; entitlement is deterministic |
| Locked R3 classes | Refund is R3 by construction; shown in cold open |
| Vocabulary compliance | Full pitch uses authorise/admit/prove/bind/refuse/hold/escalate/gate |
| Opening on held transaction, not risk | Cold open — transaction log before any spoken word |
| Closing resolves opening | Beat 7 — "never asked to prove anything" → "nothing acts until it can prove it should" |
| No fabricated ROI or percentages | Business case uses mechanism → consequence; no "99%" |
| Proof scales with consequence | Demo Beat 3c — same verdict, different R, different actuator |
| "Retrieval ≠ permission" | Differentiation Moment 2 — stated explicitly |
| Content law: Clause 7.2 does not exist; absence ≠ conflict; company wrongly pays | Opening Beat — stated verbatim |
| Content law: held ≠ blocked | Demo Beat 3c + 3d — language verified throughout |

**No invariant is reopened. No frozen decision is overridden. The pitch is a rendering of the architecture, not a reinterpretation of it.**

---

*End of Stage 5: Pitch Architecture. This file is the structural spine from which the pitch presentation is built. Every slide, every spoken line, every screen state derives from this document and the frozen stack it renders.*