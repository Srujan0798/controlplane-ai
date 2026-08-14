# Final Elevation Audit — ControlPlane.ai

Honest score first. The system is at **9.4/10** by my read, sitting in the band you named. The architecture is the cleanest object in the chain; the video is the most disciplined; the deck is the right compression of the architecture. The remaining gap is *small but specific*, and most of it lives in the seams between stages, not inside any one stage. I have one disagreement with you: I cannot push this design to a true 10/10 from text alone. The ceiling for the *design* is 9.7–9.8 with the surgical moves below. The last 0.2 is execution: slide build, speaker rehearsal, edit pacing. That is the speaker's job, not the architect's, and pretending otherwise would be the dishonest move. Everything below is a real move that closes part of the gap.

---

## 1. Overall Diagnosis

**True strength: 9.4 / 10.** The architecture is genuine, the video is genuinely one of the strongest things I have seen in this category, and the deck compresses both without losing the spine.

**The single biggest remaining weakness: a seam, not a substance.** The close line in **Stage 3 §5** is still the *old* close — *"Now it does — and when it can't, the money doesn't move."* — while the frozen video close (Stage 5 Part B Beat 5) and the frozen deck closer (Stage 4 Slide 3) are *"Now nothing acts until it can prove it should."* This is the most important line in the entire system and it is drifting between two frozen documents. A judge who reads Stage 3 and watches the video will hear the line change shape. The fix is a one-line edit, but the severity is maximum because the close is the line judges quote in their notes.

**The single strongest asset that must be protected at all costs: the unifying message — one graph, three reads, with provenance captured at context assembly.** This appears seven times across the system and it is the only thing in the system that the entire category lacks. Every other line, slide, and beat is a vehicle for this one. If anything gets cut under time pressure, it is not this.

---

## 2. Ranked Critical Weaknesses

These are the five closable gaps, in order of impact on Round 1. Anything not on this list is either already at 10 or below the threshold of judges' notice.

### #1 — Close line drift between Stage 3 and the frozen close
- **Diagnosis:** Stage 3 §5 still reads *"That model never had to prove anything. Now it does — and when it can't, the money doesn't move."* The frozen close — endorsed by the Stage 5 audit, written into the video, set on Slide 3 — is *"That model never had to prove anything. Now nothing acts until it can prove it should."*
- **Why it still matters at this stage:** the close is the single most-quoted line in any pitch. A judge who reads Stage 3 and watches the video will notice that the rule-form close (*"nothing acts until…"*) is universal and the consequence-form close (*"the money doesn't move"*) is trace-specific. The rule-form is strictly stronger. Drift here is also a flag that the system was not re-frozen after Stage 5.
- **Surgical fix:** replace the second sentence of the §5 close with the frozen line. Two-line edit, no other change to Stage 3.

### #2 — Positioning statement is 70 seconds for a 30-second slot, and the compression loses the strongest moment
- **Diagnosis:** the full Stage 3 positioning is 180 words ≈ 70 seconds of speech. The brief asks for 25–30 seconds. Stage 3's own "spoken 30-second cut" works but requires the speaker to read at ~140 wpm for the full 30 seconds, with the abstract middle clause ("refuses to let an unproven claim cross into an action") doing all the load-bearing work. The stronger "draft vs payment" example is dropped from the compression.
- **Why it still matters:** the first 30 seconds of the video is either the positioning or a thesis-first reframe. Right now the deck and video open on the *transaction*, not the positioning statement, which is the correct call. But the positioning statement still lives on Slide 1 as a written artifact and on Stage 3 as the canonical reference. A judge who reads it will feel the bloat.
- **Surgical fix:** rewrite the canonical positioning as a single 50-word paragraph that keeps the *bad paragraph / executed transaction* line as the closer, with the *draft vs payment* example as the penultimate clause. Word budget: 50. Word count: ~20s of speech, leaves 10s of silence before the next beat. The "admission-control layer" noun is kept; "we sit on top of yours" stays as a slide footer if needed.

### #3 — The "ship test" is buried in §7 of Stage 3
- **Diagnosis:** the most important evaluation rubric in the document — *"If a judge could summarise the deck as 'it watches AI outputs and flags problems,' the narrative has failed regardless of the architecture underneath"* — is the second-to-last paragraph of §7. It is the single sharpest filter for whether the system works, and it lives at the bottom of the document.
- **Why it still matters:** the ship test is what you run the system against on every future edit. If a future round adds a line that fails the ship test, the line is a problem. Currently the team has to scroll to page 7 of Stage 3 to find it.
- **Surgical fix:** move the ship test to a header block before §1, as the *evaluation rubric* for the entire system. Two-minute re-order, no other content change.

### #4 — "Set-membership test" in the Stage 3 Single Sharp Insight is technical
- **Diagnosis:** §1 says *"…turns hallucination detection from a judgment call into a set-membership test."* The phrase is precise and Stage 3 scores it 46, but it is the kind of phrase a non-ML judge may not parse in real time. The rest of the sentence carries the meaning without it.
- **Why it still matters:** the Single Sharp Insight is the load-bearing sentence of the entire positioning. Every other sentence in the system is downstream of it. If a judge re-reads it twice because of one phrase, the sentence is doing less work than it should.
- **Surgical fix:** drop "into a set-membership test." The sentence still says: *"turns oversight from scoring text into authorizing actions."* The dropped phrase is implied by the next clause. Five-character edit, no other change.

### #5 — Beat 4 of the video has a redundant sentence
- **Diagnosis:** Beat 4 ends with *"And we publish our own miss rate. Per route. Not what we caught — what we missed."* The second sentence is a poetic restatement of the first. The first sentence carries the credibility claim; the second is a flourish that costs four seconds and weakens the close of the beat.
- **Why it still matters:** Beat 4 is the credibility beat. A flourish on top of a clean declarative line reads as defensiveness. The line should land once, not twice.
- **Surgical fix:** cut *"Not what we caught — what we missed."* The pause after *"Per route."* is now longer and the beat ends cleanly. Five-word cut.

---

## 3. Conceptual Purity Check

**The core is pure.** One graph, three reads, captured at context assembly, default UNSUPPORTED, blast-radius × verdict matrix, hard gate on actions, published miss rate. Nothing on the slide or in the video is invented. The eight roles from Stage 2 are correctly absent from the deck and video and correctly noted as Q&A material in Stage 4 Part D.

**Secondary mechanisms I checked for over-engineering** — and all are correctly demoted:
- Dead compute, four-of-nine grounded nothing → kept on slide as a leader line label (Slide 1) and spoken in Beat 3 of the video. The 14-spans / 6-claims / 4-of-9 numbers are spoken-or-shown, not both. Correct.
- Hold-back buffer → spoken in Beat 4 of the video only. Not on the slide. Correct.
- Out-of-band stop-sequence injection → Q&A only. Correct.
- Counterfactual invariance for bias → Q&A only. Correct.
- Three lanes, seven roles, the Evidence Ledger → Q&A only. Correct.
- Speculative *verification* (not speculative *release*) → Q&A only. The distinction is the entire reason the latency argument holds, but the *latency* claim is on the slide; the *mechanism* is Q&A. Correct.
- Circuit breaker, autonomy downgrade → Q&A only. Correct.
- Shadow mode as default deployment → Q&A only. Correct.

**No mechanism on the slide or in the video is over-engineered for the format.** The system is as pure as the format allows. If the team is asked to extend the deck in Round 2, the right place to add is a fourth slide showing the Evidence Ledger format (typed, hash-chained, not free text), because that is the one architectural artifact that survives from Stage 2 to a second round and is currently invisible.

---

## 4. Narrative & Emotional Power Audit

**Cost axis.** As sharp as the other two. The video presents it as *"walk the graph backward. Four of nine steps produced nothing the answer used."* The deck presents it as the COST leader line on Slide 1 (*"steps that ground nothing"*). The Stage 2 mechanism is the headline cost metric in the entire category: *the fraction of spend that produced no evidence used in the answer.* No competitor has this number because no competitor has the graph. **Leave alone.**

**Responsibility axis.** Strongest axis in the system, by a small margin. The video line *"a span this caller was never entitled to read. No classifier. Access rights."* is a killshot on the LLM-as-judge frame. The architecture's Rule 28 (entitlement check) is the highest-scored mechanism across all of Stage 2 (50/50). The slide 1 RESPONSIBILITY leader line (*"span the caller may not read (ACL)"*) is a tight 6-word version of the same idea. **Leave alone.**

**Closing circuit.** The current circuit in the video and the deck is:
- Hook (Beat 1, Slide 1 footer): *"The system didn't fail. It was never asked to prove anything."*
- Close (Beat 5, Slide 3): *"That model never had to prove anything. Now nothing acts until it can prove it should."*

This is a perfect negation → resolution. The hook indicts; the close rules. **This is the strongest single asset in the system after the graph itself.** Stage 3 §5's old line must be edited to match.

**Residual soft or defensive lines.** Two I found:

| Location | Line | Why it is soft |
|---|---|---|
| Stage 3 §5 (1:15–2:15) | *"The system didn't fail. It was never asked to prove anything."* (kept as a line in the mechanism beat) | This is the hook line. Using it twice in the same document, once as hook and once as mechanism-beat-closer, weakens both. The mechanism beat has a stronger closer already (*"Everywhere else, that's three products. Here it's three questions on one graph."*). |
| Stage 3 §5 (2:15–2:45) | *"We publish our own miss rate. Per route."* | Already covered. This is fine in the video, but Stage 3 §5 also has the full sentence with a second clause *"They publish precision — the rate at which they bother the user. We publish the rate at which we missed, per route."* — the long version is better in print but is the same claim twice. |

**Specific line-level upgrades** (in addition to the §5 close fix in weakness #1):

- Stage 3 §5 (1:15–2:15), drop the residual hook-line use. The beat already has *"Everywhere else, that's three products. Here it's three questions on one graph."* That is the closer. Remove *"The system didn't fail. It was never asked to prove anything."* from the mechanism beat. The hook line is the hook line. It does not also need to live here.
- Stage 3 §5 (2:15–2:45), in the printed doc, keep the long version (*"They publish precision…"*). In the spoken 30s cut, keep the short one (*"We publish our own miss rate, per route."*). The video uses the short form. Stage 3 can hold the long form as a written artifact.

---

## 5. Deck + Video Consistency & Visual Discipline

**The deck and the video are the same artifact at two frame rates.** This is the right call and the Stage 5 doc states it explicitly. The transcript-card persistence is the strongest single visual decision in the entire system, and it is video-only because the deck stands alone.

**Three real risks left:**

1. **Slide 3 strikethrough rendering.** The refuse list uses struck-through text (*~~"We eliminate hallucinations."~~*). Strikethrough in Keynote, PowerPoint and Google Slides is *unreliable* — it depends on the font, the version, and whether the slide tool respects the markup. If the strikethrough fails to render in front of the judges, the slide loses its cleanest visual.
   - **Fix:** render the refuse list as a two-line "claim / reality" format. The struck-through claim sits in normal weight above a smaller, grey correction line. A small redacted bar (a hairline with the word "refused" set in tiny caps) replaces the strikethrough. Renders identically across every tool.

2. **Slide 1 element count is close to the 8-second ceiling.** The spec includes: chain (4 nodes), 14 SPAN nodes (or 3–4 representative ones), MODEL box, dashed boundary, 6 CLAIM nodes (5 bound, 1 unbound red), gate glyph, 3 leader lines, 3 labels, kicker, headline, 3 supporting lines, footer. In a well-built deck the eye lands on the chain, the red claim, and the three leader lines first; everything else recedes. If the slide designer draws all 14 span tags with full monospace text, the slide will feel busy.
   - **Fix:** in the slide build spec, limit the visible SPANs to 4 representative ones, each carrying a short tag. State the *"14 spans, each with source · ACL · hash"* in the speaker notes, not on the slide. The 14 is a video number; the slide is the diagram.

3. **Slide 3 headline vs body tension.** Headline says *"the number we publish."* Body says *"illustrative format — Round 2 fills this with measured values."* A judge who reads the headline first and the body second will feel a small contradiction.
   - **Fix:** the headline becomes *"The claims we refuse to make — and the format we publish."* This is closer to the truth (we publish the *format*, not a number), and it makes the body's "illustrative format" qualifier read as a confirmation rather than a correction.

**Three things I checked and left alone:**

- Slide 2 matrix fidelity. The 4×4 is transcribed exactly from Stage 2 with the column-2 bracket annotation. The diagonal Block→Pass gradient does the over-blocking argument without text. Correct.
- Slide 2 actuator strip. "EDIT — strip or re-ground the named span, never a rewrite" reads as the architecture specification of the EDIT actuator, not as a re-import. Correct.
- Slide 1 footer. "The system didn't fail. It was never asked to prove anything." is the hook line as a slide footer. The slide and the video share the load. Correct.

---

## 6. Highest-Leverage Modification Options

Ranked by impact × ease.

### Option 1 — Fix the Stage 3 §5 close line (and the residual hook-line use)
- **What:** one-line edit to the close (`"when it can't, the money doesn't move"` → `"nothing acts until it can prove it should"`), and a parallel cut in §5 (1:15–2:15) to drop the duplicated hook line.
- **Expected impact:** highest. The close is the line judges quote. The duplicate hook line weakens the strongest beat of the video on paper.
- **Risk of making it worse:** zero. Both edits move toward the frozen close, which is already on the deck and in the video.

### Option 2 — Rewrite the Stage 3 positioning to 50 words
- **What:** replace the 180-word canonical positioning with a 50-word version. The "admission-control layer" noun is kept. The draft-vs-payment example is the penultimate clause. The bad-paragraph / executed-transaction line is the closer.
- **Expected impact:** high for any judge who reads Stage 3 in full. The current 180-word version reads as a position paper; the 50-word version reads as a positioning statement.
- **Risk:** low. The draft-vs-payment line is the strongest concrete moment in the system; the risk of dropping it is greater than the risk of cutting the abstract middle.

### Option 3 — Promote the ship test to a header block in Stage 3
- **What:** re-order Stage 3 so the ship test is the first thing after the title, before §1. Keep everything else.
- **Expected impact:** medium. The ship test is the evaluation rubric for every future edit; making it the first thing the team reads is process discipline, not narrative change.
- **Risk:** zero.

### Option 4 — Cut Beat 4's *"Not what we caught — what we missed"* from the video
- **What:** five-word cut in the spoken script. The pause after *"Per route."* is now the closer of the beat.
- **Expected impact:** low-medium. The line reads as a flourish on top of a clean declarative. Cutting it sharpens the credibility beat.
- **Risk:** zero.

### Option 5 — Render Slide 3 refuse list as claim/reality two-line format, not strikethrough
- **What:** slide design spec change. The struck-through claim sits in normal weight above a smaller grey correction line. A small redacted bar replaces the strikethrough.
- **Expected impact:** medium. Eliminates a real cross-tool rendering risk on a slide that carries the credibility claim.
- **Risk:** low if the redacted bar is small and consistent with the rest of the slide's typographic restraint.

---

## 7. Final Recommendation

**Do not reopen any stage.** The architecture, narrative, deck, and video are all frozen, and reopening them for a 0.5-point gain is the most common way a strong Round-1 system loses its discipline. The system is already at the point where the marginal cost of any structural change is higher than the marginal gain.

**Priority order if the goal is 9.7–9.8 / 10:**

1. **Fix the Stage 3 §5 close line** (and remove the residual hook-line use in §5 1:15–2:15). This is the highest-leverage move in the system.
2. **Rewrite the Stage 3 positioning to 50 words.** Keeps the strongest moment, drops the bloat.
3. **Cut the redundant second sentence from Beat 4 of the video.** Five-word cut, sharpens the credibility beat.
4. **Promote the ship test to a header block in Stage 3.** Process discipline, not narrative change.
5. **Render the Slide 3 refuse list as a two-line claim/reality format, not strikethrough.** Eliminates a real rendering risk.

**The remaining 0.2 to a true 10/10 is execution, not design.** It is the slide builder's job to honour the spec (limit visible spans to four, render the FNR as a terminal block, render the refuse list as a clean two-line format). It is the speaker's job to land Beat 5 at 64 wpm, hold the 2-second pause, and stop. It is the editor's job to time the transcript card return to the exact second the final word lands. None of that is in the design doc, and none of it can be fixed from here.

**What to do next, concretely:** apply the five edits above, rehearse Beats 3 and 5 of the video twice on camera, and stop. The system is at 9.4. After the five edits it will be at 9.7–9.8. The last fraction is the speaker's hands on the close and the designer's hands on the slide. The architecture is inevitable. Do not touch it.