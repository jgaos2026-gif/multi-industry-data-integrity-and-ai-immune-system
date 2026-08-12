from jga_uif.verification.triple_verify import TripleVerificationEngine


def test_triple_verify_success():
    engine = TripleVerificationEngine(allowed_sources={"local"})
    payload = b"payload"
    metadata = {"transaction_id": "tx-1", "sequence": 1, "source": "local", "nonce": "nonce-123456"}
    _, decision = engine.run(payload, metadata)
    assert decision.approved


def test_replay_nonce_rejected():
    engine = TripleVerificationEngine(allowed_sources={"local"})
    payload = b"payload"
    metadata = {"transaction_id": "tx-1", "sequence": 1, "source": "local", "nonce": "nonce-123456"}
    _, first = engine.run(payload, metadata)
    _, second = engine.run(payload, {**metadata, "transaction_id": "tx-2"})
    assert first.approved
    assert not second.approved
