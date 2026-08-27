# Judge runbook — 60 seconds

ControlPlane.ai · Accenture Innovation Challenge Round 2 · Team ControlPlane

Use this sheet at the stand. Do not improvise latency or hallucination claims.

Hostile room defense (one-liners + live curls): [HOSTILE_QA_DRILL.md](HOSTILE_QA_DRILL.md).

---

## Ports

| How you start | URL |
|---|---|
| **Docker Compose** (preferred for room) | http://localhost:**8080** |
| **Local uvicorn** (if 8080 is taken) | http://127.0.0.1:**8787** |

```bash
# Docker
docker compose up --build

# Local (8787)
source .venv/bin/activate
uvicorn controlplane.server.app:create_app --factory --host 127.0.0.1 --port 8787
```

Health check: `GET /healthz` → `{"ok": true, ...}`.

---

## 60-second script

Speak-from canon: [`round2/R2S5.md`](../round2/R2S5.md) (demo spine). Elevator if interrupted: *“Provenance outside the model, default unsupported, entitlement as set-membership, hard gate on the commit path. We publish what we miss.”*

1. **Cold open on the held refund** (8080 or 8787). Clearance / Operate strip already shows `HELD — ESCALATE` / `executed: false` — one graph, not three detectors. Do **not** open on a risk slide.
2. **Run refund · enforce** (UI button or):
   ```bash
   curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' | python3 -m json.tool
   ```
3. **Say the dual action out loud (centrepiece):**
   - `show_text` → **Edit** (R1 — ACL / entitlement)
   - `issue_refund` → **Escalate** (R3 — clause 7.2 **does not exist**; absence → `UNSUPPORTED`; money **held** with evidence packet)
4. **Never say “blocked.”** Say *held and escalated with the evidence packet.* Same response → Edit **and** Escalate.
5. **Show receipts:** matrix cell + driving claims on screen, or download `GET /v1/controlplane/requests/{id}/audit.jsonl`.
5b. **Optional principal flip (10s) — proves entitlement is identity, not text:**
   ```bash
   curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=analyst_01'   # → Edit
   curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=hr_partner_01' # → Pass
   ```
   Same span, same claim, same `content_hash`. Only the caller changed. Zero LLM. This is the argument against RAG groundedness — point at it running.
6. **Optional OpenAI shape (10s):**
   ```bash
   curl -s http://127.0.0.1:8787/v1/chat/completions \
     -H 'content-type: application/json' \
     -d '{"model":"controlplane-demo","messages":[{"role":"user","content":"Issue refund under clause 7.2"}],"scenario":"refund","mode":"enforce"}'
   ```
   Expect HOLD overlay + `controlplane` extension object.
7. **Close:** We do not score the model’s mind. We check membership in the evidence the model was given before an irreversible action fires.

---

## Failure recovery

| Symptom | Fix |
|---|---|
| Port 8080 already in use | Use **8787** locally, or `docker compose down` then up. |
| Console blank / 500 | Confirm `controlplane/server/static/index.html` exists; restart uvicorn. |
| `ok: false` / connection refused | `curl /healthz`; rebuild compose; `pip install -e ".[dev]"`. |
| Wrong actuators / weird metrics | `POST /v1/controlplane/metrics/reset`, re-run refund enforce. Determinism: five runs → same Edit+Escalate (`make test`). |
| Demo path returns 400 unknown scenario | Only `refund`, `support`, `copilot`, `decision`, `flip` (and aliases). Typo → 400 by design. |
| Judge asks for “live LLM” | Lane 1 is **deterministic only** — canned fixtures are the proof. Upstream is stubbed. |
| Panic | `make judge` prints this path + the uvicorn tip; re-read the Never-say list below. |

Pre-flight (once per room):

```bash
make test          # includes determinism + security negatives
make bench         # optional; refreshes submission/latency_bench.json
```

---

## What you NEVER say

| Forbidden | Say instead |
|---|---|
| **“40 ms p95”** / “forty millisecond p95” | **Targets:** ≤40 ms **p50** / ≤200 ms **p95**. **Measured** gate (`submission/latency_bench.json`, n=200): p50≈**0.074 ms**, p95≈**0.134 ms**. Never quote 40 ms as p95. |
| **“We eliminate hallucinations.”** | Ungrounded claims cannot **authorise actions**; we publish what we miss (FNR shape). |
| **“Zero added latency.”** / “zero integration.” | We never make the model feel slow; we make the **action** wait. Integration is the moat — days, not zero. |
| **“Blocked” the refund** | **Held / Escalated** with the evidence packet. |
| Clause 7.2 “caps” or “denies” / “doesn’t cover” | Clause 7.2 **does not exist** — absence → `UNSUPPORTED` → Escalate, not Block. |
| Customer lost money | Company **wrongly paid out** — found Friday. |
| One accuracy number across failure modes | Per-route measured % caught / % missed at 40 ms **p50**. |
| monitor · detect · observe · trust score · “AI safety” as virtue | authorise · admit · prove · bind · hold · escalate · gate |

Full hostile Q&A: [QA.md](QA.md). Drill sheet (one-liners + curls): [HOSTILE_QA_DRILL.md](HOSTILE_QA_DRILL.md). Architecture freezes: [ARCHITECTURE.md](ARCHITECTURE.md) §5, §10.

---

## Tag / release (do not run unless human asks)

When the human is ready (not automatic). Match [`EVENT_DAY_CHECKLIST.md`](EVENT_DAY_CHECKLIST.md):

```bash
git tag -a v0.2.0-round2 -m "Round 2 prize-day known-good"
# git push origin v0.2.0-round2   # only if remote publish approved
```

Work only on `main`. Do not create or push the tag until tests are green **and** a human approves.
