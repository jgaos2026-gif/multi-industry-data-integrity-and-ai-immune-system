from __future__ import annotations

from pathlib import Path
import shutil

from ..checkpoint.verifier import verify_checkpoint
from ..exceptions import VerificationError


class PhoenixRecoveryEngine:
    def restore(self, checkpoint_dir: Path, destination_staging_dir: Path) -> Path:
        ok, reason = verify_checkpoint(checkpoint_dir)
        if not ok:
            raise VerificationError(f"checkpoint verification failed: {reason}")
        source_state = checkpoint_dir / "state"
        if destination_staging_dir.exists():
            shutil.rmtree(destination_staging_dir)
        shutil.copytree(source_state, destination_staging_dir)
        return destination_staging_dir
