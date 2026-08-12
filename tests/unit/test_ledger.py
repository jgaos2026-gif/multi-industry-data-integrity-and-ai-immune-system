import json

from jga_uif.ledger.anchor import write_anchor
from jga_uif.ledger.proof_ledger import ProofLedger
from jga_uif.ledger.verifier import verify_anchor, verify_ledger_chain


def test_ledger_and_anchor_verify(tmp_path):
    ledger_path = tmp_path / "ledger.jsonl"
    anchor_path = tmp_path / "anchor.json"
    ledger = ProofLedger(ledger_path)
    ledger.append("stage", "tx-1", "ingress", "system", "d1", "staged", "1")
    ledger.append("verify", "tx-1", "verifier", "system", "d1", "verified", "1")
    write_anchor(ledger_path, anchor_path, generation=1)
    assert verify_ledger_chain(ledger_path) == (True, "ok")
    assert verify_anchor(ledger_path, anchor_path) == (True, "ok")


def test_tampered_ledger_fails(tmp_path):
    ledger_path = tmp_path / "ledger.jsonl"
    anchor_path = tmp_path / "anchor.json"
    ledger = ProofLedger(ledger_path)
    ledger.append("stage", "tx-1", "ingress", "system", "d1", "staged", "1")
    write_anchor(ledger_path, anchor_path, generation=1)
    lines = ledger_path.read_text().splitlines()
    rec = json.loads(lines[0])
    rec["prior_hash"] = "forged"
    lines[0] = json.dumps(rec)
    ledger_path.write_text("\n".join(lines) + "\n")
    ok, _ = verify_ledger_chain(ledger_path)
    assert not ok
