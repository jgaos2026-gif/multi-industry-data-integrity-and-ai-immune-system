from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import json
from uuid import uuid4

from ..crypto.hashing import sha256_hex
from ..models import MemoryRecord, TrustState


class MemoryBraid:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def write(self, sovereign: str, content: dict, provenance: str) -> MemoryRecord:
        ns = self.root / sovereign
        ns.mkdir(parents=True, exist_ok=True)
        digest = sha256_hex(json.dumps(content, sort_keys=True).encode())
        record = MemoryRecord(
            memory_id=str(uuid4()),
            owner_sovereign=sovereign,
            created_at=datetime.now(UTC).isoformat(),
            version=1,
            content_digest=digest,
            provenance=provenance,
            trust_status=TrustState.STAGED,
            evidence_refs=(),
        )
        (ns / f"{record.memory_id}.json").write_text(json.dumps({**record.__dict__, "trust_status": record.trust_status.value}, sort_keys=True), encoding="utf-8")
        return record
