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


def _gateway(tmp_path):
    policy = tmp_path / "policy.json"
    policy.write_text('{"version":"1","allowed_tool_actions":["read"]}')
    return AIImmuneGateway(ToolGuard(OmegaPolicyEngine(policy)), MemoryGuard(), OutputGuard())


def test_unverified_output_quarantined(tmp_path):
    # The hole the fix closes: an output that was never verified
    # used to sail through as ALLOW.
    gateway = _gateway(tmp_path)
    assert gateway.evaluate("read", "sovereign_a", "sovereign_a", {"verified": False}) == "QUARANTINE"
    assert gateway.evaluate("read", "sovereign_a", "sovereign_a", {}) == "QUARANTINE"


def test_independently_verified_output_allowed(tmp_path):
    gateway = _gateway(tmp_path)
    result = gateway.evaluate("read", "sovereign_a", "sovereign_a",
                              {"verified": True, "verified_by": "triad-verifier"})
    assert result == "ALLOW"


def test_empty_attestation_quarantined(tmp_path):
    gateway = _gateway(tmp_path)
    result = gateway.evaluate("read", "sovereign_a", "sovereign_a",
                              {"verified": True, "verified_by": "   "})
    assert result == "QUARANTINE"
    result = gateway.evaluate("read", "sovereign_a", "sovereign_a",
                              {"verified": True, "verified_by": None})
    assert result == "QUARANTINE"
