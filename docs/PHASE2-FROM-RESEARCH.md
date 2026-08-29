# Phase-2 ideas extracted from agent research shards

**Source:** `round2/_archive/stage-shards/` (deleted after extraction).  
**Canon remains:** `round2/CONTROLPLANE_R2_FINAL.md`, `round2/R2S5.md`, `docs/ARCHITECTURE.md`.  
**These are NOT Round-2 submit claims** — post-prize roadmap only. Nothing here invents FNR % or changes the frozen matrix.

## Ops / policy shipping
- Alert-fatigue: flagged+escalated / total with ~5% route ceiling → recalibration flag
- Canary ladder: ~5–10% → 24h or ~5k traces → 25% → 50% → 100%
- Shadow acceptance: Block/Escalate mix drop >30% or jump >50% vs prior → hard human review
- Auto-rollback: override >3× baseline → revert within ~5 minutes
- Policy PR flow: draft → shadow → canary → promote → audit; hash-chained policy diffs
- Geography packs: tighten-only R remaps (never soften entitlement / default UNSUPPORTED)
- Jurisdiction-configurable retention for evidence packets
- Policy YAML inheritance packs (`inherits: [global_base, …]`)

## Measurement
- FNR earn-out: ≥500 samples and CI width ≤0.05 else `insufficient_sample`
- Sampling recipe: 100% Block/Escalate, ~10% Edit/Pass+annotate, ~2% Pass; Wilson/bootstrap CI
- Dead-compute buyer schema: `dead_step_ratio` + estimated wasted tokens/cost
- Separate Pass+annotate volume metric on R0/R1
- Override taxonomy: confirmed / FP / source error / ACL gap + reason codes

## Product / demo craft (already mostly shipped; keep as polish checklist)
- Cover-right-panel test: ledger alone must prove the story
- Verdict colour law: green bound+entitled; red entitlement/contradicted; grey unsupported — no score gradient
- Provenance timestamp must precede model invocation
- Skeptical tour: empty FNR schema → live held R3 packet → override series that would roll a canary

## Explicit non-goals (never auto-loosen)
- User acceptance of an answer ≠ safety signal  
- “No complaint after action” ≠ train/loosen policy
