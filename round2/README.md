# Round 2 — one file

## Submit / pitch

**[`CONTROLPLANE_R2_FINAL.md`](CONTROLPLANE_R2_FINAL.md)** — dense Stages 1–4 hybrid.

Start at **Stage Check** (top of that file): R2S1–R2S4 = **PASS**, 10 invariants = **PASS**.

## Prototype (repo root)

```bash
cd ..
python3 -m pytest tests/ -v
python3 examples/refund_trace_demo.py
python3 examples/knowledge_flip_demo.py
```

## `_archive/`

Draft shards, old stage locks, bloated prior FINAL — **local provenance only. Do not submit.**
