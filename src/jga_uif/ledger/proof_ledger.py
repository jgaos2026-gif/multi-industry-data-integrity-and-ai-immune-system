from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import UTC, datetime
import json
from pathlib import Path

from ..crypto.hashing import sha256_hex


@dataclass(frozen=True)
class LedgerRecord:
    sequence: int
    timestamp: str
    event_type: str
    transaction_id: str
    component: str
    actor: str
    prior_hash: str
    record_hash: str
    state_digest: str
    evidence_references: list[str]
    reason: str
    policy_version: str


class ProofLedger:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def _read_all(self) -> list[dict]:
        records: list[dict] = []
        for line in self.path.read_text().splitlines():
            if not line.strip():
                continue
            records.append(json.loads(line))
        return records

    def append(self, event_type: str, transaction_id: str, component: str, actor: str, state_digest: str, reason: str, policy_version: str, evidence_references: list[str] | None = None) -> dict:
        records = self._read_all()
        sequence = len(records) + 1
        prior_hash = records[-1]["record_hash"] if records else "GENESIS"
        payload = {
            "sequence": sequence,
            "timestamp": datetime.now(UTC).isoformat(),
            "event_type": event_type,
            "transaction_id": transaction_id,
            "component": component,
            "actor": actor,
            "prior_hash": prior_hash,
            "state_digest": state_digest,
            "evidence_references": evidence_references or [],
            "reason": reason,
            "policy_version": policy_version,
        }
        record_hash = sha256_hex(json.dumps(payload, sort_keys=True).encode())
        record = LedgerRecord(**payload, record_hash=record_hash)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(record), sort_keys=True) + "\n")
        return asdict(record)
