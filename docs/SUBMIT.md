# Submit — ControlPlane.ai Round 2

**Public GitHub (only branch judges need):** https://github.com/Srujan0798/controlplane-ai (`main`)  
**Frozen rollback tag:** `v0.2.0-round2`

## Portal uploads (five fields)

| # | Portal field | Artifact |
|---|---|---|
| 1 | Public GitHub link | https://github.com/Srujan0798/controlplane-ai |
| 2 | Prototype video | [`../submission/ControlPlane_Round2_Prototype.mp4`](../submission/ControlPlane_Round2_Prototype.mp4) |
| 3 | README document (PDF) | [`../submission/ControlPlane_Round2_README.pdf`](../submission/ControlPlane_Round2_README.pdf) |
| 4 | Business proposal (PDF) | [`../submission/ControlPlane_Round2_Proposal.pdf`](../submission/ControlPlane_Round2_Proposal.pdf) |
| 5 | Pitch deck (PPTX) | [`../submission/ControlPlane_Round2_Pitch.pptx`](../submission/ControlPlane_Round2_Pitch.pptx) |

Official brief: [`ps.md`](ps.md).

## Run in 60 seconds

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
bash scripts/preflight-lite.sh
make run
```

Then: http://127.0.0.1:8787/?scenario=refund&mode=enforce&autorun=1  
Gate (paste/upload): http://127.0.0.1:8787/gate

**Expected:** `show_text` → **Edit** · `issue_refund` → **Escalate** (**held** with evidence packet — never “blocked”).

## Checks before upload

| Check | Pass means |
|---|---|
| Refund | Edit + Escalate (**held** with evidence packet — never “blocked”) |
| Amount bind | `numeric` (not fixture) |
| Flip | analyst Edit → hr_partner Pass |
| Eval / latency | Only quote `make eval` / `submission/latency_bench.json` |
| Number freeze | `make verify` green |

## Room path

1. [`../round2/R2S5.md`](../round2/R2S5.md) — speak  
2. [`JUDGE_RUNBOOK.md`](JUDGE_RUNBOOK.md) — click  
3. [`HOSTILE_QA_DRILL.md`](HOSTILE_QA_DRILL.md) — defend  

Never say the refund was “blocked.” Say **held and escalated with the evidence packet.**
