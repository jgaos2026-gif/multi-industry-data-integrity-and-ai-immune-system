from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class TrustState(str, Enum):
    UNKNOWN = "UNKNOWN"
    STAGED = "STAGED"
    VERIFYING = "VERIFYING"
    VERIFIED = "VERIFIED"
    CERTIFIED = "CERTIFIED"
    TRUSTED = "TRUSTED"
    QUARANTINED = "QUARANTINED"
    RECOVERING = "RECOVERING"
    REVOKED = "REVOKED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class VerificationEvidence:
    verifier: str
    passed: bool
    reason: str
    digest: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CertificationDecision:
    transaction_id: str
    approved: bool
    reason: str
    policy_version: str
    required_verifiers: tuple[str, ...]
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(frozen=True)
class IntegrityCapsule:
    capsule_id: str
    transaction_id: str
    source_sovereign: str
    destination_sovereign: str
    relay: str
    payload_sha256: str
    payload_sha3_256: str
    payload_size: int
    created_at: str
    nonce: str
    sequence: int
    schema_version: str
    policy_version: str
    metadata: dict[str, Any] = field(default_factory=dict)
    expires_at: str | None = None
    manifest_digest: str | None = None


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    owner_sovereign: str
    created_at: str
    version: int
    content_digest: str
    provenance: str
    trust_status: TrustState
    evidence_refs: tuple[str, ...] = ()
