from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from controlplane.models import (
    Action, Binding, Claim, Decision, Principal, Span, Step,
)


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class LedgerEntry:
    seq: int
    entry_type: str
    payload: dict[str, Any]
    prev_hash: str
    hash: str


@dataclass
class EvidenceLedger:
    request_id: str
    principal: Principal
    action_intent: str
    policy_version: str
    _entries: list[LedgerEntry] = field(default_factory=list)
    steps: dict[str, Step] = field(default_factory=dict)
    spans: dict[str, Span] = field(default_factory=dict)
    claims: dict[str, Claim] = field(default_factory=dict)
    bindings: dict[str, Binding] = field(default_factory=dict)
    actions: dict[str, Action] = field(default_factory=dict)
    decisions: dict[str, Decision] = field(default_factory=dict)
    context_frozen: bool = False

    @classmethod
    def begin(
        cls,
        request_id: str,
        principal: Principal,
        action_intent: str,
        policy_version: str = "matrix-v1",
    ) -> "EvidenceLedger":
        return cls(
            request_id=request_id,
            principal=principal,
            action_intent=action_intent,
            policy_version=policy_version,
        )

    def append(self, entry_type: str, payload: dict[str, Any]) -> str:
        prev = self._entries[-1].hash if self._entries else "GENESIS"
        digest = _sha256(prev + _canonical({"type": entry_type, "payload": payload}))
        self._entries.append(
            LedgerEntry(
                seq=len(self._entries),
                entry_type=entry_type,
                payload=dict(payload),
                prev_hash=prev,
                hash=digest,
            )
        )
        return digest

    def verify_chain(self) -> bool:
        prev = "GENESIS"
        for entry in self._entries:
            if entry.prev_hash != prev:
                return False
            expected = _sha256(prev + _canonical({"type": entry.entry_type, "payload": entry.payload}))
            if expected != entry.hash:
                return False
            prev = entry.hash
        return True

    def get(self, entry_type: str) -> list[LedgerEntry]:
        return [e for e in self._entries if e.entry_type == entry_type]
