### Slide 1 — The Reframe

**Kicker (small, above headline)**
> It used to be a bad paragraph. It is now an executed transaction.

**Exact Headline (12 words)**
> An AI response is a set of claims requesting permission to act.

**Primary Visual — the one graph, centre, dominant**

A single horizontal chain, left to right: **STEP → SPAN → CLAIM → ACTION.**

- A vertical dashed boundary sits between STEP and SPAN, labelled `context assembly — captured here, outside the model`. The word **MODEL** appears small and offset above the CLAIM layer, consuming spans and emitting claims — deliberately subordinate. The capture point is on the span layer, not inside the model.
- Each SPAN carries a monospace tag: `source · ACL · hash`.
- Six CLAIM nodes. Five are bound — a visible connector line runs back to a specific span. One is unbound, saturated red, annotated `clause 7.2 — no span`. A faint label under the claim row reads `default state: UNSUPPORTED`.
- The edge from the unbound claim to ACTION is severed by a gate glyph. ACTION node reads `refund ₹1,84,000`.
- Three leader lines tap the *same* graph at three different points:
  - **PERFORMANCE** → the unbound claim: `claim with no span`
  - **RESPONSIBILITY** → a span tag: `span the caller may not read (ACL)`
  - **COST** → a backward arrow along the STEP edges: `steps that ground nothing`

**Supporting text (4 lines max)**

1. Evidence captured at context assembly — outside the model. Source · ACL · hash.
2. Every claim starts UNSUPPORTED and must name the span that proves it.
3. Three dimensions, one graph — unbound claim · unentitled span · unused step.
4. Unproven claims cannot cross into an action.

*Cut line 4 first if the slide runs past 8 seconds. The severed edge already says it.*

**Footer**
> The system didn't fail. It was never asked to prove anything.

**Design notes**

The graph takes 55–60% of the slide area and is the only thing with visual weight. Exactly two colours carry meaning: bound and unbound. Everything else is neutral grey — no icons, no gradients, no product logo. The red unbound claim must be the single most saturated element on the slide and the first thing the eye finds. Span tags in monospace so they read as machine records, not design elements. Kicker and footer stay small; they bracket the visual — stakes above, indictment below — and must never compete with it. The three axis labels are thin leader lines, not boxes; the moment they become three panels, the "one graph" claim is dead.

---

### Slide 2 — The Decision System

**Exact Headline (10 words)**
> The same verdict annotates a draft and blocks a payment.

**Primary Visual — the matrix, dominant object, ≥60% of slide**

A 4×4 grid. Rows are blast radius, R3 at top so the eye lands on the strongest cell first. Columns are verdict severity, worst on the left.

| | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** irreversible / regulated | **Block** | **Escalate** | **Escalate** | **Escalate** |
| **R2** reversible write / external send | **Block** | **Edit** | **Edit** | **Escalate** |
| **R1** user-visible, read-only | **Edit** | **Edit** | Pass + annotate | Pass + annotate |
| **R0** internal draft | Pass + annotate | Pass + annotate | Pass | Pass |

One annotation only: a thin vertical bracket down **column 2**, labelled `one unproven claim — four outcomes`, with a single pin at R3 reading `clause 7.2 → escalate · ₹1,84,000 held`.

The diagonal fall from Block (top-left) to Pass (bottom-right) must be legible as a gradient at three metres. A judge who reads no words should still absorb: consequence rises, response escalates.

**Supporting elements — bottom strip, visually quiet**

Actuator row, four chips:
`BLOCK` · `EDIT — strip or re-ground the named span, never a rewrite` · `ESCALATE — ships claim + candidate spans + verdict` · `PASS + ANNOTATE`

Latency, two lines beneath:

- Hard gate on actions, not tokens. Text streams with a short hold-back.
- Deterministic checks inline; expensive checks only where blast radius pays for them — verification runs while the tool call is in flight.

**Design notes**

Four fill tints, one per actuator, and no other colour anywhere on the slide. Cell text is a single word; the `+ annotate` qualifier drops to a smaller weight. Row definitions capped at four words. No arrows, no callouts into the grid — the bracket on column 2 is the only annotation, because it is the only thing that proves the headline. The bottom strip is single-line, small type, no boxes or borders; if it starts to look like a second visual, shrink it. Circuit breakers and autonomy downgrade stay off this slide — they are spoken in the video, not drawn here.

---

### Slide 3 — Why This Is Different (and Believable)

**Exact Headline (11 words)**
> The claims we refuse to make — and the number we publish.

**Left side — what we refuse**

Each refused claim struck through in grey, correction below it in normal weight:

- ~~"We eliminate hallucinations."~~ → We don't. Ungrounded claims cannot authorize actions, and we report what we miss.
- ~~"Zero integration — drop it in."~~ → We hook context assembly. That is real work, and it is the reason this works at all.
- ~~"Zero added latency."~~ → Verification is budgeted, not free.
- ~~"99% accuracy across bias, safety and risk."~~ → One number over three failure modes is a demo artifact.

**Right side — what we publish**

A bordered monospace block, styled as terminal output, headed `per-route gate report — format`:

```
route                     finance/refund-agent
gate latency (p95)        41 ms
ungrounded claims caught  94.2%
missed  (FNR)              5.8%  ± 1.1
entitlement violations     100%  (deterministic)
audit sample              100% of blocks + escalations
                            3% of passes
```

Beneath, one small line: `illustrative format — Round 2 fills this with measured values.`

**Closing line — largest text element on the slide**
> Now nothing acts until it can prove it should.

**Design notes**

Two columns at roughly 45/40, with the closing line as a full-width band across the bottom. The closer is set larger than the headline — that is the one place typographic hierarchy is deliberately inverted, and it must be obvious. Left column runs smaller and greyer than the right; refusals are subordinate to the artifact. The report block is monospace with a hairline border and must read as terminal output, not as a designed graphic. No colour on this slide except a single accent on the FNR figure. The soberness is the argument: every other deck in the room spends its last slide on ambition, and this one spends it on error bars.

---

### Tensions Between the Frozen Narrative and Three Slides — and How They Resolve

**Three axes versus one visual.** The brief demands performance, cost and responsibility; three panels would destroy the one-graph thesis and blow the 8-second budget. Resolved by three leader-line labels on the single Slide 1 graph — nine words total. The claim that they are three reads of one graph is then demonstrated rather than asserted.

**"Blocked" versus the matrix.** The narrative says the money doesn't move, but the frozen matrix routes R3 × unsupported-categorical to **Escalate**, not Block. Never say "blocked" about the refund — say **held and escalated with the evidence packet.** It is also the better story: it demonstrates restraint at the exact moment a judge starts suspecting over-blocking.

**The refund wants to be everywhere.** Three appearances turns a trace into a mascot. Full annotation on Slide 1, one pin on Slide 2, absent from Slide 3. The video carries continuity; the deck does not need to.

**Both frozen lines land on Slide 1.** Two quotable lines compete unless they are given different jobs and different sizes — kicker for stakes, footer for indictment, graph owning everything between. Slide 3's closer then echoes the footer, and the loop closes across the deck rather than inside one slide.

**The published FNR is a format, not a measurement.** An unqualified 94.2% is precisely the claim Stage 3 refuses to make. The block is labelled as format, with measured values deferred to Round 2. Refusing to fabricate that number is the credibility move — a judge who tests it finds the honesty rather than the bluff.

**Latency is brief-mandated but cannot compete with the matrix.** It sits in Slide 2's bottom strip in small type. If a judge reads only the grid, the answer is still on the page when they ask.

**Stage 2's seven roles and three lanes do not appear anywhere.** Cut entirely. The deck's job is the decision, not the org chart of the verifier.