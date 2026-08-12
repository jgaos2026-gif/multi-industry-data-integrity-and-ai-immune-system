from dataclasses import dataclass


@dataclass(frozen=True)
class SovereignStatus:
    sovereign: str
    status: str
    reason: str


def aggregate_status(results: list[SovereignStatus]) -> str:
    if any(r.status == "RED" for r in results):
        return "RED"
    if any(r.status == "AMBER" for r in results):
        return "AMBER"
    return "GREEN"
