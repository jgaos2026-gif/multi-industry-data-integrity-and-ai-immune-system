from __future__ import annotations

import argparse
from pathlib import Path

from .checkpoint.verifier import verify_checkpoint


def main() -> int:
    parser = argparse.ArgumentParser(prog="jga-uif")
    parser.add_argument("verify_checkpoint", nargs="?")
    parser.add_argument("--path", type=Path)
    args = parser.parse_args()
    if args.verify_checkpoint and args.path:
        ok, reason = verify_checkpoint(args.path)
        print({"ok": ok, "reason": reason})
        return 0 if ok else 1
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
