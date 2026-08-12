from __future__ import annotations

import json
from pathlib import Path

from ..crypto.hashing import sha256_hex


def verify_ledger_chain(ledger_path: Path) -> tuple[bool, str]:
    prev = "GENESIS"
    expected_seq = 1
    for raw in ledger_path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError:
            return False, "malformed json"
        if rec.get("sequence") != expected_seq:
            return False, "sequence mismatch"
        payload = {k: rec[k] for k in rec if k != "record_hash"}
        if sha256_hex(json.dumps(payload, sort_keys=True).encode()) != rec.get("record_hash"):
            return False, "record hash mismatch"
        if rec.get("prior_hash") != prev:
            return False, "prior hash mismatch"
        prev = rec["record_hash"]
        expected_seq += 1
    return True, "ok"


def verify_anchor(ledger_path: Path, anchor_path: Path) -> tuple[bool, str]:
    ledger_ok, msg = verify_ledger_chain(ledger_path)
    if not ledger_ok:
        return False, msg
    anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
    content = ledger_path.read_bytes()
    count = len([ln for ln in content.splitlines() if ln.strip()])
    if anchor.get("record_count") != count:
        return False, "record count mismatch"
    if anchor.get("ledger_digest") != sha256_hex(content):
        return False, "ledger digest mismatch"
    if count:
        last = json.loads(content.splitlines()[-1])
        if anchor.get("head_record_hash") != last.get("record_hash"):
            return False, "head hash mismatch"
    return True, "ok"
