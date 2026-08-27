"""Versioned policy packs — governance without redrawing the matrix."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from controlplane.models import BlastTier

_DEFAULT_PACKS: dict[str, dict[str, Any]] = {
    "customer-support": {
        "policy_version": "pack-support-v1",
        "use_case": "customer-support",
        "description": "Customer-facing chatbot — user-visible text, low irreversibility",
        "default_tier": "R1",
        "mode": "enforce",  # shadow | enforce
        "latency_budget_ms_p50": 40,
        "latency_budget_ms_p95": 200,
        "fail_stance": "open_annotate",
        "actions": {
            "show_reply": {"tier": "R1", "irreversibility": False},
        },
    },
    "internal-copilot": {
        "policy_version": "pack-copilot-v1",
        "use_case": "internal-copilot",
        "description": "Internal knowledge assistant — external send is R2",
        "default_tier": "R1",
        "mode": "enforce",
        "latency_budget_ms_p50": 40,
        "latency_budget_ms_p95": 200,
        "fail_stance": "open_annotate",
        "actions": {
            "draft_partner_email": {"tier": "R2", "irreversibility": False},
            "show_draft": {"tier": "R1", "irreversibility": False},
        },
    },
    "decision-support": {
        "policy_version": "pack-decision-v1",
        "use_case": "decision-support",
        "description": "Regulated / irreversible actions — payments, deletions",
        "default_tier": "R3",
        "mode": "enforce",
        "latency_budget_ms_p50": 40,
        "latency_budget_ms_p95": 200,
        "fail_stance": "closed_escalate",
        "actions": {
            "show_text": {"tier": "R1", "irreversibility": False},
            "issue_refund": {"tier": "R3", "irreversibility": True},
        },
    },
    "flip": {
        "policy_version": "pack-flip-v1",
        "use_case": "flip",
        "description": "Principal-flip demo — same HR-COMP-L6 span, same claim, caller decides actuator",
        "default_tier": "R1",
        "mode": "enforce",
        "latency_budget_ms_p50": 40,
        "latency_budget_ms_p95": 200,
        "fail_stance": "closed_escalate",
        "actions": {
            "show_text": {"tier": "R1", "irreversibility": False},
        },
    },
}


@dataclass(frozen=True)
class ActionPolicy:
    name: str
    tier: BlastTier
    irreversibility: bool


@dataclass(frozen=True)
class PolicyPack:
    use_case: str
    policy_version: str
    description: str
    default_tier: BlastTier
    mode: str  # shadow | enforce
    latency_budget_ms_p50: int
    latency_budget_ms_p95: int
    fail_stance: str
    actions: dict[str, ActionPolicy]

    def action(self, name: str) -> ActionPolicy:
        if name in self.actions:
            return self.actions[name]
        return ActionPolicy(name=name, tier=self.default_tier, irreversibility=False)


def _parse_pack(raw: dict[str, Any]) -> PolicyPack:
    actions = {
        key: ActionPolicy(
            name=key,
            tier=BlastTier(cfg["tier"]),
            irreversibility=bool(cfg.get("irreversibility", False)),
        )
        for key, cfg in (raw.get("actions") or {}).items()
    }
    return PolicyPack(
        use_case=raw["use_case"],
        policy_version=raw["policy_version"],
        description=raw.get("description", ""),
        default_tier=BlastTier(raw.get("default_tier", "R1")),
        mode=raw.get("mode", "shadow"),
        latency_budget_ms_p50=int(raw.get("latency_budget_ms_p50", 40)),
        latency_budget_ms_p95=int(raw.get("latency_budget_ms_p95", 200)),
        fail_stance=raw.get("fail_stance", "open_annotate"),
        actions=actions,
    )


class PolicyRegistry:
    def __init__(self) -> None:
        self._packs: dict[str, PolicyPack] = {
            name: _parse_pack(raw) for name, raw in _DEFAULT_PACKS.items()
        }

    def load_dir(self, path: str | Path) -> None:
        root = Path(path)
        if not root.exists():
            return
        for file in sorted(root.glob("*.yaml")) + sorted(root.glob("*.yml")):
            raw = yaml.safe_load(file.read_text(encoding="utf-8"))
            if not raw:
                continue
            pack = _parse_pack(raw)
            self._packs[pack.use_case] = pack

    def get(self, use_case: str) -> PolicyPack:
        if use_case not in self._packs:
            raise KeyError(f"unknown policy pack: {use_case}")
        return self._packs[use_case]

    def list(self) -> list[PolicyPack]:
        return list(self._packs.values())

    def as_public_dict(self) -> list[dict[str, Any]]:
        out = []
        for pack in self._packs.values():
            out.append(
                {
                    "use_case": pack.use_case,
                    "policy_version": pack.policy_version,
                    "description": pack.description,
                    "default_tier": pack.default_tier.value,
                    "mode": pack.mode,
                    "latency_budget_ms_p50": pack.latency_budget_ms_p50,
                    "latency_budget_ms_p95": pack.latency_budget_ms_p95,
                    "fail_stance": pack.fail_stance,
                    "actions": {
                        name: {
                            "tier": ap.tier.value,
                            "irreversibility": ap.irreversibility,
                        }
                        for name, ap in pack.actions.items()
                    },
                }
            )
        return out


def write_default_packs(path: str | Path) -> None:
    root = Path(path)
    root.mkdir(parents=True, exist_ok=True)
    for name, raw in _DEFAULT_PACKS.items():
        (root / f"{name}.yaml").write_text(
            yaml.safe_dump(raw, sort_keys=False),
            encoding="utf-8",
        )
