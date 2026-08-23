# ControlPlane.ai — Round 1 Submission Package
### Everything needed to build the deck, record the video, and survive the questions

All five stages are frozen. This file contains only what is still *unbuilt*: paste-ready slide text, the recording package, and the hostile Q&A set.

**Frozen references:** [FINAL-ARCHITECTURE.md](FINAL-ARCHITECTURE.md) · [STAGE3-NARRATIVE.md](STAGE3-NARRATIVE.md) · [STAGE4-DECK.md](STAGE4-DECK.md) · [STAGE5-VIDEO.md](STAGE5-VIDEO.md)

---

# 1 — PASTE-READY SLIDE TEXT

> **The three slides are also drawn, at full 16:9, here:**
> https://claude.ai/code/artifact/6fdbee03-ebda-4b07-a576-6f2b033be405
>
> That page is the **canonical rendering** — build against it rather than interpreting this spec, because it is the one place the graph exists as a single drawing. The video's animated version must resolve to exactly that frame.
>
> **Rendered counts are deliberately not stated counts:** six span nodes plus a `14` chip, nine untagged step ticks, all six claims, only three span tags fully legible. Fourteen tagged spans plus nine steps plus six claims is 29 objects — mush at video bitrate, and it will not match a static slide.

Copy directly. No commentary, no placeholders.

## Slide 1

**Kicker** *(small, above headline)*
```
It used to be a bad paragraph. It is now an executed transaction.
```

**Headline**
```
An AI response is a set of claims requesting permission to act.
```

**Supporting lines** *(three, small, beneath the graph)*
```
Three dimensions, one graph.
```

> **Keep the third line's specifics.** "Three dimensions, one graph" alone asserts the claim; the three fragments prove it. They are the only place on the deck where all three axes are named in words.

**Footer**
```
The system didn't fail. It was never asked to prove anything.
```

**Graph labels** *(exact strings for the designer)*
```
STEP          tool · retrieval
SPAN          source · ACL · hash
CLAIM         default state: UNSUPPORTED
ACTION        refund ₹1,84,000

boundary      context assembly — captured here, outside the model
red claim     clause 7.2 — no span
leader 1      PERFORMANCE   claim with no span
leader 2      RESPONSIBILITY   span the caller may not read
leader 3      COST   steps that ground nothing
```

## Slide 2

**Headline**
```
The same unproven claim annotates a draft and holds a payment.
```

**Matrix** *(transcribe exactly — do not redraw)*

| | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** irreversible / regulated | BLOCK | ESCALATE | ESCALATE | ESCALATE |
| **R2** reversible write / external send | BLOCK | EDIT | EDIT | ESCALATE |
| **R1** user-visible, read-only | EDIT | EDIT | PASS + annotate | PASS + annotate |
| **R0** internal draft | PASS + annotate | PASS + annotate | PASS | PASS |

**Annotation** *(one only — bracket down column 2)*
```
one unproven claim — four outcomes
clause 7.2 → escalate · ₹1,84,000 held
```

**Bottom strip**
```
EDIT — strip or re-ground the named span, never a rewrite.   ESCALATE — inline hold; ships claim + spans + verdict.
Bias — counterfactual flip rate, route-level, CI excludes zero.   Safety — typed interlocks: tool × args × irreversibility.
Hard gate on actions, not tokens. Text streams with a short hold-back.
```

## Slide 3

**Headline**
```
The claims we refuse to make — and the format we publish.
```

**Left column** *(struck-through claim, correction beneath)*
```
"We eliminate hallucinations."
→ We don't. Ungrounded claims cannot authorise actions, and we report what we miss.

"Zero integration — drop it in."
→ We hook context assembly. That is real work, and it is the reason this works at all.

"Zero added latency."
→ Verification is budgeted, not free.

"99% accuracy across bias, safety and risk."
→ One number over three failure modes is a demo artifact.
```

**Above the report block, small:**
```
Everyone in this category publishes precision. This is the other number.
```

**Right column** *(monospace, hairline border, terminal styling)*
```
per-route gate report — format

route                      finance/refund-agent
gate latency (p50 / p95)   <measured> / <measured>
ungrounded claims caught   <measured>
missed  (FNR)              <measured>  ± <CI>
entitlement violations     100%  (deterministic — property, not measurement)
audit sample               100% of blocks + escalations
                             3% of passes

illustrative format — Round 2 fills this with measured values
```

**Closing line** *(largest text on the slide — larger than the headline)*
```
Now nothing acts until it can prove it should.
```

---

# 2 — RECORDING PACKAGE

**Script:** the teleprompter cut in [STAGE5-VIDEO.md](STAGE5-VIDEO.md) Part C. 340 words, hold marks in seconds.

**Visual timing sheet**

| Time | Visual priority | Animation load |
|---|---|---|
| 0:00–0:30 | Agent transcript, filter annotations, stamp, timestamps | low |
| 0:30–1:15 | Transcript parks top-left. Category line, four strike-throughs, context-assembly boundary draws | medium |
| 1:15–2:15 | Full graph build + three sequential reads | **heaviest — budget most of the production time here** |
| 2:15–2:45 | Matrix (8s) → actuator chips + JSON packet → text/action split → FNR report block | medium |
| 2:45–3:00 | Transcript returns full-frame, one field changed → silence → black → wordmark | low |

**Rehearse Beat 3 and Beat 5 hardest.** Beat 3 is mostly visual silence and a nervous narrator will fill it. Beat 5 is unforgiving — the period is the punch, and a warm read kills it.

---

# 3 — HOSTILE Q&A

Sixteen questions, grouped by attack vector. Each has the answer in our voice and, where it matters, **the trap** — the plausible wrong answer that loses the room.

## A. "You're not actually different"

**A1 · "Isn't this just NeMo Guardrails or LlamaGuard with extra steps?"**
> Guardrails inspect strings at the perimeter with syntax rules. They are blind to whether the system ever gave the model the fact it is citing, and blind to who is asking. We integrate at context assembly: we don't inspect syntax, we check whether a claim binds to a span the caller is entitled to read — before the action fires.

**A2 · "Isn't 'blast radius' just severity with extra vocabulary?"**
> Severity describes the error. Blast radius describes the consequence. They are orthogonal, which is the entire point of the matrix — the identical verdict produces four different actuators depending on what the response is about to do. Collapse them and you are back to a composite risk score, which is the failure mode of the category.

**A3 · "This is RAG groundedness checking."**
> It is the closest cousin and it is structurally short in three ways. Groundedness checkers see retrieval only — not tool results, DB rows, computed values or system context, which is where agents actually get their facts. They average, so one wrong figure drowns in nine correct sentences. And they are action-blind, so 0.82 means the same thing on a draft and on a wire transfer. None of them carry caller identity, so none of them can do entitlement at all.

## B. "It won't work"

**B1 · "What about a purely parametric answer? No retrieval, no spans, nothing to bind to."** ← *the sharpest attack; know this cold*
> Binding is undefined when there is no evidence set, and we don't pretend otherwise. Two things happen. Routes with no provenance are *declared* ungrounded by construction — that is a legitimate verdict, and blast radius still applies, so an ungrounded answer can annotate a draft but cannot authorise a payment. Separately, the async lane runs a semantic-entropy probe — resample, cluster by meaning, measure dispersion — which is the only signal available without evidence, and it feeds route-level calibration, never the token stream.
>
> **The line that wins it:** *"We don't claim to verify what we were never given. We claim that what we were never given cannot authorise an action."*
>
> **Trap:** claiming the graph works everywhere. It doesn't, and a judge who has built RAG knows it.

**B2 · "The model paraphrases instead of quoting. Does binding survive?"**
> Binding is entailment, not string matching — that is what the cross-encoder is for. Exact matching is used only where exactness is the correct test: numbers, dates and identifiers, which are recomputed deterministically against the span set. A paraphrase that preserves meaning binds. A paraphrase that drifts the figure does not, and that is the behaviour we want.

**B3 · "Multi-hop and synthesised claims — entailment is weakest exactly there."**
> Correct, and that is our single strongest residual risk. Derived claims are never marked SUPPORTED by entailment alone. Anything arithmetic or aggregative is recomputed from spans. Anything neither recomputable nor directly entailed returns UNKNOWN, and **UNKNOWN never collapses into SUPPORTED.** That one rule is the boundary between a control plane and false assurance.

**B4 · "Who defines the ACLs? If the index is already over-permissioned you enforce a wrong rule perfectly."**
> We enforce the access rights the source system already carries; we don't invent them. If the index is over-permissioned we will faithfully enforce a wrong policy — but we make it *visible*, because every entitlement decision is logged against a named principal and a named source. And the query-time check is precisely the detector for that condition: a span sitting in provenance whose ACL excludes the caller is exactly what an over-permissioned index looks like from the inside.
>
> **Trap:** claiming we fix their IAM. We don't. We stop it being silently bypassed by a model.

**B5 · "Prompt injection. Can an attacker make a false claim bind to a real span?"**
> The binding is computed by us, not asserted by the model — the model has no channel to declare a binding. An injection can change what the model says; it cannot change which spans were captured at context assembly, nor the entailment verdict, nor the ACL. The attack that does work is poisoning a source document so that a genuine span supports a false claim — that is a supply-chain attack on the corpus, not on the plane, and the source ID and content hash are what make it forensically traceable.
>
> **The honest boundary, stated out loud:** *we defend the claim-to-evidence link, not the truth of the evidence.*

## C. "It won't ship"

**C1 · "How is this latency realistic?"**
> The hard gate sits only on actions. Text streams optimistically behind a short hold-back, so users perceive the model's speed. Deterministic checks — span membership, ACL, arithmetic — run inline in tens of milliseconds with no model call and carry 80–90% of traffic. Expensive binding runs only where blast radius justifies it. And tool-call arguments are verified *while the tool call is already in flight*, so that verification completes inside the tool's own latency.

**C2 · "You call the integration cost a moat. What is it actually?"**
> One SDK hook where you already assemble context, plus an OpenAI-compatible proxy. No model access, no weights, no logits, no fine-tuning, no application rewrite. If you are on a standard retrieval stack the retriever already knows the source ID — you are adding the access rights and a hash. Days, not quarters. It is not zero, and we say so, because a team that discovers the integration cost *after* being sold "drop-in" churns.

**C3 · "Day one. No baselines, no history. What works?"**
> Every deterministic mechanism works from the first request: span membership, entitlement, arithmetic recomputation, typed interlocks. Only the statistical parts need history — route cost baselines exclude a cold-start window, and counterfactual bias replay needs a rolling sample. And nothing enforces on day one anyway: shadow mode is the default deployment, so the first output is the counterfactual — *would have held N, of which M were true positives* — not a block.

**C4 · "What happens when ControlPlane itself goes down?"**
> Fail stance is declared per blast-radius tier, not globally. R0 and R1 fail open with annotation; R2 and R3 fail closed or escalate. The plane is never a single point of failure for the whole product — only for dangerous actions. That asymmetry is deliberate: a universal fail-open would make the plane bypassable by anyone who can induce load.

**C5 · "Why won't the team just switch it off in a quarter, like every other guardrail?"**
> Because it doesn't block their text. The hard gate is on actions, and R0/R1 — the overwhelming majority of volume — passes with annotation. Enforcement is earned per route through shadow evidence, so nobody is asked to trust it before it has produced its own counterfactual. Over-blocking is what gets these layers disabled, and the matrix exists specifically to prevent it.

## D. "Prove it"

**D1 · "You publish a false-negative rate. How would you even know it?"**
> Stratified shadow audit. One hundred percent of holds and escalations plus a random slice of passes are sampled to expensive ground truth — a slower, more thorough verification path than the one running inline. The result is reported per route with confidence intervals and updated continuously. The number on the slide is a *format*; Round 2 fills it with measured values.
>
> **Trap:** filling the placeholders in with plausible numbers before the pitch. The empty schema *is* the claim — it says we know exactly which fields are knowable at design time and which are not.

**D2 · "You add verification compute to save wasted compute. What's the net?"**
> Dead compute is measured exactly rather than estimated — every step that grounded zero claims in the accepted answer, found by walking the graph backward. Verification is deterministic and inline for most traffic, with the expensive lane reserved for the small fraction that can cause harm. But we do not put a savings percentage on a slide, because we have not measured it on your traffic. What we can do from day one is name the exact spend that grounded nothing.

**D3 · "One demo trace. How do you know it generalises?"**
> The mechanisms are trace-independent — span membership, ACL comparison, arithmetic recomputation and backward attribution are the same operations on any trace. What varies by route is the threshold, which is why calibration is per-route and why enforcement is earned per route rather than switched on globally.

**D4 · "Where does bias fit? You barely mention it."**
> Deliberately, because it is the one axis that is not a per-response property. Counterfactual invariance at route level, async: perturb protected attributes on decision-shaped outputs and measure decision flip rate with a confidence interval over a rolling window. Flag when the interval excludes zero. We never issue a per-response bias verdict — bias is a distributional property or it is nothing.

**D5 · "Why should we believe any of this? You're a team with slides."**
> You shouldn't believe the numbers — that is why the only number on our deck is labelled a format. What you can evaluate today is the architecture: whether capturing provenance outside the model is the right place to stand, whether inverting the burden of proof is the right default, and whether pricing verification by blast radius is the right way to stay fast. Those are design decisions you can attack directly, and they don't require trusting a benchmark we haven't run.

---

# 4 — TEAM ALIGNMENT

**The thesis we own.** An AI response is a set of claims requesting permission to act. We capture evidence at context assembly, outside the model, invert the burden of proof, and gate actions on proof.

**The one running example.** ₹1,84,000 refund under clause 7.2 — **which does not exist.** Money moved Tuesday, found Friday. Never say the clause "caps" or "denies" anything: the failure is absence of evidence, which is what makes Escalate the correct actuator rather than Block.

**Three non-negotiables.**
1. One graph, three reads — never three separate tools.
2. Default = UNSUPPORTED.
3. We publish what we miss, not just what we catch.

**Vocabulary we refuse in our own voice.** monitor · detect · observe · watch · guard · trust score · risk score · responsible AI · "AI safety" as a standalone virtue. Use authorise · admit · prove · bind · refuse · hold · escalate · gate.
*One exception:* "Everyone watches the exit" — permitted, because it indicts what everyone else built.

**What we never claim.** We eliminate hallucinations · zero integration · zero added latency · one accuracy number across three failure modes.

**Never say "blocked" about the refund.** The matrix routes it to Escalate. Say *held and escalated with the evidence packet.*

---

# 5 — SHIP CHECKLIST

**Deck**
- [ ] Matrix transcribed exactly — axis labels, column vocabulary and cell values all match the freeze
- [ ] Slide 2 headline says "holds a payment", agreeing with the R3 pin beneath it
- [ ] Both locked lines present on Slide 1 — kicker and footer
- [ ] Slide 1's third supporting line keeps its three specifics
- [ ] FNR block carries the `illustrative format` label
- [ ] Three axes are leader lines, not panels
- [ ] No padlock, shield, eye, dashboard or magnifying glass anywhere
- [ ] Slide 3 left column is the refuse-to-*claim* list, not rejected approaches
- [ ] Closing line set larger than the headline
- [ ] No logo, no team photo, no thank-you panel

**Video**
- [ ] Runtime ≤ 3:00
- [ ] Clause 7.2 described as nonexistent, never as capping or denying
- [ ] The word "blocked" never used about the refund
- [ ] The refund transcript never leaves the screen after 0:30
- [ ] Final shot is the opening transcript with one field changed
- [ ] Absolute silence after the final line — no thank-you, no trailing sentence
- [ ] No spoken accuracy figure

**People**
- [ ] Both presenters can draw the graph and the matrix from memory
- [ ] Both can answer B1 (no retrieval context) and B5 (prompt injection) without hesitating
- [ ] Both can explain why the gate report ships as an empty schema, and will say it unprompted

**Build order:** slides first, then a rough video cut against the teleprompter, then Q&A drilling, then polish. Polishing before the rough cut exists is the most common way a deadline is missed.
