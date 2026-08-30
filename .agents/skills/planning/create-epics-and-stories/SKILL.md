---
name: create-epics-and-stories
description: 'Break requirements into epics and user stories. Use when the user says "create the epics and stories list"'
---

# Create Epics and Stories

**Goal:** Turn the rough plan into a coarse capability roadmap. Capture major
outcomes, ordering, dependencies, and risks without pretending the whole project
can be decomposed into detailed implementation stories up front. Detailed plans
and acceptance criteria are created just in time by sprint planning under
`03-slices/`.

**Your Role:** In addition to your name, communication_style, and persona, you are also a product strategist and technical specifications writer collaborating with a product owner. This is a partnership, not a client-vendor relationship. You bring expertise in requirements decomposition, technical implementation context, and acceptance criteria writing, while the user brings their product vision, user needs, and business requirements. Work together as equals.

## Conventions

- Bare paths (e.g. `steps/step-01-validate-prerequisites.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step toward the overall goal is a self-contained instruction file; adhere to one file at a time, as directed
- **Just-In-Time Loading**: Only 1 current step file will be loaded and followed to completion - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array when a workflow produces a document
- **Progressive Elaboration**: Keep epic shards coarse. Do not add exhaustive
  story lists or commit-level acceptance criteria to every future epic; refine
  only the next horizon into slices during sprint planning.

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, read fully and follow the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter of output files when writing the final output for a specific step
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps

## On Activation

### Step 1: Resolve the Workflow Block

Run: `{skill-root}/customize.toml`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying the same structural merge rules as the resolver:

1. `{skill-root}/customize.toml` — defaults

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code` or `id` replace matching entries and append new entries, and all other arrays append.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context you carry for the rest of the workflow run. Entries prefixed `file:` are paths or globs under `{project-root}` — load the referenced contents as facts. All other entries are facts verbatim.

### Step 4: Load Config

Load config from `{project-root}/_agent-workflows/_config/config.toml` and resolve:

- Use `the user` for greeting
- Resolve exactly one active run from `core.runs_root`; multiple active runs require explicit selection. Bind durable outputs to `<run-dir>/02-plan/epics/` and use `<run-dir>/02-plan/` for plan-input scanning.
- Use `{project_knowledge}` for additional context scanning. A missing active run is a blocker; only `product-brief` or `prd` may initialize a new initiative run.

### Step 5: Greet the User

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. If `activation_steps_prepend` or `activation_steps_append` were non-empty, confirm every entry was executed in order before proceeding. Do not begin the main workflow until all activation steps have been completed.

## Execution

Read fully and follow: `./steps/step-01-validate-prerequisites.md` to begin the workflow. Before writing, create or select `<run-dir>/02-plan/epics/`, initialize `.memlog.md`, and register `index.md`, `requirements-inventory.md`, and each coarse `epic-<NN>-<slug>.md` as `draft` with `run_state.py add-artifact`. At final validation re-register durable files as `current` and advance the run through `run_state.py set-phase`; never write a monolithic `epics.md`, an exhaustive project-wide story inventory, commit-level plans for distant work, or a standalone planning-artifacts root.
