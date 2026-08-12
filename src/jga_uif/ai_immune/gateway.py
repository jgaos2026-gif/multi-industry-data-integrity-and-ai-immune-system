from __future__ import annotations

from .memory_guard import MemoryGuard
from .output_guard import OutputGuard
from .tool_guard import ToolGuard


class AIImmuneGateway:
    def __init__(self, tool_guard: ToolGuard, memory_guard: MemoryGuard, output_guard: OutputGuard) -> None:
        self.tool_guard = tool_guard
        self.memory_guard = memory_guard
        self.output_guard = output_guard

    def evaluate(self, tool_action: str, memory_actor: str, memory_owner: str, output: dict) -> str:
        self.tool_guard.authorize(tool_action)
        if not self.memory_guard.authorize_write(memory_actor, memory_owner):
            return "DENY"
        if not self.output_guard.verify_claims(output):
            return "QUARANTINE"
        return "ALLOW"
