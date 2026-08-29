# Submit — ControlPlane.ai Round 2

**Public GitHub (only branch judges need):** https://github.com/Srujan0798/controlplane-ai (`main`)  
**Frozen rollback tag:** `v0.2.0-round2`

## Portal — five fields

| # | Organizer field | Artifact |
|---|---|---|
| 1 | Public GitHub link | https://github.com/Srujan0798/controlplane-ai |
| 2 | Prototype video (`.mp4`) | `submission/ControlPlane_Round2_Prototype.mp4` |
| 3 | README document (`.pdf`) | `submission/ControlPlane_Round2_README.pdf` |
| 4 | Detailed business proposal (`.pdf`) | `submission/ControlPlane_Round2_Proposal.pdf` |
| 5 | Pitch presentation (`.pptx`) | `submission/ControlPlane_Round2_Pitch.pptx` |

Official brief: [`ps.md`](ps.md).

## Verify before upload

```bash
source .venv/bin/activate
bash scripts/preflight-lite.sh
make run
# http://127.0.0.1:8787/?scenario=refund&mode=enforce&autorun=1
# Gate (paste/upload): http://127.0.0.1:8787/gate
```

| Check | Pass means |
|---|---|
| Refund | Edit + Escalate (**held** with evidence packet — never “blocked”) |
| Amount bind | `numeric` (not fixture) |
| Flip | analyst Edit → hr_partner Pass |
| Eval / latency | Only quote `make eval` / `submission/latency_bench.json` |

## Present

1. [`../round2/R2S5.md`](../round2/R2S5.md) — speak  
2. [`JUDGE_RUNBOOK.md`](JUDGE_RUNBOOK.md) — click  
3. [`HOSTILE_QA_DRILL.md`](HOSTILE_QA_DRILL.md) — defend  

Never say the refund was “blocked.” Say **held and escalated with the evidence packet.**
