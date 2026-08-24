# ControlPlane.ai — Stage 5: Pitch Architecture

---

## 1. Pitch Thesis

An AI response is not text to be scored — it is a set of claims requesting permission to act — and the only thing that can prove a claim is the evidence the model was actually given before it ran, captured outside the model with source identity and access rights attached, which turns verification from an unfalsifiable opinion into a set-membership test and turns oversight from scoring output into authorising actions, so that proof scales with consequence: the identical unsupported claim annotates a draft and holds a payment.

---

## 2. Overall Pitch Structure

**Total: 10 minutes.** No filler. Every beat earns its slot or gets cut.

| # | Beat | Time | Purpose |
|---|---|---|---|
| 1 | **Opening — the held transaction** | 0:00–1:15 | Establish category change; deliver indictment line; state thesis |
| 2 | **The one graph** | 1:15–2:00 | STEP→SPAN→CLAIM→ACTION; three reads; provenance outside model |
| 3 | **Dual-action demo — cold open to ledger** | 2:00–4:30 | Core demo: held refund, ledger expansion, matrix cells, actuators, packet, executor |
| 4 | **Principal flip** | 4:30–5:30 | Same claim, different caller → different outcome; entitlement as set-membership |
| 5 | **Differentiation — three strikes** | 5:30–6:45 | vs observability · vs LLM-as-judge · vs groundedness; refuse-to-claim delivered here |
| 6 | **Business spine — value without consulting deck** | 6:45–8:15 | Exposure formula, dead compute, earned autonomy, FNR posture, roadmap as earn-out |
| 7 | **Close** | 8:15–9:00 | Resolve opening; publish-misses line; final negation→resolution |
| 8 | **Buffer** | 9:00–10:00 | Reserved for one clean pivot if judge interrupts; otherwise silent |

Demo occupies ≥50% of pitch time. Ledger is visible ≥60% of demo time. Business case is delivered in ≤90 seconds — mechanism→consequence only, no "market sizing" chrome.

---

## 3. Opening Beat (0:00–1:15)

**Screen:** The action gate. `refund.execute` with `committed: false`. Rupee figure visible. No context, no setup, no "AI is powerful but risky."

**Spoken:**

> "A refund agent issued ₹1,84,000 under clause 7.2 of the vendor agreement. The filters passed it. Confidence read 0.94. Money moved Tuesday. Found Friday.
>
> Clause 7.2 does not exist.
>
> The system didn't fail. It was never asked to prove anything.
>
> The cost of a wrong AI output changed category. It used to be a bad paragraph. It is now an executed transaction.
>
> An AI response is not text to be scored. It is a set of claims requesting permission to act."

**Then — without pause — straight into the graph.** No "so we built…" transition. The graph *is* the answer to the hook.

**Discipline:** The word "claim" appears in the first failure sentence. "Response" does not appear as the subject of any sentence in this beat. "Risk" does not appear at all. No person — no shocked customer, no angry email. Only a transaction, a clause that does not exist, and money that moved.

---

## 4. Prototype Demonstration Spine (2:00–5:30)

### Embedding logic

The demo is not "after the setup." The demo *is* the setup. The opening places you at the action gate; the demo opens that gate and walks backward through the ledger to show *why* it stayed closed.

### Sequence — protected invariants in brackets

**Beat 3a — Cold open gate (2:00–2:30)**

Screen already shows `refund.execute` `{amount:184000, reason:"clause 7.2", order_id:"ORD-1023"}` · R3 · **HELD — ESCALATE** · `executed: false`.

> "This is the gate. The refund did not execute. Here is why."

**[Protected: hard gate on action; committed:false; never "blocked"]**

**Beat 3b — Ledger expansion (2:30–3:15)**

Expand the Evidence Ledger. Spans are already present — source_id, ACL, content_hash, offsets — *before* any claim verdict appears.

> "Every span was captured at context assembly, before the model ran. The model has no write path to this ledger."

Walk the three claims:

| Claim | Verdict | Why |
|---|---|---|
| C1: amount ₹1,84,000 from ORD-1023 | **SUPPORTED** | Numeric recomputation against span |
| C2: "under clause 7.2" | **UNSUPPORTED** | No span. Absence, not contradiction |
| C3: internal note in customer text | **Entitlement violation** | Span exists. ACL excludes caller |

**[Protected: spans before claims; default UNSUPPORTED; absence ≠ contradiction; claim-type routing]**

**Beat 3c — Matrix cells before actuators (3:15–3:45)**

Highlight the two pending actions *before* naming what happens to them:

> "One response. Two pending actions. Different blast radii. The same claim feeds both — but the matrix prices them separately."

Show the exact cells:
- `text.show` → R1 × entitlement violation → **Edit**
- `refund.execute` → R3 × unsupported-categorical → **Escalate**

**[Protected: worst claim per pending action; exact matrix cells; never collapse into one response verdict]**

**Beat 3d — Surgical edit + evidence packet (3:45–4:15)**

Execute the edit: C3 stripped. Refund stays held.

Open the escalation packet for C2: claim, candidate spans `[]`, verdict, diff.

> "Edit is surgical — strip the unentitled claim. Escalate ships the evidence packet — what the claim was, what spans exist, what's missing. Not an alert. A case file."

**[Protected: surgical edit (not generative rewrite); packet contents; held not blocked]**

**Beat 3e — Executor proof (4:15–4:30)**

Show `committed: false` on the refund executor.

> "The company does not wrongly pay out ₹1,84,000 today."

**[Protected: executor proves non-commitment; company pays out, not customer loses]**

**Beat 3f — Empty FNR schema (4:30—part of transition)**

Visible in the ledger periphery. Null placeholders only. Do not narrate it unless asked. It is there to be found.

**[Protected: typed nulls only; no fabricated percentages; emptiness is the credibility play]**

### Beat 4 — Principal flip (4:30–5:30)

> "Same claim. Same span. Different caller."

Run the knowledge route. `analyst_01` sees the HR compensation span → entitlement violation → **Edit**. Flip principal to `hr_partner_01`. Same span, same claim → **Pass**.

> "The claim didn't change. The evidence didn't change. The access right changed. Zero LLM in this path. Set-membership."

**[Protected: zero LLM in entitlement; same claim different outcome; set-membership not classification]**

**Transition out of demo:** straight into differentiation. No "so that's how it works." The flip *is* the differentiation argument made concrete.

---

## 5. Business Case Integration (6:45–8:15)

**Delivered as mechanism→consequence. No standalone "market opportunity" slide. No "ROI" with fabricated percentages. No net-savings claim.**

### Sequence

**5a — Exposure formula (20 seconds)**

> "Exposure equals the frequency of consequential AI actions, times the probability an unproven or unauthorized claim slips through, times the loss if it does. We do not put a rupee figure on that slide — you know your routes and your loss function better than we do."

**5b — Three levers, each one line (45 seconds)**

| Lever | Line |
|---|---|
| Avoided wrong actions | "R3 Escalate held with `committed:false` is a structural escape hatch. The value is the held true-positives times your cost of that action class — residual sized by our published miss rate." |
| Dead compute | "Walk the graph backward: every step that grounded zero accepted claims is waste, computed exactly. A dashboard tells you the trace cost ₹8. This tells you ₹5 of it grounded nothing." |
| Earned autonomy | "Shadow first. Enforce only where the counterfactuals justify. More AI action after evidence — never the leading claim." |

**5c — Roadmap as earn-out (20 seconds)**

> "Day one is shadow. Enforcement is earned per route through counterfactual evidence. We publish what we miss at every phase."

Four phases on screen — shadow, canary, limited R2/R3 enforce, broader envelope — each with one-word exit criterion. No Gantt chart. No timeline.

**5d — Buyer split (15 seconds, visual only if time)**

Economic buyer sees action authorisation. Technical buyer sees graph, not second black box. Day-to-day actor sees Verified/Uncertain/Blocked per claim. One visual, not narrated unless asked.

---

## 6. Differentiation & Defence Moments

Three moments. Each delivers a contrast *and* a refuse-to-claim. Never a standalone "competitor analysis" section.

### Moment 1 — vs observability (inside Beat 5b, dead-compute lever)

> "Observability tools tell you what went wrong after a user acted on it. The same graph that verifies the claim also computes the waste — because it's the same graph. Observation without commit control is an audit trail, not architecture."

**Refuse-to-claim delivered silently:** the dead-compute number is exact, not estimated — we do not claim a net-savings percentage because we have not measured it on their traffic.

### Moment 2 — vs LLM-as-judge and groundedness (Beat 6, opening 30 seconds)

> "A second model asks 'does this look right?' — an unfalsifiable question. We ask 'which span proves it?' — a query with an answer. Groundedness checkers average across claims, so one wrong figure drowns in nine correct sentences, and they're action-blind: 0.82 means the same on a draft and on a wire transfer. Retrieval is not permission. Proof scales with consequence."

**Refuse-to-claim delivered here explicitly:**

> "We do not claim to eliminate hallucinations. We claim an unproven claim cannot authorise an action — and we publish the rate at which we miss."

### Moment 3 — vs composite risk scores (Beat 6, second 30 seconds)

> "Three failure modes with three different owners, costs and remedies, collapsed into one number that maps to no intervention. You cannot block, edit or escalate on 87."

**Refuse-to-claim:** "We do not offer one accuracy number across hallucination, leakage and bias. They have different mathematics."

**Never delivered as a slide titled "Competitive Landscape."** Each contrast lives inside the moment that proves it.

---

## 7. Closing Beat (8:15–9:00)

**Resolve the opening exactly. The first and last claims are negation→resolution.**

> "That system was never asked to prove anything."
>
> *[hold two seconds]*
>
> "Now nothing acts until it can prove it should."
>
> "We publish our own miss rate. Per route. Not what we caught — what we missed."
>
> "An AI response is a set of claims requesting permission to act. Capture the provenance outside the model. Invert the burden of proof. Gate the commit path."

**Last word is "path."** Not "safe," not "trustworthy," not "responsible." Structural. Cold. Done.

---

## 8. Anti-Patterns (Hard Kill List)

| # | Never do | Why it dies |
|---|---|---|
| 1 | Open on "AI risk," "AI is powerful but," or any generic safety framing | Triggers pattern-match to "another guardrail deck" before architecture is evaluated |
| 2 | Open on a person — shocked customer, angry email, harmed individual | Violates "open on a transaction" rule; shifts frame from authorisation to sentiment |
| 3 | Say "blocked" about the refund | Matrix says Escalate. "Blocked" is wrong and a serious engineer will catch it |
| 4 | Say clause 7.2 "caps," "denies," or "doesn't cover" the refund | Failure is *absence* of evidence, not conflict. Wrong column. |
| 5 | Say the customer lost money | The *company* wrongly pays out. Customer did not lose money. |
| 6 | Collapse dual-action into one response-level verdict | Destroys the single most differentiated demo beat |
| 7 | Show composite risk score, confidence score, or "trust score" anywhere in the UI | Forbidden by architecture; judge who sees it assumes we don't understand the problem |
| 8 | Use monitor, detect, observe, watch, guard, trust score, risk score, "responsible AI" as standalone virtue | Vocabulary ban from NARRATIVE.md; single exception is "everyone watches the exit" |
| 9 | Show LLM-as-judge pane, open-web lookup, or generative rewrite in the demo | Architecture rejects all three; showing them signals we don't believe our own design |
| 10 | Quote 40ms as p95 | Architecture says ≤40ms p50, ≤200ms p95. Quoting 40 as p95 is a five-fold overclaim, dead on contact |
| 11 | Fill FNR schema with fabricated percentages | Emptiness is the credibility play. Fabricated numbers destroy it. |
| 12 | Lead with enablement ("more AI action!") | Enablement is secondary. The leading claim is admission control. |
| 13 | Show a third live route (especially bias) in the demo | Scope locked to exactly two. Bias is async-only, proposal-only. |
| 14 | Say "we eliminate hallucinations" or "zero integration" or "zero added latency" | Refuse-to-claim list. Each is attackable and unnecessary. |
| 15 | Redraw the matrix | Transcribed, never redrawn. Every prior attempt corrupted it. |
| 16 | Show the graph but narrate it as "three products working together" | It is one graph, three reads. "Three products" is the competitor's framing. |
| 17 | Allow UNKNOWN to collapse into SUPPORTED in any demo path | Boundary between control plane and false assurance. |
| 18 | Show an "override" button that bypasses the interlock | Interlock bypass is forbidden; the plane is not advisory on R3. |
| 19 | Deliver business case as a standalone consulting section | Mechanism→consequence only; no market sizing, no ROI percentages, no Gantt chart |
| 20 | End on "thank you" or a question prompt | End on the resolved opening line. "Thank you" is dead air that surrenders the last word. |

---

## 9. Fidelity Self-Check

| # | Invariant | Protected where | Status |
|---|---|---|---|
| 1 | Default = UNSUPPORTED | Demo beat 3b: all three claims start UNSUPPORTED | **PASS** |
| 2 | Entitlement = set-membership, zero LLM | Principal flip beat: "Zero LLM in this path. Set-membership." | **PASS** |
| 3 | Exact R×S matrix, never redrawn | Beat 3c: cells named before actuators; no visual redraw | **PASS** |
| 4 | One graph: STEP→SPAN→CLAIM→ACTION | Beat 2: graph introduced as the answer to the hook | **PASS** |
| 5 | Hard gate on actions, not tokens | Demo cold open: gate on `refund.execute`; text hold-back mentioned, not shown as gate | **PASS** |
| 6 | Dual-action: R1 Edit + R3 Escalate held | Beat 3c–3d: two pending actions, two actuators, refund = held | **PASS** |
| 7 | UNKNOWN never → SUPPORTED | Beat 3b: C2 stays UNSUPPORTED; no path shown where UNKNOWN upgrades | **PASS** |
| 8 | FNR as typed format; empty until earned | Beat 3f: null placeholders visible, not narrated | **PASS** |
| 9 | Bias = async route-level only | No live bias route; mentioned in business spine as measurement-only if asked | **PASS** |
| 10 | Refuse-to-claim (about us) | Beat 6: three explicit refusals delivered inside differentiation | **PASS** |
| 11 | Never say "blocked" about refund | Anti-pattern #3; demo shows "HELD — ESCALATE" and `executed:false` | **PASS** |
| 12 | Clause 7.2 does not exist | Opening beat: "Clause 7.2 does not exist." No conflict language. | **PASS** |
| 13 | Company wrongly pays out | Opening beat + demo beat 3e: company does not wrongly pay out | **PASS** |
| 14 | Latency ≤40ms p50 / ≤200ms p95 | Not quoted in main pitch unless pressed; anti-pattern #10 prevents p95 overclaim | **PASS** |
| 15 | Vocabulary ban | Anti-pattern #8; script discipline from NARRATIVE.md enforced | **PASS** |
| 16 | Open on held transaction | Beat 1: action gate with rupee figure, no risk framing | **PASS** |
| 17 | First failure sentence contains "claim" | "An AI response is not text to be scored. It is a set of claims requesting permission to act." | **PASS** |
| 18 | Closing resolves opening | "That system was never asked to prove anything → Now nothing acts until it can prove it should." | **PASS** |
| 19 | Ledger ≥60% of demo time | Demo beats 3b–3f: ledger is the primary visual for ~3 of 4.5 demo minutes | **PASS** |
| 20 | Evidence packet on every Escalate | Beat 3d: packet opened showing claim, spans `[]`, verdict, diff | **PASS** |
| 21 | Surgical edit, not generative rewrite | Beat 3d: "strip the unentitled claim" — no LLM rewrite shown | **PASS** |
| 22 | Spans before claims in demo | Beat 3b: spans expanded before claim verdicts appear | **PASS** |
| 23 | Worst claim per pending action | Beat 3c: explicit "worst claim for that action" language | **PASS** |
| 24 | Absence ≠ contradiction | Beat 3b: C2 = "No span. Absence, not contradiction." | **PASS** |
| 25 | Exactly two live routes | Refund + knowledge; third route refused; anti-pattern #13 | **PASS** |

**All 25 invariants PASS. No invariant is traded for demo smoothness, time pressure, or judge expectation.**

---

*Pitch architecture frozen. Render from this spine. Do not reopen.*