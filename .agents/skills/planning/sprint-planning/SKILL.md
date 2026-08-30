---
name: sprint-planning
description: 'Plan the next short sequence of commit-sized implementation slices, summarize progress, and validate or repair sprint coordination. Use when the user says "run sprint planning", "plan the next sprint", "show sprint status", "validate sprint status", or "fix sprint status"'
---

# Sprint Planning

Plan progressively. The project-wide material in `02-plan/` is a rough map;
it is not a command to detail every future story. Select the next useful
horizon and plan only a short ordered set of coordinated implementation slices.
Each slice has one atomic goal and should normally produce one coherent commit.
A sprint or branch may contain several slices.

## On activation

1. Resolve `customize.toml`, execute activation prepend steps, and load persistent
   facts.
2. Resolve exactly one active run from `core.runs_root`. Multiple active runs
   require explicit selection; no active run is a blocker.
3. Bind the rough plan to `{run_dir}/02-plan/`, coordination state to
   `{run_dir}/03-slices/sprint-status.yaml`, candidate work to
   `{run_dir}/03-slices/backlog.md`, and slice folders to
   `{run_dir}/03-slices/<NNN-slug>/`.
4. Detect the intent and load only its reference:
   - readiness or full planning: `references/readiness-gate.md`
   - full planning after a pass: `references/generate-tracking.md`
   - status: `references/status-view.md`
   - validate: `references/validate.md`
   - fix: `references/fix-sprint-status.md`
5. Execute activation append steps.

## Invariants

- Do not populate `04-implementation/`; it receives artifacts only after
  effectful implementation begins.
- Do not derive a project-wide story queue from every epic.
- Do not prewrite acceptance criteria for distant work.
- If two parts could be reviewed, reverted, or shipped independently, split
  them into different slices.
- Create accepted slices with `run_state.py add-slice`, write focused `plan.md`
  and `acceptance.md`, and register all durable files with `run_state.py
  add-artifact`.
- `slice.yaml` owns each slice's status. `sprint-status.yaml` owns only the
  sprint goal and ordered slice membership; it must not duplicate slice state.

## Headless mode

Do not guess priorities, scope boundaries, or missing acceptance decisions.
Return `blocked` with the ambiguity. Otherwise return JSON naming the sprint
status file and created or selected slice IDs.

## On completion

Validate `sprint-status.yaml`, set the run phase to `slice-planning`, and follow
the resolved `workflow.on_complete` instruction when non-empty.
