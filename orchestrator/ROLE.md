# Orchestrator ROLE (Tier 1)

- Write/update `work/<wave>/*.md` and review `work/reports/`.
- Update `plan/EXECUTION.md` + rewrite `HANDOFF.md` after waves.
- Run verify: `pytest -q`, `make judge`, console smoke.
- **Do not** implement product features while workers are on the same files (FM-26).
- Exception: OS scaffold / merge conflict resolution / verify-only fixes.
