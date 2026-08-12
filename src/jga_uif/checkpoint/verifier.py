from __future__ import annotations

import json
from pathlib import Path

from ..crypto.hashing import sha256_hex


def verify_checkpoint(checkpoint_dir: Path) -> tuple[bool, str]:
    data = json.loads((checkpoint_dir / "checkpoint.json").read_text(encoding="utf-8"))
    manifest = data.get("files_manifest", {})
    state_dir = checkpoint_dir / "state"
    for rel, expected in manifest.items():
        file = state_dir / rel
        if not file.exists():
            return False, f"missing file: {rel}"
        if sha256_hex(file.read_bytes()) != expected:
            return False, f"digest mismatch: {rel}"
    payload = {k: v for k, v in data.items() if k != "checkpoint_digest"}
    actual = sha256_hex(json.dumps(payload, sort_keys=True).encode())
    if actual != data.get("checkpoint_digest"):
        return False, "checkpoint metadata mismatch"
    return True, "ok"
