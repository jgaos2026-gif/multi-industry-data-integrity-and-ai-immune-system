from __future__ import annotations

from .certification import certify
from .content import verify_content
from .provenance import verify_provenance
from .structure import verify_structure


class TripleVerificationEngine:
    def __init__(self, allowed_sources: set[str] | None = None) -> None:
        self.allowed_sources = allowed_sources or {"local"}
        self.nonce_cache: set[str] = set()

    def run(self, payload: bytes, metadata: dict, expected_sha256: str | None = None, expected_sha3_256: str | None = None, policy_version: str = "1.0.0"):
        evidence = [
            verify_content(payload, expected_sha256, expected_sha3_256),
            verify_structure(metadata),
            verify_provenance(metadata, self.nonce_cache, self.allowed_sources),
        ]
        decision = certify(metadata["transaction_id"], evidence, policy_version, ("content", "structure", "provenance"))
        return evidence, decision
