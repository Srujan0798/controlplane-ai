# How to submit — ControlPlane.ai Round 2

Accenture Innovation Challenge 2026 · Team ControlPlane · PS #1  
**Known-good tag:** `v0.2.0-round2` (@ `551de81`)

## What organizers ask (`docs/ps.md`)

| # | Deliverable | What we submit |
|---|---|---|
| 1 | Detailed Business Proposal | `submission/ControlPlane_Round2_Proposal.pdf` (canon MD: `round2/CONTROLPLANE_R2_FINAL.md`) |
| 2 | Working Prototype | Live demo of this repo (Docker or local) — core gate + console |
| 3 | Pitch Presentation | `submission/ControlPlane_Round2_Pitch.pptx` (speak-from: `round2/R2S5.md`) |

## Before you upload / present

```bash
source .venv/bin/activate
bash scripts/preflight-lite.sh          # must PASS
make run                                # http://127.0.0.1:8787
# or: docker compose up --build       # http://localhost:8080
```

Prove once:
- Refund → **Edit** + **Escalate** (held, never “blocked”)
- Flip analyst→Edit, hr_partner→Pass
- Latency only from `submission/latency_bench.json` (not marketing)

## Room kit (one flow)

1. Open console Clearance  
2. Speak beats from `round2/R2S5.md`  
3. Click path in `docs/JUDGE_RUNBOOK.md`  
4. Defend with `docs/HOSTILE_QA_DRILL.md`  
5. Optional depth: `docs/ARCHITECTURE.md`, `docs/KILL_SHOT.md`

## Do not submit / do not open on stage

- `.venv/`, `graphify-out/`, `__pycache__/`
- Any Adaptoid / agent folders (removed from this tree)
- Claiming Lane-2 NLI, invented FNR %, or `p95=40ms`
