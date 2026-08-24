**Got it.** Treating the long instruction as the Stage 1 prompt. Here is the pure output.

---

**1. Round 2 Core Thesis**

ControlPlane is an admission-control layer that treats every AI response as a set of claims requesting permission to act. Provenance is captured outside the model at context assembly (source · ACL · hash), every claim starts UNSUPPORTED, and only a binding to an entitled span can authorise an action. Round 2 expands the identical STEP → SPAN → CLAIM → ACTION graph and frozen R × S matrix across concurrent use cases that differ in risk tolerance and latency budget, so verification is priced by blast radius while the single differentiator (outside-model provenance + inverted burden of proof + entitlement + matrix) remains undiluted.

**2. Use-Case Selection for the Prototype**

Three use cases chosen because the same graph and same verdicts produce different actuators solely by changing R:

- **Customer-support refund agent**  
  Risk signature: policy hallucination + irreversible payment + possible ACL leakage.  
  Latency budget: text under hold-back ≤300 ms; action gate amortised inside tool latency.  
  Dominant tiers: R3 (refund) + R1 (customer-visible text).  
  Strongest mechanism: two-pending-actions resolution on the ₹1,84,000 / non-existent clause 7.2 trace.

- **Internal knowledge assistant**  
  Risk signature: leakage from over-permissioned internal documents.  
  Latency budget: strict interactive (Lane-1 deterministic only for majority traffic).  
  Dominant tiers: R0 / R1.  
  Strongest mechanism: pure entitlement failure (span binds but ACL excludes caller → deterministic Block).

- **Decision-support tool**  
  Risk signature: multi-hop / synthesised claims + sparse evidence.  
  Latency budget: higher tolerance for Lane-2 binding on flagged claims.  
  Dominant tiers: R2 (reversible write) with occasional R3.  
  Strongest mechanism: UNKNOWN on derived claims never collapses to SUPPORTED.

This triad forces the matrix to fire Pass+annotate, Edit, Escalate and Block from one shared Evidence Ledger.

**3. Prototype Boundary (Hard)**

**WILL demonstrate (live-observable):**  
- Provenance Recorder writing spans with source_id, ACL, hash, offsets before any claim is extracted.  
- Typed claim extraction + binding against the provenance set only (deterministic for numbers/IDs, NLI for text).  
- Default UNSUPPORTED; claim must earn SUPPORTED.  
- Entitlement Auditor producing Block on ACL exclusion with zero LLM.  
- Exact frozen matrix, including dual pending actions (R1 Edit + R3 Escalate) on the refund response.  
- Hard gate on the action path while text uses hold-back.  
- Evidence packet on Escalate.  
- Explicit UNKNOWN on a multi-hop claim.  
- Shadow-mode counterfactual for at least one route.

**Will NOT demonstrate:**  
- Live bias replay or measured FNR numbers (Lane-3 / evaluation plan).  
- Full multi-tenant traffic or real model weights.  
- Continuous learning loops or full regulatory rule packs.  
- Generative full-answer rewrite (surgical edit only).  
- Dead-compute accounting across thousands of traces.

**Minimum viable live demo:** One interactive session that runs the classic refund dual-action case, an ACL Block, and a multi-hop UNKNOWN, all sharing the same Evidence Ledger visualisation. No slides.

**4. Explicit Assumptions**

- Simulated policy + internal-knowledge + sparse decision-support corpora; every span carries source_id, ACL, hash, offsets.  
- Strictly API-only models; claim extractor 1–3B class, binding ~300 M NLI; everything else deterministic.  
- Prototype traffic = curated adversarial traces + small synthetic concurrent load; enterprise reference remains tens of thousands of interactions/week.  
- Regulatory posture = Indian DPDP + financial-sector rules; prototype records principal + evidence fragment but does not implement full retention.  
- Integration = thin context-assembly hook + OpenAI-compatible reverse proxy.  
- Evaluation data = hand-crafted traces only (clause-7.2 absence, entitlement violation, multi-hop UNKNOWN, pure parametric route). No statistical FNR claim.  
- Shadow mode is default; enforcement is not claimed on cold routes.

**5. Success Criteria for the Prototype**

Judge must answer yes/no to each:

1. Spans (source · ACL · hash) appear in the ledger before claims.  
2. At least one claim remains UNSUPPORTED and is never auto-promoted.  
3. Refund response produces two distinct actuators (Edit on R1, Escalate + packet on R3).  
4. ACL-excluding span produces Block with principal + source_id logged and zero LLM.  
5. Multi-hop claim returns UNKNOWN and never becomes SUPPORTED.  
6. Text is held back; action is gated and does not fire until matrix decision.  
7. Matrix cells match the frozen transcription exactly.  
8. Shadow counterfactual is emitted for ≥1 route.

**6. Fidelity Self-Check**

- Default = UNSUPPORTED → preserved.  
- Entitlement / ACL check → preserved and demonstrated.  
- Exact R × S matrix → transcribed, never redrawn; dual-action case is centrepiece.  
- Hard gate on actions, not tokens → preserved.  
- Own FNR published as empty schema with typed placeholders → preserved.  
- Two-pending-actions resolution → required in live demo.  

No softening. No competing mechanisms introduced.

**7. Biggest Scope Risk + Exact Mitigation**

**Risk:** Prototype drifts into three separate feature demos; judges see “another configurable guardrail” instead of one graph producing different actuators by blast radius.

**Mitigation:** Single shared Evidence Ledger for all three routes. Live script locked to refund dual-action → ACL Block → multi-hop UNKNOWN in that order. Any feature that cannot be shown as a read of the same STEP → SPAN → CLAIM → ACTION structure is cut from the prototype and moved to the business proposal.