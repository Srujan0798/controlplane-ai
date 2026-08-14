# ControlPlane.ai — Final Elevation Pass
### Seven reviews adjudicated · fixes applied to the frozen docs

**Reviews:** claude · kimi · minimax · gemini · glm · mistral · gpt (plus the team lead's own)
**Verdict:** the system was at **9.3**, not 9.5. Three genuine logical contradictions were live in the frozen documents. All are now fixed.

---

# PART A — WHAT WAS ACTUALLY BROKEN

Three defects were **logical contradictions inside the frozen artifacts**, not matters of taste. Each would have been findable by a judge reading carefully.

## A1 · The entitlement contradiction — the biggest catch of the round

**Found by GLM alone.** No other reviewer, including mine, saw it.

Beat 3 states: *"Responsibility — a span this caller was never entitled to read."*
That is an **entitlement violation**. The frozen matrix routes `R3 × entitlement violation` to **BLOCK**.
But Beat 4, Slide 2's pin, and Beat 5's final card all say the payment was **held and escalated** — which is `R3 × unsupported-categorical`.

**You cannot narrate an ACL violation and then escalate it.** Worst-claim-governs means the entitlement finding dominates and the correct outcome is Block. The trace contradicted its own matrix, on the slide where the matrix is on screen.

**GLM's proposed fix was wrong.** It downgrades the Responsibility read from a *finding* to a *check* — "does the caller hold the ACL?" That removes the only demonstration of the mechanism scored **50/50** at Stage 2, the one no output-only competitor can replicate. Curing the contradiction by deleting our best asset is not a cure.

**The fix applied instead: two pending actions, two blast radii, two actuators.**

The response carries two pending actions, and the architecture already prices them separately — *"worst claim, weighted by that claim's role in the pending action."*

| Pending action | Tier | Finding | Matrix cell | Actuator |
|---|---|---|---|---|
| Show text to the customer | **R1** user-visible | unentitled span grounds a claim in the text | R1 × entitlement | **Edit** — stripped |
| Issue the refund | **R3** irreversible | clause 7.2 has no span | R3 × unsupported-categorical | **Escalate** — held |

Both are correct simultaneously. Nothing was invented; this is the frozen matrix read properly for the first time. And it is a *better* demonstration than the original, because it shows the matrix doing something more sophisticated than a single lookup.

**Beat 4 spoken line, before → after:**

> ~~"It doesn't refuse everything. The same unproven claim: annotated on a draft. Stripped from an answer. On a payment — held, and escalated with the claim, the spans, and the verdict. A human resolves it in seconds."~~
>
> **"Proof scales with consequence. This response has two pending actions. Showing text to a customer — the unentitled span is edited out before they see it. Issuing a payment — the unproven claim holds it, escalated with the claim, the spans, and the verdict. Same response. Same matrix. Two different answers."**

The old opener (*"It doesn't refuse everything"*) was also the only defensive line in the script — it rebuts an accusation nobody has made aloud yet. Claude's replacement, *"Proof scales with consequence,"* states the principle positively and **is** the matrix in four words.

The one-claim-four-outcomes device is not lost: it lives on Slide 2 as the column-2 bracket, visually, while the voice does the two-actions story. Two channels, two arguments, no duplication.

## A2 · The cost read was not computable on this trace

**Found by Claude.** Stage 2 defines dead compute as steps grounding zero claims **in the accepted answer**, with the explicit false-positive control that it counts *only* on accepted answers — exploration ending in correct abstention is legitimate spend.

On this trace the answer is **held and escalated**. There is no accepted answer. So *"four of nine steps produced nothing the answer used"* was, by our own rule, not a computable statement.

**Claude's proposed fix was also wrong.** It restores the out-of-band stop-sequence injection to the beat. But the stop-sequence kills a *non-converging loop* — and this trace converged; it produced a complete six-claim answer. Firing the loop-killer here would mean the generation was terminated *and* completed. **GLM was right that this would be faking it:** *"do not fake a runaway loop just to show the actuator."*

**The fix applied instead** removes the acceptance dependency without inventing anything:

> ~~"Cost — walk the graph backward. Four of nine steps produced nothing the answer used."~~
>
> **"Cost — walk the graph backward. Four of nine steps grounded nothing. The meter ran on all nine."**

Kimi's second sentence. It is computable regardless of acceptance, it stings harder than the original, and it gives the Cost axis the consequence clause it was missing. *Gemini's currency version (`₹5 of an ₹8 trace`) was rejected* — an ₹8 trace beside a ₹1,84,000 refund is a scale mismatch that invites "so what?"

## A3 · The latency number contradicted the architecture — in three places

**Claude caught two. I found the third, which is worse.**

The frozen target is **≤40ms p50 and ≤200ms p95.** The Slide 3 gate report read `gate latency (p95) 41 ms` — a p95 five times better than we claim. Dead on contact in Q&A.

But the same error sits in **FINAL-ARCHITECTURE.md itself**, twice, inside the credibility line we have been protecting since Stage 2: *"we catch 94% of ungrounded claims at **40ms p95**."* The architecture contradicts its own stated target in its own headline. That is not the deck under-quoting the spec — that is the spec disagreeing with itself.

Fixed at all three sites: `40ms p95` → `40ms p50`.

## A4 · Stage 3 still carried errors every later stage had already fixed

Stage 4 diagnosed the block-vs-escalate problem. Stage 5 enforced it as Rule 6. **Neither patched the source.** Stage 3 — the document a presenter actually rehearses from — still read:

- *"the identical verdict annotates a draft and **blocks** a payment"* → now **holds**
- Close: *"Now it does — and when it can't, **the money doesn't move**"* → now the frozen close

Both flagged independently by Claude, Kimi and MiniMax. One rehearsal from Stage 3 and the presenter says "blocks" over a grid that says Escalate.

---

# PART B — THE FNR BLOCK

Three reviewers attacked it from three angles, and all three were right about different things.

- **Kimi:** the numbers read as fabricated regardless of the label; the eye hits `94.2%` before it hits `illustrative format`. *"The most dangerous line in all four documents."*
- **Claude:** the label is logically weak — you make a claim, then annotate that it is not a claim, on the slide whose whole argument is that you don't make claims you can't back.
- **MiniMax:** the *headline* is the real problem. It says "the number we publish" while the body says "illustrative format." A judge reads the headline first and feels a contradiction.

**All three fixes applied, because they are complementary:**

```
route                      finance/refund-agent
gate latency (p50 / p95)   <measured> / <measured>
ungrounded claims caught   <measured>
missed  (FNR)              <measured>  ± <CI>
entitlement violations     100%  (deterministic — property, not measurement)
audit sample               100% of blocks + escalations
                             3% of passes
```

**Slide 3 headline:** *"The claims we refuse to make — and the **format** we publish."*

The one retained hard number is the only one knowable at design time, and the parenthetical says why. The schema is now the claim; the values are Round 2's. **The slide stops performing honesty and starts being honest.**

*Honest counter-argument, from Claude:* an empty-looking report may read as a mockup to a non-technical judge. Accepted as a real risk. It is outweighed by removing the last unfalsifiable element in the system — and a monospace schema with typed placeholders reads as engineering to precisely the audience we are trying to reach.

---

# PART C — CONFLICTS ADJUDICATED

Where reviewers disagreed, and how it was ruled.

| # | Conflict | Ruling |
|---|---|---|
| 1 | **Cost fix.** Claude: restore stop-sequence. GLM: leave alone, don't fake a loop. Kimi: add "the meter ran on all nine." | **GLM on the mechanism, Kimi on the line.** The trace converged, so the loop-killer never fires; restoring it would be theatre. Kimi's clause fixes the logic hole *and* the emotional flatness at once. |
| 2 | **Entitlement contradiction.** GLM: downgrade the read to a check. | **Diagnosis accepted, fix rejected.** Two pending actions at two tiers preserves the 50/50 mechanism and resolves the contradiction. See A1. |
| 3 | **"A human resolves it in seconds."** Claude: leave it. Kimi: cut it. | **Kimi.** It is an unverifiable time promise in a script that refuses every other unverifiable claim. Claude's defence — *it's our own design target* — is the exact reasoning we rejected for 94.2%. Consistency wins. Cut entirely; the packet contents are already stated. |
| 4 | **"Not what we caught — what we missed."** Claude: keep. MiniMax: cut as a flourish. | **Claude.** *"We publish our own miss rate, per route"* alone doesn't say why that is unusual. The contrast is the entire point. Kept. |
| 5 | **Slide 1 density.** Claude: cut supporting lines 1–2. GLM: cut all three. Kimi: cut to 3 claims. | **Claude.** Lines 1 and 2 restate what the graph already shows; line 3 states what the graph *cannot* say about itself. Six claims stay — the 5:1 ratio is the "most claims pass" signal that pre-empts over-blocking before Slide 2 arrives. |
| 6 | **Beat 3 state count.** Kimi: seven states is the edge, do not add an eighth. Claude: add a billing-freeze. | **Moot** — no stop-sequence, so no eighth state. Kimi's ceiling stands as a rule. |

---

# PART D — ACCEPTED WITHOUT CONFLICT

Applied or adopted as production rules:

- **`ESCALATE (INLINE HOLD)`** on the Slide 2 actuator strip *(Gemini)* — prevents the misread that escalation files a ticket while the payment executes.
- **Two-word leader labels** on Slide 1: `Unbound Claim` · `Unentitled Span` · `Unused Step` *(Gemini)*.
- **Do not render strikethrough** *(MiniMax)* — it is unreliable across PowerPoint, Keynote and Google Slides. Render the refuse list as claim-above / correction-below with a small `refused` marker. A real production catch nobody else made.
- **Node-count production rule** *(Claude + MiniMax converging)*: render 4–6 span nodes with a `14` counter chip, nine steps as untagged ticks, all six claims. Only three span tags are ever fully legible. Apply identically to deck and video so they are literally the same drawing. 29 animated objects in ten seconds is mush at video bitrate.
- **Slide 3 left column at 40% opacity on the struck claim, full weight on the correction** *(Kimi)* — the eye must land on the correction, not the rejection.
- **0.5s separation between the four dismissals** in Beat 2 *(Gemini)*, and a hard 2s pause before *"Everyone watches the exit"* *(GLM)*.

---

# PART E — REJECTED

**GPT's review — fifth consecutive stage off-freeze, and this time it reviews a system that does not exist.** It critiques MCUT, Tier-1/Tier-2 checks, "7-day shadow mode auto-calibration," NLI entailment budgets and "Performance Watcher / Cost Watcher" roles — every one of them killed or demoted at Stage 2. It then recommends:

- *"A customer just lost ₹1,84,000 due to our AI's mistake"* — **inverts the scenario again.** The customer did not lose money; the company wrongly paid out.
- *"Show a shocked customer or angry email on Slide 1"* — violates the frozen risk correction: open on a transaction, never on a person.
- *"an AI cockpit that verifies every instruction"* — a new metaphor, and a stock one.
- *"fuse performance, cost, and **fairness**"* — the moralising register the vocabulary ban exists to prevent.
- *"we **will block**"* — contradicts the matrix.

Nothing accepted. The recommendation to drop GPT from the input set now has five stages of evidence behind it.

**Also rejected:**

- **Currency-grounding the cost read** *(Gemini)* — scale mismatch against a ₹1,84,000 refund.
- **Dropping "set-membership test"** from the Single Sharp Insight *(MiniMax)* — it is the phrase that makes the insight concrete for a technical judge, and Stage 3 is a written artifact, not a spoken one.
- **Rewriting the canonical positioning to 50 words** *(MiniMax)* — the 105-word spoken cut already solves the timing problem; the long form is correct as a written reference.

---

# PART F — WHAT CHANGED, FILE BY FILE

| File | Change |
|---|---|
| `FINAL-ARCHITECTURE.md` | `40ms p95` → `40ms p50` ×2 — the spec no longer contradicts its own latency target |
| `STAGE3-NARRATIVE.md` | "blocks a payment" → "holds a payment"; close line replaced with the frozen close ×2 |
| `STAGE4-DECK.md` | FNR block → typed placeholders; Slide 3 headline → "the format we publish" |
| `STAGE5-VIDEO.md` | Beat 3 cost line; Beat 4 rewritten for two pending actions; "resolves in seconds" cut; closer → "That system was never asked…" — script and teleprompter both |
| `SUBMISSION-PACKAGE.md` | FNR block and headline; Q&A trap D1 rewritten; checklist item updated |

**Beat 4 word count:** 62 → 68 words in 30 seconds (136 wpm). Above the 113 average, inside the 145 ceiling. Rehearse it.

---

# PART G — HONEST CEILING

Every reviewer who was honest said the same thing, and they were right: **this is now ~9.8, and the last 0.2 is not reachable by editing text.**

It lives in execution:

- whether the sixth claim visibly *fails to bind* before the voice says "one doesn't"
- whether the ACL mismatch is legible at 1:56 on a laptop screen
- whether the narrator holds the two-second gap before the last line instead of filling it

**Stop editing. Go render the entitlement catch until it reads in one frame.** That single shot is worth more than every remaining word change combined.
