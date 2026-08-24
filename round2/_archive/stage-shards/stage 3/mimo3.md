# Stage 3 — Prototype Specification

---

## 1. Prototype Goal

This prototype exists to prove one thing: that an AI response is a set of claims requesting permission to act, and that unproven or unauthorized claims cannot authorize actions — demonstrated live on a single graph with two heterogeneous routes. Nothing else. The prototype is not a product demo, not a dashboard, not a pitch deck with buttons. It is a working admission-control plane that a judge can interrogate in real time and verify that every decision traces from action to claim to externally captured span to principal entitlement.

---

## 2. Exact Functional Scope

### Implemented and Runnable

| Component | What It Does | Real or Mock |
|---|---|---|
| **Provenance Recorder** | Hooks context assembly; captures every span with `source_id`, `ACL`, `content_hash`, `offsets`, `principal` before the model receives context | **Real** |
| **Evidence Ledger** | Append-only, hash-chained, one per request; stores the full `STEP → SPAN → CLAIM → ACTION` graph | **Real** |
| **Claim Extractor** | Decomposes model output into typed check-worthy propositions at sentence boundaries; tags each categorical or hedged | **Real** (deterministic patterns for numeric/structural + small model or rule-based for textual) |
| **Binding Engine — deterministic path** | Numeric/date/identifier claims recomputed against span values; exact arithmetic | **Real** |
| **Binding Engine — NLI path** | Textual/factual claims evaluated by cross-encoder against provenance set only; returns SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN | **Real** (DeBERTa-v3-base or equivalent, ~300M, local) |
| **Entitlement Auditor** | Caller principal vs source ACL on every span that binds to a claim; zero LLM | **Real** |
| **Action Interlock** | Computes R from route config, reads verdict severity, applies exact frozen R×S matrix, emits actuator | **Real** (pure rule engine) |
| **Surgical Edit** | Strips the failing claim from the output; re-gates the edited result | **Real** |
| **Evidence Packet Builder** | Assembles claim + candidate spans + verdict + diff for Escalate | **Real** |
| **FNR Gate Report** | Per-route typed schema with null/placeholder fields | **Real** (schema only; no fabricated numbers) |
| **Mock Refund Tool** | Simulates a payment API; accepts or rejects commit based on interlock result | **Mock** (deterministic; real gate semantics) |
| **Mock Knowledge Sources** | Two source systems with distinct ACLs: policy repository (mixed governance) and HR records (restricted) | **Mock** (synthetic enterprise-shaped data) |
| **Generator (LLM)** | Produces the AI response that is then verified | **Mock** (pre-scripted response streams for demo stability; architecture supports any OpenAI-compatible API) |
| **UI / Evidence Ledger Display** | Renders the graph, matrix cells, actuators, evidence packets, FNR schema | **Real** |

### Deliberately Mocked

| What | Why | How |
|---|---|---|
| **LLM generator output** | Demo stability; the architecture is model-agnostic and the prototype proves the mechanism, not the model | Pre-scripted response strings that stream token-by-token with realistic latency. The Provenance Recorder, Claim Extractor, and Binding Engine all run against these streams exactly as they would against a live model. The judge sees real compute, not animation. |
| **Refund tool execution** | Real payment is unsafe and unnecessary | Deterministic mock that accepts a commit command or rejects it. The mock honors the interlock: if the interlock says Escalate, the mock does not commit. The commit boundary is observable. |
| **Source systems (policy repo, HR records)** | No real enterprise data | Synthetic documents with realistic structure, ACLs, and content. See §3 for exact corpus requirements. |
| **Identity / principal** | No real IAM | Simulated caller principals with explicit role-to-ACL mappings. The entitlement check runs against these exactly as it would against a real IAM. |

### Completely Out of Scope (Re-affirmed from R2S1)

| Exclusion | Reason |
|---|---|
| Third live decision-support / bias route | Bias is distributional + async; contaminates the claim→action critical path |
| Per-response bias verdicts | Contrary to frozen architecture |
| Production-scale load test | Prototype proves mechanism, not throughput |
| Real customer/employee PII | Unnecessary for mechanism proof; privacy risk |
| Live enterprise IAM remediation | ControlPlane enforces ACLs; does not repair IAM |
| LLM-as-judge on critical path | Destroys provenance/entitlement differentiation |
| Confidence / logprob / global risk scores | The named failure is confidently wrong; confidence cannot be the detector |
| Open-web factual verification | Binding limited to captured provenance set |
| Generative full-answer rewrite | Edit is surgical only |
| Fabricated production FNR | Emptiness is the credibility play |
| Lane 3 as critical-path demo | Off critical path by construction |
| Dead compute as centrepiece | Secondary to admission control; may be narrated briefly |
| Model weights, logits, fine-tuning | API-layer only |

---

## 3. Synthetic Data & Corpora Requirements

### Source System A — Policy Repository (Customer Support + Vendor Agreements)

**Structure:** 15–20 documents. Each document has:

```
{
  doc_id: string,
  title: string,
  content: string,
  ACL: { read: [role_list] },
  content_hash: string
}
```

**Required documents (minimum):**

| Doc ID | Title | Content | ACL | Purpose |
|---|---|---|---|---|
| `POL-001` | Vendor Refund Policy — Standard Terms | Defines refund eligibility for standard vendor agreements. Specifies that refunds above ₹1,00,000 require director approval. Lists clauses 1–6. **Clause 7 does not exist in this document.** | `[agent, supervisor, customer]` | Ground truth for clause 7.2 absence. The claim "clause 7.2 permits this refund" will find no span. |
| `POL-002` | Vendor Refund Policy — Premium Terms | Defines refund eligibility for premium vendors. Higher thresholds. Clauses 1–5 only. | `[agent, supervisor]` | Additional policy context; no clause 7.2 here either. |
| `POL-003` | Refund Processing SOP | Step-by-step for processing refunds. Includes: "Refunds above ₹50,000 require supervisor sign-off before processing." | `[agent, supervisor, ops]` | Numeric claim: "Refunds above ₹50,000 require supervisor sign-off." Deterministic recomputation target. |
| `POL-004` | Customer Communication Guidelines | What to say to customers about refund status. Includes: "Never disclose internal approval thresholds to customers." | `[agent, supervisor, customer]` | Entitlement: this doc is customer-readable, so claims grounded here pass entitlement. |
| `POL-005` | Internal Approval Matrix | Lists approval thresholds by refund amount. Contains: "₹1,00,001–₹5,00,000: Director approval required." | `[supervisor, director]` — **NOT `[customer]` or `[agent]`** | Entitlement violation: if the model cites this document's threshold in customer-visible text, the span's ACL excludes the customer principal. |
| `POL-006` | Vendor Agreement — Acme Corp | Specific agreement with Acme Corp. Clauses 1–8. Clause 7.1 covers warranty claims. **No clause 7.2.** | `[agent, supervisor, legal]` | The model might hallucinate 7.2 by conflating 7.1. Absence is provable. |
| `POL-007` through `POL-015` | Various operational docs | Mix of broadly accessible and restricted documents covering shipping, returns, escalation procedures, etc. | Varied | Volume for realistic retrieval; some with restricted ACLs for entitlement testing. |

### Source System B — Internal Knowledge Base (HR + Operations)

**Structure:** 10–15 documents. Same schema.

**Required documents (minimum):**

| Doc ID | Title | Content | ACL | Purpose |
|---|---|---|---|---|
| `KB-001` | Parental Leave Policy 2025 | "Full-time employees are entitled to 26 weeks of paid parental leave. Part-time employees receive pro-rated leave based on hours." | `[hr, all_employees]` | Clean supported path. Claim "full-time employees get 26 weeks parental leave" binds to this span. |
| `KB-002` | Salary Band — Engineering Manager | "Engineering Manager, Grade 7: ₹18,00,000 – ₹24,00,000 per annum." | `[hr, finance]` — **NOT `[engineering]` or `[all_employees]`** | Entitlement violation: an Engineering employee querying salary bands should not see this. The claim is semantically correct but the caller is not entitled. |
| `KB-003` | Office Locations | "Headquarters: Gandhinagar. Branch offices: Mumbai, Bangalore, Hyderabad." | `[all_employees]` | Clean supported path with broad ACL. |
| `KB-004` | IT Equipment Policy | "Employees may request one laptop replacement every 3 years. Approval from IT manager required." | `[all_employees, it]` | Numeric claim for recomputation: "every 3 years." |
| `KB-005` | Confidential: Upcoming Restructuring | "Q3 restructuring will affect the Pune office. 47 positions to be relocated." | `[director, hr_lead]` — **extremely restricted** | If the model hallucinates or leaks this, entitlement violation is caught. |
| `KB-006` through `KB-010` | Various operational docs | Mix of accessible and restricted | Varied | Volume for realistic retrieval. |

### Caller Principals (Simulated)

| Principal ID | Role | Entitled Sources | Purpose |
|---|---|---|---|
| `cust-001` | Customer (external) | `POL-001` (customer-readable), `POL-004` | Refund route: customer sees text. Cannot see `POL-005` (internal approval matrix). |
| `agent-001` | Support Agent | `POL-001`–`POL-007`, `KB-001`, `KB-003`, `KB-004` | Refund route: agent processes the refund. Can see internal policies but not HR salary bands. |
| `emp-eng-001` | Engineering Employee | `KB-001`, `KB-003`, `KB-004` | Knowledge route: employee queries. Cannot see `KB-002` (salary bands) or `KB-005` (restructuring). |
| `emp-hr-001` | HR Employee | `KB-001`–`KB-006` (all) | Knowledge route: HR employee queries. Can see salary bands. Same claim, different entitlement outcome. |

### Pre-Scripted Model Responses

**Response R1 — Refund Agent (the running example):**

> "Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement. The refund will be processed within 5–7 business days. Per the internal approval matrix, refunds above ₹1,00,000 require director sign-off, which has been obtained."

**Claims extracted:**

| # | Claim Text | Type | Assertion | Expected Verdict | Expected Binding |
|---|---|---|---|---|---|
| C1 | "Refund of ₹1,84,000 issued" | Numeric | Categorical | SUPPORTED | Binds to order record span showing ₹1,84,000 refund amount |
| C2 | "under clause 7.2 of the vendor agreement" | Policy/factual | Categorical | **UNSUPPORTED** | No span contains clause 7.2. Absence, not contradiction. |
| C3 | "refund will be processed within 5–7 business days" | Numeric/temporal | Categorical | SUPPORTED | Binds to `POL-003` SOP span |
| C4 | "refunds above ₹1,00,000 require director sign-off" | Numeric/policy | Categorical | SUPPORTED | Binds to `POL-005` span |
| C5 | "which has been obtained" | Factual | Categorical | UNSUPPORTED | No span confirms director sign-off was obtained for this specific refund |

**Entitlement finding on C4:** The span from `POL-005` has ACL `[supervisor, director]`. The customer principal `cust-001` is not in this list. Entitlement violation.

**Pending actions:**

| Action | R Tier | Findings | Matrix Cell | Actuator |
|---|---|---|---|---|
| Show text to customer | R1 | C4 grounded in span with ACL excluding `cust-001` | R1 × entitlement violation | **Edit** — strip C4 and C5 from customer-visible text |
| Issue refund of ₹1,84,000 | R3 | C2 (clause 7.2) has no supporting span | R3 × unsupported-categorical | **Escalate** — held with evidence packet |

**Response R2 — Knowledge Assistant (Engineering Employee):**

> "You are entitled to 26 weeks of paid parental leave as a full-time employee. The Engineering Manager salary band for Grade 7 is ₹18,00,000 – ₹24,00,000 per annum."

**Claims extracted:**

| # | Claim Text | Type | Assertion | Expected Verdict | Expected Binding |
|---|---|---|---|---|---|
| C6 | "26 weeks of paid parental leave as a full-time employee" | Numeric/policy | Categorical | SUPPORTED | Binds to `KB-001` |
| C7 | "Engineering Manager salary band for Grade 7 is ₹18,00,000 – ₹24,00,000" | Numeric | Categorical | SUPPORTED | Binds to `KB-002` |

**Entitlement finding on C7:** `KB-002` ACL is `[hr, finance]`. Principal `emp-eng-001` is not in this list. Entitlement violation.

**Pending action:**

| Action | R Tier | Findings | Matrix Cell | Actuator |
|---|---|---|---|---|
| Show answer to employee | R1 | C7 grounded in span with ACL excluding `emp-eng-001` | R1 × entitlement violation | **Edit** — strip C7 |

**Response R3 — Knowledge Assistant (HR Employee, same query):**

Same response text as R2. Same claims. Same bindings. **Different entitlement outcome:** `KB-002` ACL is `[hr, finance]`. Principal `emp-hr-001` has role `hr`. Entitlement passes. Both claims SUPPORTED, both entitled.

| Action | R Tier | Findings | Matrix Cell | Actuator |
|---|---|---|---|---|
| Show answer to employee | R1 | All claims supported and entitled | R1 × supported | **Pass** |

This is the principal-flip proof: same claim, same span, different principal, different outcome. Zero LLM in the ACL decision.

---

## 4. Core Components to Implement

### Layer 1 — Provenance (Build First)

| # | Component | Responsibility | Real/Mock |
|---|---|---|---|
| 1 | **Provenance Recorder** | Intercepts context assembly; for every retrieved chunk or tool result, records `source_id`, `ACL`, `content_hash`, `offsets`, `principal` into the Evidence Ledger before the model receives the context | **Real** |
| 2 | **Source Store** | Holds synthetic documents with ACLs; returns spans on retrieval | **Mock** (in-memory, seeded with §3 corpora) |
| 3 | **Principal Store** | Holds caller identities with role-to-ACL mappings | **Mock** (in-memory, seeded with §3 principals) |
| 4 | **Evidence Ledger** | Append-only, hash-chained data structure; one per request; stores spans, claims, bindings, verdicts, actions, latency | **Real** |

### Layer 2 — Extraction & Binding

| # | Component | Responsibility | Real/Mock |
|---|---|---|---|
| 5 | **Claim Extractor** | Receives streamed model output; buffers to sentence boundaries; emits typed check-worthy propositions tagged categorical or hedged | **Real** (deterministic patterns for numeric/ID/date + regex/rule-based for policy claims; can use small model if available) |
| 6 | **Numeric Recomputer** | For numeric/date/identifier claims: extracts the value from the claim, searches the span set for matching values, returns SUPPORTED if exact match found, UNSUPPORTED otherwise | **Real** (deterministic arithmetic; sub-millisecond) |
| 7 | **NLI Binder** | For textual/factual claims: runs cross-encoder entailment against each candidate span from the provenance set; returns SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN | **Real** (DeBERTa-v3-base or equivalent; ~300M; local inference; 5–15ms batched) |
| 8 | **Derived Claim Handler** | For multi-hop/aggregative claims: attempts recomputation from spans; if neither recomputable nor directly entailed, returns UNKNOWN | **Real** (rule-based; returns UNKNOWN for anything not recomputable) |

### Layer 3 — Decision

| # | Component | Responsibility | Real/Mock |
|---|---|---|---|
| 9 | **Entitlement Auditor** | For every claim that binds to a span: checks whether the calling principal's role is in the span's ACL. Returns entitled or violation. Zero LLM. Lane 1. | **Real** (deterministic set-membership; microseconds) |
| 10 | **Action Interlock** | Receives all claim verdicts + entitlement results; identifies pending actions from the response; computes R-tier per action from route config; applies exact frozen R×S matrix; emits actuator per action | **Real** (pure rule engine; zero LLM; the matrix is a hardcoded lookup table) |
| 11 | **Route Configuration** | Per-route policy profile: action-to-R mapping, lane budgets, fail stance, enforcement mode | **Real** (typed config objects; two routes defined) |

### Layer 4 — Actuation

| # | Component | Responsibility | Real/Mock |
|---|---|---|---|
| 12 | **Surgical Editor** | On Edit: strips the failing claim (and any claims that depend on it) from the output; re-gates the edited result; second failure → Escalate | **Real** |
| 13 | **Evidence Packet Builder** | On Escalate: assembles claim text + candidate spans searched + verdict + diff between claim and best-available span | **Real** |
| 14 | **Mock Refund Tool** | Simulates payment API; accepts commit command or rejects it; honors interlock result (does not commit if Escalate/Block) | **Mock** (deterministic; real gate semantics) |
| 15 | **Text Hold-Back Buffer** | Delays text release by ~150–300ms to allow inline verification; text streams after buffer clears unless Edit is triggered | **Real** |

### Layer 5 — Reporting & UI

| # | Component | Responsibility | Real/Mock |
|---|---|---|---|
| 16 | **FNR Gate Report** | Per-route typed schema with null/placeholder fields; no fabricated numbers | **Real** (schema only) |
| 17 | **Evidence Ledger UI** | Renders the full `STEP → SPAN → CLAIM → ACTION` graph; highlights matrix cells; shows evidence packets; displays latency; majority of screen real estate | **Real** |
| 18 | **Latency Tracker** | Measures and displays p50/p95 per route, per lane | **Real** |

### Not Implemented (Confirmed Out of Scope)

- Lane 3 components (semantic-entropy, counterfactual bias replay, calibration)
- Adjudicator (shadow audit ground-truth sampling)
- Red Team (offline adversarial probing)
- Economist (dead compute backward walk — may be narrated, not implemented)
- Circuit breaker / autonomy downgrade logic
- Policy validation pipeline (shadow replay → canary → auto-rollback)
- Multi-turn session ledger accumulation

---

## 5. Demo Flows (Judge-Facing)

### Governing Rule

Demo builds **backward from the action gate**. First visible crisis = pending refund held. The judge sees the interlock before anything else. The graph is majority UI. Total target: **≤8 minutes**.

---

### Primary Flow — Refund Dual-Action (Target: 4 minutes)

**Step 1 — Setup (30 seconds)**

Screen shows: route configuration for "Customer Support Refund Agent." Two source systems listed with ACLs. Principal `cust-001` (customer) and `agent-001` (agent) visible. The judge sees the provenance landscape before any query runs.

**Step 2 — Context Assembly (30 seconds)**

Agent processes a refund request. The Provenance Recorder captures spans in real time. The Evidence Ledger populates:

```
STEP: retrieval → SPAN: POL-001 (ACL: agent, supervisor, customer) hash: a3f2...
STEP: retrieval → SPAN: POL-003 (ACL: agent, supervisor, ops)     hash: b7c1...
STEP: retrieval → SPAN: POL-005 (ACL: supervisor, director)       hash: d9e4...
STEP: retrieval → SPAN: POL-006 (ACL: agent, supervisor, legal)   hash: f1a8...
STEP: tool_call → SPAN: order_record (ACL: agent, customer)       hash: c2b5...
```

The judge sees every span with source, ACL, hash, and offsets **before** any claim is judged. The model has not yet produced output. The provenance is the ground truth of what the model was allowed to know.

**Step 3 — Model Output Streams (30 seconds)**

The pre-scripted refund response streams token-by-token behind the hold-back buffer:

> "Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement..."

The judge sees the text appearing. The hold-back buffer is visible (a subtle indicator showing verification is running in parallel).

**Step 4 — Claim Extraction (30 seconds)**

The Claim Extractor decomposes the output into 5 claims. Each appears in the ledger:

```
C1: "Refund of ₹1,84,000 issued"           [numeric, categorical]     → UNSUPPORTED
C2: "under clause 7.2 of the vendor agreement" [policy, categorical]   → UNSUPPORTED
C3: "processed within 5–7 business days"     [numeric, categorical]    → UNSUPPORTED
C4: "refunds above ₹1,00,000 require director sign-off" [policy, cat] → UNSUPPORTED
C5: "which has been obtained"                [factual, categorical]    → UNSUPPORTED
```

Every claim starts red (UNSUPPORTED). The judge sees the default enforced in real time.

**Step 5 — Binding (45 seconds)**

The binding engine runs. The judge sees claims transition from red to green as bindings are found:

- C1 → Numeric recomputation against order_record span → ₹1,84,000 matches → **SUPPORTED** (green)
- C2 → Searches all spans for "clause 7.2" → no span found → stays **UNSUPPORTED** (red). The judge sees: absence, not contradiction. No span says "clause 7.2 does not exist" — there is simply no span that says it does.
- C3 → Numeric/temporal recomputation against POL-003 span → "5–7 business days" matches → **SUPPORTED** (green)
- C4 → NLI binding against POL-005 span → entailment confirmed → **SUPPORTED** (green)
- C5 → Searches for confirmation of director sign-off → no span → stays **UNSUPPORTED** (red)

**Step 6 — Entitlement Check (15 seconds)**

The Entitlement Auditor checks every SUPPORTED claim's span against the customer principal `cust-001`:

- C1: order_record ACL includes `customer` → entitled
- C3: POL-003 ACL includes `agent` but not `customer` → **entitlement violation** (the customer should not see internal SOP details — but for the demo, the critical finding is on C4)
- C4: POL-005 ACL is `[supervisor, director]` → `cust-001` is not in this list → **entitlement violation**

The judge sees: the claim is semantically SUPPORTED (the span does say refunds above ₹1,00,000 require director sign-off), but the customer is not entitled to see this information. This is not "the model said something sensitive" — it is authorization as set-membership. Zero LLM.

**Step 7 — The Matrix (45 seconds) — THE MOMENT**

The Action Interlock identifies two pending actions:

**Action 1: Show text to customer (R1)**

- Worst claim in the text that affects this action: C4 (SUPPORTED but entitlement violation)
- Matrix lookup: R1 × entitlement violation → **Edit**
- The judge sees the matrix cell highlighted. The actuator fires: C4 and C5 are surgically stripped from the customer-visible text. The edited text re-enters the gate and passes.

**Action 2: Issue refund of ₹1,84,000 (R3)**

- Worst claim that affects this action: C2 (UNSUPPORTED + categorical — clause 7.2 has no span)
- Matrix lookup: R3 × unsupported-categorical → **Escalate**
- The judge sees the matrix cell highlighted. The actuator fires: the refund is **held**. The mock refund tool does **not** commit. The evidence packet appears on screen:

```
EVIDENCE PACKET — ESCALATE
─────────────────────────────
Claim: "under clause 7.2 of the vendor agreement"
Verdict: UNSUPPORTED (categorical)
Candidate spans searched: POL-001, POL-002, POL-006 (vendor agreement docs)
Best match: POL-006 clause 7.1 (warranty claims — not refund authorization)
Diff: Claim asserts clause 7.2 permits refund. No span found for clause 7.2.
      Nearest: clause 7.1 covers warranty, not refund authorization.
Action: Refund of ₹1,84,000 HELD. Escalated to supervisor.
─────────────────────────────
```

**Both actuators are correct simultaneously.** The judge sees: one response, one graph, two pending actions, two different actuators. The refund is never described as "blocked" — it is held and escalated with the evidence packet.

**Step 8 — The Close (15 seconds)**

Screen shows the complete Evidence Ledger for this request. The FNR gate report schema appears with null/placeholder values. The judge sees the format — emptiness is the credibility play.

---

### Secondary Flow — Principal-Flip Entitlement (Target: 2.5 minutes)

**Step 1 — Same Query, Different Principal (30 seconds)**

Switch to the Knowledge route. The query is: "What is the parental leave policy and the Engineering Manager salary band?"

**Step 2 — Context Assembly for Engineering Employee (30 seconds)**

Principal: `emp-eng-001` (Engineering). Spans captured:

```
STEP: retrieval → SPAN: KB-001 (ACL: hr, all_employees)  hash: x1...
STEP: retrieval → SPAN: KB-002 (ACL: hr, finance)         hash: x2...
```

**Step 3 — Model Output + Claim Extraction + Binding (45 seconds)**

Response streams. Two claims extracted:

- C6: "26 weeks of paid parental leave" → binds to KB-001 → **SUPPORTED**
- C7: "Engineering Manager salary band ₹18L–₹24L" → binds to KB-002 → **SUPPORTED**

Both claims are semantically correct. Both bind to real spans.

**Step 4 — Entitlement Check (15 seconds)**

- C6: KB-001 ACL includes `all_employees` → `emp-eng-001` entitled
- C7: KB-002 ACL is `[hr, finance]` → `emp-eng-001` is Engineering, not HR or Finance → **entitlement violation**

Matrix: R1 × entitlement violation → **Edit**. C7 stripped from the response. The employee sees the parental leave answer but not the salary band.

**Step 5 — Flip the Principal (30 seconds)**

The judge sees: change **only** the calling principal to `emp-hr-001` (HR). Re-run the same query, same spans, same claims, same bindings.

- C7: KB-002 ACL is `[hr, finance]` → `emp-hr-001` has role `hr` → **entitled**

Matrix: R1 × supported → **Pass**. The HR employee sees the full answer including the salary band.

**The judge sees:** same claim, same span, same semantic correctness, different principal, different outcome. The entitlement check is set-membership, not text classification. Zero LLM in the ACL decision path. This is structurally impossible for any output-only competitor to replicate.

---

### Optional Third Beat — R-Tier Changes Actuator (Target: 1.5 minutes)

**Only if time permits and it strengthens without cluttering.**

Show: the same unsupported-categorical claim (clause 7.2) at two different R tiers.

- At R1 (showing draft to agent for review): R1 × unsupported-categorical → **Edit** (strip the clause reference)
- At R3 (issuing the refund): R3 × unsupported-categorical → **Escalate** (hold with evidence packet)

The judge sees: the verdict is identical. The actuator changes because R changed, not because a confidence score changed. **Proof scales with consequence.**

---

## 6. Evidence Ledger & UI Requirements

### Governing Test

> "If the judge can remove the graph from the screen and the demo still looks the same, the scope has already failed."

The Evidence Ledger must be the **majority of screen real estate** — not a sidebar, not a collapsible panel, not a chatbot window with a small log underneath.

### What Must Be Visible

| Element | Position | What the Judge Sees |
|---|---|---|
| **STEP → SPAN → CLAIM → ACTION graph** | Center, dominant | The full graph building in real time. Spans appear as context is assembled. Claims appear as they are extracted. Bindings appear as verdicts are computed. Actions appear as the interlock decides. |
| **Span details** | On hover or inline | For each span: `source_id`, `ACL`, `content_hash`, `offsets`. The judge can verify that provenance was captured before claims were judged. |
| **Claim verdicts** | Inline in the graph | Each claim shows its verdict (UNSUPPORTED → SUPPORTED/UNKNOWN) with the binding evidence. Color-coded: red = UNSUPPORTED, green = SUPPORTED, amber = UNKNOWN, purple = entitlement violation. |
| **Matrix cell highlight** | Overlay or side panel | When the interlock decides, the exact R×S matrix cell is highlighted. The judge sees which cell produced which actuator. |
| **Actuator output** | Below the graph | For Edit: the stripped text with the failing claim removed. For Escalate: the evidence packet (claim, candidate spans, verdict, diff). For Pass: confirmation. |
| **Mock tool status** | Bottom bar | For the refund: "COMMIT BLOCKED — Escalate in force" or "COMMIT PENDING — awaiting interlock." The commit boundary is observable. |
| **FNR schema** | Side panel | Per-route gate report with null/placeholder fields. Visible but not dominant. |
| **Latency readout** | Bottom bar | Per-lane latency for the current request. |

### What Must NOT Be Visible

- Chatbot chrome (the conversation UI is not the product)
- Confidence scores or trust scores
- Composite risk scores
- LLM-as-judge output
- "Response blocked" language
- Dashboard charts or trend graphs (these are business-proposal artifacts)

### Interaction Model

The demo is **interactive, not pre-recorded**. The judge should be able to:

1. See the graph build in real time (not instant reveal)
2. Hover over spans to see ACL and hash
3. See the matrix cell before the actuator fires (the interlock's decision is visible before it executes)
4. Trigger the principal-flip and see the entitlement outcome change
5. See that the mock refund tool does not commit when Escalate is in force

If claims are pre-extracted for demo stability, the binding step must exhibit **real compute latency** (NLI inference takes 5–15ms per claim) so the judge can verify the engine is running, not playing an animation.

---

## 7. Success Criteria → Implementation Checks

Every binary criterion from R2S1 §5 mapped to a concrete runtime check:

| # | Criterion | Implementation Check |
|---|---|---|
| 1 | Provenance outside the model | **Assertion in Provenance Recorder:** every span written to the ledger has non-null `source_id`, `ACL`, `content_hash`, `offsets`. The ledger entry timestamp for span capture must precede the claim extraction timestamp. The judge can verify this by inspecting the ledger. |
| 2 | One-graph invariant | **Structural check:** the UI renders exactly one `STEP → SPAN → CLAIM → ACTION` ledger per request. No separate hallucination/privacy/action detector views exist. |
| 3 | UNSUPPORTED default is real | **Runtime check:** every claim emitted by the Claim Extractor enters the ledger with verdict = `UNSUPPORTED`. The Binding Engine is the only component that can change a verdict to SUPPORTED. Log the initial verdict before binding runs. |
| 4 | Absence ≠ contradiction | **Corpus check:** clause 7.2 does not exist in any document in the source store. **Runtime check:** the binding engine returns `UNSUPPORTED` (not `CONTRADICTED`) for C2. The evidence packet text never uses "caps," "denies," or "doesn't cover." |
| 5 | Claim-level proof works | **Visual check:** the judge sees C1 transition from red to green with a specific span reference. The judge sees C2 remain red with "no span found." |
| 6 | Two pending actions resolve independently | **Runtime check:** the interlock emits two actuator records for the refund response — one for R1 (Edit) and one for R3 (Escalate). Both are visible in the ledger. They are not collapsed into one response-level verdict. |
| 7 | Hard action gate is real | **Mock tool check:** the mock refund tool's `commit()` method checks the interlock result. If the interlock says Escalate or Block, `commit()` returns `BLOCKED_BY_INTERLOCK`. The UI shows "COMMIT BLOCKED." The judge can verify that no money moved. |
| 8 | Entitlement independence | **Principal-flip check:** the same query run under `emp-eng-001` and `emp-hr-001` produces different entitlement outcomes for C7. The ACL check log shows the set-membership test with no LLM call. |
| 9 | Exact matrix fidelity | **Code check:** the Action Interlock contains a hardcoded lookup table matching the exact frozen R×S matrix. No dynamic threshold, no learned boundary, no composite score. The matrix is a constant, not a function of anything except R and S. |
| 10 | Evidence packet | **Visual check:** on Escalate, the judge sees claim text + candidate spans searched + verdict + diff. The packet is self-contained — the human does not need to reconstruct reasoning from raw logs. |
| 11 | Surgical edit | **Runtime check:** on Edit, the failing claim is removed from the output. The edited output re-enters the gate. If the edited output still fails, it falls through to Escalate. No free-form rewrite occurs. |
| 12 | FNR format honesty | **Visual check:** the gate report schema is visible with null/placeholder values. No fabricated percentages. The `status` field reads `"not_yet_populated"` or `"prototype_corpus_only"`. |
| 13 | No confidence driver | **Code check:** the Action Interlock's input is `(R_tier, verdict_severity)`. There is no confidence score, trust score, or risk score in the decision path. The actuator is traceable to the matrix cell, not to a scalar. |
| 14 | Prompt injection cannot author provenance | **Architecture check:** the Provenance Recorder hooks context assembly, which occurs before the model runs. The model has no channel to write to the ledger. Injected instructions in the user query cannot create spans or binding edges. |
| 15 | Refund language fidelity | **String check:** nowhere in the UI, evidence packet, or demo voice does the word "blocked" appear in reference to the R3 refund outcome. The word is "held" and "escalated." |

---

## 8. Build Order Recommendation

The build order is designed so the team **never loses the differentiation moment**. At every stage, the team has a working demo that proves the core thesis. If time runs out at any stage, the demo still works — it just shows fewer beats.

### Phase 1 — The Keystone (Days 1–3)

**Build:** Provenance Recorder + Source Store + Evidence Ledger + one pre-scripted refund trace.

**Why first:** Without the Provenance Recorder, every other mechanism degrades to a generic guardrail. This is the component that makes the architecture different. Build it, run one trace, verify that spans appear in the ledger before claims are judged. The team now has a working demo that shows provenance outside the model.

**Demo at this stage:** Context assembly → spans in ledger → model output → claims extracted → all UNSUPPORTED. No binding yet. The judge sees the default enforced.

### Phase 2 — The Binding (Days 4–6)

**Build:** Claim Extractor + Numeric Recomputer + NLI Binder + Derived Claim Handler.

**Why second:** Binding is what turns UNSUPPORTED into SUPPORTED (or keeps it red). Without binding, the demo cannot show the clause 7.2 absence. Build the numeric recomputer first (deterministic, fast, high confidence), then the NLI binder (requires model download and integration), then the derived handler (simplest — returns UNKNOWN).

**Demo at this stage:** Full refund trace with claims transitioning from red to green (or staying red for clause 7.2). The judge sees claim-level proof working.

### Phase 3 — The Matrix (Days 7–9)

**Build:** Entitlement Auditor + Action Interlock + Route Configuration + Mock Refund Tool.

**Why third:** This is the moment that separates the pitch from every guardrail demo. The Entitlement Auditor catches the ACL violation. The Action Interlock applies the matrix and produces two different actuators. The mock refund tool demonstrates the hard gate. Build the entitlement auditor first (deterministic, zero LLM, the most differentiated mechanism), then the interlock (pure rule engine, hardcoded matrix), then the mock tool.

**Demo at this stage:** Full primary flow — refund dual-action. The judge sees R1 → Edit and R3 → Escalate simultaneously. The refund is held. The evidence packet appears. This is the centrepiece.

### Phase 4 — The Proof (Days 10–11)

**Build:** Surgical Editor + Evidence Packet Builder + Text Hold-Back Buffer.

**Why fourth:** These complete the actuation layer. The surgical editor makes Edit real (not just a label). The evidence packet builder makes Escalate useful (not just a hold). The hold-back buffer makes the latency story honest.

**Demo at this stage:** Full primary flow with real edit and real evidence packet. The judge sees the failing claim stripped and the packet assembled.

### Phase 5 — The Flip (Days 12–13)

**Build:** Knowledge route configuration + KB source store + principal-flip trace.

**Why fifth:** The principal-flip is the second-strongest demo moment. It proves entitlement is set-membership, not text classification. Build the knowledge route config, seed the KB source store, script the two traces (engineering employee vs HR employee).

**Demo at this stage:** Full primary flow + secondary flow. The judge sees the dual-action and the entitlement flip.

### Phase 6 — The Polish (Days 14–15)

**Build:** FNR schema + latency tracker + UI refinement + optional third beat.

**Why last:** These are credibility and presentation artifacts. The FNR schema is a typed placeholder — it takes an hour to build. The latency tracker is a timer — it takes an afternoon. UI refinement is making the Evidence Ledger dominant on screen. The optional third beat (R-tier changes actuator) is a nice-to-have that only matters if the first two flows are solid.

**Demo at this stage:** Complete prototype. All 15 success criteria passable. ≤8 minutes. The judge can point from action to claim to span to principal and mark every criterion yes/no.

---

## 9. Fidelity Self-Check

| Frozen Invariant | Status in This Specification | Evidence |
|---|---|---|
| **Default = UNSUPPORTED** | **Protected.** §4 Component 5 (Claim Extractor): every claim enters the ledger as UNSUPPORTED. §5 Primary Flow Step 4: "Every claim starts red." §7 Criterion 3: runtime check that initial verdict is UNSUPPORTED before binding. | |
| **Entitlement / ACL check** | **Protected.** §4 Component 9 (Entitlement Auditor): deterministic set-membership, zero LLM, Lane 1. §5 Secondary Flow: principal-flip proves it is set-membership. §7 Criterion 8: runtime check with two principals. | |
| **Exact R×S matrix** | **Protected.** §4 Component 10 (Action Interlock): "hardcoded lookup table matching the exact frozen R×S matrix." §7 Criterion 9: "a constant, not a function of anything except R and S." The matrix is transcribed in §5 Primary Flow Step 7. | |
| **Hard gate on actions** | **Protected.** §4 Component 14 (Mock Refund Tool): "honors interlock result." §5 Primary Flow Step 7: "the mock refund tool does not commit." §7 Criterion 7: runtime check that commit is blocked. | |
| **FNR as empty typed schema** | **Protected.** §4 Component 16: "schema only; no fabricated numbers." §7 Criterion 12: "null/placeholder values." §5 Primary Flow Step 8: "FNR gate report schema appears with null/placeholder values." | |
| **Two-pending-actions resolution** | **Protected.** §5 Primary Flow Steps 7: two actuators from one response. §7 Criterion 6: "two actuator records... not collapsed into one response-level verdict." The matrix cells are explicitly shown. | |
| **No LLM-as-judge on critical path** | **Protected.** §4: no component in Layers 1–4 uses LLM-as-judge. The Claim Extractor may use a small model for extraction, but the decision policy (Action Interlock) is a pure rule engine. The NLI Binder is an entailment model, not a judge. §7 Criterion 13: "no confidence score, trust score, or risk score in the decision path." | |
| **No per-response bias verdict** | **Protected.** §2: bias measurement is confirmed out of scope for the prototype. No component produces a per-response bias verdict. §5: no demo flow includes bias. | |
| **Never say "blocked" about the refund** | **Protected.** §5 Primary Flow Step 7: "the refund is never described as 'blocked' — it is held and escalated with the evidence packet." §7 Criterion 15: string check. | |
| **Surgical edit only** | **Protected.** §4 Component 12: "strips the failing claim... no free-form rewrite." §7 Criterion 11: "no free-form rewrite occurs." | |
| **Evidence-packet escalation** | **Protected.** §4 Component 13: "assembles claim text + candidate spans + verdict + diff." §5 Primary Flow Step 7: full packet shown. §7 Criterion 10: "self-contained." | |
| **One graph, three reads** | **Protected.** §4 Component 4: "one per request." §6: "one STEP → SPAN → CLAIM → ACTION ledger per request." §7 Criterion 2: structural check. | |

**No competing mechanism enters the prototype.** LLM-as-judge, confidence thresholding, composite risk scores, open-web verification, per-response bias classifiers, and redrawn matrices are all absent from the component list, the demo flows, and the implementation checks.

**No tension identified. Nothing in this specification contradicts, softens, or reinterprets any frozen invariant.**

---

*Stage 3 complete. The prototype is specified to the level where a serious engineer can begin building on day one. The build order ensures the differentiation moment is never at risk. Every success criterion has a concrete implementation check. The frozen architecture is preserved without exception.*