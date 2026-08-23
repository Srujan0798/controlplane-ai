# ControlPlane.ai

**Admission-control layer for AI that acts.**  
Accenture Innovation Challenge 2026 · Round 2 · Team ControlPlane

Every AI response is a set of **claims requesting permission to act**. ControlPlane captures provenance **outside** the model at context-assembly time (`STEP → SPAN → CLAIM → ACTION`), binds claims to that provenance set, checks entitlement (ACL), and decides with a **frozen blast-radius matrix**.

Lane 1 is deterministic only — no LLM on the critical path.

## One-command judge demo

```bash
docker compose up --build
# open http://localhost:8080
```

Or locally (use **8787** if 8080 is already taken on your machine):

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

### CLI fixtures (still available)

```bash
python3 examples/refund_trace_demo.py
python3 examples/multi_usecase_demo.py
```

## Docs

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — frozen system of record
- [docs/ROUND2-PROPOSAL.md](docs/ROUND2-PROPOSAL.md) — business proposal
- [docs/ROUND2-PITCH.md](docs/ROUND2-PITCH.md) — pitch narrative
- [docs/NARRATIVE.md](docs/NARRATIVE.md) / [docs/QA.md](docs/QA.md)

## Production elevation (this branch)

- Versioned YAML policy packs (`policies/`)
- Shadow mode + publishable FNR/FPR counters
- FastAPI OpenAI-compatible reverse proxy
- Judge console with live ledger / matrix cells / audit download
- Docker Compose + GitHub Actions CI

**Branch:** `feature/round2-controlplane` — do not merge to `main` until approved.
