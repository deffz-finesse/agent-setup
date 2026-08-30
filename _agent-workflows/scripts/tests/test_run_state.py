from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SCRIPTS_DIR.parents[1]
RUN_STATE = SCRIPTS_DIR / "run_state.py"
sys.path.insert(0, str(SCRIPTS_DIR))

import run_state


def write_config(project_root: Path, runs_root: str = "{project-root}/.workflow/runs") -> None:
    config = project_root / "_agent-workflows" / "_config" / "config.toml"
    config.parent.mkdir(parents=True)
    config.write_text(f"[core]\nruns_root = \"{runs_root}\"\n", encoding="utf-8")


def run_cli(project_root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUN_STATE), *arguments],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )


def init_run(project_root: Path, title: str = "Round trip") -> Path:
    result = run_cli(
        project_root,
        "init",
        "--project-root",
        str(project_root),
        "--title",
        title,
        "--as-of",
        "2026-08-29",
    )
    assert result.returncode == 0, result.stderr
    return project_root / ".workflow" / "runs" / run_state.slugify(title)


def add_artifact(
    project_root: Path,
    run_dir: Path,
    path: str,
    *,
    status: str = "current",
    **flags: str,
) -> subprocess.CompletedProcess[str]:
    arguments = [
        "add-artifact",
        "--run-dir",
        str(run_dir),
        "--path",
        path,
        "--type",
        "test-fixture",
        "--status",
        status,
    ]
    for key, value in flags.items():
        arguments.extend([f"--{key.replace('_', '-')}", value])
    return run_cli(project_root, *arguments)


def test_run_root_uses_configured_runs_root(tmp_path: Path) -> None:
    write_config(tmp_path, "{project-root}/.custom/runs")

    assert run_state.run_root(tmp_path, "A Named Run") == tmp_path / ".custom" / "runs" / "a-named-run"


def test_cli_init_add_slice_add_artifact_set_phase_validate_round_trip(tmp_path: Path) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path)

    slice_result = run_cli(
        tmp_path,
        "add-slice",
        "--run-dir",
        str(run_dir),
        "--number",
        "1",
        "--title",
        "A slice",
    )
    assert slice_result.returncode == 0, slice_result.stderr
    slice_dir = run_dir / "03-slices" / "001-a-slice"
    artifact = "03-slices/001-a-slice/plan.md"
    registered = add_artifact(tmp_path, run_dir, artifact)
    assert registered.returncode == 0, registered.stderr

    phase_result = run_cli(tmp_path, "set-phase", "--run-dir", str(run_dir), "--phase", "slice-planning")
    assert phase_result.returncode == 0, phase_result.stderr
    assert "Phase: slice-planning" in (run_dir / "README.md").read_text(encoding="utf-8")

    validated = run_cli(tmp_path, "validate", "--run-dir", str(run_dir))
    assert validated.returncode == 0, validated.stderr
    manifest = run_state.read_yaml(run_dir / "run.yaml")
    assert manifest["active_slice"] == "001-a-slice"
    assert manifest["artifacts"] == [{"path": artifact, "type": "test-fixture", "status": "current"}]
    assert slice_dir.is_dir()


def test_draft_later_phase_is_allowed_but_current_requires_phase_advance(tmp_path: Path) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path)
    report = run_dir / "06-review" / "draft.md"
    report.write_text("draft", encoding="utf-8")

    draft = add_artifact(tmp_path, run_dir, "06-review/draft.md", status="draft")
    assert draft.returncode == 0, draft.stderr
    assert run_cli(tmp_path, "validate", "--run-dir", str(run_dir)).returncode == 0


def test_later_slice_does_not_replace_active_slice_without_explicit_activation(tmp_path: Path) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path)
    first = run_cli(
        tmp_path,
        "add-slice",
        "--run-dir",
        str(run_dir),
        "--number",
        "0",
        "--title",
        "First commit",
    )
    assert first.returncode == 0, first.stderr
    second = run_cli(
        tmp_path,
        "add-slice",
        "--run-dir",
        str(run_dir),
        "--number",
        "1",
        "--title",
        "Second commit",
    )
    assert second.returncode == 0, second.stderr
    assert run_state.read_yaml(run_dir / "run.yaml")["active_slice"] == "000-first-commit"

    activated = run_cli(
        tmp_path,
        "set-active-slice",
        "--run-dir",
        str(run_dir),
        "--slice-id",
        "001-second-commit",
    )
    assert activated.returncode == 0, activated.stderr
    assert run_state.read_yaml(run_dir / "run.yaml")["active_slice"] == "001-second-commit"


def test_set_slice_status_updates_canonical_slice_state(tmp_path: Path) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path)
    result = run_cli(
        tmp_path,
        "add-slice",
        "--run-dir",
        str(run_dir),
        "--number",
        "0",
        "--title",
        "Atomic commit",
    )
    assert result.returncode == 0, result.stderr

    changed = run_cli(
        tmp_path,
        "set-slice-status",
        "--run-dir",
        str(run_dir),
        "--slice-id",
        "000-atomic-commit",
        "--status",
        "in-progress",
    )
    assert changed.returncode == 0, changed.stderr
    state = run_state.read_yaml(run_dir / "03-slices" / "000-atomic-commit" / "slice.yaml")
    assert state["status"] == "in-progress"


def test_move_and_remove_artifact_update_manifest_without_deleting_files(tmp_path: Path) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path)
    source = run_dir / "02-plan" / "misclassified.md"
    source.write_text("planning", encoding="utf-8")
    registered = add_artifact(tmp_path, run_dir, "02-plan/misclassified.md")
    assert registered.returncode == 0, registered.stderr
    destination = run_dir / "01-research" / "evidence.md"
    source.rename(destination)

    moved = run_cli(
        tmp_path,
        "move-artifact",
        "--run-dir",
        str(run_dir),
        "--from-path",
        "02-plan/misclassified.md",
        "--to-path",
        "01-research/evidence.md",
    )
    assert moved.returncode == 0, moved.stderr
    assert destination.is_file()
    assert run_state.read_yaml(run_dir / "run.yaml")["artifacts"][0]["path"] == (
        "01-research/evidence.md"
    )

    removed = run_cli(
        tmp_path,
        "remove-artifact",
        "--run-dir",
        str(run_dir),
        "--path",
        "01-research/evidence.md",
    )
    assert removed.returncode == 0, removed.stderr
    assert destination.is_file()
    assert run_state.read_yaml(run_dir / "run.yaml")["artifacts"] == []

    (run_dir / "06-review" / "draft.md").parent.mkdir(parents=True, exist_ok=True)
    (run_dir / "06-review" / "draft.md").write_text("review", encoding="utf-8")
    current = add_artifact(tmp_path, run_dir, "06-review/draft.md")
    assert current.returncode == 0, current.stderr
    blocked = run_cli(tmp_path, "validate", "--run-dir", str(run_dir))
    assert blocked.returncode != 0
    assert "phase" in blocked.stderr

    advanced = run_cli(tmp_path, "set-phase", "--run-dir", str(run_dir), "--phase", "review")
    assert advanced.returncode == 0, advanced.stderr
    assert run_cli(tmp_path, "validate", "--run-dir", str(run_dir)).returncode == 0


def test_blocking_artifact_blocks_later_registration_until_waived(tmp_path: Path) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path)
    blocker = run_dir / "02-plan" / "open-finding.md"
    blocker.write_text("open", encoding="utf-8")
    first = run_cli(
        tmp_path,
        "add-artifact",
        "--run-dir",
        str(run_dir),
        "--path",
        "02-plan/open-finding.md",
        "--type",
        "finding",
        "--blocking",
    )
    assert first.returncode == 0, first.stderr
    slice_result = run_cli(
        tmp_path,
        "add-slice",
        "--run-dir",
        str(run_dir),
        "--number",
        "1",
        "--title",
        "Later slice",
    )
    assert slice_result.returncode == 0, slice_result.stderr
    later = add_artifact(tmp_path, run_dir, "03-slices/001-later-slice/plan.md")
    assert later.returncode != 0
    assert "blocking finding" in later.stderr

    waived = run_cli(
        tmp_path,
        "add-artifact",
        "--run-dir",
        str(run_dir),
        "--path",
        "02-plan/open-finding.md",
        "--type",
        "finding",
        "--status",
        "current",
        "--blocking",
        "--waived",
        "--waiver-reason",
        "accepted for this migration fixture",
    )
    assert waived.returncode == 0, waived.stderr
    later = add_artifact(tmp_path, run_dir, "03-slices/001-later-slice/plan.md")
    assert later.returncode == 0, later.stderr
    advanced = run_cli(tmp_path, "set-phase", "--run-dir", str(run_dir), "--phase", "slice-planning")
    assert advanced.returncode == 0, advanced.stderr
    assert run_cli(tmp_path, "validate", "--run-dir", str(run_dir)).returncode == 0


@pytest.mark.parametrize(
    "unsafe_path",
    ["../escape.md", "/tmp/absolute.md", "09-release/future.md", "02-plan/../escape.md", r"02-plan\escape.md"],
)
def test_add_artifact_rejects_unsafe_or_unknown_paths(tmp_path: Path, unsafe_path: str) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path)

    result = add_artifact(tmp_path, run_dir, unsafe_path)

    assert result.returncode != 0


def test_add_artifact_rejects_missing_file_at_registration(tmp_path: Path) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path)

    result = add_artifact(tmp_path, run_dir, "02-plan/missing.md")

    assert result.returncode != 0
    assert "does not exist" in result.stderr
    assert run_state.read_yaml(run_dir / "run.yaml")["artifacts"] == []


def test_validate_rejects_duplicate_manifest_paths(tmp_path: Path) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path)
    artifact = run_dir / "00-discovery" / "note.md"
    artifact.write_text("note", encoding="utf-8")
    registered = add_artifact(tmp_path, run_dir, "00-discovery/note.md")
    assert registered.returncode == 0, registered.stderr
    manifest = run_state.read_yaml(run_dir / "run.yaml")
    manifest["artifacts"].append(dict(manifest["artifacts"][0]))
    run_state.write_yaml(run_dir / "run.yaml", manifest)

    result = run_cli(tmp_path, "validate", "--run-dir", str(run_dir))

    assert result.returncode != 0
    assert "duplicate artifact path" in result.stderr


def test_validate_rejects_readme_phase_drift(tmp_path: Path) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path)
    (run_dir / "README.md").write_text("# Round trip\n\nPhase: review\n", encoding="utf-8")

    result = run_cli(tmp_path, "validate", "--run-dir", str(run_dir))

    assert result.returncode != 0
    assert "README.md phase" in result.stderr


def test_migrated_fixture_phase_files_register_once_and_validate(tmp_path: Path) -> None:
    write_config(tmp_path)
    run_dir = init_run(tmp_path, "Migrated fixture")
    slice_result = run_cli(
        tmp_path,
        "add-slice",
        "--run-dir",
        str(run_dir),
        "--number",
        "2",
        "--title",
        "Fixture slice",
    )
    assert slice_result.returncode == 0, slice_result.stderr
    phase_files = {
        "00-discovery/notes.md": "discovery",
        "01-research/sources.md": "research",
        "02-plan/spec.md": "plan",
        "03-slices/002-fixture-slice/plan.md": "slice",
        "04-implementation/records.md": "implementation",
    }
    for relative_path, content in phase_files.items():
        path = run_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        result = add_artifact(tmp_path, run_dir, relative_path)
        assert result.returncode == 0, result.stderr

    phase_result = run_cli(tmp_path, "set-phase", "--run-dir", str(run_dir), "--phase", "implementation")
    assert phase_result.returncode == 0, phase_result.stderr
    validated = run_cli(tmp_path, "validate", "--run-dir", str(run_dir))
    assert validated.returncode == 0, validated.stderr
    manifest = run_state.read_yaml(run_dir / "run.yaml")
    registered_paths = [entry["path"] for entry in manifest["artifacts"]]
    assert sorted(registered_paths) == sorted(phase_files)
    assert len(registered_paths) == len(set(registered_paths))
