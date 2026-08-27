# ControlPlane.ai

**Admission-control layer for AI that acts.**  
Accenture Innovation Challenge 2026 · Round 2 · Team ControlPlane · PS #1

Every AI response is a set of **claims requesting permission to act**. ControlPlane captures provenance **outside** the model at context-assembly time (`STEP → SPAN → CLAIM → ACTION`), binds claims to that provenance set, checks entitlement (ACL), and decides with a **frozen blast-radius matrix**.

Lane 1 is deterministic only — no LLM on the critical path.

## Official deliverables (`docs/ps.md`)

| Ask | Artifact |
|---|---|
| **1. Detailed Business Proposal** | [`round2/CONTROLPLANE_R2_FINAL.md`](round2/CONTROLPLANE_R2_FINAL.md) · PDF: [`submission/ControlPlane_Round2_Proposal.pdf`](submission/ControlPlane_Round2_Proposal.pdf) |
| **2. Working Prototype** | [`controlplane/`](controlplane/) · judge console · [`examples/`](examples/) · [`tests/`](tests/) |
| **3. Pitch Presentation** | [`round2/R2S5.md`](round2/R2S5.md) · deck: [`submission/ControlPlane_Round2_Pitch.pptx`](submission/ControlPlane_Round2_Pitch.pptx) |

## One-command judge demo

```bash
docker compose up --build
# open http://localhost:8080
```

Or locally (use **8787** if 8080 is already taken):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
uvicorn controlplane.server.app:create_app --factory --host 127.0.0.1 --port 8787
# open http://127.0.0.1:8787
```

## What judges will see

| Surface | URL / command |
|---|---|
| Enterprise console | http://127.0.0.1:8787 (or :8080 via Docker) |
| OpenAI-compatible gate | `POST /v1/chat/completions` |
| Live refund demo API | `POST /v1/controlplane/demo/refund?mode=enforce` |
| Shadow / FNR metrics | `GET /v1/controlplane/metrics` |
| Policy packs | `GET /v1/controlplane/policies` |
| Audit export | `GET /v1/controlplane/requests/{id}/audit.jsonl` |

### Curl — OpenAI shape

```bash
curl -s http://127.0.0.1:8787/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"controlplane-demo","messages":[{"role":"user","content":"Issue refund under clause 7.2"}],"scenario":"refund","mode":"enforce"}' \
  | python3 -m json.tool
```

Expected: user-visible text surgically edited; irreversible refund **held** (`Escalate`); `controlplane` extension carries the evidence ledger.

### CLI fixtures

```bash
python3 examples/refund_trace_demo.py       # R1 Edit + R3 Escalate (HELD)
python3 examples/multi_usecase_demo.py      # support / copilot / decision-support
python3 examples/knowledge_flip_demo.py     # entitlement principal-flip
```

## Project hierarchy

```text
SEBI/
├── README.md
├── pyproject.toml · Makefile · Dockerfile · docker-compose.yml
├── controlplane/                 ← core gate + FastAPI server + static console
├── policies/                     ← versioned YAML policy packs
├── examples/                     ← judge CLI demos
├── tests/                        ← criteria-locked + server/e2e tests
├── scripts/                      ← PDF build, load bench, SBOM
├── submission/                   ← proposal PDF, pitch PPTX, benches
├── docs/                         ← ARCHITECTURE, ROUND2-*, NARRATIVE, QA, runbook
├── round2/                       ← FINAL proposal + R2S5 pitch (canon)
└── .github/workflows/            ← CI
```

## Document map

| Audience | Open |
|---|---|
| Judges / submit | `round2/CONTROLPLANE_R2_FINAL.md` + live console + `submission/` |
| Pitch morning-of | `round2/R2S5.md` + `docs/JUDGE_RUNBOOK.md` |
| Engineers | this README + `controlplane/` + `docs/ARCHITECTURE.md` |
| Absolute truth (internal) | `docs/ARCHITECTURE.md`, `NARRATIVE.md`, `QA.md` |
| Agent workers (next tasks) | [`docs/AGENT_PROMPTS.md`](docs/AGENT_PROMPTS.md) · gaps: `docs/PRIZE_WIN_MATRIX.md` |
| Do **not** present | `round2/_archive/`, `docs/_archive/`, agent scratch, graphify cache |

## What shipped on this tree

- Provenance recorder + binder + entitlement + frozen interlock matrix
- Versioned YAML policy packs (`policies/`)
- Shadow mode + publishable FNR/FPR counters
- FastAPI OpenAI-compatible reverse proxy + judge console
- Docker Compose + GitHub Actions CI
- Fail-closed regressions (`tests/test_fail_closed.py`)

**Branch:** `main` — single source of truth after merge of `feature/round2-controlplane`.
