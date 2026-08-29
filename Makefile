.PHONY: test coverage bench eval run judge e2e pdf sbom verify

test:
	pytest -q

# Coverage report (non-blocking soft gate). Does not run by default.
coverage:
	pytest --cov=controlplane --cov-report=term-missing

bench:
	CONTROLPLANE_RPM=100000 python3 scripts/load_bench.py -n 10000 --sweep

eval:
	python3 -m evals.run

verify: test
	pytest -q tests/test_content_laws.py
	$(MAKE) eval
	$(MAKE) bench
	$(MAKE) readme
	python3 scripts/verify.py

run:
	uvicorn controlplane.server.app:create_app --factory --host 127.0.0.1 --port 8787

judge:
	@echo "Judge runbook: docs/JUDGE_RUNBOOK.md"
	@echo "Docker (port 8080):  docker compose up --build"
	@echo "Local tip (port 8787 if 8080 is taken):"
	@echo "  uvicorn controlplane.server.app:create_app --factory --host 127.0.0.1 --port 8787"
	@echo "Autorun: http://127.0.0.1:8787/?scenario=refund&mode=enforce&autorun=1"
	@echo "Health: curl -s http://127.0.0.1:8787/healthz"
	@echo "Refund: curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce'"
	@echo "Prometheus: curl -s http://127.0.0.1:8787/prometheus"
	@python3 -c "import json; from pathlib import Path; p=Path('submission/latency_bench.json');\
	d=json.loads(p.read_text()) if p.exists() else {}; g=d.get('gate_latency_ms') or {};\
	print(f\"Latency bench (gate): p50={g.get('p50','n/a')} ms  p95={g.get('p95','n/a')} ms  ({p})\" if g else f'Latency bench: missing {p}')"

e2e:
	pytest -q tests/test_e2e_console.py

pdf:
	python3 scripts/build_proposal_pdf.py

readme:
	python3 scripts/build_readme_pdf.py

sbom:
	bash scripts/sbom.sh
