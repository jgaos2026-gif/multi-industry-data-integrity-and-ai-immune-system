from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from ..constants import DEFAULT_MAX_INGRESS_BYTES
from ..exceptions import VerificationError
from ..models import TrustState
from .validation import validate_safe_relative_path


@dataclass(frozen=True)
class IngressSubmission:
    transaction_id: str
    payload: bytes
    metadata: dict
    state: TrustState


class IngressGate:
    def __init__(self, max_bytes: int = DEFAULT_MAX_INGRESS_BYTES) -> None:
        self.max_bytes = max_bytes

    def receive(self, payload: bytes, metadata: dict) -> IngressSubmission:
        if len(payload) > self.max_bytes:
            raise VerificationError("oversized input rejected")
        path = metadata.get("path")
        if path and not validate_safe_relative_path(path):
            raise VerificationError("unsafe path")
        return IngressSubmission(str(uuid4()), payload, metadata, TrustState.STAGED)
