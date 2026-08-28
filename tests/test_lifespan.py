"""Graceful shutdown lifespan (W7-05).

On app shutdown the AuditStore and SessionStore SQLite handles close so
WAL flushes and no connection outlives the process.
"""
from __future__ import annotations

import sqlite3

import pytest
from fastapi.testclient import TestClient

from controlplane.persist import AuditStore
from controlplane.session import SessionStore
from controlplane.server.app import create_app


def test_lifespan_closes_sqlite_handles(tmp_path):
    store = AuditStore(tmp_path / "audit.db")
    sessions = SessionStore(path=":memory:")
    app = create_app(store=store, sessions=sessions)
    with TestClient(app) as client:
        assert client.get("/healthz").status_code == 200
        assert store.ok()
    with pytest.raises(sqlite3.ProgrammingError):
        store.count()
    assert sessions._conn is None


def test_lifespan_tolerates_unopened_store():
    sessions = SessionStore()  # no sqlite: close() must be a safe no-op
    app = create_app(store=None, sessions=sessions)
    with TestClient(app) as client:
        assert client.get("/healthz").status_code == 200
    assert sessions._conn is None


def test_app_works_without_lifespan_context():
    # Existing suite pattern: plain TestClient never runs startup/shutdown.
    client = TestClient(create_app(store=None))
    assert client.get("/healthz").status_code == 200
