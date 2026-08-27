from fastapi.testclient import TestClient

from controlplane.models import Actuator
from controlplane.pipeline import ControlPlaneGate
from controlplane.server.app import create_app
from controlplane.shadow import MetricsStore


def test_prometheus_exposition_after_gate():
    metrics = MetricsStore()
    gate = ControlPlaneGate(metrics=metrics)
    client = TestClient(create_app(gate=gate))

    html = client.get("/metrics")
    assert html.status_code == 200
    assert "text/html" in html.headers.get("content-type", "")

    before = client.get("/prometheus")
    assert before.status_code == 200
    assert "controlplane_decisions_total 0" in before.text

    demo = client.post("/v1/controlplane/demo/refund?mode=enforce")
    assert demo.status_code == 200

    prom = client.get("/prometheus")
    text = prom.text
    assert "text/plain" in prom.headers.get("content-type", "")
    assert "controlplane_decisions_total" in text
    assert "controlplane_would_hold_total" in text
    assert "controlplane_gate_latency_ms" in text
    # refund demo records 2 decisions, both holding (Edit + Escalate)
    assert "controlplane_decisions_total 2" in text
    assert "controlplane_would_hold_total 2" in text
    line = [
        ln for ln in text.splitlines() if ln.startswith("controlplane_gate_latency_ms ")
    ][0]
    assert float(line.split()[-1]) >= 0.0


def test_metrics_store_prometheus_text_unit():
    store = MetricsStore()
    store.record(
        use_case="decision-support",
        actuator=Actuator.EDIT,
        mode="shadow",
    )
    store.record_latency(12.5)
    body = store.prometheus_text()
    assert "controlplane_decisions_total 1" in body
    assert "controlplane_would_hold_total 1" in body
    assert "controlplane_gate_latency_ms 12.5" in body
