import json

import pytest

from jga_uif.checkpoint.manager import CheckpointManager
from jga_uif.checkpoint.verifier import verify_checkpoint
from jga_uif.exceptions import VerificationError
from jga_uif.recovery.phoenix import PhoenixRecoveryEngine


def test_checkpoint_create_verify_restore(tmp_path):
    state = tmp_path / "state"
    state.mkdir()
    (state / "a.txt").write_text("A")
    manager = CheckpointManager(tmp_path / "checkpoints")
    cp = manager.create(state, generation=1, policy_version="1", ledger_position=1)
    assert verify_checkpoint(cp) == (True, "ok")
    out = tmp_path / "restore"
    restored = PhoenixRecoveryEngine().restore(cp, out)
    assert (restored / "a.txt").read_text() == "A"


def test_modified_checkpoint_rejected(tmp_path):
    state = tmp_path / "state"
    state.mkdir()
    (state / "a.txt").write_text("A")
    manager = CheckpointManager(tmp_path / "checkpoints")
    cp = manager.create(state, generation=1, policy_version="1", ledger_position=1)
    data = json.loads((cp / "checkpoint.json").read_text())
    data["checkpoint_digest"] = "forged"
    (cp / "checkpoint.json").write_text(json.dumps(data))
    with pytest.raises(VerificationError):
        PhoenixRecoveryEngine().restore(cp, tmp_path / "restore")
