from __future__ import annotations

from ..models import VerificationEvidence


def verify_structure(metadata: dict, required_fields: tuple[str, ...] = ("transaction_id", "sequence")) -> VerificationEvidence:
    missing = [field for field in required_fields if field not in metadata]
    if missing:
        return VerificationEvidence("structure", False, f"missing fields: {missing}")
    seq = metadata.get("sequence")
    if not isinstance(seq, int) or seq < 0:
        return VerificationEvidence("structure", False, "invalid sequence")
    return VerificationEvidence("structure", True, "structure verified")
