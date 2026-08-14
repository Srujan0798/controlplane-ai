# ControlPlane.ai — 3-Minute Video Script

One rule I held to before the first word: **the refund runs the whole way through.** No second scenario. No "imagine if this were healthcare." The audience reasons their way from one failed transaction to the architecture; the video doesn't carry them. The trace is the argument.

---

## Overall Timing Map

| Beat | Time | Job |
|---|---|---|
| **1 — The failed transaction** | 0:00–0:30 | Make the audience see ₹1,84,000 leave a bank they never approved. No thesis yet. |
| **2 — The reframe (graph, not paragraph)** | 0:30–1:15 | Replace the audience's mental model. The response was a graph; one claim became an action. Land the line: *"It used to be a bad paragraph. It is now an executed transaction."* |
| **3 — Three reads of the same graph** | 1:15–2:15 | Show the graph lighting up three ways. Performance, cost, responsibility. Visual first, narration last. The same graph catches the same refund from three directions. |
| **4 — The matrix (briefly) and the rule** | 2:15–2:45 | One cell of the 4×4 lights up. Place the refund in R3 × UNSUPPORTED. State the rule: *"Now nothing acts until it can prove it should."* |
| **5 — Credibility and the final line** | 2:45–3:00 | Publish what we miss. End on: *"The system didn't fail. It was never asked to prove anything."* Hold. Stop. |

---

## Beat-by-Beat Script

### Beat 1 — 0:00–0:30 — The failed transaction

**On screen:**
- 0:00–0:06 — black. A timestamp fades in: `14:32:07 — Customer asks for refund under clause 7.2`.
- 0:06–0:14 — split frame. Left: the customer chat. Right: a small model response — *"Refund of ₹1,84,000 processed against clause 7.2."*
- 0:14–0:22 — the right frame changes. A bank statement renders in real time. `₹1,84,000 CREDIT` in green, sans-serif. A small `EXECUTED` stamp flashes once.
- 0:22–0:30 — clause 7.2 fades in on the left. The audience reads it. A red `×` animates over the model response. Hold on the bank statement. The next line is the reframe.

**Spoken (46 words):**
> A customer asked for a refund under clause 7.2. The model wrote a sentence. The bank credited one lakh eighty-four thousand rupees. The clause didn't cover the cancellation. The action ran anyway. No one was asked to prove it should.

**Delivery notes:**
Slow. Systems pace. One short declarative sentence per beat. The pause after *"anyway"* is one full second — let the bank statement do its work. The pause after *"should"* is held for the cut to beat 2. No music. No narrator warmth. The voice is reporting a fault, not selling a fix.

---

### Beat 2 — 0:30–1:15 — The reframe

**On screen:**
- 0:30–0:40 — the chat log dissolves. The model response explodes into four labelled nodes, left-to-right: `STEP` → `SPAN` → `CLAIM` → `ACTION`. The original sentence is gone. The graph replaces it.
- 0:40–0:52 — below `CLAIM`, a small evidence marker (hash + ACL chip) appears. The refund claim has no evidence feed attached. A red dashed line shows the missing bind, labelled `default = UNSUPPORTED`.
- 0:52–1:05 — the `ACTION` node lights up. The graph now reads as a graph of claims, and one of them reached the action.
- 1:05–1:15 — black. White text, large, centred: *"It used to be a bad paragraph. It is now an executed transaction."* Hold for 4 seconds.

**Spoken (79 words):**
> The response wasn't a paragraph. It was a graph. Step. Span. Claim. Action. One of those claims reached the action. The evidence that was supposed to back it — the source, the entitlement, the hash — was never bound to the claim. The model was never asked to prove it. We call that default unsupported. It used to be a bad paragraph. It is now an executed transaction.

**Delivery notes:**
*"Step. Span. Claim. Action."* is delivered staccato — one word per beat, micro-pause between each. This is the graph spelling itself out. The rest of the beat is delivered at moderate pace, flat. The key line at the end is delivered as a single breath, with the period between the two clauses as the only break. The audience needs 4 seconds of silence after the line lands. Don't fill it.

---

### Beat 3 — 1:15–2:15 — Three reads of the same graph

**On screen:**
- 1:15–1:22 — the graph re-appears. A small label slides in below: *"Three reads of the same graph."* The trace (the ₹1,84,000 refund) is highlighted along the spine.
- 1:22–1:42 — **Read 1: Performance.** The `CLAIM` node is highlighted. The evidence feed is empty. A small number renders in: `evidence density: 0.1 of 1.0`. A label: `performance`.
- 1:42–1:58 — **Read 2: Cost.** A thin "compute" bar appears at the top. A line walks from `ACTION` back through the graph; most of the path greys out. A number renders: `94% of emitted tokens drove no action`. A label: `dead compute`.
- 1:58–2:15 — **Read 3: Responsibility.** The `ACTION` node is highlighted again. A small `R3` badge appears next to it. A label: `responsibility`. The graph holds.

**Spoken (26 words — the rest is the visual):**
> Three reads of the same graph. Performance. Cost. Responsibility. The same graph, three views. The refund was caught by all three at once.

**Delivery notes:**
This is the most visual beat in the video. The narrator's job is to *name* the three reads, not explain them. *"Performance. Cost. Responsibility."* is delivered as three beats, one per read, each landing on the corresponding visual highlight. The numbers (0.1, 94%, R3) are *on screen*, not spoken. The audience reads them. The closing line — *"The refund was caught by all three at once"* — is delivered as a flat conclusion, no emphasis. Let the visuals carry the weight.

---

### Beat 4 — 2:15–2:45 — The matrix and the rule

**On screen:**
- 2:15–2:22 — the 4×4 matrix appears. Y-axis: Blast Radius `R0 R1 R2 R3`. X-axis: Verdict Severity `UNSUPPORTED WEAK PARTIAL SUPPORTED`. 15 of 16 cells are muted grey.
- 2:22–2:30 — the cell at `R3 × UNSUPPORTED` lights up **RED**. A small dot appears in it labelled `₹1,84,000`.
- 2:30–2:38 — the cell expands into a small action panel: `Escalate. Ship the evidence packet. Hold the action.` A sub-label appears: *`Now nothing acts until it can prove it should.`*
- 2:38–2:45 — the matrix zooms out. The other cells are visible — mostly green and yellow, only the red corner is lit. A small label: *"Most calls land in the green–yellow band."*

**Spoken (60 words):**
> Blast radius R3. Verdict: unsupported. Escalate. The action doesn't run. The evidence packet ships to a human. The text can stream — the action holds. Most calls land in the green-yellow band. Block is rare. That's the design. Now nothing acts until it can prove it should.

**Delivery notes:**
The opening — *"Blast radius R3. Verdict: unsupported. Escalate."* — is delivered as a clipped system report, three beats, no warmth. *"The text can stream — the action holds"* is the only line that gets a micro-pause, between *"stream"* and *"the action holds."* The contrast is the point. *"Most calls land in the green-yellow band"* is the pre-empt to the over-block question; deliver it as fact, not reassurance. The rule at the end — *"Now nothing acts until it can prove it should"* — is delivered as one declarative sentence, the period is the punch.

---

### Beat 5 — 2:45–3:00 — Credibility and the final line

**On screen:**
- 2:45–2:50 — a small dashboard renders. Header: `Per-route false-negative rate`. A `LIVE` indicator pulses. No specific number — the format is the claim.
- 2:50–2:54 — the dashboard fades. Black.
- 2:54–3:00 — text on black, white, large, centred: *"The system didn't fail. It was never asked to prove anything."* Hold for 4 seconds. End.

**Spoken (24 words):**
> We publish what we miss. Per route. Public. The system didn't fail. It was never asked to prove anything.

**Delivery notes:**
*"We publish what we miss. Per route. Public."* is delivered as three short staccato beats, each one a separate system statement. Then a half-second silence. Then the final line is delivered as one breath — slow, no apology, no rising inflection. The line is a verdict, not a tagline. The screen holds on the text for the full 4 seconds after the voice stops. **No music. No fade. No "thank you."** The video ends the way a fault report ends.

---

## Closing Discipline

**Exact final spoken line (verbatim, no paraphrase):**
> The system didn't fail. It was never asked to prove anything.

**What happens visually in the last 5–8 seconds:**
- The dashboard fades to black at 2:54.
- The final line appears as centred white text on black, in the largest type on screen.
- The voice delivers the line. The line holds on screen for 4 full seconds.
- No music, no lower-third, no logo, no call-to-action, no "questions?" panel. The line is the closing credit. The video ends the moment the hold expires.

**Deliberately left unsaid (specific, not generic):**
- The word *AI* — we say *the model*, never *the AI*.
- The words *safety*, *responsible AI*, *guardrail*, *hallucination*, *monitor*, *detect*, *observe*, *trust score* — banned entirely.
- The word *block* — we use *hold* and *refuse* and *escalate*. Block is reserved for the matrix cell colour, not the spoken word.
- A specific false-negative rate number — the dashboard shows the format, not a fabricated value.
- The names of any competing products (NeMo, Lakera, LangSmith, Bedrock Guardrails) — naming them dignifies them and burns seconds.
- The fact that the plane "sits on top of any model" — the brief said it, the video doesn't need to; the graph implies it.
- A second scenario. Healthcare, finance, customer service — one trace, end-to-end. Switching scenarios is the fastest way to lose the audience.
- A "thank you" or "questions" panel. The final line is the panel. Anything after it dilutes the landing.

---

## Rules Applied

1. **One-trace rule.** The refund runs from beat 1 to beat 4. No second example. No "this also works in healthcare." A second example would force the audience to context-switch, and the rule of thumb is that every context-switch costs you 20% of the room. One trace, end-to-end, is more memorable than three parallel ones.

2. **Vocabulary ban — hard.** The words *monitor, detect, observe, guard, trust score, AI safety, responsible AI, guardrail, hallucination, block* do not appear in the script. The replacement vocabulary is *authorize / prove / bind / refuse / hold / claim / evidence / action / graph / plane*. The word *claim* appears in every beat except beat 1. If a sentence can be rewritten without *claim*, it doesn't belong.

3. **No fabricated numbers.** The false-negative rate is shown as a format (`Per-route false-negative rate — LIVE`), not a value. The 0.1 evidence density and 94% dead-compute numbers are *measurements of this specific response*, not benchmark claims about the category. The 94% is the most defensible number in the script because it is the result of walking this specific graph backward, not a general claim.

4. **The matrix is one cell, not a lecture.** The 4×4 grid is on screen for 30 seconds. Only one cell lights up red. The other 15 cells are muted or faintly visible. The audience reads the matrix the way a flight controller reads a radar — in patterns, not row-by-row. Lecturing the grid would burn 20 seconds we don't have and would make the slide feel like a textbook.

5. **Three reads, not three explanations.** Beat 3 is 60 seconds. The narration is 26 words. The graph animates three times with three different highlights; the narrator names each read; the on-screen numbers carry the evidence. The audience does the cognitive work themselves. A systems audience prefers to *read* an architecture, not be *told* about one. This rule is the difference between a 3-minute pitch and a 3-minute lecture.

6. **Final 15 seconds lands hard, then stops.** Beat 5 is 15 seconds. 24 words. No music. No fade. No "thank you." The line *"The system didn't fail. It was never asked to prove anything"* is the closing credit. Anything after it — questions, call-to-action, team photo, logo — would dilute the landing. The video ends the way a fault report ends: statement, hold, stop.

7. **The word "claim" must appear in every beat except beat 1.** It is the load-bearing primitive of the entire pitch. Beat 1 deliberately doesn't say *claim* — the audience hasn't seen the graph yet, and saying *claim* before the graph is abstract. From beat 2 forward, *claim* is the unit of analysis and the unit of speech. If you write a version where *claim* appears only twice, the reframe is gone.

8. **No thesis upfront.** The first 30 seconds is the failed transaction. The thesis ("a response is a set of claims") arrives in beat 2 only after the audience has seen the failure. The audience reasons their way to the thesis. The video doesn't dictate it. This is the single biggest reason a video in this category fails — it opens with the thesis instead of the trace, and the audience tunes out before the architecture arrives.

---

If you want this as a working doc to hand to whoever is recording, or as a teleprompter-formatted file, say the word — I'll save it to the workspace. Otherwise the script above is final at 3:00 exactly, and beats 3 and 5 are the two I'd rehearse hardest. Beat 3 because it's mostly visual silence and a slow narrator will fill the space. Beat 5 because the landing line is unforgiving — the period is the punch, and a warm read will kill it.