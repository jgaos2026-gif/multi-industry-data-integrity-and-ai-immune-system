from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
import shutil
from uuid import uuid4

from ..crypto.hashing import sha256_hex


class CheckpointManager:
    def __init__(self, checkpoints_root: Path) -> None:
        self.root = checkpoints_root
        self.root.mkdir(parents=True, exist_ok=True)

    def create(self, source_dir: Path, generation: int, policy_version: str, ledger_position: int) -> Path:
        checkpoint_id = str(uuid4())
        target = self.root / checkpoint_id
        target.mkdir(parents=True)
        staged = target / "state"
        shutil.copytree(source_dir, staged)
        manifest: dict[str, str] = {}
        for file in staged.rglob("*"):
            if file.is_file():
                manifest[str(file.relative_to(staged))] = sha256_hex(file.read_bytes())
        payload = {
            "checkpoint_id": checkpoint_id,
            "created_at": datetime.now(UTC).isoformat(),
            "generation": generation,
            "source_state_digest": sha256_hex(json.dumps(manifest, sort_keys=True).encode()),
            "files_manifest": manifest,
            "ledger_position": ledger_position,
            "policy_version": policy_version,
        }
        payload["checkpoint_digest"] = sha256_hex(json.dumps(payload, sort_keys=True).encode())
        (target / "checkpoint.json").write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")
        return target
