# Task: W7-04 — Fail-stance by tier (PARTIAL #12)

## Goal
Enforce fail-stance by blast tier from policy packs (not YAML decoration only), preserving fail-closed.

## Writes (only)
- `controlplane/interlock.py` and/or `controlplane/policy.py` / `pipeline.py`
- `policies/*.yaml` only if schema needs a field already implied
- `tests/test_fail_closed.py` (extend) + targeted interlock tests

## Forbid
- UI copy
- LLM on path
- Redrawing MATRIX structure (you may read cells; do not invent new actuators)

## Steps
1. Read how policy packs express fail stance today.
2. Enforce: higher R tiers cannot soft-Pass when policy says fail-closed/escalate.
3. Add regression tests.
4. `pytest -q`

## Acceptance
- [ ] PARTIAL #12 meaningfully closed or report residual with test proof
- [ ] No new Pass-without-proof path
- [ ] pytest green

## Commit message
`feat: enforce fail-stance by blast tier`

## Report
`work/reports/wave-7/W7-04.report.md`
