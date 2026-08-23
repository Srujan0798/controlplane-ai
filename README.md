# ControlPlane.ai

Admission-control layer prototype: **STEP → SPAN → CLAIM → ACTION**.

Binds every claim to the evidence the model was actually given, and spends
verification budget in proportion to what the response is about to do.

## Requirements

- Python ≥ 3.11
- Stdlib-first core (pytest for tests)

## Round 2 quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python3 examples/refund_trace_demo.py
python3 examples/multi_usecase_demo.py
```

## Docs

- [docs/ROUND2-PROPOSAL.md](docs/ROUND2-PROPOSAL.md) — business proposal
- [docs/ROUND2-PITCH.md](docs/ROUND2-PITCH.md) — pitch narrative
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — system architecture

## Package

Typed models live in `controlplane.models` (`Principal`, `Step`, `Span`, `Claim`,
`Binding`, `Action`, `Decision`, `EntitlementFinding`, and related enums).

Default claim verdict is **UNSUPPORTED**. No LLM on the critical path.
