# ControlPlane.ai

**Admission-control layer for AI that acts.**  
Accenture Innovation Challenge 2026 · Round 2 · Team ControlPlane · PS #1

**Public GitHub:** https://github.com/Srujan0798/controlplane-ai  
**Branch:** `main` only · **Frozen tag:** `v0.2.0-round2`

---

## 1. Portal uploads (five fields)

These are the only artifacts the submission portal needs.

| # | Portal field | Artifact |
|---|---|---|
| 1 | Public GitHub link | https://github.com/Srujan0798/controlplane-ai |
| 2 | Prototype video | [`submission/ControlPlane_Round2_Prototype.mp4`](submission/ControlPlane_Round2_Prototype.mp4) |
| 3 | README document (PDF) | [`submission/ControlPlane_Round2_README.pdf`](submission/ControlPlane_Round2_README.pdf) |
| 4 | Business proposal (PDF) | [`submission/ControlPlane_Round2_Proposal.pdf`](submission/ControlPlane_Round2_Proposal.pdf) |
| 5 | Pitch deck (PPTX) | [`submission/ControlPlane_Round2_Pitch.pptx`](submission/ControlPlane_Round2_Pitch.pptx) |

Operator checklist: [`docs/SUBMIT.md`](docs/SUBMIT.md) · Canon: [`round2/CONTROLPLANE_R2_FINAL.md`](round2/CONTROLPLANE_R2_FINAL.md) · [`round2/R2S5.md`](round2/R2S5.md)

---

## 2. Run in 60 seconds

Python 3.11+.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
bash scripts/preflight-lite.sh   # must PASS
make run                         # http://127.0.0.1:8787
```

Refund autorun: http://127.0.0.1:8787/?scenario=refund&mode=enforce&autorun=1  
Arbitrary text (no fixtures): http://127.0.0.1:8787/gate

**Expected on the refund path:** `show_text` → **Edit** · `issue_refund` → **Escalate** (**held** with the evidence packet — never “blocked”).

Docker: `docker compose up --build` → http://localhost:8080

```bash
python3 examples/refund_trace_demo.py
python3 examples/knowledge_flip_demo.py
make eval      # FNR / FPR with Wilson CI → evals/last_run.json
make verify    # tests, content laws, number freeze
```

---

## 3. What this is

Every AI response is a set of **claims requesting permission to act**. Provenance is captured **outside** the model (`STEP → SPAN → CLAIM → ACTION`). Unproven claims cannot authorize irreversible actions. Lane 1 is deterministic — no LLM on the critical path.

---

## 4. Architecture

```text
STEP → SPAN → CLAIM → ACTION
Recorder → Binder → Entitlement → Interlock (frozen MATRIX)
```

Built: hash-chained ledger · ACL entitlement · dual-action refund · FastAPI OpenAI-compatible gate · Operate console · Docker/CI.

Mechanism: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) · Acceptance: [`docs/ACCEPTANCE.md`](docs/ACCEPTANCE.md) · Runbook: [`docs/JUDGE_RUNBOOK.md`](docs/JUDGE_RUNBOOK.md)

---

## 5. Measured evidence

Do not copy figures from this file. Numbers are produced by `make eval` / `make bench` and frozen into the README PDF.

| Source | Path |
|---|---|
| Eval (FNR, FPR, Wilson CI, self-authored corpus) | [`evals/last_run.json`](evals/last_run.json) |
| Latency (n=10000, per-stage compute) | [`submission/latency_bench.json`](submission/latency_bench.json) |
| Judge-facing ledger | [`submission/ControlPlane_Round2_README.pdf`](submission/ControlPlane_Round2_README.pdf) |

40 ms is a Lane-1 **target**, never a measured p95.

---

## 6. Layout

```text
README.md · LICENSE
controlplane/   policies/   tests/   examples/   scripts/
submission/     # portal files: mp4 · README.pdf · Proposal.pdf · Pitch.pptx
round2/         # FINAL proposal · R2S5 pitch
docs/           # SUBMIT · JUDGE_RUNBOOK · HOSTILE_QA · ARCHITECTURE · ACCEPTANCE · ps.md
docs/reference/ # optional depth (not required to submit)
```

Team: Choda Srujan Sai · Dhrithika · IIT Gandhinagar
