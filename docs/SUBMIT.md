# Submit — ControlPlane.ai Round 2

**Tag:** `v0.2.0-round2` · **Branch:** `main`

## Upload / hand in

| # | Organizer ask | Our artifact |
|---|---|---|
| 1 | Detailed business proposal | `submission/ControlPlane_Round2_Proposal.pdf` (built from `round2/CONTROLPLANE_R2_FINAL.md`) |
| 2 | Working prototype | Live demo of this repository |
| 3 | Pitch presentation | `submission/ControlPlane_Round2_Pitch.pptx` |

Official brief: [`ps.md`](ps.md) (+ PDFs in this folder).

## Verify before upload

```bash
source .venv/bin/activate
bash scripts/preflight-lite.sh
make run
# http://127.0.0.1:8787/?scenario=refund&mode=enforce&autorun=1
```

| Check | Pass means |
|---|---|
| Refund | Edit + Escalate (held) |
| Flip | analyst Edit → hr_partner Pass |
| Latency | Only quote `submission/latency_bench.json` |

## Present

1. [`../round2/R2S5.md`](../round2/R2S5.md) — speak  
2. [`JUDGE_RUNBOOK.md`](JUDGE_RUNBOOK.md) — click  
3. [`HOSTILE_QA_DRILL.md`](HOSTILE_QA_DRILL.md) — defend  

Never say the refund was “blocked.” Say **held and escalated with the evidence packet.**
