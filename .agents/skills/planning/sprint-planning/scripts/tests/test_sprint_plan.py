from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ruamel.yaml import YAML

SCRIPT = Path(__file__).resolve().parents[1] / "sprint_plan.py"


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        YAML().dump(data, stream)


def create_slice(root: Path, slice_id: str, *, status: str = "planned", depends_on=None) -> None:
    write_yaml(
        root / slice_id / "slice.yaml",
        {
            "schema_version": "1.0",
            "slice_id": slice_id,
            "title": slice_id,
            "status": status,
            "depends_on": depends_on or [],
        },
    )


def run(*arguments: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_generate_validate_and_status_short_slice_sequence(tmp_path: Path) -> None:
    slices = tmp_path / "03-slices"
    create_slice(slices, "000-foundation")
    create_slice(slices, "001-binaries", depends_on=["000-foundation"])
    status_file = slices / "sprint-status.yaml"

    generated = run(
        "generate",
        "--status-file",
        str(status_file),
        "--sprint-id",
        "sprint-001",
        "--title",
        "Foundation",
        "--goal",
        "Establish the workspace",
        "--slice",
        "000-foundation",
        "--slice",
        "001-binaries",
        "--date",
        "2026-08-29T12:00:00Z",
    )
    assert generated["ok"] is True

    validated = run("validate", "--status-file", str(status_file))
    assert validated["valid"] is True
    assert [item["slice_id"] for item in validated["slices"]] == [
        "000-foundation",
        "001-binaries",
    ]

    status = run("status", "--status-file", str(status_file))
    assert status["next_slice"] == "000-foundation"


def test_validate_rejects_missing_duplicate_or_misordered_slices(tmp_path: Path) -> None:
    slices = tmp_path / "03-slices"
    create_slice(slices, "001-binaries", depends_on=["000-foundation"])
    status_file = slices / "sprint-status.yaml"
    write_yaml(
        status_file,
        {
            "schema_version": "1.0",
            "sprint_id": "sprint-001",
            "title": "Broken",
            "goal": "Demonstrate validation",
            "created_at": "2026-08-29T12:00:00Z",
            "updated_at": "2026-08-29T12:00:00Z",
            "slice_order": ["001-binaries", "001-binaries", "999-missing"],
        },
    )

    report = run("validate", "--status-file", str(status_file))

    assert report["valid"] is False
    assert any("duplicate" in problem for problem in report["problems"])
    assert any("must appear earlier" in problem for problem in report["problems"])
    assert any("999-missing" in problem for problem in report["problems"])


def test_status_reads_slice_yaml_as_the_status_authority(tmp_path: Path) -> None:
    slices = tmp_path / "03-slices"
    create_slice(slices, "000-foundation", status="done")
    create_slice(slices, "001-binaries", status="in-progress", depends_on=["000-foundation"])
    status_file = slices / "sprint-status.yaml"
    write_yaml(
        status_file,
        {
            "schema_version": "1.0",
            "sprint_id": "sprint-001",
            "title": "Foundation",
            "goal": "Establish the workspace",
            "created_at": "2026-08-29T12:00:00Z",
            "updated_at": "2026-08-29T12:00:00Z",
            "slice_order": ["000-foundation", "001-binaries"],
        },
    )

    report = run("status", "--status-file", str(status_file))

    assert report["next_slice"] == "001-binaries"
    assert [item["status"] for item in report["slices"]] == ["done", "in-progress"]
