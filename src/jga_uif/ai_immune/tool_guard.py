from __future__ import annotations

from ..policy.omega import OmegaPolicyEngine


class ToolGuard:
    def __init__(self, policy: OmegaPolicyEngine) -> None:
        self.policy = policy

    def authorize(self, action: str) -> bool:
        self.policy.require_tool_allowed(action)
        return True
