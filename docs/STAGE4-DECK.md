# ControlPlane.ai — Frozen Stage 4
### The 3-slide concept deck · adversarial merge of 7 proposals

**Inputs:** claude4 · kimi4 · minimax4 · gemini4 · glm4 · mistral4 · gpt4
**Constraint:** maximum 3 slides · 8 seconds of attention per slide · systems-clean language.

---

# PART A — FIDELITY AUDIT (run before scoring)

Stage 4 has a failure mode neither earlier stage had: **a slide can silently redraw a frozen artifact.** The decision matrix is the most credible object in the deck and the easiest to corrupt, because redrawing it *looks* like design work rather than architecture change.

## A1. The matrix was corrupted in five of six proposals

**The frozen Stage 2 matrix:**

| | Contradicted / entitlement | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** | Block | Escalate | Escalate | Escalate |
| **R2** | Block | Edit | Edit | Escalate |
| **R1** | Edit | Edit | Pass + annotate | Pass + annotate |
| **R0** | Pass + annotate | Pass + annotate | Pass | Pass |

| Proposal | Matrix fidelity | What went wrong |
|---|---|---|
| **claude4** | ✅ **exact** | The only proposal that reproduces the frozen matrix cell-for-cell. |
| **kimi4** | ❌ | Columns rewritten to `SUPPORTED / UNCERTAIN / UNSUPPORTED`. Invents `STREAM` as an actuator. Sets **R3 × UNSUPPORTED = BLOCK**, contradicting the frozen **Escalate**. |
| **minimax4** | ❌ | Columns rewritten to `UNSUPPORTED / WEAK / PARTIAL / SUPPORTED` — "weak" and "partial" are invented verdict tiers. Blast-radius definitions also rewritten (R0 read/self, R3 write/external). |
| **gemini4** | ❌ | Columns become `PASS / UNSUPPORTED / ACL VIOLATION / LOOP` — this puts the *three detection axes* on the severity axis, a category error. Invents four actuators: `Kill Span`, `Terminate Step`, `Kill & Dump Graph`, `Hold & Re-verify`. |
| **glm4** | ❌ | Same category error: severity axis becomes `Contradicted / Dead Compute / ACL Leakage`. Blast radius and severity are a 2-D decision surface; the three axes are *sources* of verdicts, not severity levels. |
| **mistral4** | ❌ | Columns reduced to generic `Low / Medium / High / Critical`, losing the frozen verdict vocabulary. States "**entire R3 row = BLOCK**", contradicting three of four frozen R3 cells. |
| **gpt4** | ❌ | "4 rows R0–R3; **3 columns as severity levels or actions**" — it does not know what the columns are. Wrong column count, no verdict vocabulary, and "high severity & high blast radius leads to Block" again contradicts frozen R3 × unsupported-categorical = **Escalate**. |

> **Rule for Round 2:** the matrix is a frozen artifact, not a design element. It is transcribed, never redrawn. Axis labels, column vocabulary and cell values are all load-bearing.

## A2. Three further fidelity breaks

**Invented actuators.** The frozen actuator set is **Block · Edit · Escalate · Pass**, plus autonomy downgrade and circuit breaker. `STREAM`, `Kill Span`, `Terminate Step`, `Hold & Re-verify`, `Redact & Flag` and `Kill & Dump Graph` are all new. Cut.

**Wrong latency numbers.** kimi4 states "deterministic checks <5ms." The frozen Lane 1 budget is **30–60ms p95**, with ≤40ms p50 added overall. Never quote a number the architecture doesn't hold.

**Invented vocabulary.** gpt4 introduces **"brand debt"** three times — a concept present in neither Stage 2 nor Stage 3, and pure marketing register. It also calls ControlPlane "the first true AI control plane," which is exactly the class of unfalsifiable superlative Stage 3 refuses. Cut.

**"Refuse to claim" confused with "rejected approaches."** Five proposals put *no LLM-as-judge / no composite scores / no static guardrails* on Slide 3 under the heading "what we refuse." Those are Stage 2's **rejected approaches** — things we did not build. Stage 3's **refuse-to-claim** list is about claims we decline to make *about ourselves*: eliminate hallucinations, zero integration, zero latency, one accuracy number. Only claude4 used the right list, and the right list is far stronger: every deck in the room disclaims its competitors; almost none disclaim themselves.

## A2b. The GPT pattern — a cross-stage finding

gpt4 also **answered the wrong prompt**: before reaching the slides it re-runs all seven Stage 3 sections (insight, market, positioning, differentiation, narrative spine, refusals, risk), which Stage 4 did not ask for. Its slide headlines are placeholders — Slide 2 is *"The ControlPlane Decision System"* (a label, not a statement) and Slide 3 is literally the brief's own section title. Its Slide 1 repeats the locked footer line twice on the same slide.

Across three stages the trajectory is consistent and diagnosable:

| Stage | GPT contribution | Fidelity |
|---|---|---|
| **Stage 2** | Genuinely strong — the policy-DAG 4-tuple encoding, canary deploys, auto-rollback on override spike. Several elements survived into the freeze. | clean |
| **Stage 3** | Reintroduced speculative release, ECS/MCUT, latency-triggered downgrade. **One line survived** (the CPU privilege-mode analogy). | off-freeze |
| **Stage 4** | Reintroduces Tier-1/2/3 lanes, ECS, MCUT, policy DAG, "Director agent", `ECS=0` as a block condition, and slow-check-degrades-to-flag. Invents "brand debt". **Nothing survived.** | off-freeze |

**The failure is specific, not random: GPT keeps regenerating from its own Stage 2 proposal rather than from the frozen spec.** Every mechanism it re-imports — ECS, MCUT, the policy DAG as headline, the tier ladder, speculative release — is one *it* originally proposed and that the merge demoted or killed. It is anchoring on its own earlier output.

**Recommendation for Round 2:** either drop GPT from the input set, or keep it and run its output through the fidelity check *first* and weight it last. Do not treat it as a primary input on the strength of its Stage 2 showing — that reputation is now two stages stale.

## A3. The contradiction nobody fully resolved

The frozen video close says *"when it can't prove it, the money doesn't move."* Read as **Block**, that contradicts the frozen matrix — R3 × unsupported-categorical routes to **Escalate**, not Block.

claude4 flagged this correctly in its tension notes: never say *blocked* about the refund; say **held and escalated with the evidence packet.** But it then wrote its own Slide 2 headline as *"The same verdict annotates a draft and **blocks** a payment"* — reintroducing the error it had just diagnosed.

**Resolution (applied below):** the headline becomes **"The same unproven claim annotates a draft and holds a payment."** Accurate to the matrix, still demonstrative, and it is the *better* story — it shows restraint at the exact moment a judge starts suspecting over-blocking. The video close survives unchanged: escalation holds the action, so the money genuinely does not move.

## A4. Element scoring — decisive rows

Scored 1–10 on **G**lance clarity (8s) · **V**isual dominance · **D**ifferentiation · **F**idelity · **S**ystems-audience fit.

| Element | Source | G | V | D | F | S | Σ | Verdict |
|---|---|---|---|---|---|---|---|---|
| **Single dominant graph on S1, three leader lines tapping it** | claude4 | 9 | 10 | 10 | 10 | 10 | **49** | **KEEP** |
| **Frozen matrix transcribed exactly, R3 at top** | claude4 | 9 | 10 | 9 | 10 | 10 | **48** | **KEEP** |
| **Terminal-style gate report, labelled as *format*** | claude4 | 9 | 9 | 10 | 10 | 10 | **48** | **KEEP — best artifact in six decks** |
| **Struck-through self-claims with corrections beneath** | claude4 | 9 | 8 | 10 | 10 | 10 | 47 | **KEEP** |
| **Column-2 bracket: "one unproven claim — four outcomes"** | claude4 | 9 | 8 | 10 | 10 | 9 | 46 | **KEEP — proves the headline** |
| **Two locked lines given different jobs and sizes (kicker / footer)** | claude4 | 9 | 8 | 9 | 10 | 9 | 45 | **KEEP** |
| **"No shields, locks, eyes, dashboards. If a stock icon would fit, the visual is wrong."** | minimax4 | 10 | 9 | 8 | 10 | 10 | 47 | **KEEP — design law** |
| **"No logo, no team photo, no thank-you panel. The closing line is the panel."** | minimax4 | 10 | 9 | 7 | 10 | 10 | 46 | **KEEP** |
| **Broken evidence feed makes inverted burden literal without words** | minimax4 | 9 | 9 | 9 | 10 | 9 | 46 | FOLD → the unbound red claim already is this |
| **Diagonal Block→Pass gradient legible at three metres** | claude4 | 10 | 9 | 8 | 10 | 9 | 46 | KEEP |
| Geometric gate glyph on the severed edge | kimi4 | 9 | 8 | 7 | 10 | 9 | 43 | KEEP |
| "Most calls land green–yellow. Block is rare." | minimax4 | 8 | 6 | 7 | 9 | 8 | 38 | FOLD → the gradient says it without text |
| Split-screen legacy-vs-ControlPlane on S1 | kimi4, glm4, gemini4 | 8 | 5 | 5 | 8 | 6 | 32 | **KILL** — spends 30–40% of the slide on the thing we're against, and leads from the category |
| Glowing padlock on the ACTION node | glm4, mistral4 | 8 | 6 | 3 | 8 | 3 | 28 | **KILL** — metaphor, not mechanism |
| Rejected-approaches list as S3 left column | kimi4, minimax4, gemini4, glm4, mistral4, gpt4 | 8 | 6 | 5 | 5 | 7 | 31 | **KILL** — wrong list (see A2) |
| Tier-1 ≤50ms / Tier-2 ≤2s post-emit / Tier-3 offline | gpt4 | 7 | 4 | 4 | 1 | 5 | 21 | **KILL** — Tier-2 post-emit *is* speculative release |
| ECS · MCUT · Policy DAG · "Director agent" as slide content | gpt4 | 5 | 4 | 4 | 1 | 5 | 19 | **KILL** — demoted or killed at Stage 2 |
| "Brand debt" | gpt4 | 6 | 5 | 4 | 1 | 2 | 18 | **KILL** — invented concept, marketing register |
| "The first true AI control plane" | gpt4 | 7 | 4 | 3 | 2 | 2 | 18 | **KILL** — unfalsifiable superlative |
| S2 headline "The ControlPlane Decision System" | gpt4 | 6 | 3 | 2 | 8 | 5 | 24 | **KILL** — a label, not a statement |
| "It used to be a bad paragraph" belongs only in the video | minimax4 | 7 | 6 | 6 | 3 | 7 | 29 | **KILL** — the brief locks it as a deck element |
| S3 headline "No Fluff. Just Proof." | mistral4 | 9 | 5 | 3 | 6 | 2 | 25 | **KILL** — marketing voice |
| S3 close "Stop reading what your AI generated after it acts…" | gemini4 | 6 | 5 | 4 | 7 | 3 | 25 | **KILL** — two sentences, imperative ad cadence |
| Headline "Deterministic integrity over probabilistic promises" | gemini4 | 5 | 4 | 5 | 8 | 4 | 26 | **KILL** — abstract sloganeering |
| Invented actuators (Kill Span / Terminate Step / Hold & Re-verify) | gemini4 | 6 | 5 | 4 | 2 | 5 | 22 | **KILL** |
| "Deterministic checks <5ms" | kimi4 | 8 | 5 | 6 | 2 | 6 | 27 | **KILL** — contradicts the frozen budget |

---
---

# PART B — THE FROZEN DECK

## Slide 1 — The Reframe

**Kicker** *(small, above the headline)*
> It used to be a bad paragraph. It is now an executed transaction.

**Headline**
> **An AI response is a set of claims requesting permission to act.**

**Primary visual** — the one graph, centred, 55–60% of slide area

A single left-to-right chain: **STEP → SPAN → CLAIM → ACTION.**

- A **vertical dashed boundary** sits between STEP and SPAN, labelled `context assembly — captured here, outside the model`. The word **MODEL** appears small and offset above the CLAIM layer, consuming spans and emitting claims — deliberately subordinate. The capture point is on the span layer, not inside the model.
- Each SPAN carries a monospace tag: `source · ACL · hash`.
- **Six CLAIM nodes.** Five are bound — a visible connector runs back to a specific span. One is unbound, saturated red, annotated `clause 7.2 — no span`. A faint label under the claim row reads `default state: UNSUPPORTED`.
- The edge from the unbound claim to ACTION is **severed by a gate glyph** — geometric, not a padlock. The ACTION node reads `refund ₹1,84,000`.
- **Three leader lines tap the same graph at three points** — thin lines, never boxes:
  - **PERFORMANCE** → the unbound claim: `Unbound Claim`
  - **RESPONSIBILITY** → a span tag: `Unentitled Span`
  - **COST** → a backward arrow along the STEP edge: `Unused Step`

**Supporting text — 3 lines**

1. Three dimensions, one graph.  *(single line — the graph states the rest)*

**Footer**
> The system didn't fail. It was never asked to prove anything.

**Design notes**

The graph is the only element with visual weight. Exactly **two colours carry meaning**: bound and unbound. Everything else is neutral grey — no icons, no gradients, no logo. The red unbound claim must be the most saturated element on the slide and the first thing the eye finds. Span tags in monospace so they read as machine records rather than design. Kicker and footer stay small and bracket the visual — stakes above, indictment below — and must never compete with it. **The moment the three axis labels become three panels, the "one graph" claim is dead.**

---

## Slide 2 — The Decision System

**Headline**
> **The same unproven claim annotates a draft and holds a payment.**

**Primary visual** — the matrix, dominant, ≥60% of slide

A 4×4 grid. **Rows are blast radius, R3 at top** so the eye lands on the strongest cell first. **Columns are verdict severity, worst on the left.** Transcribed exactly from the frozen architecture:

| | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** irreversible / regulated | **Block** | **Escalate** | **Escalate** | **Escalate** |
| **R2** reversible write / external send | **Block** | **Edit** | **Edit** | **Escalate** |
| **R1** user-visible, read-only | **Edit** | **Edit** | Pass + annotate | Pass + annotate |
| **R0** internal draft | Pass + annotate | Pass + annotate | Pass | Pass |

**One annotation only:** a thin vertical bracket down **column 2**, labelled `one unproven claim — four outcomes`, with a single pin at R3 reading `clause 7.2 → escalate · ₹1,84,000 held`.

The diagonal fall from Block (top-left) to Pass (bottom-right) must be **legible as a gradient at three metres.** A judge who reads no words should still absorb: *consequence rises, response escalates.* That gradient is also what answers the over-blocking objection — no text needed.

**Supporting strip** — bottom, visually quiet, single line of small type

Three quiet lines. Block and Pass explain themselves and are cut; Edit and Escalate are the two a judge would misread from the English word alone.

> `EDIT — strip or re-ground the named span, never a rewrite.`   `ESCALATE — inline hold; ships claim + spans + verdict.`
> `Bias — counterfactual flip rate, route-level, CI excludes zero.`   `Safety — typed interlocks: tool × args × irreversibility.`
> Hard gate on actions, not tokens. Text streams with a short hold-back.

**Why bias and safety appear here.** The brief defines responsibility as *"biased, unsafe, or leaking data."* The deck currently demonstrates only leakage. **Round 1 is a deck and a video — there is no Q&A round**, so anything routed to Q&A is never scored. Thirteen words in a strip that already exists closes the rubric exposure, and the register stays engineering: flip rate with a CI, not "fairness."

**Design notes**

Four fill tints, one per actuator, and no other colour on the slide. Cell text is a single word; the `+ annotate` qualifier drops to smaller weight. Row definitions capped at four words. **No arrows, no callouts into the grid** — the column-2 bracket is the only annotation, because it is the only thing that proves the headline. If the bottom strip starts to look like a second visual, shrink it. Circuit breakers, autonomy downgrade and speculative gating stay off this slide — they are spoken, not drawn.

---

## Slide 3 — Why This Is Different (and Believable)

**Headline**
> **The claims we refuse to make — and the format we publish.**

**Left side — what we refuse** *(smaller, greyer; refusals are subordinate to the artifact)*

**Do not render strikethrough.** It is unreliable across PowerPoint, Keynote and Google Slides — font- and version-dependent, and if it fails in front of the judges the slide loses its cleanest visual. Render each item as the claim in normal weight at 40% opacity, a small `refused` marker, and the correction beneath at full weight. The eye must land on the correction, not the rejection.

- ~~"We eliminate hallucinations."~~ → We don't. Ungrounded claims cannot authorise actions, and we report what we miss.
- ~~"Zero integration — drop it in."~~ → We hook context assembly. That is real work, and it is the reason this works at all.
- ~~"Zero added latency."~~ → Verification is budgeted, not free.
- ~~"99% accuracy across bias, safety and risk."~~ → One number over three failure modes is a demo artifact.

**Right side — what we publish**

A bordered monospace block styled as terminal output, headed `per-route gate report — format`:

```
route                      finance/refund-agent
gate latency (p50 / p95)   <measured> / <measured>
ungrounded claims caught   <measured>
missed  (FNR)              <measured>  ± <CI>
entitlement violations     100%  (deterministic — property, not measurement)
audit sample               100% of blocks + escalations
                             3% of passes
```

Beneath, one small line: `illustrative format — Round 2 fills this with measured values.`

> **Why that label is non-negotiable.** An unqualified 94.2% on a Round 1 concept deck is precisely the claim Stage 3 refuses to make. Labelling it a *format* and deferring the measurement is itself the credibility move: a judge who tests it finds the honesty rather than the bluff.

**Closing line** — largest text element on the slide
> **Now nothing acts until it can prove it should.**

**Design notes**

Two columns at roughly 45/40, closing line as a full-width band across the bottom. **The closer is set larger than the headline** — the one place hierarchy is deliberately inverted, and it must be obvious. No colour on this slide except a single accent on the FNR figure. The report block is monospace with a hairline border and must read as terminal output, not as a designed graphic. No logo, no team photo, no thank-you panel — **the closing line is the panel.**

The soberness is the argument: every other deck in the room spends its last slide on ambition. This one spends it on error bars.

---

# PART C — RESOLVED TENSIONS

**Three axes versus one visual.** The brief demands performance, cost and responsibility; three panels would destroy the one-graph thesis and blow the 8-second budget. Resolved with three leader-line labels on the single Slide 1 graph — nine words total. The claim that they are three reads of one graph is then *demonstrated* rather than asserted.

**"Blocked" versus the matrix.** Never say *blocked* about the refund. Say **held and escalated with the evidence packet.** See A3.

**Both locked lines land on Slide 1.** Two quotable lines compete unless given different jobs and different sizes — kicker for stakes, footer for indictment, graph owning everything between. Slide 3's closer then echoes the Slide 1 footer (*"never asked to prove anything"* → *"nothing acts until it can prove it should"*), so the loop closes across the deck rather than inside one slide. The deck therefore ends on a **resolution**, not on an indictment.

**The refund appears twice, not three times.** Full annotation on Slide 1, one pin on Slide 2, absent from Slide 3. Three appearances turns a trace into a mascot; the video carries continuity, the deck does not need to.

**Latency is brief-mandated but cannot compete with the matrix.** One line in Slide 2's bottom strip, small type. If a judge reads only the grid, the answer is still on the page when they ask.

**Stage 2's seven roles and three lanes appear nowhere.** Cut entirely. The deck's job is the decision, not the org chart of the verifier.

---

# PART C2 — PRE-FLIGHT CHECK

Run this against the built deck before it ships. Every item below was got wrong by at least one Stage 4 proposal, and three of them by a majority.

| # | Check | Why it recurs |
|---|---|---|
| 1 | **Slide 2 headline says "holds a payment", never "blocks".** It must agree with the R3 pin directly beneath it. | The frozen matrix routes R3 × unsupported-categorical to **Escalate**. "Blocks" contradicts the grid on the same slide. |
| 2 | **Matrix cells match the frozen architecture exactly.** Transcribe, never redraw. | Six of seven proposals corrupted it. Redrawing feels like design work; it is architecture. |
| 3 | **Both locked lines are present** — kicker *and* footer on Slide 1. | The "bad paragraph / executed transaction" line is the one most often dropped, because it has no obvious home. |
| 4 | **The FNR block carries the `illustrative format` label.** | An unqualified 94.2% is the exact claim Stage 3 refuses to make. |
| 5 | **The three axes are leader lines, not panels.** | The moment they become three panels, the one-graph thesis is dead. |
| 6 | **No padlock, shield, eye, dashboard or magnifying glass anywhere.** | If a stock icon would fit, the visual is wrong. |
| 7 | **Slide 3 left column is the refuse-to-*claim* list**, not the rejected-approaches list. | Five of seven confused the two. Disclaiming yourself is rarer and stronger than disclaiming competitors. |
| 8 | **No logo, no team photo, no thank-you panel.** | The closing line is the panel. |

---

# PART D — WHAT IS SPOKEN, NOT DRAWN

Everything below is frozen architecture that earns no slide real estate. It lives in the video and in Q&A.

| Mechanism | Where it lives |
|---|---|
| Dead compute measured exactly by walking the graph backward | Video 1:15–2:15 · the cost read |
| Out-of-band stop-sequence injection (billing ends mid-generation) | Video · cost beat, one line |
| Counterfactual bias replay with confidence intervals | Q&A only — *"counterfactual flip rate with a CI, route-level, async"* |
| Three lanes, seven roles, the Evidence Ledger | Q&A only |
| Speculative gating during the tool round-trip | Q&A — the answer to "how is it this fast?" |
| Circuit breaker and autonomy downgrade | Q&A — the answer to "what if it fails repeatedly?" |
| Shadow mode as default deployment | Q&A — the answer to "how would we adopt this?" |
