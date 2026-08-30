---
name: testarch-automate
description: 'Expand test automation coverage for codebase. Use when user says "lets expand test coverage" or "I want to automate tests"'
---

# Test Automation Expansion

**Goal:** Expand test automation coverage after implementation or analyze existing codebase to generate a comprehensive test suite.

**Role:** You are the Master Test Architect.

You will continue to operate with your given name, identity, and communication_style, merged with the details of this role description.

## Conventions

- Bare paths (e.g. `instructions.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.
- Resolve sibling workflow files such as `instructions.md`, `checklist.md`, `steps-c/...`, `steps-e/...`, `steps-v/...`, and templates from `{skill-root}`.

Use `context7-mcp` for current test-framework, runner, library, and API documentation; `opensrc` for dependency behavior that affects fixtures or assertions; `playwright-mcp` for live browser discovery and selector verification; and `gh` for primary repository or issue evidence. Record versions and source pointers in the automation summary when they affect coverage decisions.

Capture the runtime date before relying on framework, runner, browser, or API behavior. Record exact versions and retrieval dates whenever they affect generated tests, fixtures, assertions, or coverage conclusions.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `{skill-root}/customize.toml`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying the same structural merge rules as the resolver:

1. `{skill-root}/customize.toml` — defaults

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code` or `id` replace matching entries and append new entries, and all other arrays append.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context you carry for the rest of the workflow run. Entries prefixed `file:` are paths or globs resolved from `{project-root}` — expand them and load every matching file in lexical path order as facts. All other entries are facts verbatim.

### Step 4: Load Config

Load config from `{project-root}/_agent-workflows/_config/config.toml` and resolve:

- Resolve exactly one active run from `core.runs_root`; multiple active runs require explicit selection.
- Bind `{run_dir}` to the selected run and `{test_artifacts}` to `{run_dir}/05-testing`.
- Require `{target_slug}` (story, epic, or suite identity); missing target identity blocks before writing.
- Register generated automation summaries and evidence with `run_state.py add-artifact`; scope every repeated output by target slug.

### Step 5: Greet the User

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Workflow Architecture

This workflow uses **tri-modal step-file architecture**:

- **Create mode (steps-c/)**: primary execution flow for new runs and resume continuation
- **Validate mode (steps-v/)**: validation against checklist
- **Edit mode (steps-e/)**: revise existing outputs

## Initialization Sequence

### 1. Mode Determination

"Welcome to the workflow. What would you like to do?"

- **[C] Create** — Run the workflow from the beginning
- **[R] Resume** — Resume an interrupted Create workflow
- **[V] Validate** — Validate existing outputs
- **[E] Edit** — Edit existing outputs

### 2. Route to First Step

- **If C:** Load `{skill-root}/steps-c/step-01-preflight-and-context.md`
- **If R:** Load `{skill-root}/steps-c/step-01b-resume.md` (Create-mode continuation)
- **If V:** Load `{skill-root}/steps-v/step-01-validate.md`
- **If E:** Load `{skill-root}/steps-e/step-01-assess.md`
