from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

from ..crypto.hashing import sha256_hex


def write_anchor(ledger_path: Path, anchor_path: Path, generation: int) -> dict:
    content = ledger_path.read_bytes()
    line_count = len([ln for ln in content.splitlines() if ln.strip()])
    digest = sha256_hex(content)
    head_hash = "GENESIS"
    if line_count:
        last = json.loads(content.splitlines()[-1])
        head_hash = last["record_hash"]
    anchor = {
        "record_count": line_count,
        "head_record_hash": head_hash,
        "ledger_digest": digest,
        "generation": generation,
        "timestamp": datetime.now(UTC).isoformat(),
    }
    anchor_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = anchor_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(anchor, sort_keys=True), encoding="utf-8")
    tmp.replace(anchor_path)
    return anchor
