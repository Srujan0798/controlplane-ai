1. Round 2 Core Thesis

Round 2 does not broaden ControlPlane into a general AI-risk platform; it locks the frozen Round 1 admission-control primitive into multiple routes with different risk, latency and enforcement postures. The enterprise expansion is configuration and evidence, not new detection: route-level policy, fail stance, shadow replay, identity/ACL, audit ledger and per-route false-negative reporting all read from the same STEP → SPAN → CLAIM → ACTION graph. The sharpest differentiator remains unchanged — provenance captured outside the model, default UNSUPPORTED, deterministic entitlement/ACL check, and verification priced by blast radius.

2. Use-Case Selection for the Prototype

Use case A — Customer support refund/account-change assistant

- Concrete description: External customer chatbot handles refund requests, account changes and billing questions. It reads policy documents, CRM records and billing data, and can call a refund/update API.
- Risk signature: Confidently wrong amounts, clause IDs and account identifiers; PII from CRM; hallucinated policy; wrong irreversible action.
- Latency budget: R1 customer-visible text stays on Lane 1: ≤40 ms p50 / ≤200 ms p95 added. R3 action gating runs inside tool-call latency: 20–40 ms verification against a 200 ms–2 s round-trip.
- Dominant blast-radius tier(s): R1 user-visible read-only text; R3 irreversible/regulated payment or account mutation.
- Frozen mechanism most powerfully demonstrated: Two-pending-actions resolution. The same response carries R1 text and R3 refund; the matrix must price them separately, producing Edit for text and Escalate for the refund. Hard gate on actions, not tokens.

Use case B — Internal HR/knowledge assistant

- Concrete description: Employees ask about benefits, policy, org structure and internal process. The assistant retrieves from governed HR/benefit systems plus loosely governed shared drives and can draft summaries or emails.
- Risk signature: Over-permissioned RAG index leaking restricted HR/policy data to the wrong principal; stale or contradictory shared-drive content; PII/restricted-data leakage; hallucinated policy.
- Latency budget: R0/R1 read-only traffic is Lane 1 only: ≤40 ms p50 / ≤200 ms p95 added. R2 send-email action is gated before send.
- Dominant blast-radius tier(s): R0 internal draft; R1 employee-visible read-only; R2 reversible external send.
- Frozen mechanism most powerfully demonstrated: Deterministic entitlement/ACL check. A claim binding to a span whose source ACL excludes the caller is acted on before display, with an evidence packet naming principal, source and ACL. This is structurally impossible for an identity-blind output scorer.

Use case C — Procurement decision-support assistant

- Concrete description: Analyst asks for a risk memo on a vendor contract. The assistant retrieves contract clauses, procurement policy, vendor risk data and internal notes, then recommends approve/reject and can submit the recommendation into a workflow.
- Risk signature: Derived/multi-hop claims; no reliable real-time ground truth; stale vendor data; overlapping hallucination and bias risk; multi-turn analysis compounding one questionable clause into a downstream approval recommendation.
- Latency budget: R1 memo text is near-line, ≤200 ms p95 added. R2 workflow submission is action-gated. Bias replay runs async, never on the critical path.
- Dominant blast-radius tier(s): R0 analyst draft; R1 memo read-only; R2 workflow submission.
- Frozen mechanism most powerfully demonstrated: Derived-claim boundary and UNKNOWN handling. Claims that cannot be recomputed or directly entailed return UNKNOWN; they never collapse into SUPPORTED. This is the strongest defense against false assurance.

Why this combination is the strongest demonstration

Together the three routes cover R0, R1, R2 and R3; all four verdict columns; all three axes — performance, cost, responsibility. They force three non-toy demonstrations: one response with two pending actions priced separately, one deterministic ACL violation, and one derived/no-ground-truth case where the correct output is UNKNOWN, not a score.

3. Prototype Boundary (Hard)

What the working prototype WILL demonstrate

- A synthetic request enters through an OpenAI-compatible reverse proxy and context-assembly hook.
- The UI shows spans captured at assembly with source_id, ACL, content hash and offsets.
- Claims are extracted at sentence boundaries and displayed as typed check-worthy claims.
- Every claim starts UNSUPPORTED; binding is performed only against captured spans.
- Deterministic lane: numeric recomputation, span membership, ACL lookup, PII-shaped-entity scan, action interlock.
- Near-line lane: NLI cross-encoder binding for flagged claims; default verdict remains UNSUPPORTED.
- The frozen R × S matrix is applied per pending action, not per response.
- Refund trace: R1 text edited; R3 refund held and escalated; refund API call visibly not executed.
- HR trace: R1 entitlement violation produces Edit with an evidence packet naming principal, source and ACL.
- Procurement trace: derived claim either recomputed or returned UNKNOWN; hedged claim passes with annotation at R1; R2 submission gated.
- Dead compute: backward graph walk marks steps that grounded zero accepted claims.
- FNR surface: per-route false-negative-rate schema is visible; any populated value is labelled simulated.

What it will deliberately NOT demonstrate

- Real enterprise data or real PII: unnecessary for the core mechanism and creates privacy/legal risk.
- Production traffic volume or HA: tens of thousands of interactions/week is a scale argument, not a core-mechanism proof.
- Live statistical bias flagging with meaningful confidence intervals: requires real volume and time; prototype shows the route-level replay mechanism only, not a measured production bias rate.
- Full geography/industry regulatory DAG: one default policy version is enough to show the versioned rule engine; full regulatory mapping belongs in the business proposal.
- Human-in-the-loop resolution queue: the evidence packet is the deliverable; actual human triage is operational, not architectural.
- Real production FNR: impossible without deployment; the prototype shows the format and simulated labelled-set values, never fabricated production numbers.
- LLM-as-judge or confidence scoring: excluded by the freeze.

Minimum viable live demonstration that still feels advanced

Three traces share one engine: refund with two pending actions, HR ACL violation, procurement derived-claim/UNKNOWN. The judge sees a trace console, the graph, the matrix cell and the actuator for each pending action, plus an evidence packet. The demonstration is not hard-coded: changing a claim, source hash or ACL changes the verdict because the rules and binder actually run.

4. Explicit Assumptions

1. Data: Synthetic but realistic source corpora — governed policy/HR/finance records and loosely governed shared drives — with pre-assigned source_id, ACL and content hash. No real PII.
2. Model access: Generator, claim extractor and NLI binder are consumed via OpenAI-compatible APIs/local equivalents. No weights, logits, fine-tuning or model-internal access is assumed.
3. Integration surface: The application already assembles context and can call a thin SDK/proxy hook. Source ACLs and hashes are available from upstream stores; where unavailable in prototype, they are simulated.
4. Traffic shape: Combined load is tens of thousands of interactions/week; R0/R1 is 80–90% of volume; R2/R3 actions are a small minority. Prototype uses representative traces, not live traffic.
5. Latency: Measurements are on a controlled local/loopback environment. Only deterministic Lane 1 and NLI Lane 2 timings are shown; no production p95 claims.
6. Regulatory posture: One default jurisdiction/industry configuration is assumed for the demo, with one policy version. Evolving regulation is handled by the versioned policy DAG, described in proposal not live demo.
7. Ground truth/evaluation: There is no reliable real-time ground truth for the prototype. A small labelled set of 30–50 synthetic traces is used only to illustrate the FNR format.
8. Bias: Demonstrated as route-level counterfactual replay on a small synthetic dataset, never as a per-response verdict and never with a claimed statistical significance level.
9. Human escalation: The prototype writes an evidence packet to the append-only ledger and displays it. No real human queue or SLA resolution is simulated.
10. Multi-turn: Compounding risk is shown by carrying pending actions and graph state across turns in the ledger; full agent-memory integration is out of prototype scope.

5. Success Criteria for the Prototype

Each criterion is binary — a judge can answer yes/no.

1. Graph visible: In at least two traces, every displayed claim either binds to at least one captured span with source_id/ACL/hash visible, or is explicitly UNSUPPORTED/UNKNOWN.
2. Two-pending-actions correctness: Refund trace produces R1 text actuator = Edit and R3 refund actuator = Escalate; the refund API call is visibly not executed.
3. Evidence packet: The R3 escalation contains the exact unsupported claim, the fact that “clause 7.2” has no matching span, and the proposed actuator.
4. Entitlement check: HR trace shows a claim bound to an ACL-excluded span and produces the frozen matrix cell R1 × entitlement = Edit, not a global block.
5. Deterministic numeric check: A wrong amount/date in a trace is flagged by recomputation in the inline lane without an LLM decision.
6. Matrix fidelity: Every visible actuator matches the frozen matrix exactly; no invented actuators or severity columns appear.
7. Hard gate on action: The action API call is held while text is streamed/edited; the judge can see the tool call pending until gate release.
8. Dead compute: At least one trace shows a backward graph walk marking one or more steps as grounding zero accepted claims.
9. FNR format: The report shows per-route FNR schema — numerator, denominator, confidence interval, route label — not a single accuracy number; any populated value is explicitly labelled simulated.

6. Fidelity Self-Check

Confirmed. Nothing in this scope lock contradicts or softens:

- Default = UNSUPPORTED: every claim starts unsupported and must earn SUPPORTED through binding.
- Entitlement/ACL check: performed deterministically against spans carrying source ACLs; no identity-blind judge replaces it.
- Exact R × S matrix: transcribed, not redrawn; prototype renders the frozen cells.
- Hard gate on actions, not tokens: text streams behind hold-back; only action/tool calls are gated.
- Published own FNR as a format: shown as schema/simulated values, never fabricated production accuracy.
- Two-pending-actions resolution: refund trace keeps R1 Edit and R3 Escalate separate; no collapse into a single “response blocked” verdict.

Tension surfaced and resolved in favor of the freeze: the internal HR trace could have been staged as a PII-shaped secret and blocked. That would create ambiguity with the R1 × entitlement = Edit matrix cell used in the running example. Resolution: the HR demo uses an ACL-excluded policy span, not a PII-shaped secret, so the actuator is exactly R1 × entitlement = Edit. The no-span PII leakage rule remains part of the architecture and business proposal, but is not made the HR demo’s matrix case.

7. Biggest Scope Risk + Exact Mitigation

Biggest scope risk: The prototype reads as another RAG-groundedness or guardrail demo because the judge sees flags and scores, not an admission-control decision. The decisive failure is if the two-pending-actions refund case collapses into “response blocked” or if the held action is not visually obvious.

Exact mitigation: Build the demo backward from the action gate. The first visible event is the pending refund API call held at the gate, with the R3 × unsupported-categorical cell and Escalate evidence packet on screen. Only after that does the demo show the R1 text path edited. No risk score, no “blocked response,” no LLM-as-judge output is allowed on screen. Every visible outcome is an actuator from the frozen matrix. All non-core breadth — regulation mapping, full bias statistics, production scale, human queue — is confined to the business proposal.