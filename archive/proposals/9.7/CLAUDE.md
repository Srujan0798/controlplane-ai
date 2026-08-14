You've hit your session limit · resets 2:40pm (UTC)# Final Elevation Audit — ControlPlane.ai

## 1. Overall Diagnosis

**Current true strength: 9.3/10.**

Not 9.5. The architecture is genuinely production-grade, the narrative discipline is unusual, and the cross-stage fidelity auditing is better than anything a two-person team is expected to produce. But there is one *structural* defect — not cosmetic — that a sharp judge can find, and four smaller breaks that survived the freeze because each stage audited its own inputs rather than its own outputs.

**Biggest remaining weakness: the Cost axis is passive while the other two act.**

The central claim is *three reads of one graph*. Performance produces a gate. Responsibility produces a gate. Cost produces **a number on a screen**. That asymmetry breaks the symmetry that makes the claim beautiful — and it breaks it in the exact direction the deck attacks: "a dashboard can tell you the trace cost ₹8." Right now, on screen, the cost read *is* the dashboard. Worse, it is also logically unsound on this trace (see §2.1).

**Strongest asset, protect at all costs: the entitlement catch rendered inside the running trace.**

Scored 50/50 at Stage 2, structurally impossible for any output-only competitor, deterministic, and the only mechanism in the system that catches a real, expensive, *nameable* enterprise incident. If a rendering constraint forces something out of Slide 1 or Beat 3, everything else goes first. Second-protected: the first-image/last-image loop — same transcript card, one field changed. That is the single most memorable structural decision in the deliverable and no other team will have anything like it.

---

## 2. Ranked Critical Weaknesses

### 2.1 — The Cost read has no actuator, and is logically invalid on this trace

**Diagnosis.** Two defects, same location.

*First:* Stage 2 defines dead compute as steps grounding zero claims **in the accepted answer**, with the explicit FP control that it counts only when the answer *was* accepted — exploration that ends in correct abstention is legitimate spend. On the running trace the answer is **held and escalated**. There is no accepted answer. Beat 3 says "four of nine steps produced nothing the answer used" about an answer the system just refused. By the architecture's own rule, that number is not computable here.

*Second:* Stage 4 Part D explicitly assigns the stop-sequence injection to the video — *"Out-of-band stop-sequence injection (billing ends mid-generation) → Video · cost beat, one line."* Stage 5 never delivers that line. This is a documented handoff break, not a judgment call. Stage 2 scored that mechanism 46/50 and called it "the only real-time cost actuator in any proposal." It is currently in the deliverable nowhere.

**Why it still matters.** The judge does not need to catch the accepted-answer subtlety for this to cost you. They will feel the asymmetry pre-consciously: two axes stop something, one axis counts something. And the one that counts is the one the deck spent Slide 3 mocking other people for.

**Surgical fix.** Restore the loop kill to Beat 3 and reframe the cost read as *in-flight yield*, not post-hoc accounting. This fixes both defects with one edit, because in-flight yield needs no accepted answer.

> **Before:** "Cost — walk the graph backward. Four of nine steps produced nothing the answer used."
>
> **After:** "Cost — walk the graph backward. Four of nine steps grounded nothing, and the plan never advanced. So we injected a stop sequence. Billing ended mid-generation."

+11 words. Beat 3 goes 110 → 121 words (121 wpm), still the slowest beat in the video. Visual: at 2:00–2:10 the backward arrow greys four step nodes, then a billing counter in the corner freezes mid-increment. One frame. Two seconds.

Now all three reads *act*: hold, block, kill. The claim becomes symmetric, and it is true.

---

### 2.2 — Bias and safety are invisible in the deliverables. Direct rubric exposure.

**Diagnosis.** The brief defines responsibility as *"biased, unsafe, or leaking data."* Slide 1's RESPONSIBILITY leader line says `span the caller may not read (ACL)`. Beat 3 says "a span this caller was never entitled to read." That is leakage — one of three. Bias and safety appear nowhere in either deliverable. Stage 3's own appendix warned that dropping bias "scores against the rubric," then routed it to Q&A. **Round 1 is a deck and a video. There is no Q&A.**

**Why it still matters.** You have optimised toward the single strongest mechanism and let it stand for the whole dimension. That is correct architecture and incorrect scoring. A judge with a rubric sheet ticks what they can see.

**Surgical fix.** One quiet line in Slide 2's bottom strip — paid for by cutting the actuator chips (§2.4):

> `Bias — counterfactual flip rate, route-level, CI excludes zero, async lane.  Safety — typed action interlocks: tool × args × irreversibility.`

Thirteen words, in the strip that already exists, both mechanisms frozen at Stage 2 (#30, #31). Nothing invented. Net word count on the slide goes **down**. A judge scoring against the three sub-dimensions can now tick all three, and the register stays engineering — flip rate with a CI, not "fairness."

---

### 2.3 — Stage 3 still contains the "blocks a payment" error that every later stage fixed

**Diagnosis.** Stage 4 §A3 diagnosed this precisely and Stage 5 enforced it as Rule 6. Neither patched the source. Stage 3 still reads:

- Line 186 (differentiation table): *"the identical verdict annotates a draft and **blocks** a payment."*
- Line 229 (narrative spine, 2:15–2:45): *"The identical unproven claim annotates a draft, gets stripped from a read-only answer, and **blocks** a payment."*

**Why it still matters.** Stage 3 is the document a human rehearses from. It is the narrative spine — the one you re-read the night before recording. The error is preserved in the exact beat where the matrix appears on screen saying *Escalate*. One rehearsal from Stage 3 and the presenter says "blocks" over a grid that says otherwise.

**Fix.** Two-word patch, zero risk, zero cost: **blocks → holds**, both locations. Do it before anything else in this list.

---

### 2.4 — Density: Slide 1 is ~15 readable elements against an 8-second budget; Beat 4 is five visual states in 30 seconds

**Diagnosis.** Slide 1 carries kicker, headline, dashed boundary + label, MODEL box, span row with monospace tags, six claim nodes, the `default state: UNSUPPORTED` label, gate glyph, ACTION node, three leader lines with three labels, three supporting text lines, and a footer. The 8-second absorption target is asserted, never measured. It is not achievable at that element count.

The three supporting lines are the correct cut, because **all three restate what the graph already shows.** Line 1 duplicates the dashed boundary and the span tags. Line 2 duplicates the `UNSUPPORTED` label and the visible bindings. Line 3 is the only one that states something the graph *cannot* say about itself.

Beat 4 runs matrix → actuator chips → JSON packet → split frame → report block. Six seconds per state, in the beat where the judge is forming their over-blocking verdict. The chip row is the weakest state: it is text on screen restating the three outcomes the voice is speaking at that exact moment.

**Fix.**

- **Slide 1:** cut supporting lines 1 and 2. Keep line 3 only — *"Three dimensions, one graph — unbound claim · unentitled span · unused step."* It is the thesis of the visual, not a caption on it.
- **Slide 2:** cut the four actuator chips. Retain one line, the only actuator whose meaning a judge would get wrong from the English word alone: `EDIT — strip or re-ground the named span. Never a rewrite.` Block, Escalate and Pass explain themselves; Edit does not, and Edit is the differentiated one. This is also what pays for §2.2.
- **Beat 4:** cut the chip state. Extend the JSON evidence packet to 2:23–2:31. Four states, eight seconds each.

---

### 2.5 — The FNR block still contains the system's only unfalsifiable number — and one that contradicts the architecture

**Diagnosis.** Two problems in one block.

*First:* `94.2%` and `5.8% ± 1.1` are specified to one decimal with a confidence interval. That is the typography of measurement. The `illustrative format` label underneath is read second, if at all. Stage 4 defends the label correctly, but the position is logically weak: you make a claim, then annotate that it is not a claim. On the slide whose entire argument is *we don't make claims we can't back*, that is the one place the argument leaks.

*Second, and harder:* the block states `gate latency (p95) 41 ms`. Stage 2's defended target is **"≤40ms p50 and ≤200ms p95."** The deck quotes a p95 five times better than the architecture claims. In a Q&A that is a dead-on-contact contradiction with your own spec.

**Fix.** Convert values to typed placeholders. The schema is the claim; the values are Round 2's.

```
route                      finance/refund-agent
gate latency (p50 / p95)   <measured> / <measured>
ungrounded claims caught   <measured>
missed  (FNR)              <measured>  ± <CI>
entitlement violations     100%  (deterministic — property, not measurement)
audit sample               100% of blocks + escalations · 3% of passes
```

The one retained hard number is the one that *is* knowable at design time, and the parenthetical says why. The p95 contradiction disappears. And the block stops asserting anything it cannot defend, which is the actual credibility move — right now the slide performs honesty; this version *is* honest.

**Honest counter-argument:** an empty-looking report reads as a mockup to a non-technical judge. I still recommend it. The line beneath already promises measured values, the deterministic row proves you know which fields are knowable, and a monospace schema with typed placeholders reads as engineering to exactly the audience you are trying to reach. But this is the one item on the list where a reasonable person could rule the other way — take it or leave it as a unit, and if you leave it, you **must** still fix `41 ms`.

---

## 3. Conceptual Purity Check

**The core is pure. It has not over-engineered.** This is the finding I expected to reverse and could not. Count what actually reaches the 3 slides + 3 minutes: one graph, context-assembly capture, inverted burden, entitlement, blast-radius matrix, surgical edit, evidence packet, action-gate/hold-back, published FNR. Nine elements, each earning its place, none explained twice. Stage 4's Part D demotion table is correct and should not be touched.

Two things are demoted *correctly and invisibly*, and should stay that way:

- **Assertion strength** (categorical vs hedged) appears only as matrix column labels and is never explained. Correct. The column reads fine without it; explaining it costs fifteen seconds and buys nothing.
- **Worst-claim-governs** appears nowhere. Correct. One red claim gating the action demonstrates it without naming it.

**One thing is now demoted too far and should come partly back:** the stop-sequence injection (§2.1). It is not a secondary mechanism — it is the only actuator on one of the three mandated axes.

**Nothing else should move to Q&A.** The lanes, the seven roles, the Evidence Ledger, speculative gating, shadow mode, circuit breakers, proof cache, bounded proof depth — all correctly absent. Do not let a reviewer talk you into adding a single one of them "for depth." Depth is already demonstrated by the trace going all the way to the bottom.

---

## 4. Narrative & Emotional Power Audit

### Is the Cost axis as sharp as Performance and Responsibility?

**No — it is the weakest of the three, and it is the only one that is weak.** Performance has an image (a claim that stays red while five turn). Responsibility has an image (an ACL tag mismatching a caller chip) and a *victim* (the wrong employee reads the HR file). Cost has a counter. After the §2.1 fix it gains an actuator and a moment — a billing meter freezing mid-increment is the single most visceral image available to the cost axis, and it is the only one of the three where money visibly *stops*. Fix it and the three reads are finally peers.

### Is the closing circuit perfect?

Structurally, yes — and it is the best thing in the system. Hook line and close are the same claim negated then resolved; first image and last image are the same object with one field different; Slide 1 footer and Slide 3 closer carry the same loop across the deck. Protect all of it.

One line-level slip. The hook indicts **the system**: *"The system didn't fail."* The close indicts **the model**: *"That model never had to prove anything."* That quietly reintroduces the frame the entire thesis rejects — that the model is the problem. It is a system property. And the hook's operative verb is *asked*; the close paraphrases it instead of echoing it.

> **Before:** "That model never had to prove anything."
> **After:** "Nobody ever asked that system to prove anything."

Seven words either way. Keeps *asked* as the exact echo, keeps the locus of blame on the system, and the pivot from *nobody asked* to *nothing acts* is tighter than *never had to* → *nothing acts*.

### Residual soft or defensive lines

One, and it is the opening line of Beat 4 — the worst possible place for a defensive posture.

> **Before:** "It doesn't refuse everything."
> **After:** "Proof scales with consequence."

Four words for four. The original opens the beat with a negation of your own strongest verb — it answers an accusation nobody has made out loud yet, which is what defensiveness sounds like. The replacement states the principle positively, *is* the matrix in four words, and pre-empts the objection faster because "scales" immediately implies "not always block." The three staccato outcomes then demonstrate it instead of defending it.

One minor item I recommend **leaving alone**: *"A human resolves it in seconds."* Stage 2's target is under twenty seconds; "in seconds" states a design target as fact. Technically a violation of your own numbers rule. But it describes your own design, the packet is on screen making it self-evident, and hedging it costs five words in a beat with none to spare. Leave it.

### Line-level upgrade — one addition

Stage 3 element #32 scored **50/50** — *"They publish precision — the rate at which they bother the user. We publish the rate at which we missed"* — and appears in neither the deck nor the video. A perfect-scoring element is unused. The video's compressed version ("Not what we caught — what we missed") is tighter in the mouth and should stay. But the deck has room, and the comparative is what turns a disclosure into a kill.

> **Add above the Slide 3 report block, small:**
> `Everyone in this category publishes precision. This is the other number.`

Eleven words. Converts the block from *here is our data* to *here is the number nobody else prints*.

---

## 5. Deck + Video Consistency & Visual Discipline

**Breaks found:**

| # | Break | Severity |
|---|---|---|
| 1 | Stage 4 Part D promises the stop-sequence line in the video's cost beat; Stage 5 does not contain it | **High** — §2.1 |
| 2 | Stage 3 lines 186 and 229 still say "blocks a payment" | **High** — §2.3 |
| 3 | `gate latency (p95) 41 ms` on Slide 3 vs `≤200ms p95` in the frozen architecture | **High** — §2.5 |
| 4 | Stage 5 renders **14 span nodes with monospace tags**; Slide 1 specifies no span count. The two graphs will not look like the same object | Medium |
| 5 | Beat 4 carries a JSON operator terminal that has no counterpart anywhere in the deck | Low — video may exceed the deck; but it contributes to the five-state crowding in §2.4 |

**Break 4 needs a production rule that no document currently states: separate *stated* counts from *rendered* counts.**

Fourteen tagged spans, nine step nodes and six claim nodes is 29 objects animating in ten seconds. On a laptop at video bitrate that is mush, and it will not match a static slide. Fix:

- **Spans render as six nodes plus a `14` counter chip.** The number stays a fact of the trace; the row stays legible.
- **Steps render as nine small ticks with no tags** — they only ever need to grey out four.
- **Claims render as all six.** They are the only layer where every individual node carries meaning.
- **Only three span tags are ever fully legible** — the one that grounds a claim, the one with the ACL mismatch, and one neutral. The rest are typographic texture.

Apply the same counts to Slide 1 so the deck and the video are literally the same drawing.

**Visual discipline elsewhere is already excellent and should not be touched.** The two-colour rule, the no-stock-icon law, the gradient-legible-at-three-metres test, "the closing line is the panel," leader lines never becoming panels — all correct, all rare, keep every one.

---

## 6. Highest-Leverage Modification Options

**Option 1 — Restore the cost actuator to Beat 3. (Ranked first.)**
*Change:* the twelve-word replacement in §2.1, plus a two-second billing-counter freeze at 2:00–2:10.
*Impact:* highest in the system. Makes all three reads act, repairs the accepted-answer logic hole, closes the Stage 4 → Stage 5 handoff break, and hands the cost axis its only visceral image.
*Risk:* low-moderate. Beat 3 goes to 121 wpm — still the slowest beat, but the animation now has to carry four states in sixty seconds instead of three. Rehearse it twice.

**Option 2 — Patch Stage 3's two "blocks" instances to "holds."**
*Change:* two words.
*Impact:* prevents the presenter contradicting the grid on camera, from the document they will actually rehearse from.
*Risk:* **zero.** Do this first regardless of what else you accept.

**Option 3 — Trade Slide 2's four actuator chips for one Edit line plus the bias/safety line.**
*Change:* §2.2 and §2.4 executed as a single swap.
*Impact:* closes the rubric exposure on responsibility, reduces net word count on the slide, and retains the one actuator definition a judge would otherwise misread.
*Risk:* low. The only loss is the escalate-packet contents, which are already spoken in Beat 4 and rendered as JSON on screen — currently stated three times.

**Option 4 — Density cuts: Slide 1 supporting lines 1 and 2, Beat 4's chip state.**
*Change:* delete three items.
*Impact:* moves Slide 1 within plausible reach of its own 8-second claim; gives Beat 4 four states at eight seconds instead of five at six.
*Risk:* low. Both cuts remove pure duplication. The only residual risk is that a judge skimming Slide 1 does not construct "three reads of one graph" unaided — which is why line 3 stays.

**Option 5 — Convert the FNR block to typed placeholders. (Ranked last; highest variance.)**
*Change:* §2.5.
*Impact:* removes the last unfalsifiable element in the system and resolves the p95 contradiction.
*Risk:* moderate — a non-technical judge may read empty fields as thin. This is the only item where I would accept a decision against my recommendation. **But if you decline it, you must still change `41 ms` to a p50, or change the label to `(p50)`.** The contradiction with your own architecture is not optional.

---

## 7. Final Recommendation

**Reopen two stages. Patch one. Leave one sealed.**

- **Stage 2 — stays sealed.** The architecture is correct throughout. Every defect found above is a case of the deliverables *under-quoting* the architecture, never contradicting it. Do not touch it.
- **Stage 3 — patch, do not reopen.** Two words. It is a correction of an error Stage 4 already diagnosed, not a redesign.
- **Stage 4 — reopen narrowly.** Slide 1 supporting lines; Slide 2 bottom strip; Slide 3 report block and the comparative line. Nothing else.
- **Stage 5 — reopen narrowly.** Beat 3 cost line; Beat 4 opening line and chip state; the closer's seven words. Nothing else.

**Priority order:**

1. **Stage 3: blocks → holds**, both locations. Two words, zero risk, and it is the doc you will rehearse from.
2. **Beat 3 cost actuator.** The single highest-leverage change in the system.
3. **Slide 3: fix `41 ms`** — either as part of the placeholder conversion or standalone. This is a live Q&A landmine.
4. **Slide 2 swap:** actuator chips out, Edit line + bias/safety line in.
5. **Beat 4 opener:** "It doesn't refuse everything" → "Proof scales with consequence."
6. **Closer:** "That model never had to" → "Nobody ever asked that system to."
7. **Density cuts:** Slide 1 lines 1–2, Beat 4 chip state.
8. **Node-count production rule** applied to both the deck and the video graph.
9. **Slide 3 comparative line** above the report block.

Every item above is a drop-in replacement — none requires rewriting a section, and none introduces a mechanism that is not already frozen in Stage 2.

**One honest thing to end on.** Items 1–9 take this to roughly **9.8**. The remaining 0.2 is not reachable by editing text, and any reviewer who tells you otherwise is selling you another revision pass. It lives entirely in execution: whether the sixth claim visibly *fails to bind* before the voice says "one doesn't"; whether the ACL mismatch is legible at 1:56 on a laptop screen; whether the narrator holds the two-second gap before the last line instead of filling it. Stage 5 already told you which beats to rehearse hardest and it was right. Stop editing after item 9 and go render the entitlement catch until it reads in one frame. That single shot is worth more than every remaining word change combined.