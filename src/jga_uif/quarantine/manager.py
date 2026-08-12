from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import json
import shutil

from ..crypto.hashing import sha256_hex


class QuarantineManager:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def place(self, source: Path, reason: str, transaction_id: str) -> Path:
        target = self.root / transaction_id
        target.mkdir(parents=True, exist_ok=True)
        preserved = target / source.name
        shutil.copy2(source, preserved)
        metadata = {
            "reason": reason,
            "transaction_id": transaction_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "digest": sha256_hex(preserved.read_bytes()),
        }
        (target / "metadata.json").write_text(json.dumps(metadata, sort_keys=True), encoding="utf-8")
        return target
