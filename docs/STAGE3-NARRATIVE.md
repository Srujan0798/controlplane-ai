# ControlPlane.ai — Frozen Stage 3
### Differentiation + Narrative Spine · adversarial merge of 7 proposals

**Deliverable:** max 3-slide concept deck + max 3-minute video.
**Constraint:** architecture is frozen. No new mechanisms invented below.

---

# PART A — AUDIT

## A1. Fidelity check (run first, before scoring anything)

Stage 3 has a failure mode Stage 2 did not: a narrative proposal can quietly re-import mechanisms the architecture already killed. Every proposal was checked against the freeze before it was scored.

| Proposal | Fidelity | Notes |
|---|---|---|
| **claude3** | ✅ clean | Stays inside the freeze throughout. Uses only locked mechanisms. |
| **kimi3** | ✅ clean | Clean. Adds framing, not mechanisms. |
| **minimax3** | ✅ clean | Clean. Adds production discipline and competitor names. |
| **mistral3** | ✅ clean | Thin but faithful. |
| **gemini3** | ⚠️ minor | "Kills the span" on cost is loose phrasing for the loop breaker; markdown table is malformed. |
| **glm3** | ⚠️ **trap** | Recommends *dropping bias entirely* in favour of "data exfiltration." The brief names bias explicitly under responsibility — deliberately omitting it scores against the rubric. **Rejected.** |
| **gpt3** | ❌ **off-freeze** | Reintroduces **speculative release** ("we'd rather release a plausible answer and fix it in the background"), **ECS / MCUT** as headline mechanisms, and **latency-triggered action downgrade** — all three were killed or folded in Stage 2. Also the most marketing-inflected of the seven ("provable trust", "the inevitable answer", "enterprise-grade control, not guesswork"). **Contributes exactly one line** (see #14). |

> **This is the single most important audit finding.** GPT was a primary input at Stage 2 and produced the weakest, least faithful Stage 3. Do not let its framing back into the deck — its narrative describes a system we deliberately did not build.

## A2. Element inventory & scoring

Scored 1–10 on **S**harpness (non-obvious) · **D**ifferentiation power · **C**redibility with a serious engineer · **F**ormat fit (3 slides / 3 min) · **A**rchitecture fidelity. Total /50.

### Single Sharp Insight

| # | Element | Source | S | D | C | F | A | Σ | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **The evidence that proves an output existed *before* the model ran — and is discarded at generation** | claude | 10 | 10 | 10 | 9 | 10 | **49** | **KEEP — the spine** |
| 2 | **"Reads the model's receipts," not the model's mind** | glm | 9 | 8 | 8 | 10 | 9 | 44 | **KEEP — as the compression** |
| 3 | Detection becomes a *set-membership test*, not a judgment call | claude | 9 | 9 | 10 | 8 | 10 | 46 | KEEP |
| 4 | Response = **unprivileged execution claim** that must prove entitlement | kimi | 9 | 9 | 9 | 8 | 10 | 45 | KEEP → §3 + §5 |
| 5 | Unit-of-analysis shift: the claim, not the response | minimax | 8 | 8 | 8 | 9 | 10 | 43 | FOLD → 1 |
| 6 | "Deterministic execution gating bound to context-assembly provenance" | gemini | 6 | 7 | 8 | 4 | 10 | 35 | FOLD — accurate but unspeakable aloud |
| 7 | "Evidence as a first-class runtime constraint" | gpt | 6 | 5 | 7 | 5 | 8 | 31 | KILL — abstract, no image |

### Market failure analysis

| # | Element | Source | S | D | C | F | A | Σ | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 8 | **Judge asks "does this look right?" (unfalsifiable) — we ask "which span proves it?" (has an answer)** | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP** |
| 9 | Guardrails are **identity-blind**: the same string is fine for one caller, a breach for another | claude | 10 | 10 | 10 | 9 | 10 | **49** | **KEEP** |
| 10 | **"A dashboard can say the trace cost ₹8. It cannot say ₹5 of it grounded nothing."** | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP** |
| 11 | "You cannot detect a calibration failure with the calibration" | claude | 10 | 9 | 10 | 9 | 10 | 48 | KEEP |
| 12 | **"Retrieval is not permission."** | kimi | 10 | 9 | 9 | 10 | 10 | 48 | KEEP |
| 13 | RAG checkers fail three structural ways (retrieval-only · they average · action-blind) | claude | 9 | 10 | 10 | 8 | 10 | 47 | KEEP |
| 14 | **Naming real products** (NeMo, LlamaGuard, Lakera, LangSmith, Arize, Bedrock Guardrails) | minimax, gemini | 8 | 9 | 10 | 9 | 10 | 46 | **KEEP — nobody else names names** |
| 15 | **"Not one of them publishes its own false-negative rate."** | minimax | 9 | 10 | 10 | 10 | 10 | **49** | **KEEP — the unifying kill** |
| 16 | "You cannot block, edit or escalate on 87." | claude | 9 | 9 | 9 | 10 | 10 | 47 | KEEP |
| 17 | "Observation without execution control is an audit trail, not architecture" | kimi | 8 | 8 | 9 | 9 | 10 | 44 | KEEP |
| 18 | "Turns risk management into an expensive autopsy report" | gemini | 7 | 6 | 7 | 9 | 10 | 39 | FOLD → 10 is stronger |
| 19 | "Tells you the car crashed; doesn't apply the brakes" | glm | 6 | 5 | 6 | 9 | 10 | 36 | KILL — worn metaphor |
| 20 | "By Gödel-style logic no finite ruleset can cover all cases" | gpt | 4 | 4 | 3 | 5 | 8 | 24 | KILL — pretentious and wrong |

### Positioning statement

| # | Element | Source | S | D | C | F | A | Σ | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 21 | **"The cost of a wrong output changed category: it used to be a bad paragraph, it is now an executed transaction."** | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP — best line in all 7** |
| 22 | "From AI that answers to AI that acts, while oversight is still built for the answering era" | claude | 9 | 9 | 9 | 10 | 10 | 47 | KEEP |
| 23 | **"Admission-control layer"** as the category noun | claude | 9 | 9 | 10 | 9 | 10 | 47 | KEEP |
| 24 | "Execution-boundary layer between any model and the outside world" | kimi | 8 | 8 | 9 | 9 | 10 | 44 | FOLD → 23 |
| 25 | "Verification proxy, not a guardrail" | glm | 7 | 7 | 8 | 9 | 10 | 41 | FOLD → 23 |
| 26 | claude's full positioning paragraph verbatim | claude | 9 | 9 | 10 | 6 | 10 | 44 | **KEEP but CUT — 180 words ≈ 70s, overruns the 30s slot** |
| 27 | "ControlPlane delivers provable trust" / "the inevitable answer" | gpt | 2 | 2 | 2 | 6 | 7 | 19 | KILL — pitch-deck fluff |

### Differentiation points

| # | Element | Source | S | D | C | F | A | Σ | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 28 | Score the output → **Query the evidence** | claude | 9 | 10 | 10 | 10 | 10 | 49 | KEEP |
| 29 | Monitor and alert → **Interlock in the commit path** | claude | 9 | 10 | 10 | 10 | 10 | 49 | KEEP |
| 30 | Default allow → **Default UNSUPPORTED; nothing passes because nobody objected** | claude | 10 | 9 | 10 | 10 | 10 | 49 | KEEP |
| 31 | One threshold for all traffic → **Blast radius × verdict severity** | claude, kimi, mistral | 9 | 9 | 10 | 10 | 10 | 48 | KEEP |
| 32 | **"They publish precision — the rate at which they bother the user. We publish the rate at which we missed."** | minimax | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP — sharpest FNR framing produced** |
| 33 | "Evidence-gated micro-services" as the differentiator | gpt | 5 | 4 | 6 | 5 | 6 | 26 | KILL — implementation detail, not a difference |

### Narrative beats

| # | Element | Source | S | D | C | F | A | Σ | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 34 | **One trace end to end** — the same refund in hook, mechanism, matrix and close | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP — the structural decision** |
| 35 | **Hook: ₹1,84,000 refund under "clause 7.2," which does not exist. Confidence 0.94. Moved Tuesday, found Friday.** | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP** |
| 36 | **"The system didn't fail. It was never asked to prove anything."** | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP — hook button** |
| 37 | **"Everyone watches the exit; nobody records the entrance."** | claude | 10 | 10 | 9 | 10 | 10 | **49** | **KEEP — the reframe line** |
| 38 | 6 claims start red, 5 turn green, one stays red — **"not low-confidence: unproven"** | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP — best 10 seconds of video** |
| 39 | **"Everywhere else that's three products. Here it's three queries — because it's the same graph."** | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP** |
| 40 | **Visual rule: one graph, three highlight passes — never three side-by-side dashboards** | minimax | 9 | 10 | 9 | 10 | 10 | 48 | **KEEP — production instruction** |
| 41 | **Close: "That system was never asked to prove anything. Now nothing acts until it can prove it should."** | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP** |
| 42 | Close: "Monitoring tells you the plane crashed. ControlPlane is air traffic control." | kimi | 7 | 7 | 6 | 9 | 10 | 39 | KILL — the plane/plane pun undercuts it; "remain a passenger" is ad copy |
| 43 | Close: green PERMISSION GRANTED / red PERMISSION DENIED stamp bookend | mistral | 6 | 6 | 5 | 9 | 10 | 36 | KILL — literal, and the hook already bookends |
| 44 | Opening: "Every AI safety pitch you've heard this week starts the same way…" | minimax | 8 | 7 | 7 | 8 | 10 | 40 | KILL — names the category before you've escaped it |
| 45 | Opening: "Six weeks is how long a system leaked data before an audit found it" | kimi | 7 | 7 | 7 | 9 | 10 | 40 | FOLD — no rupee figure, no action; weaker than 35 |
| 46 | Split-screen: dashboard green / agent drops a database | gemini | 8 | 8 | 7 | 9 | 10 | 42 | FOLD → the visual works, attach it to 35 |
| 47 | **Framing rule: every line must name a claim, a graph, an action or a measurement — or it gets cut** | minimax | 9 | 9 | 9 | 10 | 10 | 47 | **KEEP — script discipline** |

### Claims to refuse

| # | Element | Source | S | D | C | F | A | Σ | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 48 | **"We eliminate hallucinations"** — invites *"then what's your miss rate?"* | claude, all | 9 | 9 | 10 | 10 | 10 | 48 | KEEP |
| 49 | **"Model-agnostic, zero integration" — the integration cost IS the moat; say it out loud** | claude, mistral | 10 | 10 | 10 | 9 | 10 | **49** | **KEEP — most counterintuitive item in all 7** |
| 50 | **"Zero latency" → "we never make the model feel slow; we make the action wait"** | minimax, claude | 9 | 9 | 10 | 10 | 10 | 48 | KEEP |
| 51 | "99% accuracy across bias, safety and risk" — one number over three incommensurables | claude | 9 | 8 | 10 | 9 | 10 | 46 | KEEP |
| 52 | "Powered by a proprietary safety-trained foundation model" | kimi | 8 | 8 | 9 | 8 | 10 | 43 | FOLD → 49 |
| 53 | "We replace human review" | minimax, gpt, kimi | 7 | 6 | 8 | 9 | 10 | 40 | FOLD → 51 (crowded; four is the limit) |

### Narrative risks

| # | Element | Source | S | D | C | F | A | Σ | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 54 | **Risk: pattern-matched to "another AI safety tool" in 20s; trigger is any opening that starts from risk** | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP** |
| 55 | **Correction: open on a blocked transaction, never on risk** | claude | 10 | 10 | 10 | 10 | 10 | **50** | **KEEP** |
| 56 | **Ban the vocabulary** — kill monitor/observe/detect/guard/trust score; use authorize/admit/prove/bind/refuse | claude, kimi, mistral, glm | 9 | 10 | 9 | 10 | 10 | 48 | **KEEP — 4/7 convergence** |
| 57 | **"Safety" may appear only after "deterministic entitlement check" — never as a standalone virtue** | kimi | 10 | 9 | 9 | 10 | 10 | 48 | KEEP |
| 58 | **The ship test:** if a judge could summarise it as "watches AI outputs and flags problems," it failed | claude | 10 | 10 | 9 | 10 | 10 | **49** | **KEEP** |
| 59 | First sentence must contain "claim," not "response" | minimax | 8 | 8 | 8 | 10 | 10 | 44 | KEEP |
| 60 | Pre-loaded Q&A rebuttal to "isn't this NeMo/LlamaGuard?" | gemini | 8 | 8 | 9 | 8 | 10 | 43 | KEEP → Q&A prep, not the deck |
| 61 | Position as infra reliability proxy — a firewall or transaction validator | glm | 8 | 8 | 9 | 9 | 10 | 44 | KEEP |
| 62 | "The CPU's privilege mode for AI" | gpt | 8 | 8 | 9 | 9 | 9 | 43 | KEEP → gpt3's only surviving contribution |
| 63 | **Drop "bias" entirely; talk only about data exfiltration** | glm | 5 | 6 | 6 | 7 | 3 | 27 | **KILL — scores against the rubric. The brief names bias explicitly.** |

---
---

# PART B — THE FROZEN STAGE 3

## 1. Single Sharp Insight

> Every oversight tool inspects what the model **said**, but the only thing that can prove it is the evidence assembled **before the model ran** — and that record is thrown away the moment generation starts. ControlPlane keeps the receipts, which turns hallucination detection from a judgment call into a set-membership test, and turns oversight from scoring text into authorizing actions.

---

## 2. What the Market Currently Does — and Why Each Fails

**LLM-as-judge.** *(NeMo Guardrails, most "AI safety" wrappers.)* A second model is asked whether the first was right — usually without the source documents, always without knowing who was asking. It produces an opinion using the same reasoning that produced the error, from the same family of blind spots. It cannot state its own error rate, and it is too slow to stand in front of an action.
> The judge asks **"does this look right?"** — an unfalsifiable question. We ask **"which span proves it?"** — a query with an answer.

**Static guardrails.** *(LlamaGuard, Lakera, regex and deny-lists.)* They match banned surface forms. A fabricated invoice number, a salary leaked from an over-permissioned index, and a correct answer are all lexically clean, so guardrails see none of them. And they are **identity-blind**: the same string is fine for one caller and a breach for another. Deterministic entitlement checking is not a better classifier — it is a different question.

**Post-hoc observability.** *(LangSmith, Helicone, Arize, WhyLabs.)* Beautifully engineered, exactly the wrong product. They tell you what went wrong after a user acted on it — the precise thing the brief asks to eliminate. Observation without execution control is an audit trail, not architecture. They also measure spend rather than waste:
> A dashboard can tell you the trace cost **₹8**. It cannot tell you that **₹5 of it grounded nothing** in the final answer. Walking the graph backward can — because the graph that verifies is the graph that accounts.

**Confidence thresholding.** Logprobs, self-reported certainty, verbalised hedging. This fails by definition: the named failure mode is *confidently* wrong. **You cannot detect a calibration failure with the calibration.** Fluent, high-probability fabrication is the modal enterprise incident and it sails past every confidence gate.

**Simple RAG groundedness checkers.** The closest cousin, and structurally short in three ways. They see **retrieval only** — not tool results, DB rows, computed values or system context, which is where agents actually get their facts. They **average**, so one wrong figure drowns in nine correct sentences. And they are **action-blind**, so 0.82 means the same thing on a draft and on a wire transfer.
> **Retrieval is not permission.**

**Composite risk scores.** *(Azure AI Content Safety, Bedrock Guardrails, most "responsible AI" suites.)* "Trust: 87/100." Three failure modes with three different owners, costs and remedies, collapsed into one number that maps to no intervention. **You cannot block, edit or escalate on 87.**

**What all six share:** they inspect the output, not the context contract. They score the text rather than verify the claim. They gate on words rather than on actions. **And not one of them publishes its own false-negative rate.**

---

## 3. Positioning Statement

**Slide 1 / full version:**

> ControlPlane.ai is an **admission-control layer** for AI systems. Enterprises have moved from AI that answers to AI that acts — it refunds, files, sends, books and writes to production — while oversight tooling is still built for the answering era: score the text, chart the failure, review the log next week. ControlPlane treats every response as a set of **claims requesting permission to act**. It captures the evidence the model was actually given at context-assembly time, with source identity and access rights attached, binds each claim in the output back to a specific span of that evidence, and refuses to let an unproven claim cross into an action. Verification effort is priced by what the response is about to do: a draft is checked cheaply, a payment is not. Performance, cost and responsibility stop being three tools and become **three reads of one graph — STEP → SPAN → CLAIM → ACTION.** This matters now because the cost of a wrong AI output has changed category: **it used to be a bad paragraph. It is now an executed transaction.**

**Slide-text compression** *(if Slide 1 runs out of room, this clause replaces the draft/payment example — tighter on the page, weaker in the mouth)*:

> …binds each claim back to a specific span of that evidence, and refuses to let an unproven claim cross into an action. **Verification effort is priced by blast radius.** Performance, cost and responsibility stop being three tools and become three reads of one graph.

Use the compressed clause on the slide and the draft/payment example in the video. Same content, two media, different optimum: the page rewards density, the microphone rewards the concrete image.

**Spoken 30-second cut** *(the full paragraph runs ~70s aloud — do not read it verbatim on camera)*:

> "ControlPlane is an admission-control layer for AI. Enterprises moved from AI that answers to AI that acts — it refunds, files, sends, writes to production — but oversight is still built for the answering era. We treat every response as a set of claims requesting permission to act, bind each claim to the evidence the model was actually given, and refuse to let an unproven claim cross into an action. Because the cost of a wrong output has changed category: it used to be a bad paragraph. It's now an executed transaction."

---

## 4. Differentiation Table

| Common approach | ControlPlane |
|---|---|
| **Score the output** — a judge or groundedness model forms an opinion about finished text | **Query the evidence** — the verdict is a lookup against spans captured before the model ran, with source and ACL attached. Not an opinion formed after the fact; a binding that either exists or doesn't. |
| **Monitor and alert** — traces, dashboards, weekly review | **Interlock in the commit path** — text streams optimistically; actions do not proceed without proof. The output is a decision, not a chart. The same graph also prices the waste: we can name the exact spend that grounded nothing. |
| **Flag what looks wrong; default is allow** | **Default is UNSUPPORTED** — the claim carries the burden of proof. Nothing passes because nobody objected. |
| **One threshold, one score, all traffic** | **Blast radius × verdict severity** — the identical verdict annotates a draft and holds a payment. Budget is spent where the harm is, which is also why it stays fast. |
| **Publish precision** — the rate at which the tool bothers the user | **Publish our own per-route false-negative rate** — the rate at which we *missed*. The plane is audited by the standard it enforces. |

---

## 5. Narrative Spine — 3:00

> **Script discipline:** every line must name a claim, a graph, an action or a measurement. Any sentence that only says "the AI" or "the response" in the abstract gets cut. That rule alone is why this won't sound like the other fifty pitches.

### 0:00–0:30 · Hook — one screen, one transaction

An agent's output on screen: **"Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement."**

Beat. **Clause 7.2 does not exist.** Every guardrail passed it — nothing was toxic, nothing was off-policy, confidence was 0.94. Optional split-screen: the observability dashboard beside it, green and healthy. The money moved on a Tuesday. It was found on a Friday.

**Land it:** *"The system didn't fail. It was never asked to prove anything."*

### 0:30–1:15 · Problem, then reframe

The failure category changed: AI stopped answering and started acting. Oversight didn't move with it. Fast sweep — ten seconds, no survey: a judge gives you an opinion, a guardrail checks surface forms, a dashboard tells you on Friday, and confidence is the instrument that's broken.

Then the structural point: the evidence that could have caught this existed **before** the model ran, at context assembly — and nobody is standing there.

**Land it:** *"Everyone watches the exit. Nobody records the entrance."*

The reframe: an AI response is not text to be scored — it is a set of claims requesting permission to act. Put the graph on screen once: **STEP → SPAN → CLAIM → ACTION.**

### 1:15–2:15 · Mechanism and the three-axis read — same refund trace, all the way down

Provenance captured outside the model: **14 spans**, each with source ID, hash, ACL. The response decomposes into **6 claims — all six start red**, because the default is UNSUPPORTED. Five turn green as spans prove them. *"Clause 7.2 permits this refund"* finds no span. **It stays red. Not low-confidence — unproven.**

Then the same graph, three questions:

- **Performance** — one unproven categorical claim, and it is the one authorising the payment. Worst claim governs.
- **Responsibility** — one span that *did* ground a claim came from a document whose ACL excludes the caller. Deterministic. No classifier involved.
- **Cost** — walk the graph backward: of 9 tool calls in this trace, 4 produced spans that ground nothing in the answer. Measured, not estimated.

> **Visual rule (non-negotiable):** one graph, three highlight passes. **Never** three side-by-side dashboards. The moment the audience realises they are looking at the *same structure* three times is the most valuable second in the video.

**Land it:** *"Everywhere else that's three products. Here it's three queries — because it's the same graph."*

### 2:15–2:45 · Why it doesn't over-block

The matrix on screen for two seconds: blast radius R0–R3 against verdict severity, only a few cells lit. The identical unproven claim **annotates** a draft, gets **stripped** from a read-only answer, and **blocks** a payment.

Edits are surgical — strip the claim or force re-grounding on the named span, never a rewrite, because a rewrite is a new unverified artifact. Escalation ships the claim, the candidate spans and the verdict, so a human resolves in seconds rather than triaging a severity colour.

Latency: text streams with a short hold-back, and the hard gate sits on the **action**, not the tokens. Users feel the model's speed; the gate sits where the money moves.

Then the credibility line: **every other product in this category publishes precision — the rate at which it bothers the user. We publish the rate at which we missed, per route.**

### 2:45–3:00 · Close — answer the hook exactly

> **"That system was never asked to prove anything. Now nothing acts until it can prove it should."**

*(Title card if one is needed: "ControlPlane — proof before permission." Optional; the spoken line is stronger alone.)*

---

## 6. What We Deliberately Refuse to Claim

**"We eliminate hallucinations."** Anyone who has shipped knows this is false, and it invites the one question that ends the pitch: *then what's your miss rate?* We claim something narrower and much harder to attack — ungrounded claims cannot authorise actions, and we report what we miss.

**"Model-agnostic, zero integration, drop it in."** We hook context assembly. That is real integration work, and it is the exact reason the design works. Trading our strongest structural claim for a weaker convenience claim is a bad trade. **The integration cost is the moat — say it out loud.** (Corollary: we also don't claim a proprietary safety-trained model. We sit on top of yours.)

**"Zero added latency."** Nobody believes it and we don't need it. The honest version is stronger: **we never make the model feel slow; we make the action wait.** Deterministic checks inline in tens of milliseconds, expensive checks only where blast radius justifies them.

**"99% accuracy detecting bias, safety and risk."** One accuracy number across three incommensurable failure modes is a demo artifact — and any figure we cannot reproduce on their traffic becomes a liability the first time they test it.

---

## 7. Strongest Narrative Risk + Exact Correction

**The risk:** judges pattern-match this to "another AI safety tool" inside the first twenty seconds, and everything after is heard as a variant of decks they have already sat through. The architecture never gets evaluated on its merits.

**The trigger is specific: any opening that starts from risk.** *"AI is powerful but risky, and here's how we make it safe"* is the first line of every guardrail deck in the room, and it sets the frame before you have said anything of your own.

### The correction — four moves

**1 · Open on a blocked transaction, never on risk.** The first thing on screen is a specific action with a rupee figure attached that did or did not happen. This is an authorisation system that happens to catch errors, not a safety system that happens to have a gate. Lead with the interlock; the danger is implied by the money.

**2 · Ban the vocabulary.** *(Four of seven proposals converged on this independently.)*

| Never say | Say instead |
|---|---|
| monitors, observes, detects, watches, guards | authorises, admits, proves, binds, refuses, gates |
| trust score, risk score, safety score | verdict, binding, entitlement, blast radius |
| observability layer, guardrail | admission-control layer, permission layer |
| responsible AI, ethics, trustworthy | deterministic entitlement check, ACL violation |

The first sentence must contain the word **"claim,"** not "response." And **"safety" may appear only *after* "deterministic entitlement check" — never as a standalone virtue.** The brief says watch, catch, act: say plainly that watching and catching are commoditised and we compete on the third.

**3 · Run one trace end to end.** The same refund appears in the hook, the mechanism, the matrix and the closing line. Generic decks cycle through three shallow scenarios; following one case to the bottom is what reads as production experience. Breadth reads as slideware; depth reads as someone who has run this in anger.

**4 · Position as infrastructure, not ethics.** The reference class is a firewall, a transaction validator, **the CPU's privilege mode** — not an AI-safety wrapper. Cold, structural, graph-shaped language throughout.

### The ship test

> If a judge could summarise the deck as *"it watches AI outputs and flags problems,"* the narrative has failed regardless of the architecture underneath. Rewrite until that sentence no longer fits.

---

## Appendix — Two traps to avoid

**Do not drop bias.** One proposal recommended cutting bias entirely and speaking only about data exfiltration, on the grounds that it sounds more like engineering. **The brief names bias explicitly** under responsibility; omitting it scores against the rubric. The correct move is to keep it and state it in *measurement* terms, never moral ones: **counterfactual flip rate with a confidence interval, route-level, async.** If a judge asks about bias, that sentence is the whole answer — it is more rigorous than anything a fairness-dashboard team will say, and it never leaves engineering register.

**Pre-loaded rebuttal — "Isn't this just NeMo Guardrails / LlamaGuard?"**
> "Guardrails inspect strings at the perimeter with syntax rules. They are blind to whether the system ever gave the model the fact it is citing, and blind to who is asking. We integrate at context assembly: we don't inspect syntax, we check whether a claim binds to a span the caller is entitled to read — before the action fires."
