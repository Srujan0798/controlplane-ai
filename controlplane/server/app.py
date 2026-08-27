"""FastAPI application — production admission-control surface."""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from controlplane import signing, upstream, webhook
from controlplane.holdback import admit_for_decisions
from controlplane.persist import AuditStore
from controlplane.pipeline import ControlPlaneGate
from controlplane.policy import PolicyRegistry
from controlplane.session import SessionStore
from controlplane.security import (
    MAX_BODY_SIZE,
    SECURITY_HEADERS,
    RateLimiter,
    api_key_authorized,
    client_ip,
    content_length_ok,
)
from controlplane.shadow import MetricsStore
from controlplane.scenarios.multi_usecase import (
    run_customer_support,
    run_decision_refund,
    run_knowledge_copilot,
)

ROOT = Path(__file__).resolve().parents[2]
STATIC = Path(__file__).resolve().parent / "static"


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "controlplane-demo"
    messages: list[ChatMessage] = Field(default_factory=list)
    stream: bool = False
    # ControlPlane extensions (also accepted via headers)
    use_case: str | None = None
    mode: str | None = None  # shadow | enforce
    scenario: str | None = None  # refund | support | copilot | decision


class AuditVerifyRequest(BaseModel):
    content: str
    signature: str


class SessionStartRequest(BaseModel):
    session_id: str = Field(min_length=1)
    principal_id: str = "anonymous"


def audit_jsonl_bytes(found: dict[str, Any]) -> bytes:
    """Rebuild JSONL audit bytes from a public gate dict."""
    lines = [
        json.dumps(
            {
                "type": "request",
                "payload": {
                    "request_id": found["request_id"],
                    "use_case": found["use_case"],
                    "mode": found["mode"],
                    "policy_version": found["policy_version"],
                },
            }
        )
    ]
    for sp in found.get("spans") or []:
        lines.append(json.dumps({"type": "span", "payload": sp}))
    for c in found.get("claims") or []:
        lines.append(json.dumps({"type": "claim", "payload": c}))
    for d in (found.get("decisions") or {}).values():
        lines.append(json.dumps({"type": "decision", "payload": d}))
    lines.append(
        json.dumps({"type": "chain", "payload": {"valid": found.get("chain_valid")}})
    )
    return ("\n".join(lines) + "\n").encode("utf-8")


def create_app(
    *,
    gate: ControlPlaneGate | None = None,
    enable_upstream: bool = False,
    store: AuditStore | None = None,
    sessions: SessionStore | None = None,
) -> FastAPI:
    policies = PolicyRegistry()
    policies.load_dir(ROOT / "policies")
    metrics = MetricsStore()
    gate = gate or ControlPlaneGate(policies=policies, metrics=metrics)
    if store is None:
        try:
            store = AuditStore.from_env()
        except Exception:
            store = None
    if sessions is None:
        try:
            db_path = store.path if store is not None else os.environ.get("CONTROLPLANE_DB")
            sessions = SessionStore(path=db_path) if db_path else SessionStore()
        except Exception:
            sessions = SessionStore()
    limiter = RateLimiter()

    app = FastAPI(
        title="ControlPlane.ai",
        description=(
            "Admission-control layer for AI that acts. "
            "OpenAI-compatible reverse proxy + evidence ledger APIs."
        ),
        version="0.2.0",
    )
    app.state.gate = gate
    app.state.store = store
    app.state.sessions = sessions
    app.state.started_at = time.time()

    def _persist(public_dict: dict[str, Any]) -> None:
        if store is None:
            return
        try:
            store.save(public_dict)
        except Exception:
            return

    def _after_gate(public_dict: dict[str, Any]) -> None:
        _persist(public_dict)
        try:
            if webhook.should_notify(public_dict):
                webhook.notify_escalate(public_dict)
        except Exception:
            return

    def _session_summary(public_dict: dict[str, Any]) -> dict[str, Any]:
        overlay = public_dict.get("response_overlay") or {}
        actuators = overlay.get("actuators_applied") or overlay.get(
            "actuators_would_apply"
        ) or {}
        if not actuators:
            decisions = public_dict.get("decisions") or {}
            actuators = {
                k: (v.get("actuator") if isinstance(v, dict) else v)
                for k, v in decisions.items()
            }
        return {
            "request_id": public_dict.get("request_id"),
            "use_case": public_dict.get("use_case"),
            "mode": public_dict.get("mode"),
            "would_hold": public_dict.get("would_hold"),
            "enforced": public_dict.get("enforced"),
            "action_allowed": overlay.get("action_allowed"),
            "actuators": actuators,
            "holdback": overlay.get("holdback"),
        }

    def _attach_session(session_id: str | None, public_dict: dict[str, Any]) -> None:
        if not session_id:
            return
        try:
            principal = (public_dict.get("principal") or {}).get("id") or "anonymous"
            sessions.begin_session(session_id, str(principal))
            rid = public_dict.get("request_id")
            if not rid:
                return
            sessions.attach_request(session_id, str(rid), _session_summary(public_dict))
            public_dict["session_id"] = session_id
            public_dict["compounding_risk"] = sessions.compounding_risk(session_id)
        except Exception:
            return

    def _lookup(request_id: str) -> dict[str, Any] | None:
        if store is not None:
            try:
                found = store.get(request_id)
                if found is not None:
                    return found
            except Exception:
                pass
        return gate.get(request_id)

    def _list_requests(limit: int, offset: int) -> list[dict[str, Any]]:
        if store is not None:
            try:
                if store.count() > 0:
                    return store.list(limit=limit, offset=offset)
            except Exception:
                pass
        return gate.history(limit=limit)

    @app.middleware("http")
    async def enterprise_guards(request: Request, call_next):
        if not content_length_ok(request.headers, MAX_BODY_SIZE):
            return JSONResponse(
                {"detail": "payload too large"},
                status_code=413,
                headers=dict(SECURITY_HEADERS),
            )
        path = request.url.path
        if not api_key_authorized(request.headers, path, request.method):
            return JSONResponse(
                {"detail": "unauthorized"},
                status_code=401,
                headers=dict(SECURITY_HEADERS),
            )
        if path.startswith("/v1/"):
            ip = client_ip(
                request.headers,
                request.client.host if request.client else None,
            )
            if not limiter.allow(ip):
                return JSONResponse(
                    {"detail": "rate limit exceeded"},
                    status_code=429,
                    headers={**SECURITY_HEADERS, "Retry-After": "60"},
                )
        response = await call_next(request)
        for key, value in SECURITY_HEADERS.items():
            response.headers[key] = value
        return response

    def _page(name: str) -> HTMLResponse:
        path = STATIC / name
        if not path.exists():
            return HTMLResponse(f"<h1>Missing {name}</h1>", status_code=500)
        return HTMLResponse(path.read_text(encoding="utf-8"))

    @app.get("/", response_class=HTMLResponse)
    def console() -> HTMLResponse:
        return _page("index.html")

    @app.get("/policies", response_class=HTMLResponse)
    def page_policies() -> HTMLResponse:
        return _page("policies.html")

    @app.get("/metrics", response_class=HTMLResponse)
    def page_metrics() -> HTMLResponse:
        return _page("metrics.html")

    @app.get("/audit", response_class=HTMLResponse)
    def page_audit() -> HTMLResponse:
        return _page("audit.html")

    @app.get("/matrix", response_class=HTMLResponse)
    def page_matrix() -> HTMLResponse:
        return _page("matrix.html")

    @app.get("/architecture", response_class=HTMLResponse)
    def page_architecture() -> HTMLResponse:
        return _page("architecture.html")

    @app.get("/runbook", response_class=HTMLResponse)
    def page_runbook() -> HTMLResponse:
        return _page("runbook.html")

    @app.get("/print", response_class=HTMLResponse)
    def page_print() -> HTMLResponse:
        return _page("print.html")

    if STATIC.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")

    @app.get("/healthz")
    def healthz() -> dict[str, Any]:
        db_ok = False
        if store is not None:
            try:
                db_ok = store.ok()
            except Exception:
                db_ok = False
        return {
            "ok": True,
            "service": "controlplane",
            "uptime_s": round(time.time() - app.state.started_at, 1),
            "mode_default": "shadow_or_enforce_per_pack",
            "lane1": "deterministic_only",
            "db_ok": db_ok,
            "policies_count": len(gate.policies.list()),
        }

    @app.get("/v1/models")
    def list_models() -> dict[str, Any]:
        return {
            "object": "list",
            "data": [
                {
                    "id": "controlplane-demo",
                    "object": "model",
                    "owned_by": "controlplane",
                    "description": "Demo path — gates canned enterprise scenarios",
                }
            ],
        }

    @app.get("/v1/controlplane/policies")
    def list_policies() -> dict[str, Any]:
        return {"policies": gate.policies.as_public_dict()}

    @app.get("/v1/controlplane/metrics")
    def get_metrics() -> dict[str, Any]:
        return gate.metrics.snapshot()

    @app.post("/v1/controlplane/metrics/reset")
    def reset_metrics() -> dict[str, str]:
        gate.metrics.reset()
        return {"status": "reset"}

    @app.get("/prometheus", response_class=PlainTextResponse)
    def prometheus_metrics() -> PlainTextResponse:
        """Prometheus text exposition — separate from HTML GET /metrics."""
        return PlainTextResponse(
            gate.metrics.prometheus_text(),
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

    @app.get("/v1/controlplane/requests")
    def list_requests(limit: int = 50, offset: int = 0) -> dict[str, Any]:
        return {"requests": _list_requests(limit=limit, offset=offset)}

    @app.get("/v1/controlplane/requests/{request_id}")
    def get_request(request_id: str) -> dict[str, Any]:
        found = _lookup(request_id)
        if not found:
            raise HTTPException(status_code=404, detail="request not found")
        return found

    @app.get("/v1/controlplane/ledger/{request_id}/verify")
    def verify_ledger(request_id: str) -> dict[str, Any]:
        found = _lookup(request_id)
        if not found:
            raise HTTPException(status_code=404, detail="request not found")
        return {
            "request_id": request_id,
            "chain_valid": bool(found.get("chain_valid")),
        }

    @app.get("/v1/controlplane/requests/{request_id}/audit.jsonl")
    def audit_export(request_id: str) -> StreamingResponse:
        found = _lookup(request_id)
        if not found:
            raise HTTPException(status_code=404, detail="request not found")
        body = audit_jsonl_bytes(found)
        sig = signing.sign_bytes(body)

        def gen():
            yield body

        return StreamingResponse(
            gen(),
            media_type="application/x-ndjson",
            headers={
                "Content-Disposition": f'attachment; filename="{request_id}.audit.jsonl"',
                "X-ControlPlane-Signature": sig,
            },
        )

    @app.get("/v1/controlplane/requests/{request_id}/audit.jsonl.sig")
    def audit_signature(request_id: str) -> PlainTextResponse:
        found = _lookup(request_id)
        if not found:
            raise HTTPException(status_code=404, detail="request not found")
        sig = signing.sign_bytes(audit_jsonl_bytes(found))
        return PlainTextResponse(
            sig,
            headers={
                "X-ControlPlane-Signature": sig,
                "Content-Disposition": (
                    f'attachment; filename="{request_id}.audit.jsonl.sig"'
                ),
            },
        )

    @app.post("/v1/controlplane/audit/verify")
    def audit_verify(body: AuditVerifyRequest) -> dict[str, bool]:
        valid = signing.verify(body.content.encode("utf-8"), body.signature)
        return {"valid": valid}

    @app.post("/v1/controlplane/sessions")
    def start_session(body: SessionStartRequest) -> dict[str, Any]:
        return sessions.begin_session(body.session_id, body.principal_id)

    @app.get("/v1/controlplane/sessions/{session_id}")
    def get_session(session_id: str) -> dict[str, Any]:
        found = sessions.get(session_id)
        if not found:
            raise HTTPException(status_code=404, detail="session not found")
        return found

    @app.post("/v1/controlplane/demo/{scenario}")
    def run_demo(
        scenario: str,
        mode: str | None = None,
        session_id: str | None = None,
        principal: str | None = None,
    ) -> dict[str, Any]:
        result = _run_scenario(gate, scenario, mode_override=mode, principal_id=principal)
        pub = result.public_dict()
        _after_gate(pub)
        _attach_session(session_id, pub)
        return pub

    @app.post("/v1/chat/completions")
    async def chat_completions(
        body: ChatCompletionRequest,
        request: Request,
        x_controlplane_use_case: str | None = Header(default=None),
        x_controlplane_mode: str | None = Header(default=None),
        x_controlplane_scenario: str | None = Header(default=None),
    ) -> JSONResponse:
        """OpenAI-compatible entrypoint.

        Demo path: maps user text / scenario hint onto frozen enterprise fixtures
        and returns a gated completion plus `controlplane` extension object.
        If no scenario is resolved and CONTROLPLANE_UPSTREAM_URL is set, the
        request is forwarded as-is. Upstream replies are not given fake
        Edit/Escalate actuators — Lane-1 fixtures were not used.
        """
        use_case = body.use_case or x_controlplane_use_case
        mode = body.mode or x_controlplane_mode
        scenario = body.scenario or x_controlplane_scenario or _infer_scenario(body.messages)

        if scenario:
            result = _run_scenario(gate, scenario, mode_override=mode)
            pub = result.public_dict()
            _after_gate(pub)
            content = pub["response_overlay"].get("user_visible_text") or (
                body.messages[-1].content if body.messages else ""
            )
            if not pub["response_overlay"].get("action_allowed", True):
                hold = pub["response_overlay"].get("hold_reason") or {}
                content = (
                    f"{content}\n\n"
                    f"[ControlPlane HOLD] {hold.get('actuator')} — {hold.get('matrix')}. "
                    "Irreversible action not released. Evidence packet attached."
                )
            completion = {
                "id": f"chatcmpl-{pub['request_id']}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": body.model,
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": content},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                "controlplane": pub,
            }
            return JSONResponse(completion)

        if enable_upstream or upstream.configured():
            try:
                forwarded = upstream.forward_chat(
                    [{"role": m.role, "content": m.content} for m in body.messages],
                    body.model,
                )
            except upstream.UpstreamNotConfigured as exc:
                raise HTTPException(status_code=501, detail=str(exc)) from exc
            except upstream.UpstreamError as exc:
                raise HTTPException(status_code=502, detail=str(exc)) from exc
            completion = dict(forwarded)
            completion["controlplane"] = {
                "upstream": True,
                "demo_fixtures_used": False,
                "note": (
                    "Upstream passthrough. Lane-1 demo fixtures were not used. "
                    "Edit/Escalate/Block are not applied without provenance."
                ),
            }
            return JSONResponse(completion)

        raise HTTPException(
            status_code=400,
            detail=(
                "No scenario resolved. Pass scenario=refund|support|copilot|decision "
                "or include those keywords in the user message. "
                "This keeps the Lane-1 demo deterministic for judges. "
                "Set CONTROLPLANE_UPSTREAM_URL for honest OpenAI-compatible passthrough."
            ),
        )

    return app


def _infer_scenario(messages: list[ChatMessage]) -> str | None:
    text = " ".join(m.content for m in messages).lower()
    if "refund" in text or "clause 7.2" in text or "7.2" in text:
        return "refund"
    if "partner" in text or "sla" in text or "copilot" in text:
        return "copilot"
    if "support" in text or "chatbot" in text:
        return "support"
    if "decision" in text:
        return "decision"
    return None


def _run_scenario(
    gate: ControlPlaneGate,
    scenario: str,
    mode_override: str | None,
    principal_id: str | None = None,
):
    scenario = scenario.lower().strip()
    if scenario in {"refund", "decision-support", "decision"}:
        return gate.run_refund_demo(mode_override=mode_override or "enforce")
    if scenario == "flip":
        return gate.run_flip_demo(
            principal_id=principal_id or "analyst_01",
            mode_override=mode_override or "enforce",
        )
    if scenario in {"support", "customer-support"}:
        return _wrap_multi(gate, "customer-support", run_customer_support, mode_override)
    if scenario in {"copilot", "internal-copilot"}:
        return _wrap_multi(gate, "internal-copilot", run_knowledge_copilot, mode_override)
    raise HTTPException(status_code=400, detail=f"unknown scenario: {scenario}")


def _wrap_multi(gate, use_case, runner, mode_override):
    """Run existing multi-usecase ledger through metrics without double-decide."""
    # For support/copilot the scenario modules already decide. Prefer gate path:
    # call runner for structure then use gate.run_refund style — simpler: execute
    # runner and synthesize GateResult-like public dict via a dedicated helper.
    from controlplane.pipeline import GateResult
    from controlplane.entitlement import audit_claim
    import time as _time

    t0 = _time.perf_counter()
    led = runner()
    pack = gate.policies.get(use_case)
    mode = mode_override or pack.mode
    findings = {cid: audit_claim(led, cid) for cid in led.claims}
    decisions = dict(led.decisions)
    from controlplane.shadow import HOLDING_ACTUATORS

    would_hold = any(d.actuator in HOLDING_ACTUATORS for d in decisions.values())
    for d in decisions.values():
        gate.metrics.record(use_case=use_case, actuator=d.actuator, mode=mode)
    visible = f"[{use_case}] gated response"
    overlay = {
        "shadow": mode == "shadow",
        "actuators_applied": {k: v.actuator.value for k, v in decisions.items()},
        "user_visible_text": visible,
        "action_allowed": not would_hold or mode == "shadow",
        "note": f"Scenario={use_case} mode={mode}",
        "holdback": admit_for_decisions(visible, decisions),
    }
    result = GateResult(
        request_id=led.request_id,
        use_case=use_case,
        mode=mode,
        policy_version=pack.policy_version,
        ledger=led,
        findings=findings,
        decisions=decisions,
        latency_ms=(_time.perf_counter() - t0) * 1000.0,
        enforced=mode == "enforce" and would_hold,
        would_hold=would_hold,
        response_overlay=overlay,
    )
    gate._history.append(result)
    return result


def main() -> None:
    import uvicorn

    uvicorn.run(
        "controlplane.server.app:create_app",
        factory=True,
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "8080")),
        reload=False,
    )


if __name__ == "__main__":
    main()
