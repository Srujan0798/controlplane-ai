# Stage 5 — Pitch Architecture

## 1. Pitch Thesis

**ControlPlane.ai is not another system that judges whether AI text looks safe; it is an admission-control layer for AI that acts.** It treats every response as a set of claims requesting permission to act, records the evidence available to the model before generation, binds claims to that evidence, checks whether the caller is entitled to it, and prices the admission decision by blast radius. The pitch must leave one idea in the room: **the cost of a wrong AI output has changed from a bad paragraph to an executed transaction, so the control point must move from scoring the output to authorizing the action.**  

---

# 2. Overall Pitch Structure

### Target: **10 minutes**

The pitch should feel like **one technical argument with a business consequence**, not "business slides + technical demo."

|           Time | Beat                                     | Purpose                                                                           |
| -------------: | ---------------------------------------- | --------------------------------------------------------------------------------- |
|  **0:00–1:20** | **Opening: ₹1,84,000 action**            | Establish category change and create the unresolved problem                       |
|  **1:20–2:20** | **Reframe: admission control**           | Explain why existing approaches stand at the wrong boundary                       |
|  **2:20–3:10** | **One graph + mechanism**                | Show the entire architecture in one minute                                        |
|  **3:10–6:40** | **Prototype: live proof**                | Dual-action first, principal flip second, FNR third                               |
|  **6:40–7:50** | **Why this matters commercially**        | Translate the demonstrated control into enterprise value                          |
|  **7:50–9:10** | **Enterprise rollout + differentiation** | Explain how the same primitive scales and why competitors do not collapse into it |
| **9:10–10:00** | **Credibility + close**                  | Refuse unsupported claims, state what is measured, resolve opening                |

### The governing narrative shape

```text id="pitchshape"
ACTION AT RISK
     ↓
WHY EXISTING BOUNDARY FAILS
     ↓
ADMISSION-CONTROL REFRAME
     ↓
ONE GRAPH
     ↓
LIVE ACTION GATE
     ↓
BUSINESS CONSEQUENCE
     ↓
ENTERPRISE SCALE
     ↓
CREDIBILITY
     ↓
RESOLUTION
```

This deliberately follows the frozen narrative instruction to run **one trace end-to-end** rather than cycling through several shallow scenarios. 

---

# 3. Opening Beat — First 60–90 Seconds

## 0:00–0:15 — Start with the action, not the category

**Screen:** only the pending transaction.

```text
REFUND REQUEST
₹1,84,000
Action: issue_refund
Status: AWAITING ADMISSION
```

No title slide. No "AI is transforming enterprises." No risk taxonomy.

### Opening line

> **“It used to be a bad paragraph. It is now an executed transaction.”** 

Then immediately:

> **“Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.”**

Pause.

> **“Clause 7.2 does not exist.”**

Then:

> **“The system didn't fail. It was never asked to prove anything.”** 

## 0:15–0:45 — Establish the actual failure

Do not say "hallucination detector."

Say:

> “The claim had no supporting evidence. Yet the claim was allowed to authorize an irreversible action.”

Then:

> **“If ungated, the company wrongly pays out ₹1,84,000. The customer did not lose money.”** 

The unresolved screen state remains visible:

```text
₹1,84,000
R3
AWAITING ADMISSION
```

## 0:45–1:20 — Reframe

Use the strongest narrative hinge:

> **“Everyone watches the exit. Nobody records the entrance.”** 

Then:

> **“An AI response is not text to be scored. It is a set of claims requesting permission to act.”** 

Then immediately hand over to the prototype:

> “So we changed the boundary.”

**Cut directly into the Evidence Ledger.**

This avoids the generic "AI risk" frame that the narrative explicitly identifies as the first 20-second failure mode. 

---

# 4. Prototype Demonstration Spine

The prototype is the **intellectual center** of the pitch. Allocate approximately **3 minutes 30 seconds**.

The demo must be executed **backward from the action gate**, exactly as frozen.

## 4.1 Beat A — Start at the R3 gate

### 3:10–3:30

Show:

```text
PENDING ACTION
refund.execute
₹1,84,000
R3

CLAIM
Clause 7.2 permits the refund

VERDICT
UNSUPPORTED + categorical

MATRIX
R3 × Unsupported + categorical
          ↓
       ESCALATE
          ↓
HELD
```

Say:

> “This action is not executing.”

Do **not** say "blocked."

The frozen wording is **held and escalated with the evidence packet**. 

## 4.2 Beat B — Reveal the proof chain backward

### 3:30–4:05

Now expand the graph:

```text
ACTION
  ↑
CLAIM
  ↑
SPAN
  ↑
SOURCE + ACL + HASH
  ↑
STEP
```

Then show:

```text
Clause 7.2
↓
NO SPAN
↓
UNSUPPORTED
```

The important moment is that the audience sees **the missing proof**, not a red score.

Say:

> **“Not low confidence. Unproven.”** 

Then reveal:

```text
Evidence was captured before generation.
```

This establishes the strongest differentiator: provenance is external to the model and cannot be authored by it. 

---

## 4.3 Beat C — Show the second pending action

### 4:05–4:45

The same response contains customer-visible text grounded in an ACL-excluded span.

Show:

```text
ACTION: text.show
R1

CLAIM
supported semantically
but caller not entitled

R1 × entitlement violation
          ↓
        EDIT
```

Then show both actions simultaneously:

```text
SAME RESPONSE
     │
     ├── text.show
     │     R1 × entitlement
     │           → EDIT
     │
     └── refund.execute
           R3 × unsupported categorical
                    → ESCALATE (HELD)
```

Then say:

> **“Two pending actions. One graph. Two different actuators.”**

This is the point where the judge should understand that the matrix is not renamed severity. The frozen architecture requires the dual action to remain independent. 

---

## 4.4 Beat D — Make the action gate physically observable

### 4:45–5:05

Attempt:

```text
commit_refund()
```

Show:

```text
COMMIT = FALSE
ACTION = HELD
ESCALATION PACKET = READY
```

Then say:

> “The gate is not on tokens. It is on the commit.”

This directly demonstrates the architecture's core placement: optimistic text, hard action gate. 

---

## 4.5 Beat E — Principal flip

### 5:05–5:45

Switch only:

```text
principal = agent_refund_7
```

to:

```text
principal = authorized_principal
```

Same:

* source;
* claim;
* content;
* hash;
* evidence.

Different entitlement result.

Show:

```text
principal A
span.acl ⊄ clearance
→ entitlement violation

principal B
span.acl ⊆ clearance
→ entitled
```

Say:

> **“Nothing about the sentence changed. Only the principal changed.”**

Then:

> **“Authorization is set-membership. The ACL decision uses zero LLM.”**

This is the strongest answer to "Isn't this just RAG groundedness?" because it proves semantic correctness and authorization are separate questions. 

---

## 4.6 Beat F — Empty FNR schema

### 5:45–6:05

Briefly show:

```text
FNR REPORT
route: customer-support-refund

ground_truth_positive_count: null
false_negative_count: null
FNR_estimate: null
CI: null

measurement_status:
INSUFFICIENT_SAMPLE
```

Say:

> **“We publish our own miss rate. We do not invent it.”** 

Do not spend more than 15–20 seconds here.

The point is credibility, not analytics.

---

## 4.7 Optional micro-beat — exact matrix

### 6:05–6:25

Show the complete 4×4 matrix for only a few seconds, with the active cells illuminated.

Do not teach all 16 cells.

Say:

> **“The matrix is one immutable function of blast radius and verdict. Routes supply R; they do not receive different safety products.”**

The exact matrix is load-bearing and must not be visually simplified. 

---

# 5. Business Case Integration

The business case must **follow the proof**, not precede it.

## 6:40–7:50 — Four value levers

Use **one slide**, not a six-slide consulting section.

### Slide: "What the graph buys the enterprise"

```text
CONSEQUENCE CONTROL
Wrong action → held before commit

VERIFICATION ECONOMICS
High consequence → deeper proof
Low consequence → cheaper Lane 1 path

COMPUTE ECONOMICS
Accepted claims ← backward walk ← dead compute

ACCOUNTABILITY
Action → matrix → claim → span → ACL → principal → policy
```

Then speak to each in ~15 seconds.

### 1. Avoided wrong action

> “The first economic value is not a better answer. It is preventing a consequential action that had no proof.”

Use the ₹1,84,000 example again, but do not extrapolate an ROI percentage.

### 2. Verification cost

> “We do not run the same expensive proof on every interaction. Proof scales with consequence.”

The architecture explicitly allocates verification budget by R and uses separate lanes. 

### 3. Dead compute

> “The same graph tells us which tool calls produced nothing that grounded an accepted claim.”

That makes cost a graph read rather than a separate observability product. 

### 4. Auditability

> “An auditor can reconstruct why the action was admitted from the ledger, matrix, policy version and evidence.”

The enterprise ledger records principal, evidence fragment, verdict, matrix cell, actuator, policy and verifier versions. 

---

## 7:50–8:25 — Buyer + deployment logic

Do not introduce a persona matrix.

Say:

> “The first buyer is the team already running AI that can write, send, refund or otherwise commit something consequential.”

Then:

```text
Shadow
  ↓
Measured counterfactual
  ↓
Canary
  ↓
Earn enforcement
  ↓
Second route
  ↓
Enterprise rollout
```

Explain only the principle:

> **“Enforcement is earned per route. It is not switched on from a slide.”** 

This is where the R2S4 roadmap belongs. The enterprise envelope scales the same primitive across support, knowledge, and eventually decision-support/agentic routes; the prototype remains exactly two routes. 

---

# 6. Differentiation & Defence Moments

There should be **three deliberate defence moments**, not a giant competitor slide.

## Defence Moment 1 — Immediately after mechanism

### ~2:20

Three-line contrast:

```text
LLM-as-judge
→ asks “does this look right?”

RAG groundedness
→ asks “does retrieval resemble the answer?”

ControlPlane
→ asks “which captured span proves this claim,
   and is this caller entitled to it?”
```

Then:

> **“Retrieval is not permission.”** 

This is the cleanest moment to distinguish from LLM-as-judge, static controls, and groundedness.

---

## Defence Moment 2 — Inside the dual-action demo

### ~4:40

When the screen shows:

```text
R1 → Edit
R3 → Escalate
```

say:

> **“Severity describes the error. Blast radius describes the consequence.”**

Then:

> **“Proof scales with consequence.”**

This directly answers the hardest matrix objection: blast radius is not severity with different vocabulary. 

---

## Defence Moment 3 — Final credibility move

### ~8:25

Show the empty FNR schema again in a small corner.

Say:

> **“We are not claiming 99% accuracy. We are telling you exactly how we will measure our misses.”**

Then:

> **“We do not claim to eliminate hallucinations, bias, or privacy risk.”**

Then one line on bias:

> **“Bias is route-level counterfactual flip rate with a confidence interval, asynchronously—not a live per-response verdict.”** 

This converts apparent incompleteness into disciplined scope.

---

# 7. Closing Beat

## 9:10–10:00

Return visually to the opening transaction.

Do not show a "Thank You" slide.

Screen:

```text
₹1,84,000
CLAIM: clause 7.2 permits refund
PROOF: none
R3
ESCALATE
HELD
```

Then compress the entire architecture into one final graph:

```text
STEP → SPAN → CLAIM → ACTION
```

Then say:

> **“We started with a system that was allowed to act without being asked to prove anything.”**

Pause.

Then:

> **“That system was never asked to prove anything.”**

Pause.

> **“Now nothing acts until it can prove it should.”** 

Stop.

No extra paragraph. No "thank you for your time." No feature recap.

The close is deliberately the negation/resolution of the opening, exactly as the frozen narrative specifies. 

---

# 8. Anti-Patterns — Hard Kill List

## Opening

**Never:**

* open with "AI is powerful but risky";
* open with bias/hallucination/privacy;
* begin with company background;
* begin with market size;
* begin with architecture diagrams;
* begin with a generic chatbot.

The first visible object is the **₹1,84,000 action**. The frozen narrative explicitly calls opening on risk a pattern-match failure. 

## Prototype

**Never:**

* collapse the dual action into "response blocked";
* say the refund is **blocked**;
* hide the Evidence Ledger behind chatbot UI;
* put a risk/confidence score beside the transaction;
* reveal the matrix only after the actuator;
* run three shallow scenarios;
* start with the knowledge principal flip;
* spend minutes explaining the corpus;
* turn the FNR schema into an analytics dashboard.

The refund must be **held and escalated with the evidence packet**. 

## Business case

**Never:**

* lead with TAM/SAM/SOM;
* lead with "AI governance market";
* present fabricated ROI;
* claim percentages without measured enterprise data;
* sell "enterprise transformation" before showing the primitive;
* call integration "zero";
* make regulatory certification a prototype claim.

The official brief explicitly treats scale parameters as directional and allows simulated scope; the frozen business logic therefore refuses fabricated production numbers. 

## Language

Hard-ban:

```text
monitor
detect
observe
watch
guard
trust score
risk score
responsible AI
AI safety
```

Use:

```text
authorise
admit
prove
bind
entitlement
hold
escalate
gate
blast radius
verdict
```

The narrative explicitly defines this vocabulary discipline. 

One deliberate exception:

> **“Everyone watches the exit. Nobody records the entrance.”**

That line stays because it is the indictment of the existing architecture. 

## Technical explanation

Never:

* redraw the matrix;
* introduce a composite score;
* explain Lane 3 during the central demo;
* claim the system proves source truth;
* claim ControlPlane repairs IAM;
* turn bias into an actuator;
* imply the model can author provenance;
* let an LLM become the final decision-maker.

The system explicitly defends the claim-to-evidence link, not the truth of the underlying source. 

---

# 9. Fidelity Self-Check

| Frozen invariant                       | Pitch protection                                                                                                                                                       |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Default = UNSUPPORTED**              | The opening demo starts with the Clause 7.2 claim entering without proof. The phrase used is **“Not low confidence. Unproven.”**                                       |
| **Entitlement / ACL**                  | The principal-flip is mandatory, and the pitch explicitly shows same claim/source with different principal outcomes.                                                   |
| **Exact R×S matrix**                   | The complete matrix appears in the pitch; centrepiece cells are R1 entitlement → Edit and R3 unsupported categorical → Escalate. No alternative matrix is introduced.  |
| **One graph**                          | The graph is shown before and during the demo and returns in the close.                                                                                                |
| **Hard gate on actions**               | The physical/mock refund commit is demonstrated as held; the pitch states the gate is on commit, not tokens.                                                           |
| **Two pending actions**                | Both actuators are shown simultaneously from the same response. No global response verdict.                                                                            |
| **Refund language**                    | The refund is always described as **held and escalated with the evidence packet**, never blocked.                                                                      |
| **FNR format**                         | Empty/typed FNR schema is shown as a deliberate credibility move; no fabricated production number.                                                                     |
| **UNKNOWN ≠ SUPPORTED**                | Mentioned during mechanism explanation; not hidden behind a generic "uncertain" score.                                                                                 |
| **No LLM-as-judge**                    | Contrast explicitly appears as a defence moment; no second model is positioned as the final decider.                                                                   |
| **No confidence/composite score**      | Confidence is explicitly rejected as the broken instrument for the "confidently wrong" failure.                                                                        |
| **Bias async-only**                    | Bias is acknowledged once in measurement terms and never placed on the live matrix.                                                                                    |
| **API-only boundary**                  | No model-internal access is claimed; integration is presented as context hook + API proxy.                                                                             |
| **Refuse-to-claim**                    | The pitch explicitly refuses elimination, zero integration, zero latency, and universal accuracy claims.                                                               |
| **Enterprise vs prototype separation** | Prototype proves the primitive; enterprise story explains how the same plane is operated across routes.                                                                |

### The final structural test

The pitch passes only if a judge can reconstruct this without the presenters rescuing it verbally:

```text
₹1,84,000 ACTION
       ↓
R3
       ↓
CLAIM
       ↓
UNSUPPORTED
       ↓
NO PROVING SPAN
       ↓
EXACT MATRIX CELL
       ↓
ESCALATE
       ↓
REFUND HELD
```

and then:

```text
SAME RESPONSE
       ↓
R1 TEXT ACTION
       ↓
ENTITLEMENT VIOLATION
       ↓
EDIT
```

and finally:

```text
PRINCIPAL CHANGES
       ↓
ENTITLEMENT RESULT CHANGES
       ↓
NO LLM INVOLVED
```

That is the pitch. Everything else exists only to make those three facts commercially and architecturally credible.

The frozen sources explicitly prescribe this depth-over-breadth approach: follow one refund trace from context assembly through matrix and closing rather than cycling through shallow scenarios. 
