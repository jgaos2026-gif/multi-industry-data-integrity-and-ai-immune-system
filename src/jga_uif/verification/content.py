from __future__ import annotations

from ..crypto.hashing import sha256_hex, sha3_256_hex
from ..models import VerificationEvidence


def verify_content(payload: bytes, expected_sha256: str | None = None, expected_sha3_256: str | None = None) -> VerificationEvidence:
    actual_sha256 = sha256_hex(payload)
    actual_sha3 = sha3_256_hex(payload)
    if expected_sha256 and expected_sha256 != actual_sha256:
        return VerificationEvidence("content", False, "sha256 mismatch", actual_sha256)
    if expected_sha3_256 and expected_sha3_256 != actual_sha3:
        return VerificationEvidence("content", False, "sha3_256 mismatch", actual_sha3)
    return VerificationEvidence("content", True, "content verified", actual_sha256, {"sha3_256": actual_sha3, "size": len(payload)})
