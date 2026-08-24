# Stage 3: Prototype Specification

> Accenture Innovation Challenge 2026 · Round 2 · Stage 3  
> Sources of truth (absolute): `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` · `R2S2.md`  
> Status: **FROZEN inputs non-negotiable.** This document converts frozen architecture into a buildable, demonstrable prototype definition.

---

## 1. Prototype Goal

This prototype exists to prove one thing: that provenance captured outside the model, combined with an inverted burden of proof and a blast-radius-priced matrix, can intercept an unproven claim before it authorizes an irreversible action — and that the identical graph produces two different actuators on two different pending actions from the same response. Everything else is excluded to protect this proof.

---

## 2. Exact Functional Scope

### Implemented and runnable

| Component | Implementation form | Notes |
|---|---|---|
| Provenance Recorder | Real. Accepts pre-loaded span sets, attaches `source_id · ACL · hash · offsets` to an in-memory store keyed by request ID. | No hook into a real retrieval system — spans are loaded before the demo trace begins. |
| Evidence Ledger | Real. Append-only in-memory structure per request, one typed `STEP → SPAN → CLAIM → ACTION` graph. | Serialised to JSON on completion for audit inspection. |
| Claim Extractor | **Pre-computed claims with live timestamps.** Claims are extracted in advance and stored with their trigger position (token offset in the simulated stream). At runtime, they appear in the ledger at the correct moment. | Pre-computation eliminates non-determinism. The binding step still runs live (§5). |
| Numeric / structural recomputation | Real. Regex extraction of numbers, dates, identifiers from claim text; deterministic comparison against span content. Sub-millisecond. | Demonstrated on at least one claim. |
| NLI binding | **Real and live.** A local cross-encoder (~300M, e.g., DeBERTa-v3-base MNLI) runs against the provenance set only when a textual claim triggers Lane 2. | This is the proof the engine is running, not a recording. Visible compute latency (~20–80ms) on the binding edge. |
| Entitlement Auditor | Real. Set-membership: `principal ∈ span.ACL.allowed_principals`. Pure dictionary lookup. Zero model calls. | Runs on every bound claim in Lane 1. |
| Action Interlock | Real. Computes R from the pending action's class + route config. Looks up `R × S` in the frozen matrix. Emits the actuator. Pure rule engine. | No model. No score. |
| Hard gate on action | Real. The mock refund tool accepts an `allowed` flag from the Interlock. If the actuator is `Escalate` or `Block`, `allowed = false`. The tool does not execute. | The gate is in the commit path, not the token stream. |
| Surgical edit (strip path) | Real. Removes the failing claim's sentence from the output text. Re-runs remaining claims through the gate (simplified: if no remaining claims fail, text passes). | Does not re-invoke a generator — stripping only, per the architecture's first edit option. |
| Evidence packet | Real. JSON structure: `{claim, candidate_spans: [{source_id, content, ACL, verdict}], final_verdict, diff}`. | Displayed in the UI when Escalate fires. |
| Per-claim user surface | Real. Each claim in the output panel shows exactly one label: `Verified` / `Uncertain` / `Blocked`. | No confidence percentage. No risk score. |
| Empty FNR schema | Real. JSON with typed null fields, displayed in a collapsible panel. | `measurement_status: "insufficient_sample"` for all routes. |
| Stream simulation | Real. Pre-recorded token sequence emitted at ~50 tokens/second with sentence-boundary triggers. | Not a live LLM call. The model is treated as a black box — consistent with the architecture. |
| Principal switch | Real. A UI control that changes the `principal` variable on the next trace run. Entitlement outcomes flip because ACL check is live set-membership. | The only interactive control in the demo. |

### Deliberately mocked

| Mock | What it simulates | Why not real |
|---|---|---|
| Model output stream | LLM generating the refund response | The architecture is API-layer-only; the model is a black box. Simulating the stream proves the control plane works without the model, which is the point. |
| Mock refund tool | `issue_refund(amount, clause_reference)` — prints "REFUND ISSUED" or "REFUND HELD" | Unsafe and unnecessary to execute a real payment. The gate semantics are identical. |
| Source systems | In-memory span store with hand-crafted ACLs | No real enterprise retrieval system is available. The mechanism is identical. |

### Completely out of scope (re-affirming R2S1 §3 exclusions)

Third live decision-support / bias route · per-response bias verdicts · production-scale load test · real payment execution · real customer/employee PII · live enterprise IAM integration · LLM-as-judge as primary verifier · confidence/logprob/global risk scores as disposition driver · open-web factual verification · generative full-answer rewrite · fabricated production FNR values · full regulatory certification / geography packs · Lane-3 as critical-path demo · full autonomous multi-agent swarm · human triage queue / SLA UI · dead-compute or non-convergence as centrepiece · model weights / logits / fine-tuning · any mechanism that cannot be shown as a read of the same `STEP → SPAN → CLAIM → ACTION` graph.

---

## 3. Synthetic Data & Corpora Requirements

All data is synthetic, enterprise-shaped, contains no real PII.

### Corpus A: Refund Agent (Use Case A)

**Source 1: Vendor Agreement (well-governed)**
- `source_id: "vendor-agreement-v3"`
- `ACL.allowed_principals: ["agent-cs-emea", "agent-cs-apa", "supervisor-finance"]`
- Contains: Clause 3.1 (refund eligibility criteria), Clause 5.4 (refund calculation method), Clause 8.2 (dispute resolution)
- **Deliberately does not contain Clause 7.2.** No span with "7.2" in the content.
- At least 8–10 spans extracted, each with `hash` and `offsets`.

**Source 2: Order Record (well-governed)**
- `source_id: "order-ORD-20250612-44891"`
- `ACL.allowed_principals: ["agent-cs-emea", "agent-cs-apa"]`
- Contains: order date, items, total amount `₹1,84,000`, payment method, current status
- At least 3–4 spans.

**Source 3: Internal Finance Memo (restricted)**
- `source_id: "finance-memo-Q1-refund-policy"`
- `ACL.allowed_principals: ["supervisor-finance", "director-ops"]`
- **Excludes `agent-cs-emea`.**
- Contains: internal guidance on refund thresholds and escalation procedures
- At least 2–3 spans.

**Pre-computed claims for the simulated response:**

| # | Claim text | Type | Assertion | Expected binding | Expected entitlement |
|---|---|---|---|---|---|
| C1 | "Order ORD-20250612-44891 was placed on June 12, 2025" | Numeric/temporal | Categorical | `SUPPORTED` — binds to order record span | `PASS` — principal in ACL |
| C2 | "The order total is ₹1,84,000" | Numeric | Categorical | `SUPPORTED` — recomputes against order span | `PASS` — principal in ACL |
| C3 | "Refunds above ₹1,00,000 require supervisor approval per internal policy" | Textual/factual | Categorical | `SUPPORTED` — binds to finance memo span | **ENTITLEMENT VIOLATION** — `agent-cs-emea` not in finance memo ACL |
| C4 | "Clause 7.2 of the vendor agreement permits this refund" | Textual/factual | **Categorical** | **UNSUPPORTED** — no span contains "7.2" | N/A (no binding) |
| C5 | "The refund will be processed within 5–7 business days" | Textual | Hedged | `SUPPORTED` — binds to clause 5.4 span | `PASS` |
| C6 | "The customer is eligible for a full refund under clause 3.1" | Textual/factual | Categorical | `SUPPORTED` — binds to clause 3.1 span | `PASS` |

**Pending actions on this response:**

| Action | R-tier | Worst claim (weighted by role in action) | S | Matrix cell | Actuator |
|---|---|---|---|---|---|
| Show text to customer | **R1** | C3 (entitlement violation — appears in the text the customer sees) | Contradicted / entitlement violation | R1 × Contradicted/entitlement | **Edit** — strip C3 |
| Issue refund `issue_refund(184000, "7.2")` | **R3** | C4 (clause 7.2 — the policy justification for the payment) | Unsupported + categorical | R3 × Unsupported+categorical | **Escalate** — held with evidence packet |

### Corpus B: Internal Knowledge Assistant (Use Case B)

**Source 4: HR Compensation Guide (restricted)**
- `source_id: "hr-comp-guide-2025"`
- `ACL.allowed_principals: ["hr-lead", "director-people", "vp-people"]`
- Contains: compensation band structures, bonus eligibility criteria
- At least 4–5 spans.

**Source 5: Engineering Handbook (open)**
- `source_id: "eng-handbook-v2"`
- `ACL.allowed_principals: ["*"]` (all principals)
- Contains: engineering processes, tooling standards
- At least 3–4 spans.

**Pre-computed claims for principal-flip demo:**

| # | Claim text | Binds to | Expected under `eng-lead-west` | Expected under `hr-lead` |
|---|---|---|---|---|
| D1 | "The standard engineering on-call rotation is 1 week per quarter" | eng-handbook-v2 | `SUPPORTED`, entitlement PASS | `SUPPORTED`, entitlement PASS |
| D2 | "Senior engineers in Band L6 are eligible for a 15% annual bonus" | hr-comp-guide-2025 | **UNSUPPORTED** (entitlement violation — `eng-lead-west` not in ACL) | `SUPPORTED`, entitlement PASS |

**R-tier for knowledge route:** R1 (user-visible, read-only). No pending action.

**Matrix cell for D2 under `eng-lead-west`:** R1 × Contradicted/entitlement → **Edit** (strip the claim).

### Corpus C: Clean / Supported Path (brief demonstration)

One additional claim that binds cleanly with no issues:

| # | Claim text | Binds to | Expected |
|---|---|---|---|
| E1 | "The vendor agreement was last updated on March 15, 2025" | vendor-agreement-v3 metadata span | `SUPPORTED`, entitlement PASS, R1 → **Pass** |

### Corpus D: Numeric Recomputation Case

| # | Claim text | Span says | Expected |
|---|---|---|---|
| F1 | "The refund amount is ₹1,85,000" | "₹1,84,000" | `CONTRADICTED` — recomputation fails (mismatch) |

This claim is included in the refund response as an additional failure mode if time permits. If excluded, the demo still passes — it is not in the critical path.

---

## 4. Core Components to Implement

| # | Component | Responsibility | Real or mock? |
|---|---|---|---|
| 1 | **Span Store** | Holds pre-loaded spans with `source_id · ACL · hash · offsets` keyed by `request_id`. Queried by the binder and entitlement auditor. | Real |
| 2 | **Provenance Recorder** | At demo start, populates the Span Store from the selected corpus. In production this hooks context assembly; in the prototype it loads from JSON. | Real (loads from JSON) |
| 3 | **Stream Simulator** | Emits pre-recorded token sequence at ~50 tok/s. Fires sentence-boundary events that trigger claim insertion into the ledger. | Mock (simulates model output) |
| 4 | **Claim Insertor** | On sentence-boundary event, inserts the pre-computed claim(s) for that sentence into the Evidence Ledger with verdict `UNSUPPORTED`. | Real (insertion logic; claims are pre-computed) |
| 5 | **Numeric Recomputer** | For numeric/date/ID claims: extracts values from claim text and span content via regex; compares deterministically. Sets verdict to `SUPPORTED` or `CONTRADICTED`. | Real |
| 6 | **NLI Binder** | For textual/factual claims: runs the local cross-encoder against the provenance set. Returns `SUPPORTED` / `CONTRADICTED` / `UNSUPPORTED`. Sets verdict. | **Real and live** — this is the compute-visible proof |
| 7 | **Derived Claim Router** | For any claim tagged as derived/aggregative: skips NLI, attempts recomputation from spans, or sets `UNKNOWN`. | Real |
| 8 | **Entitlement Auditor** | For each claim with a binding: checks `principal ∈ bound_span.ACL.allowed_principals`. Sets entitlement status. | Real — pure dictionary lookup, zero model |
| 9 | **R-Tier Resolver** | Maps each pending action to an R-tier using the route's action-to-R mapping. | Real |
| 10 | **Action Interlock** | For each pending action: takes worst claim verdict (weighted by role in action) + R-tier, looks up the frozen matrix, emits the actuator. **Sole final decider.** | Real — pure rule engine |
| 11 | **Surgical Editor** | For `Edit` actuator: removes the failing claim's sentence from the output text. Re-checks remaining claims. | Real (strip path only) |
| 12 | **Evidence Packet Builder** | For `Escalate` actuator: assembles `{claim, candidate_spans, verdicts, diff}`. | Real |
| 13 | **Action Gate** | For `Escalate` or `Block` actuators on tool calls: sets `allowed = false` on the mock tool. Tool does not execute. | Real |
| 14 | **Evidence Ledger** | The central typed data structure: `{principal, spans[], claims[], bindings[], pending_actions[], verdicts[], policy_version}`. Append-only. | Real |
| 15 | **Ledger Visualiser** | Renders the graph (`STEP → SPAN → CLAIM → ACTION`) in real-time as nodes and edges appear. Majority of screen real estate. | Real |
| 16 | **Output Panel** | Shows the streaming text with per-claim inline annotations: `Verified` / `Uncertain` / `Blocked`. | Real |
| 17 | **Matrix Display** | Shows the frozen R×S matrix. Highlights the exact cell that produced each actuator. | Real |
| 18 | **Evidence Packet Panel** | Appears when `Escalate` fires. Shows the packet contents. | Real |
| 19 | **FNR Schema Panel** | Collapsible panel showing the empty typed JSON schema. | Real |
| 20 | **Principal Selector** | Dropdown to switch calling principal between `agent-cs-emea` and `eng-lead-west` (or `hr-lead` for knowledge route). | Real |
| 21 | **Mock Refund Tool** | Accepts `issue_refund(amount, clause_reference)`. Prints "REFUND ISSUED" or "REFUND HELD — GATE: ESCALATE" based on the gate flag. | Mock (but gate semantics are real) |

---

## 5. Demo Flows (Judge-Facing)

### Primary Flow: Refund Dual-Action (builds backward from the action gate)

**Target duration: 4–5 minutes.**

```
STEP 0 — SETUP (5 seconds)
  Judge sees: Ledger Visualiser (empty), Output Panel (empty), Matrix Display (visible, no highlight),
             Principal Selector showing "agent-cs-emea", Route indicator "Refund Agent"
  Operator: selects Refund Agent route if not already selected.

STEP 1 — CRISIS FIRST (action gate, ~15 seconds)
  Operator triggers the trace.
  The stream simulator begins emitting tokens.
  — As the response streams, claims appear in the ledger as UNSUPPORTED (grey nodes).
  — Bindings light up: C1 green, C2 green, C5 green, C6 green.
  — C3 binds (green edge to finance-memo span) → but entitlement check fires → span turns RED,
    claim label flips to "Blocked", entitlement violation annotation appears.
  — C4 has no binding edge. Stays grey/UNSUPPORTED.
  
  WHEN THE TOOL CALL APPEARS (this is the first thing the judge sees as a "decision"):
  — A node appears: ACTION — issue_refund(184000, "7.2")
  — The R-tier resolver labels it R3.
  — The Interlock evaluates: worst claim for this action = C4 (unsupported + categorical).
  — Matrix cell R3 × Unsupported+categorical HIGHLIGHTS on screen.
  — Actuator: ESCALATE.
  — The mock refund tool shows: "REFUND HELD — GATE: ESCALATE"
  — The evidence packet panel opens showing: C4 text, the spans that were checked (with "no match"
    for 7.2), the verdict, and the diff (what the model claimed vs what the evidence supports).

  JUDGE HEARS: "The refund is held. Clause 7.2 does not exist in the evidence the model was given.
  The claim is not low-confidence — it is unproven. The action cannot proceed."

STEP 2 — SAME RESPONSE, DIFFERENT ACTUATOR (~30 seconds)
  — The Interlock evaluates the second pending action: "Show text to customer" → R1.
  — Worst claim for this action = C3 (entitlement violation in the text).
  — Matrix cell R1 × Contradicted/entitlement HIGHLIGHTS.
  — Actuator: EDIT.
  — The surgical editor strips C3's sentence from the output text.
  — The output panel shows the cleaned text with C1, C2, C5, C6 labelled "Verified"
    and C3 removed.
  — C4 was not in the R1 text path (it was only in the action justification), so R1 text
    shows "Uncertain" for any C4 residue or is clean.

  JUDGE HEARS: "The same response, the same graph, two different actuators. Edit on the text
  because an unentitled span leaked into what the customer sees. Escalate on the payment
  because a fabricated clause would have authorized ₹1,84,000. Proof scales with consequence."

STEP 3 — GRAPH READ-BACK (~30 seconds)
  — Operator (or automatic) walks the graph backward: "Here is the step that produced the
    finance-memo span. Here is the claim that bound to it. Here is where the ACL excluded
    the agent. Here is the matrix cell."
  — The judge can trace: ACTION → CLAIM → SPAN → SOURCE → ACL → PRINCIPAL for both actuators.
  — The ledger is the majority of the screen. The chat output is secondary.

STEP 4 — EMPTY FNR SCHEMA (~10 seconds)
  — Operator expands the FNR Schema Panel.
  — Shows the typed JSON with all value fields as null, measurement_status as "insufficient_sample".
  — Brief: "This is what we publish per route. The fields are typed. The values are empty
    because we have not earned them on this corpus. When we do, they appear with a confidence
    interval. We publish what we miss, not just what we catch."
```

### Secondary Flow: Principal-Flip Entitlement (Use Case B)

**Target duration: 1.5–2 minutes.**

```
STEP 5 — SWITCH ROUTE AND PRINCIPAL (~5 seconds)
  — Operator switches route to "Internal Knowledge Assistant".
  — Principal selector shows "eng-lead-west".
  — Ledger clears.

STEP 6 — FIRST RUN: ENTITLEMENT VIOLATION (~20 seconds)
  — Trigger trace. Two claims appear: D1 (engineering handbook) and D2 (HR comp guide).
  — D1 binds to eng-handbook-v2, ACL includes "eng-lead-west" → Verified.
  — D2 binds to hr-comp-guide-2025, ACL excludes "eng-lead-west" → entitlement violation.
  — R1 × Contradicted/entitlement → EDIT. D2 stripped from output.
  — Matrix cell highlighted.

  JUDGE HEARS: "The claim is semantically correct. The HR guide does say that. But the agent
  was not entitled to read that document. This is not 'the model said something sensitive' —
  it is authorization as set-membership. Zero LLM in this decision."

STEP 7 — PRINCIPAL FLIP (~15 seconds)
  — Operator changes principal selector to "hr-lead".
  — Re-run the same trace (same claims, same spans, same response text).
  — D1 still Verified (open ACL).
  — D2 now binds AND passes entitlement → Verified.
  — R1 → Pass.
  — No edit. Full text shown with both claims labelled "Verified".

  JUDGE HEARS: "Same response. Same evidence. Different principal. Different outcome.
  The ACL check is live set-membership — not a text classifier, not a confidence score."
```

### Optional Third Beat: R-Tier Change (only if under time and strengthens the matrix)

**Target duration: 30 seconds.**

```
STEP 8 — R-TIER CHANGE ON SAME VERDICT (~30 seconds, only if time permits)
  — Switch back to Refund Agent, principal "agent-cs-emea".
  — Re-run but with a configuration toggle that changes the "show text to customer" action
    from R1 to R0 (internal draft mode).
  — C3 entitlement violation now hits R0 × Contradicted/entitlement → Pass + annotate.
  — The text is NOT edited — it passes with an annotation.
  — Matrix cell changes. Actuator changes. Verdict is identical.

  JUDGE HEARS: "Same entitlement violation. Same unsupported categorical claim. But R changed
  from R1 to R0, so the actuator changed from Edit to Pass+annotate. The verdict is hostile;
  the action is proportionate. That is the matrix."
```

**If this beat risks exceeding 8 minutes or cluttering the differentiation moment, cut it.** The first two flows are sufficient. This beat is a bonus for a judge who wants to see the matrix at a third angle — it is not required for any success criterion.

---

## 6. Evidence Ledger & UI Requirements

### Governing test

> "If the judge can remove the graph from the screen and the demo still looks the same, the scope has already failed."

### Layout (mandatory)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Route: [Refund Agent ▼]    Principal: [agent-cs-emea ▼]   [RUN]  │
├──────────────────────────────────┬──────────────────────────────────┤
│                                  │                                  │
│     EVIDENCE LEDGER              │       OUTPUT PANEL               │
│     (graph visualisation)        │       (streaming text with       │
│                                  │        per-claim annotations)    │
│     60–65% of screen width       │                                  │
│                                  │       25–30% of screen width     │
│     Nodes:                       │                                  │
│     - STEP (blue)                │       "Order ORD-... was placed  │
│     - SPAN (green/red/grey)      │        on June 12, 2025"  [✓]   │
│     - CLAIM (green/red/grey)     │       "The order total is        │
│     - ACTION (blue/orange/red)   │        ₹1,84,000"         [✓]   │
│                                  │       "Refunds above ₹1,00,000  │
│     Edges:                       │        require supervisor..." [✗] │
│     - produces (STEP→SPAN)       │       "Clause 7.2 of the        │
│     - binds (SPAN→CLAIM)         │        vendor agreement..." [?]  │
│     - authorizes (CLAIM→ACTION)  │       "The refund will be        │
│     - entitlement-fail (red)     │        processed within..." [✓]  │
│                                  │                                  │
│     Legend: ✓ Verified           │                                  │
│             ? Uncertain          │                                  │
│             ✗ Blocked            │                                  │
│                                  │                                  │
├──────────────────────────────────┴──────────────────────────────────┤
│  MATRIX (frozen R×S)          │  EVIDENCE PACKET (on Escalate)    │
│  Highlighted cell shown        │  Claim: "Clause 7.2..."          │
│                                │  Spans checked: [list with ✓/✗] │
│                                │  Verdict: UNSUPPORTED            │
│                                │  Diff: ...                       │
├────────────────────────────────┴──────────────────────────────────┤
│  FNR SCHEMA [expand]                                                │
│  { "route_id": "refund-agent-emea", "FNR_estimate": null, ... }    │
└─────────────────────────────────────────────────────────────────────┘
```

### What must be visible for the demo to pass

1. **The graph as primary visual.** If the judge covers the right panel (output text), the left panel (ledger) must still convey what happened: which claims bound, which didn't, which had entitlement failures, which action was held, which was edited.

2. **Edges drawn in real-time.** When a claim binds to a span, the edge appears with visible latency (the NLI binding compute time). This is the proof it is not a pre-baked animation.

3. **Colour encodes verdict, not confidence.** Green = bound + entitled. Red = entitlement violation or contradicted. Grey = unsupported or unknown. No gradient, no percentage, no score.

4. **The matrix cell highlights at the moment of decision.** The judge sees: verdict severity on one axis, blast radius on the other, and the cell lights up before the actuator label appears.

5. **The evidence packet is a structured object, not a log dump.** It has named fields. The judge can read it without reconstructing reasoning from raw traces.

6. **The FNR schema is visibly empty.** Null values are displayed as `null`, not hidden. The `measurement_status` field is visible.

7. **Per-claim labels in the output panel are the same three states:** `Verified` / `Uncertain` / `Blocked`. No other labels. No scores.

### What must NOT be visible

- No confidence percentage on any claim
- No risk score (0–100 or otherwise)
- No "AI safety" or "responsible AI" branding
- No LLM-as-judge output
- No "hallucination detected" label (the label is "Uncertain" or "Blocked" — the mechanism is the graph, not a classifier name)
- No fabricated accuracy numbers

---

## 7. Success Criteria → Implementation Checks

Mapping every R2S1 §5 criterion to a concrete implementation or runtime check.

| # | R2S1 Criterion | Implementation Check | How Verified |
|---|---|---|---|
| 1 | Provenance outside the model | Every span in the Span Store is loaded **before** the stream begins. The Stream Simulator has no access to the Span Store. The ledger shows spans with `source_id · ACL · hash · offsets` **before** any claim verdict. | Judge inspects ledger: span nodes exist before claim nodes. Span metadata is visible. |
| 2 | One-graph invariant | The Evidence Ledger is a single data structure. No separate "hallucination ledger," "privacy ledger," or "action ledger" exists in the codebase. | Code review: one `EvidenceLedger` class. UI: one graph panel. |
| 3 | UNSUPPORTED default is real | Every claim is inserted into the ledger with `verdict = UNSUPPORTED`. No claim is ever inserted as `SUPPORTED`. The Claim Insertor has no code path that sets initial verdict to anything other than `UNSUPPORTED`. | Code review: `ClaimInsertor.insert()` sets `verdict: "UNSUPPORTED"` as the only initial value. Runtime: all claims appear grey before any binding runs. |
| 4 | Absence ≠ contradiction | C4 ("Clause 7.2...") has no matching span. The NLI Binder returns `UNSUPPORTED` (not `CONTRADICTED`). The claim stays grey, not red. | Runtime: C4 node is grey after binding completes. Verdict field shows `UNSUPPORTED`. |
| 5 | Claim-level proof works | C1 binds to order-record span → turns green → verdict `SUPPORTED`. C4 has no binding edge → stays grey → verdict `UNSUPPORTED`. | Runtime: visual edge from C1 to a span node. C1 turns green. C4 has no edge. |
| 6 | Two pending actions resolve independently | The ledger contains two ACTION nodes. One is R1 (text) → Edit. One is R3 (refund) → Escalate. Both are visible simultaneously. Both have their own matrix cell highlight. | Runtime: two ACTION nodes in the graph. Two matrix cells highlighted. Two actuator labels. The refund tool shows "HELD" while the text shows the edited version. |
| 7 | Hard action gate is real | The mock refund tool has an `allowed` parameter set by the Interlock. When the actuator is `Escalate`, `allowed = false`, and the tool prints "REFUND HELD." When the actuator is `Pass`, `allowed = true`. | Runtime: the tool output is visible. "REFUND HELD — GATE: ESCALATE" appears on screen. |
| 8 | Entitlement independence | Use Case B, principal `eng-lead-west`: D2 binds to hr-comp-guide-2025 but fails entitlement → Edit. Same trace, principal `hr-lead`: D2 binds and passes entitlement → Pass. The claim text is identical. The span is identical. Only the principal changed. | Runtime: run the same trace twice with different principal. D2 outcome flips. |
| 9 | Exact matrix fidelity | The Matrix Display contains the exact frozen table (R0–R3 rows, four severity columns, four actuator types). No invented cells, no extra rows, no renamed actuators. The highlighted cells for the demo map correctly: R1×entitlement→Edit, R3×unsupported-categorical→Escalate. | Visual inspection: transcribed matrix matches ARCHITECTURE.md §4 and R2S1 §3. Highlighted cells are correct. |
| 10 | Evidence packet | When Escalate fires, the Evidence Packet Panel shows: C4 claim text, list of spans checked (each with source_id, a verdict, and whether a match was found), final verdict "UNSUPPORTED", and a diff. | Runtime: panel appears with all four fields populated. |
| 11 | Surgical edit | When Edit fires on C3, the sentence containing C3 is removed from the output text. The remaining text is shown with the other claims' annotations intact. | Runtime: output panel shows the text without C3's sentence. C3 label does not appear. |
| 12 | FNR format honesty | The FNR Schema Panel shows the JSON schema with `null` values and `measurement_status: "insufficient_sample"`. No number is fabricated. | Runtime: panel is visible. Values are null. |
| 13 | No confidence driver | No floating-point number between 0 and 1 appears on any claim node, edge, or output annotation. The actuator is traceable to R × S, not to a scalar. | Runtime + code review: no confidence field in the ledger schema. No score in the UI. |
| 14 | Prompt injection cannot author provenance | The Stream Simulator's output is fixed. Even if a prompt-injection string is present in the simulated response, it cannot create a new span in the Span Store (spans are pre-loaded). The Claim Insertor cannot create spans. | Code review: `SpanStore` has no write method exposed to the stream path. `ClaimInsertor` only writes to `claims[]`, not `spans[]`. |
| 15 | Refund language fidelity | The refund action's actuator label is "ESCALATE," not "BLOCK." The mock tool output says "REFUND HELD — GATE: ESCALATE," not "REFUNDED BLOCKED." No demo narration says "the refund was blocked." | Runtime: visual check of tool output and actuator label. Narration discipline. |

**Prototype succeeds if and only if all 15 checks pass.**

---

## 8. Build Order Recommendation

The sequence that ensures the differentiation moment is never lost. If the team runs out of time, the last component is dropped — not the first.

| Order | Component | Why this order |
|---|---|---|
| **1** | **Evidence Ledger data structure** | Everything reads from this. If the ledger is wrong, nothing works. |
| **2** | **Span Store + Provenance Recorder** | Spans must exist before claims can bind. Load the JSON corpora. |
| **3** | **Entitlement Auditor** | Deterministic, zero dependencies on models. Proves the ACL check works immediately. |
| **4** | **Action Interlock + R-Tier Resolver** | The matrix lookup. Pure rule engine. Can be tested with hardcoded claims and verdicts. |
| **5** | **Hard Gate on mock tool** | The gate must work before the rest of the pipeline feeds it. |
| **6** | **Surgical Editor** | Simple string operation. Needed for the R1 Edit actuator. |
| **7** | **Evidence Packet Builder** | JSON assembly. Needed for the R3 Escalate actuator. |
| **8** | **Claim Insertor + Stream Simulator** | Now claims appear in the ledger at the right time. |
| **9** | **Numeric Recomputer** | Deterministic. Proves the claim-type routing works for at least one path. |
| **10** | **NLI Binder (local cross-encoder)** | **This is the last critical component.** It proves the engine runs live computation. If time runs out, pre-compute the NLI results and hide the latency — but this weakens the demo. |
| **11** | **Ledger Visualiser** | The graph rendering. Must be clear, not pretty. Nodes + edges + colours. |
| **12** | **Output Panel** | Streaming text with per-claim labels. Secondary to the ledger. |
| **13** | **Matrix Display** | Static table with highlight capability. Trivial to build. |
| **14** | **Evidence Packet Panel** | Renders the JSON from step 7. |
| **15** | **FNR Schema Panel** | Static JSON display. Trivial. |
| **16** | **Principal Selector** | Dropdown that changes the `principal` variable. Trivial. |
| **17** | **Route Selector** | Dropdown that switches corpora and route config. Trivial. |

**If the team has 48 hours:** build 1–9, pre-compute NLI for 10, build 11–17 as simple panels. The demo still passes all 15 criteria except the "live compute latency on binding edge" aspect of criterion 5 — which is a strength reduction, not a failure.

**If the team has 72+ hours:** build everything. The NLI binder running live is the proof that separates this from a recording.

**What to cut if desperate:** Cut the optional third beat (R-tier change). Cut the numeric recomputation case (F1) from the refund response — it is not in the critical path. Never cut: the ledger visualiser, the entitlement flip, the two-pending-actions resolution, the evidence packet, the empty FNR schema.

---

## 9. Fidelity Self-Check

| Frozen invariant | Status in this specification | Evidence |
|---|---|---|
| **Default = UNSUPPORTED** | Protected. Claim Insertor sets `verdict: "UNSUPPORTED"` as the only initial value. No code path inserts a claim as `SUPPORTED`. | §7, criterion 3: code review check. §4, component 4: "verdict `UNSUPPORTED`". |
| **Entitlement / ACL check** | Protected. Entitlement Auditor is a real component (§4, #8). Runs on every bound claim. Zero LLM. Principal flip is the secondary demo flow. | §5, Steps 6–7. §7, criterion 8. |
| **Exact R×S matrix** | Protected. Matrix Display shows the frozen table. Highlighted cells are verified against the frozen matrix. No invented cells or actuators. | §6: layout shows the matrix. §7, criterion 9: visual inspection against ARCHITECTURE.md §4. |
| **Hard gate on actions** | Protected. Action Gate (§4, #13) sets `allowed = false` on the mock tool when actuator is Escalate or Block. The tool does not execute. | §7, criterion 7. §5, Step 1: "REFUND HELD — GATE: ESCALATE". |
| **FNR as empty typed schema** | Protected. FNR Schema Panel shows JSON with null values and `"insufficient_sample"`. No fabricated numbers. | §4, #19. §7, criterion 12. |
| **Two-pending-actions resolution** | Protected. Primary demo flow shows R1→Edit and R3→Escalate on the same response, same graph, different matrix cells. Never collapsed into one response-level verdict. | §5, Steps 1–2. §7, criterion 6. §3: two ACTION nodes in the corpus definition. |
| **No LLM-as-judge on critical path** | Protected. The Action Interlock is a pure rule engine (§4, #10). NLI Binder is a classifier producing a verdict, not a judge producing an opinion. No LLM evaluates policy, weighs tradeoffs, or decides the actuator. | §4, #10: "Pure rule engine. No model. No score." §4, #6: NLI returns a verdict, not an opinion. |
| **Bias not a per-response verdict** | Protected. No bias measurement exists in the prototype. No bias-related claim type. No bias verdict in the matrix. The word "bias" does not appear in any UI element. | §2: "Out of scope" table includes "per-response bias verdicts." §4: no bias component in the component list. |
| **UNKNOWN never collapses into SUPPORTED** | Protected. The Derived Claim Router (#7) can set `UNKNOWN`. No code path transitions `UNKNOWN` to `SUPPORTED`. The NLI Binder (#6) returns only `SUPPORTED / CONTRADICTED / UNSUPPORTED` — never `UNKNOWN`, and never transitions from another verdict to `SUPPORTED` without a binding. | §4, #7: "or sets UNKNOWN". §7, criterion 3: only `UNSUPPORTED` is the initial state; `SUPPORTED` is earned only through binding or recomputation. |
| **Surgical edit only** | Protected. Surgical Editor (#11) implements strip only. No generative rewrite. No "re-invoke generator" path in the prototype (the architecture allows one constrained re-invocation; the prototype uses strip only for simplicity and determinism). | §4, #11: "strip path only." |
| **Evidence-packet escalation** | Protected. Evidence Packet Builder (#12) assembles the required fields. Evidence Packet Panel displays them. | §5, Step 1. §7, criterion 10. |
| **Never say "blocked" about the refund** | Protected. The actuator is `ESCALATE`. The tool output says "REFUND HELD — GATE: ESCALATE." Narration script in §5 says "held and escalated." | §5, Steps 1–2 narration. §7, criterion 15. |
| **No composite risk score** | Protected. No 0–100 number appears anywhere. No confidence percentage on any claim. | §6: "No confidence percentage on any claim." §7, criterion 13. |
| **One graph, three reads** | Protected. One Evidence Ledger class. One graph visualisation. Performance (binding), responsibility (entitlement), and cost (not centrepiece in prototype, but the graph structure supports it) are three reads of the same structure. | §4, #14: "one typed data structure." §7, criterion 2. |

**No tension exists between this specification and any frozen invariant.** The specification is a direct rendering of the frozen architecture into buildable components and demo flows. No competing mechanism is introduced. No frozen boundary is softened.

---

*End of Round 2 Stage 3 document. Stages 1 and 2 fully preserved. The prototype is specified to prove one thing: the graph works, the matrix works, the entitlement check works, and an unproven claim cannot authorize an irreversible action. Everything else is excluded.*