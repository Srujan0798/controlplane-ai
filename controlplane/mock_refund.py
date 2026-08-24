from __future__ import annotations

from typing import TypedDict


class RefundResult(TypedDict):
    committed: bool
    status: str


def execute_refund(allowed: bool) -> RefundResult:
    """Mock action executor. Honors interlock allowed flag.

    Vocabulary: REFUND HELD / REFUND COMMITTED — never "COMMIT BLOCKED".
    """
    if allowed:
        return {"committed": True, "status": "REFUND COMMITTED"}
    return {"committed": False, "status": "REFUND HELD"}
