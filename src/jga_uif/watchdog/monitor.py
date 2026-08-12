from __future__ import annotations

from pathlib import Path

from ..ledger.verifier import verify_anchor


class WatchdogMonitor:
    def classify(self, ledger_path: Path, anchor_path: Path) -> str:
        ok, _ = verify_anchor(ledger_path, anchor_path)
        return "GREEN" if ok else "RED"
