import pytest

from jga_uif.exceptions import VerificationError
from jga_uif.ingress.gate import IngressGate


def test_ingress_stages_data():
    gate = IngressGate(max_bytes=128)
    submission = gate.receive(b"abc", {"path": "safe/file.txt"})
    assert submission.transaction_id
    assert submission.payload == b"abc"


def test_oversized_input_rejected():
    gate = IngressGate(max_bytes=2)
    with pytest.raises(VerificationError):
        gate.receive(b"abc", {"path": "safe/file.txt"})


def test_path_traversal_rejected():
    gate = IngressGate(max_bytes=128)
    with pytest.raises(VerificationError):
        gate.receive(b"abc", {"path": "../escape"})
