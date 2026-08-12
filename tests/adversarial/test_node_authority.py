from jga_uif.nodes.certification import CertificationNode
from jga_uif.nodes.defender import DefenderNode
from jga_uif.nodes.hunter import HunterNode
from jga_uif.nodes.repair import RepairNode


def test_hunter_only_detects():
    hunter = HunterNode()
    assert hunter.detect({"anomaly": True})
    assert not hasattr(hunter, "certify")
    assert not hasattr(hunter, "repair")


def test_repair_cannot_self_certify():
    repair = RepairNode()
    assert repair.propose_restore("cp-1") == "cp-1"
    assert not hasattr(repair, "certify")


def test_defender_quarantine_only():
    defender = DefenderNode()
    assert defender.quarantine("id1") == "quarantined:id1"
    assert not hasattr(defender, "delete_evidence")


def test_certification_node_no_mutation_method():
    cert = CertificationNode()
    assert cert.certify(True)
    assert not hasattr(cert, "mutate")
