import pytest

from jga_uif.ai_immune.gateway import AIImmuneGateway
from jga_uif.ai_immune.memory_guard import MemoryGuard
from jga_uif.ai_immune.output_guard import OutputGuard
from jga_uif.ai_immune.tool_guard import ToolGuard
from jga_uif.exceptions import PolicyError
from jga_uif.policy.omega import OmegaPolicyEngine


def test_unauthorized_tool_action_denied(tmp_path):
    policy = tmp_path / "policy.json"
    policy.write_text('{"version":"1","allowed_tool_actions":["read"]}')
    engine = OmegaPolicyEngine(policy)
    with pytest.raises(PolicyError):
        ToolGuard(engine).authorize("shell")


def test_output_cannot_self_certify(tmp_path):
    policy = tmp_path / "policy.json"
    policy.write_text('{"version":"1","allowed_tool_actions":["read"]}')
    gateway = AIImmuneGateway(ToolGuard(OmegaPolicyEngine(policy)), MemoryGuard(), OutputGuard())
    result = gateway.evaluate("read", "sovereign_a", "sovereign_a", {"verified": True})
    assert result == "QUARANTINE"
