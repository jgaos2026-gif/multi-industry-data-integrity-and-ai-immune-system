from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from uuid import uuid4

from ..crypto.hashing import sha256_hex


class EvidenceStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def write(self, transaction_id: str, kind: str, payload: dict) -> Path:
        evidence_id = str(uuid4())
        path = self.root / f"{evidence_id}.json"
        record = {
            "evidence_id": evidence_id,
            "transaction_id": transaction_id,
            "created_at": datetime.now(UTC).isoformat(),
            "kind": kind,
            "digest": sha256_hex(json.dumps(payload, sort_keys=True).encode()),
            "metadata": payload,
        }
        path.write_text(json.dumps(record, sort_keys=True, indent=2), encoding="utf-8")
        return path
