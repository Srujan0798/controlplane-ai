# Round 2 — pitch & proposal canon

## Submit / pitch

- **[`CONTROLPLANE_R2_FINAL.md`](CONTROLPLANE_R2_FINAL.md)** — dense Stages 1–4 hybrid (business proposal truth).
- **[`R2S5.md`](R2S5.md)** — Stage 5 frozen pitch architecture (speak from this).

Start at **Stage Check** (top of FINAL): R2S1–R2S4 = **PASS**, 10 invariants = **PASS**.

Packaged binaries live in [`../submission/`](../submission/).

## Prototype (repo root)

```bash
cd ..
python3 -m pytest tests/ -q
python3 examples/refund_trace_demo.py
python3 examples/multi_usecase_demo.py
python3 examples/knowledge_flip_demo.py
# or: docker compose up --build  → http://localhost:8080
```

## `_archive/`

Draft shards, old stage locks, bloated prior FINAL — **local provenance only. Do not submit.**
