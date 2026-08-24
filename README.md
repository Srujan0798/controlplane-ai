# ControlPlane.ai — Accenture Innovation Challenge 2026 · Round 2

Admission-control layer for AI that **acts**: every response is a set of **claims requesting permission to act**. Provenance is captured outside the model (`STEP → SPAN → CLAIM → ACTION`). Unproven or unauthorized claims cannot authorize actions.

## Official deliverables (`docs/ps.md`)

| Ask | Artifact |
|---|---|
| **1. Detailed Business Proposal** | [`round2/CONTROLPLANE_R2_FINAL.md`](round2/CONTROLPLANE_R2_FINAL.md) |
| **2. Working Prototype** | [`controlplane/`](controlplane/) · [`examples/`](examples/) · [`tests/`](tests/) |
| **3. Pitch Presentation** | *Next — build from FINAL + live demo* |

## How to run the prototype

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python3 -m pytest tests/ -v
python3 examples/refund_trace_demo.py      # R1 Edit + R3 Escalate (HELD)
python3 examples/knowledge_flip_demo.py    # entitlement principal-flip
```

**Expected:** refund path = **Escalate (held)** / `committed=false` — never “blocked”. Knowledge path flips **Edit → Pass** when only the principal changes.

## Project hierarchy

```text
SEBI/
├── README.md                          ← you are here
├── pyproject.toml
├── controlplane/                      ← working prototype
├── examples/                          ← judge demos
├── tests/                             ← 36 criteria-locked tests
├── docs/
│   ├── ps.md                          ← official Round 2 brief
│   ├── ARCHITECTURE.md · NARRATIVE.md · QA.md
│   └── … (PDFs / internal plans)
└── round2/
    ├── CONTROLPLANE_R2_FINAL.md       ← THE proposal (dense)
    ├── README.md
    └── _archive/                      ← drafts & old locks (do not submit)
```

## Document map

| Audience | Open |
|---|---|
| Judges / submit | `round2/CONTROLPLANE_R2_FINAL.md` + live demos |
| Engineers | this README + `controlplane/` |
| Absolute truth (internal) | `docs/ARCHITECTURE.md`, `NARRATIVE.md`, `QA.md` |
| Do **not** present | `round2/_archive/`, agent drafts, graph tooling |

Open the FINAL and read **Stage Check** at the top — R2S1–R2S4 coverage and all 10 eternal invariants are marked **PASS**.
