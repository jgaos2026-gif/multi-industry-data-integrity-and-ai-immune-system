from __future__ import annotations

from dataclasses import asdict

from ..exceptions import VerificationError
from ..models import IntegrityCapsule
from ..verification.triple_verify import TripleVerificationEngine


class StitchGate:
    def __init__(self, verifier: TripleVerificationEngine) -> None:
        self.verifier = verifier

    def verify_capsule(self, capsule: IntegrityCapsule, payload: bytes):
        metadata = {
            "transaction_id": capsule.transaction_id,
            "sequence": capsule.sequence,
            "source": capsule.relay,
            "nonce": capsule.nonce,
            "capsule_id": capsule.capsule_id,
        }
        evidence, decision = self.verifier.run(payload, metadata, capsule.payload_sha256, capsule.payload_sha3_256, capsule.policy_version)
        if not decision.approved:
            raise VerificationError(decision.reason)
        return asdict(capsule), evidence, decision
