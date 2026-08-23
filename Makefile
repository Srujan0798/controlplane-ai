.PHONY: test bench run judge

test:
	pytest -q

bench:
	python3 scripts/load_bench.py -n 200

run:
	uvicorn controlplane.server.app:create_app --factory --host 127.0.0.1 --port 8787

judge:
	@echo "Judge runbook: docs/JUDGE_RUNBOOK.md"
	@echo "Docker (port 8080):  docker compose up --build"
	@echo "Local tip (port 8787 if 8080 is taken):"
	@echo "  uvicorn controlplane.server.app:create_app --factory --host 127.0.0.1 --port 8787"
	@echo "Health: curl -s http://127.0.0.1:8787/healthz"
	@echo "Refund: curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce'"
