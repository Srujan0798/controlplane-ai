# ControlPlane.ai

Admission-control layer prototype: **STEP → SPAN → CLAIM → ACTION**.

Binds every claim to the evidence the model was actually given, and spends
verification budget in proportion to what the response is about to do.

## Requirements

- Python ≥ 3.11
- Stdlib-first core (pytest for tests)

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Package

Typed models live in `controlplane.models` (`Principal`, `Step`, `Span`, `Claim`,
`Binding`, `Action`, `Decision`, `EntitlementFinding`, and related enums).

Default claim verdict is **UNSUPPORTED**. No LLM on the critical path.
