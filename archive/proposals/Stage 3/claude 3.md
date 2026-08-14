# Stage 3 — Differentiation & Narrative Spine

## 1. Single Sharp Insight

Every AI oversight product inspects the model's output, but the only thing that can prove an output true is the evidence assembled *before* the model ran — and that record is discarded the moment generation starts. ControlPlane captures it outside the model, which turns hallucination detection from a judgment call into a set-membership test, and turns oversight from scoring text into authorizing actions.

---

## 2. What the Market Currently Does — and Why Each Fails Against This Design

**LLM-as-judge.** A second model is asked whether the first was right, usually without the source documents and always without knowing who was asking. It produces an opinion using the same reasoning that produced the error, from the same family of blind spots. It cannot state its own error rate, and it is too slow to stand in front of an action. The judge asks *"does this look right?"* — an unfalsifiable question. ControlPlane asks *"which span proves it?"* — a query with an answer.

**Static guardrails.** Deny-lists, regex, policy classifiers over text. They match banned surface forms. A fabricated invoice number, a salary leaked from an over-permissioned index, and a correct answer are all lexically clean, so guardrails see none of them. They are also identity-blind: the same string is fine for one caller and a breach for another. Deterministic entitlement checking is not a better classifier — it is a different question entirely.

**Post-hoc observability dashboards.** Traces, spans, eval runs, weekly review. They tell you what went wrong after a user acted on it — precisely the thing the brief asks to eliminate. An artifact you read is not a control. They also measure spend rather than waste: a dashboard can say a trace cost ₹8; it cannot say that ₹5 of it grounded nothing in the final answer. Walking the graph backward can, because the graph that verifies is the graph that accounts.

**Confidence thresholding.** Logprobs, self-reported certainty, verbalized uncertainty. This fails by definition: the named failure mode is *confidently* wrong. You cannot detect a calibration failure with the calibration. Fluent, high-probability fabrication is the modal enterprise incident, and it sails past every confidence gate. ControlPlane never reads confidence — it reads assertion strength against grounding deficit.

**Simple RAG groundedness checkers.** The closest cousin, and structurally short in three ways. They see retrieval only — not tool results, DB rows, computed values, or system context, which is where agents actually get their facts. They average, so one wrong figure drowns in nine correct sentences. And they know nothing about the pending action, so 0.82 means the same thing on a draft and on a wire transfer. Their default is *supported unless suspicious*; ours is UNSUPPORTED until proven, with worst-claim-governs and the verdict priced against blast radius.

**Composite risk scores.** "Trust: 87/100." Three failure modes with three different owners, costs, and remedies collapsed into one number that maps to no intervention. You cannot block, edit, or escalate on 87. We keep the axes separate because each drives a different actuator — and we can afford to, because all three read off one graph.

---

## 3. Positioning Statement

ControlPlane.ai is an admission-control layer for AI systems. Enterprises have moved from AI that answers to AI that acts — it refunds, files, sends, books, and writes to production — while oversight tooling is still built for the answering era: score the text, chart the failure, review the log next week. ControlPlane treats every response as a set of claims requesting permission to act. It captures the evidence the model was actually given at context-assembly time, with source identity and access rights attached, binds each claim in the output back to a specific span of that evidence, and refuses to let an unproven claim cross into an action. Verification effort is priced by what the response is about to do: a draft is checked cheaply, a payment is not. Performance, cost, and responsibility stop being three tools and become three reads of one graph — STEP → SPAN → CLAIM → ACTION. This matters now because the cost of a wrong AI output has changed category: it used to be a bad paragraph. It is now an executed transaction.

---

## 4. Differentiation Table

| Common approach | ControlPlane |
|---|---|
| **Score the output** — a judge or groundedness model forms an opinion about finished text | **Query the evidence** — the verdict is a lookup against spans captured before the model ran, with source and ACL attached. Not an opinion formed after the fact; a binding that either exists or doesn't. |
| **Monitor and alert** — traces, dashboards, weekly review | **Interlock in the commit path** — text streams optimistically; actions do not proceed without proof. The output is a decision, not a chart. The same graph also prices the waste: we can name the exact spend that grounded nothing. |
| **Flag what looks wrong; default is allow** | **Default is UNSUPPORTED** — the claim carries the burden of proof. Nothing passes because nobody objected. |
| **One threshold, one score, all traffic** | **Blast radius × verdict severity** — the identical verdict annotates a draft and blocks a payment. Verification budget is spent where the harm is, which is also why it stays fast. |
| **Claim detection accuracy** | **Publish our own per-route false-negative rate** — the plane is audited by the standard it enforces. We state what we miss. |

---

## 5. Narrative Spine — 3:00

**0:00–0:30 — Hook. One screen, one transaction.**
An agent's output: *"Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement."* Beat. Clause 7.2 does not exist. Every guardrail passed it — nothing was toxic, nothing was off-policy, confidence was 0.94. The money moved on a Tuesday and it was found on a Friday. Land it: **"The system didn't fail. It was never asked to prove anything."**

**0:30–1:15 — Problem, then reframe.**
The failure category changed: AI stopped answering and started acting. Oversight didn't move with it. Fast sweep, ten seconds, no survey: a judge gives you an opinion, a guardrail checks surface forms, a dashboard tells you on Friday, and confidence is the instrument that's broken. Then the structural point — the evidence that could have caught this existed *before* the model ran, at context assembly, and nobody is standing there. **Everyone watches the exit; nobody records the entrance.** The reframe: an AI response is not text to be scored, it is a set of claims requesting permission to act. Put the graph on screen once: STEP → SPAN → CLAIM → ACTION.

**1:15–2:15 — Mechanism and the three-axis read. Same refund trace, all the way down.**
Provenance captured outside the model: 14 spans, each with source ID, hash, ACL. The response decomposes into 6 claims — all six start red, because the default is UNSUPPORTED. Five turn green as spans prove them. *"Clause 7.2 permits this refund"* finds no span. It stays red. Not low-confidence — **unproven**.
Then the same graph, three questions:
- **Performance** — one unproven categorical claim, and it is the one authorizing the payment. Worst claim governs.
- **Responsibility** — one span that *did* ground a claim came from a document whose ACL excludes the caller. Deterministic. No classifier was involved.
- **Cost** — walk the graph backward: of 9 tool calls in this trace, 4 produced spans that ground nothing in the answer. Measured, not estimated.

Land it: **"Everywhere else that's three products. Here it's three queries — because it's the same graph."**

**2:15–2:45 — Why it doesn't over-block.**
The matrix, on screen for two seconds: blast radius R0–R3 against verdict severity. The identical unproven claim annotates a draft, gets stripped from a read-only answer, and blocks a payment. Edits are surgical — strip the claim or force re-grounding on the named span, never a rewrite, because a rewrite is a new unverified artifact. Escalation ships the claim, the candidate spans, and the verdict, so a human resolves in seconds rather than triaging a severity colour. Latency: text streams with a short hold-back, and the hard gate sits on the action, not the tokens — users feel the model's speed; the gate sits where the money moves. Then the credibility line: **we publish our own false-negative rate, per route.**

**2:45–3:00 — Close. Answer the hook exactly.**
**"That model never had to prove anything. Now it does — and when it can't, the money doesn't move."**
*(Title card, if one is needed: "ControlPlane — proof before permission." Optional; the spoken line is stronger alone.)*

---

## 6. What We Deliberately Refuse to Claim

**"We eliminate hallucinations."** Anyone who has shipped knows this is false, and it invites the one question that ends the pitch: *then what's your miss rate?* We claim something narrower and much harder to attack — ungrounded claims cannot authorize actions, and we report what we miss.

**"Model-agnostic, zero integration, drop it in."** We hook context assembly. That is real integration work, and it is the exact reason the design works. Trading our strongest structural claim for a weaker convenience claim is a bad trade. The integration cost is the moat; say it out loud.

**"Zero added latency."** Nobody believes it, and we don't need it. The honest version is stronger: verification is budgeted, not free — deterministic checks inline in tens of milliseconds, expensive checks only where blast radius justifies them, and the hard gate in front of the action rather than the tokens.

**"99% accuracy detecting bias, safety, and risk."** One accuracy number across three incommensurable failure modes is a demo artifact, and any figure we cannot reproduce on their traffic becomes a liability the first time they test it.

---

## 7. Strongest Narrative Risk + Exact Correction

**The risk:** judges pattern-match this to "another AI safety tool" inside the first twenty seconds, and everything after that is heard as a variant of decks they've already sat through. The architecture never gets evaluated on its merits. The trigger is specific — **any opening that starts from risk.** *"AI is powerful but risky, and here's how we make it safe"* is the first line of every guardrail deck in the room, and it sets the frame before you've said anything of your own.

**The correction, three moves:**

**Open on a blocked transaction, never on risk.** The first thing on screen is a specific action with a rupee figure attached that did or did not happen. This is an authorization system that happens to catch errors — not a safety system that happens to have a gate. Lead with the interlock; the danger is implied by the money.

**Ban the vocabulary.** No *monitors, observes, detects, guards, trust score, risk score.* Use *authorizes, admits, proves, binds, refuses.* Verbs of permission, not verbs of watching. The brief says watch, catch, act — say plainly that watching and catching are commoditized and we are competing on the third.

**Run one trace end to end.** The same refund appears in the hook, the mechanism, the decision matrix, and the closing line. Generic decks cycle through three shallow scenarios; following one case to the bottom is what reads as production experience. Breadth reads as slideware; depth reads as someone who has actually run this in anger.

**The ship test:** if a judge could summarize the deck as *"it watches AI outputs and flags problems,"* the narrative has failed regardless of the architecture underneath. Rewrite until that sentence no longer fits.