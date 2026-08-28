"""Shadow metrics CSV export (W7-07).

Real rows only; no invented FNR column. Verified via TestClient.
"""
from __future__ import annotations

import csv
import io

from fastapi.testclient import TestClient

from controlplane.server.app import create_app


def _client():
    return TestClient(create_app(store=None))


def test_csv_download_works():
    client = _client()
    r = client.post("/v1/controlplane/demo/refund?mode=enforce")
    assert r.status_code == 200
    rid = r.json()["request_id"]
    csv_resp = client.get("/v1/controlplane/metrics.csv")
    assert csv_resp.status_code == 200
    assert "text/csv" in csv_resp.headers.get("content-type", "")
    assert "attachment" in csv_resp.headers.get("content-disposition", "")

    reader = csv.reader(io.StringIO(csv_resp.text))
    rows = list(reader)
    assert rows[0] == [
        "request_id",
        "use_case",
        "mode",
        "mode_label",
        "ts_unix",
        "would_hold",
        "enforced",
        "text_actuator",
        "refund_actuator",
    ]
    # Find the row for the exact request we just ran.
    data = next(row for row in rows[1:] if row[0] == rid)
    # Refund demo persists under the decision-support use_case (policy pack name).
    assert data[1] == "decision-support"
    # enforce + would-hold (Escalate on issue_refund).
    assert data[5] == "1"
    assert data[8] == "Escalate"


def test_csv_has_no_invented_fnr_column():
    client = _client()
    csv_resp = client.get("/v1/controlplane/metrics.csv")
    assert csv_resp.status_code == 200
    header = csv_resp.text.splitlines()[0]
    # We deliberately do NOT publish a fake FNR percentage column.
    assert "fnr" not in header.lower()
    assert "published_fnr" not in header.lower()
