"""Multi-turn session ledger — parent chain of requests + compounding risk.

In-memory always. Optional SQLite tables on the same CONTROLPLANE_DB path as
``AuditStore``. Lane 1: no LLM, no network.
"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any

_HOLD_ACTUATORS = frozenset({"edit", "escalate", "block"})


def _canonical(obj: Any) -> str:
    return json.dumps(obj, separators=(",", ":"), default=str)


def _actuators_of(summary: dict[str, Any]) -> list[str]:
    raw: Any = summary.get("actuators")
    if raw is None:
        decisions = summary.get("decisions")
        if isinstance(decisions, dict):
            raw = [
                (v.get("actuator") if isinstance(v, dict) else v)
                for v in decisions.values()
            ]
        else:
            overlay = summary.get("response_overlay") or {}
            raw = overlay.get("actuators_applied") or overlay.get(
                "actuators_would_apply"
            )
    if isinstance(raw, dict):
        values = list(raw.values())
    elif isinstance(raw, (list, tuple)):
        values = list(raw)
    elif raw is None:
        values = []
    else:
        values = [raw]
    out: list[str] = []
    for item in values:
        if hasattr(item, "value"):
            out.append(str(item.value))
        else:
            out.append(str(item))
    return out


def _is_escalate(summary: dict[str, Any]) -> bool:
    return any(a.lower() == "escalate" for a in _actuators_of(summary))


def _is_hold(summary: dict[str, Any]) -> bool:
    if summary.get("would_hold") is True:
        return True
    if summary.get("action_allowed") is False:
        return True
    if summary.get("held") is True:
        return True
    holdback = summary.get("holdback")
    if isinstance(holdback, dict) and holdback.get("held") is True:
        return True
    return any(a.lower() in _HOLD_ACTUATORS for a in _actuators_of(summary))


class SessionStore:
    """Parent-chain of gate requests, in-memory + optional sqlite."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path: Path | None
        if path is None:
            self.path = None
        else:
            self.path = Path(str(path))
        self._lock = threading.Lock()
        self._sessions: dict[str, dict[str, Any]] = {}
        self._conn: sqlite3.Connection | None = None
        if self.path is not None:
            self._open_sqlite()

    @classmethod
    def from_env(cls) -> "SessionStore":
        raw = os.environ.get("CONTROLPLANE_DB")
        return cls(path=raw) if raw else cls()

    def _open_sqlite(self) -> None:
        assert self.path is not None
        try:
            if str(self.path) != ":memory:":
                self.path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(
                str(self.path),
                check_same_thread=False,
                timeout=30.0,
            )
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    principal_id TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS session_requests (
                    session_id TEXT NOT NULL,
                    request_id TEXT NOT NULL,
                    parent_request_id TEXT,
                    seq INTEGER NOT NULL,
                    summary TEXT NOT NULL,
                    attached_at REAL NOT NULL,
                    PRIMARY KEY (session_id, request_id)
                )
                """
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_session_requests_seq "
                "ON session_requests(session_id, seq)"
            )
            self._conn.commit()
            self._load_unlocked()
        except sqlite3.Error:
            self._conn = None

    def _load_unlocked(self) -> None:
        if self._conn is None:
            return
        rows = self._conn.execute(
            "SELECT session_id, principal_id, created_at FROM sessions"
        ).fetchall()
        for session_id, principal_id, created_at in rows:
            self._sessions[session_id] = {
                "session_id": session_id,
                "principal_id": principal_id,
                "created_at": created_at,
                "requests": [],
            }
        reqs = self._conn.execute(
            "SELECT session_id, request_id, parent_request_id, seq, summary, "
            "attached_at FROM session_requests ORDER BY seq ASC"
        ).fetchall()
        for session_id, request_id, parent, seq, summary, attached_at in reqs:
            sess = self._sessions.get(session_id)
            if sess is None:
                continue
            try:
                payload = json.loads(summary)
            except json.JSONDecodeError:
                payload = {"raw": summary}
            sess["requests"].append(
                {
                    "request_id": request_id,
                    "parent_request_id": parent,
                    "seq": int(seq),
                    "summary": payload,
                    "attached_at": attached_at,
                }
            )

    def begin_session(self, session_id: str, principal_id: str) -> dict[str, Any]:
        session_id = str(session_id)
        principal_id = str(principal_id)
        now = time.time()
        with self._lock:
            existing = self._sessions.get(session_id)
            if existing is not None:
                return self._public_unlocked(session_id)
            rec = {
                "session_id": session_id,
                "principal_id": principal_id,
                "created_at": now,
                "requests": [],
            }
            self._sessions[session_id] = rec
            if self._conn is not None:
                try:
                    self._conn.execute(
                        "INSERT OR IGNORE INTO sessions "
                        "(session_id, principal_id, created_at) VALUES (?, ?, ?)",
                        (session_id, principal_id, now),
                    )
                    self._conn.commit()
                except sqlite3.Error:
                    pass
            return self._public_unlocked(session_id)

    def attach_request(
        self,
        session_id: str,
        request_id: str,
        summary: dict[str, Any],
    ) -> dict[str, Any]:
        session_id = str(session_id)
        request_id = str(request_id)
        payload = dict(summary)
        now = time.time()
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                sess = {
                    "session_id": session_id,
                    "principal_id": "anonymous",
                    "created_at": now,
                    "requests": [],
                }
                self._sessions[session_id] = sess
                if self._conn is not None:
                    try:
                        self._conn.execute(
                            "INSERT OR IGNORE INTO sessions "
                            "(session_id, principal_id, created_at) "
                            "VALUES (?, ?, ?)",
                            (session_id, "anonymous", now),
                        )
                        self._conn.commit()
                    except sqlite3.Error:
                        pass
            for existing in sess["requests"]:
                if existing["request_id"] == request_id:
                    existing["summary"] = payload
                    existing["attached_at"] = now
                    self._persist_request_unlocked(session_id, existing)
                    return dict(existing)
            parent = (
                sess["requests"][-1]["request_id"] if sess["requests"] else None
            )
            rec = {
                "request_id": request_id,
                "parent_request_id": parent,
                "seq": len(sess["requests"]),
                "summary": payload,
                "attached_at": now,
            }
            sess["requests"].append(rec)
            self._persist_request_unlocked(session_id, rec)
            return dict(rec)

    def _persist_request_unlocked(
        self, session_id: str, rec: dict[str, Any]
    ) -> None:
        if self._conn is None:
            return
        try:
            self._conn.execute(
                "INSERT OR REPLACE INTO session_requests "
                "(session_id, request_id, parent_request_id, seq, summary, "
                "attached_at) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    session_id,
                    rec["request_id"],
                    rec["parent_request_id"],
                    rec["seq"],
                    _canonical(rec["summary"]),
                    rec["attached_at"],
                ),
            )
            self._conn.commit()
        except sqlite3.Error:
            return

    def compounding_risk(self, session_id: str) -> dict[str, Any]:
        session_id = str(session_id)
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                return {
                    "session_id": session_id,
                    "request_count": 0,
                    "prior_holds": 0,
                    "prior_escalations": 0,
                    "compounded": False,
                }
            holds = 0
            escalations = 0
            for rec in sess["requests"]:
                summary = rec.get("summary") or {}
                if _is_hold(summary):
                    holds += 1
                if _is_escalate(summary):
                    escalations += 1
            return {
                "session_id": session_id,
                "request_count": len(sess["requests"]),
                "prior_holds": holds,
                "prior_escalations": escalations,
                "compounded": escalations > 0,
            }

    def get(self, session_id: str) -> dict[str, Any] | None:
        session_id = str(session_id)
        with self._lock:
            if session_id not in self._sessions:
                return None
            return self._public_unlocked(session_id)

    def _public_unlocked(self, session_id: str) -> dict[str, Any]:
        sess = self._sessions[session_id]
        requests = [dict(r) for r in sess["requests"]]
        holds = 0
        escalations = 0
        for rec in requests:
            summary = rec.get("summary") or {}
            if _is_hold(summary):
                holds += 1
            if _is_escalate(summary):
                escalations += 1
        return {
            "session_id": sess["session_id"],
            "principal_id": sess["principal_id"],
            "created_at": sess["created_at"],
            "requests": requests,
            "parent_chain": [r["request_id"] for r in requests],
            "compounding_risk": {
                "session_id": session_id,
                "request_count": len(requests),
                "prior_holds": holds,
                "prior_escalations": escalations,
                "compounded": escalations > 0,
            },
        }

    def close(self) -> None:
        with self._lock:
            if self._conn is not None:
                self._conn.close()
                self._conn = None
