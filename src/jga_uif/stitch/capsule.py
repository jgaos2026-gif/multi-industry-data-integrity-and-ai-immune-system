from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
import json
from uuid import uuid4

from ..constants import DEFAULT_POLICY_VERSION, DEFAULT_SCHEMA_VERSION, SUPPORTED_RELAYS
from ..crypto.hashing import sha256_hex, sha3_256_hex
from ..exceptions import VerificationError
from ..models import IntegrityCapsule


def create_capsule(payload: bytes, transaction_id: str, source_sovereign: str, destination_sovereign: str, relay: str, nonce: str, sequence: int, metadata: dict | None = None) -> IntegrityCapsule:
    if relay not in SUPPORTED_RELAYS:
        raise VerificationError("unsupported relay")
    created_at = datetime.now(UTC).isoformat()
    capsule = IntegrityCapsule(
        capsule_id=str(uuid4()),
        transaction_id=transaction_id,
        source_sovereign=source_sovereign,
        destination_sovereign=destination_sovereign,
        relay=relay,
        payload_sha256=sha256_hex(payload),
        payload_sha3_256=sha3_256_hex(payload),
        payload_size=len(payload),
        created_at=created_at,
        nonce=nonce,
        sequence=sequence,
        schema_version=DEFAULT_SCHEMA_VERSION,
        policy_version=DEFAULT_POLICY_VERSION,
        metadata=metadata or {},
    )
    manifest_digest = sha256_hex(json.dumps(asdict(capsule), sort_keys=True).encode())
    return IntegrityCapsule(**asdict(capsule), manifest_digest=manifest_digest)
