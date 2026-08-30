# INTERNAL ENGINEERING BOARD — NOT PRODUCT SURFACE

**Not a portal upload. Not part of the product claim.** Operator excellence checklist only.

# Excellence Gate — 100/100 means this, not “pytest green”

**Rule:** An agent may say **DONE** only if every row in the task’s Excellence Checklist is **YES** with pasted command output.  
`pytest passed` alone = **NOT DONE**. Dummy / partial / nested-broken / uncommitted = **REJECT**.

Branch: `feature/round2-elevation` · Fallback: `v0.2.0-round2` · Design score ceiling: **99** + honesty point.

---

## 0. Universal DONE definition (every agent)

Paste this at the top of every agent prompt:

```
DONE is forbidden unless ALL of these are true and you paste evidence:

1. Acceptance in tasks/<ID>.md — every bullet — demonstrated with commands.
2. Full suite: `pytest -q` → 0 failed (no ignores, no “skip the broken file”).
3. Content laws: `pytest -q tests/test_content_laws.py` green.
4. Owns-only commits; frozen files untouched (ARCHITECTURE, interlock MATRIX, Actuator/BlastTier, AGENTS.md).
5. No regression of a prior DONE task (prove with a smoke command that still works).
6. If you touch app.py / pipeline / binder: curl or TestClient hit for every new HTTP route — unit tests on a Store class are NOT enough.
7. Numbers in PDF/PPTX/README/video MUST equal `make eval` / `make bench` output — or `make verify` fails.
8. Working tree clean for your Owns after commit. Untracked “almost done” = NOT DONE.
9. Refund language: held / escalated with evidence packet — never “blocked”.
10. Report format: DONE|REJECT-SELF · SHA · pytest line · smoke commands · concerns.

If anything is partial, reply REJECT-SELF and list the missing YES rows. Do not claim DONE.
```

---

## 1. Honest score right now (audited 2026-08-30)

| Band | Score | Meaning |
|---|---|---|
| Mechanism spine (extract→binder→PII→lanes→matrix) | ~84 | Real: zero-fixture refund, analyze API, override route live, 16-cell tests |
| Numbers (eval+bench+economist) | ~92 | `make eval` FNR=1.1% (CI 0.2–5.8%) honest; n=10000 bench; hard negatives 31.7%; self-authored stated |
| Governance | ~94 | override HTTP live (top-level, tested); bias/jurisdiction/canary/threshold code exists |
| Multi-turn | ~96 | `examples/multiturn_demo.py` prints turn1 Pass+annotate, turn3 Escalate; test passes |
| Room / Track B | ~95 | Gate page + PDFs + PPTX + video(w/voiceover) exist; `make verify` ALL GREEN |
| **Excellence / submit-ready** | **≠ 100** | portal-complete + honest prototype; see §2 |

**Do not tell judges you are 100.** Tell them the honest ceiling (~95) when verify is green and Track B is complete. FNR is published with a real miss story, not a fake-perfect 0%.

---

## 2. Excellence checklist by deliverable (YES/NO)

### Track A — mechanism

| # | Excellence criterion | Status now |
|---|---|---|
| A1 | Refund Edit+Escalate(held), **zero fixtures**, amount via **numeric** not fixture | YES (smoke: examples/refund_trace_demo.py) |
| A2 | All 16 matrix cells reachable via production binder paths | YES (tests) |
| A3 | `POST /v1/controlplane/analyze` works on arbitrary text | YES (TestClient 200) |
| A4 | `POST /v1/controlplane/decisions/{id}/override` registered + TestClient 200 + ledger chain | **YES** — top-level route `app.py:677`; `tests/test_override_api.py` green |
| A5 | PII Rule A: fabricated PAN → Block at R3 (integration) | YES (unit) — re-prove with analyze smoke |
| A6 | EU vs IN packs → **different actuators** (behaviour, not YAML labels) | YES (tests) |
| A7 | Multi-turn: turn1 Pass+annotate, turn3 Escalate **and** `python3 examples/multiturn_demo.py` prints chain | **YES** — demo exists; test passes |
| A8 | Lanes: slow Lane2 → UNKNOWN; slow probabilistic never overturns deterministic | YES (tests) |
| A9 | `make eval` FNR/FPR with Wilson CI; hard negatives ≥20%; self-authored stated; thresholds have FP/FN curve | **YES** — FNR=1.1% (CI 0.2–5.8%), hard neg 31.7%, self-authored stated, threshold curve printed |
| A10 | Live gate/shadow `published_fnr` reads last eval (not forever None) | **YES** — `/v1/controlplane/metrics` returns published_fnr from last_run.json |
| A11 | Bench n=10000 + stages + methodology; never 40ms as p95 | YES |
| A12 | Full `pytest -q` green on clean tree | **YES** — 340 passed, 2 skipped; `make verify` ALL GREEN |

### Track B — portal uploads

| # | Excellence criterion | Status now |
|---|---|---|
| B1 | Public GitHub URL resolves in browser; CI green; README renders | **YES** — curl 200 PUBLIC; README renders 5 portal fields |
| B2 | README PDF ≤20MB, capability ledger, every command works from clean clone | **YES** — 8.6KB, ledger, `make verify --drift-only` green |
| B3 | Proposal PDF rebuilt from **measured** eval/bench numbers only | **YES** — 15pp; seven sections; number-diff verify green |
| B4 | PPTX rebuilt from JS; same number freeze; content laws on extracted text | **YES** — rebuilt from JS; n=10000 numbers; content laws green |
| B5 | Prototype video `.mp4` 1080p, shows live gate (not slides), held≠blocked | **YES** — 212.8s, voiceover muxed, Edit+Escalate on screen, never "blocked" |
| B6 | `make verify` green: preflight → tests → laws → eval → bench → **PDF/deck number diff** | **YES** — `make verify` ALL GREEN, no drift |

---

## 3. REJECT list — agents claiming DONE with these = fire the claim

1. “Tests passed” but HTTP route 404  
2. Commit message `T7.x` while Wave 7 gate (T3.2+T3.4 numbers freeze) was faked  
3. Nested / broken `app.py` that silently disables another task’s route  
4. Missing Owns file (`examples/multiturn_demo.py`, `VIDEO_SCRIPT`, `.mp4`)  
5. Uncommitted WIP left as “done in working tree”  
6. FNR = 0.000 with no hard-negative analysis and no published miss story  
7. PDF quotes a number not in `evals/last_run.json` / `submission/latency_bench.json`  
8. Remote configured but GitHub page 404 / private / bad credentials  
9. `pytest --ignore=…` to hide red  
10. Touching frozen MATRIX / ARCHITECTURE “just this once”

---

## 4. Rework queue — assign in this order (excellence, not busywork)

### R0 — YOU (human) — submission blocker
```
tasks/T0.1.md
Prove: browser opens public repo; Actions green; .env.example placeholders only.
```

### R1 — Agent FIX-OVERRIDE (blocks governance excellence)
```
Read docs/EXCELLENCE_GATE.md §0. Fix T5.2 regression:
- Un-nest override_decision from analyze_arbitrary in controlplane/server/app.py
- Register top-level POST /v1/controlplane/decisions/{decision_id}/override
- Add tests/test_override_api.py with TestClient: refund demo → override → 200 → ledger has override → chain_valid
- Prove: python3 -c "… list routes …" shows override path
- pytest -q green; no Owns outside app.py + that test
Commit: FIX: restore override route broken by T7.1 nesting
REJECT-SELF if route still missing from app.routes
```

### R2 — Agent T6.2
```
Read docs/EXCELLENCE_GATE.md §0 and tasks/T6.2.md
Create examples/multiturn_demo.py that prints turn1 actuator, turn3 actuator, inheritance.
Prove: python3 examples/multiturn_demo.py exits 0 and shows Escalate on turn3.
pytest -q tests/test_multiturn.py green.
```

### R3 — Agent T3.2-HARDEN
```
Excellence: published_fnr must surface in gate/metrics from evals/last_run.json after make eval.
Hard negatives documented in evals/README.md (≥20%).
Derived-route precision 0% must be explained or fixed — do not ship silent garbage.
make eval output pasted in report. Thresholds: FP/FN curve printed (not magic constants only).
```

### R4 — Agent T8-VERIFY
```
Only after R1–R3.
Implement/finish make verify: tests + laws + eval + bench + diff every number in PDF/PPTX/README vs last_run.json + latency_bench.json.
Working tree clean. pytest -q green INCLUDING test_verify.
REJECT-SELF if any quoted number drifts.
```

### R5 — Agents T7.2/T7.3/T7.4 REBUILD (after R4 numbers freeze)
```
Rebuild README PDF, proposal PDF, deck ONLY from frozen make eval / make bench output.
Content laws green on extracted text. Capability ledger honest (designed vs proven).
```

### R6 — Human + agent T7.5
```
docs/VIDEO_SCRIPT.md + record mp4 per submission protocol (prototype, not pitch).
Show analyze/gate live. Never say blocked for refund.
```

### R7 — Final excellence review agent
```
Re-run every YES/NO row in docs/EXCELLENCE_GATE.md §2.
Any NO → REJECT submission readiness.
Paste make verify full output.
```

---

## 5. What “100% effort” looks like for an agent report

Bad (reject):
> DONE. 12 tests passed.

Good (acceptable):
> DONE  
> SHA: abc123  
> pytest -q: 340 passed, 0 failed  
> smoke: TestClient POST …/override → 200; routes include override  
> smoke: refund demo Edit+Escalate; amount method=numeric  
> content laws: 10 passed  
> Owns only: app.py, test_override_api.py  
> Concerns: none  

---

## 6. Scoreboard language for you

| Phrase agents use | What you should hear |
|---|---|
| “tests pass” | **Incomplete** until smoke + excellence rows YES |
| “committed” | **Incomplete** until verify + no regression |
| “DONE” without pasted commands | **Lie** — send back with EXCELLENCE_GATE §0 |
| “PARTIAL / REJECT-SELF” | **Honest** — this is the only allowed non-DONE |

When every §2 row is YES and Track B uploads exist: you are submit-ready at design **~99**, with the honesty admission as the last point — that is excellence. Dummy green is not.
