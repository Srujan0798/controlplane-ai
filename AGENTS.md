# AGENTS.md — ControlPlane law

**Branch:** `main` · **Tag:** `v0.2.0-round2`

## Run
`pip install -e ".[dev]"` · `bash scripts/preflight-lite.sh` · `make run` (:8787)

## Invariants (do not “improve”)
1. Provenance outside the model.  
2. Default `UNSUPPORTED`.  
3. Clause 7.2 does not exist → absence → `UNSUPPORTED`.  
4. MATRIX never redrawn.  
5. Interlock sole decider.  
6. Refund: held/escalated — never “blocked”.  
7. No LLM on Lane 1.  
8. Fail closed.

## Canon
`docs/SUBMIT.md` · `docs/ARCHITECTURE.md` · `round2/CONTROLPLANE_R2_FINAL.md` · `round2/R2S5.md` · `docs/JUDGE_RUNBOOK.md`

Latency only from `submission/latency_bench.json`. After code: `graphify update .`
