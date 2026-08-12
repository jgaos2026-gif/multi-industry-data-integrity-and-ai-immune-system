class OutputGuard:
    def verify_claims(self, output: dict) -> bool:
        return output.get("verified") is not True
