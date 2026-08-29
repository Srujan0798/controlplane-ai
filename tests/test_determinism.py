"""T8.2 — determinism (cross-process ledger hash stability).

Acceptance: the same input yields a BYTE-IDENTICAL ledger hash across runs and
across processes. We run the refund demo (and an eval case) in separate Python
processes and compare `EvidenceLedger.chain_hash()`, which excludes the
per-run request_id so the decision logic — not the id — is what is reproducible.
"""
from __future__ import annotations

import subprocess
import sys

import pytest

_DRIVER = '''
import json
from controlplane.pipeline import ControlPlaneGate
from controlplane.policy import PolicyRegistry

g = ControlPlaneGate(policies=PolicyRegistry())
r = g.run_refund_demo(mode_override="enforce")
print(r.ledger.chain_hash())
'''


def _run_once() -> str:
    out = subprocess.run(
        [sys.executable, "-c", _DRIVER],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0, out.stderr
    return out.stdout.strip().splitlines()[-1]


def test_refund_demo_chain_hash_stable_across_processes():
    a = _run_once()
    b = _run_once()
    assert a == b, f"ledger hash drift across processes: {a} != {b}"


_DRIVER_CASE = '''
import json, glob, yaml
from controlplane.extract import extract_claims
from controlplane.models import Action, BlastTier, Principal
from controlplane.recorder import ProvenanceRecorder
from controlplane.binder import bind_claims
from controlplane.entitlement import audit_claim
from controlplane.interlock import decide

path = sorted(glob.glob("evals/cases/*.yaml"))[0]
data = yaml.safe_load(open(path)) or []
case = data[0] if isinstance(data, list) else data
led = ProvenanceRecorder().begin_request(case["id"], Principal(id="x", clearance=frozenset()), "eval")
actions = [Action(a["action_id"], a.get("name", a["action_id"]), BlastTier[a["tier"]],
                 args=dict(a.get("args") or {}), irreversibility=bool(a.get("irreversibility")))
          for a in case.get("actions") or []]
claims = extract_claims(case["response_text"], actions=actions)
bind_claims(led, claims)
findings = {cid: audit_claim(led, cid) for cid in led.claims}
for a in actions:
    decide(led, a, findings=findings)
print(led.chain_hash())
'''


def _run_case_once() -> str:
    out = subprocess.run(
        [sys.executable, "-c", _DRIVER_CASE],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0, out.stderr
    return out.stdout.strip().splitlines()[-1]


def test_eval_case_chain_hash_stable_across_processes():
    a = _run_case_once()
    b = _run_case_once()
    assert a == b, f"eval-case ledger hash drift: {a} != {b}"
