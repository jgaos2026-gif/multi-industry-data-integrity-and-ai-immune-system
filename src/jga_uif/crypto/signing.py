from dataclasses import dataclass


@dataclass(frozen=True)
class SignatureMetadata:
    algorithm: str
    key_id: str
    signature: str
