"""Console E2E / smoke tests.

Default path: FastAPI TestClient (httpx under the hood) — no browser install.
Optional: Playwright sync API when `playwright` is installed (extras: e2e).
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from controlplane.server.app import create_app

CONSOLE_ROUTES = (
    "/",
    "/policies",
    "/metrics",
    "/audit",
    "/matrix",
    "/architecture",
    "/runbook",
)


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


def test_console_routes_return_200(client: TestClient) -> None:
    for path in CONSOLE_ROUTES:
        r = client.get(path)
        assert r.status_code == 200, f"{path} -> {r.status_code}"
        assert "text/html" in r.headers.get("content-type", "")


def test_demo_refund_enforce_edit_and_escalate(client: TestClient) -> None:
    r = client.post("/v1/controlplane/demo/refund?mode=enforce")
    assert r.status_code == 200
    body = r.json()
    assert body["decisions"]["show_text"]["actuator"] == "Edit"
    assert body["decisions"]["issue_refund"]["actuator"] == "Escalate"


def test_audit_list_non_error(client: TestClient) -> None:
    page = client.get("/audit")
    assert page.status_code == 200
    listing = client.get("/v1/controlplane/requests")
    assert listing.status_code == 200
    payload = listing.json()
    assert "requests" in payload
    assert isinstance(payload["requests"], list)


def test_playwright_console_routes_optional() -> None:
    """Browser walk when playwright + chromium are available; else skip clearly."""
    sync_api = pytest.importorskip(
        "playwright.sync_api",
        reason="playwright not installed (optional extra: pip install '.[e2e]')",
    )
    import threading
    import time

    import uvicorn

    config = uvicorn.Config(create_app(), host="127.0.0.1", port=18787, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.time() + 10
    while not server.started and time.time() < deadline:
        time.sleep(0.05)
    if not server.started:
        pytest.skip("uvicorn test server failed to start for Playwright walk")

    try:
        with sync_api.sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception as exc:  # noqa: BLE001 — browser binary may be missing
                pytest.skip(f"Playwright chromium unavailable: {exc}")
            page = browser.new_page()
            for path in CONSOLE_ROUTES:
                resp = page.goto(
                    f"http://127.0.0.1:18787{path}", wait_until="domcontentloaded"
                )
                assert resp is not None and resp.status == 200, path
            browser.close()
    finally:
        server.should_exit = True
        thread.join(timeout=5)
