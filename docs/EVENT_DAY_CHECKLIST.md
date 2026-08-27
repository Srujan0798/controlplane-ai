# Event-day checklist — Round 2 prize stand

ControlPlane.ai · Accenture Innovation Challenge Round 2 · Team ControlPlane

Event readiness only. Full how-to-run: [README.md](../README.md). Judge 60s script + failure table: [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md).

---

## Night-before / morning-of

- [ ] **Backup laptop** charged, same repo checkout as primary, same known-good commit (see below).
- [ ] Primary laptop charged; HDMI/USB-C adapter tested; browser zoom set for projector.
- [ ] `git status` clean on `main` (or only intentional local notes).
- [ ] Print or pin this checklist + [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) failure table.

---

## Known-good commit

Record the SHA you will demo from (do not improvise mid-room):

```bash
git rev-parse HEAD
git log -1 --oneline
```

Write it here before walking in: `________________` (full SHA).

### Annotated tag (human-approved only)

Do **not** create or push a tag until tests are green **and** a human approves. Suggested command only:

```bash
git tag -a v0.2.0-round2 -m "Round 2 prize-day known-good"
# git push origin v0.2.0-round2   # only if remote publish approved
```

To verify later: `git show v0.2.0-round2` / `git rev-parse v0.2.0-round2`.

---

## Ports

| Mode | Port | URL |
|---|---|---|
| **Docker Compose** (preferred for room) | **8080** | http://localhost:8080 |
| **Local uvicorn** (fallback if 8080 taken) | **8787** | http://127.0.0.1:8787 |

Health: `GET /healthz` → `{"ok": true, ...}`.

If 8080 is busy: use 8787, or `docker compose down` then `docker compose up --build`. Details: [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) § Ports / Failure recovery.

---

## USB / airgap offline

Assume venue Wi‑Fi fails. Before leaving base:

- [ ] Full clone on both laptops (no need to `git pull` on site).
- [ ] `.venv` already created and `pip install -e ".[dev]"` done **or** Docker images already built (`docker compose build`).
- [ ] Optional: copy repo + `.venv` (or a tarball of the image) to USB as cold spare.
- [ ] Confirm demos run **without** network: Lane 1 is deterministic; no live LLM required for the refund / flip path.
- [ ] Open console from localhost only; do not depend on CDN or remote fonts beyond what ships in-tree.

Smoke offline:

```bash
make test
make judge          # prints URLs / curls — no network needed for the echoes
# then either:
docker compose up --build
# or:
make run            # uvicorn on 8787
```

---

## Pre-flight commands (once per room)

```bash
make test           # pytest -q (determinism + security negatives)
make judge          # prints runbook path, Docker/local tips, health/refund curls, bench p50/p95
# optional:
make bench          # refreshes submission/latency_bench.json
make e2e            # console e2e smoke
```

Docker path (preferred):

```bash
docker compose up --build
# open http://localhost:8080
curl -s http://localhost:8080/healthz
```

Local path:

```bash
source .venv/bin/activate
make run
# open http://127.0.0.1:8787
curl -s http://127.0.0.1:8787/healthz
```

---

## Makefile targets (confirmed on `main`)

| Target | What it does |
|---|---|
| `make test` | `pytest -q` |
| `make bench` | Load bench → updates latency numbers (`CONTROLPLANE_RPM=100000`, `scripts/load_bench.py -n 200`) |
| `make run` | Local uvicorn on **127.0.0.1:8787** |
| `make judge` | Prints [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) path, Docker **8080** / local **8787** tips, health + refund curls, latency bench summary |
| `make e2e` | `pytest -q tests/test_e2e_console.py` |
| `make pdf` | `python3 scripts/build_proposal_pdf.py` |
| `make sbom` | `bash scripts/sbom.sh` |

See also [README.md](../README.md) for install and console map.

---

## Panic recovery

Stay on the failure table in [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) § **Failure recovery**. Quick pointers:

| Symptom | First move |
|---|---|
| Port 8080 in use | Switch to **8787** (`make run`) or `docker compose down` then up |
| Console blank / 500 | Confirm static `index.html`; restart uvicorn / compose |
| Connection refused / `ok: false` | `curl /healthz`; rebuild compose; `pip install -e ".[dev]"` |
| Weird actuators / metrics | `POST /v1/controlplane/metrics/reset`; re-run refund enforce; `make test` |
| Unknown scenario 400 | Only known demo names — typo fails closed by design |
| Judge asks for live LLM | Lane 1 is deterministic; canned fixtures are the proof |
| Full panic | `make judge`; re-read Never-say list in the runbook |

Autorun tip (from `make judge`):  
`http://127.0.0.1:8787/?scenario=refund&mode=enforce&autorun=1`

Never say “blocked” — say **held / escalated with evidence packet**. Never quote marketing p95; use measured bench if pressed.

---

## Submission artifacts (spot-check)

- [ ] `submission/ControlPlane_Round2_Proposal.pdf`
- [ ] `submission/ControlPlane_Round2_Pitch.pptx`
- [ ] `submission/latency_bench.json` (after `make bench` if you refreshed)
- [ ] SBOM output from `make sbom` (path per `scripts/sbom.sh`)

---

## End-of-day

- [ ] `docker compose down` (if used)
- [ ] Note final demo SHA again: `git rev-parse HEAD`
- [ ] Do not force-push; do not retag without human approval
