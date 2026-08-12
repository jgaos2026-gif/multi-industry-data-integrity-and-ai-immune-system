from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tempfile

from ..models import TrustState


@dataclass(frozen=True)
class StagedObject:
    transaction_id: str
    path: Path
    size: int
    state: TrustState = TrustState.STAGED


class StagingStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def stage(self, transaction_id: str, payload: bytes) -> StagedObject:
        with tempfile.NamedTemporaryFile(dir=self.root, delete=False) as tmp:
            tmp.write(payload)
            tmp.flush()
            path = Path(tmp.name)
        return StagedObject(transaction_id=transaction_id, path=path, size=len(payload))
