from __future__ import annotations

import json
from pathlib import Path

from ..exceptions import PolicyError


class OmegaPolicyEngine:
    def __init__(self, policy_path: Path) -> None:
        self.policy_path = policy_path
        self.policy = json.loads(policy_path.read_text(encoding="utf-8"))

    def require_tool_allowed(self, action: str) -> None:
        allowed = set(self.policy.get("allowed_tool_actions", []))
        if action not in allowed:
            raise PolicyError(f"tool action denied: {action}")

    @property
    def version(self) -> str:
        return self.policy.get("version", "0")
