# ControlPlane.ai — The 3-Slide Deck

One rule I'm holding to while writing this: every slide has 8 seconds of a judge's attention. The dominant visual carries the slide. The bullets confirm it. Everything else gets cut. Two lines I considered for the slides got killed in this pass; I'll name them at the end so you know what I removed and why.

---

## Slide 1 — The Reframe

**Headline (10 words):**
**An AI response is a graph of claims asking to act.**

**Primary visual (centre, ~60% of slide):**
A single rectangle on the left, labelled `RESPONSE`, containing a small block of placeholder text. From its right edge, four nodes flow left-to-right: `STEP` → `SPAN` → `CLAIM` → `ACTION`. The `ACTION` node is rendered larger than the other three and is the only saturated-colour element on the slide. Below `CLAIM`, four small "evidence" markers (tiny hash icons, each tagged with a small `ACL` chip) feed upward into the node. One of the four evidence feeds is broken — rendered as a dashed line terminating in red, with the label `default = UNSUPPORTED` sitting next to the break.

**Supporting text (4 short lines, top-left under headline):**
- Evidence captured at context assembly. Outside the model. Source, ACL, hash.
- Default = UNSUPPORTED. Burden of proof is inverted.
- Three reads of one graph: performance, cost, responsibility.
- We gate the action. Not the text.

**Footer (lower-right, small):**
*Without the plane: ₹1,84,000 against clause 7.2. With the plane: the claim never reached the action.*

**Design notes:**
- The graph is the argument. Roughly 60% of the slide.
- The broken evidence feed (red dashed line) is the second-strongest visual — it makes the inverted burden of proof literal without saying the words.
- `ACTION` is the only saturated node. Everything else is muted greyscale.
- No shields, locks, eyes, dashboards, magnifying glasses. The visual is a graph, not a metaphor. If a stock-photo icon would fit, the visual is wrong.

---

## Slide 2 — The Decision System

**Headline (10 words):**
**The matrix decides. The text streams. The action waits.**

**Primary visual (centre, ~55% of slide):**
A 4×4 matrix, the dominant object on the slide.
- **Y-axis (top→bottom):** Blast Radius — `R0` (read, self), `R1` (read, internal), `R2` (write, internal), `R3` (write, external / customer).
- **X-axis (left→right):** Verdict Severity — `UNSUPPORTED`, `WEAK`, `PARTIAL`, `SUPPORTED`.
- **Cell colour:** 12 of 16 cells are muted grey. Four cells light up:
  - `R3 × UNSUPPORTED` — **RED** — *Escalate. Block the action.*
  - `R2 × UNSUPPORTED` — **ORANGE** — *Surgical edit.*
  - `R1 × WEAK` — **YELLOW** — *Audit. Pass.*
  - `R0 × SUPPORTED` — **GREEN** — *Pass.*
- One small annotation in the lower-right of the matrix: *"Most calls land in green–yellow. Block is rare. That's the design."*

**Supporting elements (single column beneath the matrix, smaller, muted):**
- Hard gate on actions. Optimistic text stream with a short hold-back.
- Surgical edit only. Escalate ships the evidence packet.
- Dead compute measured by walking the graph backward.

**Design notes:**
- The matrix is the slide. The headline is a sentence-long caption; the matrix is the proof.
- Exactly one RED cell. Multiple reds dilute it. The R3×UNSUPPORTED cell is the visual climax of the deck — that is where the ₹1,84,000 example would have lived.
- "Dead compute" is the weakest of the three supporting lines. If the slide crowds, kill that line first. It survives in the speaker notes; it does not survive on the slide.
- No per-axis sub-graphics. No separate "performance / cost / responsibility" mini-charts. The matrix is the answer to all three at once.

---

## Slide 3 — Why This Is Different (and Believable)

**Headline (9 words):**
**We don't score the model. We publish what we miss.**

**Left side (what we refuse — grey, dimmed):**
- ✕ LLM-as-judge
- ✕ Composite risk scores
- ✕ Static guardrails
- ✕ Post-hoc observability

**Right side (what we publish — single accent colour):**
- Per-route false-negative rate.
- Public. Updated continuously.
- Policy auto-rolls back on override-spike.

**Closing line (largest text on the slide, ~40–50pt, centred, bottom third):**
**The system didn't fail. It was never asked to prove anything.**

**Design notes:**
- The closing line is roughly 2.5–3× the size of every other text on the slide. It is the slide. Everything else is supporting cast.
- The refusals on the left are deliberately grey. The publications on the right are the only saturated items besides the closing line. The visual logic: *we've already conceded the standard answers; here's the unusual part.*
- No company logo, no team photo, no "thank you" panel. The closing line is the panel.
- If the slide starts to look like a list, you've added something that doesn't earn its place. Cut until the closing line is alone on the bottom half.

---

## Tensions I had to resolve (and what I cut)

**1. Slide 1 wants the reframe, the graph, the inverted burden, and the three-axis idea all at once.** They are four ideas, not one. Resolution: the *graph* is the visual; the inverted burden is the *broken evidence feed* (a single line, not a paragraph); the three-axis idea is *one* supporting line, not three sub-visuals. The graph is doing 70% of the cognitive work. Bullets confirm it, they don't replace it.

**2. Slide 2 wants the matrix, the action-vs-text latency principle, surgical edit, escalate, AND dead compute.** Five ideas, one slide. Resolution: "the action waits, the text streams" is *already in the headline* — the latency principle doesn't need its own line. Surgical edit and escalate are *shown* by the cell colours, not stated separately. Dead compute survives only as one supporting line; if the slide crowds, it gets cut first. *I want you to know I considered cutting it — but it earns its place because it is the cost-axis equivalent of the inverted-burden-of-proof idea on slide 1. Without it, slide 2 becomes a safety matrix, not the cost-and-responsibility-reads-of-the-graph story.* Keep it, but only if the matrix leaves room.

**3. Slide 3 wants refusals + publications + closing line + (possibly) the matrix recap.** Resolution: the matrix and graph do *not* appear on slide 3. This slide is "why should I believe you," not "how does it work." The closing line is the slide. Five text elements total: headline, four refusals, three publications, one closing line. If you add a sixth, you dilute the closing line — and the closing line is the line judges quote in their notes.

**4. The frozen key line "it used to be a bad paragraph. It is now an executed transaction" doesn't have a natural home on the slides.** I tried it on slide 1 as the headline (too long, too clever for 8 seconds of attention) and on slide 2 as a footer (fights the matrix). **It belongs in the 3-minute video, spoken at 0:30–0:45, not on the slides.** Slides are for visuals; the video is where the punchline lands. The slides end on *"The system didn't fail. It was never asked to prove anything."* The video ends on the same line, but arrives at it via the bad-paragraph line first.

**5. The refund example (₹1,84,000 / clause 7.2) appears on exactly one slide — slide 1, as a footer annotation.** It is the only concrete example on the deck. It earns its place because it grounds the abstract graph in a single failure the judges can picture. Using it on slides 2 or 3 would dilute the matrix climax and the closing line respectively.

---

**One last cut I made for you:** I considered adding a small "stage 0" callout on slide 2 — *context assembly is the only place we touch the model*. The matrix is already implying it. Don't add it. The slide stops being absorbable in 8 seconds the moment a sixth element appears.

If you want this as a working doc to hand to a slide designer, say the word — I'll save it to the workspace and you can pass it through. Otherwise the deck above is final, and the speaker notes for the video are where the remaining mechanisms (dead compute, the ACL deterministic check, the override-spike rollback) live.