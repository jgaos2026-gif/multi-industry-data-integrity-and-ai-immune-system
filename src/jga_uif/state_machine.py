from __future__ import annotations

from .exceptions import TransitionError
from .models import TrustState

_ALLOWED_TRANSITIONS: dict[TrustState, set[TrustState]] = {
    TrustState.UNKNOWN: {TrustState.STAGED},
    TrustState.STAGED: {TrustState.VERIFYING, TrustState.QUARANTINED},
    TrustState.VERIFYING: {TrustState.VERIFIED, TrustState.QUARANTINED},
    TrustState.VERIFIED: {TrustState.CERTIFIED, TrustState.QUARANTINED},
    TrustState.CERTIFIED: {TrustState.TRUSTED, TrustState.REVOKED},
    TrustState.TRUSTED: {TrustState.REVOKED, TrustState.QUARANTINED},
    TrustState.QUARANTINED: {TrustState.RECOVERING},
    TrustState.RECOVERING: {TrustState.STAGED, TrustState.FAILED},
    TrustState.REVOKED: {TrustState.QUARANTINED},
    TrustState.FAILED: {TrustState.QUARANTINED},
}


def can_transition(current: TrustState, nxt: TrustState) -> bool:
    return nxt in _ALLOWED_TRANSITIONS.get(current, set())


def require_transition(current: TrustState, nxt: TrustState) -> None:
    if not can_transition(current, nxt):
        raise TransitionError(f"invalid transition: {current.value} -> {nxt.value}")
