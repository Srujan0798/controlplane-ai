# ControlPlane.ai — Narrative & Positioning

> How the system is explained, differentiated and defended in language.
> Companion to [ARCHITECTURE.md](ARCHITECTURE.md) — that file is what we built, this is how we say it.

---

## 1. The single sharp insight

> Every oversight tool inspects what the model **said**, but the only thing that can prove it is
> the evidence assembled **before the model ran** — and that record is thrown away the moment
> generation starts. ControlPlane keeps the receipts, which turns hallucination detection from a
> judgment call into a **set-membership test**, and turns oversight from scoring text into
> authorizing actions.

Compressed: *we read the model's receipts, not the model's mind.*

The load-bearing phrase is **set-membership test** — it is what makes the insight concrete for a
technical judge. Do not drop it for brevity.

---

## 2. Positioning

**Full version:**

> ControlPlane.ai is an **admission-control layer** for AI systems. Enterprises have moved from
> AI that answers to AI that acts — it refunds, files, sends, books and writes to production —
> while oversight tooling is still built for the answering era: score the text, chart the
> failure, review the log next week. ControlPlane treats every response as a set of **claims
> requesting permission to act**. It captures the evidence the model was actually given at
> context-assembly time, with source identity and access rights attached, binds each claim in the
> output back to a specific span of that evidence, and refuses to let an unproven claim cross
> into an action. Verification effort is priced by what the response is about to do: a draft is
> checked cheaply, a payment is not. Performance, cost and responsibility stop being three tools
> and become **three reads of one graph — STEP → SPAN → CLAIM → ACTION.** This matters now
> because the cost of a wrong AI output has changed category: **it used to be a bad paragraph. It
> is now an executed transaction.**

**Spoken 30-second cut** *(the full paragraph runs ~70s aloud — never read it verbatim)*:

> "ControlPlane is an admission-control layer for AI. Enterprises moved from AI that answers to
> AI that acts — it refunds, files, sends, writes to production — but oversight is still built
> for the answering era. We treat every response as a set of claims requesting permission to act,
> bind each claim to the evidence the model was actually given, and refuse to let an unproven
> claim cross into an action. Because the cost of a wrong output has changed category: it used to
> be a bad paragraph. It's now an executed transaction."

**Page version** *(where space is tight — tighter on the page, weaker in the mouth)*:

> …binds each claim back to a specific span of that evidence, and refuses to let an unproven
> claim cross into an action. **Verification effort is priced by blast radius.** Performance,
> cost and responsibility stop being three tools and become three reads of one graph.

The category noun is **admission-control layer**. Not "verification proxy," not
"execution-boundary layer," not "observability."

---

## 3. What the market does — and why each fails

**LLM-as-judge.** *(NeMo Guardrails, most "AI safety" wrappers.)* A second model is asked whether
the first was right — usually without the source documents, always without knowing who was
asking. It produces an opinion using the same reasoning that produced the error, from the same
family of blind spots. It cannot state its own error rate, and it is too slow to stand in front
of an action.

> The judge asks **"does this look right?"** — an unfalsifiable question.
> We ask **"which span proves it?"** — a query with an answer.

**Static guardrails.** *(LlamaGuard, Lakera, regex and deny-lists.)* They match banned surface
forms. A fabricated invoice number, a salary leaked from an over-permissioned index, and a
correct answer are all lexically clean, so guardrails see none of them. And they are
**identity-blind**: the same string is fine for one caller and a breach for another.
Deterministic entitlement checking is not a better classifier — it is a different question.

**Post-hoc observability.** *(LangSmith, Helicone, Arize, WhyLabs.)* Beautifully engineered,
exactly the wrong product. They tell you what went wrong after a user acted on it — the precise
thing the brief asks to eliminate. Observation without execution control is an audit trail, not
architecture. They also measure spend rather than waste:

> A dashboard can tell you the trace cost **₹8**. It cannot tell you that **₹5 of it grounded
> nothing** in the final answer. Walking the graph backward can — because the graph that verifies
> is the graph that accounts.

**Confidence thresholding.** Logprobs, self-reported certainty, verbalised hedging. This fails by
definition: the named failure mode is *confidently* wrong. **You cannot detect a calibration
failure with the calibration.**

**RAG groundedness checkers.** The closest cousin, structurally short in three ways. They see
**retrieval only** — not tool results, DB rows, computed values or system context, which is where
agents actually get their facts. They **average**, so one wrong figure drowns in nine correct
sentences. And they are **action-blind**, so 0.82 means the same thing on a draft and on a wire
transfer.

> **Retrieval is not permission.**

**Composite risk scores.** *(Azure AI Content Safety, Bedrock Guardrails.)* "Trust: 87/100."
Three failure modes with three different owners, costs and remedies, collapsed into one number
that maps to no intervention. **You cannot block, edit or escalate on 87.**

**What all six share:** they inspect the output, not the context contract. They score the text
rather than verify the claim. They gate on words rather than on actions. **And not one of them
publishes its own false-negative rate.**

> Naming real products is itself a differentiator — nobody else in the room will name names.

---

## 4. Differentiation

| Common approach | ControlPlane |
|---|---|
| **Score the output** — a judge or groundedness model forms an opinion about finished text | **Query the evidence** — the verdict is a lookup against spans captured before the model ran, with source and ACL attached. Not an opinion formed after the fact; a binding that either exists or doesn't. |
| **Monitor and alert** — traces, dashboards, weekly review | **Interlock in the commit path** — text streams optimistically; actions do not proceed without proof. The output is a decision, not a chart. The same graph also prices the waste. |
| **Flag what looks wrong; default is allow** | **Default is UNSUPPORTED** — the claim carries the burden of proof. Nothing passes because nobody objected. |
| **One threshold, one score, all traffic** | **Blast radius × verdict severity** — the identical verdict annotates a draft and holds a payment. Budget is spent where the harm is, which is also why it stays fast. |
| **Publish precision** — the rate at which the tool bothers the user | **Publish our own per-route false-negative rate** — the rate at which we *missed*. The plane is audited by the standard it enforces. |

> The sharpest framing of the last row: *"They publish precision — the rate at which they bother
> the user. We publish the rate at which we missed."*

---

## 5. What we refuse to claim

Four refusals, about **ourselves** — not about competitors. This is the rarer and stronger move:
every deck in the room disclaims its rivals; almost none disclaim themselves.

**"We eliminate hallucinations."** Anyone who has shipped knows this is false, and it invites the
one question that ends the pitch: *then what's your miss rate?* We claim something narrower and
much harder to attack — ungrounded claims cannot authorise actions, and we report what we miss.

**"Model-agnostic, zero integration, drop it in."** We hook context assembly. That is real
integration work, and it is the exact reason the design works. **The integration cost is the
moat — say it out loud.** Trading our strongest structural claim for a weaker convenience claim
is a bad trade. *(Corollary: we don't claim a proprietary safety-trained model either. We sit on
top of yours.)*

**"Zero added latency."** Nobody believes it and we don't need it. The honest version is
stronger: **we never make the model feel slow; we make the action wait.**

**"99% accuracy detecting bias, safety and risk."** One accuracy number across three
incommensurable failure modes is a demo artifact — and any figure we cannot reproduce on their
traffic becomes a liability the first time they test it.

---

## 6. The narrative risk, and the correction

**The risk:** judges pattern-match this to "another AI safety tool" inside the first twenty
seconds, and everything after is heard as a variant of decks they have already sat through. The
architecture never gets evaluated on its merits.

**The trigger is specific: any opening that starts from risk.** *"AI is powerful but risky, and
here's how we make it safe"* is the first line of every guardrail deck in the room, and it sets
the frame before you have said anything of your own.

### Four corrections

**1 · Open on a blocked transaction, never on risk.** The first thing on screen is a specific
action with a rupee figure attached that did or did not happen. This is an authorisation system
that happens to catch errors, not a safety system that happens to have a gate. Lead with the
interlock; the danger is implied by the money. **Never open on a person** — no shocked customer,
no angry email. Open on a transaction.

**2 · Ban the vocabulary.** *(Four of seven proposals converged on this independently.)*

| Never say | Say instead |
|---|---|
| monitors, observes, detects, watches, guards | authorises, admits, proves, binds, refuses, gates |
| trust score, risk score, safety score | verdict, binding, entitlement, blast radius |
| observability layer, guardrail | admission-control layer, permission layer |
| responsible AI, ethics, trustworthy | deterministic entitlement check, ACL violation |

The first sentence must contain the word **"claim,"** not "response." **"Safety" may appear only
*after* "deterministic entitlement check" — never as a standalone virtue.** The brief says watch,
catch, act: say plainly that watching and catching are commoditised and we compete on the third.

> **One deliberate exception:** *"Everyone watches the exit. Nobody records the entrance."* —
> permitted, because it indicts what everyone else built. A total ban would cost us the best line
> we have.

**3 · Run one trace end to end.** The same refund appears in the hook, the mechanism, the matrix
and the closing line. Generic decks cycle through three shallow scenarios; following one case to
the bottom is what reads as production experience. Breadth reads as slideware; depth reads as
someone who has run this in anger.

**4 · Position as infrastructure, not ethics.** The reference class is a firewall, a transaction
validator, **the CPU's privilege mode** — not an AI-safety wrapper. Cold, structural,
graph-shaped language throughout.

### The ship test

> If a judge could summarise it as *"it watches AI outputs and flags problems,"* the narrative has
> failed regardless of the architecture underneath. Rewrite until that sentence no longer fits.

---

## 7. The lines that carry weight

Ranked by how much work each does. These survived seven-model adversarial scoring at 49–50/50.

**The stakes**
> It used to be a bad paragraph. It is now an executed transaction.

**The indictment** *(the hook's button)*
> The system didn't fail. It was never asked to prove anything.

**The reframe** *(the hinge of the whole argument)*
> Everyone watches the exit. Nobody records the entrance.

**The thesis**
> An AI response is not text to be scored. It is a set of claims requesting permission to act.

**The mechanism, in one line**
> Not low confidence. Unproven.

**The one-graph proof**
> Everywhere else that's three products. Here it's three questions on one graph.

**The decision principle**
> Proof scales with consequence.

**The credibility play**
> We publish our own miss rate. Per route. Not what we caught — what we missed.

**The close** *(answers the hook exactly — first and last claim, negated then resolved)*
> That system was never asked to prove anything.
> *[hold]*
> Now nothing acts until it can prove it should.

### Script discipline

**Every line must name a claim, a graph, an action or a measurement — or it gets cut.** Any
sentence that only says "the AI" or "the response" in the abstract goes. That rule alone is why
this doesn't sound like the other fifty pitches.

**If a line could survive being moved into a different company's video, it was cut.**

---

## 8. Two traps

**Do not drop bias.** One proposal recommended cutting bias entirely and speaking only about data
exfiltration, on the grounds that it sounds more like engineering. **The brief names bias
explicitly** under responsibility; omitting it scores against the rubric. Keep it and state it in
*measurement* terms, never moral ones: **counterfactual flip rate with a confidence interval,
route-level, async.** If a judge asks about bias, that sentence is the whole answer — it is more
rigorous than anything a fairness-dashboard team will say, and it never leaves engineering
register.

**Never say "blocked" about the refund.** The matrix routes R3 × unsupported-categorical to
Escalate. Say *held and escalated with the evidence packet*. Spoken word and grid must agree —
this was corrupted at four separate stages by five different models.
