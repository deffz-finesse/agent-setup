#!/usr/bin/env python3
"""Create and validate the user-facing project-run artifact workspace."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

from ruamel.yaml import YAML

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from config_utils import central_path

PHASES = (
    "discovery",
    "research",
    "overall-plan",
    "slice-planning",
    "implementation",
    "testing",
    "review",
    "release",
    "retrospective",
    "complete",
)
STATUSES = ("active", "blocked", "paused", "complete")
SLICE_STATUSES = ("planned", "in-progress", "testing", "in-review", "done", "blocked")
ARTIFACT_STATUSES = ("draft", "current")

# Maps a run artifact's leading path segment to the phase that owns it, so
# artifact placement can be checked against `run.yaml`'s recorded phase and
# against any unresolved blocking finding.
DIR_PHASES = {
    "00-discovery": "discovery",
    "01-research": "research",
    "02-plan": "overall-plan",
    "03-slices": "slice-planning",
    "04-implementation": "implementation",
    "05-testing": "testing",
    "06-review": "review",
    "07-release": "release",
    "08-retrospective": "retrospective",
}


def now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("slug must contain at least one letter or number")
    return slug


def yaml() -> YAML:
    parser = YAML()
    parser.default_flow_style = False
    return parser


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        yaml().dump(data, stream)


def sync_readme_phase(root: Path, phase: str) -> None:
    """Keep the human-facing README's phase line in sync with run.yaml."""
    readme = root / "README.md"
    if not readme.is_file():
        return
    content = readme.read_text(encoding="utf-8")
    updated, count = re.subn(r"(?m)^Phase: .*?$", f"Phase: {phase}", content, count=1)
    if count == 0:
        separator = "" if not content or content.endswith("\n") else "\n"
        updated = f"{content}{separator}\nPhase: {phase}\n"
    if updated != content:
        readme.write_text(updated, encoding="utf-8")


def read_yaml(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"missing YAML file: {path}")
    with path.open(encoding="utf-8") as stream:
        data = yaml().load(stream)
    if not isinstance(data, dict):
        raise TypeError(f"YAML root must be a mapping: {path}")
    return dict(data)


def run_root(project_root: Path, slug: str) -> Path:
    configured_root = central_path(project_root.resolve(), "core.runs_root")
    return configured_root / slugify(slug)


def artifact_phase(path: str) -> str | None:
    """The phase that owns an artifact, from its leading path segment; None if unrecognized."""
    first = path.split("/", 1)[0]
    return DIR_PHASES.get(first)


def _artifact_path(path: str) -> Path:
    """Validate and normalize a manifest path as a POSIX-relative path."""
    if not isinstance(path, str) or not path.strip():
        raise ValueError("artifact path must be a non-empty relative path")
    candidate = Path(path)
    if candidate.is_absolute() or "\\" in path:
        raise ValueError(f"artifact path must be relative and use '/': {path}")
    parts = candidate.parts
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise ValueError(f"artifact path contains an unsafe segment: {path}")
    if artifact_phase(path) is None:
        raise ValueError(f"artifact path must begin with a known phase directory: {path}")
    return candidate


def _validate_artifact_entry(entry: dict, *, root: Path | None = None) -> None:
    if not isinstance(entry, dict):
        raise TypeError("run.yaml artifacts must contain mappings")
    path = entry.get("path")
    if not isinstance(path, str):
        raise TypeError("artifact entry is missing a string path")
    _artifact_path(path)
    if not isinstance(entry.get("type"), str) or not entry["type"].strip():
        raise ValueError(f"artifact '{path}' is missing a type")
    if entry.get("status") not in ARTIFACT_STATUSES:
        raise ValueError(
            f"artifact '{path}' has invalid status '{entry.get('status')}', "
            f"expected one of {', '.join(ARTIFACT_STATUSES)}"
        )
    if entry.get("blocking") and entry.get("waived") and not entry.get("waiver_reason"):
        raise ValueError(f"waived blocking artifact '{path}' requires waiver_reason")
    if root is not None and not (root / _artifact_path(path)).is_file():
        raise ValueError(f"registered artifact does not exist: {path}")


def _validate_artifacts(artifacts: object, *, root: Path | None = None) -> list[dict]:
    if artifacts is None:
        return []
    if not isinstance(artifacts, list):
        raise TypeError("run.yaml artifacts must be a list")
    seen: set[str] = set()
    validated: list[dict] = []
    for entry in artifacts:
        _validate_artifact_entry(entry, root=root)
        path = entry["path"]
        if path in seen:
            raise ValueError(f"run.yaml contains duplicate artifact path: {path}")
        seen.add(path)
        validated.append(entry)
    return validated


def phase_index(phase: str) -> int:
    return PHASES.index(phase)


def check_blocking_gates(artifacts: list[dict]) -> None:
    """Refuse a later-phase artifact while an earlier unresolved blocker exists."""
    blockers = [entry for entry in artifacts if entry.get("blocking") and not entry.get("waived")]
    for blocker in blockers:
        blocker_phase = artifact_phase(blocker.get("path", ""))
        if blocker_phase is None:
            continue
        blocker_index = phase_index(blocker_phase)
        for other in artifacts:
            if other is blocker:
                continue
            other_phase = artifact_phase(other.get("path", ""))
            if other_phase is None or phase_index(other_phase) <= blocker_index:
                continue
            raise ValueError(
                f"blocking finding unresolved: '{blocker['path']}' (phase {blocker_phase}) "
                f"blocks later-phase artifact '{other['path']}' (phase {other_phase}). "
                "Resolve the finding and drop --blocking, or re-register it with "
                "--waived and a --waiver-reason."
            )


def init_run(args: argparse.Namespace) -> int:
    slug = slugify(args.slug or args.title)
    root = run_root(Path(args.project_root), slug)
    manifest = root / "run.yaml"
    if manifest.exists():
        raise ValueError(f"run already exists: {manifest}")
    timestamp = now()
    write_yaml(
        manifest,
        {
            "schema_version": "1.0",
            "run_id": slug,
            "title": args.title,
            "slug": slug,
            "phase": "discovery",
            "status": "active",
            "created_at": timestamp,
            "updated_at": timestamp,
            "as_of": args.as_of or timestamp[:10],
            "active_slice": None,
            "branch": None,
            "baseline_commit": None,
            "artifacts": [],
        },
    )
    for name in (
        "00-discovery",
        "01-research",
        "02-plan",
        "03-slices",
        "04-implementation",
        "05-testing",
        "06-review",
        "07-release",
        "08-retrospective",
    ):
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "README.md").write_text(
        f"# {args.title}\n\nPhase: discovery\n\nSee `run.yaml` for machine-readable state.\n",
        encoding="utf-8",
    )
    print(root)
    return 0


def add_slice(args: argparse.Namespace) -> int:
    root = Path(args.run_dir).resolve()
    run = read_yaml(root / "run.yaml")
    slice_slug = slugify(args.slug or args.title)
    slice_id = f"{args.number:03d}-{slice_slug}"
    destination = root / "03-slices" / slice_id
    if (destination / "slice.yaml").exists():
        raise ValueError(f"slice already exists: {destination / 'slice.yaml'}")
    timestamp = now()
    write_yaml(
        destination / "slice.yaml",
        {
            "schema_version": "1.0",
            "slice_id": slice_id,
            "title": args.title,
            "slug": slice_slug,
            "status": "planned",
            "created_at": timestamp,
            "updated_at": timestamp,
            "acceptance": [],
            "artifacts": [],
        },
    )
    (destination / "plan.md").write_text(f"# {args.title}\n", encoding="utf-8")
    (destination / "acceptance.md").write_text(f"# Acceptance: {args.title}\n", encoding="utf-8")
    # Planning a later slice must not silently steal focus from the current
    # implementation. The first slice becomes active automatically; later
    # activation is explicit.
    if run.get("active_slice") is None or args.activate:
        run["active_slice"] = slice_id
    run["updated_at"] = timestamp
    write_yaml(root / "run.yaml", run)
    print(destination)
    return 0


def set_active_slice(args: argparse.Namespace) -> int:
    root = Path(args.run_dir).resolve()
    manifest = root / "run.yaml"
    run = read_yaml(manifest)
    slice_file = root / "03-slices" / args.slice_id / "slice.yaml"
    state = read_yaml(slice_file)
    if state.get("slice_id") != args.slice_id:
        raise ValueError(f"slice id does not match its directory: {slice_file}")
    run["active_slice"] = args.slice_id
    run["updated_at"] = now()
    write_yaml(manifest, run)
    print(args.slice_id)
    return 0


def set_slice_status(args: argparse.Namespace) -> int:
    if args.status not in SLICE_STATUSES:
        raise ValueError(f"invalid slice status: {args.status}")
    root = Path(args.run_dir).resolve()
    slice_file = root / "03-slices" / args.slice_id / "slice.yaml"
    state = read_yaml(slice_file)
    if state.get("slice_id") != args.slice_id:
        raise ValueError(f"slice id does not match its directory: {slice_file}")
    state["status"] = args.status
    state["updated_at"] = now()
    write_yaml(slice_file, state)
    print(f"{args.slice_id}: {args.status}")
    return 0


def add_artifact(args: argparse.Namespace) -> int:
    """Register a run artifact, or re-register (upsert) an existing path — e.g. to
    flip its status, or to attach --waived/--waiver-reason to a blocking entry so
    later-phase artifacts can proceed past it."""
    root = Path(args.run_dir).resolve()
    manifest = root / "run.yaml"
    run = read_yaml(manifest)
    artifacts = run.setdefault("artifacts", [])
    _artifact_path(args.path)
    if args.status not in ARTIFACT_STATUSES:
        raise ValueError(
            f"invalid artifact status '{args.status}', expected one of {', '.join(ARTIFACT_STATUSES)}"
        )
    if args.waived and not args.waiver_reason:
        raise ValueError("--waived requires --waiver-reason")
    entry = {"path": args.path, "type": args.type, "status": args.status}
    if args.blocking:
        entry["blocking"] = True
    if args.waived:
        entry["waived"] = True
        entry["waiver_reason"] = args.waiver_reason
    _validate_artifact_entry(entry, root=root)
    existing_index = next((i for i, item in enumerate(artifacts) if item.get("path") == args.path), None)
    prospective = list(artifacts)
    if existing_index is None:
        prospective.append(entry)
    else:
        prospective[existing_index] = entry
    check_blocking_gates(prospective)
    if existing_index is None:
        artifacts.append(entry)
    else:
        artifacts[existing_index] = entry
    run["updated_at"] = now()
    write_yaml(manifest, run)
    print(args.path)
    return 0


def remove_artifact(args: argparse.Namespace) -> int:
    """Remove one manifest entry without deleting its file."""
    root = Path(args.run_dir).resolve()
    manifest = root / "run.yaml"
    run = read_yaml(manifest)
    artifacts = _validate_artifacts(run.get("artifacts"))
    remaining = [entry for entry in artifacts if entry.get("path") != args.path]
    if len(remaining) == len(artifacts) and not args.missing_ok:
        raise ValueError(f"artifact is not registered: {args.path}")
    check_blocking_gates(remaining)
    run["artifacts"] = remaining
    run["updated_at"] = now()
    write_yaml(manifest, run)
    print(args.path)
    return 0


def move_artifact(args: argparse.Namespace) -> int:
    """Update one registered path after the file has been moved on disk."""
    root = Path(args.run_dir).resolve()
    manifest = root / "run.yaml"
    run = read_yaml(manifest)
    artifacts = _validate_artifacts(run.get("artifacts"))
    source_index = next(
        (index for index, entry in enumerate(artifacts) if entry.get("path") == args.from_path),
        None,
    )
    if source_index is None:
        raise ValueError(f"artifact is not registered: {args.from_path}")
    if any(entry.get("path") == args.to_path for entry in artifacts):
        raise ValueError(f"destination artifact is already registered: {args.to_path}")
    _artifact_path(args.to_path)
    if not (root / args.to_path).is_file():
        raise ValueError(f"moved artifact does not exist: {args.to_path}")
    updated = dict(artifacts[source_index])
    updated["path"] = args.to_path
    _validate_artifact_entry(updated, root=root)
    prospective = list(artifacts)
    prospective[source_index] = updated
    check_blocking_gates(prospective)
    run["artifacts"] = prospective
    run["updated_at"] = now()
    write_yaml(manifest, run)
    print(f"{args.from_path} -> {args.to_path}")
    return 0


def set_phase(args: argparse.Namespace) -> int:
    root = Path(args.run_dir).resolve()
    manifest = root / "run.yaml"
    run = read_yaml(manifest)
    if args.phase not in PHASES:
        raise ValueError(f"invalid phase: {args.phase}")
    if args.status not in STATUSES:
        raise ValueError(f"invalid status: {args.status}")
    run["phase"] = args.phase
    run["status"] = args.status
    run["updated_at"] = now()
    write_yaml(manifest, run)
    sync_readme_phase(root, args.phase)
    print(f"{args.phase} ({args.status})")
    return 0


def validate(args: argparse.Namespace) -> int:
    root = Path(args.run_dir).resolve()
    run = read_yaml(root / "run.yaml")
    required = (
        "schema_version",
        "run_id",
        "title",
        "slug",
        "phase",
        "status",
        "created_at",
        "updated_at",
        "as_of",
    )
    missing = [key for key in required if not run.get(key)]
    if missing:
        raise ValueError(f"run.yaml missing required values: {', '.join(missing)}")
    if run["phase"] not in PHASES:
        raise ValueError(f"run.yaml has invalid phase: {run['phase']}")
    if run["status"] not in STATUSES:
        raise ValueError(f"run.yaml has invalid status: {run['status']}")
    active_slice = run.get("active_slice")
    if active_slice is not None:
        slice_file = root / "03-slices" / str(active_slice) / "slice.yaml"
        slice_state = read_yaml(slice_file)
        if slice_state.get("slice_id") != active_slice:
            raise ValueError(f"active_slice does not match its slice.yaml: {active_slice}")
        if slice_state.get("status") not in SLICE_STATUSES:
            raise ValueError(f"active slice has invalid status: {slice_state.get('status')}")
    readme = root / "README.md"
    if readme.is_file():
        readme_match = re.search(r"(?m)^Phase: (.+)$", readme.read_text(encoding="utf-8"))
        if readme_match is None or readme_match.group(1).strip() != run["phase"]:
            raise ValueError(f"README.md phase does not match run.yaml: {run['phase']}")
    artifacts = _validate_artifacts(run.get("artifacts"), root=root)
    check_blocking_gates(artifacts)
    max_index, max_phase = -1, None
    for entry in artifacts:
        # Drafts are intentionally allowed to live in a later phase while a
        # workflow is being authored. Only durable/current artifacts advance
        # the manifest's phase-order invariant.
        if entry.get("status") != "current":
            continue
        entry_phase = artifact_phase(entry.get("path", ""))
        if entry_phase is not None and phase_index(entry_phase) > max_index:
            max_index, max_phase = phase_index(entry_phase), entry_phase
    if max_phase is not None and phase_index(run["phase"]) < max_index:
        raise ValueError(
            f"run.yaml phase is '{run['phase']}' but artifacts exist through '{max_phase}'; "
            "call set-phase to advance it."
        )
    print(f"valid run: {root}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="create a run workspace")
    init.add_argument("--project-root", required=True)
    init.add_argument("--title", required=True)
    init.add_argument("--slug")
    init.add_argument("--as-of")
    init.set_defaults(handler=init_run)

    add = subparsers.add_parser("add-slice", help="add a slice to an existing run")
    add.add_argument("--run-dir", required=True)
    add.add_argument("--number", required=True, type=int)
    add.add_argument("--title", required=True)
    add.add_argument("--slug")
    add.add_argument("--activate", action="store_true")
    add.set_defaults(handler=add_slice)

    active = subparsers.add_parser("set-active-slice", help="select an existing slice explicitly")
    active.add_argument("--run-dir", required=True)
    active.add_argument("--slice-id", required=True)
    active.set_defaults(handler=set_active_slice)

    slice_status = subparsers.add_parser("set-slice-status", help="update one slice's canonical state")
    slice_status.add_argument("--run-dir", required=True)
    slice_status.add_argument("--slice-id", required=True)
    slice_status.add_argument("--status", required=True)
    slice_status.set_defaults(handler=set_slice_status)

    artifact = subparsers.add_parser("add-artifact", help="register a run artifact and enforce phase gates")
    artifact.add_argument("--run-dir", required=True)
    artifact.add_argument("--path", required=True, help="artifact path relative to the run directory")
    artifact.add_argument("--type", required=True)
    artifact.add_argument("--status", default="current")
    artifact.add_argument(
        "--blocking",
        action="store_true",
        help="mark this artifact's findings as blocking any later-phase artifact until resolved or waived",
    )
    artifact.add_argument(
        "--waived",
        action="store_true",
        help="register as an explicitly waived blocker (requires --waiver-reason)",
    )
    artifact.add_argument("--waiver-reason")
    artifact.set_defaults(handler=add_artifact)

    remove = subparsers.add_parser("remove-artifact", help="remove one manifest entry without deleting the file")
    remove.add_argument("--run-dir", required=True)
    remove.add_argument("--path", required=True)
    remove.add_argument("--missing-ok", action="store_true")
    remove.set_defaults(handler=remove_artifact)

    move = subparsers.add_parser("move-artifact", help="update one registered path after moving its file")
    move.add_argument("--run-dir", required=True)
    move.add_argument("--from-path", required=True)
    move.add_argument("--to-path", required=True)
    move.set_defaults(handler=move_artifact)

    phase = subparsers.add_parser("set-phase", help="update run phase and status")
    phase.add_argument("--run-dir", required=True)
    phase.add_argument("--phase", required=True)
    phase.add_argument("--status", default="active")
    phase.set_defaults(handler=set_phase)

    check = subparsers.add_parser("validate", help="validate a run manifest")
    check.add_argument("--run-dir", required=True)
    check.set_defaults(handler=validate)

    args = parser.parse_args()
    try:
        return args.handler(args)
    except (OSError, TypeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
