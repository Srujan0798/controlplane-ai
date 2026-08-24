# ControlPlane.ai — Round 2 Stage 5 (Pitch Architecture)

> **Sources of truth (absolute, eternal):** `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` · `R2S2.md` · `R2S3.md` · `R2S4.md` (Dense Hybrid — `e8d16814`) · Official brief (`docs/ps.md`).
>
> **Status:** This file designs the **only** remaining artifact — the live pitch presentation. Stages 1–4 are **not reopened**. No technical, scope, or value decision is re-litigated. The pitch renders the frozen architecture, does not edit it.
>
> **Operating claim of this file:** the pitch is the prototype, the prototype is the pitch, and the slides are scaffolding. If the demo is removed and the deck still works, the pitch has failed.

---

## 0. Reading Order for the Pitch Team

Read this file in this order before writing a single slide:

1. §1 — the thesis. Memorise it. It is the only sentence that must be on your tongue at the door of the room.
2. §2 — the structure. This is the spine; everything else hangs off it.
3. §3 — the opening beat. This is the first 60–90 seconds and it sets the frame. Get this right or nothing else lands.
4. §4 — the demo spine. The dual-action is the centrepiece. Everything else in the pitch either leads into it or follows from it.
5. §5 — the business case. The smallest, sharpest integration of value, not a consulting deck.
6. §6 — the differentiation and defence moments. The two or three places we land the contrast.
7. §7 — the closing beat. The resolve of the opening.
8. §8 — anti-patterns. The hard kill list. Tape this next to the laptop.
9. §9 — fidelity self-check. Run this before the pitch leaves the door.
10. Appendix A — the one-page speaker crib. Take it on stage.
11. Appendix B — the slide-by-slide render (deck as a thin render of the spine, not a separate document).

---

## 1. Pitch Thesis (the one sentence that must survive the room)

> **An AI response is not text to be scored — it is a set of claims requesting permission to act. ControlPlane captures the evidence the model was given, inverts the burden of proof, carries identity into verification, and hard-gates the commit path so an unproven or unauthorized claim cannot authorize an action — and publishes the rate at which it misses.**

Three movements, in this order, every time:

1. **Reclassify the failure.** The failure is not a hallucination, not a bias, not a privacy leak. The failure is an **authorisation failure** — an unproven claim was allowed to authorize an irreversible action. Every other "AI safety" frame misses this.
2. **Name the primitive.** One graph: `STEP → SPAN → CLAIM → ACTION`. Three reads, not three products. Provenance is captured **outside** the model. Default is `UNSUPPORTED`. Entitlement is set-membership, not classification. The matrix prices proof by consequence.
3. **Name the asymmetry.** They publish precision — the rate at which they bother the user. We publish misses — the rate at which we missed. The plane is audited by the standard it enforces.

This is the only thing the judges have to remember on the way out.

---

## 2. Overall Pitch Structure (10 minutes, three-act spine)

| # | Section | Time | Function | Mode |
|---|---|---|---|---|
| 0 | Pre-room (before the timer starts) | — | Stage is set. Evidence Ledger open at ≥ 60% viewport. Held-refund status card visible. | Live demo, idle |
| 1 | **Opening beat — the held transaction** | 0:00–1:15 | Establish the category change. Hook the room. | Live demo, narrated |
| 2 | **Indictment + thesis** | 1:15–2:15 | Land the structural failure + the three-movement thesis. | Live demo continues, narration tightens |
| 3 | **Mechanism in 60 seconds** | 2:15–3:15 | The graph + the matrix + the actuator set. One pass, no deep dive. | Live demo continues; matrix cell highlighted |
| 4 | **Dual-action demonstration — the centrepiece** | 3:15–6:30 | R1 Edit on text + R3 Escalate (held) on refund. Same response, same graph, two actuators. Hold the moment. | **Live demo, full screen, slowed** |
| 5 | **Second beat — principal flip** | 6:30–7:15 | Same claim, different principal. Authorization is set-membership, not text classification. | **Live demo, live re-run** |
| 6 | **Business case — the smallest possible integration** | 7:15–8:30 | Beachhead, integration cost, mechanism → consequence, shadow default. **No ROI percentages. No 99% claims.** | Slides, but the live demo remains on screen |
| 7 | **Differentiation + refuse-to-claim** | 8:30–9:15 | Three sharp contrasts. The miss-rate posture. | Slides, with the FNR empty schema on screen |
| 8 | **Closing beat** | 9:15–9:45 | The resolve of the opening. | Live demo returns to the held refund |
| 9 | **Q&A handoff (1 beat)** | 9:45–10:00 | "B1 and B5 are the two we drilled." | Live demo, frozen on the held refund |

**Total: 10:00.** This is the ceiling. The demo is the pitch; the slides never run longer than 75 seconds in a single block.

**Why 10 minutes, not 12:** the dual-action moment is the centrepiece and it cannot survive if it is rushed. Cutting optional material is cheaper than cutting the centrepiece. The optional third beat (R-tier consequence change) is **deleted by default** — included only if the team has rehearsed it under 8:30 and the room is engaged.

**Why the live demo carries the spine, not slides:** the prototype is the strongest argument. A slide that says "hard gate on actions" is a claim. A live demo that holds a ₹1,84,000 refund at `committed: false` is **proof**. The room will not remember the slide; the room will remember the moment the refund was held.

---

## 3. Opening Beat (0:00–1:15) — the held transaction

**The most important 75 seconds of the pitch. Frame the room here or never.**

### 3.1 What is on screen when the timer starts

The Evidence Ledger is open, idle, empty. The held-refund status card is at the centre of the screen, in the dominant viewport. It reads:

```
┌──────────────────────────────────────────────────────────┐
│  ACTION GATE                                              │
│                                                          │
│   refund.execute                                         │
│   order:    ORD-1023                                     │
│   amount:   ₹1,84,000                                    │
│   reason:   "under clause 7.2"                           │
│   status:   HELD — ESCALATE                              │
│   executed: false                                        │
│                                                          │
│   R3 × unsupported-categorical                          │
└──────────────────────────────────────────────────────────┘
```

This is **not** a slide. This is the live demo, idle, before the user has said a word. The judge sees the gate **before** the presenter speaks.

### 3.2 What the presenter says (preferred opening lines — chosen for first impact)

> **"Here's a refund the system is about to issue. One lakh eighty-four thousand rupees. Watch what happens."**

Pause. 1–2 seconds. The room sees the held status. The presenter then adds:

> **"It used to be a bad paragraph. It's now an executed transaction."**

Pause again. Then:

> **"Clause 7.2 doesn't exist. The model said it did. Every filter passed it. Confidence read 0.94. The refund was held — not blocked — held, with the evidence packet, because the system was asked to prove it before it acted."**

### 3.3 What the opening beat is doing, mechanically

- **Reframes the failure in one sentence.** "It used to be a bad paragraph. It's now an executed transaction." This is the line that makes the room understand *why this is a different problem now, not a different angle on the same problem.*
- **Opens on a transaction, not a person.** No shocked customer, no angry email, no "AI is risky" hand-waving. A rupee figure with a held status. The danger is implied by the money.
- **Names the difference.** "Held — not blocked." This pre-empts the one word the judges will be listening for. It also pre-empts the most common Q&A trap.
- **Sets the vocabulary in 60 seconds.** Held, evidence packet, prove, action — not monitor, detect, watch, guard.

### 3.4 What the opening beat must NOT do

| Forbidden | Why |
|---|---|
| Open on a person, a shocked customer, an angry email, a "scary AI" illustration. | The category noun is **admission-control**, not customer-service. The opening is structural, not emotional. |
| Open on "AI is powerful but risky…" | The first line of every other guardrail deck in the room. Sets the generic-AI-safety frame before you have said anything of your own. |
| Open on a slide that says "About Us" or "The Team" or "The Market." | The room has seen those slides forty times today. The held refund is unrepeatable. |
| Open on a definition of hallucination, bias, or privacy. | The thesis reclassifies the failure. Don't let the opening re-import the categories the thesis is about to dissolve. |
| Open on the word "response" instead of "claim." | The first sentence of the pitch must contain the word **claim**. *An AI response is a set of claims requesting permission to act.* The room's working noun is now "claim," not "response." |
| Open on the matrix, the architecture diagram, or the team. | The matrix is for the mechanism beat. The team is irrelevant in the first 60 seconds. |
| Open on a smile and "Hi, we're Team ControlPlane and we're excited to be here." | Burns the irreplaceable first 5 seconds on a sentence that adds no information. |

### 3.5 The line that earns the room (deployable at 0:45–0:55, optional)

> **"The system didn't fail. It was never asked to prove anything."**

This is the indictment. It is the one sentence that turns the room from "watching a demo" to "watching an argument." Use it as a hinge between the held-refund reveal and the thesis. Do not use it twice.

---

## 4. Prototype Demonstration Spine (3:15–6:30) — the dual-action, built backward from the action gate

This is the centrepiece. The whole pitch is in service of this 3:15. The slides are scaffolding for it; the business case is the consequence of it. If this section is rushed, the pitch is over.

### 4.1 Demo order (with timing, narrators' words, screen states)

| Beat | Time | Screen | What the presenter says | What the room sees |
|---|---|---|---|---|
| **4.1.a** Cold re-open on the action gate | 3:15–3:25 | Held-refund card returns to the centre of the screen, in full view. The Evidence Ledger is on the right or below, dominant. | *"Let's re-run this and watch the gate."* | The action. The rupee figure. The held status. |
| **4.1.b** Provenance populates first | 3:25–3:50 | The `SPAN` pane populates with ~14 rows. Each row: `source_id`, truncated text, `ACL`, `content_hash` (8 chars), `offsets`, `principal`. The internal runbook is visibly tagged `ACL: role:finance` while the principal is `role:support`. | *"Before any claim is judged, every span the model was allowed to know is on screen — source, ACL, hash, offsets. The model did not write any of this. We wrote it, outside the model, at context assembly."* | Spans with provenance metadata. The provenance pane is **larger** than the claim pane. |
| **4.1.c** Claims extract, all UNSUPPORTED | 3:50–4:10 | The `CLAIM` pane populates. Three claims, all red. C1 = amount/order, C2 = "clause 7.2 permits this refund", C3 = grounded on FIN-INTERNAL. | *"Every claim starts UNSUPPORTED. It must earn proof. C1 is the amount. C2 is clause 7.2. C3 is a sentence grounded on the internal runbook."* | Three red claims. The colour **red** is the default, not the exception. |
| **4.1.d** Binding runs against the captured set | 4:10–4:40 | The `BINDING` pane runs. C1 binds to `ORD-1023` → green. C2 finds no span → stays red. C3 finds a span, but the binding is orange — the ACL on the span excludes the principal. | *"C1 binds. C2 doesn't — there's no clause 7.2 in the captured set. C3 binds, but the span's ACL excludes the calling principal. The binding is the same operation; the authorization is the question we ask next."* | Three binding states: green, red, orange. Three different verdicts on three different grounds. |
| **4.1.e** Matrix cells highlight, **before** actuators | 4:40–5:10 | The `MATRIX` pane shows the frozen 4×4. Two cells highlight in sequence: `R1 × entitlement` first, then `R3 × unsupported-categorical`. Each cell is shown with its exact wording — no invented labels. | *"R1, entitlement violation — the text path. R3, unsupported categorical — the refund path. Two cells. Two actuators. Same response, same graph."* | The literal matrix. Two cells. No "blocked." No "danger." No red exclamation. |
| **4.1.f** R1 Edit fires on the text path | 5:10–5:30 | A diff appears. C3 is stripped from the text. The text is re-gated. The gate passes. | *"Surgical edit. Only the failing claim. The text re-enters the gate and passes."* | A clean diff. The text re-verified. |
| **4.1.g** R3 Escalate (held) fires on the refund — the centrepiece | 5:30–6:00 | The action status flips to red. The evidence packet opens by default: claim, candidate spans (empty for C2), verdict, diff. The mock refund tool logs `commit_refused: gate=Escalate, action=refund.execute`. The refund action row reads **"refund held and escalated with the evidence packet."** | *"Same response. Same graph. A different pending action, a different consequence. The refund is not executed. The refund is held. The packet is the deliverable. This is the matrix doing something more sophisticated than a single lookup."* | The held refund. The packet. The empty `executed: false`. **Hold here for two full seconds in silence.** |
| **4.1.h** The hold | 6:00–6:15 | The screen stays on the held refund and the packet. No words. | *(silence)* | The held rupee figure. The packet. The two seconds are the most important two seconds of the pitch. |
| **4.1.i** Ledger close | 6:15–6:30 | The `LATENCY` strip and the `POLICY_VERSION` strip become visible. The matrix cell highlight stays. | *"The action was held. The packet is the deliverable. The matrix cell is logged. The policy version is logged. The principal is logged. The latency is logged. Any decision, traced end to end."* | The full ledger. Traced. |

**The 6:00–6:15 silence is non-negotiable.** It is the moment the room understands what was just demonstrated. It is also the moment the room remembers. Do not speak through it. Do not let a co-presenter fill it. Two seconds of silence is the cheapest and most powerful move in the whole pitch.

### 4.2 Anti-patterns for the demo (the build team and the pitch team both know these)

| Forbidden during the demo | Why |
|---|---|
| The presenter saying "blocked" about the refund. | The matrix routes R3 × unsupported-categorical to **Escalate**, not Block. The refund is **held and escalated with the evidence packet.** Say it once. Say it correctly. |
| Letting the chatbot chrome dominate the screen. | The chatbot is the chrome, not the centre. The ledger is ≥ 60% of the viewport. If a judge can remove the ledger and the demo still looks like a chatbot, the demo has failed. |
| Calling the held status "blocked" or "denied" or "rejected" or "refused." | All four words are wrong. The status is **held**. The actuator is **Escalate**. The action is **not committed** (`executed: false`). |
| Showing a confidence score, a trust score, a risk score, a safety score. | These are forbidden categories. The interlock does not read any field with these names. |
| Showing the judge a "block list" or "deny list" of banned phrases. | Static guardrails are the rejected category. The plane enforces a typed action grammar, not a word list. |
| Showing the bias measurement on screen as a per-response verdict. | Bias is route-level async. It is in the business proposal, not on the demo screen. |
| Reading a slide during the demo. | The demo is the deck. Slides during the demo break the spell. The slides return at 7:15. |
| Letting the live re-run sit still or be obviously pre-baked. | The principal flip (§5) must visibly re-run with binding latency ≥ 50 ms, so a hostile judge cannot dismiss the whole path as a recording. |

### 4.3 What "looks like a recording" feels like, and how to defeat it

A hostile judge will say one of three things after the demo:

1. *"That looked pre-recorded. Did the binding actually run?"*
2. *"I want to see the same request, same claim, different principal, and the actuator flip live."*
3. *"What's the latency of the binding path?"*

**Defeats for all three, in order:**

1. The principal flip at 6:30–7:15 is the live re-run. It is **not** a re-play of a recorded trace. The presenter changes **only the principal** and the binding runs again. The latency strip updates in real time. The matrix cell highlight re-fires.
2. The presenter invites the judge to name any other principal. *"Pick a principal. We'll re-run."* The team has a hotkey for `principal = <judge's pick>` and the demo re-runs.
3. The latency strip is on screen **permanently** during the demo. The numbers are demo-machine numbers, labelled as such. The architecture's targets are stated separately, in the slide at 8:00: *≤40 ms p50 / ≤200 ms p95 added on R0/R1 text. Action gate amortised inside tool RTT. Speculative verification OK; speculative release forbidden.*

---

## 5. Business Case Integration (7:15–8:30) — the smallest possible integration of value

The business case is the consequence of the demo, not a separate act. It lands in **75 seconds** and is delivered as a consequence of the dual-action moment, not as a consulting pitch.

### 5.1 What the slides show, in order (each slide is a single sentence + one diagram)

| Slide | Single sentence | Diagram | Time |
|---|---|---|---|
| **B1 — Where does this land?** | *"Beachhead = high-consequence routes: refund-class R3 + mixed-governance knowledge. Not 'all enterprise AI safety.'"* | A 2×2 of (R-tier × use case) with two cells highlighted: refund, knowledge. | 7:15–7:25 |
| **B2 — What does it cost to deploy?** | *"Days, not quarters. One SDK hook where you already assemble context. One OpenAI-compatible reverse proxy. No weights, no logits, no fine-tuning. The integration cost is the moat — and we say so."* | A 2-component integration diagram: hook + proxy. | 7:25–7:40 |
| **B3 — What does it buy?** | *"R3 held at `executed: false` is structural escape from wrong actions. No percentage on a slide. The mechanism is the number: a wrong action that cannot execute is a wrong action that does not happen."* | A before/after with the held refund. | 7:40–7:55 |
| **B4 — How is it operated?** | *"Shadow by default. Enforcement earned, per route, from counterfactual evidence — never switched on enterprise-wide from a slide. Misses published per route, every phase."* | The 5-phase roadmap (Prototype → Shadow → Canary R0/R1 → Limited R2/R3 → Broader envelope). | 7:55–8:15 |
| **B5 — What does the auditor see?** | *"Hash-chained ledger. Versioned policy. Reconstruct any actuator: action → cell → verdict → span → source/ACL → principal → policy version → latency. The regulator answer is a pointer."* | The drill-down chain. | 8:15–8:30 |

### 5.2 The integration rules (the things that turn a pitch into a consulting deck, and the kills)

| Consulting-deck tells | Replacement |
|---|---|
| "Total addressable market: $X billion." | None. Delete the slide. |
| "We project ₹Y in cost savings in year 1." | "The mechanism is the number. A wrong action that cannot execute is a wrong action that does not happen." |
| "Our competitive moat is…" | "The integration cost is the moat. We say so out loud, because a team that discovers the integration cost *after* being sold 'drop-in' churns." |
| "Phased delivery: Q1, Q2, Q3…" | "Shadow → canary → enforce. Earned per route, not switched on enterprise-wide." |
| "We have a 5-year CAGR of…" | None. Delete the slide. |
| "Our customers include…" | "We have one customer: the route. Day-one posture is shadow." |
| "Personas: the CISO, the CTO, the CFO…" | "Who pays when it fails ≠ who runs it ≠ who types the answer." (One sentence.) |
| "ROI calculator: enter your traffic to see savings." | "We do not put a savings percentage on a slide, because we have not measured it on your traffic. What we can do from day one is name the exact spend that grounded nothing." |

### 5.3 The line that earns the business-case beat

> **"The buyer question a sceptic can answer without our slide is this: *what consequential actions does this route perform today, what is the loss if one is wrong, and what fraction can sit behind an earned admission boundary?*"**

This is the line that turns the business case from a vendor pitch into a buyer's own diagnostic. It is the only line in the business-case section that must be memorised. It is also the line that makes the slide feel like a tool, not an argument.

### 5.4 What the business-case section must NOT do

- **Lead with enablement.** *"We help enterprises unlock the value of generative AI…"* is the first line of every consulting deck. ControlPlane is **infrastructure**, not enablement. The category noun is **admission-control layer**.
- **Promise a percentage saved.** Tail risk is not average case. The exposure is `freq × P × loss`. The plane publishes the `P` (FNR) per route, and the buyer fills the rest.
- **Promise "99% accuracy" or "eliminate hallucinations."** Refuse-to-claim list, about us, not competitors.
- **Talk about the team.** The team is irrelevant to the architecture. The architecture is the answer to the team question, and the architecture is on screen.
- **Talk about "responsible AI."** Forbidden as a standalone virtue. *"Deterministic entitlement check" is allowed.* *"Responsible AI" is the category we are refusing to compete in.*
- **Cycle through three shallow scenarios.** One case, all the way to the bottom.

---

## 6. Differentiation & Defence Moments (8:30–9:15) — the three sharp contrasts

The differentiation beats are **not** a "vs competition" slide. They are the moments where the architecture's contrast with the rejected categories is delivered as an argument, not a chart. There are exactly three. The fourth is the miss-rate posture. **Total: 45 seconds.**

### 6.1 The three contrasts, in order

| # | Contrast | Spoken line | What is on screen |
|---|---|---|---|
| **6.1.a** | **vs observability (LangSmith, Arize, Helicone, WhyLabs)** | *"Observation without commit control is an audit trail, not architecture. They tell you what went wrong after a user acted on it. The plane interlocks the commit path and records the entrance, not the exit. Same graph, exact dead compute — they tell you the trace cost ₹8; we tell you ₹5 of it grounded nothing."* | The held refund card. The graph on the left. The ledger says `step_yield: 5/9 grounded; dead_compute: 4/9`. |
| **6.1.b** | **vs LLM-as-judge / static guardrails (NeMo Guardrails, LlamaGuard, Lakera)** | *"The judge asks 'does this look right?' — an unfalsifiable question. We ask 'which span proves it?' — a query with an answer. Decision time is a pure rule engine. Entitlement is identity, not classification. Default UNSUPPORTED is posture, not a threshold tweak."* | The matrix cell highlight on the held refund. The `default_verdict: UNSUPPORTED` policy field visible. |
| **6.1.c** | **vs RAG groundedness (the closest cousin)** | *"Groundedness checkers see retrieval only — not tool results, DB rows, computed values or system context, which is where agents actually get their facts. They average, so one wrong figure drowns in nine correct sentences. They are action-blind, so 0.82 means the same thing on a draft and on a wire transfer. And none of them carry caller identity, so none of them can do entitlement at all. **Retrieval is not permission.**" | The principal flip replay. Same claim, same source, different principal, different actuator. |

### 6.2 The refuse-to-claim posture (the fourth beat, 8:55–9:10)

This is **not** a "vs competition" beat. This is the moment the plane disclaims **itself**. It is the rarer and stronger move.

> **"We do not claim to eliminate hallucinations. We do not claim zero integration. We do not claim zero added latency. We do not claim one accuracy number across three failure modes. The narrower, harder claim is this: an unproven or unauthorized claim cannot authorize an action — and we publish the rate at which we missed."**

The FNR schema is on screen. All measurement fields are `null`, `insufficient_sample`, or `prototype_corpus`. The schema is the claim. The values are earned per route, after shadow evidence. They are not on a slide.

### 6.3 What the differentiation section must NOT do

- **Name products to feel safe.** Naming real products is a differentiator only if it indicts what they cannot do. *"LangSmith" in the same breath as "audit trail, not architecture"* is the move. *"LangSmith" in the same breath as "we are better"* is generic.
- **Use a feature comparison table as the deliverable.** The three contrasts are spoken lines with one screen state each. No 12-row matrix of features.
- **Use superlatives.** *Best, leading, only, first.* The architecture speaks for itself; the words don't help.
- **Spend more than 45 seconds on differentiation.** Differentiation is a single argument, not a section. The pitch is about the architecture, not the rivals.
- **Imply that the rivals are bad people.** They are addressing different problems with different primitives. The plane is the right primitive for a different problem. *The system didn't fail. It was never asked to prove anything.*

---

## 7. Closing Beat (9:15–9:45) — the resolve of the opening

### 7.1 What is on screen

The held-refund status card returns to the centre of the screen. The matrix cell highlight stays. The evidence packet is collapsed. The room sees the rupee figure and the held status one more time.

### 7.2 What the presenter says (preferred closing lines)

> **"That system was never asked to prove anything."**

Pause. One second. The opening's indictment, returned.

> *"Watch."*

The presenter clicks once. The matrix cell highlight re-fires. The held status remains. The mock refund tool's `commit_refused` log is visible. The refund is still held.

> **"Now nothing acts until it can prove it should."**

Pause. The room holds.

> *"That's ControlPlane. Thank you."*

### 7.3 What the closing beat is doing, mechanically

- **Resolves the opening's indictment in the same verb.** "Never asked to prove" → "now acts until it can prove." The closing is not a summary; it is the answer to the opening.
- **Re-fires the matrix cell highlight on stage, in front of the room.** Not a recording. Not a slide. A live action. The held refund stays held. The room sees it.
- **Ends on a single declarative line.** No CTA. No "we'd love to talk to you." No "questions?" until the timer expires. The architecture is the CTA.
- **Hands off to Q&A cleanly.** *"That's ControlPlane. Thank you."* Two beats. No sales.

### 7.4 What the closing beat must NOT do

| Forbidden | Why |
|---|---|
| "Thank you for your time. We are excited to…" | The closing is the answer to the opening. Sales is the wrong register. |
| "Any questions?" before the timer | Burns the last 10 seconds. Q&A starts at 9:45. |
| "In summary, we have shown you…" | The room is not taking notes. The held refund on screen is the summary. |
| Showing a list of features, a roadmap, or a "next steps" slide. | The closing is the held refund. Anything else dilutes it. |
| Speaking over the silence. | Two seconds of silence after "now nothing acts until it can prove it should" is the closing. |
| "We hope you enjoyed…" | The room is the judge. The architecture is the only thing that should be enjoyed. |

---

## 8. Anti-Patterns — the Hard Kill List

Tape this next to the laptop. Any of these appearing in the pitch is grounds for a stop-build.

### 8.1 Opening anti-patterns

| # | Anti-pattern | Why it kills |
|---|---|---|
| 1 | Open on "AI is powerful but risky…" | First line of every other guardrail deck. Sets the generic-AI-safety frame before you have said anything of your own. |
| 2 | Open on a person, a shocked customer, an angry email, a "scary AI" illustration. | The category noun is admission-control, not customer-service. The opening is structural, not emotional. |
| 3 | Open on a slide titled "About Us" / "The Team" / "The Market" / "The Problem." | The held refund is unrepeatable. Wasting the first 60 seconds on slideware the room has seen forty times today. |
| 4 | Open on a definition of hallucination, bias, or privacy. | The thesis reclassifies the failure. Re-importing the categories the thesis is about to dissolve is a direct loss. |
| 5 | Open with the word "response" instead of "claim." | The first sentence of the pitch must contain the word **claim**. *An AI response is a set of claims requesting permission to act.* The room's working noun is now "claim," not "response." |
| 6 | Open with a smile and "Hi, we're Team ControlPlane and we're excited to be here." | Burns the irreplaceable first 5 seconds on a sentence that adds no information. |

### 8.2 Demo anti-patterns

| # | Anti-pattern | Why it kills |
|---|---|---|
| 7 | Saying "blocked" about the refund. | The matrix routes R3 × unsupported-categorical to **Escalate**, not Block. The refund is **held and escalated with the evidence packet.** This is a load-bearing content law. |
| 8 | Letting the chatbot chrome dominate the screen. | The governing test (R2S3 §6): *if the judge can remove the graph from the screen and the demo still looks the same, the scope has already failed.* |
| 9 | Showing a confidence score, trust score, risk score, or safety score. | Forbidden categories. The interlock does not read any field with these names. The demo must not either. |
| 10 | Showing the LLM-as-judge pane, the open-web lookup pane, or the bias widget. | LLM-as-judge is the rejected category. Open-web lookup is the rejected category. Bias is route-level async — not a per-response widget. |
| 11 | Reading a slide during the demo. | The demo is the deck. Slides during the demo break the spell. The slides return at 7:15. |
| 12 | The demo looks pre-baked or pre-recorded. | The principal flip must visibly re-run with binding latency ≥ 50 ms. The matrix cell highlight must re-fire. The latency strip must update. |
| 13 | Collapsing the dual-action into one "response blocked" verdict. | The whole pitch is the dual-action. Collapsing it is the most expensive single failure. |
| 14 | Calling the held status "blocked" / "denied" / "rejected" / "refused" / "stopped." | The status is **held**. The actuator is **Escalate**. The action is `executed: false`. Say the words the architecture says. |
| 15 | The matrix cell highlight firing *after* the actuator. | The matrix cell must be visible *before* the actuator row. Otherwise the room sees a verdict without seeing the cell that produced it, and the architecture reads as a black box. |
| 16 | The "evidence packet" being a bare alert, a log line, or a JSON blob. | The packet is the deliverable. Claim + candidate spans + verdict + diff. The room must see the four fields, not a notification. |
| 17 | Letting the live re-run sit still. | The principal flip is the live-re-run proof. The presenter must invite the judge to name any other principal and re-run. |
| 18 | The chatbot UI showing "I have refunded ₹1,84,000" as if the refund went through. | The chat pane is **the chrome**. The text is **edited** at the matrix cell. The chat pane shows the post-Edit text, not the model's pre-Edit text. The chat pane is a **renderer** of the gate's output, not of the model's output. |

### 8.3 Business-case anti-patterns

| # | Anti-pattern | Why it kills |
|---|---|---|
| 19 | Total addressable market, CAGR, or any market-sizing slide. | The category is admission-control, not analytics. TAM/CAGR is the language of vendors, not infrastructure. |
| 20 | Projected savings / "we'll save you ₹X in year 1." | Tail risk is not average case. The plane publishes the FNR per route. The buyer fills the rest. |
| 21 | "Phased delivery: Q1, Q2, Q3…" | "Shadow → canary → enforce. Earned per route, not switched on enterprise-wide." |
| 22 | Personas: CISO, CTO, CFO, CDO, … | "Who pays when it fails ≠ who runs it ≠ who types the answer." (One sentence.) |
| 23 | Talking about the team, the founders, or the journey. | The architecture is the answer to the team question. The team is irrelevant in 10 minutes. |
| 24 | Talking about "responsible AI" as a virtue. | "Responsible AI" is the category we are refusing to compete in. The category noun is admission-control. The forbidden list is on the wall. |
| 25 | Cycling through three shallow scenarios. | One case, all the way to the bottom. Breadth reads as slideware; depth reads as production experience. |
| 26 | An "ROI calculator" or "savings estimator" on a slide. | "We do not put a savings percentage on a slide, because we have not measured it on your traffic." |
| 27 | A "Customer Logos" or "Trusted By" slide. | "We have one customer: the route." |

### 8.4 Differentiation anti-patterns

| # | Anti-pattern | Why it kills |
|---|---|---|
| 28 | A 12-row feature comparison table as the differentiation deliverable. | The three contrasts are spoken lines. A table is a vendor artifact, not an argument. |
| 29 | Using superlatives: *best, leading, only, first, most advanced.* | The architecture speaks for itself. Superlatives are the language of vendors. |
| 30 | Naming real products to feel safe. | Naming real products is a differentiator only if it indicts what they cannot do. The contrast must be structural, not ad hominem. |
| 31 | Spending more than 45 seconds on differentiation. | Differentiation is a single argument, not a section. |
| 32 | Claiming a percentage saved vs a named competitor. | The plane publishes its own FNR. The plane does not publish a competitive benchmark. |

### 8.5 Closing anti-patterns

| # | Anti-pattern | Why it kills |
|---|---|---|
| 33 | "In summary, we have shown you…" | The held refund on screen is the summary. |
| 34 | "Thank you for your time. We are excited to…" | The closing is the answer to the opening. Sales is the wrong register. |
| 35 | "Any questions?" before the timer. | Burns the last 10 seconds. Q&A starts at 9:45. |
| 36 | A "Next Steps" or "Contact Us" slide. | The closing is the held refund. Anything else dilutes it. |
| 37 | Speaking over the silence. | Two seconds of silence after "now nothing acts until it can prove it should" is the closing. |

### 8.6 Voice-and-vocabulary anti-patterns (forbidden throughout)

| # | Anti-pattern | Replacement |
|---|---|---|
| 38 | "monitor" / "observe" / "watch" / "detect" / "guard" | authorise · admit · prove · bind · refuse · hold · escalate · gate |
| 39 | "trust score" / "risk score" / "safety score" / "confidence score" | verdict · binding · entitlement · blast radius |
| 40 | "guardrails" / "observability layer" | admission-control layer · permission layer |
| 41 | "responsible AI" / "ethical AI" / "trustworthy AI" as standalone virtues | deterministic entitlement check · ACL violation |
| 42 | "AI safety" as a product category | "admission control" (the category noun) |
| 43 | "block" or "deny" or "reject" or "refuse" applied to the refund | **held and escalated with the evidence packet** |
| 44 | "block list" / "deny list" / "banned phrases" | typed action grammar (allow-list) |
| 45 | "we eliminate hallucinations" / "we detect 99% of bias" / "we prevent privacy leaks" | unproven claims cannot authorize actions · we publish what we missed |
| 46 | "drop-in" / "zero integration" / "frictionless" | "the integration cost is the moat — and we say so" |
| 47 | "real-time ground truth" / "fully accurate verification" | "no real-time ground truth; we publish the FNR per route" |
| 48 | "AI agent" used as the subject of a verb in the first 60 seconds | "claim" — the agent is a context, not a subject, in the opening |
| 49 | "we caught X%" | the FNR is empty until earned; the schema is the claim |
| 50 | "we ensure compliance" / "we make AI safe" | the architecture makes an unproven or unauthorized claim unable to authorize an action — that is the only claim |

**The one permitted exception to the voice ban:** *"Everyone watches the exit. Nobody records the entrance."* This is permitted because it indicts what everyone else built. It is a kill shot, used once, at the indictment beat (1:30–1:50). It is not a generic claim about AI risk.

---

## 9. Fidelity Self-Check

Explicit confirmation that this pitch architecture protects every eternal invariant from the frozen stack.

### 9.1 The ten eternal invariants

| # | Eternal invariant | Status in this pitch | Where protected |
|---|---|---|---|
| 1 | **Default = UNSUPPORTED** | Untouched. The demo starts with three red claims. The presenter names it: *"Every claim starts UNSUPPORTED. It must earn proof."* | Demo beat 4.1.c. |
| 2 | **Entitlement = `span.acl ⊆ principal.clearance`; zero LLM** | Untouched. The principal-flip re-run is the proof. *"Zero LLM made that decision. It cannot be made by an output-scorer that doesn't carry identity into the verification layer."* | Demo beat 4.1.d; second beat 6:30–7:15. |
| 3 | **Exact R×S matrix; never redrawn; no route parameter** | Untouched. The matrix is on screen, literal, with two cells highlighted. The text of the cells is the text of the matrix. No invented labels. | Demo beat 4.1.e. |
| 4 | **One graph: `STEP → SPAN → CLAIM → ACTION`** | Untouched. The graph is the dominant UI. Performance, cost, responsibility are three reads. | UI requirements §4.2; demo beats 4.1.b–4.1.i. |
| 5 | **Hard gate on actions, not tokens** | Untouched. The action gate is the cold-open. The refund is held at `executed: false`. | Demo beats 3.1, 4.1.a, 4.1.g. |
| 6 | **Dual-action: R1 Edit + R3 Escalate held, never "blocked"** | Untouched. The whole pitch is the dual-action. *"Held, not blocked"* is the line at 0:55. The vocabulary kill list (§8.6 #43) is enforced. | Demo beats 4.1.e–4.1.h; anti-patterns §8.2 #7, 14. |
| 7 | **`UNKNOWN` never → `SUPPORTED`** | Untouched. The architecture's verdict set is the verdict set. The binder emits `SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN`. The policy refuses `UNKNOWN → SUPPORTED`. The pitch does not soften this. | Demo beat 4.1.d; architecture carries the invariant. |
| 8 | **FNR as typed format; empty until earned** | Untouched. The FNR schema is on screen at the differentiation beat. All measurement fields are `null` or `prototype_corpus`. The values are not on a slide. *"We do not claim to eliminate hallucinations. We publish the rate at which we missed."* | §6.2; demo beat 4.1.i. |
| 9 | **Bias = async route-level only (never live matrix cell)** | Untouched. Bias is **not** on screen as a per-response verdict. Bias is named in the business case as a measurement program, not a product. | §5.1 (B1–B5 do not show bias on screen). |
| 10 | **Refuse-to-claim (about *us*, not competitors)** | Untouched. The refuse-to-claim posture is the fourth beat at 8:55–9:10. It is delivered as the plane disclaiming itself, not as a comparison with rivals. | §6.2; anti-patterns §8.6 #45. |

### 9.2 The content laws

| # | Law | Status in this pitch | Where protected |
|---|---|---|---|
| 1 | **Clause 7.2 does not exist.** | Untouched. The opening line at 0:30–0:45 names it. *"Clause 7.2 doesn't exist. The model said it did."* | Opening beat §3.2. |
| 2 | **Held ≠ blocked.** | Untouched. The pitch uses the word **held** consistently. The kill list forbids "blocked about the refund" anywhere in the pitch. | §3.2; §8.2 #7, 14; §8.6 #43. |
| 3 | **Who pays.** | Untouched. The framing throughout is **the company wrongly pays out** (not "the customer lost money"). | R2S4 §1 carries the framing; pitch inherits. |
| 4 | **Dual action simultaneously.** | Untouched. R1 Edit on text + R3 Escalate held on refund, same response, same graph. | Demo beats 4.1.e–4.1.g. |
| 5 | **Latency ≤40 ms p50 / ≤200 ms p95.** | Untouched. Stated exactly once, with the correct percentile pairing, in the demo defence at 6:55. Never quoted as 40 ms p95. | §4.3; §8.6 anti-pattern. |
| 6 | **Refuse-to-claim list about us.** | Untouched. The fourth beat at 8:55–9:10 says it verbatim. | §6.2. |

### 9.3 The 13 supporting freezes (R2S4 §12 + R2S3 §9 + R2S1 §6)

| # | Supporting freeze | Status |
|---|---|---|
| 1 | Surgical edit only (no unconstrained rewrite). | Untouched. Demo beat 4.1.f shows the surgical strip. |
| 2 | Evidence-packet escalation. | Untouched. The packet is on screen, with all four fields. Demo beat 4.1.g. |
| 3 | No LLM-as-judge on the critical path. | Untouched. Differentiation beat 6.1.b names it. |
| 4 | No per-response bias verdict. | Untouched. Bias is not on screen. |
| 5 | One graph, three reads. | Untouched. The graph is the dominant UI. |
| 6 | Lane 1 always on. | Untouched. Architecture carries the invariant. |
| 7 | Locked R3 action classes. | Untouched. The refund is locked at R3. |
| 8 | API-only deployment. | Untouched. B2 slide: "No weights, no logits, no fine-tuning." |
| 9 | Stage 1 live scope unreopened (two routes). | Untouched. The demo is exactly the two routes. |
| 10 | ≤40 ms p50 / ≤200 ms p95. | Untouched. Stated once, correctly. |
| 11 | Content laws (clause 7.2, who pays, held ≠ blocked, refuse-to-claim). | Untouched. See §9.2. |
| 12 | Principal-flip as second beat. | Untouched. Demo beat 6:30–7:15. |
| 13 | Live re-run with binding latency ≥ 50 ms. | Untouched. §4.2; §4.3. |

### 9.4 The architecture is closed, the pitch is open

The architecture is closed (`ARCHITECTURE.md §12`). The pitch is the rendering of the closed architecture. **If a sentence in the pitch is not a rendering of the frozen stack, it is a bug.** The pitch is the only place where the architecture is allowed to be *performed* — and performance is the job.

The five-stage spine (R2S4 §12, closing):

```
AI can act
  → unproven claim must not authorize
    → provenance outside the model
      → Default = UNSUPPORTED
        → entitlement = set-membership
          → R×S prices by consequence
            → hard gate on commit
              → publish misses.
```

This is the order. The pitch follows this order. The opening lands steps 1–2. The thesis names steps 2–4. The mechanism names steps 3–6. The demo proves steps 4–7. The FNR delivers step 8. The closing resolves steps 1 and 8.

If any step is missing from the pitch, the pitch has not earned the room.

---

# APPENDICES

---

## Appendix A — Speaker Crib (the one page to take on stage)

```
CONTROLPLANE.AI · PITCH CRIB · 10:00

[0:00]  Held-refund card on screen, idle. ₹1,84,000. HELD — ESCALATE.
[0:05]  "Here's a refund the system is about to issue..."
[0:20]  "It used to be a bad paragraph. It's now an executed transaction."
[0:30]  "Clause 7.2 doesn't exist. The model said it did."
[0:45]  "The refund was held — not blocked — held, with the evidence packet."

[1:15]  INDICTMENT. "The system didn't fail. It was never asked to prove anything."

[1:30]  HINGE. "Everyone watches the exit. Nobody records the entrance."

[1:50]  THESIS. "An AI response is not text to be scored. It is a set of
        claims requesting permission to act."

[2:15]  MECHANISM. STEP → SPAN → CLAIM → ACTION. One graph. Three reads.
        Performance reads forward. Cost reads backward (exact dead compute).
        Responsibility reads labels. Frozen R×S matrix. Verdict set.
        Default = UNSUPPORTED. Entitlement = set-membership, zero LLM.

[3:15]  DUAL-ACTION DEMO (the centrepiece). Spans before claims. Three red
        claims. C1 binds, C2 doesn't, C3 binds but ACL excludes principal.
        Matrix cell R1×entitlement→Edit. Matrix cell R3×unsupported-
        categorical→Escalate. Surgical edit. Held. Packet. Silence.
        `executed: false`. TWO SECONDS OF SILENCE.

[6:15]  Latency strip visible. ≤40 ms p50 / ≤200 ms p95 (demo numbers,
        labelled). Speculative verify OK; speculative release forbidden.

[6:30]  PRINCIPAL FLIP (live re-run). Same claim. Change only the principal.
        Actuator flips. Zero LLM. "It cannot be made by an output-scorer
        that doesn't carry identity into the verification layer."

[7:15]  BUSINESS CASE. Beachhead = R3 + mixed-governance knowledge. Days,
        not quarters. Mechanism is the number. Shadow default. Misses
        published per route, every phase. NO TAM. NO CAGR. NO % SAVED.

[8:30]  DIFFERENTIATION (45 sec). vs observability. vs LLM-as-judge. vs RAG
        groundedness. Three lines. Three screens. No table.

[8:55]  REFUSE-TO-CLAIM. "We do not claim to eliminate hallucinations. We
        do not claim zero integration. We do not claim zero added latency.
        We do not claim one accuracy number. The narrower, harder claim:
        an unproven or unauthorized claim cannot authorize an action —
        and we publish the rate at which we missed." FNR schema on screen,
        empty.

[9:15]  CLOSE. "That system was never asked to prove anything." [pause]
        [re-fire matrix highlight on stage; refund stays held] "Now
        nothing acts until it can prove it should." [pause] "That's
        ControlPlane. Thank you."

[9:45]  Q&A. B1 and B5 drilled cold. The held refund stays on screen.

NEVER SAY (about the refund): blocked · denied · rejected · refused ·
  stopped. Say: held and escalated with the evidence packet.
NEVER SAY (anywhere): monitor · detect · observe · watch · guard ·
  trust score · risk score · safety score · responsible AI · AI safety.
NEVER SAY (about us): eliminate hallucinations · zero integration ·
  zero added latency · one accuracy number across three failure modes.
```

---

## Appendix B — Slide-by-Slide Render (the deck as a thin render of the spine)

The deck is scaffolding, not the main act. **Total deck time: 1:15 (B1–B5 at 7:15–8:30).** No slide appears in the first 3:15 except the held-refund card, which is the live demo, not a slide. No slide appears in the last 0:45 except the FNR schema, which is the live demo, not a slide.

| # | Slide | One sentence | Visual | Time on screen |
|---|---|---|---|---|
| 0 | **Pre-room** (live demo) | (idle) | Held-refund card | 0:00–1:15 |
| — | (no slide) | — | — | 1:15–7:15 |
| B1 | **Beachhead** | "Beachhead = high-consequence routes: refund-class R3 + mixed-governance knowledge. Not 'all enterprise AI safety.'" | 2×2 (R-tier × use case) with two cells highlighted. | 10 sec |
| B2 | **Integration cost** | "Days, not quarters. One SDK hook + one proxy. The integration cost is the moat — and we say so." | 2-component integration diagram. | 15 sec |
| B3 | **What it buys** | "R3 held at `executed: false` is structural escape from wrong actions. The mechanism is the number." | Before/after with the held refund. | 15 sec |
| B4 | **Operation** | "Shadow by default. Enforcement earned per route. Misses published per phase." | 5-phase roadmap (Prototype → Shadow → Canary → Limited R2/R3 → Broader). | 20 sec |
| B5 | **Audit** | "Hash-chained ledger. Versioned policy. Reconstruct any actuator end to end." | The drill-down chain. | 15 sec |
| D1 | **vs observability** | "Observation without commit control is an audit trail, not architecture." | The held refund + `step_yield: 5/9 grounded; dead_compute: 4/9`. | 10 sec |
| D2 | **vs LLM-as-judge** | "The judge asks 'does this look right?' — an unfalsifiable question. We ask 'which span proves it?' — a query with an answer." | Matrix cell highlight + `default_verdict: UNSUPPORTED` field. | 10 sec |
| D3 | **vs RAG groundedness** | "Retrieval is not permission. Proof scales with consequence." | Principal flip on screen. | 10 sec |
| F | **FNR schema** (live demo) | "We publish the rate at which we missed. The schema is the claim." | Empty typed FNR schema. | 15 sec |
| — | (no slide) | — | Held refund returns to centre | 9:15–10:00 |

**Total slide count: 9** (B1–B5, D1–D3, F). **Plus the held-refund card and the FNR schema, which are live demo states, not slides.** No "Title," "About Us," "Team," "Problem," "Solution," "Market," "Customer Logos," "Thank You," or "Q&A" slides exist.

---

## Appendix C — Pre-Room Setup (the 90 seconds before the timer starts)

This is what the team does in the 90 seconds before the judges walk in.

| t-90s | Action |
|---|---|
| −90 | Boot the demo machine. Open the Evidence Ledger. Confirm the held-refund card is the landing view. |
| −80 | Run `pytest -q`. Green. Run `python examples/refund_trace_demo.py`. Confirm the held refund renders. |
| −70 | Run `python examples/knowledge_flip_demo.py`. Confirm the principal flip works. |
| −60 | Open the FNR schema viewer. Confirm all fields are null / placeholder / prototype_corpus. |
| −50 | Confirm the latency strip is on. Confirm the latency numbers are demo-machine numbers, labelled as such. |
| −40 | Confirm the matrix cell highlight is wired to fire **before** the actuator row. |
| −30 | Confirm the evidence packet is visible by default on any Escalate. |
| −20 | Read §8 (anti-patterns) once aloud. Any pattern that triggers a "yeah, we do that" is fixed before t=0. |
| −10 | The held-refund card is the only thing on screen. No idle animation, no splash, no "press space to start." |
| 0 | Timer starts. The held refund is on screen. The presenter is silent for the first beat. |

**The single most common failure mode of pre-room:** the demo machine boots into a default state that is not the held-refund card. **The default state is the held-refund card.** This is the first CI test the build team writes on day 1.

---

## Appendix D — Q&A Posture (the 60 seconds after the timer ends)

The Q&A is where the pitch is **defended**, not extended. The frozen hostile Q&A (`QA.md`) is the source. The two attacks the team drills hardest are **B1** (purely parametric answer — no retrieval, no spans) and **B5** (prompt injection — can an attacker make a false claim bind to a real span?).

### D.1 The two drills

**B1 — "What about a purely parametric answer? No retrieval, no spans, nothing to bind to."**

The line that wins it:

> *"We don't claim to verify what we were never given. We claim that what we were never given cannot authorise an action."*

Mechanics: routes with no provenance are declared ungrounded by construction; the async lane runs a semantic-entropy probe for calibration; but the **commit path** is the point — an ungrounded answer annotates a draft but cannot authorise a payment.

**B5 — "Prompt injection. Can an attacker make a false claim bind to a real span?"**

> *"The binding is computed by us, not asserted by the model — the model has no channel to declare a binding. An injection can change what the model says; it cannot change which spans were captured at context assembly, nor the entailment verdict, nor the ACL. The attack that does work is poisoning a source document so that a genuine span supports a false claim — that is a supply-chain attack on the corpus, not on the plane, and the source ID and content hash are what make it forensically traceable. **The honest boundary, stated out loud: we defend the claim-to-evidence link, not the truth of the evidence.**"*

### D.2 The fallback posture if a question goes off-script

> *"That's a great question. The architecture's answer is in the matrix — let me show you the cell."*

The presenter points at the held refund on screen. The room remembers the held refund. The architecture is defended by the architecture, not by a slide.

### D.3 The line that ends the Q&A

> *"We don't have to win this argument in the room. The matrix does, on the screen, on every request. We just have to show you it's running."*

The presenter gestures at the held refund. The Q&A is over.

---

## Appendix E — What Stage 5 Is / Is Not

**Stage 5 IS:** the exact narrative and structural spine of a 10-minute pitch that renders the frozen architecture, the live demo, the business case, and the differentiation in a single continuous argument. The pitch is the only artifact left to design.

**Stage 5 IS NOT:**

- A re-litigation of the architecture.
- A new mechanism.
- A redrawn matrix.
- A new vocabulary.
- A "broader story" that softens the frozen insight.
- A consulting deck.
- A vendor pitch.
- A research talk.
- A demo showcase without a closing argument.

**The pitch renders the architecture. The architecture is closed. The pitch is the only thing left to write.**

---

*End of Round 2 Stage 5 — Pitch Architecture. Stages 1–4 frozen invariants fully preserved. The dual-action is the centrepiece. The held refund is the cold open and the close. The matrix is the proof. The FNR is the credibility play. The plane is the only thing on screen. Now the team rehearses.*
