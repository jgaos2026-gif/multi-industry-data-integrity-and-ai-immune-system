class VerifierNode:
    def verify(self, candidate: dict) -> bool:
        return "digest" in candidate
