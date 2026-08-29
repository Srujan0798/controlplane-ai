# ControlPlane.ai

**Admission-control layer for AI that acts.**  
Accenture Innovation Challenge 2026 · Round 2 · Team ControlPlane · PS #1 · tag `v0.2.0-round2`

Every AI response is a set of **claims requesting permission to act**. Provenance is captured **outside** the model (`STEP → SPAN → CLAIM → ACTION`). Unproven or unauthorized claims cannot authorize irreversible actions.

Lane 1 is deterministic — no LLM on the critical path.

---

## Submit (start here)

→ **[`docs/SUBMIT.md`](docs/SUBMIT.md)**

| Deliverable | Artifact |
|---|---|
| Proposal | [`submission/ControlPlane_Round2_Proposal.pdf`](submission/ControlPlane_Round2_Proposal.pdf) · canon [`round2/CONTROLPLANE_R2_FINAL.md`](round2/CONTROLPLANE_R2_FINAL.md) |
| Prototype | this repo — console below |
| Pitch | [`submission/ControlPlane_Round2_Pitch.pptx`](submission/ControlPlane_Round2_Pitch.pptx) · speak [`round2/R2S5.md`](round2/R2S5.md) |

---

## Run the prototype

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
bash scripts/preflight-lite.sh
make run
# open http://127.0.0.1:8787
# autorun: http://127.0.0.1:8787/?scenario=refund&mode=enforce&autorun=1
```

Docker: `docker compose up --build` → http://localhost:8080

**Expected (refund):** `show_text` → **Edit** · `issue_refund` → **Escalate** (held with evidence packet — never “blocked”).

```bash
python3 examples/refund_trace_demo.py
python3 examples/knowledge_flip_demo.py   # Edit → Pass when principal changes
```

---

## Architecture (one line)

```text
STEP → SPAN → CLAIM → ACTION
Recorder → Binder → Entitlement → Interlock (frozen MATRIX)
```

Full system of record: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

---

## Repo map (single flow)

```text
SEBI/
├── README.md · AGENTS.md · LICENSE · docs/SUBMIT.md
├── controlplane/     # gate + FastAPI + Operate console
├── policies/         # YAML packs
├── tests/ · examples/ · scripts/
├── submission/       # PDF · PPTX · latency_bench.json · SBOM
├── round2/           # CONTROLPLANE_R2_FINAL.md · R2S5.md
└── docs/             # ARCHITECTURE · JUDGE_RUNBOOK · HOSTILE_QA · ACCEPTANCE · …
```

| Need | Open |
|---|---|
| Submit / how | [`docs/SUBMIT.md`](docs/SUBMIT.md) |
| Stand script | [`docs/JUDGE_RUNBOOK.md`](docs/JUDGE_RUNBOOK.md) |
| Hostile Q&A | [`docs/HOSTILE_QA_DRILL.md`](docs/HOSTILE_QA_DRILL.md) · depth [`docs/QA.md`](docs/QA.md) |
| Architecture | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |
| Acceptance | [`docs/ACCEPTANCE.md`](docs/ACCEPTANCE.md) |
| Event checklist | [`docs/EVENT_DAY_CHECKLIST.md`](docs/EVENT_DAY_CHECKLIST.md) |
| Kill-shot | [`docs/KILL_SHOT.md`](docs/KILL_SHOT.md) |
| Official PS | [`docs/ps.md`](docs/ps.md) + PDFs in `docs/` |

---

## What we built

- Provenance ledger outside the model (hash-chained)
- Deterministic binding + entitlement (ACL set-membership)
- Frozen blast-radius matrix · dual-action refund (Edit + Escalate)
- Clause 7.2 absence → UNSUPPORTED → held money path
- FastAPI OpenAI-compatible gate · Operate console (Clearance → Print)
- Policy packs · shadow metrics · signed audits · Docker + CI

Team: Choda Srujan Sai · Dhrithika · IIT Gandhinagar
