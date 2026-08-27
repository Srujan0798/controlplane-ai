"""SQLite audit store for gate public_dict results.

Path from CONTROLPLANE_DB (default ``.data/controlplane.db``). Stdlib sqlite3 only.
"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any

_DEFAULT_DB = ".data/controlplane.db"


class AuditStore:
    """Thread-safe append/replace store keyed by request_id."""

    def __init__(self, path: str | Path | None = None) -> None:
        raw = path if path is not None else os.environ.get("CONTROLPLANE_DB", _DEFAULT_DB)
        self.path = Path(str(raw))
        if str(self.path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(
            str(self.path),
            check_same_thread=False,
            timeout=30.0,
        )
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=NORMAL")
        with self._lock:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS gate_results (
                    request_id TEXT PRIMARY KEY,
                    saved_at REAL NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_gate_results_saved_at "
                "ON gate_results(saved_at DESC)"
            )
            self._conn.commit()

    @classmethod
    def from_env(cls) -> "AuditStore":
        return cls()

    def save(self, public_dict: dict[str, Any]) -> None:
        request_id = public_dict.get("request_id")
        if not request_id:
            raise ValueError("public_dict requires request_id")
        payload = json.dumps(public_dict, separators=(",", ":"), default=str)
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO gate_results "
                "(request_id, saved_at, payload) VALUES (?, ?, ?)",
                (str(request_id), time.time(), payload),
            )
            self._conn.commit()

    def list(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        limit = max(0, int(limit))
        offset = max(0, int(offset))
        with self._lock:
            rows = self._conn.execute(
                "SELECT payload FROM gate_results "
                "ORDER BY saved_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()
        return [json.loads(row[0]) for row in rows]

    def get(self, request_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT payload FROM gate_results WHERE request_id = ?",
                (request_id,),
            ).fetchone()
        if row is None:
            return None
        return json.loads(row[0])

    def count(self) -> int:
        with self._lock:
            (n,) = self._conn.execute("SELECT COUNT(*) FROM gate_results").fetchone()
        return int(n)

    def ok(self) -> bool:
        try:
            with self._lock:
                self._conn.execute("SELECT 1").fetchone()
            return True
        except sqlite3.Error:
            return False

    def close(self) -> None:
        with self._lock:
            self._conn.close()
