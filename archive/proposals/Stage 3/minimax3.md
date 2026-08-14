# ControlPlane.ai — Positioning & Narrative Spine

One framing rule I'm holding to before I write a word: every line in this document must reference a claim, an evidence graph, an action, or a measurement. If a sentence only talks about "the AI" or "the response" in the abstract, it gets cut. That discipline is the whole reason this won't sound like the other 50 pitches judges saw today.

---

## 1. Single Sharp Insight

**The category of "AI safety" tools treats the model output as text; ControlPlane treats it as a graph of claims requesting permission to act, and gates the action against the evidence the model was actually given — not against a re-judged copy of the text.** This single unit-of-analysis shift (claim, not response) is what makes one plane read all three axes honestly instead of collapsing them into a number.

---

## 2. What the market currently does (and why each fails)

**LLM-as-judge** (NeMo Guardrails, most "AI safety" wrappers) — uses another language model to score the first one. Circular (same blind spots), slow (300ms–2s), expensive, and famously disagrees with humans on the cases that matter. Fails because it inherits the model's epistemology.

**Static guardrails** (regex PII filters, deny-lists, keyword blocks, Lakera-style pattern matchers) — string matching on output text. Catches the obvious 20%, misses the structural failure (a confidently-wrong claim with no strings to match), and breaks on every prompt-injection variant. Fails because it treats text as text.

**Post-hoc observability dashboards** (LangSmith, Helicone, Arize, WhyLabs) — beautifully engineered, exactly the wrong product. They show you what already happened to a user. The brief says "find it first, not find out." Fails because it is a monitor, not a control plane.

**Confidence thresholding** (model routers, some RAG query engines) — "model said 0.9, ship it." Confidence is a calibration artifact, not a correctness artifact. Models are confidently wrong routinely; that's literally the failure mode the brief names. Fails because it confuses the model's verbal hedge with the evidence it had.

**Simple RAG checkers** (citation faithfulness, retrieval-match score) — only catch one axis, and only when the evidence happens to live in a vector store. The real evidence contract is the entire context assembly — system prompt, retrieved docs, tool outputs, ACL, hashes — none of which a retrieval score sees. Fails because it measures one input, not the context graph.

**Composite risk scores** (Azure AI Content Safety, AWS Bedrock Guardrails, most enterprise "responsible AI" suites) — collapse three axes into one number on a 0–1 scale. The user can't act on it, the policy can't decompose it, and the decision is unreviewable by a human. Fails because it is the antithesis of a *control* plane.

**What all six share:** they look at the output, not the context contract. They score the text, not verify the claim. They block on words, not on actions. And not one of them publishes its own false-negative rate.

---

## 3. Positioning Statement

> **ControlPlane.ai is the verification layer that sits between any AI model and the actions it triggers. We treat every response not as text to be scored but as a set of claims requesting permission to act, and we bind each claim to the evidence the model was actually given — captured at context-assembly time, not inferred after the fact. By inverting the burden of proof, walking the evidence graph backward to expose dead compute, and gating actions instead of text, we catch the confidently-wrong, the quietly-expensive, and the subtly-unsafe on the same plane. And we publish our own per-route false-negative rate — because a control plane that doesn't measure itself is just another monitor.**

Verbatim-ready for Slide 1 or the first 25 seconds. Read it once aloud. If it doesn't make a judge who has seen fifty of these pitches lean forward, cut a clause.

---

## 4. Differentiation Table

| Common approach | What it actually does | Why ControlPlane is fundamentally different |
|---|---|---|
| **LLM-as-judge** | Re-scores the response with another LLM | We don't score outputs; we verify claims against the evidence captured at context assembly — outside the model, with ACL and hash |
| **Static guardrails** | String/pattern match on the response | We gate the **action** against the claim graph, not the text; the structural failure has no string to match |
| **Post-hoc observability** | Dashboards for what already happened | We gate at context assembly, before the claim is ever released; the plane is a write-path component, not a read-path tool |
| **Confidence thresholding** | "Model said 0.9, ship it" | We measure **evidence density per claim**, not verbal hedge; the confidently-wrong case is exactly what confidence misses |
| **Composite risk score** | One 0–1 number across three axes | We use a **Blast Radius × Verdict Severity** matrix — every decision is decomposable, reviewable, and appealable |

---

## 5. Narrative Spine — 3-minute video

**0:00–0:30 — Opening hook**
"Every AI safety pitch you've heard this week starts the same way: here is a model, here is a thing it said, here is a score we gave it. We started somewhere else. We started at the *context contract* — the place where evidence is given to the model — and we asked a different question. Not *is this text safe?* but *does this claim have permission to act?*"
*[Visual: a single response on screen, then exploded into a graph — STEP → SPAN → CLAIM → ACTION — with evidence pointers feeding back.]*

**0:30–1:15 — Problem + reframe**
"Three failure modes. Confidently wrong: a model that cites a number that isn't in the source, with high verbal confidence and zero structural backing. Quietly expensive: a model that re-asks the same thing four times because the evidence never closed the loop. Subtly unsafe: a model that walks a request one step past the ACL boundary. The industry treats these as three different problems on three different dashboards. They're not. They're three reads of the same graph. STEP into SPAN, SPAN into CLAIM, CLAIM into ACTION. Performance is the read of evidence-to-claim. Cost is the read of how much of the graph actually drove the action. Responsibility is the read of what the action could touch."
*[Visual: the same response animated three times, each time highlighting one axis, showing the graph underneath is identical.]*

**1:15–2:15 — Core mechanism + three-axis demo**
"Here's the mechanism. At context assembly — before the model ever speaks — we capture provenance. Every source, every tool output, every ACL boundary, every hash. The model doesn't see the plane; the plane sees the contract. The model emits claims. We default each claim to UNSUPPORTED — the burden of proof is inverted. Then we walk the graph. For performance: how dense is the evidence behind each claim? For cost: walking *backward* from the action, how much of the emitted compute never reached a claim that drove a decision? That's dead compute, measured exactly. For responsibility: deterministic ACL and entitlement checks on the action, not on the text."
*[Visual: live demo, one response, three numbers emerging from the same graph — one slide per axis, then overlaid.]*

**2:15–2:45 — Decision logic / why it doesn't over-block**
"Now — the part that decides whether anyone turns this on. We don't gate the text. We gate the **action**. Text streams optimistically with a short hold-back; only the action waits for the verdict. And the verdict isn't a number. It's a position in a matrix: Blast Radius R0 to R3, crossed with Verdict Severity. R0 plus supported claim plus read-only action: pass. R2 plus unsupported claim plus write action: surgical edit, or escalate, with the full evidence packet shipped to the human. Block is reserved for the corner where blast radius and unsupported severity both peak. That's why this doesn't over-block. Most of the time, the answer is *pass with audit*, not *block*. The plane prefers friction-free to paranoid."
*[Visual: the 4×4 matrix on screen, lighting up only a few cells in a typical run.]*

**2:45–3:00 — Closing line (must land)**
"One more thing, and this is the line that decides whether we're a tool or a control plane. We publish our own per-route false-negative rate. Public. Per route. Updated continuously. Every other product in this category publishes precision — the rate at which it bothers the user. We publish the rate at which we *missed*. Because a control plane that doesn't measure itself is just another monitor. And the difference between finding out and finding it first is the only thing that matters."
*[Visual: a live dashboard, FN rate per route, ticking.]*

---

## 6. What we deliberately refuse to claim

These are the lines that sound strong and will lose serious judges. Do not put them in the deck.

1. **"We catch every confidently-wrong response."** No system does, and any judge who has shipped one knows it. The honest claim is: *we make the catch-rate measurable per route and force the policy to face it*. That is a stronger claim and a defensible one.

2. **"We replace human review."** We do the opposite and we say so: every escalation ships a structured evidence packet, because the human is the highest-trust verifier in the loop. Anyone who says they replaced the human is selling a demo.

3. **"Latency is zero / we add no overhead."** We add latency. We add it to the *action*, not the *text*. The honest line: *we never make the model feel slow; we make the action wait*. The moment a judge hears "zero overhead" they stop believing the rest.

4. **"One risk score, simple."** Composite scores are the failure mode of the entire category. Naming the matrix (Blast Radius × Verdict Severity) is the differentiator. Collapsing it to a number is the giveaway that we are the same product wearing different clothes.

---

## 7. Strongest narrative risk + exact correction

**Risk:** the story collapses into "another AI safety tool" before the first 60 seconds are out. The category is saturated, the judges have seen it, and the default reading of any new entrant in this space is *probably the same as the last one*. Every word in the deck competes against that prior.

**Correction — three disciplined moves, in order:**

1. **The first sentence of the deck must contain the word "claim," not "response."** This is the reframe and it has to land before the audience categorizes you. If the first sentence says "AI response," you have already lost. The thesis sentence above is the one to use.

2. **Every visual must show the same graph three times, not three separate dashboards.** The single most powerful moment in the narrative spine is the one where the same response is re-read for performance, cost, and responsibility and the audience realizes they are looking at the *same* structure. Three side-by-side charts is the wrong slide. One graph, three highlight passes, is the right one.

3. **The closing line must name the false-negative rate, not the precision.** Precision is what monitors publish. False-negative rate is what control planes publish. This is the line that separates a product from a category. If you can't defend that number publicly, you don't have a control plane, you have a dashboard with confidence.

If a slide doesn't earn its place against those three moves, it gets cut. Three slides is not a lot of room. Spend it on the reframe, the unified graph, and the self-measured FN rate. The rest is supporting evidence.

---

If you want, I'll save this as a working doc in your workspace so you can hand it to a slide designer without re-pasting. And if you want a stress-test before Round 2 — three reviewers, one playing an Accenture architect who's seen this category saturated, one playing a security lead who'll push on ACL and the false-negative claim, one playing a finance lead who'll push on the cost math — I can spin that up in about 10 minutes. Your call.