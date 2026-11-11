class OutputGuard:
    """An output never certifies itself.

    The gate allows an output only when an independent verifier
    attests to it: ``verified`` True AND ``verified_by`` naming that
    verifier (a non-empty string). A self-asserted ``verified`` flag
    alone is quarantined, and so is any output with no attestation —
    the gate fails closed (quarantine by default).

    Attestation identity authentication — proving the named verifier
    really performed the check — is a separate open item, not
    claimed here. This guard enforces that an attestation is
    present; it does not authenticate who made it.
    """

    def verify_claims(self, output: dict) -> bool:
        if output.get("verified") is not True:
            return False
        attestation = output.get("verified_by")
        return isinstance(attestation, str) and bool(attestation.strip())
