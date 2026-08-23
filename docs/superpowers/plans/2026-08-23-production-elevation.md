# Production Elevation Plan — Win Round 2

> Branch only: `feature/round2-controlplane` · **DO NOT MERGE TO MAIN** until human says so.

**Goal:** Elevate the Provenance Recorder MVP into an enterprise-grade ControlPlane demonstration: OpenAI-compatible reverse proxy, judge console, versioned policy packs, shadow/FNR metrics, Docker one-shot, and a production pitch deck — without reopening the frozen architecture.

**Architecture (frozen):** STEP→SPAN→CLAIM→ACTION · Provenance outside the model · default UNSUPPORTED · matrix transcribed · Interlock sole decider · deployment shape = OpenAI-compatible proxy + context-assembly SDK · shadow default · ≤40ms p50 / ≤200ms p95 on R0/R1 (never quote 40ms as p95).

**Stack:** Python 3.11+, FastAPI, httpx, uvicorn, PyYAML, Jinja2/static console, Docker Compose, PptxGenJS for deck.

## Surfaces

| Surface | Purpose |
|---|---|
| `controlplane.pipeline` | Production gate: assemble → bind → entitle → decide → (shadow\|enforce) |
| `controlplane.policy` | Versioned YAML packs per use-case (support / copilot / refund) |
| `controlplane.shadow` | Dual-emit counterfactual + FNR/FP counters |
| `controlplane.server` | FastAPI: `/v1/chat/completions` proxy, `/v1/controlplane/*` APIs, `/` console |
| `console/` | Enterprise judge UI — live ledger, matrix cell, actuators, hash chain |
| `docker-compose.yml` | One command for judges |
| `submission/ControlPlane_Round2_Pitch.pptx` | Production pitch |

## Non-negotiables

- No LLM on Lane 1 critical path
- Clause 7.2 does not exist
- Matrix never redrawn
- Work stays on feature branch — no merge

## Build order

1. Policy + shadow + pipeline  
2. FastAPI proxy + APIs  
3. Judge console  
4. Docker  
5. PPTX  
6. CI + audit export + docs sync  
