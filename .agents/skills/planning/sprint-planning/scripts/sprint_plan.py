#!/usr/bin/env python3
"""Create and inspect a short sprint made of commit-sized run slices."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from ruamel.yaml import YAML

SLICE_STATUSES = {"planned", "in-progress", "testing", "in-review", "done", "blocked"}
REQUIRED_FIELDS = ("schema_version", "sprint_id", "title", "goal", "created_at", "updated_at")


def yaml() -> YAML:
    parser = YAML()
    parser.default_flow_style = False
    return parser


def read_mapping(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"missing file: {path}")
    with path.open(encoding="utf-8") as stream:
        data = yaml().load(stream)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return dict(data)


def atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            yaml().dump(data, stream)
        os.replace(temporary, path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise


def validate_status(path: Path) -> tuple[list[str], list[dict]]:
    problems: list[str] = []
    slices: list[dict] = []
    try:
        sprint = read_mapping(path)
    except (OSError, TypeError, ValueError) as exc:
        return [str(exc)], []

    for field in REQUIRED_FIELDS:
        if not sprint.get(field):
            problems.append(f"missing required key '{field}'")

    order = sprint.get("slice_order")
    if not isinstance(order, list):
        return [*problems, "'slice_order' must be a list"], []
    if len(order) != len(set(map(str, order))):
        problems.append("'slice_order' contains duplicate slice ids")

    known: set[str] = set()
    for raw_slice_id in order:
        slice_id = str(raw_slice_id)
        slice_file = path.parent / slice_id / "slice.yaml"
        try:
            state = read_mapping(slice_file)
        except (OSError, TypeError, ValueError) as exc:
            problems.append(str(exc))
            continue
        if state.get("slice_id") != slice_id:
            problems.append(f"{slice_file}: slice_id does not match directory '{slice_id}'")
        status = state.get("status")
        if status not in SLICE_STATUSES:
            problems.append(f"{slice_file}: invalid status '{status}'")
        dependencies = state.get("depends_on", [])
        if not isinstance(dependencies, list):
            problems.append(f"{slice_file}: depends_on must be a list")
            dependencies = []
        for dependency in dependencies:
            if str(dependency) not in known:
                problems.append(
                    f"{slice_file}: dependency '{dependency}' must appear earlier in slice_order"
                )
        known.add(slice_id)
        slices.append(
            {
                "slice_id": slice_id,
                "title": state.get("title", slice_id),
                "status": status,
                "depends_on": list(map(str, dependencies)),
            }
        )
    return problems, slices


def cmd_generate(args: argparse.Namespace) -> None:
    path = Path(args.status_file)
    timestamp = args.date or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    existing = read_mapping(path) if path.exists() else {}
    data = {
        "schema_version": "1.0",
        "sprint_id": args.sprint_id,
        "title": args.title,
        "goal": args.goal,
        "created_at": existing.get("created_at", timestamp),
        "updated_at": timestamp,
        "slice_order": args.slice or [],
    }
    if not args.dry_run:
        atomic_write(path, data)
    problems, slices = validate_status(path) if not args.dry_run else ([], [])
    print(
        json.dumps(
            {
                "ok": not problems,
                "action": "generate",
                "status_file": str(path),
                "written": not args.dry_run,
                "problems": problems,
                "slices": slices,
            }
        )
    )


def cmd_validate(args: argparse.Namespace) -> None:
    problems, slices = validate_status(Path(args.status_file))
    print(
        json.dumps(
            {
                "ok": True,
                "action": "validate",
                "status_file": args.status_file,
                "valid": not problems,
                "problems": problems,
                "slices": slices,
            }
        )
    )


def cmd_status(args: argparse.Namespace) -> None:
    path = Path(args.status_file)
    problems, slices = validate_status(path)
    sprint = read_mapping(path) if not problems or path.is_file() else {}
    next_slice = next((item["slice_id"] for item in slices if item["status"] != "done"), None)
    print(
        json.dumps(
            {
                "ok": not problems,
                "action": "status",
                "status_file": str(path),
                "sprint_id": sprint.get("sprint_id"),
                "title": sprint.get("title"),
                "goal": sprint.get("goal"),
                "slices": slices,
                "next_slice": next_slice,
                "problems": problems,
            }
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)

    generate = commands.add_parser("generate")
    generate.add_argument("--status-file", required=True)
    generate.add_argument("--sprint-id", required=True)
    generate.add_argument("--title", required=True)
    generate.add_argument("--goal", required=True)
    generate.add_argument("--slice", action="append")
    generate.add_argument("--date")
    generate.add_argument("--dry-run", action="store_true")
    generate.set_defaults(func=cmd_generate)

    status = commands.add_parser("status")
    status.add_argument("--status-file", required=True)
    status.add_argument("--date")
    status.set_defaults(func=cmd_status)

    validate = commands.add_parser("validate")
    validate.add_argument("--status-file", required=True)
    validate.set_defaults(func=cmd_validate)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
