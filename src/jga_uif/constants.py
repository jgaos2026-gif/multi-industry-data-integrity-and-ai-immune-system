from pathlib import Path

DEFAULT_POLICY_VERSION = "1.0.0"
DEFAULT_SCHEMA_VERSION = "1.0.0"
DEFAULT_MAX_INGRESS_BYTES = 10 * 1024 * 1024
LEDGER_FILENAME = "proof_ledger.jsonl"
ANCHOR_FILENAME = "ledger_anchor.json"
CHECKPOINTS_DIRNAME = "checkpoints"
QUARANTINE_DIRNAME = "quarantine"
EVIDENCE_DIRNAME = "evidence"
MEMORY_DIRNAME = "memory"
STATE_DIRNAME = "state"
SUPPORTED_RELAYS = {"local", "filesystem", "usb", "email", "cloud", "api", "ai_to_ai", "network"}
PROJECT_ROOT = Path(__file__).resolve().parents[2]
