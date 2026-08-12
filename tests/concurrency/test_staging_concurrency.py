from concurrent.futures import ThreadPoolExecutor

from jga_uif.staging.store import StagingStore


def test_10_concurrent_writers(tmp_path):
    store = StagingStore(tmp_path / "staging")

    def writer(i: int):
        return store.stage(f"tx-{i}", f"payload-{i}".encode())

    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(writer, range(10)))
    assert len(results) == 10
    assert len({r.path for r in results}) == 10


def test_100_concurrent_writers(tmp_path):
    store = StagingStore(tmp_path / "staging")

    def writer(i: int):
        return store.stage(f"tx-{i}", f"payload-{i}".encode())

    with ThreadPoolExecutor(max_workers=20) as ex:
        results = list(ex.map(writer, range(100)))
    assert len(results) == 100
    assert all(r.path.exists() for r in results)
