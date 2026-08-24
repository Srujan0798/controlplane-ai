**1. Expanded Core Thesis**

ControlPlane remains an admission-control layer whose single primitive is the STEP → SPAN → CLAIM → ACTION graph assembled outside the model. Every claim starts UNSUPPORTED, entitlement is deterministic set-membership against the caller and source ACL, and the frozen R × S matrix prices verification by blast radius. Round 2 deploys that identical graph across concurrent enterprise routes by making risk tolerance, latency budget and regulatory posture pure configuration of the same ledger and the same rule engine, never a new detector. The differentiator therefore survives intact: one structure yields three reads (performance, cost, responsibility) while actions remain gated and text remains optimistic.

**2. Multi-Route Architecture**

**Shared (immutable core)**  
- Provenance Recorder at context assembly (source_id · ACL · hash · offsets · principal).  
- Typed Evidence Ledger (append-only, hash-chained, one per request).  
- Claim Extractor (typed check-worthy propositions, categorical/hedged).  
- Prosecutor (binding against the captured provenance set only; numeric/structural recomputation; NLI for textual entailment; derived claims never auto-SUPPORTED).  
- Entitlement Auditor (Lane-1, zero LLM).  
- Action Interlock (computes R, applies the exact frozen matrix, emits actuator).  
- Three lanes with hard deadlines; fail stance owned by tier (R0/R1 open+annotate, R2/R3 closed/escalate).  
- Hard gate only on the action/commit boundary; text uses hold-back.

**Configured per route**  
- Blast-radius mapping: which tool schemas and audience/data-class combinations resolve to R0–R3.  
- Latency budget: which lanes are permitted (R0/R1 default to Lane-1 only; high-R routes may enable Lane-2).  
- Thresholds inside the matrix cells that are already fixed (e.g., when UNKNOWN on R2 escalates vs edits).  
- Policy pack identifiers (geography, sector, risk appetite) that select the active versioned rule set.  
- Shadow-mode window and enforcement-earning criteria.  

The matrix itself is never redrawn and never becomes route-specific product logic. A claim that is UNSUPPORTED + categorical still produces Escalate on R3 and Edit on R1; only the assignment of a given pending action to an R tier is route-configurable. Overlapping failure modes (a fabricated detail that is simultaneously a privacy leak) are handled by the same ledger: the Entitlement Auditor and the Prosecutor both write verdicts; the Interlock takes the worst relevant cell for each pending action. Multi-turn compounding risk is contained because every subsequent turn re-assembles provenance and re-evaluates claims against the current ledger; an earlier unproven claim cannot silently authorise a later tool call.

**3. Governance & Policy Layer**

Policy is a versioned DAG of 4-tuples `(signal, threshold, action, latency_budget)`. The engine that evaluates the DAG is a pure rule engine: zero LLM reasoning at decision time.  

- **Variation surfaces**  
  - Use-case / route: selects the active pack and the R-mapping table.  
  - Risk appetite: can tighten or loosen only the thresholds that the matrix already exposes (never invents new actuators).  
  - Geography / regulatory posture: selects a pack that may add or remove allowed tool schemas or force higher R for regulated data classes.  
  - Blast-radius tier: already owns fail stance and which lanes may run.  

- **Versioning & audit**  
  Every decision writes the exact policy_version, the evidence fragment that fired, and the principal into the append-only ledger.  

- **Change control**  
  No threshold or pack change reaches live traffic without:  
  1. Shadow replay over the last N traces of the target route(s), producing FP/FN delta and override-rate projection.  
  2. Canary by route.  
  3. Auto-rollback if human-override rate exceeds 3× baseline on the canary.  

This satisfies evolving regulation without hard-coding rules that age and without moving the critical path into an LLM.

**4. Feedback & Learning Loops**

- Human overrides and escalations are written back to the ledger with the original evidence packet.  
- The Adjudicator (Lane-3) samples 100 % of holds/escalations plus a random slice of passes to an expensive ground-truth path; the result updates the per-route FNR format and confidence intervals.  
- Threshold calibration (when a given signal fires Edit vs Escalate inside an already-fixed matrix cell) is updated from the stratified sample; the update itself is subject to the same shadow-replay + canary gate.  
- What is never learned: the default UNSUPPORTED rule, the entitlement set-membership test, the matrix cells, or any model that would sit on the critical path. The control plane does not become a trained classifier; it remains a rule engine whose parameters are evidence-gated.

**5. Metrics, Monitoring & Trustworthiness Reporting**

All metrics are ledger-derived; none are model opinions.

- **Per-route false-negative rate** — stratified shadow audit; reported as a typed schema (route, sample definition, numerator, denominator, CI / measurement status). The schema ships; production numbers are filled only when ground truth exists. Emptiness remains the credibility statement.  
- **False-positive / override rates** — human overrides per route per sliding window; used both for canary rollback and for alert-fatigue control.  
- **Dead compute** — exact backward walk of the graph: any STEP that produced zero spans that grounded an accepted CLAIM.  
- **Latency by lane** — p50/p95 per lane per route; R0/R1 targets remain ≤40 ms p50 / ≤200 ms p95 added.  
- **Entitlement violations** — count and rate of ACL exclusions, broken out by source and principal class.  

A sceptical stakeholder is shown the empty FNR schema first, then the live ledger of a held R3 action with its evidence packet, then the measured override rate that would have triggered auto-rollback. The plane is audited by the standard it enforces.

**6. Complete Enterprise Solution vs Prototype**

**Full solution**  
Multi-route deployment of the shared graph + per-route configuration packs, full governance DAG with shadow-canary-rollback, Adjudicator-driven FNR measurement, dead-compute accounting, multi-turn ledger continuity, versioned regulatory packs, and the business-proposal treatment of bias as route-level asynchronous counterfactual flip-rate + CI.

**Stage 1 prototype (deliberately limited)**  
Exactly the two routes frozen in R2S1: refund agent (R1+R3 dual-action centrepiece) and internal knowledge assistant (entitlement flip). Live Evidence Ledger, surgical Edit, evidence-packet Escalate, hard action gate, empty FNR schema. No third live decision-support route, no per-response bias verdict, no production-scale load, no real money movement.

**Proposal-only**  
Bias measurement (async counterfactual), full geography/sector packs, continuous evaluation pipelines at tens-of-thousands/week scale, human triage SLA surfaces, and any quantitative FNR numbers beyond the schema format.

**7. Residual Risks & Explicit Mitigations**

1. **False assurance on derived / multi-hop claims**  
   Mitigation (already frozen): derived claims are never marked SUPPORTED by entailment alone; they are recomputed or returned UNKNOWN; UNKNOWN never collapses to SUPPORTED. Prototype must surface at least one such UNKNOWN.

2. **Alert fatigue from over-flagging on high-volume R0/R1 routes**  
   Mitigation: matrix already prices verification by blast radius; R0/R1 receive Lane-1 only and Pass+annotate for most unsupported-hedged/UNKNOWN cells; enforcement is earned per route through shadow evidence so teams are never forced to trust an unproven block rate.

3. **Policy drift or silent over-permissioned index**  
   Mitigation: every entitlement decision is logged against named principal and named source; the query-time ACL check is itself the detector; policy changes require shadow replay and auto-rollback on elevated override rate. ControlPlane does not repair IAM; it makes the violation visible and prevents the model from bypassing it.

**8. Fidelity Self-Check**

- Default = UNSUPPORTED — untouched; claims still earn SUPPORTED.  
- Entitlement / ACL check — untouched; remains deterministic Lane-1, identity-carrying.  
- Exact R × S matrix — transcribed, never redrawn; dual-action resolution preserved as centrepiece.  
- Hard gate on actions, not tokens — untouched.  
- No LLM-as-judge on the critical path — untouched; pure rule engine at decision time.  
- Two-pending-actions resolution — untouched; R1 Edit + R3 Escalate remain simultaneous and distinct.  
- Bias remains distributional / async / route-level — never a per-response matrix verdict.  

No competing mechanism, composite score, or confidence-driven disposition has been introduced. The expansion is configuration and evidence around the frozen core.