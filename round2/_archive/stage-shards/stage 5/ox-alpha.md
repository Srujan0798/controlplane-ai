# ControlPlane.ai — Stage 5: Pitch Architecture (ox-alpha shard)

**Accenture Innovation Challenge 2026 · Round 2 · Pitch Presentation Design**
Sources of truth (absolute, eternally frozen): `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` · `R2S2.md` · `R2S3.md` · `R2S4.md`
Status: working shard for adversarial merge. Stages 1–4 are non-negotiable; this document only architects how they are performed in the room.

---

## 1. Pitch Thesis

The entire pitch installs one sentence in the room: **an AI response is a set of claims requesting permission to act** — which retires the market's question (*is the text good?*) and replaces it with ours (*which span proves it, and is this caller entitled to that span?*). ControlPlane answers that question mechanically: provenance captured outside the model at context assembly, every claim born UNSUPPORTED until it earns proof against the captured span set, entitlement as deterministic set-membership (`span.acl ⊆ principal.clearance`, zero LLM), and the exact frozen R×S matrix hard-gating the commit path per pending action — so the identical unsupported claim annotates a draft and holds a ₹1,84,000 refund. The plane publishes its own per-route miss rate, empty until earned. **Nothing acts until it can prove it should.** Success criterion for the pitch: the room leaves saying "claims requesting permission" and "held, not blocked." If they leave saying "AI safety tool," the pitch failed regardless of the architecture underneath.

---

## 2. Overall Pitch Structure

Planned runtime **9:25 inside a 10:00 envelope**. Two presenters (P1 narrative/liability voice, P2 systems/demo voice); both must clear the QA readiness bar (§9). Three slides exist in total — title card, one exposure equation, close card — and **the deck never covers the ledger**.

| Beat | Clock | Voice | Content | Guard |
|---|---|---|---|---|
| **B1 · Cold open — the held transaction** | 0:00–1:15 | P1 | Gate panel on screen before speech; indictment; thesis; category change | Never open on risk, person, or market stat |
| **B2 · The graph in 45 seconds** | 1:15–2:00 | P2 | STEP → SPAN → CLAIM → ACTION over the live ledger; provenance outside the model; default UNSUPPORTED | Set-membership phrase is load-bearing — never dropped |
| **B3 · Dual-action crisis (centrepiece)** | 2:00–4:30 | P2 | Refund response: R1 × entitlement → **Edit**; R3 × unsupported-categorical → **Escalate**, held with evidence packet, `committed:false`; matrix cells highlighted **before** actuators | Core crisis ≤90 s; never one response-level verdict |
| **B4 · Proof honesty** | 4:30–5:15 | P2 | Empty FNR schema; publish-the-miss-rate; `UNKNOWN` never → `SUPPORTED`; parametric boundary | Emptiness presented as the claim, never apologised for |
| **B5 · Principal flip** | 5:15–6:15 | P2 | Same span, same claim, only the caller changes → entitlement flips; zero LLM | Entitlement shown as set-membership, never a score |
| **B6 · Business case as consequence math** | 6:15–7:45 | P1 | Exposure equation; levers A/C/F lead; buyer split; beachhead; earn-out ladder; commercial honesty | ≤90 s, one slide; no consulting-deck furniture |
| **B7 · Differentiation + self-disclaimer** | 7:45–8:50 | P1 | Compressed restatement of the three contrasts (seeded live in B3–B5); four refusals about *us*; bias in measurement terms | Contrasts anchored in evidence already seen, not asserted |
| **B8 · Close — resolve the opening** | 8:50–9:25 | P1 | Return to the gate panel; frozen close lines; category noun; stop | No new information after the close line |

Buffer: 9:25–10:00 absorbs slippage and hands to Q&A standing still.

**Format adaptors**
- **8-minute format:** compress in this order — B7 contrasts to one breath each; dead-compute line folds into contrast 1; B6 trims to equation + beachhead + ladder. **Never cut:** cold open, dual-action, principal flip, FNR schema, close.
- **12-minute format:** expand B5 to the full interactive flip (≤2 min) and add one optional beat (numeric `14 days` vs `11` → deterministic Edit). Never add breadth.
- **Recorded variant:** identical beat structure; if any segment is pre-recorded it is labelled on screen (`recorded · build <hash>`), and spoken anchors stay verbatim. The dual-action segment is recorded in one unbroken take.
- **Live-failure protocol:** if the demo dies mid-crisis, switch to the labelled recording of the same build — never re-narrate from slides, never skip to business case. The crisis must be seen resolving.

---

## 3. Opening Beat (0:00–1:15)

**Approach:** the first thing in the room is a specific irreversible action with a rupee figure attached, held. Not a risk statement, not a person, not a market size. The danger is implied by the money.

**Staging:** screen shows the Action Gate panel from second zero, silent for three seconds:

```
Action:    refund.execute
Args:      { amount: 184000, reason: "clause 7.2", order_id: "ORD-1023" }
Blast R:   R3 — irreversible payment
Status:    HELD — ESCALATE
Executed:  false
```

**Script (verbatim anchors from the frozen narrative):**

> *(0:03)* "Everyone watches the exit. Nobody records the entrance." — the one sanctioned exception to the vocabulary ban; it indicts what everyone else built.

> *(incident, four sentences, past tense — the ungated world)* "Tuesday, a support agent approved a refund of ₹1,84,000 under clause 7.2 of a vendor agreement. Clause 7.2 does not exist. Every filter passed it; confidence read 0.94. The money moved Tuesday. Someone found it Friday." — the company wrongly paid; the customer did not lose money. The 0.94 lives in this narration only — it is never rendered in our UI.

> *(indictment)* "The system didn't fail. It was never asked to prove anything."

> *(thesis)* "An AI response is not text to be scored. It is a set of claims requesting permission to act."

> *(category change)* "Because the cost of a wrong output changed category: it used to be a bad paragraph. It is now an executed transaction."

> *(handoff to P2)* "So we didn't build a better opinion about text. We built the thing that stands between a claim and an action. Don't take the architecture from me — watch it hold the money."

**Discipline:** 75 seconds hard cap. The first substantive sentence after the exception line names a **claim**, never "AI" in the abstract. No context-setting, no "AI is powerful but."

---

## 4. Prototype Demonstration Spine (B2–B5, 1:15–6:15)

Governing rule: **build backward from the action gate.** The audience has already seen the outcome (HELD); the demo's job is to make them unable to argue with *why*. Ledger ≥60% of screen throughout; if removing the graph leaves the pitch looking the same, the pitch has failed.

### B2 · The graph (1:15–2:00)
| Visual | Spoken anchor |
|---|---|
| Ledger expands; spans with `source_id · ACL · hash · offsets` already present **before** any claim verdict | "Provenance captured at context assembly, outside the model. The model has no write path to this graph." |
| Graph edges form `STEP → SPAN → CLAIM → ACTION` | "Injection can change what the model says; it cannot change which spans were captured." *(pre-empts QA B5)* |
| Claims appear tagged UNSUPPORTED | "Every claim starts UNSUPPORTED and must earn SUPPORTED. Not low confidence. Unproven." |

### B3 · Dual-action crisis (2:00–4:30) — the centre
Core crisis ≤90 s inside this window. Sequence is fixed:

1. Claims resolve on screen: **C1** (amount/order) binds to `ORD-1023` → SUPPORTED. **C2** ("under clause 7.2…") finds **zero spans** → stays UNSUPPORTED. **C3** binds to `FIN-INTERNAL-NOTE`, whose ACL excludes `agent_refund_7` → entitlement violation.
   — Anchor: *"Absence of evidence, not conflict. That places C2 in Unsupported+categorical — which is why the actuator is Escalate, not Block."*
2. Two pending actions priced separately; matrix cell highlighted **before** each actuator fires: `text.show` → **R1 × entitlement → Edit**; `refund.execute` → **R3 × unsupported-categorical → Escalate**.
   — Anchor: *"Worst claim weighted by that claim's role in the pending action. Groundedness tools average — one wrong figure drowns in nine correct sentences. We never average."* *(groundedness contrast seeded)*
   — Anchor at the Interlock: *"Zero LLM decided this. A pure rule engine applied f(R,S). Their judge asks 'does this look right?' We ask 'which span proves it?' — a query with an answer."* *(judge contrast seeded)*
3. Surgical Edit strips only C3; edited text re-enters the gate. Refund remains held. Text streams behind the ~150–300 ms hold-back; the commit path waits.
   — Anchor: *"Proof scales with consequence. Same response, two actions, two different correct outcomes."*
4. Evidence packet opens: claim · candidate spans `[]` · verdict · diff · action.
   — Anchor: *"Escalation ships an evidence packet, not an alert."*
5. Executor log renders `refund.execute → committed:false`.
   — Anchor: *"Held and escalated with the evidence packet. The company does not wrongly pay out."*

**Protected invariants in this beat:** never one response-level verdict; never "blocked" about the refund; binding/entitlement/interlock visibly compute (~20–80 ms, real work, not animation); first spoken failure sentence contains **"claim,"** not "response."

### B4 · Proof honesty (4:30–5:15)
- FNR gate report on screen — full typed schema, every field null: `route_id · policy_version · window · strata · counts · FNR_estimate · CI_lower/upper · ground_truth_method · measurement_status · limitations`.
  — Anchor: *"We publish our own miss rate. Per route. Not what we caught — what we missed. The fields are typed; the values are null until earned. The emptiness is the claim."*
- Method in one clause: 100% of holds and escalations plus a random slice of passes audited to ground truth — human or expensive multi-verifier, never an LLM judging another LLM.
- Derived-claim rule: *"Arithmetic is recomputed from spans; what can neither be recomputed nor entailed returns UNKNOWN — and UNKNOWN never collapses into SUPPORTED. That rule is the boundary between a control plane and false assurance."*
- Parametric boundary, unprompted (QA B1 pre-empt, verbatim): *"We don't claim to verify what we were never given. We claim that what we were never given cannot authorise an action."*

### B5 · Principal flip (5:15–6:15)
Knowledge route. `analyst_01` queries L6 compensation → claim binds to `HR-COMP-L6`, ACL excludes caller → **R1 × entitlement → Edit**. Change **only** the principal → `hr_partner_01`: same span, same claim, same graph, outcome flips. Zero LLM in the path.
— Anchor: *"Authorization is set-membership, not text classification. Semantically correct and unauthorized still fails. Retrieval is not permission."*

---

## 5. Business Case Integration (B6, 6:15–7:45)

Delivered by P1 over **one slide** — the exposure equation — immediately after the flip, while the room is still looking at the graph. Every value claim must trace to something just demonstrated. Anti-consulting-deck rules: no TAM, no logos, no net-savings slide, no percentage-saved, no feature calendar.

Order of delivery (90 seconds):

1. **Exposure equation, anchored on the trace they watched:**
   `Exposure = frequency of consequential AI actions × probability of an unproven/unauthorized claim × loss per wrong action.` *"You know your frequency and your loss. The middle term is what you just watched go to zero structurally — not statistically. Fill the middle terms from your own sample; we won't invent them for you."*
2. **Levers, in frozen priority — mechanism → consequence, one sentence each:**
   - **A (lead):** `refund.execute` cannot commit while Escalate is in force — the escape from a wrong payout is structural. Buyer-verifiable artifact: attempt · matrix cell · evidence gap · `committed:false`.
   - **C:** the same graph accounts — walk it backward and any step that grounded zero accepted claims is dead compute, exact: *"a dashboard can say the trace cost ₹8; the graph says ₹5 of it grounded nothing."*
   - **F:** the plane publishes what it missed, per route — the conversation moves from "trust our score" to "here is the population, what we missed, and the uncertainty around that measurement."
   - Clauses only: blast-radius pricing keeps R0/R1 fast so the gate survives contact with users (D); the hash-chained ledger makes "why did this hold?" a pointer, not a paragraph (E); the same plane stops the correct-answer/wrong-person leak — half the beachhead (E2). Earned autonomy (G) is named last and explicitly secondary.
3. **Buyer split, three sentences:** *"The person who pays when it fails is not the person who runs it daily, and neither is the person who types the answer. The actor never enforces — the Interlock does. The buyer is never asked to trust a score — the plane publishes its own miss rate."*
4. **Beachhead:** *"We enter through high-consequence routes — refund-class agents and mixed-governance knowledge assistants. Not an enterprise-wide ethics purchase: an authorisation purchase for the routes where text commits money."*
5. **Roadmap as earn-out ladder, not calendar:** *"Phase 0 you just watched. Phase 1 puts the same plane on one real route in shadow — the first output is the counterfactual: would-have-held N, of which M true positives; no action held yet. Deterministic mechanisms work from the first request; statistics earn thresholds. Enforcement is earned per route from that evidence — never switched on from a slide."*
6. **Envelope clauses (fast):** same graph, same matrix, routes configure budgets — never truth semantics; payment/deletion/publication/regulated-advice lock to R3 at parse time; fail stance is tier-owned (R0/R1 open-with-annotation, R2/R3 closed-or-escalate — universal fail-open would make the plane bypassable under induced load); multi-turn is more STEPs on the same session ledger — prior assistant text is never evidence by reappearance; decision-support exists as an enterprise template on the same plane, not a third demo route.
7. **Commercial honesty, said out loud:** *"Integration is one SDK hook where you assemble context plus a reverse proxy — days, not quarters on a standard retrieval stack, and it is not zero. The integration cost is the moat; we say so, because drop-in is the promise that gets layers switched off. Latency: ≤40 milliseconds median, ≤200 at p95 on the read-only lanes that carry the volume — and we never make the model feel slow; we make the action wait."*

---

## 6. Differentiation & Defence Moments

Contrasts are **delivered inline where the evidence appears** (seeds in B3–B5), then compressed in B7 — never as a standalone attack slide.

| Contrast | Anchored at | Compressed B7 form |
|---|---|---|
| vs post-hoc observability | B3 step 5 (executor log) | "They record the exit beautifully. An audit trail is not an interlock." |
| vs LLM-as-judge | B3 step 2 (Interlock) | "'Does this look right?' is unfalsifiable, identity-blind, and cannot state its own error rate. 'Which span proves it?' has an answer — and no LLM sits in our decision path." |
| vs groundedness checkers | B3 step 2 + B5 | "Retrieval-only, averaged, action-blind. We price the worst claim per pending action. Retrieval is not permission." |

**Self-disclaimer (B7, verbatim spine):** *"Four things we refuse to claim: that we eliminate hallucinations. That integration is zero. That latency is zero. That one accuracy number covers three different mathematics. Every deck in this room disclaims its rivals. Almost none disclaim themselves. We just did — and we publish the number those claims would hide: our own miss rate, per route, empty until earned."*

**Bias (one sentence, measurement register):** *"The brief names bias; our entire posture fits in one sentence — counterfactual flip rate with a confidence interval, route-level, asynchronous, flagged when the interval excludes zero. Bias is a distributional property or it is nothing; it is never a per-response verdict."*

**Pre-empted attacks (delivered unprompted where marked; otherwise held loaded for Q&A):**

| Attack | Pre-empt at | The line that wins |
|---|---|---|
| B1 purely parametric | B4 (unprompted) | "We don't claim to verify what we were never given. We claim that what we were never given cannot authorise an action." |
| B5 prompt injection | B2 (unprompted) | "Binding is computed by us, not asserted by the model — injection has no channel to declare a binding." Honest boundary if pressed: "we defend the claim-to-evidence link, not the truth of the evidence." |
| A3 groundedness | B3/B5 | Retrieval-only · averages · action-blind · identity-blind. "Retrieval is not permission." |
| C1 latency | B6 (numbers stated correctly) | ≤40 ms p50 / ≤200 ms p95; tool-call verification completes inside the tool's own round-trip. **Never quote 40 as p95.** |
| C2 integration | B6 (said out loud as moat) | Real scope, days-not-quarters, never sold as drop-in. |
| D1 "how would you know your FNR?" | B4 (method clause) | Stratified shadow audit; the schema ships empty because the emptiness distinguishes design-time-knowable from not-yet-measured. **Never fill the placeholders.** |
| C5 "switched off in a quarter" | B6 ladder | The gate sits on actions; majority volume passes with annotation; enforcement is earned from counterfactuals nobody is asked to trust blind. |

---

## 7. Closing Beat (8:50–9:25)

Screen returns to the opening Action Gate panel — the same visual, now fully explained. P1. No new material.

> *(resolution of the opening)* "Tuesday, a system moved money on a clause that does not exist, and nothing in its path ever asked it for proof. *(gesture to the panel)* This is what asking looks like. Clause 7.2 has no span. The text was edited. The refund is held and escalated with the evidence packet. The money did not move."

> *(frozen close — negated then resolved, with a two-second hold between)* "That system was never asked to prove anything." *[hold]* "Now nothing acts until it can prove it should."

> *(button, category noun only)* "ControlPlane. Admission control for AI that acts."

Then stop speaking. Stand still. Do not thank the room twice, do not gesture at a "questions?" slide. The silence after the close is part of the close.

---

## 8. Anti-Patterns (Hard Kill List)

1. **Never open on risk** — no "AI is powerful but," no shocked customer, no angry email, no market statistic. Open on the held transaction.
2. **Never collapse the dual-action** into one response-level verdict or a "response blocked" banner. Two pending actions, two actuators, simultaneously.
3. **Never say "blocked" about the refund.** Say *held and escalated with the evidence packet*. Spoken word and grid must agree.
4. **Never lead with enablement.** Earned autonomy (Lever G) is named last and secondary; leading with "more AI, safely" is the generic deck's move.
5. **Never give clause 7.2 properties.** No "caps," "denies," "doesn't cover." Absence of evidence, not conflict.
6. **Never invert who loses.** The company wrongly pays out; the customer did not lose money.
7. **Never fill the FNR placeholders** — with plausible numbers, decorative values, or "prototype results" dressed as production. The emptiness *is* the claim.
8. **Never misquote latency.** ≤40 ms p50 / ≤200 ms p95; never 40 as p95, never relabel p50.
9. **Never redraw the matrix** — no low/med/high collapse, no invented tiers or actuators (`STREAM`, `Kill Span`, `Hold & Re-verify`, `Redact & Flag`). Transcribed, cells highlighted before actuators.
10. **Never use the banned register**: monitor · detect · observe · watch · guard · trust score · risk score · "responsible AI" as a standalone virtue. Sole exception: "Everyone watches the exit." Say: authorise · admit · prove · bind · refuse · hold · escalate · gate.
11. **Never show a confidence/logprob/trust-score surface** or an LLM-judge pane as ours; the incident's 0.94 exists only in narration.
12. **Never cycle scenarios.** One trace — the ₹1,84,000 refund — from hook through mechanism, matrix, packet and close. Breadth reads as slideware; depth reads as production experience.
13. **Never claim the four refused things about us**: eliminates hallucinations · zero integration · zero added latency · one accuracy number across failure modes. The refuse-to-claim list is about *us* — do not confuse it with the rejected-competitors list.
14. **Never drop bias, never moralise it.** One measurement-register sentence; never a per-response verdict; never a live third route.
15. **Never let secondary surfaces crowd the centre** — dead-compute charts, regulatory packs, bias widgets, chatbot chrome, triage-queue mock-ups. If a feature cannot be shown as a read of `STEP → SPAN → CLAIM → ACTION`, it lives in the proposal, not the pitch.
16. **Never present pre-baked motion as live compute.** Binding/entitlement/interlock visibly work (~20–80 ms); recordings are labelled with the build hash.
17. **Never let a slide say what the screen can prove.** The deck never covers the ledger; three slides maximum.
18. **Never soften the close.** No new information, no hedging, no trailing "so yeah" after the category noun.

---

## 9. Fidelity Self-Check

| Frozen invariant (Stages 1–4) | Protected at | How |
|---|---|---|
| Thesis: response = claims requesting permission to act | §1, B1, B8 | Stated verbatim in opening; resolved in close |
| Open on held transaction, never risk/person | B1 | Gate panel cold-open; incident narrated as fact, indictment structural |
| Provenance captured outside the model; model cannot author bindings | B2 | "No write path"; injection pre-empt; spans precede verdicts on screen |
| Default = UNSUPPORTED; "Not low confidence. Unproven." | B2, B3 | Claims born UNSUPPORTED on screen; C1 earns proof, C2 never does |
| Entitlement = deterministic set-membership, zero LLM | B3, B5, B6 | Dual-action C3 leg + full principal-flip beat; clearance ⊆ check shown, never scored |
| Exact R×S matrix transcribed; cells highlighted before actuators | B3 | Both cells (R1 × entitlement → Edit; R3 × unsupported-categorical → Escalate) shown before firing |
| Two-pending-actions resolution; never collapsed; refund never "blocked" | B1, B3, B8 | Fixed sequence; language law enforced in script and on-screen labels |
| Evidence-packet escalation; surgical edit only | B3 | Packet fields enumerated; strip-only edit, re-gated |
| Hard gate on actions, not tokens; hold-back; speculative release forbidden | B3, B6 | Text streams behind hold-back; `committed:false` in executor log; "make the action wait" |
| Worst claim per pending action — never an average | B3 | Spoken anchor contrasting groundedness averaging |
| `UNKNOWN` never → `SUPPORTED` | B4 | Stated as the false-assurance boundary |
| Parametric/no-provenance routes cannot authorise action | B4 | QA B1 line delivered verbatim, unprompted |
| Published FNR as format; emptiness is the credibility play | B4, B6, B7 | Full typed schema, all null; method clause; never filled (Kill List 7) |
| Latency law ≤40 p50 / ≤200 p95 | B6 | Correct quotation; never 40-as-p95 |
| Refuse-to-claim list is about *us* | B7 | Four refusals delivered as self-disclaimer, not competitor disclaimers |
| Bias kept, measurement terms, async route-level, never per-response | B7 | Single-sentence posture per frozen stance |
| One graph, three reads; no separate detectors/scores | B2, B6, B7 | Performance/cost/responsibility as reads of the same ledger; dead compute as backward walk |
| Roadmap = earn-out, shadow default, enforcement earned | B6 | Ladder, not calendar; "never switched on from a slide" |
| Exactly two live routes; decision-support proposal-only | B6 | Named as envelope template; no third demo route anywhere in the pitch |
| Content laws (clause 7.2 absent; company wrongly pays; customer did not lose) | B1, B3, B8 | Verbatim incident narration; Kill List 5–6 |
| Ship test | §1, §8 | If a judge can summarise the pitch as "it watches AI outputs and flags problems," the pitch has failed — every beat above is built to make that sentence impossible |

**Readiness bar (both presenters, from QA.md):** draw the `STEP → SPAN → CLAIM → ACTION` graph and the 4×4 matrix from memory · answer B1 and B5 cold · explain the empty FNR schema unprompted · state the two pending actions without conflating them · quote latency correctly. Drill B1 and B5 hardest — they are the first questions a serious engineer asks.

**Economic spine confirmed end-to-end (R2S4 §8):** AI can now act → an unproven claim must not authorise the action → provenance outside the model → default UNSUPPORTED → entitlement is set-membership → R×S prices proof by consequence → the hard gate sits on the commit path → the plane publishes what it missed. The pitch performs that spine in exactly that order.

---

*End of Stage 5 shard (ox-alpha). Stages 1–4 untouched; no new mechanism, no softened claim.*
