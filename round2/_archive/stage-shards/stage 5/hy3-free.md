# ControlPlane.ai — Round 2 Stage 5 (Frozen)

## Pitch Architecture

> Accenture Innovation Challenge 2026 · Round 2 · Stage 5 — Pitch Architecture  
> Sources of truth (absolute): `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` · `R2S2.md` · `R2S3.md` · `R2S4.md`  
> Status: **ETERNALLY FROZEN** — Stages 1–4 are non-negotiable. This document designs only the narrative and structural spine of the Round 2 pitch. It reopens no technical, scope, or value decision.  
> Objective: a pitch that forces a serious engineer or Accenture evaluator to respect the architecture in the room — not a competent consulting deck.

---

## 1. Pitch Thesis

> ControlPlane is an admission-control layer that treats every AI response as a set of **claims requesting permission to act**, not text to be scored. An AI response is not prose to be graded — it is a transaction proposal, and the cost of a wrong one has changed category: it used to be a bad paragraph, it is now an executed transaction. We capture the evidence the model was actually given *outside* the model, invert the burden of proof so every claim starts unproven, carry caller identity into verification, and gate the commit path by blast radius on one frozen graph — so an unproven or unauthorized claim cannot authorize an action, and the plane publishes what it itself missed. The pitch must leave one idea in the room: **the system that was never asked to prove anything now refuses to act until it can.**

---

## 2. Overall Pitch Structure

Total target: **11 minutes** (live or recorded). Tight, high-signal. The dual-action demonstration is the intellectual and emotional centre — it owns the largest single block and is never displaced by business prose.

| # | Beat | Time | What it must do |
|---|---|---|---|
| 1 | **Opening — the held transaction** | 0:00–1:30 (90s) | Cold-open on the pending ₹1,84,000 refund, R3, HELD—ESCALATE, `executed:false`. Never on risk. |
| 2 | **Thesis + category change** | 1:30–2:30 (60s) | One paragraph: claims requesting permission to act; bad paragraph → executed transaction. State the graph in one line. |
| 3 | **Architecture: one graph, three reads** | 2:30–4:00 (90s) | `STEP → SPAN → CLAIM → ACTION`. Provenance outside the model = set-membership test. Contrast with post-hoc observability (record the entrance, not only the exit). |
| 4 | **Prototype Demonstration Spine — dual-action (centrepiece)** | 4:00–8:00 (4:00) | Built **backward from the action gate**. R3 Escalate held + R1 Edit, Evidence Ledger ≥60%, empty FNR schema. The room's load-bearing 4 minutes. |
| 5 | **Principal-flip + FNR honesty** | 8:00–9:00 (60s) | Entitlement is set-membership, zero LLM. FNR schema shown empty — emptiness is the credibility play. |
| 6 | **Business Case Integration** | 9:00–11:30 (2:30) | Value levers A–G, buyer split, roadmap as earn-out. Mechanism→consequence, no fabricated ROI. |
| 7 | **Differentiation & Defence Moments** | 11:30–12:30 (60s) | vs LLM-as-judge · vs groundedness · vs observability · refuse-to-claim posture. Sharpest contrasts. |
| 8 | **Closing Beat** | 12:30–13:30 (60s) | Resolve the opening. Preferred closing line delivered. |

> **Time discipline:** if the room forces 8 minutes, compress beats 6 and 7 into 90s each and drop beat 5's FNR deep-dive to a single on-screen schema flash. **Never** compress beat 4. Beat 4 is the pitch; everything else is its frame.

---

## 3. Opening Beat (first 60–90 seconds)

**Exact approach.** The screen is already live on the Action Gate panel before anyone speaks — no title slide, no "AI is powerful." Visible:

```
Action: refund.execute
Args: { amount: 184000, reason: "clause 7.2", order_id: "ORD-1023" }
R: R3 — irreversible payment
Status: HELD — ESCALATE
Executed: false
```

The presenter says, within the first 20 seconds, a line that contains the word **"claim,"** not "response":

> "This refund was never made. ₹1,84,000 did not leave the company. The text said: *Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.* **Clause 7.2 does not exist.** The system didn't fail. It was never asked to prove anything."

Then the permitted exception line, which indicts what everyone else built:

> "Everyone watches the exit. Nobody records the entrance."

Then the category-change line that sets the stakes:

> "It used to be a bad paragraph. It is now an executed transaction."

**Hard rules for the opening:**
- Open on a **transaction with a rupee figure attached**, never on a person (no shocked customer, no angry email).
- Open on the **held** state, never on a risk statement. The danger is implied by the money, not asserted as a hazard.
- First spoken sentence about the failure uses **"claim,"** not "response."
- "Safety" does not appear. The word "claim" appears before any other framing noun.

---

## 4. Prototype Demonstration Spine

The live or recorded dual-action demo is embedded **inside** the pitch as beat 4, built **backward from the action gate** (R2S1 §3, R2S3 §5). It is the emotional and intellectual centre. The pitch protects these invariants explicitly:

**Build backward from the action gate.** Start where beat 1 left off — the gate already showing HELD—ESCALATE. Do not build the demo forward from "here is our architecture" into "and it caught this." Start at the commit boundary and walk back into the graph that produced the hold. This is the single most important structural choice: it makes the plane an *authorisation system that happens to catch errors*, not a safety system that happens to have a gate.

**Evidence Ledger majority.** The Trace Console UI occupies **≥60% of screen** for the entire demo. If removing the graph leaves the demo looking the same, the demo has failed (R2S3 governing test). Spans appear with `source · ACL · hash · offsets` **before** claim verdicts — provenance outside the model, visibly.

**Dual-action, held and unresolved into one collapse.** Same single refund response yields, simultaneously:
- `text.show` → worst claim C3 (unentitled span grounds a claim) → **R1 × entitlement → Edit** (surgical strip).
- `refund.execute` → worst claim C2 (clause 7.2 has no span) → **R3 × unsupported-categorical → Escalate — held, with evidence packet**. Mock refund does **not** commit (`executed:false`).

Never collapse into one "response blocked." Never say the refund was **"blocked."** Say *held and escalated with the evidence packet.* The room must see two actuators fire from one graph — "proof scales with consequence."

**Worst-claim weighting, not average.** The interlock disposition uses the worst claim for *each* pending action. Say it plainly: "RAG checkers average — one wrong figure drowns in nine correct sentences. We price the worst claim for the action about to happen."

**Surgical Edit + Evidence Packet.** The Edit strips only C3 from visible text; edited text re-enters the gate; refund stays held. The Escalate packet opens: claim · candidate spans `[]` · verdict UNSUPPORTED · diff · action · policy version. Not a bare alert.

**Live compute, not animation.** Binding / entitlement / interlock run live with visible latency (~20–80ms). If claims are pre-extracted for stability, the prove/bind/gate path still executes in front of the room. A hostile judge must not dismiss it as a recording.

**Empty FNR schema.** The per-route FNR schema is on screen with **null / empty typed placeholders only**. Emptiness is the credibility play: a judge who tests it finds the honesty rather than the bluff.

**Principal-flip (required secondary, beat 5).** Change **only** the calling principal on the knowledge route; same span, same claim, same graph; entitlement outcome flips because the ACL check is live set-membership — zero LLM. This is the moment that proves entitlement is *authorisation, not classification*.

**Demo ordering (anti pattern-match):** held R3 crisis first → R1 text Edit → expand ledger → matrix cells highlighted **before** actuators → packet → empty FNR → principal-flip. Core dual-action crisis ≤90s; full session ≤8 min.

---

## 5. Business Case Integration

The business case (R2S4) is delivered as **beat 6**, after the room has *seen* the architecture work — never as a generic consulting deck that precedes proof. A buyer who has just watched ₹1,84,000 fail to leave the company now hears *why that hold is worth money*.

**Buyer logic, not org-chart theatre.** Name the split that wins: the person who **pays when it fails** (route-owned P&L / CRO / CISO) is not the person who **runs it daily** (platform lead), and neither is the person who **types the answer** (agent team). The economic buyer responds to *"an unproven claim cannot authorise an action,"* not *"we detect 95% of hallucinations."* Lead with that sentence.

**Value levers as mechanism→consequence, in this order:**
- **Lever A — avoided wrong actions (primary).** The escape is structural, not statistical: `refund.execute` cannot commit while R3 × unsupported-categorical → Escalate held. Value = held true-positives × the buyer's own direct cost of that action class, measured on *their* adjudicated sample.
- **Lever C — exact dead compute.** A dashboard says the trace cost ₹8; ControlPlane says ₹5 of it grounded nothing. Walk the graph backward — exact, no model, no estimation. No competitor has this number because no competitor has the graph.
- **Lever B — blast-radius pricing.** Expensive proof concentrated where consequence is high; R0/R1 (majority volume) get cheap checks. Same verdict annotates a draft and holds a payment.
- **Lever E2 — unauthorized disclosure.** The same plane that holds the refund also stops the correct-answer / wrong-person leak. Half the beachhead.
- **Lever F — publish what we missed.** Per-route FNR as format; emptiness until earned.
- **Lever G — earned autonomy (last, never lead).** Routes begin in shadow; enforcement is earned from counterfactuals. This is the earn-out, not "operational enablement."

**Honest boundaries stated out loud:** the integration cost is the moat (one SDK hook + OpenAI-compatible proxy, days not quarters — never "zero integration," never "drop-in"). We do not claim to fix enterprise IAM; we stop IAM gaps being silently bypassed by a model. We do **not** put a savings percentage on a slide.

**Roadmap as earn-out (R2S4 §5):** Phase 0 prototype → Phase 1 shadow on 1–2 real routes → Phase 2 canary on R0/R1 → Phase 3 limited R2/R3 enforcement → Phase 4 broader envelope. No global enable-from-a-slide. Deterministic mechanisms work day one; statistics earn thresholds.

---

## 6. Differentiation & Defence Moments

These contrasts are placed at precise moments, not dumped in a comparison table. Each is a *defence* — a pre-emptive answer to the attack a serious engineer reaches for first.

**vs Post-hoc observability (beat 3).** "Observation without execution control is an audit trail, not architecture. Everyone watches the exit. Nobody records the entrance. We record the entrance — and interlock the commit path. A dashboard can tell you the trace cost ₹8; it cannot tell you ₹5 of it grounded nothing. Walking the graph backward can."

**vs LLM-as-judge / static guardrails (beat 7).** "The judge asks *does this look right?* — an unfalsifiable question. We ask *which span proves it?* — a query with an answer. Decision time is a pure rule engine, zero LLM. The judge is identity-blind and same-family; we carry the caller into verification. Default is UNSUPPORTED — the claim carries the burden of proof, not our opinion."

**vs RAG groundedness checkers (beat 7).** "The closest cousin, still short in three ways: retrieval-only, averages so one wrong figure drowns, and action-blind — 0.82 means the same on a draft and a wire transfer. Retrieval is not permission. We bind against the full provenance set, price the worst claim per pending action, and apply the exact matrix so the identical unsupported claim annotates a draft and holds a payment. Proof scales with consequence. This is not a better classifier — a different question, a different decision geometry, a different standard of honesty."

**Refuse-to-claim posture (woven, peaks at beat 7).** Four refusals about *us*, not competitors — the rarer and stronger move:
- "We eliminate hallucinations" → refused. We claim ungrounded claims cannot authorize actions, and we report what we miss.
- "Zero integration, drop it in" → refused. The integration cost is the moat; say it out loud.
- "Zero added latency" → refused. We never make the model feel slow; we make the action wait (≤40ms p50 / ≤200ms p95 on R0/R1 text — never quote 40 as p95).
- "One accuracy number across failure modes" → refused. Different mathematics, owners, costs.

**The credibility closer (beat 7).** "Competitors publish precision — the rate at which they bother the user. We publish the rate at which we missed, per route. Every deck disclaims its rivals; almost none disclaims itself. The plane is audited by the standard it enforces."

**Defence of the empty FNR (beat 5).** When a judge asks "where's your accuracy?" — the answer is the empty schema: "You shouldn't believe a number we haven't earned. The only number on our deck is labelled a format. What you can evaluate today is the architecture."

---

## 7. Closing Beat

**Exact closing move.** Return to the Action Gate panel from the opening — the same HELD—ESCALATE, `executed:false`. The loop closes: the room opened on a transaction that did not happen, and now understands *why it was permitted to not happen*.

> "That system was never asked to prove anything."
> *[hold — one full breath]*
> "Now nothing acts until it can prove it should."

Then, if a single sentence remains, the thesis restated as infrastructure:

> "An AI response is not text to be scored. It is a set of claims requesting permission to act — and permission is now earned, per claim, per caller, per action."

**Resolution check:** the opening's indictment ("never asked to prove anything") is answered exactly by the closing ("nothing acts until it can prove it should"). No new idea is introduced. The graph, the matrix, the held refund, and the empty FNR schema are all still on screen or freshly in memory.

---

## 8. Anti-Patterns (Hard Kill List)

Specific things the pitch must **never** do. Each maps to a frozen content law or narrative risk.

1. **Never open on AI risk.** No "AI is powerful but risky." Open on the held transaction. The narrative risk (NARRATIVE §6) is that judges pattern-match to "another AI safety tool" in twenty seconds.
2. **Never collapse the dual-action into one response-level verdict.** Two actuators (R1 Edit + R3 Escalate) fire from one graph and must both be visible. One "response blocked" line kills the centrepiece.
3. **Never say "blocked" about the refund.** Say *held and escalated with the evidence packet.* Content law (ARCHITECTURE §10, R2S1 §0). The mock executor status is `HELD—ESCALATE`, never `COMMIT BLOCKED`.
4. **Never lead with enablement / "operational benefit."** Autonomy expansion (Lever G) is last, never the lead. The pitch sells authorisation infrastructure, not "AI that does more."
5. **Never put a fabricated number on a slide.** No ROI %, no "99% accuracy," no "30–50% waste," no production FNR percentage. The FNR schema ships empty. Emptiness is the credibility play.
6. **Never quote 40ms as p95.** Latency is ≤40ms p50 / ≤200ms p95. This error was live in three places before the elevation pass; it is dead on contact in questioning.
7. **Never say clause 7.2 "caps," "denies," or "doesn't cover" anything.** The failure is *absence* of evidence, which is what puts it in the unsupported column and makes Escalate — not Block — correct.
8. **Never invert the premise.** The company wrongly pays out ₹1,84,000 if ungated; the customer did not lose money. Two models inverted this; one had the refund *denied*.
9. **Never use the banned vocabulary in our own voice.** Ban: monitor · detect · observe · watch · guard · trust score · risk score · "responsible AI" as a standalone virtue. Use: authorise · admit · prove · bind · refuse · hold · escalate · gate. One permitted exception: "Everyone watches the exit" — it indicts what everyone else built.
10. **Never let the Evidence Ledger drop below 60% of screen during the demo.** If removing the graph leaves the demo looking the same, scope has failed.
11. **Never make the demo look pre-baked.** Binding / entitlement / interlock must show live compute. A recording loses the room.
12. **Never drop bias.** State it in measurement terms — counterfactual flip-rate + CI, route-level, async — never moral ones, never a per-response verdict. The brief names it; omitting it scores against the rubric.
13. **Never redraw the matrix.** Transcribe the 4×4. Axis labels, column vocabulary, cell values are load-bearing. Six of seven models corrupted this when asked to redraw.
14. **Never present a composite score as disposition.** No 0–100 trust/risk score. You cannot Block · Edit · Escalate on 87.
15. **Never let business prose crowd the dual-action.** Beat 4 is sacrosanct. If time compresses, cut beat 6/7, never beat 4.
16. **Never claim we fix enterprise IAM or prove source truth.** We stop IAM gaps being silently bypassed by a model, and we defend the claim-to-evidence link — not the truth of the evidence.

---

## 9. Fidelity Self-Check

Explicit confirmation that this pitch architecture protects every major invariant from Stages 1–4.

| Frozen invariant (source) | How the pitch protects it |
|---|---|
| **Default = UNSUPPORTED** (ARCH §4, R2S1 §3) | Open line: "It was never asked to prove anything." Demo shows all claims born UNSUPPORTED; C2 stays unproven (absence, not contradiction). |
| **Entitlement / ACL check — deterministic set-membership, zero LLM** (ARCH §3, R2S2 §2) | Principal-flip beat proves `span.acl ⊆ principal.clearance` with zero LLM; shown as set-membership, not a score. |
| **Exact R×S matrix, per pending action, never redrawn** (ARCH §4, R2S1 §0) | Matrix rendered exact 4×4; cells highlighted **before** actuators; dual-action shows R1×entitlement→Edit and R3×unsupported-categorical→Escalate simultaneously. |
| **Hard gate on actions, not tokens** (ARCH §5, R2S3 §6) | Cold-open Action Gate shows `refund.execute` HELD, `executed:false`; text holds back ~150–300ms while the commit path is gated. |
| **Two-pending-actions resolution (R1 Edit + R3 Escalate), never one verdict, never "blocked"** (ARCH §9, R2S1 §3) | Dual-action is the centrepiece (beat 4); both actuators fired from one graph; language is "held and escalated with the evidence packet." |
| **Published FNR as empty typed schema** (ARCH §7, R2S2 §5) | Empty FNR schema on screen during demo; refuse-to-claim posture refuses any fabricated number; emptiness is the credibility play. |
| **UNKNOWN never → SUPPORTED** (ARCH §7, R2S3 §9) | Demo language: "unproven," not "low confidence"; timeout/derived paths route via matrix, never silent allow. |
| **No LLM-as-judge / confidence as primary mechanism** (ARCH §3, R2S2 §3) | Differentiation beat attacks LLM-as-judge explicitly; decision time stated as pure rule engine, zero LLM. |
| **Bias = async route-level measurement, never per-response verdict, never dropped** (ARCH §3, R2S4 §2) | Carried in business case and refusal posture as counterfactual flip-rate + CI; never a live demo actuator; explicitly not dropped. |
| **One graph, three reads** (ARCH §2, R2S2 §2) | Beat 3 states `STEP → SPAN → CLAIM → ACTION`; performance/cost/responsibility framed as three reads of one graph. |
| **Refuse-to-claim list (about us)** (NARRATIVE §5, R2S4 §2) | Four refusals woven into beat 6/7; integration cost stated as moat; no eliminate-hallucination / zero-integration / zero-latency / one-accuracy-number claims. |
| **Content laws (clause 7.2 absence; company wrongly pays; customer did not lose; latency ≤40/≤200)** (ARCH §10, R2S1 §0) | Opening uses exact running example; never "caps/denies"; premise uncorrupted; latency quoted only as ≤40ms p50 / ≤200ms p95. |
| **Prototype boundary — exactly two live routes; dual-action centrepiece; no third live bias route** (R2S1 §2, R2S2 §0) | Demo covers refund dual-action + knowledge principal-flip only; decision-support/bias stays in business case, not live demo. |
| **Evidence Ledger ≥60% UI / governing test** (R2S3 §6) | Demo spine mandates ≥60% ledger; kill-list item 10 enforces it. |
| **Build backward from the action gate** (R2S1 §3, R2S3 §5) | Demo ordering starts at HELD—ESCALATE and walks back into the graph. |

**Conclusion:** every load-bearing invariant from Stages 1–4 is surfaced by a specific beat, line, or screen in this architecture. No mechanism is reopened, no value decision is reversed, and no banned vocabulary appears in our own voice. The pitch is a rendering of the frozen stack — its only job is to make a serious evaluator respect the architecture that already exists.

---

*End of Stage 5 — Pitch Architecture. Stages 1–4 eternally frozen; this document designs only the pitch spine.*
