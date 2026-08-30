#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Resolve the central workflow TOML configuration to JSON."""

import argparse
import json
import sys
from pathlib import Path

# Installed scripts are consumer files, not a location for interpreter caches.
sys.dont_write_bytecode = True

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

try:
    from config_utils import (  # ty: ignore[unresolved-import] -- sibling is added to sys.path above
        ConfigError,
        load_central_config,
    )
except ModuleNotFoundError as error:
    if error.name != "tomllib":
        raise
    sys.stderr.write("error: Python 3.11+ is required (stdlib `tomllib` not found).\n")
    raise SystemExit(3) from None


_MISSING = object()


def extract_key(data, dotted_key: str):
    current = data
    for part in dotted_key.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return _MISSING
    return current


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve the central workflow TOML configuration.")
    parser.add_argument(
        "--project-root",
        "-p",
        required=True,
        help="Absolute project root containing _agent-workflows/",
    )
    parser.add_argument(
        "--key",
        "-k",
        action="append",
        default=[],
        help="Dotted field path to resolve (repeatable). Omit for full dump.",
    )
    args = parser.parse_args()

    try:
        merged = load_central_config(Path(args.project_root).resolve())
    except ConfigError as error:
        sys.stderr.write(f"error: {error}\n")
        return 1

    output = merged
    if args.key:
        output = {}
        for key in args.key:
            value = extract_key(merged, key)
            if value is not _MISSING:
                output[key] = value
    sys.stdout.write(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
