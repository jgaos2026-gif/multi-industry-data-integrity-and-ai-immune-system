from dataclasses import dataclass


@dataclass(frozen=True)
class HeartbeatSummary:
    liveness: bool
    queue_depth: int
    verification_backlog: int
    recovery_ready: bool
