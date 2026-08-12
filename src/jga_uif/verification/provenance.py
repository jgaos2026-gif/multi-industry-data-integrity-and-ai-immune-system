from __future__ import annotations

from ..models import VerificationEvidence


def verify_provenance(metadata: dict, nonce_cache: set[str], allowed_sources: set[str]) -> VerificationEvidence:
    source = metadata.get("source")
    nonce = metadata.get("nonce")
    if source not in allowed_sources:
        return VerificationEvidence("provenance", False, "unapproved source")
    if not isinstance(nonce, str) or len(nonce) < 8:
        return VerificationEvidence("provenance", False, "invalid nonce")
    if nonce in nonce_cache:
        return VerificationEvidence("provenance", False, "replay nonce")
    nonce_cache.add(nonce)
    return VerificationEvidence("provenance", True, "provenance verified")
