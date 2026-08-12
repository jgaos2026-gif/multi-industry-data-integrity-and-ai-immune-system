from __future__ import annotations

from ..models import CertificationDecision, VerificationEvidence


def certify(transaction_id: str, evidences: list[VerificationEvidence], policy_version: str, required: tuple[str, ...]) -> CertificationDecision:
    by_name = {ev.verifier: ev for ev in evidences}
    for verifier in required:
        ev = by_name.get(verifier)
        if not ev or not ev.passed:
            return CertificationDecision(transaction_id, False, f"{verifier} failed or missing", policy_version, required)
    return CertificationDecision(transaction_id, True, "certified", policy_version, required)
