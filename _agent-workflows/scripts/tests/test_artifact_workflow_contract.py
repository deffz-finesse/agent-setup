from __future__ import annotations

import csv
import sys
from argparse import Namespace
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = PROJECT_ROOT / ".agents" / "skills"
CONFIG_ROOT = PROJECT_ROOT / "_agent-workflows" / "_config"
sys.path.insert(0, str(SCRIPTS_DIR))

import run_state


def skill_text(relative_path: str) -> str:
    return (SKILLS_ROOT / relative_path).read_text(encoding="utf-8")


def test_initiative_start_contract_offers_init_and_blocks_ambiguous_headless() -> None:
    for skill in ("planning/product-brief/SKILL.md", "planning/prd/SKILL.md"):
        content = skill_text(skill)
        assert "core.runs_root" in content
        assert "run_state.py init" in content
        assert "headless" in content.lower()
        assert "blocks" in content.lower()


def test_artifact_producing_skills_bind_to_a_run_phase_and_register_outputs() -> None:
    required_fragments = {
        "planning/product-brief/SKILL.md": (
            "00-discovery/product-brief/",
            "01-research/product-brief/",
            "02-plan/brief.md",
            "add-artifact",
        ),
        "planning/prd/SKILL.md": ("02-plan/prd.md", "add-artifact"),
        "planning/architecture/SKILL.md": ("02-plan/architecture/", "add-artifact"),
        "planning/ux/SKILL.md": ("02-plan/ux/", "add-artifact"),
        "planning/prfaq/SKILL.md": ("02-plan/prfaq/", "add-artifact"),
        "planning/spec/SKILL.md": ("02-plan/spec/", "add-artifact"),
        "planning/create-epics-and-stories/SKILL.md": ("02-plan/epics/", "add-artifact"),
        "planning/sprint-planning/SKILL.md": ("03-slices/sprint-status.yaml", "add-artifact"),
        "delivery/implement/SKILL.md": ("active_slice", "04-implementation/", "run_state.py"),
        "delivery/retrospective/SKILL.md": ("08-retrospective/", "add-artifact"),
        "quality/review/SKILL.md": ("06-review/", "add-artifact"),
        "quality/code-review/SKILL.md": ("06-review/", "add-artifact"),
        "creative/brainstorming/SKILL.md": ("00-discovery/", "add-artifact"),
        "creative/cis-design-thinking/SKILL.md": ("00-discovery/", "add-artifact"),
        "creative/cis-innovation-strategy/SKILL.md": ("00-discovery/", "add-artifact"),
        "creative/cis-problem-solving/SKILL.md": ("00-discovery/", "add-artifact"),
    }
    for skill, fragments in required_fragments.items():
        content = skill_text(skill)
        for fragment in fragments:
            assert fragment in content, f"{fragment!r} missing from {skill}"

    for skill_name in (
        "testarch-atdd",
        "testarch-automate",
        "testarch-ci",
        "testarch-framework",
        "testarch-nfr",
        "testarch-test-design",
        "testarch-test-review",
        "testarch-trace",
    ):
        content = skill_text(f"quality/{skill_name}/SKILL.md")
        assert "05-testing" in content
        assert "add-artifact" in content


def test_quality_outputs_are_target_scoped() -> None:
    output_contracts = (
        "quality/review/customize.toml",
        "quality/code-review/customize.toml",
        "quality/testarch-atdd/workflow.yaml",
        "quality/testarch-automate/workflow.yaml",
        "quality/testarch-nfr/workflow.yaml",
        "quality/testarch-test-design/workflow.yaml",
        "quality/testarch-test-review/workflow.yaml",
        "quality/testarch-trace/workflow.yaml",
        "quality/testarch-atdd/steps-v/step-01-validate.md",
        "quality/testarch-automate/steps-v/step-01-validate.md",
        "quality/testarch-ci/steps-v/step-01-validate.md",
        "quality/testarch-framework/steps-v/step-01-validate.md",
        "quality/testarch-nfr/steps-v/step-01-validate.md",
        "quality/testarch-test-design/steps-v/step-01-validate.md",
        "quality/testarch-test-review/steps-v/step-01-validate.md",
        "quality/testarch-trace/steps-v/step-01-validate.md",
    )
    for contract in output_contracts:
        content = skill_text(contract)
        assert "{target_slug}" in content, f"target slug missing from {contract}"
        if contract.endswith("workflow.yaml"):
            assert "{run_dir}/05-testing" in content


def test_epics_templates_enforce_coarse_sharded_ownership() -> None:
    template_root = SKILLS_ROOT / "planning" / "create-epics-and-stories" / "templates"
    index = (template_root / "epics-template.md").read_text(encoding="utf-8")
    inventory = (template_root / "requirements-inventory-template.md").read_text(encoding="utf-8")
    epic = (template_root / "epic-template.md").read_text(encoding="utf-8")

    assert "requirements-inventory.md" in index
    assert "{{epics_list}}" in index
    assert "{{fr_list}}" not in index
    assert "{{story_title" not in index
    assert "{{fr_list}}" in inventory
    assert "{{requirements_coverage_map}}" in inventory
    assert "{{candidate_increments_N}}" in epic
    assert "{{dependencies_and_risks_N}}" in epic
    assert "Acceptance Criteria" not in epic


def test_progressive_planning_keeps_implementation_evidence_only() -> None:
    lifecycle = (CONFIG_ROOT / "artifact-lifecycle.md").read_text(encoding="utf-8")
    sprint = skill_text("planning/sprint-planning/SKILL.md")
    implement = skill_text("delivery/implement/SKILL.md")

    assert "one coherent commit" in lifecycle
    assert "not a planning or backlog folder" in lifecycle
    assert "must not duplicate slice state" in sprint
    assert "effectful implementation begins" in sprint
    assert "commit-sized" in implement

    # Both commit-completion paths must actually record 04-implementation/
    # evidence after committing, not just describe the policy in prose.
    for step in ("delivery/implement/step-oneshot.md", "delivery/implement/step-05-present.md"):
        content = skill_text(step)
        assert "record-implementation-evidence.md" in content, (
            f"{step} commits without recording 04-implementation/ evidence"
        )


def test_repeated_quality_outputs_keep_distinct_targets_and_register(tmp_path: Path) -> None:
    config = tmp_path / "_agent-workflows" / "_config" / "config.toml"
    config.parent.mkdir(parents=True)
    config.write_text('[core]\nruns_root = "{project-root}/.workflow/runs"\n', encoding="utf-8")
    run_state.init_run(
        Namespace(
            project_root=str(tmp_path),
            title="Repeated quality outputs",
            slug="repeated-quality-outputs",
            as_of="2026-08-29",
        )
    )
    run_dir = run_state.run_root(tmp_path, "repeated-quality-outputs")
    templates = (
        "05-testing/test-review-{target_slug}.md",
        "05-testing/nfr-{target_slug}-assessment.md",
        "05-testing/traceability-{target_slug}-matrix.md",
        "05-testing/automation-{target_slug}-summary.md",
        "06-review/review-{target_slug}-2026-08-29.md",
        "06-review/code-review-{target_slug}-2026-08-29.md",
    )
    registered: list[str] = []
    for template in templates:
        for target_slug in ("story-one", "story-two"):
            relative_path = template.replace("{target_slug}", target_slug)
            path = run_dir / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(target_slug, encoding="utf-8")
            run_state.add_artifact(
                Namespace(
                    run_dir=str(run_dir),
                    path=relative_path,
                    type="quality-report",
                    status="current",
                    blocking=False,
                    waived=False,
                    waiver_reason=None,
                )
            )
            registered.append(relative_path)

    run_state.set_phase(Namespace(run_dir=str(run_dir), phase="review", status="active"))
    run_state.validate(Namespace(run_dir=str(run_dir)))
    assert len(registered) == len(set(registered))
    assert all((run_dir / path).read_text(encoding="utf-8") in ("story-one", "story-two") for path in registered)


def test_help_outputs_match_review_and_status_contracts() -> None:
    with (CONFIG_ROOT / "help.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    review = next(row for row in rows if row["module"] == "Core" and row["skill"] == "review")
    assert review["output-location"] == "runs/<run-slug>/06-review/review-<target-slug>-<date>.md"
    code_review = next(row for row in rows if row["module"] == "Workflow" and row["skill"] == "code-review")
    assert code_review["output-location"] == "runs/<run-slug>/06-review/code-review-<target-slug>-<date>.md"
    status = next(
        row
        for row in rows
        if row["module"] == "Workflow" and row["skill"] == "sprint-planning" and row["menu-code"] == "SS"
    )
    assert status["output-location"] == "runs/<run-slug>/03-slices/sprint-status.yaml"


def test_implement_and_code_review_prompt_mirrors_remain_byte_identical() -> None:
    pairs = (
        (
            "delivery/implement/references/deletion-check.md",
            "quality/code-review/references/deletion-check.md",
        ),
        (
            "delivery/implement/review-prompts/edge-case-hunter.md",
            "quality/code-review/review-prompts/edge-case-hunter.md",
        ),
        (
            "delivery/implement/review-prompts/verification-gap.md",
            "quality/code-review/review-prompts/verification-gap.md",
        ),
    )
    for implement_path, code_review_path in pairs:
        assert (SKILLS_ROOT / implement_path).read_bytes() == (SKILLS_ROOT / code_review_path).read_bytes()
