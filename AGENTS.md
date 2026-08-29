# AGENTS.md — ControlPlane project law

Branch: **`main` only**. Tag: **`v0.2.0-round2`**.

## Stack
Python ≥ 3.11 · FastAPI · pytest · YAML policies · static Operate console  
`pip install -e ".[dev]"` · `bash scripts/preflight-lite.sh` · `make run` (:8787)

## Frozen invariants
1. Provenance outside the model — output never creates spans.  
2. Default verdict `UNSUPPORTED`.  
3. Clause **7.2 does not exist** → absence → `UNSUPPORTED`.  
4. MATRIX transcribed, never redrawn.  
5. Action Interlock is the sole decider.  
6. Refund: **held / escalated with evidence packet** — never “blocked”.  
7. Lane 1 deterministic — no LLM on critical path.  
8. Fail closed — never Pass without proof.

## Evidence
Cite `submission/latency_bench.json` for latency (never quote 40ms as p95).  
No invented FNR % or logos. After code changes: `graphify update .`

## Canon
`docs/ARCHITECTURE.md` · `round2/CONTROLPLANE_R2_FINAL.md` · `round2/R2S5.md` · `docs/JUDGE_RUNBOOK.md` · `docs/SUBMIT.md`
