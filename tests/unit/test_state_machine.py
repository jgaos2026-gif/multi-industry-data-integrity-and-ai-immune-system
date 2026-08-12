import pytest

from jga_uif.exceptions import TransitionError
from jga_uif.models import TrustState
from jga_uif.state_machine import can_transition, require_transition


def test_valid_state_flow():
    assert can_transition(TrustState.UNKNOWN, TrustState.STAGED)
    assert can_transition(TrustState.STAGED, TrustState.VERIFYING)
    assert can_transition(TrustState.VERIFYING, TrustState.VERIFIED)
    assert can_transition(TrustState.VERIFIED, TrustState.CERTIFIED)
    assert can_transition(TrustState.CERTIFIED, TrustState.TRUSTED)


def test_no_quarantine_direct_to_trusted():
    assert not can_transition(TrustState.QUARANTINED, TrustState.TRUSTED)
    with pytest.raises(TransitionError):
        require_transition(TrustState.QUARANTINED, TrustState.TRUSTED)
