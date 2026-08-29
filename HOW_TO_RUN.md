# HOW_TO_RUN

## Judge / local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
uvicorn controlplane.server.app:create_app --factory --host 127.0.0.1 --port 8787
# or: docker compose up --build  → http://localhost:8080
```

```bash
make judge
bash orchestrator/scripts/preflight-lite.sh
```

## Demos

```bash
python3 examples/refund_trace_demo.py
python3 examples/multi_usecase_demo.py
python3 examples/knowledge_flip_demo.py
```

## Flow map

See `MASTER-FLOW.md`. Wave tasks under `work/` are **already shipped** (see `plan/EXECUTION.md` + `work/reports/`). Next work is prize-day verify + tag, not new scaffold.
