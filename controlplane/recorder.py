from __future__ import annotations
import hashlib
import itertools

from controlplane.ledger import EvidenceLedger
from controlplane.models import Principal, Span, Step, StepKind


def _content_hash(content: str) -> str:
    normalized = " ".join(content.split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


class ProvenanceRecorder:
    def __init__(self) -> None:
        self._step_seq = itertools.count(1)
        self._span_seq = itertools.count(1)

    def begin_request(
        self,
        request_id: str,
        principal: Principal,
        action_intent: str,
        policy_version: str = "matrix-v1",
    ) -> EvidenceLedger:
        led = EvidenceLedger.begin(request_id, principal, action_intent, policy_version)
        led.append(
            "request_begin",
            {
                "request_id": request_id,
                "principal": principal.id,
                "action_intent": action_intent,
            },
        )
        return led

    def record_step(self, led: EvidenceLedger, kind: StepKind, name: str) -> str:
        if led.context_frozen:
            raise RuntimeError("context assembly frozen; cannot record step")
        step_id = f"step-{next(self._step_seq)}"
        step = Step(step_id=step_id, kind=kind, name=name)
        led.steps[step_id] = step
        led.append("step", {"step_id": step_id, "kind": kind.value, "name": name})
        return step_id

    def record_span(
        self,
        led: EvidenceLedger,
        step_id: str,
        *,
        source_id: str,
        acl: frozenset[str],
        content: str,
        offsets: tuple[int, int] | None = None,
    ) -> str:
        if led.context_frozen:
            raise RuntimeError("context assembly frozen; cannot record span")
        if step_id not in led.steps:
            raise KeyError(f"unknown step_id: {step_id}")
        span_id = f"span-{next(self._span_seq)}"
        span = Span(
            span_id=span_id,
            step_id=step_id,
            source_id=source_id,
            acl=frozenset(acl),
            content=content,
            content_hash=_content_hash(content),
            offsets=offsets,
        )
        led.spans[span_id] = span
        led.append(
            "span",
            {
                "span_id": span_id,
                "step_id": step_id,
                "source_id": source_id,
                "acl": sorted(acl),
                "content_hash": span.content_hash,
            },
        )
        return span_id

    def finish_context_assembly(self, led: EvidenceLedger) -> None:
        led.context_frozen = True
        led.append("context_frozen", {"span_count": len(led.spans)})
