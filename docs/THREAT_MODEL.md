# ControlPlane.ai — Threat model (Round 2)

STRIDE-style review of the **shipped Round 2 surface**: OpenAI-compatible proxy, Evidence Ledger, and judge console. Scoped to what is in this branch — not the full multi-lane production vision in [ARCHITECTURE.md](ARCHITECTURE.md).

**Branch:** `feature/round2-controlplane` · **Do not claim production-hardened auth.**

---

## Trust boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│  Judge / demo operator laptop                                   │
│  (browser console, curl, TestClient benches)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP (no auth in Round 2 demo)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  BOUNDARY A — HTTP surface                                      │
│  FastAPI app: controlplane/server/app.py                        │
│  · /v1/chat/completions (OpenAI-shaped proxy)                   │
│  · /v1/controlplane/demo/{scenario}                             │
│  · /v1/controlplane/metrics[+ /reset]                           │
│  · /v1/controlplane/requests/{id}/audit.jsonl                   │
│  · GET /  → static console (server/static/index.html)           │
└────────────────────────────┬────────────────────────────────────┘
                             │ in-process calls only (Lane 1)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  BOUNDARY B — Gate + ledger                                     │
│  ControlPlaneGate (pipeline.py)                                 │
│  ProvenanceRecorder → EvidenceLedger (hash-chained)             │
│  binder → entitlement → interlock (sole decider)                │
│  MetricsStore (in-memory shadow counters)                       │
│  PolicyRegistry (YAML packs under policies/)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │ optional env CONTROLPLANE_UPSTREAM_URL
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  BOUNDARY C — Upstream model (stub in Round 2)                  │
│  Not exercised on the judge demo path; scenarios are canned.    │
└─────────────────────────────────────────────────────────────────┘
```

| Boundary | Trust assumption | Round 2 reality |
|---|---|---|
| A (HTTP) | Caller is a local judge / CI | **Unauthenticated.** Bind to `127.0.0.1` for live demos. |
| B (Gate) | Process memory is not hostile | Single process; history capped at 500; resets wipe metrics. |
| C (Upstream) | Model is untrusted | Demo path never needs upstream; Lane 1 has **no LLM**. |

---

## Assets

1. **Actuator decisions** — Edit / Escalate / Pass / Block that gate irreversible money movement.
2. **Evidence Ledger** — append-only hash chain (`ledger.py`) proving what the model was allowed to know.
3. **Audit JSONL export** — judge-facing receipt download.
4. **Shadow metrics / FNR shape** — publishable counterfactuals (`shadow.py`).
5. **Policy packs** — blast-radius matrix transcription (`policies/*.yaml`).
6. **Console UX** — what judges believe they saw (must not invent commercial claims).

---

## STRIDE by component

### 1. OpenAI-compatible proxy (`app.py` · `/v1/chat/completions`)

| Threat | Risk | Mitigation mapped to code |
|---|---|---|
| **S** Spoofing caller identity | Low–Med (demo) | No API keys yet (PRIZE_WIN_MATRIX #49). Mitigate operationally: localhost bind. Principal is **fixture-bound** inside scenarios (`pipeline._rerun_refund`), not taken from request headers. |
| **T** Tampering request / scenario | Med | Unknown scenario → `HTTP 400` (`_run_scenario`). Chat path resolves only known canned fixtures; upstream passthrough is stubbed (`enable_upstream` / `CONTROLPLANE_UPSTREAM_URL` → 501). |
| **R** Repudiation of a gate decision | Low | Each result gets `request_id`; `GET .../audit.jsonl` rebuilds span/claim/decision lines; `chain_valid` from `EvidenceLedger.verify_chain()`. |
| **I** Information disclosure | Med | Demo payloads include span content (intentional for judges). Do not expose real PII fixtures. Metrics reset is open — anyone on the port can wipe counters (`POST /v1/controlplane/metrics/reset`). |
| **D** Denial of service | Med | No rate limit / body cap yet (#50–51). Negative test `test_oversized_json_does_not_500` asserts no 500 on ~1.5MB JSON; production must add hard limits. History truncates at 500 (`pipeline.py`). |
| **E** Elevation of privilege | Low–Med | Mode override (`?mode=enforce`) is intentional for judges. Policy packs are filesystem-loaded at process start — not mutable via HTTP. |

### 2. Evidence Ledger (`ledger.py`, `recorder.py`)

| Threat | Risk | Mitigation mapped to code |
|---|---|---|
| **S** Spoofed provenance | High if hook bypassed | Provenance is recorded **outside** the model at context assembly (`ProvenanceRecorder`). Demo path rebuilds the ledger inside the gate — model text cannot invent spans. |
| **T** Tamper ledger after the fact | Med | Append-only entries with `_sha256` hash chain; `verify_chain()` exposed in `GateResult.public_dict()["chain_valid"]`. |
| **R** Missing audit trail | Low | Steps, spans, claims, bindings, decisions all land in the ledger before actuators emit. |
| **I** Cross-tenant leakage in spans | Med (product) | Entitlement auditor (`entitlement.audit_claim`) compares span ACL vs principal clearance — R1 Edit on ACL miss (refund fixture). |
| **D** Ledger growth DoS | Low | In-memory per request; history list bounded. |
| **E** Forcing SUPPORTED | High (product) | Default verdict **UNSUPPORTED** (`binder.bind_claims`); derived claims never shallow-supported. Interlock is sole decider (`interlock.decide`). |

### 3. Judge console (`server/static/index.html` + `GET /`)

| Threat | Risk | Mitigation mapped to code |
|---|---|---|
| **S** Fake UI / phishing demo | Op | Serve only from our process; Docker Compose maps 8080. |
| **T** XSS via reflected scenario content | Low–Med | Console is static HTML/JS talking to same-origin APIs; fixture text is controlled. Still: treat future free-text fields as untrusted. |
| **R** Operator disputes what was shown | Low | Audit download + on-screen matrix cells / driving claims (receipts over rhetoric — PRODUCT.md). |
| **I** Metrics / history visible to anyone with URL | Med (demo) | Acceptable for stand demo; document in runbook — do not put on a public IP. |
| **D** UI spam-clicking demos | Low | Server-side sequential; metrics can be reset between rooms. |
| **E** UI claiming enforcement when shadow | Low | API returns `mode`, `enforced`, `would_hold`, `response_overlay.shadow` — console must display mode from JSON, not hard-code. |

---

## Abuse cases ↔ tests

| Abuse / negative | Test / check |
|---|---|
| Unknown scenario probe | `tests/test_security_negatives.py::test_unknown_scenario_is_400` |
| Metrics wiped / reset | `test_metrics_reset_works` |
| Health probe | `test_healthz_ok` |
| Oversized JSON | `test_oversized_json_does_not_500` |
| Non-deterministic actuators (integrity of demo) | `tests/test_determinism.py` |
| Dual-action refund integrity | `tests/test_policy_shadow_pipeline.py`, `tests/test_refund_scenario.py` |

---

## Explicit non-claims (Round 2)

- No API-key auth, mTLS, or signed audit exports yet.
- No request size / rate limits on the proxy.
- Upstream model passthrough is **not** the judge path.
- Threat model does **not** cover Lane 2/3 NLI or bias replay (deferred).

When elevating past demo: close PRIZE_WIN_MATRIX items 49–53, 67–74 before any public deployment language.
