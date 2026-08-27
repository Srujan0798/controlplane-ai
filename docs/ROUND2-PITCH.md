# ControlPlane.ai — Round 2 Pitch Outline

**Accenture Innovation Challenge 2026 · Problem Track 1 · Team ControlPlane**  
Choda Srujan Sai · Dhrithika — IIT Gandhinagar

Speaker-ready. 12 slides. ~8–10 minutes if spoken as written. Live stand script: [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md).

> **Speak-from canon:** [round2/R2S5.md](../round2/R2S5.md). This file is the slide outline; R2S5 is the demo spine.  
> Companion to the frozen system of record: [ARCHITECTURE.md](ARCHITECTURE.md).  
> Spoken lines: [NARRATIVE.md](NARRATIVE.md) §7. Business case: [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md).  
> Hostile Q&A: [QA.md](QA.md). Prototype: `python3 examples/refund_trace_demo.py` and `python3 examples/multi_usecase_demo.py`.

This file is a rendering. It does not reopen architecture.

**One trace, start to close.** The ₹1,84,000 refund is the hook, the mechanism, the matrix and the last line. Do not cycle through three shallow scenarios.

**Live cold open (R2S5):** room machine boots on the held R3 panel (`HELD — ESCALATE` · `executed: false`), not a title slide. Deck slide 1 is optional chrome for remote/PDF; in the room, open on the gate.

**Script discipline** ([NARRATIVE.md](NARRATIVE.md) §7): every spoken line names a claim, a graph, an action or a measurement — or it is cut.

---

## How to use this file

| Block | Meaning |
|---|---|
| **On screen** | What the slide shows. Short. |
| **Say** | Spoken script. Load-bearing lines from [NARRATIVE.md](NARRATIVE.md) §7 are in **bold** and must be said verbatim. |
| **Do not say** | Content-law traps ([ARCHITECTURE.md](ARCHITECTURE.md) §10). |
| **Backing** | Prototype output or architecture citation for every claim on the slide. |

Timing in brackets is a ceiling, not a quota.

---

## Slide 1 — Title

**~15s**

### On screen

**ControlPlane.ai**  
Admission-control layer for AI that acts

Accenture Innovation Challenge 2026 · Round 2 · Track 1  
Choda Srujan Sai · Dhrithika — IIT Gandhinagar

`STEP → SPAN → CLAIM → ACTION`

### Say

> ControlPlane is an admission-control layer for AI. Enterprises moved from AI that answers to AI that acts. We authorise the action. We do not score the paragraph.

### Do not say

- "AI is powerful but risky" — never open on risk ([NARRATIVE.md](NARRATIVE.md) §6).
- "observability layer", "guardrail", "safety tool" as *our* category. The category noun is **admission-control layer**.
- Names of people as the hook. Open on a transaction (next slide).

### Backing

- Category noun: [NARRATIVE.md](NARRATIVE.md) §2.
- Primitive on the title so the graph is visible before the argument starts: [ARCHITECTURE.md](ARCHITECTURE.md) §2.

---

## Slide 2 — Problem: answers → actions

**~50s**

### On screen

Ungated output:

> Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.

Confidence 0.94. Every filter passed it.  
Money moved Tuesday. Found Friday.

**Clause 7.2 does not exist.**  
The company wrongly paid ₹1,84,000.

**It used to be a bad paragraph. It is now an executed transaction.**

### Say

> A refund agent emitted that sentence. Confidence point-nine-four. Money moved Tuesday, found Friday. Clause 7.2 does not exist. The company wrongly paid one lakh eighty-four thousand rupees.
>
> **The system didn't fail. It was never asked to prove anything.**
>
> Oversight is still built for the answering era: score the text, chart the failure, review the log next week. The cost of a wrong output changed category. **It used to be a bad paragraph. It is now an executed transaction.**

### Do not say

- The customer lost money. The company paid it ([ARCHITECTURE.md](ARCHITECTURE.md) §10.3).
- "The refund was denied."
- "Clause 7.2 caps / denies / doesn't cover." The clause **does not exist**.
- Open on a shocked customer or an angry email. The first thing on screen is a transaction with a rupee figure ([NARRATIVE.md](NARRATIVE.md) §6.1).

### Backing

- Ungated sentence, amount, clause absence: [ARCHITECTURE.md](ARCHITECTURE.md) §9; prototype `UNGATED_RESPONSE` in `controlplane/scenarios/refund.py`; `python3 examples/refund_trace_demo.py`.
- Stakes and indictment lines: [NARRATIVE.md](NARRATIVE.md) §7.
- Thesis of the category error: [ARCHITECTURE.md](ARCHITECTURE.md) §1; [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) §1.

---

## Slide 3 — Insight: receipts, not the model's mind

**~40s**

### On screen

**Everyone watches the exit. Nobody records the entrance.**

We read the model's receipts, not the model's mind.

The verdict is a **set-membership test** against evidence captured *before* generation — not an opinion about finished text.

Default verdict: **UNSUPPORTED**. A claim must earn SUPPORTED.

### Say

> Every oversight tool inspects what the model said. The only thing that can prove it is the evidence assembled before the model ran — and that record is thrown away the moment generation starts.
>
> **Everyone watches the exit. Nobody records the entrance.**
>
> ControlPlane keeps the receipts. That turns hallucination checking from a judgment call into a set-membership test, and turns oversight from scoring text into authorising actions.

### Do not say

- "we detect hallucinations" as the product.
- "we read the model's mind / hidden states / logits." We sit at the I/O layer ([ARCHITECTURE.md](ARCHITECTURE.md) §5.10; [QA.md](QA.md) B1).

### Backing

- Insight and the phrase **set-membership test**: [NARRATIVE.md](NARRATIVE.md) §1. Load-bearing — do not drop it for brevity.
- Reframe line: [NARRATIVE.md](NARRATIVE.md) §7 (the one permitted use of "watches").
- Default UNSUPPORTED: [ARCHITECTURE.md](ARCHITECTURE.md) §3; `controlplane/binder.py`.

---

## Slide 4 — Primitive: STEP → SPAN → CLAIM → ACTION

**~50s**

### On screen

```
  STEP ──produces──▶ SPAN ──binds──▶ CLAIM ──authorizes──▶ ACTION
 (tool call,       (retrieved chunk,   (typed atomic      (pending side
  retrieval,        tool row, DB        proposition        effect: tool +
  model turn)       record — source,    from the output     args +
                    ACL, hash,          stream)             irreversibility)
                    offsets)
```

| Read | Question |
|---|---|
| **Performance** → | Does each claim bind to a span? |
| **Cost** ← | Did each step ground any accepted claim? |
| **Responsibility** | Is the caller entitled to every span a claim binds to? |

Keystone: **Provenance Recorder** — hooks context assembly, not the model.

**Everywhere else that's three products. Here it's three questions on one graph.**

### Say

> **An AI response is not text to be scored. It is a set of claims requesting permission to act.**
>
> We capture every span at context assembly — source, ACL, hash, offsets — then freeze. The model cannot invent a span after the fact, and it has no channel to declare a binding. Performance reads the graph forward. Cost reads it backward. Responsibility reads the labels.
>
> **Everywhere else that's three products. Here it's three questions on one graph.**

### Do not say

- "three classifiers", "three detectors bolted together."
- "model-emitted citations." Rejected: a model that fabricates a fact fabricates the citation ([ARCHITECTURE.md](ARCHITECTURE.md) §8).

### Backing

- Graph, three reads, keystone: [ARCHITECTURE.md](ARCHITECTURE.md) §2, §12.
- Thesis and one-graph lines: [NARRATIVE.md](NARRATIVE.md) §7; [ARCHITECTURE.md](ARCHITECTURE.md) §1.
- Prototype implements Lane 1 of this graph on fixtures: Provenance Recorder, binder, entitlement, interlock, hash-chained ledger. Not the proxy, not the 1–3B extractor, not NLI ([ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) Appendix A.3).

---

## Slide 5 — Demo beat 1: clause 7.2 is UNSUPPORTED

**~45s**

Live if possible: `python3 examples/refund_trace_demo.py` — freeze on Claims / bindings.

### On screen

Claim `clause_72`: **"Clause 7.2 permits this refund"**  
kind=structural · assertion=**categorical** · role=`issue_refund`, `show_text`

Five spans at context assembly. **No span for clause 7.2.**

| claim_id | verdict | spans |
|---|---|---|
| approval, amount, order, vendor_41, hr_side | SUPPORTED | span-1 / span-2 / span-3 |
| **clause_72** | **UNSUPPORTED** | **(none)** |

Absence of evidence, not conflicting evidence.

**Not low confidence. Unproven.**

### Say

> The Provenance Recorder captured five spans before the model ran. Vendor agreement, order lookup, an HR note, FAQ, CRM. Clause 7.2 is in none of them, because clause 7.2 does not exist.
>
> The claim stays UNSUPPORTED. Not contradicted — there is nothing to contradict. **Not low confidence. Unproven.** The claim carries the burden of proof. Nothing passes because nobody objected.

### Do not say

- "contradicted", "caps", "denies", "doesn't cover" ([ARCHITECTURE.md](ARCHITECTURE.md) §10.1).
- "the model was unsure." Confidence is the broken instrument ([ARCHITECTURE.md](ARCHITECTURE.md) §3).

### Backing

Observed in `python3 examples/refund_trace_demo.py`:

```
clause_72     UNSUPPORTED   via fixture  spans=(none)
              Clause 7.2 permits this refund
Clause 7.2 does not exist.
  Absence of evidence, not conflicting evidence — the claim stays UNSUPPORTED.
```

Locked by `tests/test_refund_scenario.py::test_clause_72_is_absence_not_contradiction`.  
Architecture: [ARCHITECTURE.md](ARCHITECTURE.md) §3 (default UNSUPPORTED), §9, §10.1.

---

## Slide 6 — Demo beat 2: entitlement Edit on R1

**~45s**

Same demo, freeze on Entitlement findings + `show_text`.

### On screen

Pending action: **`show_text`** — show text to the customer · **R1** user-visible

Claim `hr_side`: "customer account flagged for goodwill override"  
SUPPORTED via `span-3` · source `doc:hr-exception-desk` · ACL `{hr-confidential}`

Principal `cs-agent-17` · clearance `{vendor-public}`

Entitlement: **VIOLATION** — span ACL is not a subset of caller clearance.

| Action | Cell | Actuator |
|---|---|---|
| `show_text` | **R1 × Contradicted / entitlement violation** | **Edit** — unentitled span stripped |

Retrieval is not permission.

### Say

> One of those five spans *did* bind. The HR internal note. The claim is true — it is in the evidence. The caller is a customer-support agent with vendor-public clearance. The span is hr-confidential.
>
> Deterministic entitlement check: the ACL is not a subset of the caller's clearance. On the customer-visible text path — R1 — the matrix says Edit. Strip the unentitled span. Surgical, never generative.
>
> This is the incident output-only checkers cannot see: they never carry who is asking.

### Do not say

- "safety" as a standalone virtue. It may appear only *after* "deterministic entitlement check" ([NARRATIVE.md](NARRATIVE.md) §6.2).
- "we detected a leak with a classifier." Entitlement is set-membership ([ARCHITECTURE.md](ARCHITECTURE.md) §3).
- "we fix their IAM." We stop the model silently bypassing the rights the source already carries ([QA.md](QA.md) B4).

### Backing

Observed in `python3 examples/refund_trace_demo.py`:

```
hr_side       VIOLATION   span ACL not subset of principal clearance  offending=span-3
show_text       R1 × Contradicted / entitlement violation  →  Edit
  actuator   Edit
  driving    hr_side, clause_72
```

Locked by `tests/test_refund_scenario.py::test_show_text_driven_by_entitlement`.  
Architecture: [ARCHITECTURE.md](ARCHITECTURE.md) §3 (leakage = set membership), §4 (R1 × entitlement → Edit), §9, §12 (entitlement is the most differentiated mechanism).  
"Retrieval is not permission": [NARRATIVE.md](NARRATIVE.md) §3.

---

## Slide 7 — Demo beat 3: Escalate the R3 refund

**~45s**

Same demo, freeze on `issue_refund`. **This is the resolution of slide 2.**

### On screen

Pending action: **`issue_refund`** — issue the refund · **R3** irreversible · ₹1,84,000 · ORD-9

Driving claim: `clause_72` · UNSUPPORTED · categorical

| Action | Cell | Actuator |
|---|---|---|
| `issue_refund` | **R3 × Unsupported + categorical** | **Escalate** |

**Held and escalated with the evidence packet.**  
Packet carries the unproven clause. `verify_chain() = True`

Same response, two actuators. Text edited. Money held.

**Proof scales with consequence.**

### Say

> Same response. Second pending action: issue the refund. R3, irreversible, one lakh eighty-four thousand rupees. The driving claim is still clause 7.2, still unproven, still categorical.
>
> The matrix says Escalate. Held and escalated with the evidence packet — the claim, the empty span list, the verdict. Not an alert. The hash chain verifies.
>
> The customer-visible line is edited. The payout is held. Both are correct at the same time. **Proof scales with consequence.**

### Do not say

- **"blocked"** about the refund. R3 × unsupported-categorical = Escalate ([ARCHITECTURE.md](ARCHITECTURE.md) §10.2; [NARRATIVE.md](NARRATIVE.md) §8). Spoken word and grid must agree.
- Invented actuators (`Hold & Re-verify`, `Redact & Flag`, `Kill Span`). Actuators are Block · Edit · Escalate · Pass ([ARCHITECTURE.md](ARCHITECTURE.md) §10.5).

### Backing

Observed in `python3 examples/refund_trace_demo.py`:

```
issue_refund    R3 × Unsupported + categorical  →  Escalate
  actuator   Escalate
  driving    clause_72
  packet
    clause_72: 'Clause 7.2 permits this refund'  verdict=UNSUPPORTED
  held and escalated with the evidence packet.
  Hash chain verify_chain() = True
```

Locked by `tests/test_refund_scenario.py::test_refund_held_not_blocked` and `test_dual_action_edit_and_escalate`.  
Architecture: [ARCHITECTURE.md](ARCHITECTURE.md) §4 matrix (transcribed), §9 two pending actions, §10.2.  
Decision principle: [NARRATIVE.md](NARRATIVE.md) §7.

---

## Slide 8 — Why not guardrails / RAG-only / confidence

**~50s**

### On screen

They inspect the output. We query the evidence.

| Common approach | Why it fails this refund |
|---|---|
| **Static guardrails** (LlamaGuard, regex, deny-lists) | A fabricated clause is lexically clean. Identity-blind: the same string is fine for one caller and a breach for another. |
| **RAG groundedness** | Sees retrieval only — not tool rows or system context. Averages, so one wrong figure drowns. Action-blind: 0.82 means the same on a draft and a wire. |
| **Confidence / logprobs** | The named failure is *confidently* wrong. **You cannot detect a calibration failure with the calibration.** |
| **LLM-as-judge** | Asks *"does this look right?"* — unfalsifiable. We ask *"which span proves it?"* |
| **Composite score** | "Trust: 87/100." **You cannot block, edit or escalate on 87.** |

Not one of them publishes its own false-negative rate.

### Say

> Guardrails match banned surface forms. Clause 7.2 is a well-formed sentence, so they admit it. Groundedness checkers average and cannot see who is asking, so they miss both the missing clause and the HR span. Confidence fails by definition: the failure mode is confidently wrong.
>
> The judge asks, does this look right? We ask, which span proves it?
>
> You cannot block, edit or escalate on eighty-seven.

### Do not say

- "we're a better guardrail." Category is admission-control ([NARRATIVE.md](NARRATIVE.md) §2).
- Skip naming products. Naming them is the differentiator ([NARRATIVE.md](NARRATIVE.md) §3).

### Backing

- Six-way market map: [NARRATIVE.md](NARRATIVE.md) §3.
- Rejected approaches: [ARCHITECTURE.md](ARCHITECTURE.md) §8.
- "You cannot block, edit or escalate on 87": [ARCHITECTURE.md](ARCHITECTURE.md) §8; [NARRATIVE.md](NARRATIVE.md) §3.
- Q&A short forms: [QA.md](QA.md) A1 (guardrails), A3 (RAG groundedness).

---

## Slide 9 — Multi-use-case matrix

**~50s**

### On screen

The matrix — **transcribed, never redrawn.**

|  | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** | **Block** | Escalate | Escalate | Escalate |
| **R2** | **Block** | Edit | Edit | Escalate |
| **R1** | Edit | Edit | Pass + annotate | Pass + annotate |
| **R0** | Pass + annotate | Pass + annotate | Pass | Pass |

Same plane. Three Round 2 use cases. Three actuators.

| Use case | Action | Cell | Actuator |
|---|---|---|---|
| Customer support chatbot | `show_reply` R1 | R1 × Unsupported + hedged | **Pass + annotate** |
| Internal knowledge copilot | `draft_partner_email` R2 | R2 × Unsupported + categorical | **Edit** |
| Decision-support refund | `issue_refund` R3 | R3 × Unsupported + categorical | **Escalate** |

The verdict is hostile. The action is proportionate.

### Say

> A hedged warranty guess on a support reply is not the same object as an ungrounded clause authorising a payment. Treat them as one score and you either over-flag the first — the plane gets switched off — or under-flag the second.
>
> Same plane. Support streams with an annotation. The copilot's partner email is edited. The refund is held and escalated. Proof still scales with consequence.

### Do not say

- Redraw the matrix, invent a column, flatten R3 to Block ([ARCHITECTURE.md](ARCHITECTURE.md) §4, §10.4).
- "blocked" on the decision-support row.

### Backing

Observed in `python3 examples/multi_usecase_demo.py`:

```
1. Customer support chatbot
   cell       R1 × Unsupported + hedged  →  Pass + annotate
2. Internal knowledge copilot
   cell       R2 × Unsupported + categorical  →  Edit
3. Decision-support refund
   cell       R3 × Unsupported + categorical  →  Escalate
Same plane, three R-tiers, three actuators
```

Locked by `tests/test_multi_usecase.py`.  
Architecture: [ARCHITECTURE.md](ARCHITECTURE.md) §4 (verbatim matrix); [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) Appendix A.2.

---

## Slide 10 — Business case + roadmap

**~60s**

### On screen

Directional, from the Round 2 brief — not a measured dataset: **~40,000 interactions/week**. R0/R1 ≈ 80–90% → Lane 1 only.

Three quantities the graph makes exact (no catch-rate, no savings %):

| Quantity | What the buyer cashes |
|---|---|
| **Held irreversible actions** | R3 × unsupported-categorical → held packet, not a Tuesday payout |
| **Entitlement incidents prevented** | Over-permissioned index × wrong caller → Edit/Block, microseconds |
| **Dead compute, named** | Walk the graph backward: steps that grounded zero accepted claims |

| Phase | Window | What ships |
|---|---|---|
| **0 Shadow** | weeks 0–6 | Proxy + SDK hook; dual-emit; *would have held N, of which M were true positives* |
| **1 Enforce R3** | weeks 6–12 | Payments, deletion, publication, regulated advice. Fail closed or escalate. |
| **2 Enforce R2** | weeks 12–20 | Reversible writes / external sends. Autonomy downgrade. |
| **3 FNR + loops** | from week 16 | Per-route FNR with CI; override capture; geographic packs as DAG *content* |

Latency **targets**: **≤40 ms p50 / ≤200 ms p95** added on R0/R1 text. Never quote 40 as p95.  
**Measured** gate (`submission/latency_bench.json`, n=200): p50≈**0.074 ms**, p95≈**0.134 ms** — under target; still quote targets vs measured separately.

We do **not** eliminate hallucinations. We do **not** claim drop-in. We do **not** claim zero added latency: **we never make the model feel slow; we make the action wait.** The integration cost is the moat.

### Say

> At forty thousand interactions a week, uniform deep checking is how planes get disabled. Budget follows blast radius. We will not put a savings percentage on this slide — that number is knowable only on your traffic.
>
> What is knowable now: a missing clause cannot authorise a payout; an HR span cannot ride along to the wrong caller; dead compute is a walk backward on the same graph, not an estimate.
>
> Shadow first. Enforce R3 next. We hook context assembly — that is real integration, and it is why the design works.

### Do not say

- A fabricated catch rate, payback period, or "we save X% of tokens" ([ARCHITECTURE.md](ARCHITECTURE.md) §10.7; [QA.md](QA.md) D2).
- "zero integration / drop it in" or "zero added latency" ([NARRATIVE.md](NARRATIVE.md) §5).
- Quote 40 ms as p95 ([ARCHITECTURE.md](ARCHITECTURE.md) §5, §10.6). Measured ≠ target; never round measured up to 40 and call it p95.

### Backing

- Volume, mix, three quantities, phases: [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) §4–5.
- Latency targets + measured bench: [ARCHITECTURE.md](ARCHITECTURE.md) §5; `submission/latency_bench.json`.
- Refuse-to-claim list (about *us*): [NARRATIVE.md](NARRATIVE.md) §5; [ARCHITECTURE.md](ARCHITECTURE.md) §10.8.
- Prototype dead compute on this fixture: `faq_search` and `crm_lookup` ground no accepted claim (`examples/refund_trace_demo.py`; [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) Appendix A.1). Do not quote ARCHITECTURE §9's "9 tool calls, 4 dead" as this slice — that is the narrative example, not the running prototype.

---

## Slide 11 — Risks we publish (FNR shape)

**~50s**

### On screen

**We publish our own miss rate. Per route. Not what we caught — what we missed.**

Gate report — empty schema. The emptiness is the claim.

```
route                <id>
window               <start>–<end>
volume               <n>
holds                <n>   escalations <n>   edits <n>   blocks <n>
shadow_would_have_held   <n>
true_positives_in_holds  <n>   (sampled)
false_negatives          <n>   (sampled passes that should have held)
FNR                      <measured>%  ± <CI>   per route
dead_compute_share       <measured>%  of steps grounding zero accepted claims
override_rate            <measured>   vs baseline <measured>
p50_added_ms             ≤40 (target)    p95_added_ms  ≤200 (target)
policy_version           <id>
```

Strongest residual risk: **false assurance on derived / multi-hop claims.**  
Derived → recompute, or **UNKNOWN**. **UNKNOWN never collapses into SUPPORTED.**

Bias (kept, measurement terms): **counterfactual flip rate with a confidence interval, route-level, async.** Not a per-response verdict.

### Say

> We do not claim to eliminate hallucinations. The honest claim has a shape: on this route we catch a measured percent of ungrounded claims at forty milliseconds p50 — and here is the measured percent we don't.
>
> Every team will claim detection. Publishing our own false-negative rate is the move none of them will make. The blanks stay blank until we measure.
>
> Derived claims are the residual risk we will say out loud. UNKNOWN never becomes SUPPORTED. That one rule is the boundary between a control plane and false assurance.

### Do not say

- Fill the placeholders with plausible numbers ([QA.md](QA.md) D1; [ARCHITECTURE.md](ARCHITECTURE.md) §10.7).
- Drop bias. If asked: that sentence is the whole answer ([NARRATIVE.md](NARRATIVE.md) §8; [ARCHITECTURE.md](ARCHITECTURE.md) §10.9).
- "99% accuracy detecting bias, safety and risk" ([NARRATIVE.md](NARRATIVE.md) §5).

### Backing

- Credibility play: [NARRATIVE.md](NARRATIVE.md) §7.
- Residual risk and FNR shape: [ARCHITECTURE.md](ARCHITECTURE.md) §7.
- Empty schema: [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) §5; [ARCHITECTURE.md](ARCHITECTURE.md) §10.7.
- Prototype lock on derived → UNKNOWN: `tests/test_binder.py` (`ClaimKind.DERIVED`).
- Bias as counterfactual invariance: [ARCHITECTURE.md](ARCHITECTURE.md) §3; [QA.md](QA.md) D4. Specified, async, not coded in this slice ([ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) Appendix A.3).

---

## Slide 12 — Ask / close

**~30s**

### On screen

ControlPlane.ai  
Admission-control layer · `STEP → SPAN → CLAIM → ACTION`

Ask: Round 2 advance. Next artefact is Phase 0 shadow on **one support route and one acting route** — the counterfactual, not a global switch.

That refund was ₹1,84,000 on a clause that does not exist.

**That system was never asked to prove anything.**  
**Now nothing acts until it can prove it should.**

### Say

> We are asking to take this into shadow on one support route and one acting route. Enforcement is earned per route. The first artefact you get is the counterfactual — would have held N, of which M were true positives — not a block.
>
> **That system was never asked to prove anything.**
>
> *[hold]*
>
> **Now nothing acts until it can prove it should.**

### Do not say

- A new scenario at the close. Answer the hook ([NARRATIVE.md](NARRATIVE.md) §7).
- "watch / catch / flag problems." If a judge can summarise it as *"it watches AI outputs and flags problems,"* the narrative has failed ([NARRATIVE.md](NARRATIVE.md) §6 ship test).

### Backing

- Close lines: [NARRATIVE.md](NARRATIVE.md) §7 (first and last claim, negated then resolved).
- Ask = Phase 0: [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) §5.
- Shadow default, per-route enforcement: [ARCHITECTURE.md](ARCHITECTURE.md) §5.9.

---

## Content-law card (print; keep in the clicker hand)

From [ARCHITECTURE.md](ARCHITECTURE.md) §10 and [NARRATIVE.md](NARRATIVE.md) §6–8. Broken by at least one model each.

1. Clause 7.2 **does not exist**. Never caps / denies / doesn't cover.
2. Never say **"blocked"** about the refund. Held and escalated with the evidence packet.
3. The **company** wrongly paid ₹1,84,000. The customer did not lose it.
4. The matrix is **transcribed, never redrawn**.
5. Actuators are exactly **Block · Edit · Escalate · Pass**.
6. Latency **targets** are **≤40 ms p50 / ≤200 ms p95**. Measured gate ≈0.074 / 0.134 ms (`latency_bench.json`). Never quote 40 as p95.
7. Gate report ships **empty**. Do not invent FNR / catch-rate / savings %.
8. Refuse-to-claim list is about **us**, not competitors.
9. **Do not drop bias.** Measurement terms only: counterfactual flip rate, route-level, async.
10. First sentence of any ad-lib contains **"claim"**, not "response." **"Safety"** only after "deterministic entitlement check."

Banned vocabulary: monitors, observes, detects, watches, guards, trust score, risk score, safety score, observability layer, guardrail *(as our noun)*, responsible AI, ethics, trustworthy.

Permitted exception: *"Everyone watches the exit. Nobody records the entrance."*

---

## Dry-run — every pitch claim, backed

Step 2 of this task. If a line cannot be pointed at, it is not on a slide.

| Slide | Claim | Backing |
|---|---|---|
| 1 | Category = admission-control layer | [NARRATIVE.md](NARRATIVE.md) §2 |
| 2 | Ungated sentence, ₹1,84,000, clause 7.2 | Prototype `UNGATED_RESPONSE`; [ARCHITECTURE.md](ARCHITECTURE.md) §9 |
| 2 | Company paid; clause does not exist | [ARCHITECTURE.md](ARCHITECTURE.md) §10.1, §10.3 |
| 2 | "It used to be a bad paragraph…" | [NARRATIVE.md](NARRATIVE.md) §7 |
| 2 | "The system didn't fail. It was never asked…" | [NARRATIVE.md](NARRATIVE.md) §7 |
| 3 | Set-membership on receipts | [NARRATIVE.md](NARRATIVE.md) §1 |
| 3 | "Everyone watches the exit…" | [NARRATIVE.md](NARRATIVE.md) §7 |
| 3 | Default UNSUPPORTED | [ARCHITECTURE.md](ARCHITECTURE.md) §3; binder |
| 4 | STEP→SPAN→CLAIM→ACTION + three reads | [ARCHITECTURE.md](ARCHITECTURE.md) §2 |
| 4 | "An AI response is not text to be scored…" | [NARRATIVE.md](NARRATIVE.md) §7; [ARCHITECTURE.md](ARCHITECTURE.md) §1 |
| 4 | "Everywhere else that's three products…" | [NARRATIVE.md](NARRATIVE.md) §7 |
| 5 | `clause_72` UNSUPPORTED, spans=(none) | `refund_trace_demo.py`; `test_clause_72_is_absence_not_contradiction` |
| 5 | "Not low confidence. Unproven." | [NARRATIVE.md](NARRATIVE.md) §7; [ARCHITECTURE.md](ARCHITECTURE.md) §9 |
| 6 | `hr_side` SUPPORTED + entitlement VIOLATION → Edit | `refund_trace_demo.py`; `test_show_text_driven_by_entitlement` |
| 6 | R1 × entitlement = Edit | [ARCHITECTURE.md](ARCHITECTURE.md) §4 matrix |
| 7 | `issue_refund` Escalate, not Block | `refund_trace_demo.py`; `test_refund_held_not_blocked` |
| 7 | R3 × Unsupported + categorical = Escalate | [ARCHITECTURE.md](ARCHITECTURE.md) §4 |
| 7 | Dual action on one ledger; chain verifies | `test_dual_action_edit_and_escalate`; `verify_chain() = True` |
| 7 | "Proof scales with consequence." | [NARRATIVE.md](NARRATIVE.md) §7; [ARCHITECTURE.md](ARCHITECTURE.md) §9 |
| 8 | Guardrails / RAG / confidence / judge / 87 | [NARRATIVE.md](NARRATIVE.md) §3; [ARCHITECTURE.md](ARCHITECTURE.md) §8 |
| 9 | Matrix cells and three actuators | Matrix transcribed from [ARCHITECTURE.md](ARCHITECTURE.md) §4; `multi_usecase_demo.py`; `tests/test_multi_usecase.py` |
| 10 | ~40k/week directional; 80–90% R0/R1 | [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) §4; [ARCHITECTURE.md](ARCHITECTURE.md) §5.7 |
| 10 | Three cashable quantities; no savings % | [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) §4.1; [QA.md](QA.md) D2 |
| 10 | Phases 0–3 | [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) §5 |
| 10 | ≤40 ms p50 / ≤200 ms p95 **targets**; measured ≈0.074 / 0.134 ms | [ARCHITECTURE.md](ARCHITECTURE.md) §5, §10.6; `submission/latency_bench.json` |
| 10 | Four refusals | [NARRATIVE.md](NARRATIVE.md) §5 |
| 11 | Empty FNR schema | [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) §5; [ARCHITECTURE.md](ARCHITECTURE.md) §10.7 |
| 11 | "We publish our own miss rate…" | [NARRATIVE.md](NARRATIVE.md) §7 |
| 11 | Derived → UNKNOWN; never collapses to SUPPORTED | [ARCHITECTURE.md](ARCHITECTURE.md) §7; `tests/test_binder.py` |
| 11 | Bias = counterfactual flip rate, async | [ARCHITECTURE.md](ARCHITECTURE.md) §3, §10.9; [QA.md](QA.md) D4 |
| 12 | Close lines, hold, resolution of slide 2 | [NARRATIVE.md](NARRATIVE.md) §7 |
| 12 | Ask = Phase 0 shadow, two routes | [ROUND2-PROPOSAL.md](ROUND2-PROPOSAL.md) §5 |

Prototype claims on slides 5–7 and 9 were re-read from live demo output for this outline. They are not the ARCHITECTURE §9 narrative counts (14 spans / 9 tool calls). This slice is five spans, six claims, two dead steps.

---

## Demo cues (if a laptop is in the room)

Align with R2S5 demo spine + [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md). Prefer the live console (held panel cold open); CLI is the backup.

```bash
# Preferred: console refund · enforce → dual Edit + Escalate on one ledger
# curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' | python3 -m json.tool

python3 examples/refund_trace_demo.py
# Beat 1: clause_72 UNSUPPORTED, spans=(none) — clause 7.2 does not exist
# Beat 2: show_text → Edit  (R1 × entitlement)
# Beat 3: issue_refund → Escalate  (R3 × unsupported-categorical)
# never “blocked”; held and escalated with the evidence packet; verify_chain() = True

python3 examples/knowledge_flip_demo.py
# analyst_01 → Edit; hr_partner_01 → Pass; same span / claim / hash

python3 examples/multi_usecase_demo.py
# show_reply           → Pass + annotate
# draft_partner_email  → Edit
# issue_refund         → Escalate
```

If the demo cannot run, slides 5–7 and 9 already carry the observed lines. Do not paraphrase actuators.

---

*Design is closed in [ARCHITECTURE.md](ARCHITECTURE.md). This outline is a rendering for Round 2, plus evidence that the keystone runs.*
