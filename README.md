# ControlPlane.ai

**Admission-control layer for AI that acts.**  
Accenture Innovation Challenge 2026 · Round 2 · Team ControlPlane · PS #1  

**Public repo (single branch `main`):** https://github.com/Srujan0798/controlplane-ai  
**Tag:** `v0.2.0-round2` (frozen baseline; `main` is the elevation tip judges should open)

Every AI response is a set of **claims requesting permission to act**. Provenance is captured **outside** the model (`STEP → SPAN → CLAIM → ACTION`). Unproven claims cannot authorize irreversible actions. Lane 1 is deterministic — no LLM on the critical path.

---

## 1. Portal uploads (five fields)

| # | Portal field | Artifact |
|---|---|---|
| 1 | Public GitHub link | https://github.com/Srujan0798/controlplane-ai |
| 2 | Prototype video | [`submission/ControlPlane_Round2_Prototype.mp4`](submission/ControlPlane_Round2_Prototype.mp4) |
| 3 | README document (PDF) | [`submission/ControlPlane_Round2_README.pdf`](submission/ControlPlane_Round2_README.pdf) |
| 4 | Business proposal (PDF) | [`submission/ControlPlane_Round2_Proposal.pdf`](submission/ControlPlane_Round2_Proposal.pdf) |
| 5 | Pitch deck (PPTX) | [`submission/ControlPlane_Round2_Pitch.pptx`](submission/ControlPlane_Round2_Pitch.pptx) |

Full checklist: [`docs/SUBMIT.md`](docs/SUBMIT.md) · Canon: [`round2/CONTROLPLANE_R2_FINAL.md`](round2/CONTROLPLANE_R2_FINAL.md) · [`round2/R2S5.md`](round2/R2S5.md)

---

## 2. Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
bash scripts/preflight-lite.sh   # must PASS
make run                         # http://127.0.0.1:8787
```

Autorun refund demo:  
http://127.0.0.1:8787/?scenario=refund&mode=enforce&autorun=1

Docker: `docker compose up --build` → http://localhost:8080

**Expected:** `show_text` → **Edit** · `issue_refund` → **Escalate** (held — never “blocked”).

```bash
python3 examples/refund_trace_demo.py
python3 examples/knowledge_flip_demo.py
```

---

## 3. Room flow (one path)

| Step | Open |
|---|---|
| Speak | [`round2/R2S5.md`](round2/R2S5.md) |
| Click | [`docs/JUDGE_RUNBOOK.md`](docs/JUDGE_RUNBOOK.md) |
| Defend | [`docs/HOSTILE_QA_DRILL.md`](docs/HOSTILE_QA_DRILL.md) |
| Mechanism | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |
| Prove | [`docs/ACCEPTANCE.md`](docs/ACCEPTANCE.md) |

---

## 4. Architecture

```text
STEP → SPAN → CLAIM → ACTION
Recorder → Binder → Entitlement → Interlock (frozen MATRIX)
```

Built: hash-chained ledger · ACL entitlement · dual-action refund · FastAPI OpenAI-compatible gate · Operate console · Docker/CI.

---

## 5. Layout

```text
README.md · AGENTS.md · LICENSE
controlplane/   policies/   tests/   examples/   scripts/
submission/     # PDF · PPTX · latency_bench.json · SBOM
round2/         # FINAL proposal · R2S5 pitch
docs/           # SUBMIT · JUDGE_RUNBOOK · HOSTILE_QA · ARCHITECTURE · ACCEPTANCE · ps.md
docs/reference/ # optional depth (not required to submit)
```

Team: Choda Srujan Sai · Dhrithika · IIT Gandhinagar
