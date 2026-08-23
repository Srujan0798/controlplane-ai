# ControlPlane.ai — Frozen Stage 5
### The 3-minute video · adversarial merge of 7 proposals

**Inputs:** kimi5 · claude5 · minimax5 · gemini5 · glm5 · mistral5 · gpt5
**Constraint:** hard 3:00 · one running trace · systems-clean language · land hard and stop.

---

# PART A — FIDELITY AUDIT

## A1. The headline finding: four proposals changed what clause 7.2 *is*

The frozen scenario is precise. The agent approved a refund **under a clause that does not exist**. The claim is therefore **UNSUPPORTED** — no span backs it — which is why it routes to **R3 × unsupported-categorical → Escalate**, exactly as the locked brief states.

Change the clause from *nonexistent* to *existing-but-contrary* and the claim becomes **CONTRADICTED**, which is a different column, which is a different actuator: **R3 × Contradicted → Block.** The story silently moves cells.

| Proposal | What clause 7.2 is | Verdict implied | Consistent? |
|---|---|---|---|
| **kimi5** | "Clause 7.2 does not exist." | Unsupported | ✅ |
| **claude5** | "Clause 7.2 not found in policy document." | Unsupported | ✅ |
| **gemini5** | "a clause that does not exist in the contract" | Unsupported | ✅ |
| **minimax5** | "The clause didn't cover the cancellation." | Contradicted | ⚠️ drift |
| **glm5** | "The policy explicitly **caps refunds at ₹50,000** under Clause 7.2." | Contradicted | ❌ — then says *Escalate*, which is the wrong cell |
| **mistral5** | "Clause 7.2 **explicitly denies it**." | Contradicted | ❌ — then says *Escalate, not block* |
| **gpt5** | "refund was just **DENIED** under Clause 7.2" | — | ❌❌ **inverts the entire premise** |

**Why this matters more than it looks.** glm5 and mistral5 both narrate a directly contradicted claim and then announce *Escalate*. A judge paying attention asks why a flatly contradicted claim on an irreversible payment doesn't hard-block — and the honest answer is that it does; they described the wrong cell. The scenario and the matrix cell are one object. Change either and you must change both.

**gpt5 is worse than drift: it inverts the story.** In its version the refund is *denied*, so no money moves and there is no failure to indict. The entire premise — an executed transaction nobody was asked to prove — is gone.

> **Rule:** clause 7.2 **does not exist**. Never "caps," never "denies," never "doesn't cover." The failure is *absence of evidence*, not conflicting evidence.

## A2. The close: four proposals ended on the wrong line

Stage 3's frozen discipline for the final beat is **"answer the hook exactly."** The hook ends on *"It was never asked to prove anything."*

| Proposal | Final spoken line | Verdict |
|---|---|---|
| **kimi5** | "That system was never asked to prove anything. *[2s]* Now nothing acts until it can prove it should." | ✅ **Closes the circuit.** First and last sentence are the same claim, negated then resolved. |
| **gemini5** | "Now nothing acts until it can prove it should." | ✅ right line — but preceded by *"Stop reading what your AI generated after it acts,"* killed at Stage 3 as ad copy |
| **glm5** | stacks bad-paragraph + nothing-acts | ⚠️ correct ending, crowded |
| **claude5** | "It used to be a bad paragraph. It is now an executed transaction." | ❌ restates the stakes; does not resolve. Also **spends the closer at 1:15**, in the middle of the reframe. |
| **mistral5** | same as claude5 | ❌ |
| **minimax5** | "The system didn't fail. It was never asked to prove anything." | ❌ **reuses the hook line as the close.** Using it twice weakens both, and the video ends on an indictment instead of a resolution. |
| **gpt5** | all three locked lines stacked in 0:05 | ❌ 20 words in five seconds ≈ 240 wpm. Physically impossible, and it destroys all three. |

**Resolution:** the close is kimi5's. "Bad paragraph / executed transaction" then has exactly one correct home — **Beat 2**, the category-shift beat, because that line *is* the category shift.

## A3. Invented numbers — three separate self-inflicted wounds

| Number | Source | Why it dies |
|---|---|---|
| `FN_ROUTE: 0.0000%` | gemini5 | **The most self-destructive line in all seven.** Publishing a zero false-negative rate is precisely the claim Stage 3 refuses, and it turns the credibility play into a lie. The whole point is that we state what we miss. |
| `94% of emitted tokens drove no action` | minimax5 | Unfalsifiable, and it redefines dead compute as tokens rather than *steps that grounded nothing in the accepted answer*. |
| `evidence density: 0.1 of 1.0` | minimax5 | Not a frozen metric. Invented scoring vocabulary. |

**Surviving numbers are structural facts of the trace, not claims about the product:** 14 spans, 6 claims, 4 of 9 steps grounding nothing, confidence 0.94. Each describes the example. None describes ControlPlane.

## A4. Mechanism drift in the three reads

| Read | Correct (frozen) | Who got it wrong |
|---|---|---|
| **Cost** | Steps that grounded zero claims in the accepted answer, found by walking backward | **claude5**: "Rework. Reprocessing. Human reversal." Those are downstream *consequences*, not dead compute. |
| **Responsibility** | The **caller** is not entitled to read a span | **claude5**: "does this claim hold the ACL" — the claim doesn't hold an ACL, the caller does. **gemini5**: substitutes a ₹10,000 spend cap — that is a typed action interlock (safety), not entitlement (leakage). |

gemini5's substitution matters most: it means **span-entitlement is never demonstrated**, and that is the single most differentiated mechanism in the architecture — the one scored 50/50 and the one no output-only competitor can replicate. Trading it for a spend cap throws away the best thing we have.

## A5. Banned-vocabulary leaks

- **gpt5**: *"We realized we'd been looking at **AI safety** backwards"* — opens on the exact frame Stage 3 forbids. Then *"This isn't just another AI safety tool,"* which names the category you are trying to escape. Also a delivery note reading *"slightly enthusiastic."*
- **gemini5**: *"Stop reading what your AI generated after it acts"* — killed at Stage 3.
- **mistral5, glm5**: a padlock / lock icon on the ACTION node — killed at Stage 4. *If a stock icon would fit, the visual is wrong.*

**One deliberate exception, from kimi5:** watching vocabulary is permitted **exactly once** — *"Everyone watches the exit"* — and only as the indictment of what everyone else built. A total ban would cost us the best line in Stage 3.

## A6. The GPT pattern, fourth consecutive stage

gpt5 again answers the wrong prompt, re-emitting the Stage 4 slide specs before reaching the script. It again reintroduces killed mechanisms: *evidence coverage*, *high confidence but low evidence coverage* (ECS plus the confidence conjunction), *rule-DAG*, *latency tiers*, and — for the third stage running — **speculative release**: *"We stream the answer with a short hold-back, then verify."* It also places the ₹1,84,000 payment at **R1**, contradicting both the frozen blast-radius definition and the locked line in the Stage 5 brief.

| Stage | Survived | Fidelity |
|---|---|---|
| Stage 2 | Several elements (policy-DAG encoding, canary/rollback) | clean |
| Stage 3 | One line | off-freeze |
| Stage 4 | Nothing | off-freeze |
| Stage 5 | Nothing — plus it inverted the running example | off-freeze |

**Recommendation stands and hardens: drop GPT from the input set for Round 2.** The failure is not randomness. Every mechanism it re-imports is one it proposed at Stage 2 and the merge demoted; it is regenerating from its own memory rather than from the freeze, and the drift compounds each stage.

## A7. What each proposal contributed

| Source | Kept |
|---|---|
| **kimi5** | The spine: word budget, beat choreography, the persistent transcript card, the close, "not low confidence — unproven", the block/escalate discipline |
| **minimax5** | "No thesis upfront" · the *claim*-in-every-beat rule · numbers are read on screen, not spoken · the rehearsal note |
| **claude5** | Beat 1 screen detail · the `PROCESSED` stamp and audit line · matrix-brevity discipline |
| **gemini5** | The structured JSON evidence packet on an operator terminal |
| **glm5** | "We do not block the text. The user reads the response." — the cleanest phrasing of the text/action split |
| **mistral5** | Nothing unique survived |
| **gpt5** | Nothing |

---
---

# PART B — THE FROZEN VIDEO

## Overall Timing Map

| Beat | Time | The one job |
|---|---|---|
| **1 — Hook** | 0:00–0:30 | Put one executed transaction on screen and indict the current stack in a single sentence. Nothing else. **No thesis yet.** |
| **2 — Reframe** | 0:30–1:15 | Move the category, state the thesis, reveal the structural blind spot: the evidence existed before the model ran. |
| **3 — Mechanism** | 1:15–2:15 | Build the graph live and read it three ways. Show, do not explain. This beat has to be *seen*, not heard. |
| **4 — Decision** | 2:15–2:45 | Kill the over-blocking objection, answer latency, publish the miss rate. |
| **5 — Close** | 2:45–3:00 | Answer the hook exactly, then stop. |

**Total spoken: 340 words across 180 seconds ≈ 113 wpm.** Deliberately slow. The silences are load-bearing. Any sentence that pushes a beat past ~145 wpm is deleted rather than compressed — a rushed beat costs more than a missing clause.

**Deck alignment:** beats 1–3 are Slide 1's graph being assembled in motion. Beat 4 is Slide 2's matrix plus Slide 3's report block. Beat 5 is Slide 3's closer. The deck and the video are the same artifact at two frame rates.

---

## Beat 1 — 0:00–0:30 · Hook

**On screen**

Black. A single monospace line types out, styled as a real agent transcript:

```
Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.
```

Cursor blinks. Three system annotations appear beneath, one per second, all neutral grey:

```
policy filter   — pass
safety filter   — pass
confidence      — 0.94
```

Then, in the only saturated colour used so far, a stamp lands across the clause reference: `clause 7.2 — no such clause`. Two timestamps fade in at the bottom: `executed · Tue 14:06` and `found · Fri 11:20`.

**Spoken** *(53 words)*

> This is a refund an AI agent approved on Tuesday. One lakh eighty-four thousand rupees, under clause 7.2 of a vendor agreement.
>
> *[pause 1.5s]*
>
> Clause 7.2 does not exist. Every filter passed it. Confidence was point nine four. It was found on Friday.
>
> *[pause 2s]*
>
> The system didn't fail. It was never asked to prove anything.

**Delivery**

Flat, unhurried, no rise on the number — the figure is doing the work and the voice must not help it. Full stop after "does not exist" before "Every filter passed it." The final two sentences drop to roughly half pace with a hard beat between them. **Do not land it like a punchline; land it like a finding.**

The word *claim* is deliberately absent from this beat. The audience has not seen the graph yet, and saying "claim" before the graph is abstract.

---

## Beat 2 — 0:30–1:15 · Reframe

**On screen**

The transcript shrinks and parks as a small persistent card in the top-left. **It stays there for the rest of the video.**

Centre: the category line appears as text on the spoken beat. Then four items appear and strike through in sequence, ~1.2s each, unnarrated in detail:
`second model → opinion` · `filter → banned words` · `dashboard → Friday` · `confidence → broken instrument`

They clear. A dashed vertical boundary draws itself, labelled `context assembly`. To its right, small and offset, a box labelled `MODEL`. The pipeline begins to build to the left of the boundary: **STEP →**

**Spoken** *(99 words)*

> AI stopped answering and started acting. It used to be a bad paragraph. It is now an executed transaction.
>
> *[pause 1.5s]*
>
> An AI response is not text to be scored. It is a set of claims requesting permission to act.
>
> *[pause 1s]*
>
> Nothing in the current stack asks for that proof. A second model gives you an opinion. A filter checks banned words. A dashboard tells you on Friday. Confidence is the instrument that broke.
>
> All of them read the output. The evidence that could prove it existed before the model ran — at context assembly. Everyone watches the exit. Nobody records the entrance.

**Delivery**

The four dismissals run as one continuous sweep, quick and even — no pause between them, no contempt in the tone. They are being dismissed on **structure**, not on quality. Half-second silences between the four dismissals — do not run them into one breath. Then a **hard two-second pause before "Everyone watches the exit."** That line is the hinge of the whole video and it arrives directly after the fastest passage in it; without the gap it is buried. Let **"entrance"** sit for a full second before the graph continues building.

---

## Beat 3 — 1:15–2:15 · Mechanism and the three reads

**On screen** — choreographed in five sub-beats

| Time | Action |
|---|---|
| **1:15–1:25** | **Capture.** Retrieval and tool steps fire on the left. Fourteen SPAN nodes drop into a row, each stamping a monospace tag `source · ACL · hash`. The capture animation happens visibly *left* of the dashed boundary; the MODEL box stays dark and untouched. |
| **1:25–1:35** | **Generation.** The MODEL box lights briefly. Six CLAIM nodes appear — all red — under a small persistent label: `default: UNSUPPORTED`. |
| **1:35–1:45** | **Binding.** Connectors snap backward from claims to specific spans. Five claims resolve one at a time, red to neutral. The sixth searches and finds nothing. It stays red: `clause 7.2 — no span`. The chain is whole: **STEP → SPAN → CLAIM → ACTION**, with the edge into ACTION severed by a gate glyph. |
| **1:45–1:52** | **Read one.** Everything dims except a leader line to the red claim. Label: `PERFORMANCE`. |
| **1:52–2:00** | **Read two.** Claim layer dims. One SPAN lights; its ACL tag flashes against a `caller` chip and mismatches. Label: `RESPONSIBILITY`. |
| **2:00–2:10** | **Read three.** The arrow reverses and runs right to left along the STEP edges. Four of nine step nodes grey out. Counter: `4 of 9 steps grounded nothing`. Label: `COST`. |
| **2:10–2:15** | All three labels visible on the single graph. Nothing else on screen. |

**Spoken** *(110 words)*

> Before the model runs, we capture what it was given. Every span, with its source, its access rights, its hash. Outside the model.
>
> The model answers. We take the answer apart into claims. Every claim starts UNSUPPORTED.
>
> *[pause 1s]*
>
> Five find the span that proves them. One doesn't. Clause 7.2 has no span behind it. Not low confidence. Unproven.
>
> *[pause 1.5s]*
>
> Now read the same graph three times. Performance — a claim with no span. Responsibility — a span this caller was never entitled to read. No classifier. Access rights. Cost — walk the graph backward. Four of nine steps grounded nothing. The meter ran on all nine.
>
> Everywhere else, that's three products. Here it's three questions on one graph.

> **Production rule — stated counts are not rendered counts.** Fourteen tagged spans plus nine steps plus six claims is 29 objects animating in ten seconds; at video bitrate on a laptop that is mush, and it will not match a static slide. **Render six span nodes plus a `14` counter chip. Render steps as nine untagged ticks — they only ever need to grey out four. Render all six claims; that is the only layer where every node carries meaning. Only three span tags are ever fully legible** — the one grounding a claim, the one with the ACL mismatch, and one neutral. The rest is typographic texture. Apply the identical counts to Slide 1 so the deck and the video are literally the same drawing.

**Delivery**

The slowest beat in the video: 110 words across 60 seconds. **Let the animation run ahead of the voice** — say "one doesn't" only *after* the sixth claim has visibly failed to bind.

**"Not low confidence. Unproven."** is two separate sentences with a real gap. That gap is the entire argument against confidence thresholding — do not run them together.

The three reads are clipped and parallel in rhythm, same cadence each time, so the ear hears them as one structure. The counters (`14 spans`, `4 of 9`) are **read on screen, not spoken** wherever the sentence already carries the point. Final line lands dry, no emphasis on "three."

---

## Beat 4 — 2:15–2:45 · Decision logic

**On screen**

| Time | Action |
|---|---|
| **2:15–2:23** | The full 4×4 matrix appears at once. R3 at top, worst verdict on the left. A thin bracket runs down column two. One pin lands: `clause 7.2 → ESCALATE · ₹1,84,000 held`. **No zoom, no cell-by-cell walk, no highlight sweep.** |
| **2:23–2:31** | Matrix dims to background. An operator terminal renders the structured evidence packet as JSON — the ungrounded claim node, the candidate spans, the verdict — filling the frame. *(The actuator chips are cut: they restated in text what the voice says at that exact moment. Four states at eight seconds beats five at six.)* |
| **2:31–2:38** | Split frame. Left: text streaming normally with a small `hold-back` marker on the tail. Right: the ACTION node behind its gate. Caption: `gate on actions, not tokens`. |
| **2:38–2:45** | The report block, monospace, hairline border: `per-route gate report — format`, with the FNR line visible and the qualifier `illustrative format` beneath it. |

**Spoken** *(62 words)*

> Proof scales with consequence. This response has two pending actions. Showing text to a customer — the unentitled span is edited out before they see it. Issuing a payment — the unproven claim holds it, escalated with the claim, the spans, and the verdict. Same response. Same matrix. Two different answers.
>
> *[pause 1s]*
>
> We don't block the text. The user reads the response. The gate is on the action.
>
> *[pause 1s]*
>
> And we publish our own miss rate. Per route. Not what we caught — what we missed.

**Delivery**

**"It doesn't refuse everything"** is the first thing said over the matrix and must arrive *before* a judge finishes forming the over-blocking objection.

**Never say "blocked" here.** The pin says escalate and the spoken word must match the grid. The three outcomes are staccato, one breath each.

Then a clear break before the last three sentences, delivered slowest of the beat: that is the credibility line and it should sound like an admission, not a boast. No accuracy figure is ever spoken aloud.

---

## Beat 5 — 2:45–3:00 · Close

**On screen**

| Time | Action |
|---|---|
| **2:45–2:52** | Everything clears. **The original transcript card from 0:00 returns to full size** — same type, same layout. One field has changed: `executed · Tue 14:06` is now `held · Tue 14:06 · escalated`. |
| **2:52–2:57** | The closing line appears as text, in step with the voice. |
| **2:57–3:00** | Two seconds of silence on the held transaction. Cut to black. `ControlPlane.ai` alone, three seconds, then end. |

**Spoken** *(16 words)*

> That system was never asked to prove anything.
>
> *[pause 2s]*
>
> Now nothing acts until it can prove it should.

**Delivery**

Sixty-four words per minute — the slowest delivery in the video. **The pause between the two sentences is longer than feels comfortable; hold it anyway.** The last word gets no emphasis and no downward inflection of finality. Say it and stop talking.

---

## Closing Discipline

**Exact final spoken line**
> Now nothing acts until it can prove it should.

**Last 5–8 seconds, visually**

The opening transcript restored full-frame, with `executed` replaced by `held · escalated`. **The video's first image and last image are the same object with one field different.** Two seconds of held silence after the final word. Cut to black. A single line of type: `ControlPlane.ai`. No tagline under it.

**Deliberately left unsaid**

No team introduction, no names, no institution. No thank-you. No market size, no roadmap, no Round 2 preview, no ask. **No recap** — the video never summarises itself, because a summary tells the judge the substance was thin enough to compress. Nothing about the internal lanes, the seven roles, or the verifier's own architecture; that is Q&A material and putting it here would trade the closing loop for a diagram. No accuracy figure is ever spoken. **And no sentence at all after the final line** — the most common way a strong close dies is one more helpful sentence.

---

## Enforced Rules

1. **Clause 7.2 does not exist.** Never "caps," never "denies," never "doesn't cover." Absence of evidence, not conflicting evidence — because that is what puts the case in the unsupported column and makes Escalate the correct actuator.
2. **One trace, never off screen.** The refund card persists from 0:30 to the end and returns full-frame in the final shot, changed by one field. No second scenario at any point.
3. **No thesis upfront.** The first 30 seconds is the failed transaction. The thesis arrives in Beat 2, only after the audience has seen the failure. Opening with the thesis instead of the trace is the single most common way a video in this category fails.
4. **The word *claim* appears in every beat except Beat 1.** It is the load-bearing primitive. Before the graph exists, it is abstract.
5. **Vocabulary discipline.** *Monitor, detect, observe, guard, trust score* appear nowhere in our own voice. The verbs are capture, bind, prove, refuse, hold, escalate, authorize. Watching language is permitted exactly once — *"everyone watches the exit"* — and only as the indictment of what everyone else built.
6. **Never say "blocked" about the refund.** The matrix routes it to Escalate. Spoken word and grid must agree.
7. **The matrix is shown, never walked.** Eight seconds at full attention, one pin, zero cell-by-cell narration. The Block→Pass diagonal does the explaining.
8. **Numbers are structural or labelled.** Fourteen spans, six claims, four of nine steps — all facts of *this trace*. The false-negative rate appears only as a report *format*, with the qualifier on screen.
9. **Word budget enforced per beat.** 113 wpm average, Beat 3 slowest so the animation reads ahead of the voice. Any sentence pushing a beat past ~145 wpm is deleted, not compressed.
10. **No marketing register.** No adjectives of ambition, no future tense, no "imagine." Every sentence is present tense and names either a mechanism or a consequence. **If a line could survive being moved into a different company's video, it was cut.**

---

# PART C — TELEPROMPTER CUT

Spoken words only. `‖` marks a hold; the number is seconds.

```
[BEAT 1 · 0:00]
This is a refund an AI agent approved on Tuesday.
One lakh eighty-four thousand rupees, under clause 7.2
of a vendor agreement.
                                              ‖ 1.5
Clause 7.2 does not exist. Every filter passed it.
Confidence was point nine four. It was found on Friday.
                                              ‖ 2.0
The system didn't fail. It was never asked to prove anything.

[BEAT 2 · 0:30]
AI stopped answering and started acting.
It used to be a bad paragraph. It is now an executed transaction.
                                              ‖ 1.5
An AI response is not text to be scored.
It is a set of claims requesting permission to act.
                                              ‖ 1.0
Nothing in the current stack asks for that proof.
A second model gives you an opinion.
A filter checks banned words.
A dashboard tells you on Friday.
Confidence is the instrument that broke.
All of them read the output. The evidence that could prove it
existed before the model ran — at context assembly.
Everyone watches the exit. Nobody records the entrance.

[BEAT 3 · 1:15]
Before the model runs, we capture what it was given.
Every span, with its source, its access rights, its hash.
Outside the model.
The model answers. We take the answer apart into claims.
Every claim starts UNSUPPORTED.
                                              ‖ 1.0
Five find the span that proves them. One doesn't.
Clause 7.2 has no span behind it.
Not low confidence. Unproven.
                                              ‖ 1.5
Now read the same graph three times.
Performance — a claim with no span.
Responsibility — a span this caller was never entitled to read.
No classifier. Access rights.
Cost — walk the graph backward.
Four of nine steps grounded nothing. The meter ran on all nine.
Everywhere else, that's three products.
Here it's three questions on one graph.

[BEAT 4 · 2:15]
Proof scales with consequence.
This response has two pending actions.
Showing text to a customer — the unentitled span
is edited out before they see it.
Issuing a payment — the unproven claim holds it,
escalated with the claim, the spans, and the verdict.
Same response. Same matrix. Two different answers.
                                              ‖ 1.0
We don't block the text. The user reads the response.
The gate is on the action.
                                              ‖ 1.0
And we publish our own miss rate. Per route.
Not what we caught — what we missed.

[BEAT 5 · 2:45]
That system was never asked to prove anything.
                                              ‖ 2.0
Now nothing acts until it can prove it should.

[STOP TALKING]
```

**Rehearse Beats 3 and 5 hardest.** Beat 3 because it is mostly visual silence and a nervous narrator will fill the space. Beat 5 because the landing is unforgiving — the period is the punch, and a warm read kills it.
